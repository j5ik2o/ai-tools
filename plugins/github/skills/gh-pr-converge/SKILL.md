---
name: gh-pr-converge
description: Address unresolved PR review feedback with the gh-pr-review-follow-up skill and fix failing PR checks until no actionable review threads remain and all required checks are green. Use when finishing a pull request requires both review-comment resolution and CI convergence.
---

# GitHub PR Convergence

## Trigger

Need to finish a branch or pull request by resolving actionable review feedback and iterating on CI failures until both review threads and required checks converge.

Use `gh pr checks` as the source of truth. It includes all PR-attached checks, while `gh run list` only covers GitHub Actions.

## Workflow

1. Resolve the PR for the current branch.
2. At the start of every iteration, invoke the `gh-pr-review-follow-up` skill to inspect unresolved review threads, implement all unambiguous actionable fixes, and obtain any approval that skill requires before replying to or resolving threads.
3. Validate, commit, and push accepted review fixes when the request authorizes those remote writes.
4. Inspect the complete PR check set before waiting.
5. If checks already failed, diagnose the failures, apply the smallest scoped fixes, validate, commit, and push them.
6. If checks are pending, watch with `gh pr checks --watch --fail-fast`.
7. After every push, return to step 2 before checking CI again; finish only when a final thread-aware review read finds no unresolved actionable feedback and the complete required check set is green.

## Commands

```bash
# Resolve the active PR
gh pr view --json number,url,headRefName

# Inspect all attached checks
gh pr checks --json name,bucket,state,workflow,link

# Watch pending checks and fail fast
gh pr checks --watch --fail-fast

# GitHub Actions logs, when the failing check links to a GHA run
gh run view <run-id> --log-failed
```

## Guardrails

- Treat the `gh-pr-review-follow-up` skill as the source of truth for review-thread actionability and resolution state; do not infer thread state from flat comments.
- Before the first remote mutation, obtain explicit approval if the request does not already authorize comment replies, thread resolution, commits, and pushes.
- Keep each fix scoped to a single failure cause when possible.
- Do not bypass hooks (`--no-verify`) to force progress.
- If the failure is clearly unrelated to the PR and appears fixed on main, merge latest main instead of bloating the PR with unrelated fixes.
- If failures are flaky, retry once and report flake evidence.
- Re-run `gh pr checks --json name,bucket,state,workflow,link` after every push; the check set can change.
- Do not report completion while either actionable review threads remain unresolved or required checks are pending or failing.

## Output

- Addressed, skipped, and remaining review threads
- Current CI status
- Failure summary and fixes applied
- Commits and pushes performed
- PR URL once review threads are resolved and checks are green
