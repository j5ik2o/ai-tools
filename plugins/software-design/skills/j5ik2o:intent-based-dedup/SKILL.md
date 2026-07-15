---
name: j5ik2o:intent-based-dedup
description: >-
  Use when deciding whether similar code should be deduplicated. Prioritizes shared intent and change reason over textual similarity, avoiding harmful DRY abstractions when code looks alike but changes for different reasons. Trigger for duplicate code, DRY decisions, merging functions, common helpers, or refactoring similar implementations.
---

# Intent-Based Deduplication

Deduplicate by intent, not by appearance. Similar text with different reasons to change should stay separate.

## Workflow

1. Identify the duplicated code and every caller.

2. Name the business or technical intent of each copy.

3. Compare future change reasons, owners, invariants, and release cadence.

4. Deduplicate only when the shared abstraction can be named honestly and will change for one reason.

5. If intent differs, keep duplication or extract smaller mechanical helpers that do not pretend to be domain concepts.

## Decision Matrix

- Same text, same intent: merge.

- Same text, different intent: keep separate.

- Different text, same intent: consider unifying.

- Different text, different intent: do not merge.

## Detailed Reference

For non-trivial implementation, review, or refactoring work, read `references/details.md` before giving final guidance. It contains the detailed rules, examples, smells, and migration notes that do not belong in the short invocation body.

## Output

Return the intent comparison, decision, proposed abstraction name if any, and risks of coupling.
