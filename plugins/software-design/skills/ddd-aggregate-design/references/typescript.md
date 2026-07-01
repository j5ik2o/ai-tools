# TypeScript Aggregate Patterns

Use private props plus immutable updates.

```typescript
type OrderProps = {
  id: OrderId;
  customerId: CustomerId;
  items: readonly OrderItem[];
  status: OrderStatus;
};

class Order {
  private constructor(private readonly props: OrderProps) {}

  static create(props: OrderProps): Result<Order, DomainError> {
    if (props.items.length === 0) return err(new EmptyOrder());
    return ok(new Order({ ...props, items: [...props.items] }));
  }

  addItem(item: OrderItem): Result<Order, DomainError> {
    return Order.create({ ...this.props, items: [...this.props.items, item] });
  }
}
```

Avoid public mutable fields and direct child collection mutation.
