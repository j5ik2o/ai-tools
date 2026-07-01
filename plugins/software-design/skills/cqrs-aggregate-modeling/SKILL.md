---
name: cqrs-aggregate-modeling
description: >-
  Use when CQRS changes aggregate boundaries or state shape. Helps reduce oversized command aggregates by moving read concerns to read models, keeping only command-decision state in aggregates, and using events for state transitions. Trigger for large aggregates, heavy command updates, aggregates containing query-only data, or boundary redesign during CQRS adoption.
---

# CQRS Aggregate Modeling

In CQRS, an aggregate is not a read model. It only needs the state required to decide whether a command is valid and which events to emit.

## Workflow

1. Identify each command the aggregate handles.

2. List the state needed to validate and execute those commands.

3. Remove query-only projections, history lists, counters, denormalized display fields, and report data from the command aggregate.

4. Put read concerns into read models updated from events.

5. Redraw aggregate boundaries around true invariants and command contention.

## Modeling Rules

- Keep state minimal, invariant-bearing, and command-oriented.

- Prefer IDs and event references over embedded external aggregates.

- Model lifecycle as explicit state transitions when commands depend on it.

- Treat unbounded collections as read-model material unless they enforce a true invariant.

## Detailed Reference

For non-trivial implementation, review, or refactoring work, read `references/details.md` before giving final guidance. It contains the detailed rules, examples, smells, and migration notes that do not belong in the short invocation body.

## Output

Return the command-state matrix, proposed aggregate boundary, events, read models, and migration risks.
