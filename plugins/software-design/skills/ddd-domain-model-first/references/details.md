# Domain Model First Development Details

## Rationale

Infrastructure-first development lets frameworks, databases, and DTOs shape the domain model. Domain-model-first development makes business behavior testable before persistence and delivery concerns appear.

## Implementation Order

1. Write examples in domain language.
2. Implement value objects and domain primitives.
3. Implement entities and aggregates with invariant protection.
4. Add in-memory repositories for use-case tests.
5. Implement application use cases.
6. Add infrastructure adapters.
7. Add delivery adapters such as controllers or message consumers.

## Test Strategy

- Domain tests should be fast and framework-free.
- Use-case tests can use in-memory repositories.
- Adapter tests verify persistence and serialization separately.
- End-to-end tests cover wiring, not every domain rule.

## Repository Timing

Do not introduce database repositories before use cases need persistence. In-memory repositories reveal the port contract without locking the domain to a database.
