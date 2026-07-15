#!/usr/bin/env python3
"""Generate Codex agents/openai.yaml metadata for a skill.

Run as a module so shared helpers resolve: `uv run python -m scripts.generate_openai_yaml`.
"""

import argparse
import hashlib
import sys
from pathlib import Path

from scripts.utils import parse_frontmatter

ACRONYMS = {
    "AI",
    "API",
    "CI",
    "CLI",
    "GH",
    "LLM",
    "MCP",
    "PDF",
    "PR",
    "SQL",
    "UI",
    "URL",
}

BRANDS = {
    "codex": "Codex",
    "github": "GitHub",
    "openai": "OpenAI",
    "openapi": "OpenAPI",
    "sqlite": "SQLite",
}

SMALL_WORDS = {"and", "for", "in", "of", "or", "to", "up", "with"}

ALLOWED_INTERFACE_KEYS = {
    "brand_color",
    "default_prompt",
    "display_name",
    "icon_large",
    "icon_small",
    "short_description",
}


def yaml_quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
    return f'"{escaped}"'


def read_frontmatter(skill_dir: Path) -> dict:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        raise ValueError(f"SKILL.md not found in {skill_dir}")
    return parse_frontmatter(skill_md.read_text())


def format_display_name(skill_name: str) -> str:
    words = [word for word in skill_name.split("-") if word]
    formatted = []
    for index, word in enumerate(words):
        lower = word.lower()
        upper = word.upper()
        if upper in ACRONYMS:
            formatted.append(upper)
        elif lower in BRANDS:
            formatted.append(BRANDS[lower])
        elif index > 0 and lower in SMALL_WORDS:
            formatted.append(lower)
        else:
            formatted.append(word[:1].upper() + word[1:])
    return " ".join(formatted)


def normalize_short_description(description: str, display_name: str) -> str:
    text = " ".join(description.split())
    text = text.rstrip(".")

    if 25 <= len(text) <= 64:
        return text

    fallback = f"Use {display_name} workflows in Codex"
    if 25 <= len(fallback) <= 64:
        return fallback

    compact = f"{display_name} workflow helper"
    if len(compact) < 25:
        compact = f"{compact} for Codex"
    if len(compact) > 64:
        compact = compact[:64].rstrip()
    return compact


def default_prompt_for(skill_name: str, description: str) -> str:
    text = " ".join(description.split()).rstrip(".")
    if not text:
        return f"Use ${skill_name} to help with this task."
    lower = text.lower()
    for prefix in ("use this skill when ", "use when "):
        if lower.startswith(prefix):
            body = text[len(prefix):].strip()
            return f"Use ${skill_name} when {body[:96].rstrip()}."
    return f"Use ${skill_name} to {text[:96].rstrip()}."


def parse_interface_overrides(raw_overrides: list[str]) -> dict[str, str]:
    overrides = {}
    for item in raw_overrides:
        if "=" not in item:
            raise ValueError(f"Invalid interface override '{item}'. Use key=value.")
        key, value = item.split("=", 1)
        key = key.strip()
        value = value.strip()
        if key not in ALLOWED_INTERFACE_KEYS:
            allowed = ", ".join(sorted(ALLOWED_INTERFACE_KEYS))
            raise ValueError(f"Unknown interface field '{key}'. Allowed: {allowed}")
        overrides[key] = value
    return overrides


def build_openai_yaml(skill_dir: Path, raw_overrides: list[str] | None = None) -> str:
    frontmatter = read_frontmatter(skill_dir)
    skill_name = frontmatter.get("name")
    description = frontmatter.get("description", "")
    if not isinstance(skill_name, str) or not skill_name.strip():
        raise ValueError("Frontmatter 'name' is missing or invalid")
    if not isinstance(description, str):
        raise ValueError("Frontmatter 'description' must be a string")

    skill_name = skill_name.strip()
    description = description.strip()
    overrides = parse_interface_overrides(raw_overrides or [])

    display_name = overrides.get("display_name") or format_display_name(skill_name)
    short_description = overrides.get("short_description") or normalize_short_description(
        description,
        display_name,
    )
    default_prompt = overrides.get("default_prompt") or default_prompt_for(skill_name, description)

    if not display_name.strip():
        raise ValueError("display_name must not be empty")
    if not 25 <= len(short_description) <= 64:
        raise ValueError(f"short_description must be 25-64 characters (got {len(short_description)})")
    if f"${skill_name}" not in default_prompt:
        raise ValueError(f"default_prompt must mention ${skill_name}")

    interface = {
        "display_name": display_name,
        "short_description": short_description,
        "default_prompt": default_prompt,
    }
    for key in ("icon_small", "icon_large", "brand_color"):
        if key in overrides:
            interface[key] = overrides[key]

    source_hash = hashlib.sha256((skill_dir / "SKILL.md").read_bytes()).hexdigest()
    lines = [
        f"# skill-forge-source-sha256: {source_hash}",
        "interface:",
    ]
    for key, value in interface.items():
        lines.append(f"  {key}: {yaml_quote(value)}")
    return "\n".join(lines) + "\n"


def write_openai_yaml(skill_dir: Path, raw_overrides: list[str] | None = None) -> Path:
    content = build_openai_yaml(skill_dir, raw_overrides)
    agents_dir = skill_dir / "agents"
    agents_dir.mkdir(parents=True, exist_ok=True)
    output_path = agents_dir / "openai.yaml"
    output_path.write_text(content)
    return output_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Create agents/openai.yaml for a skill directory")
    parser.add_argument("skill_dir", help="Path to the skill directory")
    parser.add_argument(
        "--interface",
        action="append",
        default=[],
        help="Interface override in key=value format. Repeat for multiple fields.",
    )
    args = parser.parse_args()

    skill_dir = Path(args.skill_dir).resolve()
    if not skill_dir.exists():
        print(f"[ERROR] Skill directory not found: {skill_dir}", file=sys.stderr)
        return 1
    if not skill_dir.is_dir():
        print(f"[ERROR] Path is not a directory: {skill_dir}", file=sys.stderr)
        return 1

    try:
        output_path = write_openai_yaml(skill_dir, args.interface)
    except ValueError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    print(f"[OK] Created {output_path.relative_to(skill_dir)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
