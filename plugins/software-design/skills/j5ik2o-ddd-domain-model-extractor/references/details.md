# Domain Model Extractor Details

## Evidence Sources

Read commands, handlers, services, tests, database constraints, validation code, state transitions, and error messages. Names alone are weak evidence; behavior is stronger.

## Extraction Heuristics

- Repeated validation suggests a value object or domain primitive.
- A lifecycle status field suggests an entity or aggregate root.
- A transaction that updates a cluster suggests an aggregate boundary.
- A stateless operation spanning multiple concepts may be a domain service.
- Past-tense records or notifications may be domain events.

## Analysis Flow

1. List observable use cases.
2. Trace state changes per use case.
3. Identify invariants and who protects them today.
4. Identify concepts with identity and lifecycle.
5. Propose aggregate roots and internal members.
6. Mark uncertain decisions and missing domain questions.

## Output Expectations

Every proposed model should cite evidence from the code. Include pseudocode only after the concepts and invariants are clear.
