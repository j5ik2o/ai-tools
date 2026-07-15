---
name: j5ik2o:ddd-aggregate-design
description: >-
  Use for DDD aggregate design, implementation, refactoring, or review. Covers aggregate boundaries, aggregate roots, true invariants, immutable updates, ID references, eventual consistency, domain events, and Evans/Vernon aggregate rules. Trigger for aggregate boundary questions, aggregate roots, entity design inside aggregates, large aggregates, mutable aggregate code, public fields, direct child mutation, or cross-aggregate coordination.
---

# DDD Aggregate Design

An aggregate is a consistency boundary. Design it around true invariants, not object graphs, database tables, or UI screens.

## Workflow

1. Name the command and business invariant under discussion.

2. Decide what must be strongly consistent immediately. Put only that inside one aggregate.

3. Choose one aggregate root as the only external entry point.

4. Reference other aggregates by ID and coordinate them with events, policies, sagas, or process managers.

5. Prefer immutable updates unless the language or framework strongly pushes otherwise.

6. Review constructors/factories for complete initialization and invariant protection.

## Core Rules

- Design aggregates around true invariants.

- Keep aggregates small.

- Update one aggregate per transaction.

- Never expose mutable child collections or public fields.

- Use domain events for cross-aggregate effects.

- Add optimistic locking only when concurrent updates are a real requirement.

## Language References

Read the matching file in `references/` for TypeScript, Scala, Rust, or Python implementation patterns.

## Detailed Reference

For non-trivial implementation, review, or refactoring work, read `references/details.md` before giving final guidance. It contains the detailed rules, examples, smells, and migration notes that do not belong in the short invocation body.

## Output

Return the boundary decision, invariant list, aggregate root API, event list, transaction model, and concrete code or review findings.
