# Clean Architecture Details

## Dependency Rule

Source-code dependencies point inward. Domain does not know use cases, adapters, infrastructure, frameworks, databases, RPC, HTTP, or UI. Use cases know domain and ports. Adapters translate between external mechanisms and use-case ports. Infrastructure wires concrete mechanisms.

## Layer Placement

| Concern | Layer |
| --- | --- |
| Entity, value object, aggregate, invariant | Domain |
| Use-case orchestration, authorization policy, transaction boundary | Use case |
| Controller, presenter, gateway, repository implementation | Interface adapter |
| Logging, metrics, configuration, DI, clock, ID generator | Infrastructure |

## Important Distinction

Persistence and RPC are not automatically "infrastructure" in this four-layer vocabulary. The database driver and connection setup are infrastructure mechanisms, but repository implementations and DTO mapping are interface adapters because they adapt external data shapes to internal use cases.

## Review Procedure

1. Draw imports between layers.
2. Mark each concrete framework type that crosses inward.
3. Check whether domain types contain persistence annotations or serialization concerns.
4. Check whether controllers contain business decisions that should be in use cases.
5. Check whether use cases return persistence models or API DTOs directly.

## Acceptable Compromises

Small projects may collapse physical packages, but logical dependency direction still matters. If a framework requires annotations on domain objects, document the tradeoff and keep framework behavior passive.
