---
name: j5ik2o-custom-linter-creator
description: >-
  Use when creating project-specific lint rules for AI agents or humans using existing language linter ecosystems. Generates rules under a `lints/` directory with actionable diagnostic messages that tell an agent exactly how to repair the violation. Trigger for custom lint rules, AI linter rules, enforcing naming or structure patterns, or turning code-review rules into lint checks.
---

# Custom Linter Creator

Prefer the host language's existing linter ecosystem. The diagnostic message is part of the design: it should be a repair prompt, not just a complaint.

## Workflow

1. Extract the rule as a precise, statically detectable condition.

2. Pick the native ecosystem: ESLint for TypeScript/JavaScript, pylint for Python, Go analysis/golangci-lint for Go, dylint or Clippy-style tooling for Rust.

3. Create the rule under `lints/` with tests or fixtures.

4. Write diagnostics that include the violation, repair steps, scope limits, and rationale.

5. Integrate the rule into the project lint command.

## Diagnostic Template

Use this shape: `Problem: ... Repair: 1. ... 2. ... Scope: ... Rationale: ...`.

## Reference

Read `references/language-ecosystems.md` for ecosystem-specific scaffolding.

## Detailed Reference

For non-trivial implementation, review, or refactoring work, read `references/details.md` before giving final guidance. It contains the detailed rules, examples, smells, and migration notes that do not belong in the short invocation body.

## Output

Return the rule definition, file layout, diagnostic text, test fixture, and command to run it.
