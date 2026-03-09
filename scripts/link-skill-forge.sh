#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
REPO_ROOT=$(cd "${SCRIPT_DIR}/.." && pwd)
cd "$REPO_ROOT"

SKILL_NAME="skill-forge"
SKILL_SOURCE="plugins/agent-skills/skills/$SKILL_NAME"

SKILL_DIRS=(
  ".agents/skills"
  ".claude/skills"
  ".codex/skills"
  ".gemini/skills"
  ".cursor/skills"
  ".opencode/skills"
)

for dir in "${SKILL_DIRS[@]}"; do
  if [ ! -d "$dir" ]; then
    echo "SKIP: $dir (not found)"
    continue
  fi

  ln -sf "../../${SKILL_SOURCE}" "$dir/$SKILL_NAME"
  echo "LINK: $dir/$SKILL_NAME -> ../../${SKILL_SOURCE}"
done
