---
name: j5ik2o:git-commit
description: >
  Commit working-tree changes using Conventional Commits. Stage changes in
  meaningful units, write commit messages in English, and avoid co-author or
  agent attribution in commit messages. Use this skill only when the user
  explicitly asks to create a real git commit, such as "commit these changes",
  "create a git commit", "git commit", or "commit this work". Do not use it
  when the user only wants commit message wording without making an actual
  commit. This skill commits locally only; it does not push.
---

# Git Commit

Create clear project history by committing changes in meaningful, reviewable units.

## Workflow

### 1. Inspect Recent Commit History

Review the latest commits to match the repository's commit style.

```bash
git log --oneline -10
```

### 2. Inspect Current Changes

Check the working tree state. Do not use the `-uall` flag because it can cause memory problems in large repositories.

```bash
git status
git diff
git diff --staged
```

### 3. Stage Meaningful Units

Stage only the files that belong in the current logical change. Do not blindly run `git add -A` or `git add .`; specify the intended files or directories.

```bash
git add <target-files-or-directories>
```

After staging, **always inspect the exact content that will be committed**. `git diff` does not show new untracked file contents or all staged changes, so use `git diff --staged` to review staged content, including new files and any changes produced by hooks or formatters.

```bash
git diff --staged
```

Never include `.env` files or files containing credentials. If the user explicitly asks to commit such files, stop and ask them to remove or redact the secret material first.

Also do not include files the user explicitly asked to exclude.

If one staged set contains multiple logically independent changes, split it into multiple commits.

### 4. Write the Commit Message and Commit

Use Conventional Commits and write the message in English.

```bash
git commit -m "$(cat <<'EOF'
<type>(<scope>): <description>

<body-if-needed>
EOF
)"
```

**Commit message rules:**

- **Conventional Commits format**: `type(scope): description`
  - type: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `ci`, `perf`, `build`, and similar types
  - scope: affected area, optional
  - description: concise summary of the change
- **Write in English**
- **Do not include co-author lines or agent names such as "Claude Code" or "Codex"**
- Emphasize why the change exists, not just what changed
- Write the description in imperative mood, for example "add" rather than "added"

### 5. Verify the Commit

Verify the commit that was actually created. Pre-commit hooks or formatters may modify and re-stage files during commit creation, so the post-commit check is required even after reviewing staged changes.

```bash
git log --oneline -5
git show --stat HEAD   # Files included in the commit
git show HEAD          # Exact committed diff, including hook-produced changes
git status             # Confirm hook-produced changes were not left uncommitted
```

- If hooks introduced unintended committed content, or if hook-produced changes remain uncommitted, inspect the result and address it with a follow-up commit when appropriate.

## Notes

- If a pre-commit hook fails, no commit was created. Fix the problem and create a new commit; do not use `--amend`.
- If a pre-commit hook modifies files, step 5 must verify whether those changes were included in the commit or left unstaged.
- Do not bypass hooks with `--no-verify`. Investigate and fix failing hooks.
- Pushing is outside this skill's scope. Do not push unless the user explicitly asks for it.
