#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
PROJECT_ROOT=$(cd "$SCRIPT_DIR/.." && pwd)
SKILL_FORGE="$PROJECT_ROOT/plugins/agent-skills/skills/j5ik2o-skill-forge"
export UV_PROJECT_ENVIRONMENT="${UV_PROJECT_ENVIRONMENT:-${TMPDIR:-/tmp}/j5ik2o-skill-forge-venv}"

cd "$SKILL_FORGE"

uv run python -m scripts.generate_openai_yaml ../../../git/skills/j5ik2o-git-commit \
  --interface 'display_name=Git Commit' \
  --interface 'short_description=Create safe Conventional Commits' \
  --interface 'default_prompt=Use $j5ik2o-git-commit to commit these changes.'

uv run python -m scripts.generate_openai_yaml ../../../github/skills/j5ik2o-deep-research-read-me \
  --interface 'display_name=README Research' \
  --interface 'short_description=Create and review GitHub OSS READMEs' \
  --interface 'default_prompt=Use $j5ik2o-deep-research-read-me to improve this README.'

uv run python -m scripts.generate_openai_yaml ../../../github/skills/j5ik2o-gh-issue-organizer \
  --interface 'display_name=GitHub Issue Organizer' \
  --interface 'short_description=Triage and organize GitHub issues' \
  --interface 'default_prompt=Use $j5ik2o-gh-issue-organizer to triage open GitHub issues.'
