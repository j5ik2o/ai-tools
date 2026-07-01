---
name: ddd-when-to-wrap-primitives
description: >-
  Use when deciding whether a primitive value should become a domain-specific type or value object. Balances primitive obsession against value-object obsession using risk, invariants, behavior, and cost. Trigger for wrapping strings/ints/UUIDs, value object decisions, too many tiny types, or whether a primitive is good enough.
---

# When To Wrap Primitives

Wrap primitives when the wrapper changes correctness, not when it only signals virtue.

## Wrap When

- The value has a domain name and invariant.

- Two values of the same primitive type can be confused.

- Validation is repeated or easy to forget.

- Behavior naturally belongs with the value.

- Invalid states cause meaningful business risk.

## Do Not Wrap Yet When

- The value has no behavior or invariant.

- The wrapper would only forward primitive operations.

- The type is local, temporary, or purely technical.

- The team would pay high ceremony for little safety.

## Workflow

1. List candidate primitives and their risks.

2. Score invariant strength, misuse risk, behavior, reuse, and migration cost.

3. Wrap the highest-value candidates first.

4. Keep construction explicit and error reporting useful.

## Detailed Reference

For non-trivial implementation, review, or refactoring work, read `references/details.md` before giving final guidance. It contains the detailed rules, examples, smells, and migration notes that do not belong in the short invocation body.

## Output

Return a wrap/keep table with rationale and example APIs for the chosen wrappers.
