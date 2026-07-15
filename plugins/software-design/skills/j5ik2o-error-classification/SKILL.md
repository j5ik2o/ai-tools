---
name: j5ik2o-error-classification
description: >-
  Use when clarifying software abnormal-state terminology such as error, defect, fault, failure, bug, incident, and exception. Helps choose handling, testing, and mitigation strategies from precise classification. Trigger for error terminology, fault versus failure, defect versus bug, abnormal-state design, failure analysis, or test classification.
---

# Error Classification

Classify abnormal states before designing their handling. Different words imply different interventions.

## Working Vocabulary

- Error: a human or system mistake in reasoning, input, configuration, or operation.

- Defect: a flaw in an artifact such as code, requirements, tests, or documentation.

- Bug: an informal report or label for a defect, fault, or failure; clarify which precise category is meant before choosing a response.

- Fault: an incorrect internal state or latent condition that can cause failure.

- Failure: externally observable deviation from expected service.

- Incident: an operational event requiring response.

- Exception: a language/runtime control mechanism or signal, not a domain classification by itself; classify the condition it represents.

## Workflow

1. Describe what was observed and by whom.

2. Separate external failure from internal fault and underlying defect.

3. Identify whether the condition is recoverable, retryable, user-correctable, or fatal.

4. Choose handling: validation error, typed domain error, exception, retry, circuit breaker, alert, or defect fix.

## Detailed Reference

For non-trivial implementation, review, or refactoring work, read `references/details.md` before giving final guidance. It contains the detailed rules, examples, smells, and migration notes that do not belong in the short invocation body.

## Output

Return the classification chain, handling strategy, tests to add, and terms the team should use consistently.
