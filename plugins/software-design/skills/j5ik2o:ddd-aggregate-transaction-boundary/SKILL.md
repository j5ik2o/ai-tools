---
name: j5ik2o:ddd-aggregate-transaction-boundary
description: >-
  Use when reviewing or designing transaction boundaries that touch DDD aggregates. Detects the anti-pattern of updating multiple aggregates in one transaction and replaces it with one-aggregate transactions plus eventual consistency, domain events, sagas, or process managers. Trigger for cross-aggregate transactions, `@Transactional` use cases, one transaction one aggregate, or aggregate consistency coordination.
---

# DDD Aggregate Transaction Boundary

One transaction should update one aggregate. If multiple aggregates must change, model coordination explicitly.

## Workflow

1. Identify every aggregate loaded or modified by the use case.

2. Mark which aggregate owns the command's true invariant.

3. Keep that aggregate in the synchronous transaction.

4. Move other aggregate updates behind domain events, an outbox, a saga, or a process manager.

5. Define compensating behavior for failures and retries.

## Checks

- A use case that saves two aggregate roots is suspect.

- Repository calls from inside aggregates are violations.

- Database foreign keys do not define aggregate consistency boundaries.

- If the business demands immediate consistency across roots, challenge whether the boundary is wrong.

## Detailed Reference

For non-trivial implementation, review, or refactoring work, read `references/details.md` before giving final guidance. It contains the detailed rules, examples, smells, and migration notes that do not belong in the short invocation body.

## Output

Return the current transaction map, the corrected command flow, events/messages, idempotency strategy, and residual consistency risk.
