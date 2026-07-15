---
name: j5ik2o-ddd-domain-primitives-and-always-valid
description: >-
  Use when replacing raw primitive values with validated domain primitives or value objects so invalid domain states cannot be represented. Covers always-valid construction, smart constructors, parse-don't-validate, and avoiding primitive obsession. Trigger for domain primitive design, validated IDs, email/money/range types, always-valid models, or preventing invalid states.
---

# Domain Primitives And Always-Valid Models

Make illegal states unrepresentable when the domain rule is stable enough to deserve a type.

## Workflow

1. Identify primitives that carry domain meaning or repeated validation.

2. Separate syntax checks from domain invariants.

3. Add a domain primitive with a private constructor and smart constructor or parser.

4. Store only valid values inside entities and aggregates.

5. Keep formatting, localization, and transport parsing outside the core type unless they are domain rules.

## Use A Domain Primitive When

- The value has a domain name.

- Validation appears in multiple places.

- Mixing two values of the same primitive type would be dangerous.

- Behavior belongs with the value.

## Avoid Wrapping When

- The value is purely technical, temporary, or has no invariant.

- A wrapper would add ceremony without changing correctness.

## Detailed Reference

For non-trivial implementation, review, or refactoring work, read `references/details.md` before giving final guidance. It contains the detailed rules, examples, smells, and migration notes that do not belong in the short invocation body.

## Output

Return the primitive candidates, chosen wrappers, construction API, error type, and migration steps.
