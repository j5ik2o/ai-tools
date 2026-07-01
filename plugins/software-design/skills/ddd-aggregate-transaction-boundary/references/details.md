# Aggregate Transaction Boundary Details

## Core Rule

One transaction updates one aggregate root. This follows from the aggregate definition: the aggregate is the strong consistency boundary. If one transaction must update two roots, the boundary or requirement deserves scrutiny.

## Common Anti-Patterns

- A use case loads and saves two aggregate roots under one `@Transactional` method.
- An aggregate method accepts a repository to look up another aggregate.
- A domain service updates multiple roots synchronously while claiming they are separate aggregates.
- Database transactions are used to hide missing process modeling.

## Replacement Patterns

- Domain event plus outbox for asynchronous reaction.
- Saga or process manager for multi-step coordination.
- Reservation aggregate for scarce resources.
- Boundary redesign when the rule is a true invariant.

## Failure Handling

Every eventual-consistency design needs idempotency, retry policy, failure visibility, and compensating behavior. Do not just say "use events"; describe what happens when the subscriber fails.

## Review Output

Show current synchronous flow, corrected flow, events/messages, retry/idempotency keys, and the inconsistency window.
