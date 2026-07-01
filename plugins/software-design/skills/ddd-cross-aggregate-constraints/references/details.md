# Cross-Aggregate Constraints Details

## First Question

Ask whether the rule is a true invariant or a business policy. A true invariant must be protected immediately inside one aggregate boundary. A policy can be eventual and repaired.

## Examples

- "An order total equals the sum of lines" is usually a true invariant inside Order.
- "A customer cannot place an order if suspended" may be a policy depending on tolerated race conditions.
- "A brand cannot be deleted while products exist" may require boundary redesign, a read-model check with accepted staleness, or a deletion process that can fail later.

## Saga Caution

A saga coordinates steps; it does not magically create immediate consistency. If the first command must not happen unless another aggregate state is current, a saga may be too late.

## CQRS/ES Constraint

Command-side reads from projections are stale by design. Use them only when the business accepts stale decisions. Otherwise use a reservation, same aggregate boundary, or synchronous domain service backed by a strongly consistent source.

## Decision Record

Document chosen consistency, stale-data risk, retry behavior, compensation, and the business owner who accepted the tradeoff.
