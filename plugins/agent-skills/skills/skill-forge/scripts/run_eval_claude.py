"""Claude-specific trigger evaluation helpers."""

import json
import os
import select
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

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


def run_single_query_claude(
    query: str,
    skill_name: str,
    skill_description: str,
    timeout: int,
    project_root: str,
    model: str | None = None,
    cli_command: str | None = None,
) -> bool:
    """Run a single query via Claude Code and return whether the skill was triggered."""
    project_root_path = Path(project_root)
    source_skills_dir = resolve_skill_dir(CLI_CLAUDE, project_root_path)
    temp_claude_home = Path(tempfile.mkdtemp(prefix="skill-forge-claude-home-", dir=project_root_path))
    temp_skills_dir = temp_claude_home / "skills"
    temp_skill_dir = temp_skills_dir / skill_name
    skill_file = temp_skill_dir / "SKILL.md"

    try:
        source_skill_dir = source_skills_dir / skill_name
        if source_skill_dir.exists():
            shutil.copytree(source_skill_dir, temp_skill_dir)
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

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=project_root,
            env=env,
        )

        triggered = False
        start_time = time.time()
        buffer = ""
        pending_tool_name = None
        accumulated_json = ""

        try:
            while time.time() - start_time < timeout:
                if process.poll() is not None:
                    remaining = process.stdout.read()
                    if remaining:
                        buffer += remaining.decode("utf-8", errors="replace")
                    break

                ready, _, _ = select.select([process.stdout], [], [], 1.0)
                if not ready:
                    continue

                chunk = os.read(process.stdout.fileno(), 8192)
                if not chunk:
                    break
                buffer += chunk.decode("utf-8", errors="replace")

                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    line = line.strip()
                    if not line:
                        continue

                    try:
                        event = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    if event.get("type") == "stream_event":
                        se = event.get("event", {})
                        se_type = se.get("type", "")

                        if se_type == "content_block_start":
                            cb = se.get("content_block", {})
                            if cb.get("type") == "tool_use":
                                tool_name = cb.get("name", "")
                                if tool_name in ("Skill", "Read"):
                                    pending_tool_name = tool_name
                                    accumulated_json = ""

                        elif se_type == "content_block_delta" and pending_tool_name:
                            delta = se.get("delta", {})
                            if delta.get("type") == "input_json_delta":
                                accumulated_json += delta.get("partial_json", "")
                                try:
                                    tool_input = json.loads(accumulated_json)
                                except json.JSONDecodeError:
                                    continue
                                if _is_expected_claude_tool_input(
                                    pending_tool_name,
                                    tool_input,
                                    skill_name,
                                    temp_skills_dir,
                                ):
                                    return True

                        elif se_type in ("content_block_stop", "message_stop"):
                            if pending_tool_name:
                                try:
                                    tool_input = json.loads(accumulated_json)
                                except json.JSONDecodeError:
                                    tool_input = {}
                                if _is_expected_claude_tool_input(
                                    pending_tool_name,
                                    tool_input,
                                    skill_name,
                                    temp_skills_dir,
                                ):
                                    return True
                                pending_tool_name = None
                                accumulated_json = ""

                    elif event.get("type") == "assistant":
                        message = event.get("message", {})
                        for content_item in message.get("content", []):
                            if content_item.get("type") != "tool_use":
                                continue
                            if _is_expected_claude_tool_input(
                                content_item.get("name", ""),
                                content_item.get("input", {}),
                                skill_name,
                                temp_skills_dir,
                            ):
                                triggered = True
                                return True

                    elif event.get("type") == "result":
                        return triggered
        finally:
            killed = False
            if process.poll() is None:
                process.kill()
                process.wait()
                killed = True
            if not killed and process.returncode and process.returncode != 0:
                stderr_output = process.stderr.read().decode("utf-8", errors="replace") if process.stderr else ""
                raise RuntimeError(
                    f"Claude CLI exited with code {process.returncode}: {stderr_output[:500]}"
                )

        return triggered
    finally:
        shutil.rmtree(temp_claude_home, ignore_errors=True)
