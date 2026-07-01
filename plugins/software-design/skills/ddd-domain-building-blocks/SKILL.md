---
name: ddd-domain-building-blocks
description: >-
  Use for choosing and applying DDD building blocks: value objects, entities, aggregates, domain services, repositories, factories, and domain events. Trigger for domain modeling, entity versus value object decisions, aggregate boundaries, domain service placement, or implementing a domain model from requirements.
---

# DDD Domain Building Blocks

Choose the smallest DDD building block that expresses the domain rule without leaking infrastructure concerns.

## Building Blocks

- Value object: identity-free, immutable, validated by construction, compared by value.

- Entity: stable identity plus lifecycle, behavior, and invariants.

- Aggregate: consistency boundary with one root.

- Domain service: stateless domain operation that does not naturally belong to one entity or value object.

- Repository: collection-like access to aggregate roots.

- Factory: creation logic that protects invariants or hides construction complexity.

- Domain event: something meaningful that happened in the domain.

## Workflow

1. Extract ubiquitous language from the requirement.

2. Classify each concept by identity, lifecycle, invariants, and behavior.

3. Put validation into construction where possible.

4. Keep application orchestration out of domain objects.

5. Check that persistence details do not shape the model.

## Detailed Reference

For non-trivial implementation, review, or refactoring work, read `references/details.md` before giving final guidance. It contains the detailed rules, examples, smells, and migration notes that do not belong in the short invocation body.

## Output

Return a concept table, chosen building blocks, aggregate boundaries, and example APIs.
