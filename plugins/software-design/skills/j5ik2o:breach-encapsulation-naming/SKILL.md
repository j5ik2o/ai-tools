---
name: j5ik2o:breach-encapsulation-naming
description: >-
  Use when designing or reviewing domain-model accessors that expose internal state for persistence, serialization, tests, or framework integration. Applies the breachEncapsulationOf naming pattern so unavoidable getters are visibly treated as encapsulation breaches, not casual domain APIs. Trigger for getter naming conventions, persistence-only getters, serialization accessors, Tell Don't Ask pressure, or requests to prevent getter misuse.
---

# Breach Encapsulation Naming

Make unavoidable state exposure loud. Domain objects should express behavior first; when an accessor is required for persistence, serialization, debugging, or tests, name it as an explicit encapsulation breach.

## Workflow

1. Classify every requested accessor by consumer: domain behavior, persistence, serialization, tests, framework glue, or presentation.

2. Replace domain-behavior access with Tell Don't Ask methods on the object that owns the data.

3. For unavoidable exposure, use `breachEncapsulationOfX()` or the idiomatic local equivalent such as `breach_encapsulation_of_x`.

4. Keep exposed values immutable or defensively copied.

5. Add a review note explaining why the breach is tolerated and which callers may use it.

## Review Checks

- Ordinary getters on entities and aggregates need justification.

- Accessors used by domain logic are design smells; move the decision to the model.

- Framework-required access should be isolated in adapters, serializers, mappers, or repository glue.

- Tests may use breach accessors, but assertions should still prefer observable behavior when possible.

## References

Read `references/patterns.md` for language-specific naming and migration examples.

## Detailed Reference

For non-trivial implementation, review, or refactoring work, read `references/details.md` before giving final guidance. It contains the detailed rules, examples, smells, and migration notes that do not belong in the short invocation body.

## Output

Return the accessor classification, recommended names, any Tell Don't Ask replacements, and the smallest migration path.
