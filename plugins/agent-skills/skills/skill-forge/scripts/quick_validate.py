#!/usr/bin/env python3
"""Quick validation script for skills."""

import argparse
import sys
import re
import yaml
from pathlib import Path

PLATFORM_AUTO = "auto"
PLATFORM_CLAUDE = "claude"
PLATFORM_CODEX = "codex"
PLATFORMS = {PLATFORM_AUTO, PLATFORM_CLAUDE, PLATFORM_CODEX}

COMMON_PROPERTIES = {"name", "description", "license", "metadata"}

CLAUDE_PROPERTIES = COMMON_PROPERTIES | {
    "agent",
    "allowed-tools",
    "argument-hint",
    "arguments",
    "compatibility",
    "context",
    "disable-model-invocation",
    "disallowed-tools",
    "effort",
    "hooks",
    "model",
    "paths",
    "shell",
    "user-invocable",
    "when_to_use",
}

CODEX_PROPERTIES = COMMON_PROPERTIES | {
    "allowed-tools",
    "compatibility",
}

OPENAI_YAML_TOP_LEVEL_KEYS = {"interface", "dependencies", "policy"}
OPENAI_YAML_INTERFACE_KEYS = {
    "brand_color",
    "default_prompt",
    "display_name",
    "icon_large",
    "icon_small",
    "short_description",
}
OPENAI_YAML_POLICY_KEYS = {"allow_implicit_invocation"}
OPENAI_YAML_DEPENDENCIES_KEYS = {"tools"}
OPENAI_YAML_TOOL_KEYS = {"type", "value", "description", "transport", "url"}


def _allowed_properties(platform: str) -> set[str]:
    if platform == PLATFORM_CLAUDE:
        return CLAUDE_PROPERTIES
    if platform == PLATFORM_CODEX:
        return CODEX_PROPERTIES
    return CLAUDE_PROPERTIES | CODEX_PROPERTIES


def _validate_openai_yaml(skill_path: Path) -> tuple[bool, str]:
    openai_yaml = skill_path / "agents" / "openai.yaml"
    if not openai_yaml.exists():
        return True, ""

    try:
        metadata = yaml.safe_load(openai_yaml.read_text())
    except yaml.YAMLError as e:
        return False, f"Invalid YAML in agents/openai.yaml: {e}"

    if not isinstance(metadata, dict):
        return False, "agents/openai.yaml must be a YAML dictionary"

    unexpected_keys = set(metadata.keys()) - OPENAI_YAML_TOP_LEVEL_KEYS
    if unexpected_keys:
        allowed = ", ".join(sorted(OPENAI_YAML_TOP_LEVEL_KEYS))
        unexpected = ", ".join(sorted(unexpected_keys))
        return False, (
            f"Unexpected key(s) in agents/openai.yaml: {unexpected}. "
            f"Allowed properties are: {allowed}"
        )

    interface = metadata.get("interface")
    if interface is not None:
        if not isinstance(interface, dict):
            return False, "agents/openai.yaml interface must be a YAML dictionary"

        unexpected_interface_keys = set(interface.keys()) - OPENAI_YAML_INTERFACE_KEYS
        if unexpected_interface_keys:
            allowed = ", ".join(sorted(OPENAI_YAML_INTERFACE_KEYS))
            unexpected = ", ".join(sorted(unexpected_interface_keys))
            return False, (
                f"Unexpected key(s) in agents/openai.yaml interface: {unexpected}. "
                f"Allowed properties are: {allowed}"
            )

        for key, value in interface.items():
            if value is not None and not isinstance(value, str):
                return False, f"agents/openai.yaml interface.{key} must be a string"

    policy = metadata.get("policy")
    if policy is not None:
        if not isinstance(policy, dict):
            return False, "agents/openai.yaml policy must be a YAML dictionary"
        unexpected_policy_keys = set(policy.keys()) - OPENAI_YAML_POLICY_KEYS
        if unexpected_policy_keys:
            allowed = ", ".join(sorted(OPENAI_YAML_POLICY_KEYS))
            unexpected = ", ".join(sorted(unexpected_policy_keys))
            return False, (
                f"Unexpected key(s) in agents/openai.yaml policy: {unexpected}. "
                f"Allowed properties are: {allowed}"
            )
        allow_implicit_invocation = policy.get("allow_implicit_invocation")
        if allow_implicit_invocation is not None and not isinstance(allow_implicit_invocation, bool):
            return False, "agents/openai.yaml policy.allow_implicit_invocation must be a boolean"

    dependencies = metadata.get("dependencies")
    if dependencies is not None:
        if not isinstance(dependencies, dict):
            return False, "agents/openai.yaml dependencies must be a YAML dictionary"
        unexpected_dependencies_keys = set(dependencies.keys()) - OPENAI_YAML_DEPENDENCIES_KEYS
        if unexpected_dependencies_keys:
            allowed = ", ".join(sorted(OPENAI_YAML_DEPENDENCIES_KEYS))
            unexpected = ", ".join(sorted(unexpected_dependencies_keys))
            return False, (
                f"Unexpected key(s) in agents/openai.yaml dependencies: {unexpected}. "
                f"Allowed properties are: {allowed}"
            )
        tools = dependencies.get("tools")
        if tools is not None:
            if not isinstance(tools, list):
                return False, "agents/openai.yaml dependencies.tools must be a YAML list"
            for index, tool in enumerate(tools):
                if not isinstance(tool, dict):
                    return False, f"agents/openai.yaml dependencies.tools[{index}] must be a YAML dictionary"
                unexpected_tool_keys = set(tool.keys()) - OPENAI_YAML_TOOL_KEYS
                if unexpected_tool_keys:
                    allowed = ", ".join(sorted(OPENAI_YAML_TOOL_KEYS))
                    unexpected = ", ".join(sorted(unexpected_tool_keys))
                    return False, (
                        f"Unexpected key(s) in agents/openai.yaml dependencies.tools[{index}]: {unexpected}. "
                        f"Allowed properties are: {allowed}"
                    )
                for key, value in tool.items():
                    if value is not None and not isinstance(value, str):
                        return False, f"agents/openai.yaml dependencies.tools[{index}].{key} must be a string"

    return True, ""


