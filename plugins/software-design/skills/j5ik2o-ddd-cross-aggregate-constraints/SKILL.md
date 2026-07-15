---
name: j5ik2o-ddd-cross-aggregate-constraints
description: >-
  Use when a use case wants to check another aggregate's state before changing the current aggregate. Helps separate true invariants from policies, detect Saga misuse, reason about CQRS/Event Sourcing lookup limits, and decide whether inconsistent data is acceptable. Trigger for cross-aggregate validation, checking another aggregate, command-side read-model access, reverse lookup constraints, or Saga-based validation.
---

# DDD Cross-Aggregate Constraints

A cross-aggregate constraint is usually a requirements question before it is a technical question.

## Workflow

1. Restate the rule in business language and ask whether it must be immediately true.

2. If it is a true invariant, consider merging the aggregate boundary or changing the command owner.

3. If it is a policy, use events, reservations, or compensating actions; use a saga only for multi-step orchestration and compensation, not for synchronous existence checks.

4. In CQRS/ES, avoid command decisions based on stale read models unless the business accepts that staleness.

5. Document the inconsistency window and repair mechanism.

## Decision Options

- Same aggregate: use when the rule is a true invariant.

- Reservation aggregate: use when scarce resources need temporary holds.

- Policy or saga: use when the reaction can be eventual; reject saga for rules that must block the first command synchronously.

- Read-model check: use only when stale decisions are acceptable.

## Detailed Reference

For non-trivial implementation, review, or refactoring work, read `references/details.md` before giving final guidance. It contains the detailed rules, examples, smells, and migration notes that do not belong in the short invocation body.

## Output

Return the business interpretation, chosen consistency model, rejected options, and exact failure/retry behavior.
