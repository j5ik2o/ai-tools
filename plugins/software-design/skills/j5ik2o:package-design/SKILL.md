---
name: j5ik2o:package-design
description: >-
  Use when redesigning package or module structure for messy codebases, large modules, dependency problems, or new project structure. Applies information hiding, change reasons, dependency direction, and release boundaries. Trigger for package structure review, module dependencies, file placement, circular dependency cleanup, or module hierarchy design.
---

# Package Design

Package design is about controlling change, not arranging files aesthetically.

## Workflow

1. Identify change reasons: what decisions are likely to vary independently?

2. Map current dependencies and cycles.

3. Group code by stable domain or technical decisions, not by temporary implementation steps.

4. Define public APIs that hide volatile internals.

5. Make dependency direction explicit and acyclic.

6. Plan migration in small, behavior-preserving moves.

## Design Rules

- Put volatile details behind stable interfaces.

- Keep high-level policy independent from low-level mechanisms.

- Prefer feature/domain packages when change reasons are domain-shaped.

- Split large modules only when the split reduces change coupling.

## References

Read `references/principles.md` for design principles and `references/rust-patterns.md` for Rust-specific layouts.

## Detailed Reference

For non-trivial implementation, review, or refactoring work, read `references/details.md` before giving final guidance. It contains the detailed rules, examples, smells, and migration notes that do not belong in the short invocation body.

## Output

Return current problems, target package tree, dependency rules, migration steps, and verification commands.
