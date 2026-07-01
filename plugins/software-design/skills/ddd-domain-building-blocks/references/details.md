# DDD Building Blocks Details

## Value Object

A value object has no identity, is compared by value, is immutable, and protects its own invariants. Examples include Money, EmailAddress, DateRange, and Quantity.

## Entity

An entity has stable identity and lifecycle. Equality is based on identity, not all fields. Put behavior that depends on the entity's state on the entity.

## Aggregate

An aggregate is a consistency boundary with one root. External code talks to the root. Repositories load and save aggregate roots.

## Domain Service

Use a domain service for stateless domain behavior that does not naturally belong to one entity or value object. Do not use it as a dumping ground for application orchestration.

## Factory

Use a factory when construction is complex, named, or must protect invariants across multiple values.

## Domain Event

A domain event is a past-tense fact meaningful to the business. It is not a command and should not describe implementation mechanics.

## Classification Questions

Does the concept have identity? Does it have lifecycle? Is it immutable? Does it enforce an invariant? Is behavior currently scattered around it? These answers determine the building block.
