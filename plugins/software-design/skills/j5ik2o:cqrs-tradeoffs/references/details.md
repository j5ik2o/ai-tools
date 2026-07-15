# CQRS Tradeoffs Details

## Evaluation Axes

Evaluate CQRS using consistency, availability, scalability, operational complexity, model complexity, auditability, and team maturity. CQRS is an architectural trade, not an upgrade.

## Benefits

- Command model can focus on invariants.
- Read models can be optimized for screens and reports.
- Read and write workloads can scale independently.
- Events or outbox records improve audit and repair options.
- Complex domains avoid forcing one model to satisfy every use case.

## Costs

- Eventual consistency becomes user-visible.
- Projection lag must be monitored.
- Tests need to cover command decisions and projection behavior.
- Debugging crosses messages, versions, retries, and read-model state.
- Schema evolution and replay become operational responsibilities.

## Adoption Checklist

Use CQRS when at least one pressure is real: high read/write asymmetry, complex invariants, divergent query shapes, audit/replay needs, or write contention. Avoid it for simple CRUD, low traffic, or teams that cannot operate asynchronous pipelines.

## Recommendation Format

Always state the smallest sufficient option: unified model, tactical read model, CQRS with outbox, or event-sourced CQRS.
