# Rust Aggregate Patterns

Use private fields, validating constructors, and methods returning `Result<Self, DomainError>` or mutating through controlled methods when ownership makes immutable returns expensive.

```rust
pub struct Order {
    id: OrderId,
    customer_id: CustomerId,
    items: Vec<OrderItem>,
    status: OrderStatus,
}

impl Order {
    pub fn create(id: OrderId, customer_id: CustomerId, items: Vec<OrderItem>) -> Result<Self, DomainError> {
        if items.is_empty() {
            return Err(DomainError::EmptyOrder);
        }
        Ok(Self { id, customer_id, items, status: OrderStatus::Draft })
    }
}
```

Expose slices or iterators instead of mutable vectors.
