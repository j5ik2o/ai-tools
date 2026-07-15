# Python Aggregate Patterns

Use frozen dataclasses or explicit private attributes when immutability matters. Provide classmethods for validated construction.

```python
@dataclass(frozen=True)
class Order:
    id: OrderId
    customer_id: CustomerId
    items: tuple[OrderItem, ...]
    status: OrderStatus

    @classmethod
    def create(cls, id: OrderId, customer_id: CustomerId, items: Iterable[OrderItem]) -> "Order":
        item_tuple = tuple(items)
        if not item_tuple:
            raise EmptyOrder()
        return cls(id=id, customer_id=customer_id, items=item_tuple, status=OrderStatus.DRAFT)
```

Avoid exposing mutable lists. Use tuples, copies, or intention-revealing methods.
