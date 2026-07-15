# Tell, Don't Ask Patterns

## Getter Branch Smell

Before:

```typescript
if (account.balance().isLessThan(amount)) {
  account.freeze();
}
```

After:

```typescript
account.freezeIfWithdrawalWouldOverdraw(amount);
```

## Keep Asking At Boundaries

DTO mapping, serialization, rendering, logging, and persistence mapping may need data access. Keep those accessors out of domain decision flow.

## Refactoring Steps

1. Name the decision.
2. Move the decision to the data owner.
3. Keep returned data minimal.
4. Delete now-unused getters when possible.
