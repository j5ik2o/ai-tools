---
name: first-class-collection
description: >-
  Use when wrapping collections in a domain-specific class to centralize collection rules, invariants, and behavior. Trigger for scattered list logic, collection wrappers, raw Order lists becoming `Orders`, enforcing collection invariants, or reviewing collection-heavy domain code.
---

# First Class Collection

A first-class collection gives a collection a domain name and keeps collection rules in one place.

## Rule

The wrapper should own one collection field and behavior around that collection. Extra unrelated fields usually mean it is an entity or aggregate instead.

## Workflow

1. Find repeated collection operations, filters, totals, limits, ordering, or validation.

2. Name the collection as a domain concept.

3. Move rules into methods on the wrapper.

4. Keep the internal collection immutable or defensively copied.

5. Expose intention-revealing operations instead of raw mutation.

## Checks

- Good: `OrderLines.totalAmount()`, `Members.hasQuorum()`.

- Bad: exposing `items` and expecting callers to remember invariants.

- Avoid wrapping a collection that has no domain behavior.

## Reference

Read `references/patterns.md` for implementation patterns.

## Detailed Reference

For non-trivial implementation, review, or refactoring work, read `references/details.md` before giving final guidance. It contains the detailed rules, examples, smells, and migration notes that do not belong in the short invocation body.

## Output

Return wrapper candidates, APIs, invariants, and migration steps.
