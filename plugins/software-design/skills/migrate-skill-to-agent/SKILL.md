---
name: migrate-skill-to-agent
description: >-
  Use only when migrating an existing skill directory from `.claude/skills/{name}` to `.agents/skills/{name}` and creating `.claude/skills/{name}` and `.codex/skills/{name}` symlinks. Requires a skill name argument. Trigger for migrating skills to `.agents`, unifying Claude and Codex skill locations, or creating these skill symlinks.
---

# Migrate Skill To Agent

This skill migrates one skill directory into `.agents/skills/` and creates Claude/Codex symlinks.

## Workflow

1. Confirm the skill name and project root.

2. Verify `.claude/skills/{name}` exists and is not already a symlink.

3. Verify `.agents/skills/{name}` does not already exist.

4. Run `bash scripts/migrate.sh <skill-name> <project-root>` from this skill directory, or run the script from the project root and pass `.` explicitly.

5. Check the resulting symlinks and `git status`.

## Detailed Reference

For non-trivial implementation, review, or refactoring work, read `references/details.md` before giving final guidance. It contains the detailed rules, examples, smells, and migration notes that do not belong in the short invocation body.

## Output

Report the moved directory, created symlinks, and any manual cleanup needed.

## Safety

Do not overwrite an existing real skill directory. Stop if the source or destination state does not match the expected migration.
