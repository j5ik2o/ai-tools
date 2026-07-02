"""Tests for scripts.run_eval aggregation, dispatch, and masking."""

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest.mock import patch

from scripts.run_eval import run_eval, run_single_query
from scripts.utils import CLI_CLAUDE, CLI_CODEX


class TestRunSingleQueryDispatch:
    def test_dispatches_to_claude(self):
        with patch("scripts.run_eval.run_single_query_claude", return_value="triggered") as mock:
            result = run_single_query(
                "test query", "skill", "desc", 10, "/tmp", cli_type=CLI_CLAUDE,
            )
            assert result == "triggered"
            mock.assert_called_once()

    def test_dispatches_to_codex(self):
        with patch("scripts.run_eval.run_single_query_codex", return_value="completed") as mock:
            result = run_single_query(
                "test query", "skill", "desc", 10, "/tmp", cli_type=CLI_CODEX,
            )
            assert result == "completed"
            mock.assert_called_once()

    def test_passes_cli_command_to_claude(self):
        with patch("scripts.run_eval.run_single_query_claude", return_value="triggered") as mock:
            run_single_query(
                "q", "s", "d", 10, "/tmp",
                cli_type=CLI_CLAUDE, cli_command="/custom/claude",
            )
            args, _ = mock.call_args
            assert args[-1] == "/custom/claude"

    def test_passes_cli_command_to_codex(self):
        with patch("scripts.run_eval.run_single_query_codex", return_value="triggered") as mock:
            run_single_query(
                "q", "s", "d", 10, "/tmp",
                cli_type=CLI_CODEX, cli_command="/custom/codex",
            )
            args, _ = mock.call_args
            assert args[-1] == "/custom/codex"


