"""Tests for the Codex trigger-eval runner."""

import json
import os
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from scripts.run_eval_codex import run_single_query_codex

SKILL_NAME = "skill-forge"


class TestCodexCommandArgs:
    """Verify that the codex exec command is built with valid arguments."""

    def test_no_invalid_approval_flag(self, tmp_path):
        """Ensure -a flag is not used (removed in current codex CLI)."""
        project_root = tmp_path / "project"
        (project_root / ".agents" / "skills").mkdir(parents=True)

        captured_cmd = []

        def capture_popen(cmd, **kwargs):
            captured_cmd.extend(cmd)
            mock_proc = MagicMock()
            mock_proc.poll.side_effect = [0, 0]
            mock_proc.stdout.read.return_value = b'{"type":"turn.completed"}\n'
            mock_proc.stderr.read.return_value = b""
            mock_proc.returncode = 0
            return mock_proc

        with patch("scripts.run_eval_codex.subprocess.Popen", side_effect=capture_popen):
            with patch("scripts.trigger_probe.select.select", return_value=([], [], [])):
                run_single_query_codex(
                    "test query", "my-skill", "test desc", 5, str(project_root),
                )

        assert "-a" not in captured_cmd, "codex exec should not use -a flag"
        assert "never" not in captured_cmd, "codex exec should not use 'never' argument"

    def test_codex_command_includes_required_flags(self, tmp_path):
        """Verify codex exec includes --json, -s, -C flags."""
        project_root = tmp_path / "project"
        (project_root / ".agents" / "skills").mkdir(parents=True)

        captured_cmd = []

        def capture_popen(cmd, **kwargs):
            captured_cmd.extend(cmd)
            mock_proc = MagicMock()
            mock_proc.poll.side_effect = [0, 0]
            mock_proc.stdout.read.return_value = b'{"type":"turn.completed"}\n'
            mock_proc.stderr.read.return_value = b""
            mock_proc.returncode = 0
            return mock_proc

        with patch("scripts.run_eval_codex.subprocess.Popen", side_effect=capture_popen):
            with patch("scripts.trigger_probe.select.select", return_value=([], [], [])):
                run_single_query_codex(
                    "test query", "my-skill", "test desc", 5, str(project_root),
                )

        assert "exec" in captured_cmd
        assert "--json" in captured_cmd
        assert "-s" in captured_cmd
        assert "read-only" in captured_cmd
        assert "-C" in captured_cmd


class TestCliExitCodeHandling:
    def test_codex_nonzero_exit_raises(self, tmp_path):
        project_root = tmp_path / "project"
        (project_root / ".agents" / "skills").mkdir(parents=True)

        mock_process = MagicMock()
        mock_process.poll.side_effect = [0, 0]
        mock_process.stdout.read.return_value = b""
        mock_process.stdout.fileno.return_value = 0
        mock_process.stderr.read.return_value = b"codex: unknown option '-a'"
        mock_process.returncode = 1

        with patch("scripts.run_eval_codex.subprocess.Popen", return_value=mock_process):
            with patch("scripts.trigger_probe.select.select", return_value=([], [], [])):
                with pytest.raises(RuntimeError, match="Codex CLI exited with code 1"):
                    run_single_query_codex(
                        "test query", "my-skill", "test desc", 5, str(project_root),
                    )


