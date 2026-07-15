"""Tests for scripts.utils module."""

import os
import scripts.utils as utils_module
from pathlib import Path
from unittest.mock import patch

import pytest

from scripts.utils import (
    CLI_CLAUDE,
    CLI_CODEX,
    detect_cli,
    find_project_root,
    get_cli_command,
    mask_installed_skill,
    parse_skill_md,
    project_skill_install_dir,
    resolve_cli_home,
    resolve_skill_dir,
)


class TestGetCliCommand:
    def test_explicit_path_takes_priority(self):
        result = get_cli_command(CLI_CLAUDE, explicit_path="/custom/bin/claude")
        assert result == "/custom/bin/claude"

    def test_explicit_path_ignores_env(self):
        with patch.dict(os.environ, {"SKILL_FORGE_CLAUDE_COMMAND": "/env/claude"}):
            result = get_cli_command(CLI_CLAUDE, explicit_path="/arg/claude")
            assert result == "/arg/claude"

    def test_claude_default(self):
        with patch.dict(os.environ, {}, clear=True):
            result = get_cli_command(CLI_CLAUDE)
            assert result == "claude"

    def test_codex_default(self):
        with patch.dict(os.environ, {}, clear=True):
            result = get_cli_command(CLI_CODEX)
            assert result == "codex"

    def test_claude_env_override(self):
        with patch.dict(os.environ, {"SKILL_FORGE_CLAUDE_COMMAND": "/opt/claude"}):
            result = get_cli_command(CLI_CLAUDE)
            assert result == "/opt/claude"

    def test_codex_env_override(self):
        with patch.dict(os.environ, {"SKILL_FORGE_CODEX_COMMAND": "/opt/codex"}):
            result = get_cli_command(CLI_CODEX)
            assert result == "/opt/codex"

    def test_unknown_cli_type_returns_as_is(self):
        result = get_cli_command("unknown")
        assert result == "unknown"


class TestDetectCli:
    def test_explicit_claude(self):
        assert detect_cli("claude") == CLI_CLAUDE

    def test_explicit_codex(self):
        assert detect_cli("codex") == CLI_CODEX

    def test_explicit_invalid_raises(self):
        with pytest.raises(ValueError, match="Unknown CLI"):
            detect_cli("invalid")

    def test_env_var_claude(self):
        with patch.dict(os.environ, {"SKILL_FORGE_EVAL_CLI": "claude"}):
            with patch("scripts.utils.shutil.which", return_value=None):
                assert detect_cli() == CLI_CLAUDE

    def test_env_var_codex(self):
        with patch.dict(os.environ, {"SKILL_FORGE_EVAL_CLI": "codex"}):
            with patch("scripts.utils.shutil.which", return_value=None):
                assert detect_cli() == CLI_CODEX

    def test_env_var_invalid_raises(self):
        with patch.dict(os.environ, {"SKILL_FORGE_EVAL_CLI": "bad"}):
            with pytest.raises(ValueError, match="Unknown SKILL_FORGE_EVAL_CLI"):
                detect_cli()

    def test_auto_detect_claude_first(self):
        with patch.dict(os.environ, {}, clear=True):
            with patch("scripts.utils.shutil.which", side_effect=lambda cmd: "/usr/bin/claude" if cmd == "claude" else None):
                assert detect_cli() == CLI_CLAUDE

    def test_auto_detect_codex_fallback(self):
        with patch.dict(os.environ, {}, clear=True):
            with patch("scripts.utils.shutil.which", side_effect=lambda cmd: "/usr/bin/codex" if cmd == "codex" else None):
                assert detect_cli() == CLI_CODEX

    def test_auto_detect_neither_raises(self):
        with patch.dict(os.environ, {}, clear=True):
            with patch("scripts.utils.shutil.which", return_value=None):
                with pytest.raises(RuntimeError, match="Neither"):
                    detect_cli()

    def test_explicit_overrides_env(self):
        with patch.dict(os.environ, {"SKILL_FORGE_EVAL_CLI": "codex"}):
            assert detect_cli("claude") == CLI_CLAUDE

    def test_auto_detect_both_warns_and_defaults_claude(self, capsys):
        with patch.dict(os.environ, {}, clear=True):
            with patch("scripts.utils.shutil.which", return_value="/usr/bin/found"):
                result = detect_cli()
                assert result == CLI_CLAUDE
                captured = capsys.readouterr()
                assert "Both" in captured.err


