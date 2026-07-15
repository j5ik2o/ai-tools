---
name: j5ik2o:clean-architecture
description: >-
  Use only when the user explicitly asks for Clean Architecture design, implementation, or review. Applies a domain, use case, interface adapter, and infrastructure layer model, with persistence and RPC adapters outside the domain and use-case rules. Do not trigger for generic architecture advice, hexagonal architecture, onion architecture, or ordinary design review unless Clean Architecture is named.
---

# Clean Architecture

Use this skill only for projects that intentionally follow Clean Architecture. Keep policy inward and mechanisms outward.

## Layer Rule

- Domain: entities, value objects, aggregates, domain services, domain events, and invariants.

- Use cases: application-specific orchestration, transaction boundaries, ports, authorization decisions that are application policy, and repository interface usage.

- Interface adapters: controllers, presenters, gateways, repository implementations, RPC adapters, DTO mapping, and persistence mapping.

- Infrastructure: cross-cutting mechanisms such as logging, configuration, metrics, DI wiring, clocks, IDs, and concrete driver setup.

## Workflow

1. Confirm the project actually uses Clean Architecture.

2. Map the touched code to the four layers.

3. Check dependency direction: outer layers may depend inward; inward layers must not know outer mechanisms.

4. Move persistence, RPC, UI, and framework details out of domain and use-case code.

5. Report the minimal relocation or interface extraction needed.

## Reference

Read `references/layer-responsibilities.md` when placement is ambiguous.

## Detailed Reference

For non-trivial implementation, review, or refactoring work, read `references/details.md` before giving final guidance. It contains the detailed rules, examples, smells, and migration notes that do not belong in the short invocation body.

## Output

Provide a layer-by-layer finding list, dependency violations, and concrete file-placement recommendations.
