# Scala Aggregate Patterns

Use case classes for immutable state and methods that return `Either[DomainError, Aggregate]`.

```scala
final case class Order private (
  id: OrderId,
  customerId: CustomerId,
  items: Vector[OrderItem],
  status: OrderStatus
) {
  def addItem(item: OrderItem): Either[DomainError, Order] =
    Order.create(id, customerId, items :+ item, status)
}
```

Keep constructors private when invariants require factory validation. Use opaque types or value classes for domain primitives when they carry invariants.
