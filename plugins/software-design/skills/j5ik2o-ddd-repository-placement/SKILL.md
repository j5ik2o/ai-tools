---
name: j5ik2o-ddd-repository-placement
description: >-
  Use when deciding where repository interfaces and implementations belong in layered, Clean Architecture, or DDD projects. Emphasizes that aggregates should not depend on repositories and that application/use-case layers own repository orchestration. Trigger for repository-in-domain questions, repository package placement, or aggregates calling repositories.
---

# DDD Repository Placement

Repository placement should prevent domain models from reaching outward for data.

## Placement Rules

- Aggregate code: no repository dependencies.

- Application/use-case layer: depends on repository interfaces and orchestrates loading/saving.

- Domain layer: may define repository abstractions only when the project convention treats them as domain contracts, but aggregates still must not call them.

- Infrastructure/interface adapters: implement repositories using databases, APIs, or files.

## Workflow

1. Find repository interfaces, implementations, and all call sites.

2. Move calls from domain objects into use cases or domain services invoked by use cases.

3. Keep persistence mapping outside aggregates.

4. Align package placement with the project's architecture style.

## Detailed Reference

For non-trivial implementation, review, or refactoring work, read `references/details.md` before giving final guidance. It contains the detailed rules, examples, smells, and migration notes that do not belong in the short invocation body.

## Output

Return a placement map, violations, corrected dependencies, and file moves.
