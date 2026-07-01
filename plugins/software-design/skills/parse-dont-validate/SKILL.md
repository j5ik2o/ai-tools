---
name: parse-dont-validate
description: >-
  Use when replacing validation that discards information with parsing that returns a typed, validated value. Helps enforce invariants through the type system and reduce shotgun parsing. Trigger for validation refactors, type-safe inputs, invalid-state prevention, reducing `Maybe`/nullable checks, or converting validators into constructors/parsers.
---

# Parse, Don't Validate

Do not merely check data and then throw the proof away. Parse it into a type that carries the proof.

## Workflow

1. Find validators that return `bool`, `void`, or throw while leaving the original untyped value in circulation.

2. Define a target type whose construction proves the invariant.

3. Replace validation calls with parser or smart-constructor calls that return `Result`, `Either`, option, or exceptions as appropriate for the language.

4. Change downstream APIs to accept the parsed type.

5. Remove redundant re-validation.

## Checks

- A parsed type should make invalid states unrepresentable.

- Keep boundary parsing near input edges.

- Preserve error detail for users and logs.

## Reference

Read `references/patterns.md` for language patterns.

## Detailed Reference

For non-trivial implementation, review, or refactoring work, read `references/details.md` before giving final guidance. It contains the detailed rules, examples, smells, and migration notes that do not belong in the short invocation body.

## Output

Return the current validation leak, parsed type design, API changes, and migration steps.
