#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
PROJECT_ROOT=$(cd "$SCRIPT_DIR/.." && pwd)
SKILL_FORGE="$PROJECT_ROOT/plugins/agent-skills/skills/skill-forge"

cd "$SKILL_FORGE"

uv run python scripts/generate_openai_yaml.py ../../../git/skills/git-commit \
  --interface 'display_name=Git Commit' \
  --interface 'short_description=Create safe Conventional Commits' \
  --interface 'default_prompt=Use $git-commit to commit these changes.'

uv run python scripts/generate_openai_yaml.py ../../../github/skills/deep-research-read-me \
  --interface 'display_name=README Research' \
  --interface 'short_description=Create and review GitHub OSS READMEs' \
  --interface 'default_prompt=Use $deep-research-read-me to improve this README.'

uv run python scripts/generate_openai_yaml.py ../../../github/skills/gh-issue-organizer \
  --interface 'display_name=GitHub Issue Organizer' \
  --interface 'short_description=Triage and organize GitHub issues' \
  --interface 'default_prompt=Use $gh-issue-organizer to triage open GitHub issues.'
