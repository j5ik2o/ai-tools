# Repository Placement Details

## Placement Options

Different architectures place repository interfaces differently. What must not change: aggregates should not depend on repositories, and implementations belong outside domain policy.

## Recommended Default

Use cases/application services depend on repository interfaces and orchestrate loading/saving. Infrastructure or interface-adapter packages implement those interfaces.

## Domain-Layer Interfaces

Some DDD styles place repository interfaces in the domain layer because repositories are part of the domain model vocabulary. This is acceptable only if domain objects still do not call them.

## Smells

- Aggregate method receives a repository argument.
- Domain service performs application orchestration.
- Repository implementation sits next to aggregates and imports ORM details into the domain package.

## Correction

Move repository calls to use cases. Pass already-loaded domain objects into domain behavior. Publish events when other aggregates must react.
