"""Tests for scripts.quick_validate module."""

from pathlib import Path

from scripts.quick_validate import validate_skill


def write_skill(skill_dir: Path, frontmatter: str = "") -> None:
    skill_dir.mkdir(parents=True, exist_ok=True)
    if not frontmatter:
        frontmatter = (
            "name: test-skill\n"
            "description: Test skill\n"
        )
    (skill_dir / "SKILL.md").write_text(f"---\n{frontmatter}---\n\n# Test\n")


class TestPlatformFrontmatter:
    def test_auto_accepts_claude_frontmatter(self, tmp_path):
        write_skill(
            tmp_path,
            "name: test-skill\n"
            "description: Test skill\n"
            "disable-model-invocation: true\n"
            "user-invocable: false\n"
            "when_to_use: Use for tests\n"
            "argument-hint: '[file]'\n",
        )

        valid, message = validate_skill(tmp_path)

        assert valid is True
        assert message == "Skill is valid!"

    def test_claude_accepts_latest_frontmatter_keys(self, tmp_path):
        write_skill(
            tmp_path,
            "name: test-skill\n"
            "description: Test skill\n"
            "allowed-tools: Read, Bash\n"
            "disallowed-tools: WebFetch\n"
            "disable-model-invocation: true\n"
            "user-invocable: true\n"
            "when_to_use: Use for tests\n"
            "argument-hint: '[file]'\n"
            "arguments:\n"
            "  file: Required path\n"
            "model: claude-sonnet-4-5\n"
            "effort: high\n"
            "context: fork\n"
            "agent: reviewer\n"
            "hooks:\n"
            "  Stop: echo done\n"
            "paths:\n"
            "  - '**/*.py'\n"
            "shell: bash\n",
        )

        valid, message = validate_skill(tmp_path, platform="claude")

        assert valid is True
        assert message == "Skill is valid!"

    def test_codex_rejects_claude_only_frontmatter(self, tmp_path):
        write_skill(
            tmp_path,
            "name: test-skill\n"
            "description: Test skill\n"
            "disable-model-invocation: true\n",
        )

        valid, message = validate_skill(tmp_path, platform="codex")

        assert valid is False
        assert "disable-model-invocation" in message
        assert "platform 'codex'" in message

    def test_codex_accepts_builtin_style_uppercase_name(self, tmp_path):
        write_skill(
            tmp_path,
            'name: "Spreadsheets"\n'
            'description: Test skill\n',
        )

        valid, message = validate_skill(tmp_path, platform="codex")

        assert valid is True
        assert message == "Skill is valid!"

    def test_unknown_platform_returns_error(self, tmp_path):
        write_skill(tmp_path)

        valid, message = validate_skill(tmp_path, platform="other")

        assert valid is False
        assert "Unknown platform" in message


class TestOpenAiYaml:
    def test_codex_validates_openai_yaml_when_present(self, tmp_path):
        write_skill(tmp_path)
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()
        (agents_dir / "openai.yaml").write_text(
            'interface:\n'
            '  display_name: "Test Skill"\n'
            '  short_description: "Test helper"\n'
            '  default_prompt: "Use $test-skill to do the task."\n'
            'policy:\n'
            '  allow_implicit_invocation: true\n'
            'dependencies:\n'
            '  tools:\n'
            '    - type: "mcp"\n'
            '      value: "github"\n'
            '      description: "GitHub MCP server"\n'
            '      transport: "streamable_http"\n'
            '      url: "https://example.com/mcp/"\n'
        )

        valid, message = validate_skill(tmp_path, platform="codex")

        assert valid is True
        assert message == "Skill is valid!"

    def test_codex_rejects_invalid_openai_yaml_interface_value(self, tmp_path):
        write_skill(tmp_path)
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()
        (agents_dir / "openai.yaml").write_text(
            'interface:\n'
            '  display_name: 123\n'
        )

        valid, message = validate_skill(tmp_path, platform="codex")

        assert valid is False
        assert "interface.display_name must be a string" in message

    def test_auto_validates_openai_yaml_when_present(self, tmp_path):
        write_skill(tmp_path)
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()
        (agents_dir / "openai.yaml").write_text("unexpected: true\n")

        valid, message = validate_skill(tmp_path)

        assert valid is False
        assert "Unexpected key(s) in agents/openai.yaml" in message

    def test_codex_rejects_invalid_openai_yaml_policy_value(self, tmp_path):
        write_skill(tmp_path)
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()
        (agents_dir / "openai.yaml").write_text(
            'policy:\n'
            '  allow_implicit_invocation: "yes"\n'
        )

        valid, message = validate_skill(tmp_path, platform="codex")

        assert valid is False
        assert "policy.allow_implicit_invocation must be a boolean" in message

    def test_codex_rejects_invalid_openai_yaml_dependency_tool_value(self, tmp_path):
        write_skill(tmp_path)
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()
        (agents_dir / "openai.yaml").write_text(
            'dependencies:\n'
            '  tools:\n'
            '    - type: "mcp"\n'
            '      value: ["github"]\n'
        )

        valid, message = validate_skill(tmp_path, platform="codex")

        assert valid is False
        assert "dependencies.tools[0].value must be a string" in message
