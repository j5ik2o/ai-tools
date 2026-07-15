---
name: j5ik2o-refactoring-packages
description: >-
  Use when actively refactoring an existing codebase's package or module structure. Detects cycles, oversized modules, misplaced responsibilities, and dependency direction problems, then proposes and executes a migration plan. Trigger for cleaning dependencies, breaking cycles, splitting modules, moving files, or structural refactoring work.
---

# Refactoring Packages

Refactor structure in small, verifiable moves. Preserve behavior while improving dependency shape.

## Workflow

1. Inventory the current package tree and dependency graph.

2. Identify cycles, large modules, unstable public APIs, and misplaced responsibilities.

3. Propose a target structure based on change reasons and dependency direction.

4. Move one coherent slice at a time.

5. Update imports, tests, build files, and public documentation as needed.

6. Run the relevant checks after each meaningful batch.

## Reference

Read `references/analysis-patterns.md` for common structural smells and remedies.

## Detailed Reference

For non-trivial implementation, review, or refactoring work, read `references/details.md` before giving final guidance. It contains the detailed rules, examples, smells, and migration notes that do not belong in the short invocation body.

## Output

Return findings, target structure, migration checklist, executed changes, and verification results.
