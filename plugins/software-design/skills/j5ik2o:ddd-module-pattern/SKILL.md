---
name: j5ik2o:ddd-module-pattern
description: >-
  Use when designing DDD module boundaries, package layout, bounded-context internals, or language-specific module organization. Helps keep domain concepts cohesive while exposing narrow APIs and hiding implementation details. Trigger for DDD modules, package-by-domain, bounded context internals, module visibility, or organizing aggregates and value objects.
---

# DDD Module Pattern

A DDD module should hide implementation detail and expose a small language-shaped API.

## Workflow

1. Identify the bounded context or subdomain the module represents.

2. Group aggregates, value objects, domain services, policies, and events by domain concept.

3. Expose only stable commands, queries, ports, and domain types needed by other modules.

4. Keep persistence mapping and framework glue outside the domain module or behind adapters.

5. Use language visibility features to enforce the boundary.

## Checks

- Module names should be domain terms, not technical layers alone.

- Public APIs should be smaller than internal files.

- Cross-module calls should go through explicit interfaces or application services.

- Shared kernels must stay small and stable.

## Reference

Read `references/language-guides.md` for language-specific visibility and package patterns.

## Detailed Reference

For non-trivial implementation, review, or refactoring work, read `references/details.md` before giving final guidance. It contains the detailed rules, examples, smells, and migration notes that do not belong in the short invocation body.

## Output

Return a proposed module tree, public API, hidden internals, and dependency direction.
