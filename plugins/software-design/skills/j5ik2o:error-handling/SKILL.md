---
name: j5ik2o:error-handling
description: >-
  Use when designing or reviewing error handling across domain logic, application services, and infrastructure. Uses recoverability to choose typed errors, Result/Either, exceptions, retries, and logging. Trigger for improving error handling, Result types, exception design, recoverable errors, domain errors, or error-handling refactors.
---

# Error Handling

Choose error mechanisms by recoverability and caller responsibility.

## Workflow

1. Classify each error as domain, validation, application, infrastructure, programming defect, or fatal system condition.

2. Use typed `Result`/`Either`-style returns for recoverable domain and validation errors.

3. Use exceptions or panics for defects and truly exceptional infrastructure failures when callers cannot make a local decision.

4. Preserve causal context without leaking secrets.

5. Put retry, timeout, and circuit-breaker policy at integration boundaries.

## Rules

- Domain errors should be explicit in function signatures where the language supports it.

- Do not use exceptions for ordinary business branching.

- Log once at the boundary that handles or reports the error.

- Convert low-level errors into application-facing errors at layer boundaries.

## Reference

Read `references/guidelines.md` for detailed patterns.

## Detailed Reference

For non-trivial implementation, review, or refactoring work, read `references/details.md` before giving final guidance. It contains the detailed rules, examples, smells, and migration notes that do not belong in the short invocation body.

## Output

Return the error taxonomy, mechanism choices, API changes, and tests.
