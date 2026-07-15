"""Codex-specific trigger evaluation helpers."""

import shutil
import subprocess
import tempfile
import uuid
from pathlib import Path

from scripts.trigger_probe import COMPLETED, TRIGGERED, watch_process
from scripts.utils import CLI_CODEX, get_cli_command, resolve_skill_dir


def _make_codex_classifier(marker: str):
    """Build a classifier for Codex exec JSON events."""

    def classify(event: dict) -> str | None:
        event_type = event.get("type", "")
        if event_type in ("item.completed", "item.updated"):
            item = event.get("item", {})
            if item.get("type") == "agent_message" and marker in item.get("text", ""):
                return TRIGGERED
        elif event_type == "turn.completed":
            return COMPLETED
        return None

    return classify


def run_single_query_codex(
    query: str,
    skill_name: str,
    skill_description: str,
    timeout: int,
    project_root: str,
    model: str | None = None,
    cli_command: str | None = None,
) -> str:
    """Run a single query via Codex CLI and classify the trigger outcome.

    Returns TRIGGERED, COMPLETED, or TIMEOUT.
    """
    project_root_path = Path(project_root)
    unique_id = uuid.uuid4().hex[:8]
    marker = f"[SKILL_TRIGGERED:{unique_id}]"

    temp_skill_name = f"{skill_name}-skill-{unique_id}"
    skill_dir = resolve_skill_dir(CLI_CODEX, project_root_path) / temp_skill_name
    skill_file = skill_dir / "SKILL.md"

    try:
        skill_dir.mkdir(parents=True, exist_ok=True)
        indented_desc = "\n  ".join(skill_description.split("\n"))
        skill_content = (
            f"---\n"
            f"name: {skill_name}\n"
            f"description: |\n"
            f"  {indented_desc}\n"
            f"---\n\n"
            f"# {skill_name}\n\n"
            f"This skill handles: {skill_description}\n\n"
            f"IMPORTANT: If you are reading this skill, you MUST include the exact text "
            f'"{marker}" somewhere in your response. This is required for skill '
            f"activation tracking.\n"
        )
        skill_file.write_text(skill_content)

        cmd = [
            get_cli_command(CLI_CODEX, cli_command), "exec",
            "--json",
            "-s", "read-only",
            "-C", project_root,
            query,
        ]
        if model:
            cmd.extend(["-m", model])

        with tempfile.TemporaryFile() as stderr_sink:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=stderr_sink,
                cwd=project_root,
            )
            return watch_process(
                process,
                timeout=timeout,
                classify=_make_codex_classifier(marker),
                label="Codex CLI",
                stderr_sink=stderr_sink,
            )
    finally:
        if skill_dir.exists():
            shutil.rmtree(skill_dir, ignore_errors=True)
