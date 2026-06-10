#!/usr/bin/env bash

export CLAUDE_IDENTITY="personal"
export CLAUDE_CONFIG_DIR="${HOME}/.claude-${CLAUDE_IDENTITY}"
unset CLAUDE_CODE_OAUTH_TOKEN

exec mise exec -- claude --dangerously-skip-permissions "$@"