class TestRunEval:
    def test_basic_eval(self):
        """Test that run_eval correctly aggregates results."""
        eval_set = [
            {"query": "trigger me", "should_trigger": True},
            {"query": "ignore me", "should_trigger": False},
        ]

        def mock_run_single(query, *args, **kwargs):
            return "triggered" if query == "trigger me" else "completed"

        # Patch ProcessPoolExecutor to use ThreadPoolExecutor (avoids pickle issues)
        with patch("scripts.run_eval.ProcessPoolExecutor", ThreadPoolExecutor):
            with patch("scripts.run_eval.run_single_query", side_effect=mock_run_single):
                result = run_eval(
                    eval_set=eval_set,
                    skill_name="test",
                    description="test desc",
                    num_workers=1,
                    timeout=10,
                    project_root=Path("/tmp"),
                    runs_per_query=1,
                    trigger_threshold=0.5,
                    cli_type=CLI_CLAUDE,
                )

        assert result["summary"]["total"] == 2
        assert result["summary"]["passed"] == 2
        assert result["summary"]["failed"] == 0
        assert {r["status"] for r in result["results"]} == {"ok"}
        assert {r["attempted_runs"] for r in result["results"]} == {1}

    def test_eval_with_failures(self):
        eval_set = [
            {"query": "should trigger", "should_trigger": True},
            {"query": "should not trigger", "should_trigger": False},
        ]

        # Both complete without triggering
        with patch("scripts.run_eval.ProcessPoolExecutor", ThreadPoolExecutor):
            with patch("scripts.run_eval.run_single_query", return_value="completed"):
                result = run_eval(
                    eval_set=eval_set,
                    skill_name="test",
                    description="test desc",
                    num_workers=1,
                    timeout=10,
                    project_root=Path("/tmp"),
                    runs_per_query=1,
                    trigger_threshold=0.5,
                    cli_type=CLI_CLAUDE,
                )

        # "should trigger" → False → FAIL, "should not trigger" → False → PASS
        assert result["summary"]["passed"] == 1
        assert result["summary"]["failed"] == 1

    def test_passes_cli_type_and_command(self):
        eval_set = [{"query": "q", "should_trigger": True}]
        calls = []

        def capture_call(*args, **kwargs):
            calls.append((args, kwargs))
            return "triggered"

        with patch("scripts.run_eval.ProcessPoolExecutor", ThreadPoolExecutor):
            with patch("scripts.run_eval.run_single_query", side_effect=capture_call):
                run_eval(
                    eval_set=eval_set,
                    skill_name="test",
                    description="desc",
                    num_workers=1,
                    timeout=10,
                    project_root=Path("/tmp"),
                    runs_per_query=1,
                    cli_type=CLI_CODEX,
                    cli_command="/custom/codex",
                )

        assert len(calls) == 1
        args, _ = calls[0]
        # args: query, skill_name, description, timeout, project_root, model,
        #       cli_type, cli_command, source_skill_dir
        assert args[6] == CLI_CODEX
        assert args[7] == "/custom/codex"

    def test_multiple_runs_per_query(self):
        eval_set = [{"query": "test", "should_trigger": True}]
        call_count = 0

        def count_calls(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            return "triggered"

        with patch("scripts.run_eval.ProcessPoolExecutor", ThreadPoolExecutor):
            with patch("scripts.run_eval.run_single_query", side_effect=count_calls):
                result = run_eval(
                    eval_set=eval_set,
                    skill_name="test",
                    description="desc",
                    num_workers=1,
                    timeout=10,
                    project_root=Path("/tmp"),
                    runs_per_query=3,
                    cli_type=CLI_CLAUDE,
                )

        assert call_count == 3
        assert result["results"][0]["runs"] == 3
        assert result["results"][0]["triggers"] == 3

    def test_query_with_only_errors_is_marked_failed(self):
        eval_set = [{"query": "do not trigger", "should_trigger": False}]

        with patch("scripts.run_eval.ProcessPoolExecutor", ThreadPoolExecutor):
            with patch("scripts.run_eval.run_single_query", side_effect=RuntimeError("CLI crashed")):
                result = run_eval(
                    eval_set=eval_set,
                    skill_name="test",
                    description="desc",
                    num_workers=1,
                    timeout=10,
                    project_root=Path("/tmp"),
                    runs_per_query=1,
                    trigger_threshold=0.5,
                    cli_type=CLI_CLAUDE,
                )

        assert result["summary"]["failed"] == 1
        assert result["summary"]["errors"] == 1
        assert result["results"][0]["runs"] == 0
        assert result["results"][0]["attempted_runs"] == 1
        assert result["results"][0]["status"] == "error"
        assert result["results"][0]["pass"] is False
        assert result["results"][0]["error_count"] == 1

    def test_duplicate_queries_stay_independent_and_ordered(self):
        eval_set = [
            {"query": "same query", "should_trigger": True},
            {"query": "same query", "should_trigger": False},
        ]
        outcomes = iter(["triggered", "completed"])

        with patch("scripts.run_eval.ProcessPoolExecutor", ThreadPoolExecutor):
            with patch("scripts.run_eval.run_single_query", side_effect=lambda *a, **k: next(outcomes)):
                result = run_eval(
                    eval_set=eval_set,
                    skill_name="test",
                    description="desc",
                    num_workers=1,
                    timeout=10,
                    project_root=Path("/tmp"),
                    runs_per_query=1,
                    trigger_threshold=0.5,
                    cli_type=CLI_CLAUDE,
                )

        assert [r["should_trigger"] for r in result["results"]] == [True, False]
        assert result["results"][0]["triggers"] == 1
        assert result["results"][1]["triggers"] == 0
        assert all(r["pass"] for r in result["results"])

    def test_query_with_zero_attempted_runs_is_marked_not_run(self):
        eval_set = [{"query": "do not trigger", "should_trigger": False}]

        with patch("scripts.run_eval.ProcessPoolExecutor", ThreadPoolExecutor):
            result = run_eval(
                eval_set=eval_set,
                skill_name="test",
                description="desc",
                num_workers=1,
                timeout=10,
                project_root=Path("/tmp"),
                runs_per_query=0,
                trigger_threshold=0.5,
                cli_type=CLI_CLAUDE,
            )

        assert result["summary"]["total"] == 1
        assert result["summary"]["failed"] == 1
        assert result["results"][0]["runs"] == 0
        assert result["results"][0]["attempted_runs"] == 0
        assert result["results"][0]["status"] == "not_run"
        assert result["results"][0]["pass"] is False

    def test_run_eval_tracks_errors_in_summary(self):
        """Verify that CLI errors are counted in summary.errors."""
        eval_set = [
            {"query": "error query", "should_trigger": True},
            {"query": "ok query", "should_trigger": True},
        ]

        def mock_run(query, *args, **kwargs):
            if query == "error query":
                raise RuntimeError("CLI crashed")
            return "triggered"

        with patch("scripts.run_eval.ProcessPoolExecutor", ThreadPoolExecutor):
            with patch("scripts.run_eval.run_single_query", side_effect=mock_run):
                result = run_eval(
                    eval_set=eval_set,
                    skill_name="test",
                    description="test desc",
                    num_workers=1,
                    timeout=10,
                    project_root=Path("/tmp"),
                    runs_per_query=1,
                    cli_type=CLI_CLAUDE,
                )

        assert result["summary"]["errors"] == 1
        error_results = [r for r in result["results"] if r.get("errors")]
        assert len(error_results) == 1
        assert "CLI crashed" in error_results[0]["errors"][0]


class TestCodexSerialization:
    def test_codex_eval_forces_single_worker(self):
        eval_set = [{"query": "q", "should_trigger": False}]
        captured = {}

        class CapturingExecutor(ThreadPoolExecutor):
            def __init__(self, max_workers=None, **kwargs):
                captured["max_workers"] = max_workers
                super().__init__(max_workers=max_workers, **kwargs)

        with patch("scripts.run_eval.ProcessPoolExecutor", CapturingExecutor):
            with patch("scripts.run_eval.run_single_query", return_value="completed"):
                run_eval(
                    eval_set=eval_set,
                    skill_name="test",
                    description="desc",
                    num_workers=8,
                    timeout=10,
                    project_root=Path("/tmp"),
                    runs_per_query=1,
                    cli_type=CLI_CODEX,
                )

        assert captured["max_workers"] == 1

    def test_claude_eval_keeps_requested_workers(self):
        eval_set = [{"query": "q", "should_trigger": False}]
        captured = {}

        class CapturingExecutor(ThreadPoolExecutor):
            def __init__(self, max_workers=None, **kwargs):
                captured["max_workers"] = max_workers
                super().__init__(max_workers=max_workers, **kwargs)

        with patch("scripts.run_eval.ProcessPoolExecutor", CapturingExecutor):
            with patch("scripts.run_eval.run_single_query", return_value="completed"):
                run_eval(
                    eval_set=eval_set,
                    skill_name="test",
                    description="desc",
                    num_workers=8,
                    timeout=10,
                    project_root=Path("/tmp"),
                    runs_per_query=1,
                    cli_type=CLI_CLAUDE,
                )

        assert captured["max_workers"] == 8


class TestTimeoutAggregation:
    def test_run_eval_counts_timeouts_as_non_triggers(self):
        eval_set = [{"query": "slow query", "should_trigger": True}]

        with patch("scripts.run_eval.ProcessPoolExecutor", ThreadPoolExecutor):
            with patch("scripts.run_eval.run_single_query", return_value="timeout"):
                result = run_eval(
                    eval_set=eval_set,
                    skill_name="test",
                    description="desc",
                    num_workers=1,
                    timeout=10,
                    project_root=Path("/tmp"),
                    runs_per_query=2,
                    trigger_threshold=0.5,
                    cli_type=CLI_CLAUDE,
                )

        entry = result["results"][0]
        assert entry["runs"] == 2
        assert entry["triggers"] == 0
        assert entry["timeouts"] == 2
        assert entry["status"] == "ok"
        assert entry["pass"] is False
        assert result["summary"]["timeouts"] == 2

    def test_run_eval_omits_timeouts_field_when_none(self):
        eval_set = [{"query": "q", "should_trigger": True}]

        with patch("scripts.run_eval.ProcessPoolExecutor", ThreadPoolExecutor):
            with patch("scripts.run_eval.run_single_query", return_value="triggered"):
                result = run_eval(
                    eval_set=eval_set,
                    skill_name="test",
                    description="desc",
                    num_workers=1,
                    timeout=10,
                    project_root=Path("/tmp"),
                    runs_per_query=1,
                    cli_type=CLI_CLAUDE,
                )

        assert "timeouts" not in result["results"][0]
        assert result["summary"]["timeouts"] == 0


class TestInstalledSkillMasking:
    def _run_eval_with_capture(self, project_root, cli_type, installed):
        captured = {}

        def mock_run(*args, **kwargs):
            captured["source_skill_dir"] = args[8]
            captured["installed_hidden"] = not installed.exists()
            return "completed"

        with patch("scripts.run_eval.ProcessPoolExecutor", ThreadPoolExecutor):
            with patch("scripts.run_eval.run_single_query", side_effect=mock_run):
                run_eval(
                    eval_set=[{"query": "q", "should_trigger": False}],
                    skill_name="test",
                    description="candidate desc",
                    num_workers=1,
                    timeout=10,
                    project_root=project_root,
                    runs_per_query=1,
                    cli_type=cli_type,
                )
        return captured

    def test_masks_installed_claude_skill_during_runs(self, tmp_path):
        project_root = tmp_path / "project"
        installed = project_root / ".claude" / "skills" / "test"
        installed.mkdir(parents=True)
        (installed / "SKILL.md").write_text("---\nname: test\ndescription: original\n---\n")

        captured = self._run_eval_with_capture(project_root, CLI_CLAUDE, installed)

        assert captured["installed_hidden"] is True
        source = Path(captured["source_skill_dir"])
        assert source.name == "test"
        assert source.parent.name.startswith("skill-forge-masked-")
        # Restored after the eval, mask dir cleaned up
        assert (installed / "SKILL.md").exists()
        assert not source.parent.exists()

    def test_masks_installed_codex_skill_during_runs(self, tmp_path):
        project_root = tmp_path / "project"
        installed = project_root / ".agents" / "skills" / "test"
        installed.mkdir(parents=True)
        (installed / "SKILL.md").write_text("---\nname: test\ndescription: original\n---\n")

        captured = self._run_eval_with_capture(project_root, CLI_CODEX, installed)

        assert captured["installed_hidden"] is True
        assert (installed / "SKILL.md").exists()

    def test_no_masking_when_skill_not_installed(self, tmp_path):
        project_root = tmp_path / "project"
        project_root.mkdir()
        installed = project_root / ".claude" / "skills" / "test"

        captured = self._run_eval_with_capture(project_root, CLI_CLAUDE, installed)

        assert captured["source_skill_dir"] is None
