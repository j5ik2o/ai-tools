# Domain Model Extraction Heuristics

Look for evidence, not just names.

## Strong Signals

- Methods that change state after checking rules.
- Transactions that load and save the same cluster of data.
- Repeated validation around the same fields.
- Tests written in business language.
- Database constraints that protect business rules.
- Status fields with lifecycle transitions.

## Classification

- Stable identity plus lifecycle suggests an entity.
- Identity-free validated data suggests a value object.
- A transactionally consistent cluster suggests an aggregate.
- Stateless behavior that spans concepts may be a domain service.
- A stored fact in past tense suggests a domain event.
