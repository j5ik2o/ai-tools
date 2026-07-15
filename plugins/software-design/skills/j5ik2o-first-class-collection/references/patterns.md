# First Class Collection Patterns

## Good Wrapper

```typescript
class OrderLines {
  private constructor(private readonly lines: readonly OrderLine[]) {}

  total(): Money {
    return this.lines.reduce((sum, line) => sum.add(line.subtotal()), Money.zero());
  }
}
```

## Use When

- Collection operations are repeated.
- The collection has a domain name.
- There are invariants such as max size, uniqueness, ordering, or totals.

## Avoid When

- The wrapper only forwards `map`, `filter`, and `length`.
- Extra fields make it an entity or aggregate.
