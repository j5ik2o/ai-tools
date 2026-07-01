# Custom Linter Creator Details

## Purpose

These linters are often written for AI agents as much as for humans. The diagnostic should be a repair prompt with enough context that the next agent can fix the issue without rediscovering the rule.

## Rule Design

1. Make the rule statically detectable.
2. Keep false positives low; a noisy linter will be ignored.
3. Include examples of allowed and forbidden code.
4. Provide suppression policy only if the project needs it.
5. Test diagnostics, not just detection.

## Ecosystem Defaults

| Language | Recommended ecosystem |
| --- | --- |
| TypeScript/JavaScript | ESLint |
| Python | pylint for custom rules |
| Go | `golang.org/x/tools/go/analysis` |
| Rust | dylint or Clippy-style tooling |

## Diagnostic Contract

Use this shape:

```text
Problem: <what violates the project rule>
Repair:
1. <mechanical step>
2. <follow-up step>
Scope: <files the agent may change>
Rationale: <why the rule exists>
```

## Directory Shape

Place custom rules under `lints/` so they are discoverable and separate from production code. Add fixtures and a command that CI can run.
