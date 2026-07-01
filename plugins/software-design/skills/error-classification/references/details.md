# Error Classification Details

## Terms

| Term | Meaning |
| --- | --- |
| Error | A human or system mistake in reasoning, input, configuration, or operation |
| Defect | A flaw in an artifact such as code, requirements, tests, or docs |
| Bug | Informal label that must be mapped to defect, fault, or failure |
| Fault | An incorrect internal condition that may cause failure |
| Failure | Externally observable deviation from expected service |
| Incident | An operational event requiring response |
| Exception | A language/runtime mechanism that carries or signals an abnormal condition |

## Classification Chain

User-visible failure may be caused by an internal fault, which may be caused by a code defect, which may originate from a human error in requirements or implementation.

An exception may be how a fault or failure is surfaced, but the exception itself does not tell you whether the underlying condition is a domain error, validation error, infrastructure fault, or programming defect.

## Design Consequences

- Validation errors are usually user-correctable.
- Domain errors are expected business outcomes.
- Infrastructure faults may need retry or fallback.
- Defects should be fixed, not modeled as normal flow.
- Failures require observability and sometimes incident response.

## Review Output

Name the observed failure, likely fault, suspected defect, and prevention strategy.
