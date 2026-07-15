---
name: j5ik2o-cqrs-tradeoffs
description: >-
  Use when evaluating whether CQRS is worth adopting, especially tradeoffs among consistency, availability, scalability, operational complexity, and event sourcing. Trigger for read/write separation decisions, eventual consistency concerns, CQRS architecture review, or choosing between a unified model and CQRS.
---

# CQRS Tradeoffs

CQRS buys independent read/write models at the cost of more moving parts and explicit consistency choices.

## Decision Frame

1. Identify the forces: read scale, write contention, model complexity, audit needs, team maturity, and latency tolerance.

2. Decide which consistency guarantees are required for commands and which can be eventual in reads.

3. Check whether separate read models remove real complexity or just duplicate code.

4. Choose the smallest pattern: unified model, CQRS without ES, CQRS with outbox, or event-sourced CQRS.

## Tradeoffs

- Benefits: optimized reads, simpler command invariants, independent scaling, better audit/projection options.

- Costs: projection lag, more tests, operational monitoring, replay tooling, schema evolution, and debugging complexity.

- Red flags: low traffic, simple CRUD, no contention, no audit need, or a team that cannot operate async pipelines.

## Detailed Reference

For non-trivial implementation, review, or refactoring work, read `references/details.md` before giving final guidance. It contains the detailed rules, examples, smells, and migration notes that do not belong in the short invocation body.

## Output

Return a recommendation, rejected alternatives, consistency model, migration path, and operational prerequisites.
