# When To Wrap Primitives Details

## Balance

Primitive obsession causes repeated validation and swapped values. Value-object obsession creates noise and slows change. Choose based on risk and behavior.

## Scoring Questions

1. Does the value have a domain name?
2. Does it have an invariant?
3. Is it reused across boundaries?
4. Can it be confused with another same-typed value?
5. Does behavior belong with it?
6. Is migration cost acceptable?

## Definition Conflicts

"Value Object" can mean a DDD value object, a persistence object, or a general immutable data object depending on context. Clarify the meaning before reviewing code.

## Strong Wrappers

EmailAddress, Money, Quantity, NonEmptyName, DateRange, AccountId, OrderId, and Percentage often earn wrappers.

## Weak Wrappers

One-off local values, technical offsets, and values with no invariant or behavior often do not.
