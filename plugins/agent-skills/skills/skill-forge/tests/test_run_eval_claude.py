"""Tests for the Claude trigger-eval runner."""

import json
import os
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest.mock import MagicMock, patch

from scripts.run_eval_claude import run_single_query_claude

SKILL_NAME = "skill-forge"


class TestRunSingleQueryClaude:
    def _make_process_mock(self, output_lines: list[str]):
        output = ("\n".join(output_lines) + "\n").encode()
        mock_process = MagicMock()
        mock_process.poll.side_effect = [None, 0]
        mock_process.stdout.read.return_value = b""
        mock_process.stdout.fileno.return_value = 0
        mock_process.stderr.read.return_value = b""
        mock_process.returncode = 0
        return mock_process, output

    def test_detects_canonical_skill_name_from_assistant_tool_use(self, tmp_path):
        project_root = tmp_path / "project"
        project_root.mkdir()

        events = [
            json.dumps({
                "type": "assistant",
                "message": {
                    "content": [
                        {"type": "tool_use", "name": "Skill", "input": {"skill": SKILL_NAME}},
                    ],
                },
            }),
            json.dumps({"type": "result"}),
        ]
        mock_process, output = self._make_process_mock(events)

        with patch("scripts.run_eval_claude.subprocess.Popen", return_value=mock_process):
            with patch("scripts.trigger_probe.select.select", return_value=([mock_process.stdout], [], [])):
                with patch("scripts.trigger_probe.os.read", return_value=output):
                    result = run_single_query_claude(
                        "test query", SKILL_NAME, "test desc", 5, str(project_root),
                    )

        assert result == "triggered"

    def test_detects_stream_event_skill_tool_use(self, tmp_path):
        project_root = tmp_path / "project"
        project_root.mkdir()

        events = [
            json.dumps({
                "type": "stream_event",
                "event": {
                    "type": "content_block_start",
                    "content_block": {"type": "tool_use", "name": "Skill"},
                },
            }),
            json.dumps({
                "type": "stream_event",
                "event": {
                    "type": "content_block_delta",
                    "delta": {
                        "type": "input_json_delta",
                        "partial_json": json.dumps({"skill": SKILL_NAME}),
                    },
                },
            }),
            json.dumps({
                "type": "stream_event",
                "event": {"type": "content_block_stop"},
            }),
        ]
        mock_process, output = self._make_process_mock(events)

        with patch("scripts.run_eval_claude.subprocess.Popen", return_value=mock_process):
            with patch("scripts.trigger_probe.select.select", return_value=([mock_process.stdout], [], [])):
                with patch("scripts.trigger_probe.os.read", return_value=output):
                    result = run_single_query_claude(
                        "test query", SKILL_NAME, "test desc", 5, str(project_root),
                    )

        assert result == "triggered"

    def test_stream_event_shape_change_does_not_trigger(self, tmp_path):
        project_root = tmp_path / "project"
        project_root.mkdir()

        events = [
            json.dumps({
                "type": "stream_event",
                "event": {
                    "type": "content_block_delta",
                    "delta": {
                        "type": "text_delta",
                        "text": json.dumps({"skill": SKILL_NAME}),
                    },
                },
            }),
            json.dumps({"type": "result"}),
        ]
        mock_process, output = self._make_process_mock(events)

        with patch("scripts.run_eval_claude.subprocess.Popen", return_value=mock_process):
            with patch("scripts.trigger_probe.select.select", return_value=([mock_process.stdout], [], [])):
                with patch("scripts.trigger_probe.os.read", return_value=output):
                    result = run_single_query_claude(
                        "test query", SKILL_NAME, "test desc", 5, str(project_root),
                    )

        assert result == "completed"

    def test_ignores_non_matching_tool_before_skill_trigger(self, tmp_path):
        project_root = tmp_path / "project"
        project_root.mkdir()

        events = [
            json.dumps({
                "type": "assistant",
                "message": {
                    "content": [
                        {"type": "tool_use", "name": "Bash", "input": {"command": "pwd"}},
                    ],
                },
            }),
            json.dumps({
                "type": "assistant",
                "message": {
                    "content": [
                        {"type": "tool_use", "name": "Skill", "input": {"skill": SKILL_NAME}},
                    ],
                },
            }),
            json.dumps({"type": "result"}),
        ]
        mock_process, output = self._make_process_mock(events)

        with patch("scripts.run_eval_claude.subprocess.Popen", return_value=mock_process):
            with patch("scripts.trigger_probe.select.select", return_value=([mock_process.stdout], [], [])):
                with patch("scripts.trigger_probe.os.read", return_value=output):
                    result = run_single_query_claude(
                        "test query", SKILL_NAME, "test desc", 5, str(project_root),
                    )

        assert result == "triggered"

    def test_detects_skill_path_from_read_tool_use(self, tmp_path):
        project_root = tmp_path / "project"
        project_root.mkdir()

        events = [
            json.dumps({
                "type": "assistant",
                "message": {
                    "content": [
                        {
                            "type": "tool_use",
                            "name": "Read",
                            "input": {
                                "file_path": str(project_root / ".claude" / "skills" / SKILL_NAME / "SKILL.md"),
                            },
                        },
                    ],
                },
            }),
            json.dumps({"type": "result"}),
        ]
        mock_process, output = self._make_process_mock(events)

        with patch("scripts.run_eval_claude.subprocess.Popen", return_value=mock_process):
            with patch("scripts.trigger_probe.select.select", return_value=([mock_process.stdout], [], [])):
                with patch("scripts.trigger_probe.os.read", return_value=output):
                    result = run_single_query_claude(
                        "test query", SKILL_NAME, "test desc", 5, str(project_root),
                    )

        assert result == "triggered"

    def test_uses_isolated_workspace_for_temp_skill_even_with_override(self, tmp_path):
        project_root = tmp_path / "project"
        project_root.mkdir()
        claude_home = tmp_path / "custom-claude-home"
        observed = {}

        events = [
            json.dumps({"type": "result"}),
        ]
        mock_process, output = self._make_process_mock(events)

        with patch.dict(os.environ, {"SKILL_FORGE_CLAUDE_HOME": str(claude_home)}, clear=True):
            def capture_popen(*args, **kwargs):
                observed["cwd"] = Path(kwargs["cwd"])
                observed["claude_home"] = Path(kwargs["env"]["SKILL_FORGE_CLAUDE_HOME"])
                observed["claude_config_dir"] = Path(kwargs["env"]["CLAUDE_CONFIG_DIR"])
                return mock_process

            with patch("scripts.run_eval_claude.subprocess.Popen", side_effect=capture_popen):
                with patch("scripts.trigger_probe.select.select", return_value=([mock_process.stdout], [], [])):
                    with patch("scripts.trigger_probe.os.read", return_value=output):
                        result = run_single_query_claude(
                            "test query", SKILL_NAME, "test desc", 5, str(project_root),
                        )

        assert result == "completed"
        assert observed["cwd"] == project_root
        # Temp home lives in system temp so a hard kill cannot litter the repo
        assert not str(observed["claude_home"]).startswith(str(project_root))
        assert observed["claude_home"].name.startswith("skill-forge-claude-home-")
        assert observed["claude_config_dir"] == observed["claude_home"]
        assert not observed["claude_home"].exists()
        assert not (claude_home / "commands").exists()
        assert not (claude_home / "skills").exists()
        assert not (project_root / ".claude").exists()

    def test_copies_supporting_files_into_temp_skill(self, tmp_path):
        project_root = tmp_path / "project"
        source_skill = project_root / ".claude" / "skills" / SKILL_NAME
        source_skill.mkdir(parents=True)
        (source_skill / "SKILL.md").write_text(
            "---\n"
            f"name: {SKILL_NAME}\n"
            "description: old desc\n"
            "---\n\n"
            "# Old\n"
        )
        (source_skill / "references").mkdir()
        (source_skill / "references" / "guide.md").write_text("supporting file")

        observed = {}

        events = [
            json.dumps({"type": "result"}),
        ]
        mock_process, output = self._make_process_mock(events)

        def capture_popen(*args, **kwargs):
            temp_skill = Path(kwargs["env"]["SKILL_FORGE_CLAUDE_HOME"]) / "skills" / SKILL_NAME
            observed["skill_md"] = (temp_skill / "SKILL.md").read_text()
            observed["supporting_file"] = (temp_skill / "references" / "guide.md").read_text()
            return mock_process

        with patch("scripts.run_eval_claude.subprocess.Popen", side_effect=capture_popen):
            with patch("scripts.trigger_probe.select.select", return_value=([mock_process.stdout], [], [])):
                with patch("scripts.trigger_probe.os.read", return_value=output):
                    result = run_single_query_claude(
                        "test query", SKILL_NAME, "test desc", 5, str(project_root),
                    )

        assert result == "completed"
        assert "description: |\n  test desc\n" in observed["skill_md"]
        assert "old desc" not in observed["skill_md"]
        assert observed["supporting_file"] == "supporting file"

    def test_detects_relative_skill_path_from_read_tool_use(self, tmp_path):
        project_root = tmp_path / "project"
        project_root.mkdir()
        claude_home = tmp_path / "custom-claude-home"

        events = [
            json.dumps({
                "type": "assistant",
                "message": {
                    "content": [
                        {
                            "type": "tool_use",
                            "name": "Read",
                            "input": {
                                "file_path": f"skills/{SKILL_NAME}/SKILL.md",
                            },
                        },
                    ],
                },
            }),
            json.dumps({"type": "result"}),
        ]
        mock_process, output = self._make_process_mock(events)

        with patch.dict(os.environ, {"SKILL_FORGE_CLAUDE_HOME": str(claude_home)}, clear=True):
            with patch("scripts.run_eval_claude.subprocess.Popen", return_value=mock_process):
                with patch("scripts.trigger_probe.select.select", return_value=([mock_process.stdout], [], [])):
                    with patch("scripts.trigger_probe.os.read", return_value=output):
                        result = run_single_query_claude(
                            "test query", SKILL_NAME, "test desc", 5, str(project_root),
                        )

        assert result == "triggered"


