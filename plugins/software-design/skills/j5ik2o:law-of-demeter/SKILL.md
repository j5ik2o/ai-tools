---
name: j5ik2o:law-of-demeter
description: >-
  Use when reviewing or refactoring object coupling caused by train-wreck call chains and knowledge of nested internals. Applies the Law of Demeter / Principle of Least Knowledge to move behavior closer to the owning object. Trigger for chained calls, dot chains, train wrecks, high coupling, Feature Envy, or reducing object navigation.
---

# Law Of Demeter

Talk to direct collaborators, not strangers reached through them.

## Workflow

1. Find call chains such as `a.getB().getC().doX()` and code that navigates object structure.

2. Identify the decision or behavior being performed by the caller.

3. Move that behavior to the object that owns the needed knowledge.

4. Replace navigation with intention-revealing methods.

5. Keep DTO, builder, and fluent API exceptions explicit; not every chain is a domain coupling problem.

## Checks

- Train wrecks expose structure and make callers fragile.

- Repeated navigation paths usually indicate a missing method.

- Getters used only to make a decision are Tell Don't Ask candidates.

## Reference

Read `references/patterns.md` for refactoring patterns and exceptions.

## Detailed Reference

For non-trivial implementation, review, or refactoring work, read `references/details.md` before giving final guidance. It contains the detailed rules, examples, smells, and migration notes that do not belong in the short invocation body.

## Output

Return the chain, the hidden behavior, the target owner, and replacement code.
