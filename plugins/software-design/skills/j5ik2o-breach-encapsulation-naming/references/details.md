# Breach Encapsulation Naming Details

## Intent

This pattern exists because ordinary getters are too comfortable. Once a domain model exposes `getName()` or `items`, callers start making decisions outside the object and the model becomes an anemic data holder. The breach name makes the cost visible every time state is exposed.

## Core Rule

Domain behavior should not consume breach accessors. If a caller reads state in order to make a business decision, move the decision to the object that owns the state. Keep breach accessors for integration seams that cannot use behavior-oriented APIs.

## Consumer Classification

| Consumer | Recommendation |
| --- | --- |
| Domain behavior | Replace with Tell Don't Ask behavior |
| Persistence mapper | Allow breach accessor |
| Serialization | Allow breach accessor or dedicated DTO mapper |
| Tests | Allow when behavior cannot be observed directly |
| UI projection | Prefer read model or DTO mapping |
| Framework reflection | Isolate in adapter or mapping layer |

## Design Notes

- Return immutable values or defensive copies for collections.
- Avoid `get` prefixes on aggregates and entities unless the project has a strong convention and a lint rule.
- Value objects may expose their wrapped value more freely when the value object is specifically a transparent domain primitive, but the exposure should still be intentional.
- Public fields are worse than getters because they remove any naming signal and mutation control.

## Migration

1. Find all public getters and public fields in domain entities and aggregates.
2. Classify each caller by consumer category.
3. Replace behavior callers first; they are the real encapsulation leaks.
4. Rename remaining tolerated accessors to the breach pattern.
5. Add lint or review rules so new ordinary getters do not reappear.