class TestTemporarySkillNames:
    def test_claude_temp_skill_keeps_original_visible_name(self, tmp_path):
        project_root = tmp_path / "project"
        project_root.mkdir()

        observed = {}

        def capture_popen(cmd, **kwargs):
            skill_root = Path(kwargs["env"]["SKILL_FORGE_CLAUDE_HOME"]) / "skills"
            skill_file = next(skill_root.glob("*/SKILL.md"))
            observed["path"] = skill_file
            observed["content"] = skill_file.read_text()

            mock_process = MagicMock()
            mock_process.poll.side_effect = [0, 0]
            mock_process.stdout.read.return_value = b'{"type":"result"}\n'
            mock_process.stderr.read.return_value = b""
            mock_process.returncode = 0
            return mock_process

        with patch("scripts.run_eval_claude.subprocess.Popen", side_effect=capture_popen):
            with patch("scripts.trigger_probe.select.select", return_value=([], [], [])):
                run_single_query_claude(
                    "test query", SKILL_NAME, "test desc", 5, str(project_root),
                )

        assert observed["path"].parent.name == SKILL_NAME
        assert observed["path"].name == "SKILL.md"
        assert f"name: {SKILL_NAME}\n" in observed["content"]
        assert f"# {SKILL_NAME}\n" in observed["content"]

    def test_claude_temp_skill_paths_are_isolated_per_run(self, tmp_path):
        project_root = tmp_path / "project"
        project_root.mkdir()

        observed_paths = []
        observed_lock = threading.Lock()
        barrier = threading.Barrier(2)

        def capture_popen(cmd, **kwargs):
            claude_home = Path(kwargs["env"]["SKILL_FORGE_CLAUDE_HOME"])
            skill_root = claude_home / "skills"
            barrier.wait(timeout=2)
            snapshot = sorted(path.name for path in skill_root.iterdir())
            with observed_lock:
                observed_paths.append((claude_home.name, snapshot))

            mock_process = MagicMock()
            mock_process.poll.side_effect = [0, 0]
            mock_process.stdout.read.return_value = b'{"type":"result"}\n'
            mock_process.stderr.read.return_value = b""
            mock_process.returncode = 0
            return mock_process

        with patch("scripts.run_eval_claude.subprocess.Popen", side_effect=capture_popen):
            with patch("scripts.trigger_probe.select.select", return_value=([], [], [])):
                with ThreadPoolExecutor(max_workers=2) as executor:
                    futures = [
                        executor.submit(
                            run_single_query_claude,
                            "test query",
                            SKILL_NAME,
                            "test desc",
                            5,
                            str(project_root),
                        )
                        for _ in range(2)
                    ]
                    for future in futures:
                        assert future.result() == "completed"

        assert len(observed_paths) == 2
        assert len({path for path, _ in observed_paths}) == 2
        assert all(snapshot == [SKILL_NAME] for _, snapshot in observed_paths)

    def test_claude_runs_in_project_root_with_isolated_home(self, tmp_path):
        project_root = tmp_path / "project"
        project_root.mkdir()

        observed = {}

        def capture_popen(cmd, **kwargs):
            observed["cwd"] = Path(kwargs["cwd"])
            observed["claude_home"] = Path(kwargs["env"]["SKILL_FORGE_CLAUDE_HOME"])

            mock_process = MagicMock()
            mock_process.poll.side_effect = [0, 0]
            mock_process.stdout.read.return_value = b'{"type":"result"}\n'
            mock_process.stderr.read.return_value = b""
            mock_process.returncode = 0
            return mock_process

        with patch("scripts.run_eval_claude.subprocess.Popen", side_effect=capture_popen):
            with patch("scripts.trigger_probe.select.select", return_value=([], [], [])):
                result = run_single_query_claude(
                    "test query", SKILL_NAME, "test desc", 5, str(project_root),
                )

        assert result == "completed"
        assert observed["cwd"] == project_root
        assert not str(observed["claude_home"]).startswith(str(project_root))
        assert observed["claude_home"].name.startswith("skill-forge-claude-home-")
        assert not observed["claude_home"].exists()


class TestTimeoutOutcome:
    def test_claude_timeout_returns_timeout_outcome(self, tmp_path):
        project_root = tmp_path / "project"
        project_root.mkdir()

        mock_process = MagicMock()
        mock_process.poll.return_value = None

        with patch("scripts.run_eval_claude.subprocess.Popen", return_value=mock_process):
            result = run_single_query_claude(
                "test query", SKILL_NAME, "test desc", 0, str(project_root),
            )

        assert result == "timeout"
        mock_process.kill.assert_called_once()
