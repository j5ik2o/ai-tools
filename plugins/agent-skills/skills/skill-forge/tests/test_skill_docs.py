"""Regression tests for skill-forge docs and dependency metadata."""

from pathlib import Path

from scripts.utils import parse_skill_md


SKILL_DIR = Path(__file__).parent.parent


class TestSkillDocs:
    def test_frontmatter_description_mentions_existing_skill_and_boundary(self):
        _, description, _ = parse_skill_md(SKILL_DIR)

        assert "improving an existing skill" in description
        assert "generic automation/workflow setup" in description
        assert "GitHub Actions" in description
        assert "database migrations" in description
        assert "turn this workflow into a skill" in description

    def test_description_optimization_requires_boundary_extraction(self):
        skill_md = (SKILL_DIR / "SKILL.md").read_text()

        assert "read the target skill's `SKILL.md`" in skill_md
        assert "`helps with`" in skill_md
        assert "`should not help with`" in skill_md

    def test_description_optimization_does_not_reference_anthropic_api(self):
        skill_md = (SKILL_DIR / "SKILL.md").read_text()

        assert "improvement step always uses the Anthropic API directly" not in skill_md
        assert "No separate Anthropic API client setup is required" in skill_md

    def test_codex_openai_yaml_flow_is_documented(self):
        skill_md = (SKILL_DIR / "SKILL.md").read_text()
        reference = (SKILL_DIR / "references" / "openai_yaml.md").read_text()

        assert "references/openai_yaml.md" in skill_md
        assert "scripts/generate_openai_yaml.py" in skill_md
        assert "--strict-openai-yaml" in skill_md
        assert "display_name" in reference
        assert "short_description" in reference
        assert "default_prompt" in reference
        assert "Difference from OpenAI skill-creator" in reference

    def test_trigger_eval_boundaries_are_documented(self):
        skill_md = (SKILL_DIR / "SKILL.md").read_text()
        reference = (SKILL_DIR / "references" / "trigger_eval_boundaries.md").read_text()
        schemas = (SKILL_DIR / "references" / "schemas.md").read_text()

        assert "references/trigger_eval_boundaries.md" in skill_md
        assert "Claude Code detector" in reference
        assert "Codex CLI detector" in reference
        assert "false positives" in reference
        assert "false negatives" in reference
        assert "status" in schemas
        assert "attempted_runs" in schemas


class TestProjectMetadata:
    def test_pyproject_does_not_depend_on_anthropic(self):
        pyproject = (SKILL_DIR / "pyproject.toml").read_text()

        assert '"anthropic"' not in pyproject
