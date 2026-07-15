# DDD Aggregate Design Details

## Definition

An aggregate is a cluster of objects treated as one consistency boundary. The aggregate root is the only object outside code may directly reference. Internal entities and value objects are reachable only through root behavior.

## Design By Contract

| Contract | Meaning | Owner |
| --- | --- | --- |
| Precondition | Required before a method call | Caller |
| Postcondition | Guaranteed after method completion | Implementation |
| Invariant | Always true for valid aggregate state | Aggregate |

Protect invariants in constructors, factories, and command methods. Invalid aggregate instances should not be representable.

## Evans Rules

- The root is the only member obtained directly by external objects.
- Internal objects have local identity only inside the aggregate.
- External objects may hold references only to the root.
- Deleting the root should remove or make unreachable everything inside the aggregate boundary.

## Vernon Rules

- Design aggregates around true invariants.
- Keep aggregates small.
- Reference other aggregates by identity.
- Use eventual consistency outside the aggregate boundary.

## Review Smells

- Public fields on aggregate roots.
- Direct mutation of child collections.
- Direct object references to other aggregate roots.
- A single transaction saves multiple aggregate roots.
- Aggregate methods require repositories.
- Query-only data or unbounded histories live inside the command aggregate.

## Modeling Output

For every aggregate proposal, list root, internal members, invariants, commands, emitted events, transaction boundary, and cross-aggregate coordination.
