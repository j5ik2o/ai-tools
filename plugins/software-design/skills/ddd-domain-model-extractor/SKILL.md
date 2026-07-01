---
name: ddd-domain-model-extractor
description: >-
  Use when analyzing existing non-DDD or legacy code to propose DDD domain models with aggregates, local entities, value objects, domain services, invariants, and pseudocode. Trigger for extracting a domain model from code, redesigning legacy code with DDD, finding aggregates, or proposing domain boundaries from an existing implementation.
---

# DDD Domain Model Extractor

Extract the model from behavior and invariants, not from table names alone.

## Workflow

1. Confirm the target files, domain overview, and areas of concern.

2. Explore commands, state changes, validation, persistence operations, and tests.

3. Identify domain concepts, lifecycle states, invariants, and transactional boundaries.

4. Propose aggregates, entities, value objects, and domain services.

5. Produce pseudocode and a migration path that preserves behavior.

## References

Read `references/analysis-heuristics.md` before analyzing large codebases. Use `references/output-template.md` for the final report shape.

## Detailed Reference

For non-trivial implementation, review, or refactoring work, read `references/details.md` before giving final guidance. It contains the detailed rules, examples, smells, and migration notes that do not belong in the short invocation body.

## Output

Return candidate models with evidence from code, not just names. Include uncertain decisions and what evidence would settle them.
