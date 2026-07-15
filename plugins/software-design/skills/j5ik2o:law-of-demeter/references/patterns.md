# Law Of Demeter Patterns

## Replace Navigation With Intention

Before:

```typescript
if (order.customer().account().isDelinquent()) {
  order.reject();
}
```

After:

```typescript
order.rejectIfCustomerAccountIsDelinquent();
```

## Legitimate Chains

- Builders and fluent APIs.
- Query DSLs.
- DTO mapping at boundaries.
- Pure data traversal in serialization code.

## Smell

Repeated chains across the codebase indicate missing behavior or an unstable object boundary.
