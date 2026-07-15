# Clean Architecture Layer Responsibilities

## Domain

Owns enterprise business rules: entities, value objects, aggregates, domain services, domain events, and invariants. It must not depend on frameworks, databases, RPC clients, UI, or application orchestration.

## Use Cases

Owns application-specific rules: command/query orchestration, authorization policy, transaction boundaries, port interfaces, repository usage, and domain event publication decisions.

## Interface Adapters

Owns conversion between external shapes and internal use cases: controllers, presenters, gateways, repository implementations, RPC adapters, DTOs, and persistence mapping.

## Infrastructure

Owns mechanisms: logging, metrics, configuration, dependency injection, concrete database drivers, HTTP clients, clocks, ID generators, and runtime wiring.

## Common Placement Mistakes

- Putting repository implementations in the domain layer.
- Letting use cases import ORM models.
- Treating infrastructure as the place for all external IO; persistence adapters are interface adapters in this model.
- Allowing controllers to hold business decisions that belong in use cases.
