"""Tests for scripts.aggregate_benchmark module."""

import json

import pytest

from scripts.aggregate_benchmark import generate_benchmark, load_run_results, normalize_expectations


class TestLoadRunResults:
    def test_rejects_mixed_workspace_and_legacy_layouts(self, tmp_path):
        workspace_eval = tmp_path / "eval-0" / "with_skill" / "run-1"
        workspace_eval.mkdir(parents=True)
        (workspace_eval / "grading.json").write_text(
            '{"summary":{"pass_rate":1.0,"passed":1,"failed":0,"total":1}}'
        )

        legacy_eval = tmp_path / "runs" / "eval-0" / "with_skill" / "run-1"
        legacy_eval.mkdir(parents=True)
        (legacy_eval / "grading.json").write_text(
            '{"summary":{"pass_rate":1.0,"passed":1,"failed":0,"total":1}}'
        )

        with pytest.raises(ValueError, match="Both workspace and legacy benchmark layouts exist"):
            load_run_results(tmp_path)

    def test_legacy_assertions_are_normalized_to_expectations(self, tmp_path):
        run_dir = tmp_path / "eval-0" / "with_skill" / "run-1"
        run_dir.mkdir(parents=True)
        (run_dir / "grading.json").write_text(
            """
            {
              "summary": {"pass_rate": 1.0, "passed": 1, "failed": 0, "total": 1},
              "assertions": [
                {"text": "Output includes summary", "passed": true, "evidence": "summary.md"}
              ]
            }
            """
        )

        benchmark = generate_benchmark(tmp_path, skill_name="test-skill")

        assert benchmark["runs"][0]["expectations"] == [
            {"text": "Output includes summary", "passed": True, "evidence": "summary.md"}
        ]
        assert "assertions" not in benchmark["runs"][0]

    def test_expectations_take_precedence_over_legacy_assertions(self):
        grading = {
            "expectations": [{"text": "canonical", "passed": True}],
            "assertions": [{"text": "legacy", "passed": False}],
        }

        assert normalize_expectations(grading) == [{"text": "canonical", "passed": True}]


class TestDeltaOrientation:
    def _write_grading(self, tmp_path, config, pass_rate):
        run_dir = tmp_path / "eval-0" / config / "run-1"
        run_dir.mkdir(parents=True)
        (run_dir / "grading.json").write_text(
            json.dumps({"summary": {"pass_rate": pass_rate, "passed": 1, "failed": 0, "total": 1}})
        )

    def test_known_baseline_name_is_moved_to_baseline_position(self, tmp_path):
        # Alphabetical scan order would make "baseline" the primary and flip the sign
        self._write_grading(tmp_path, "baseline", 0.5)
        self._write_grading(tmp_path, "skill", 1.0)

        benchmark = generate_benchmark(tmp_path, skill_name="test-skill")
        delta = benchmark["run_summary"]["delta"]

        assert delta["comparison"] == "skill - baseline"
        assert delta["pass_rate"] == "+0.50"

    def test_with_without_skill_orientation_is_stable(self, tmp_path):
        self._write_grading(tmp_path, "with_skill", 1.0)
        self._write_grading(tmp_path, "without_skill", 0.5)

        benchmark = generate_benchmark(tmp_path, skill_name="test-skill")
        delta = benchmark["run_summary"]["delta"]

        assert delta["comparison"] == "with_skill - without_skill"
        assert delta["pass_rate"] == "+0.50"

    def test_baseline_takes_second_slot_with_more_than_two_configs(self, tmp_path):
        # Alphabetical scan order is alt, baseline, skill; the delta must
        # still compare a primary against the recognized baseline.
        self._write_grading(tmp_path, "alt", 0.8)
        self._write_grading(tmp_path, "baseline", 0.5)
        self._write_grading(tmp_path, "skill", 1.0)

        benchmark = generate_benchmark(tmp_path, skill_name="test-skill")
        delta = benchmark["run_summary"]["delta"]

        assert delta["comparison"] == "alt - baseline"
        assert delta["pass_rate"] == "+0.30"

    def test_runs_per_configuration_is_derived_from_data(self, tmp_path):
        for run_number in (1, 2):
            run_dir = tmp_path / "eval-0" / "with_skill" / f"run-{run_number}"
            run_dir.mkdir(parents=True)
            (run_dir / "grading.json").write_text(
                json.dumps({"summary": {"pass_rate": 1.0, "passed": 1, "failed": 0, "total": 1}})
            )

        benchmark = generate_benchmark(tmp_path, skill_name="test-skill")

        assert benchmark["metadata"]["runs_per_configuration"] == 2
