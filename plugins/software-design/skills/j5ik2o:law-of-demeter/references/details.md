# Law Of Demeter Details

## Principle

A method should talk to itself, its parameters, objects it creates, its direct fields, and stable collaborators. It should not navigate through collaborators to reach strangers.

## Train Wreck

Chains like `order.customer().account().status().isBlocked()` expose internal structure. If the path changes, every caller breaks.

## Refactoring

1. Identify the decision made after navigation.
2. Move the decision to the object that owns the required knowledge.
3. Replace the chain with an intention-revealing method.
4. Keep DTO traversal at boundaries where behavior is not being modeled.

## Exceptions

Builders, fluent query DSLs, immutable data transformations, and serialization code may use chains without violating the design intent.

## Relation To Tell Don't Ask

Law of Demeter identifies structural over-navigation. Tell Don't Ask identifies behavior that should move to the data owner. They often point to the same refactoring.
