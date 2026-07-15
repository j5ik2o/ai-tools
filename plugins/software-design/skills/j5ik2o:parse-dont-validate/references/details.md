# Parse, Don't Validate Details

## Problem

Validation that returns `bool`, `void`, or throws while leaving the original primitive in circulation loses information. Every downstream caller must trust that validation happened earlier.

## Pattern

Parse input into a type that proves the invariant. Downstream APIs accept the parsed type, not the raw value.

## Examples

- `EmailAddress.parse(raw)` returns `Result<EmailAddress, EmailError>`.
- `NonEmptyString.create(raw)` prevents empty names.
- `DateRange.create(start, end)` prevents reversed ranges.

## Migration

1. Find validation calls followed by use of the raw value.
2. Introduce parsed type.
3. Change the nearest downstream API to accept the parsed type.
4. Push parsing to input boundaries.
5. Delete redundant validation.

## Caveats

Parsing does not mean every wrapper is valuable. The invariant must matter enough to justify the type.
