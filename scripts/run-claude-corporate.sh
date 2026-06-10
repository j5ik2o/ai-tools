#fix: update TAKT-SDD slides with revised event details and contributor info- Updated event title and version for accuracy.
- Added contributor details highlighting key contributions to TAKT.!/usr/bin/env bash

export CLAUDE_CONFIG_DIR="${HOME}/.claude"
unset CLAUDE_CODE_OAUTH_TOKEN

exec mise exec -- claude --dangerously-skip-permissions "$@"
