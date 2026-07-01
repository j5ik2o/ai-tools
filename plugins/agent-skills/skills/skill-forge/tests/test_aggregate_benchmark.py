"""Tests for scripts.aggregate_benchmark module."""

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