def validate_skill(skill_path, platform=PLATFORM_AUTO):
    """Basic validation of a skill"""
    if platform not in PLATFORMS:
        return False, f"Unknown platform '{platform}'. Use one of: {', '.join(sorted(PLATFORMS))}"

    skill_path = Path(skill_path)

    # Check SKILL.md exists
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return False, "SKILL.md not found"

    # Read and validate frontmatter
    content = skill_md.read_text()
    if not content.startswith('---'):
        return False, "No YAML frontmatter found"

    # Extract frontmatter
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"

    frontmatter_text = match.group(1)

    # Parse YAML frontmatter
    try:
        frontmatter = yaml.safe_load(frontmatter_text)
        if not isinstance(frontmatter, dict):
            return False, "Frontmatter must be a YAML dictionary"
    except yaml.YAMLError as e:
        return False, f"Invalid YAML in frontmatter: {e}"

    allowed_properties = _allowed_properties(platform)

    # Check for unexpected properties (excluding nested keys under metadata)
    unexpected_keys = set(frontmatter.keys()) - allowed_properties
    if unexpected_keys:
        return False, (
            f"Unexpected key(s) in SKILL.md frontmatter: {', '.join(sorted(unexpected_keys))}. "
            f"Allowed properties for platform '{platform}' are: {', '.join(sorted(allowed_properties))}"
        )

    # Check required fields
    if 'name' not in frontmatter:
        return False, "Missing 'name' in frontmatter"
    if 'description' not in frontmatter:
        return False, "Missing 'description' in frontmatter"

    # Extract name for validation
    name = frontmatter.get('name', '')
    if not isinstance(name, str):
        return False, f"Name must be a string, got {type(name).__name__}"
    name = name.strip()
    if name:
        # Codex bundled skills include uppercase display-like names; keep path-unsafe characters out.
        if not re.match(r'^[A-Za-z0-9-]+$', name):
            return False, f"Name '{name}' should use letters, digits, and hyphens only"
        if name.startswith('-') or name.endswith('-') or '--' in name:
            return False, f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens"
        # Check name length (max 64 characters per spec)
        if len(name) > 64:
            return False, f"Name is too long ({len(name)} characters). Maximum is 64 characters."

    # Extract and validate description
    description = frontmatter.get('description', '')
    if not isinstance(description, str):
        return False, f"Description must be a string, got {type(description).__name__}"
    description = description.strip()
    if description:
        # Check for angle brackets
        if '<' in description or '>' in description:
            return False, "Description cannot contain angle brackets (< or >)"
        # Check description length (max 1024 characters per spec)
        if len(description) > 1024:
            return False, f"Description is too long ({len(description)} characters). Maximum is 1024 characters."

    # Validate compatibility field if present (optional)
    compatibility = frontmatter.get('compatibility', '')
    if compatibility:
        if not isinstance(compatibility, str):
            return False, f"Compatibility must be a string, got {type(compatibility).__name__}"
        if len(compatibility) > 500:
            return False, f"Compatibility is too long ({len(compatibility)} characters). Maximum is 500 characters."

    if platform in (PLATFORM_AUTO, PLATFORM_CODEX):
        valid, message = _validate_openai_yaml(skill_path)
        if not valid:
            return valid, message

    return True, "Skill is valid!"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate a skill directory")
    parser.add_argument("skill_directory", help="Path to the skill directory")
    parser.add_argument(
        "--platform",
        choices=sorted(PLATFORMS),
        default=PLATFORM_AUTO,
        help="Validation target. Default 'auto' accepts Claude and Codex frontmatter and validates agents/openai.yaml when present.",
    )
    args = parser.parse_args()

    valid, message = validate_skill(args.skill_directory, platform=args.platform)
    print(message)
    sys.exit(0 if valid else 1)
