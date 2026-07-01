# Error Handling Guidelines

## By Error Kind

- Domain error: typed return value such as `Result` or `Either`.
- Validation error: typed return with field/path details.
- Infrastructure error: boundary exception or typed adapter error converted at the application layer.
- Programming defect: fail fast; do not turn it into business flow.
- Fatal system condition: stop, alert, or let the runtime supervisor handle it.

## Logging

Log at the boundary that handles the error. Avoid logging the same error at every layer.

## Context

Preserve causal context, operation name, correlation id, and safe identifiers. Do not log secrets or full personal data.

## Retries

Retries belong at integration boundaries and require idempotency, timeout, backoff, and observability.
