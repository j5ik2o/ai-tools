# Package Design Details

## Parnas Principle

Package boundaries should hide design decisions likely to change. The key question is not "where does this file look tidy?" but "what change should not ripple beyond this boundary?"

## Analysis

1. List likely change reasons.
2. Draw dependency direction.
3. Find cycles and unstable public APIs.
4. Identify policies depending on mechanisms.
5. Identify modules with unrelated responsibilities.

## Boundary Candidates

- Domain concepts and bounded contexts.
- External integration adapters.
- Algorithms or policies likely to vary.
- Persistence details.
- UI or delivery mechanisms.

## Public API

Expose stable concepts and hide volatile details. A package with a large public surface is not hiding much.

## Migration

Prefer small moves: create target package, move cohesive files, update imports, run tests, then continue. Do not combine structural refactoring with behavior changes unless necessary.
