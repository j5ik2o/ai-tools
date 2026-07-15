# Breach Encapsulation Naming Patterns

## Naming By Language

Use the clearest local spelling while preserving the warning word.

| Language | Pattern |
| --- | --- |
| Java/Kotlin/Scala/TypeScript | `breachEncapsulationOfName()` |
| Python | `breach_encapsulation_of_name()` |
| Go | `BreachEncapsulationOfName()` for exported access, `breachEncapsulationOfName()` for package-local access |
| Rust | `breach_encapsulation_of_name()` |

## Allowed Consumers

- Persistence mappers.
- Serializers and deserializers.
- Test assertions that cannot observe behavior directly.
- Framework glue that cannot use richer domain APIs.

## Migration

1. Find ordinary getters on domain entities and aggregates.
2. Classify each caller as behavior, persistence, serialization, test, or presentation.
3. Convert behavior callers to Tell Don't Ask methods.
4. Rename tolerated accessors to the breach pattern.
5. Add lint or review rules for new ordinary getters.
