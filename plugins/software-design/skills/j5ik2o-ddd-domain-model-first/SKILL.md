---
name: j5ik2o-ddd-domain-model-first
description: >-
  Use when planning a DDD implementation flow that starts from the domain model and tests before infrastructure. Covers test-first domain modeling, in-memory repositories, use cases, and delaying persistence/framework choices. Trigger for starting from the domain model, TDD with DDD, in-memory repository design, use-case tests, or DDD development process.
---

# Domain Model First Development

Start with domain behavior you can test without infrastructure. Add delivery and persistence after the model earns them.

## Workflow

1. Write domain examples as tests using ubiquitous language.

2. Implement value objects, entities, aggregates, and domain services until the domain tests pass.

3. Add in-memory repositories for use-case tests.

4. Implement use cases as application orchestration over aggregate roots and ports.

5. Add infrastructure adapters last and verify they satisfy the same port contracts.

## Rules

- Do not let ORM annotations or API DTOs define the domain model.

- Use factories and constructors to protect invariants.

- Keep repository interfaces at the application boundary, not inside aggregates.

- Prefer fast tests until the domain behavior is stable.

## Detailed Reference

For non-trivial implementation, review, or refactoring work, read `references/details.md` before giving final guidance. It contains the detailed rules, examples, smells, and migration notes that do not belong in the short invocation body.

## Output

Return the implementation order, tests to write, domain API sketch, repository contract, and adapter plan.
