# First Class Collection Details

## Rule

A first-class collection wraps one collection and gives it domain behavior. It should not accumulate unrelated fields. If it needs identity or lifecycle, it may be an entity or aggregate instead.

## Good Candidates

- Repeated total, filter, ordering, uniqueness, max-size, or membership rules.
- Collections with a domain name: OrderLines, Members, Seats, Permissions.
- Collections whose invariants are easy to break when exposed raw.

## API Design

Expose intention-revealing methods such as `addLine`, `total`, `hasQuorum`, `containsActiveMember`, or `withoutCancelled`. Avoid exposing mutable lists.

## Implementation

Use immutable collections, copies, slices, iterators, or read-only views. Validate invariants in constructors or factories.

## Avoid

Do not wrap a list just to forward `map`, `filter`, and `length`. The wrapper must centralize domain behavior.
