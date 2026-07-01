---
name: pekko-cqrs-es-implementation
description: >-
  Use only for Scala 3 implementations of CQRS/Event Sourcing with Apache Pekko. Covers aggregate actors, PersistenceEffector-style command handling, domain-model separation, typed state transitions, event design, Protocol Buffers serialization, ZIO use cases, and read-model updaters. Do not trigger for non-Scala stacks or conceptual CQRS questions without Pekko/Scala implementation work.
---

# Pekko CQRS/ES Implementation

Use this skill only when the implementation stack is Scala 3 plus Apache Pekko and the architecture is CQRS/Event Sourcing.

## Workflow

1. Confirm the aggregate, commands, events, state lifecycle, and serialization requirements.

2. Keep the domain model separate from the Pekko actor shell.

3. Model command handling as validation plus event emission.

4. Apply events through pure state transition functions.

5. Define Protocol Buffers schemas and evolution rules for persisted events.

6. Put use-case orchestration in ZIO/application services, not inside the aggregate actor.

7. Build read-model updaters as idempotent projections.

## Implementation Checks

- Commands should not mutate state directly.

- Events are facts in past tense and must be versioned carefully.

- Recovery must rebuild the same state from events.

- Projection handlers must tolerate retries and duplicates.

- Serialization compatibility is part of the public contract.

## Detailed Reference

For non-trivial implementation, review, or refactoring work, read `references/details.md` before giving final guidance. It contains the detailed rules, examples, smells, and migration notes that do not belong in the short invocation body.

## Output

Return aggregate actor structure, domain model APIs, command/event/state definitions, serialization notes, and projection flow.
