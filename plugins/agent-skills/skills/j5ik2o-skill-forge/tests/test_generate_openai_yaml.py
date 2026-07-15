"""Tests for scripts.generate_openai_yaml module."""

from pathlib import Path

import pytest
import yaml

from scripts.generate_openai_yaml import (
    build_openai_yaml,
    default_prompt_for,
    format_display_name,
    write_openai_yaml,
)
from scripts.quick_validate import validate_skill


def write_skill(skill_dir: Path, name: str = "test-skill", description: str = "") -> None:
    if not description:
        description = "Use when the user wants focused test workflow assistance."
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: {description}\n---\n\n# Test\n"
    )


class TestOpenAiYamlGeneration:
    def test_format_display_name_preserves_common_acronyms_and_brands(self):
        assert format_display_name("openai-api-helper") == "OpenAI API Helper"
        assert format_display_name("github-pr-review") == "GitHub PR Review"

    def test_build_openai_yaml_generates_required_interface_fields(self, tmp_path):
        write_skill(tmp_path, name="test-skill")

        content = build_openai_yaml(tmp_path)
        metadata = yaml.safe_load(content)

        assert content.startswith("# skill-forge-source-sha256: ")
        assert metadata["interface"]["display_name"] == "Test Skill"
        assert 25 <= len(metadata["interface"]["short_description"]) <= 64
        assert "$test-skill" in metadata["interface"]["default_prompt"]

    def test_default_prompt_turns_use_when_description_into_invocation_prompt(self):
        prompt = default_prompt_for("test-skill", "Use when the user wants focused help.")

        assert prompt == "Use $test-skill when the user wants focused help."

    def test_build_openai_yaml_accepts_interface_overrides(self, tmp_path):
        write_skill(tmp_path, name="test-skill")

        content = build_openai_yaml(
            tmp_path,
            [
                "display_name=Custom Skill",
                "short_description=Custom skill workflow helper",
                "default_prompt=Use $test-skill for this workflow.",
                "brand_color=#3B82F6",
            ],
        )
        metadata = yaml.safe_load(content)

        assert metadata["interface"]["display_name"] == "Custom Skill"
        assert metadata["interface"]["short_description"] == "Custom skill workflow helper"
        assert metadata["interface"]["default_prompt"] == "Use $test-skill for this workflow."
        assert metadata["interface"]["brand_color"] == "#3B82F6"

    def test_build_openai_yaml_rejects_short_description_outside_constraints(self, tmp_path):
        write_skill(tmp_path, name="test-skill")

        with pytest.raises(ValueError, match="short_description must be 25-64 characters"):
            build_openai_yaml(tmp_path, ["short_description=Too short"])

    def test_build_openai_yaml_rejects_default_prompt_without_skill_invocation(self, tmp_path):
        write_skill(tmp_path, name="test-skill")

        with pytest.raises(ValueError, match=r"default_prompt must mention \$test-skill"):
            build_openai_yaml(tmp_path, ["default_prompt=Use this helper."])


class TestStrictOpenAiYamlValidation:
    def test_strict_validation_accepts_generated_openai_yaml(self, tmp_path):
        write_skill(tmp_path, name="test-skill")
        write_openai_yaml(tmp_path)

        valid, message = validate_skill(
            tmp_path,
            platform="codex",
            strict_openai_yaml=True,
        )

        assert valid is True
        assert message == "Skill is valid!"

    def test_strict_validation_requires_openai_yaml(self, tmp_path):
        write_skill(tmp_path, name="test-skill")

        valid, message = validate_skill(
            tmp_path,
            platform="codex",
            strict_openai_yaml=True,
        )

        assert valid is False
        assert message == "agents/openai.yaml not found"

    def test_strict_validation_detects_stale_openai_yaml(self, tmp_path):
        write_skill(tmp_path, name="test-skill")
        write_openai_yaml(tmp_path)
        skill_md = tmp_path / "SKILL.md"
        skill_md.write_text(
            "---\n"
            "name: test-skill\n"
            "description: Use when the user wants updated workflow assistance.\n"
            "---\n\n"
            "# Test\n"
        )

        valid, message = validate_skill(
            tmp_path,
            platform="codex",
            strict_openai_yaml=True,
        )

        assert valid is False
        assert "agents/openai.yaml is stale" in message
