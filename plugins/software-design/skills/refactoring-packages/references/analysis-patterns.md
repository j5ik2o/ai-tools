# Package Refactoring Analysis Patterns

## Smells

- Circular dependencies.
- Large modules with unrelated change reasons.
- Public APIs that expose internals.
- Framework code mixed with domain policy.
- Duplicate package names with different meanings.

## Remedies

- Extract stable domain types.
- Move adapters outward.
- Introduce ports at application boundaries.
- Split by change reason, not by file count.
- Deprecate old imports before deleting them when consumers are broad.
