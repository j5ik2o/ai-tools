# Domain Primitives And Always-Valid Details

## Always-Valid Model

An object should not exist in an invalid state. Instead of checking strings and numbers repeatedly, parse them into domain primitives that guarantee their own invariants.

## Candidate Signals

- The primitive has a domain name.
- Validation is repeated.
- Two same-typed values are easy to swap by mistake.
- The value has behavior.
- Invalid values cause business damage.

## Construction Patterns

- Private constructor plus `parse` or `create`.
- Return `Result` or `Either` for expected validation failure.
- Throw only when the language or framework convention makes it appropriate.
- Keep raw input at boundaries; pass domain primitives inward.

## Avoid Over-Wrapping

Do not wrap every string or integer. If there is no invariant, behavior, or misuse risk, a wrapper adds ceremony without correctness.

## Examples

Good candidates: EmailAddress, Money, Quantity, AccountId, DateRange, Percentage. Weak candidates: local loop counters, temporary pagination offsets, framework IDs with no domain rule.
