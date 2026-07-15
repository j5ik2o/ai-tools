# Tell, Don't Ask Details

## Principle

Do not ask an object for its state, make a decision outside it, and then tell it what to do. Move the decision to the object that owns the state.

## Smells

- Getter followed by `if` followed by setter.
- Feature Envy: a method uses another object's data more than its own.
- Repeated conditionals checking the same object's state.
- Domain services full of object navigation and decisions.

## Refactoring

1. Name the intention of the external decision.
2. Add a method to the data owner that expresses that intention.
3. Move the conditional and mutation inside.
4. Keep returned data minimal.
5. Delete or demote getters if they are no longer needed.

## Exceptions

DTO mapping, rendering, serialization, logging, and persistence mapping may read state. The issue is domain decision-making outside the owner, not all data access.

## Relation To Encapsulation

Tell Don't Ask strengthens encapsulation by keeping rules and state together. Breach accessors should not be used to bypass this design.
