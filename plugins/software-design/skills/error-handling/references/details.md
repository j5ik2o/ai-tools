# Error Handling Details

## Recoverability Axis

Use typed errors for conditions callers can reasonably handle. Use exceptions or fail-fast behavior for defects or conditions the local caller cannot fix.

## Domain Layer

Domain rules should expose expected failures explicitly, commonly with `Result`, `Either`, sealed error types, or language-specific equivalents. Avoid exceptions for normal business branching.

## Application Layer

Translate domain errors into use-case results. Own transaction, retry orchestration, and boundary conversion.

## Infrastructure Layer

Wrap low-level errors with context, but convert them before they leak into domain APIs. Add timeouts, retries, and circuit breakers at integration boundaries.

## Logging

Log once where the error is handled or reported. Include correlation IDs and safe identifiers. Avoid secrets and personal data.

## Tests

Test expected domain errors, mapping at boundaries, retry behavior, and that defects are not swallowed silently.
