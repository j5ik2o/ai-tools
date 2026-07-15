---
name: j5ik2o:gh-pr-resolve-conflicts
description: Resolve unresolved GitHub PR merge conflicts non-interactively after integrating the latest base branch, validate the build and relevant tests, and stage the resolution. Use when git reports unmerged paths or conflict markers while preparing a PR. Do not use when the PR is already mergeable.
---

# GitHub PR Resolve Conflicts

## Trigger

The current PR branch has unresolved merge conflicts after attempting to integrate its base branch and needs a reliable path back to a buildable state.

## Workflow

1. Confirm a merge or rebase conflict is in progress, then detect all conflicting files from git status and conflict markers.
2. Resolve each conflict with minimal, correctness-first edits.
3. Prefer preserving both sides when safe. Otherwise, choose the variant that compiles and keeps public behavior stable.
4. Regenerate lockfiles with package manager tools instead of hand-editing.
5. Run compile, lint, and relevant tests.
6. Verify that no unmerged paths or conflict markers remain.
7. Stage resolved files and summarize key decisions.

## Guardrails

- Keep changes minimal and readable.
- Do not leave conflict markers in any file.
- Avoid broad refactors while resolving conflicts.
- Do not commit, push, or tag during conflict resolution; the calling workflow owns remote mutations.

## Output

- Files resolved
- Files staged
- Notable resolution choices
- Build/test outcome
