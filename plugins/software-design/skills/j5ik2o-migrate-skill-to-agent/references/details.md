# Migrate Skill To Agent Details

## Expected Initial State

`.claude/skills/{name}` exists as a real directory. `.agents/skills/{name}` does not exist. `.codex/skills/{name}` may be absent or an old symlink.

## Resulting State

The real skill directory lives at `.agents/skills/{name}`. Both `.claude/skills/{name}` and `.codex/skills/{name}` point to it with relative symlinks.

## Safety Checks

Stop if the source is already a symlink, if the destination exists, or if the skill name is missing. Do not overwrite real directories.

## Command

Run from this skill directory with the project root explicitly supplied:

```bash
bash scripts/migrate.sh <skill-name> <project-root>
```

Alternatively, run the script from the project root and pass `.` as the project root. Do not omit the second argument when your current directory is the skill directory; the script defaults to the current directory.

## Verification

Check `ls -l .claude/skills/{name} .codex/skills/{name}` and `git status`. Confirm the symlink target works from both Claude and Codex discovery paths.
