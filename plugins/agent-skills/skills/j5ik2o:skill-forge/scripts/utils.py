"""Shared utilities for skill-forge scripts."""

import os
import re
import shutil
import sys
from contextlib import contextmanager
from pathlib import Path

import yaml

CLI_CLAUDE = "claude"
CLI_CODEX = "codex"

FRONTMATTER_PATTERN = re.compile(r"^---\n(.*?)\n---", re.DOTALL)


def get_default_cli_home_name(cli_type: str) -> str:
    """Return the default home directory name for the CLI."""
    if cli_type == CLI_CODEX:
        return ".codex"
    return ".claude"


def get_cli_command(cli_type: str, explicit_path: str | None = None) -> str:
    """Return the actual CLI command for the given CLI type.

    Priority: explicit_path argument > environment variable > default name.
      - SKILL_FORGE_CLAUDE_COMMAND: override the 'claude' binary (e.g. '/usr/local/bin/claude')
      - SKILL_FORGE_CODEX_COMMAND: override the 'codex' binary (e.g. '/opt/bin/codex')
    """
    if explicit_path:
        return explicit_path
    if cli_type == CLI_CLAUDE:
        return os.environ.get("SKILL_FORGE_CLAUDE_COMMAND", "claude")
    if cli_type == CLI_CODEX:
        return os.environ.get("SKILL_FORGE_CODEX_COMMAND", "codex")
    return cli_type


def detect_cli(explicit: str | None = None) -> str:
    """Detect which CLI to use. Returns CLI_CLAUDE or CLI_CODEX.

    Priority: explicit flag > SKILL_FORGE_EVAL_CLI env var > auto-detect.
    Auto-detection respects SKILL_FORGE_CLAUDE_COMMAND / SKILL_FORGE_CODEX_COMMAND env vars.
    """
    if explicit:
        if explicit not in (CLI_CLAUDE, CLI_CODEX):
            raise ValueError(f"Unknown CLI: {explicit}. Use 'claude' or 'codex'.")
        return explicit

    env_val = os.environ.get("SKILL_FORGE_EVAL_CLI")
    if env_val:
        if env_val not in (CLI_CLAUDE, CLI_CODEX):
            raise ValueError(f"Unknown SKILL_FORGE_EVAL_CLI value: {env_val}. Use 'claude' or 'codex'.")
        return env_val

    has_claude = shutil.which(get_cli_command(CLI_CLAUDE))
    has_codex = shutil.which(get_cli_command(CLI_CODEX))

    if has_claude and has_codex:
        print(
            "Warning: Both 'claude' and 'codex' CLIs found. Defaulting to 'claude'. "
            "Use --cli or SKILL_FORGE_EVAL_CLI to specify explicitly.",
            file=sys.stderr,
        )
        return CLI_CLAUDE
    if has_claude:
        return CLI_CLAUDE
    if has_codex:
        return CLI_CODEX

    raise RuntimeError("Neither 'claude' nor 'codex' CLI found in PATH")


def find_project_root(cli_type: str = CLI_CLAUDE) -> Path:
    """Find the project root by walking up from cwd.

    Prefers the nearest CLI home marker and falls back to the nearest git root.
    """
    current = Path.cwd()
    marker = get_default_cli_home_name(cli_type)
    parents = [current, *current.parents]

    for parent in parents:
        if (parent / marker).is_dir():
            return parent

    for parent in parents:
        if (parent / ".git").exists():
            return parent

    return current


def resolve_cli_home(cli_type: str, project_root: Path | None = None) -> Path:
    """Resolve the effective CLI home directory."""
    override_var = "SKILL_FORGE_CLAUDE_HOME" if cli_type == CLI_CLAUDE else "CODEX_HOME"
    override = os.environ.get(override_var)
    if override:
        return Path(override).expanduser()

    base_root = project_root if project_root is not None else find_project_root(cli_type)
    return base_root / get_default_cli_home_name(cli_type)


def resolve_skill_dir(cli_type: str, project_root: Path | None = None) -> Path:
    """Resolve the effective skills directory for the CLI."""
    if cli_type == CLI_CODEX:
        base_root = project_root if project_root is not None else find_project_root(cli_type)
        return base_root / ".agents" / "skills"
    return resolve_cli_home(cli_type, project_root) / "skills"


def project_skill_install_dir(cli_type: str, project_root: Path) -> Path:
    """Return the project-level skills directory the CLI discovers from cwd.

    Unlike resolve_skill_dir, home-directory overrides are irrelevant here:
    trigger evals run the CLI with cwd at the project root, and the CLI always
    discovers this path regardless of any home override.
    """
    if cli_type == CLI_CODEX:
        return project_root / ".agents" / "skills"
    return project_root / ".claude" / "skills"


@contextmanager
def mask_installed_skill(cli_type: str, skill_name: str, project_root: Path):
    """Temporarily move a same-named installed skill out of CLI discovery.

    Trigger evals present the description under test through a temporary
    skill. When the real skill is also installed in the project, both are
    visible under the same name and the real one contaminates the
    measurement (for Codex it even shadows the marker), so it is moved aside
    for the duration and restored afterwards.

    Yields the masked location (usable as a copy source), or None when the
    skill is not installed in the project.
    """
    installed = project_skill_install_dir(cli_type, project_root) / skill_name
    if not (installed.is_symlink() or installed.exists()):
        yield None
        return

    # The mask dir sits at the same depth as the skills dir so relative
    # symlink targets keep resolving from the masked location.
    mask_root = installed.parent.parent / f"skill-forge-masked-{os.getpid()}"
    mask_root.mkdir(parents=True, exist_ok=True)
    masked = mask_root / skill_name
    installed.rename(masked)
    print(
        f"Note: temporarily moved {installed} to {masked} during the trigger "
        "eval; it is restored automatically when the eval finishes.",
        file=sys.stderr,
    )
    try:
        yield masked
    finally:
        masked.rename(installed)
        try:
            mask_root.rmdir()
        except OSError:
            pass


def parse_frontmatter(content: str) -> dict:
    """Parse SKILL.md YAML frontmatter into a dict.

    Raises ValueError with a human-readable reason on malformed frontmatter.
    """
    content = content.replace("\r\n", "\n")
    if not content.startswith("---"):
        raise ValueError("SKILL.md missing frontmatter (no opening ---)")
    match = FRONTMATTER_PATTERN.match(content)
    if not match:
        raise ValueError("SKILL.md missing frontmatter (no closing ---)")
    try:
        frontmatter = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        raise ValueError(f"Invalid YAML in frontmatter: {exc}") from exc
    if not isinstance(frontmatter, dict):
        raise ValueError("Frontmatter must be a YAML dictionary")
    return frontmatter


def parse_skill_md(skill_path: Path) -> tuple[str, str, str]:
    """Parse a SKILL.md file, returning (name, description, full_content).

    The description is whitespace-normalized to a single line, since callers
    embed it in eval prompts and generated frontmatter.
    """
    content = (skill_path / "SKILL.md").read_text()
    frontmatter = parse_frontmatter(content)
    name = str(frontmatter.get("name") or "").strip()
    description = " ".join(str(frontmatter.get("description") or "").split())
    return name, description, content