class TestFindProjectRoot:
    def test_finds_claude_root(self, tmp_path):
        project = tmp_path / "myproject"
        (project / ".claude").mkdir(parents=True)
        sub = project / "src" / "deep"
        sub.mkdir(parents=True)

        with patch("scripts.utils.Path.cwd", return_value=sub):
            result = find_project_root(CLI_CLAUDE)
            assert result == project

    def test_finds_codex_root(self, tmp_path):
        project = tmp_path / "myproject"
        (project / ".codex").mkdir(parents=True)
        sub = project / "src"
        sub.mkdir(parents=True)

        with patch("scripts.utils.Path.cwd", return_value=sub):
            result = find_project_root(CLI_CODEX)
            assert result == project

    def test_returns_cwd_when_not_found(self, tmp_path):
        sub = tmp_path / "no_project"
        sub.mkdir(parents=True)

        with patch("scripts.utils.Path.cwd", return_value=sub):
            result = find_project_root(CLI_CLAUDE)
            assert result == sub

    def test_falls_back_to_git_root_when_home_override_is_external(self, tmp_path):
        project = tmp_path / "myproject"
        (project / ".git").mkdir(parents=True)
        sub = project / "src" / "deep"
        sub.mkdir(parents=True)

        with patch.dict(os.environ, {"CODEX_HOME": str(tmp_path / "external-codex-home")}, clear=True):
            with patch("scripts.utils.Path.cwd", return_value=sub):
                result = find_project_root(CLI_CODEX)
                assert result == project

    def test_prefers_cli_home_marker_over_nearer_git_root(self, tmp_path):
        project = tmp_path / "myproject"
        (project / ".codex").mkdir(parents=True)
        nested_repo = project / "nested" / "repo"
        (nested_repo / ".git").mkdir(parents=True)
        sub = nested_repo / "src"
        sub.mkdir(parents=True)

        with patch("scripts.utils.Path.cwd", return_value=sub):
            result = find_project_root(CLI_CODEX)
            assert result == project


class TestResolveCliHome:
    def test_claude_home_uses_project_root_by_default(self, tmp_path):
        project = tmp_path / "project"
        with patch.dict(os.environ, {}, clear=True):
            result = resolve_cli_home(CLI_CLAUDE, project)
            assert result == project / ".claude"

    def test_codex_home_uses_project_root_by_default(self, tmp_path):
        project = tmp_path / "project"
        with patch.dict(os.environ, {}, clear=True):
            result = resolve_cli_home(CLI_CODEX, project)
            assert result == project / ".codex"

    def test_claude_home_honors_override(self, tmp_path):
        override = tmp_path / "custom-claude-home"
        with patch.dict(os.environ, {"SKILL_FORGE_CLAUDE_HOME": str(override)}, clear=True):
            result = resolve_cli_home(CLI_CLAUDE, tmp_path / "project")
            assert result == override

    def test_codex_home_honors_codex_home(self, tmp_path):
        override = tmp_path / "custom-codex-home"
        with patch.dict(os.environ, {"CODEX_HOME": str(override)}, clear=True):
            result = resolve_cli_home(CLI_CODEX, tmp_path / "project")
            assert result == override

    def test_override_takes_priority_over_local_home(self, tmp_path):
        project = tmp_path / "project"
        (project / ".codex").mkdir(parents=True)
        override = tmp_path / "custom-codex-home"
        with patch.dict(os.environ, {"CODEX_HOME": str(override)}, clear=True):
            result = resolve_cli_home(CLI_CODEX, project)
            assert result == override

    def test_claude_resolve_skill_dir_uses_cli_home(self, tmp_path):
        override = tmp_path / "custom-claude-home"
        with patch.dict(os.environ, {"SKILL_FORGE_CLAUDE_HOME": str(override)}, clear=True):
            result = resolve_skill_dir(CLI_CLAUDE, tmp_path / "project")
            assert result == override / "skills"

    def test_codex_resolve_skill_dir_uses_repo_agents_skills(self, tmp_path):
        project = tmp_path / "project"
        with patch.dict(os.environ, {}, clear=True):
            result = resolve_skill_dir(CLI_CODEX, project)
            assert result == project / ".agents" / "skills"

    def test_codex_resolve_skill_dir_ignores_codex_home_for_repo_scope(self, tmp_path):
        project = tmp_path / "project"
        override = tmp_path / "custom-codex-home"
        with patch.dict(os.environ, {"CODEX_HOME": str(override)}, clear=True):
            result = resolve_skill_dir(CLI_CODEX, project)
            assert result == project / ".agents" / "skills"

    def test_utils_module_does_not_expose_resolve_command_dir(self):
        assert not hasattr(utils_module, "resolve_command_dir")