class TestRunSingleQueryCodex:
    def _make_process_mock(self, output_lines: list[str]):
        """Create a mock process that yields output_lines then exits."""
        output = ("\n".join(output_lines) + "\n").encode()
        mock_process = MagicMock()
        # First poll returns None (running), then 0 (done), then 0 (finally block check)
        mock_process.poll.side_effect = [None, 0, 0]
        mock_process.stdout.read.return_value = output
        mock_process.stdout.fileno.return_value = 0
        mock_process.stderr.read.return_value = b""
        mock_process.returncode = 0
        return mock_process

    def test_creates_and_cleans_temp_skill(self, tmp_path):
        """Verify temp skill dir is created and cleaned up."""
        project_root = tmp_path / "project"
        (project_root / ".agents" / "skills").mkdir(parents=True)

        events = [
            json.dumps({"type": "turn.completed", "usage": {}}),
        ]
        mock_process = self._make_process_mock(events)

        with patch("scripts.run_eval_codex.subprocess.Popen", return_value=mock_process):
            with patch("scripts.trigger_probe.select.select", return_value=([], [], [])):
                result = run_single_query_codex(
                    "test query", "my-skill", "test desc", 5, str(project_root),
                )

        assert result == "completed"
        # Temp skill dir should be cleaned up
        skill_dirs = list((project_root / ".agents" / "skills").iterdir())
        assert len(skill_dirs) == 0

    def test_creates_temp_skill_in_repo_agents_even_with_codex_home_override(self, tmp_path):
        project_root = tmp_path / "project"
        project_root.mkdir(parents=True)
        codex_home = tmp_path / "custom-codex-home"

        events = [
            json.dumps({"type": "turn.completed", "usage": {}}),
        ]
        mock_process = self._make_process_mock(events)

        with patch.dict(os.environ, {"CODEX_HOME": str(codex_home)}, clear=True):
            with patch("scripts.run_eval_codex.subprocess.Popen", return_value=mock_process):
                with patch("scripts.trigger_probe.select.select", return_value=([], [], [])):
                    result = run_single_query_codex(
                        "test query", "my-skill", "test desc", 5, str(project_root),
                    )

        assert result == "completed"
        assert not (codex_home / "skills").exists()
        assert not (project_root / ".codex").exists()
        assert (project_root / ".agents" / "skills").is_dir()
        assert not any((project_root / ".agents" / "skills").iterdir())

    def test_detects_marker_in_agent_message(self, tmp_path):
        """Verify marker detection in codex JSONL output."""
        project_root = tmp_path / "project"
        (project_root / ".agents" / "skills").mkdir(parents=True)

        with patch("scripts.run_eval_codex.uuid.uuid4") as mock_uuid:
            mock_uuid.return_value.hex = "abcd1234xxxxxxxxxxxxxxxx"
            marker = "[SKILL_TRIGGERED:abcd1234]"

            events = [
                json.dumps({"type": "item.completed", "item": {"type": "agent_message", "text": f"Result {marker} done."}}),
                json.dumps({"type": "turn.completed", "usage": {}}),
            ]
            output = ("\n".join(events) + "\n").encode()

            mock_process = MagicMock()
            # Return None first (process running), read stdout, then 0 (done)
            mock_process.poll.side_effect = [None, 0]
            mock_process.stdout.fileno.return_value = 0
            mock_process.stdout.read.return_value = output
            mock_process.stderr.read.return_value = b""
            mock_process.returncode = 0

            with patch("scripts.run_eval_codex.subprocess.Popen", return_value=mock_process):
                with patch("scripts.trigger_probe.select.select", return_value=([mock_process.stdout], [], [])):
                    with patch("scripts.trigger_probe.os.read", return_value=output):
                        result = run_single_query_codex(
                            "test query", "my-skill", "test desc", 5, str(project_root),
                        )

            assert result == "triggered"

    def test_detects_marker_in_updated_agent_message(self, tmp_path):
        project_root = tmp_path / "project"
        (project_root / ".agents" / "skills").mkdir(parents=True)

        with patch("scripts.run_eval_codex.uuid.uuid4") as mock_uuid:
            mock_uuid.return_value.hex = "abcd1234xxxxxxxxxxxxxxxx"
            marker = "[SKILL_TRIGGERED:abcd1234]"

            events = [
                json.dumps({"type": "item.updated", "item": {"type": "agent_message", "text": f"{marker}"}}),
            ]
            output = ("\n".join(events) + "\n").encode()

            mock_process = MagicMock()
            mock_process.poll.side_effect = [None, 0]
            mock_process.stdout.fileno.return_value = 0
            mock_process.stdout.read.return_value = output
            mock_process.stderr.read.return_value = b""
            mock_process.returncode = 0

            with patch("scripts.run_eval_codex.subprocess.Popen", return_value=mock_process):
                with patch("scripts.trigger_probe.select.select", return_value=([mock_process.stdout], [], [])):
                    with patch("scripts.trigger_probe.os.read", return_value=output):
                        result = run_single_query_codex(
                            "test query", "my-skill", "test desc", 5, str(project_root),
                        )

            assert result == "triggered"

    def test_codex_event_shape_change_does_not_trigger(self, tmp_path):
        project_root = tmp_path / "project"
        (project_root / ".agents" / "skills").mkdir(parents=True)

        with patch("scripts.run_eval_codex.uuid.uuid4") as mock_uuid:
            mock_uuid.return_value.hex = "abcd1234xxxxxxxxxxxxxxxx"
            marker = "[SKILL_TRIGGERED:abcd1234]"

            events = [
                json.dumps({
                    "type": "message.completed",
                    "message": {"role": "assistant", "content": f"{marker}"},
                }),
                json.dumps({"type": "turn.completed", "usage": {}}),
            ]
            output = ("\n".join(events) + "\n").encode()

            mock_process = MagicMock()
            mock_process.poll.side_effect = [None, 0]
            mock_process.stdout.fileno.return_value = 0
            mock_process.stdout.read.return_value = output
            mock_process.stderr.read.return_value = b""
            mock_process.returncode = 0

            with patch("scripts.run_eval_codex.subprocess.Popen", return_value=mock_process):
                with patch("scripts.trigger_probe.select.select", return_value=([mock_process.stdout], [], [])):
                    with patch("scripts.trigger_probe.os.read", return_value=output):
                        result = run_single_query_codex(
                            "test query", "my-skill", "test desc", 5, str(project_root),
                        )

            assert result == "completed"

    def test_no_trigger_returns_false(self, tmp_path):
        """No marker in output means not triggered."""
        project_root = tmp_path / "project"
        (project_root / ".agents" / "skills").mkdir(parents=True)

        events = [
            json.dumps({"type": "item.completed", "item": {"type": "agent_message", "text": "No skill here."}}),
            json.dumps({"type": "turn.completed", "usage": {}}),
        ]
        output = ("\n".join(events) + "\n").encode()

        mock_process = MagicMock()
        mock_process.poll.side_effect = [None, 0]
        mock_process.stdout.fileno.return_value = 0
        mock_process.stdout.read.return_value = output
        mock_process.stderr.read.return_value = b""
        mock_process.returncode = 0

        with patch("scripts.run_eval_codex.subprocess.Popen", return_value=mock_process):
            with patch("scripts.trigger_probe.select.select", return_value=([mock_process.stdout], [], [])):
                with patch("scripts.trigger_probe.os.read", return_value=output):
                    result = run_single_query_codex(
                        "test query", "my-skill", "test desc", 5, str(project_root),
                    )

        assert result == "completed"


