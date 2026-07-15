# CQRS To Event Sourcing Details

## Synchronization Problem

CQRS creates at least two models: one for commands and one for reads. The essential design problem is how read models learn about write-side changes reliably, in order, and with enough semantic information.

## Failed Approaches

- Direct dual writes create a double-commit problem when one write succeeds and the other fails.
- Database triggers see row changes but often miss domain intent and calculated values.
- Polling tables creates latency, load, ordering ambiguity, and difficult gap recovery.
- Recomputing derived values from current rows can lose the reason the value changed.

## Event-Based Resolution

Durable events record domain facts once. Projections can subscribe, retry, rebuild, and evolve independently. This does not always require fully event-sourced aggregates; a transactional outbox can be sufficient when the write model remains state-based.

## Decision Options

| Option | Use when |
| --- | --- |
| Unified model | CRUD is simple and read/write needs are aligned |
| CQRS with outbox | Need async projections but not full history |
| Event-sourced CQRS | Need audit, replay, temporal queries, or projection repair |

## Caution

Do not claim CQRS always requires event sourcing. The stronger claim is that reliable CQRS needs durable change facts, and event sourcing is the most complete form of that idea.
