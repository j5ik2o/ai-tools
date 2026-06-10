#!/usr/bin/env bash

export CODEX_HOME="${HOME}/.codex"
mkdir -p "${CODEX_HOME}"
exec mise exec -- codex --dangerously-bypass-approvals-and-sandbox "$@"
