---
name: j5ik2o-reviewing-skills
description: >-
  Use when reviewing or improving Claude Code, Codex, or compatible agent skills. Checks SKILL.md frontmatter, trigger boundary, progressive disclosure, no-op instructions, duplication, sediment, sprawl, examples, and validation readiness. Trigger for skill review, SKILL.md review, skill quality check, trigger debugging, or improving an existing skill.
---

# Reviewing Skills

Review skills for predictable agent behavior, not just readability.

## Workflow

1. Identify the target skill directory and read `SKILL.md` completely.

2. Read `references/best-practices.md` before producing findings.

3. Check frontmatter name and description for trigger precision and exclusions.

4. Check the body for clear steps, completion criteria, progressive disclosure, duplication, no-ops, sediment, and sprawl.

5. Inspect bundled references, scripts, assets, and evals when present.

6. Return prioritized findings before optional rewrites.

## Report Shape

Use: `Critical`, `Warning`, `Info`, and `Suggested rewrite` when a concrete replacement is useful.

## Detailed Reference

For non-trivial implementation, review, or refactoring work, read `references/details.md` before giving final guidance. It contains the detailed rules, examples, smells, and migration notes that do not belong in the short invocation body.

## Output

Lead with actionable findings and file references. If asked to fix, make the smallest changes that improve invocation, execution, and validation.
