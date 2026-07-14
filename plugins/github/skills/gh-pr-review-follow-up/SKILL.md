---
name: gh-pr-review-follow-up
description: Help address review/issue comments on the open GitHub PR for the current branch using gh CLI; verify gh auth first and prompt the user to authenticate if not logged in.
metadata:
  short-description: Address comments in a GitHub PR review
---

# GitHub PR Review Follow-up

Guide to find the open PR for the current branch and address its comments with gh CLI. Run all `gh` commands with network access permitted by the active agent runtime.

Prereq: ensure `gh` is authenticated (for example, run `gh auth login` once), then run `gh auth status` so `gh` commands succeed. If the runtime blocks network access, request its standard shell or network permission and retry.

## 1) Inspect comments needing attention

- Run the bundled `scripts/fetch_comments.py` by absolute path; it prints all comments and review threads on the PR.
  - In Claude Code, run `python "${CLAUDE_SKILL_DIR}/scripts/fetch_comments.py"`.
  - In other runtimes, resolve the installed skill directory first. Do not treat `scripts/fetch_comments.py` as relative to the target repository.

## 2) Ask the user for clarification

- Number all the review threads and comments and provide a short summary of what would be required to apply a fix for it.
- Ask the user which numbered comments should be addressed.

## 3) If user chooses comments

- Apply fixes for the selected comments.

Notes:

- If `gh` hits auth or rate-limit issues mid-run, prompt the user to re-authenticate with `gh auth login`, then retry.
