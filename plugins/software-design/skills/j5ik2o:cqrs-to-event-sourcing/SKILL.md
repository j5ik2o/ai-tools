---
name: j5ik2o:cqrs-to-event-sourcing
description: >-
  Use when explaining why CQRS often needs event sourcing or durable events for reliable command-to-query synchronization. Covers calculated value sync, database trigger limits, polling scalability, double commits, and making events the source of truth. Trigger for CQRS synchronization, read-model update strategy, CQRS without ES, or double-commit concerns.
---

# Why CQRS Leads To Event Sourcing

CQRS separates command decisions from query views. The hard part is not the split; it is reliable synchronization from writes to reads.

## Reasoning Chain

1. Commands change business facts, not just tables.

2. Read models need derived state that often cannot be reconstructed safely from row triggers alone.

3. Polling creates latency, missed intent, ordering ambiguity, and scaling pressure.

4. Updating the write store and read store in one use case creates a double-commit problem.

5. Durable domain events solve this by recording what happened once and projecting it many times.

## Caveats

- CQRS can be partial; non-CQRS areas can keep a unified model.

- A small system can use transactional outbox events without full event-sourced aggregates.

- Event sourcing is justified when history, replay, auditability, or projection repair matter.

## Detailed Reference

For non-trivial implementation, review, or refactoring work, read `references/details.md` before giving final guidance. It contains the detailed rules, examples, smells, and migration notes that do not belong in the short invocation body.

## Output

Explain the synchronization failure mode first, then recommend event sourcing, outbox-based events, or a simpler approach based on scale and risk.
