# DDD Repository Design Details

## Repository Meaning

A repository is a collection-like abstraction for aggregate roots. It is not a generic DAO, query builder, or persistence utility.

## Method Design

Use methods that serve aggregate lifecycle and use-case needs: `findById`, `save`, `remove`, and named retrievals that express domain concepts. Avoid uncontrolled `findBy...` growth.

## Command And Query Separation

Command repositories return aggregate roots. Complex screens, searches, reports, and joins belong in query services or read models.

## Interface Shape

Define not-found behavior, optimistic locking, transaction ownership, and persistence errors. Keep ORM entities and SQL details out of the interface.

## Anti-Patterns

- Repository returns internal entities.
- Aggregate calls repository.
- Repository exposes `updateField` methods that bypass aggregate behavior.
- Generic base repository hides domain-specific semantics.
