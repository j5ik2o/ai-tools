# CQRS Aggregate Modeling Details

## Principle

After CQRS, the command aggregate is not responsible for answering arbitrary questions. It is responsible for deciding whether commands are valid and emitting facts. Data needed only for screens, reports, searches, histories, or counters belongs in read models.

## Command-State Matrix

Build a table:

| Command | Required state | Invariant protected | Event emitted |
| --- | --- | --- | --- |

Any state that does not appear in the command column is probably read-model state.

## Oversized Aggregate Smells

- It stores unbounded child collections only to display them.
- Command handling loads thousands of records.
- It contains denormalized values for query speed.
- It tracks histories that are never used for command decisions.
- It owns data whose lifecycle and contention differ from the root.

## Boundary Redesign

Split aggregates around true invariants and contention. For example, a thread aggregate usually should not hold every message if commands only need thread status and posting permissions. Messages can become separate aggregates or event facts, with read models providing timelines.

## Event Role

Events bridge command decisions to read models. They should carry enough information for projections to update without re-querying command aggregates.
