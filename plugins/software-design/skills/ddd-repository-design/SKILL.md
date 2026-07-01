---
name: ddd-repository-design
description: >-
  Use when designing or reviewing repositories in DDD. Treats repositories as collection-like access to aggregate roots, not generic DAO layers, and separates query/read-model concerns from command persistence. Trigger for repository interfaces, aggregate persistence, save/load semantics, query placement, ORM leakage, or repository anti-patterns.
---

# DDD Repository Design

A repository gives use cases collection-like access to aggregate roots. It should not become a general database API.

## Workflow

1. Identify the aggregate root the repository owns.

2. Keep methods aligned with aggregate retrieval and persistence needs.

3. Put complex read/query screens in query services or read models, not command repositories.

4. Hide ORM, SQL, and transport details behind the implementation.

5. Define optimistic locking, transactions, and not-found behavior explicitly.

## Rules

- Repositories return aggregate roots, not internal entities.

- Repository interfaces should not be used by domain objects.

- Avoid generic `findByAnything` growth.

- Use specifications only when they express stable domain query concepts.

## Detailed Reference

For non-trivial implementation, review, or refactoring work, read `references/details.md` before giving final guidance. It contains the detailed rules, examples, smells, and migration notes that do not belong in the short invocation body.

## Output

Return the repository interface, method rationale, transaction expectations, and adapter responsibilities.