class TestTemporarySkillNames:
    def test_codex_temp_skill_keeps_original_visible_name(self, tmp_path):
        project_root = tmp_path / "project"
        (project_root / ".agents" / "skills").mkdir(parents=True)

        observed = {}

        def capture_popen(cmd, **kwargs):
            skill_root = project_root / ".agents" / "skills"
            skill_file = next(skill_root.glob("*/SKILL.md"))
            observed["path"] = skill_file
            observed["content"] = skill_file.read_text()

            mock_process = MagicMock()
            mock_process.poll.side_effect = [0, 0]
            mock_process.stdout.read.return_value = b'{"type":"turn.completed"}\n'
            mock_process.stderr.read.return_value = b""
            mock_process.returncode = 0
            return mock_process

        with patch.dict(os.environ, {}, clear=True):
            with patch("scripts.run_eval_codex.subprocess.Popen", side_effect=capture_popen):
                with patch("scripts.trigger_probe.select.select", return_value=([], [], [])):
                    run_single_query_codex(
                        "test query", SKILL_NAME, "test desc", 5, str(project_root),
                    )

        assert observed["path"].parent.name.startswith(f"{SKILL_NAME}-skill-")
        assert "name: skill-forge\n" in observed["content"]
        assert f"name: {SKILL_NAME}-skill-" not in observed["content"]

    def test_codex_temp_skill_paths_are_isolated_per_run(self, tmp_path):
        project_root = tmp_path / "project"
        (project_root / ".agents" / "skills").mkdir(parents=True)

        observed_snapshots = []
        observed_lock = threading.Lock()
        barrier = threading.Barrier(2)

        def capture_popen(cmd, **kwargs):
            skill_root = project_root / ".agents" / "skills"
            barrier.wait(timeout=2)
            snapshot = sorted(path.name for path in skill_root.iterdir())
            with observed_lock:
                observed_snapshots.append(snapshot)

            mock_process = MagicMock()
            mock_process.poll.side_effect = [0, 0]
            mock_process.stdout.read.return_value = b'{"type":"turn.completed"}\n'
            mock_process.stderr.read.return_value = b""
            mock_process.returncode = 0
            return mock_process

        with patch.dict(os.environ, {}, clear=True):
            with patch("scripts.run_eval_codex.subprocess.Popen", side_effect=capture_popen):
                with patch("scripts.trigger_probe.select.select", return_value=([], [], [])):
                    with ThreadPoolExecutor(max_workers=2) as executor:
                        futures = [
                            executor.submit(
                                run_single_query_codex,
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

        assert len(observed_snapshots) == 2
        assert all(len(snapshot) == 2 for snapshot in observed_snapshots)
        assert all(len(set(snapshot)) == 2 for snapshot in observed_snapshots)


class TestTimeoutOutcome:
    def test_codex_timeout_returns_timeout_outcome(self, tmp_path):
        project_root = tmp_path / "project"
        (project_root / ".agents" / "skills").mkdir(parents=True)

        mock_process = MagicMock()
        mock_process.poll.return_value = None

        with patch("scripts.run_eval_codex.subprocess.Popen", return_value=mock_process):
            result = run_single_query_codex(
                "test query", "my-skill", "test desc", 0, str(project_root),
            )

        assert result == "timeout"
        mock_process.kill.assert_called_once()