class TestParseSkillMd:
    def test_simple_frontmatter(self, tmp_path):
        skill_md = tmp_path / "SKILL.md"
        skill_md.write_text(
            "---\n"
            "name: test-skill\n"
            "description: A test skill for testing\n"
            "---\n\n"
            "# Test Skill\n\nBody content here.\n"
        )
        name, desc, content = parse_skill_md(tmp_path)
        assert name == "test-skill"
        assert desc == "A test skill for testing"
        assert "Body content here." in content

    def test_quoted_values(self, tmp_path):
        skill_md = tmp_path / "SKILL.md"
        skill_md.write_text(
            '---\n'
            'name: "quoted-skill"\n'
            "description: 'single quoted desc'\n"
            '---\n\n'
            '# Body\n'
        )
        name, desc, _ = parse_skill_md(tmp_path)
        assert name == "quoted-skill"
        assert desc == "single quoted desc"

    def test_multiline_pipe(self, tmp_path):
        skill_md = tmp_path / "SKILL.md"
        skill_md.write_text(
            "---\n"
            "name: multi-skill\n"
            "description: |\n"
            "  First line of description.\n"
            "  Second line of description.\n"
            "---\n\n"
            "# Body\n"
        )
        name, desc, _ = parse_skill_md(tmp_path)
        assert name == "multi-skill"
        assert desc == "First line of description. Second line of description."

    def test_multiline_folded(self, tmp_path):
        skill_md = tmp_path / "SKILL.md"
        skill_md.write_text(
            "---\n"
            "name: folded-skill\n"
            "description: >\n"
            "  Folded line one.\n"
            "  Folded line two.\n"
            "---\n\n"
            "# Body\n"
        )
        name, desc, _ = parse_skill_md(tmp_path)
        assert name == "folded-skill"
        assert desc == "Folded line one. Folded line two."

    def test_missing_opening_frontmatter_raises(self, tmp_path):
        skill_md = tmp_path / "SKILL.md"
        skill_md.write_text("name: bad\n---\n")
        with pytest.raises(ValueError, match="no opening"):
            parse_skill_md(tmp_path)

    def test_missing_closing_frontmatter_raises(self, tmp_path):
        skill_md = tmp_path / "SKILL.md"
        skill_md.write_text("---\nname: bad\n")
        with pytest.raises(ValueError, match="no closing"):
            parse_skill_md(tmp_path)

    def test_invalid_yaml_raises(self, tmp_path):
        skill_md = tmp_path / "SKILL.md"
        skill_md.write_text(
            "---\n"
            "name: bad-skill\n"
            "description: broken: because: of: colons\n"
            "---\n"
        )
        with pytest.raises(ValueError, match="Invalid YAML"):
            parse_skill_md(tmp_path)

    def test_non_dict_frontmatter_raises(self, tmp_path):
        skill_md = tmp_path / "SKILL.md"
        skill_md.write_text("---\n- just\n- a list\n---\n")
        with pytest.raises(ValueError, match="YAML dictionary"):
            parse_skill_md(tmp_path)

    def test_crlf_line_endings_are_accepted(self, tmp_path):
        skill_md = tmp_path / "SKILL.md"
        skill_md.write_bytes(
            b"---\r\n"
            b"name: crlf-skill\r\n"
            b"description: A skill saved with Windows line endings\r\n"
            b"---\r\n\r\n"
            b"# Body\r\n"
        )
        name, desc, _ = parse_skill_md(tmp_path)
        assert name == "crlf-skill"
        assert desc == "A skill saved with Windows line endings"


class TestProjectSkillInstallDir:
    def test_claude_uses_project_claude_skills(self, tmp_path):
        assert project_skill_install_dir(CLI_CLAUDE, tmp_path) == tmp_path / ".claude" / "skills"

    def test_codex_uses_project_agents_skills(self, tmp_path):
        assert project_skill_install_dir(CLI_CODEX, tmp_path) == tmp_path / ".agents" / "skills"

    def test_ignores_home_overrides(self, tmp_path):
        with patch.dict(os.environ, {"SKILL_FORGE_CLAUDE_HOME": "/elsewhere"}):
            assert project_skill_install_dir(CLI_CLAUDE, tmp_path) == tmp_path / ".claude" / "skills"


class TestMaskInstalledSkill:
    def test_noop_when_skill_not_installed(self, tmp_path):
        with mask_installed_skill(CLI_CLAUDE, "ghost", tmp_path) as masked:
            assert masked is None

    def test_masks_and_restores_installed_skill(self, tmp_path):
        installed = tmp_path / ".claude" / "skills" / "foo"
        installed.mkdir(parents=True)
        (installed / "SKILL.md").write_text("content")

        with mask_installed_skill(CLI_CLAUDE, "foo", tmp_path) as masked:
            assert not installed.exists()
            assert (masked / "SKILL.md").read_text() == "content"

        assert (installed / "SKILL.md").read_text() == "content"
        assert not masked.parent.exists()

    def test_restores_on_exception(self, tmp_path):
        installed = tmp_path / ".agents" / "skills" / "foo"
        installed.mkdir(parents=True)

        with pytest.raises(RuntimeError):
            with mask_installed_skill(CLI_CODEX, "foo", tmp_path):
                raise RuntimeError("boom")

        assert installed.exists()

    def test_masked_relative_symlink_still_resolves(self, tmp_path):
        real = tmp_path / "plugins" / "foo"
        real.mkdir(parents=True)
        (real / "SKILL.md").write_text("real content")
        skills = tmp_path / ".claude" / "skills"
        skills.mkdir(parents=True)
        (skills / "foo").symlink_to(Path("..") / ".." / "plugins" / "foo")

        with mask_installed_skill(CLI_CLAUDE, "foo", tmp_path) as masked:
            assert (masked / "SKILL.md").read_text() == "real content"

        assert (skills / "foo" / "SKILL.md").read_text() == "real content"
        assert (skills / "foo").is_symlink()
