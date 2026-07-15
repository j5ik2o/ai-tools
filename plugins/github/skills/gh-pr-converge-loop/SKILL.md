---
name: gh-pr-converge-loop
description: >-
  Run a convergence loop for GitHub PRs by resolving base-branch merge conflicts
  first with the gh-pr-resolve-conflicts skill, addressing unresolved review
  feedback with the gh-pr-review-follow-up skill, and fixing failing PR checks.
  Restart from mergeability after every push until no conflicts or actionable
  review threads remain and all required checks are green. Use when a pull
  request must be driven continuously to a merge-ready state.
---

# GitHub PR Convergence Loop

## Trigger

Need to finish a branch or pull request by clearing merge conflicts first, resolving actionable review feedback, and iterating on CI failures until mergeability, review threads, and required checks converge.

Use `gh pr checks` as the source of truth. It includes all PR-attached checks, while `gh run list` only covers GitHub Actions.

## Workflow

1. Resolve the PR and its base branch, then inspect mergeability before review or CI work.
   - If `mergeable` is `UNKNOWN`, wait for GitHub to compute it and query again.
   - Treat `mergeable: CONFLICTING` or `mergeStateStatus: DIRTY` as a blocking conflict.
2. If the PR conflicts with its base branch, fetch and merge the latest base branch to materialize the conflicts locally.
   - When the merge stops with unresolved paths, invoke the `gh-pr-resolve-conflicts` skill (`$gh-pr-resolve-conflicts` in Codex or `/gh-pr-resolve-conflicts` in Claude Code).
   - Let that skill resolve conflicts, validate the build and relevant tests, and stage the resolved files. It must not commit, push, or tag.
   - Inspect the staged resolution, then commit and push it only when the request authorizes those remote writes.
   - After the push, return to step 1 and do not continue until the PR is no longer conflicting.
3. Invoke the `gh-pr-review-follow-up` skill to inspect unresolved review threads, implement all unambiguous actionable fixes, and obtain any approval that skill requires before replying to or resolving threads.
4. Validate, commit, and push accepted review fixes when the request authorizes those remote writes.
5. Inspect the complete PR check set before waiting.
6. If checks already failed, diagnose the failures, apply the smallest scoped fixes, validate, commit, and push them.
7. If checks are pending, watch with `gh pr checks --watch --fail-fast`.
8. After every push, return to step 1 before checking review feedback or CI again; finish only when the PR is mergeable, a final thread-aware review read finds no unresolved actionable feedback, and the complete required check set is green.

## Commands

```bash
# Resolve the active PR and inspect mergeability
gh pr view --json number,url,headRefName,baseRefName,mergeable,mergeStateStatus

# Materialize base-branch conflicts locally
git fetch origin <base-branch>
git merge origin/<base-branch>

# Inspect all attached checks
gh pr checks --json name,bucket,state,workflow,link

# Watch pending checks and fail fast
gh pr checks --watch --fail-fast

# GitHub Actions logs, when the failing check links to a GHA run
gh run view <run-id> --log-failed
```

## Guardrails

- Treat the `gh-pr-review-follow-up` skill as the source of truth for review-thread actionability and resolution state; do not infer thread state from flat comments.
- Do not inspect review feedback or wait on CI while base-branch conflicts remain unresolved.
- Treat the `gh-pr-resolve-conflicts` skill as the conflict-resolution and validation workflow. Keep its no-commit, no-push, and no-tag guardrail intact.
- Before the first remote mutation, obtain explicit approval if the request does not already authorize comment replies, thread resolution, commits, and pushes.
- Keep each fix scoped to a single failure cause when possible.
- Do not bypass hooks (`--no-verify`) to force progress.
- If the failure is clearly unrelated to the PR and appears fixed on the base branch, merge the latest base branch instead of bloating the PR with unrelated fixes.
- If failures are flaky, retry once and report flake evidence.
- Re-run `gh pr checks --json name,bucket,state,workflow,link` after every push; the check set can change.
- Do not report completion while base-branch conflicts remain unresolved, actionable review threads remain unresolved, or required checks are pending or failing.

## Output

- Merge-conflict status and resolution summary
- Addressed, skipped, and remaining review threads
- Current CI status
- Failure summary and fixes applied
- Commits and pushes performed
- PR URL once review threads are resolved and checks are green
