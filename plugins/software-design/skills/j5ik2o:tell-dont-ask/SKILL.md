---
name: j5ik2o:tell-dont-ask
description: >-
  Use when reviewing or refactoring code that queries object state and makes decisions outside the object that owns the data. Moves behavior to the responsible object to improve encapsulation. Trigger for getter misuse, Feature Envy, Tell Don't Ask, encapsulation improvements, or moving responsibility into domain objects.
---

# Tell, Don't Ask

Tell the object what you want done; do not ask for its state and make the decision elsewhere.

## Workflow

1. Find code that gets state, branches on it, then updates or commands the same object.

2. Name the intention behind the external decision.

3. Move that behavior to the object that owns the state.

4. Replace getters with intention-revealing methods where possible.

5. Keep DTO, serialization, logging, and UI projection exceptions explicit.

## Checks

- Getter plus `if` plus setter is a strong smell.

- Feature Envy means behavior is closer to another object's data than its own.

- Avoid adding anemic pass-through methods; move real decisions.

## Reference

Read `references/patterns.md` for refactoring patterns.

## Detailed Reference

For non-trivial implementation, review, or refactoring work, read `references/details.md` before giving final guidance. It contains the detailed rules, examples, smells, and migration notes that do not belong in the short invocation body.

## Output

Return the ask pattern, the moved behavior, revised API, and code changes.
