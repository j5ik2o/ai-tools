"""Claude-specific trigger evaluation helpers."""

import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

from scripts.trigger_probe import COMPLETED, TRIGGERED, watch_process
from scripts.utils import CLI_CLAUDE, get_cli_command, resolve_skill_dir


def _is_expected_claude_tool_input(
    tool_name: str,
    tool_input: dict,
    skill_name: str,
    skills_dir: Path,
) -> bool:
    """Return True when a Claude tool call targets the skill under test."""
    if tool_name == "Skill":
        return tool_input.get("skill", "") == skill_name

    if tool_name == "Read":
        file_path = tool_input.get("file_path", "")
        expected_path = skills_dir / skill_name / "SKILL.md"
        expected_suffix = Path("skills") / skill_name / "SKILL.md"
        normalized_file_path = file_path.replace("\\", "/")
        return (
            normalized_file_path == str(expected_path).replace("\\", "/")
            or normalized_file_path.endswith(str(expected_path).replace("\\", "/"))
            or normalized_file_path.endswith(str(expected_suffix).replace("\\", "/"))
        )

    return False


def _write_skill_under_test(skill_file: Path, skill_name: str, skill_description: str) -> None:
    """Write a real SKILL.md for the description under test."""
    indented_desc = "\n  ".join(skill_description.split("\n"))
    skill_content = (
        f"---\n"
        f"name: {skill_name}\n"
        f"description: |\n"
        f"  {indented_desc}\n"
        f"---\n\n"
        f"# {skill_name}\n\n"
        f"This skill handles: {skill_description}\n"
    )
    skill_file.write_text(skill_content)


def _make_claude_classifier(skill_name: str, skills_dir: Path):
    """Build a stateful classifier for Claude stream-json events."""
    pending_tool = ""
    accumulated_json = ""

    def classify(event: dict) -> str | None:
        nonlocal pending_tool, accumulated_json

        event_type = event.get("type")
        if event_type == "stream_event":
            se = event.get("event", {})
            se_type = se.get("type", "")

            if se_type == "content_block_start":
                cb = se.get("content_block", {})
                if cb.get("type") == "tool_use" and cb.get("name", "") in ("Skill", "Read"):
                    pending_tool = cb.get("name", "")
                    accumulated_json = ""

            elif se_type == "content_block_delta" and pending_tool:
                delta = se.get("delta", {})
                if delta.get("type") == "input_json_delta":
                    accumulated_json += delta.get("partial_json", "")
                    try:
                        tool_input = json.loads(accumulated_json)
                    except json.JSONDecodeError:
                        return None
                    if _is_expected_claude_tool_input(
                        pending_tool, tool_input, skill_name, skills_dir,
                    ):
                        return TRIGGERED

            elif se_type in ("content_block_stop", "message_stop"):
                if pending_tool:
                    try:
                        tool_input = json.loads(accumulated_json)
                    except json.JSONDecodeError:
                        tool_input = {}
                    matched = _is_expected_claude_tool_input(
                        pending_tool, tool_input, skill_name, skills_dir,
                    )
                    pending_tool = ""
                    accumulated_json = ""
                    if matched:
                        return TRIGGERED

        elif event_type == "assistant":
            for content_item in event.get("message", {}).get("content", []):
                if content_item.get("type") != "tool_use":
                    continue
                if _is_expected_claude_tool_input(
                    content_item.get("name", ""),
                    content_item.get("input", {}),
                    skill_name,
                    skills_dir,
                ):
                    return TRIGGERED

        elif event_type == "result":
            return COMPLETED

        return None

    return classify


def run_single_query_claude(
    query: str,
    skill_name: str,
    skill_description: str,
    timeout: int,
    project_root: str,
    model: str | None = None,
    cli_command: str | None = None,
    source_skill_dir: str | None = None,
) -> str:
    """Run a single query via Claude Code and classify the trigger outcome.

    Returns TRIGGERED, COMPLETED, or TIMEOUT. `source_skill_dir` overrides
    where supporting files are copied from (used while the installed skill is
    masked during an eval batch).
    """
    project_root_path = Path(project_root)
    temp_claude_home = Path(tempfile.mkdtemp(prefix="skill-forge-claude-home-", dir=project_root_path))
    temp_skills_dir = temp_claude_home / "skills"
    temp_skill_dir = temp_skills_dir / skill_name
    skill_file = temp_skill_dir / "SKILL.md"

    try:
        if source_skill_dir is not None:
            source_dir = Path(source_skill_dir)
        else:
            source_dir = resolve_skill_dir(CLI_CLAUDE, project_root_path) / skill_name
        if source_dir.exists():
            shutil.copytree(source_dir, temp_skill_dir)
        else:
            temp_skill_dir.mkdir(parents=True, exist_ok=True)
        _write_skill_under_test(skill_file, skill_name, skill_description)

        cmd = [
            get_cli_command(CLI_CLAUDE, cli_command),
            "-p", query,
            "--output-format", "stream-json",
            "--verbose",
            "--include-partial-messages",
        ]
        if model:
            cmd.extend(["--model", model])

        env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
        env["SKILL_FORGE_CLAUDE_HOME"] = str(temp_claude_home)
        env["CLAUDE_CONFIG_DIR"] = str(temp_claude_home)

        with tempfile.TemporaryFile() as stderr_sink:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=stderr_sink,
                cwd=project_root,
                env=env,
            )
            return watch_process(
                process,
                timeout=timeout,
                classify=_make_claude_classifier(skill_name, temp_skills_dir),
                label="Claude CLI",
                stderr_sink=stderr_sink,
            )
    finally:
        shutil.rmtree(temp_claude_home, ignore_errors=True)
