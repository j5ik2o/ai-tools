# Reviewing Skills Details

## Review Goal

A good skill makes agent behavior predictable. Review for invocation accuracy, execution clarity, and maintainability.

## Frontmatter Checks

- Name is stable and path-safe.
- Description contains the real trigger boundary.
- Near misses and exclusions are explicit when the trigger word is broad.
- Description is not a full copy of the body.

## Body Checks

- Steps are ordered.
- Completion criteria are checkable.
- Branch-specific detail is behind references.
- Required tools and validation commands are explicit.
- The skill avoids no-op advice the model would already follow.

## Failure Modes

- Premature completion: vague criteria let the agent stop early.
- Duplication: one rule appears in multiple places.
- Sediment: stale content remains after behavior changed.
- Sprawl: the main file is too long for reliable attention.
- Weak trigger: description is too generic or misses user phrasing.

## Report

Findings first, ordered by severity. Include concrete rewrites for high-impact trigger or step issues.
