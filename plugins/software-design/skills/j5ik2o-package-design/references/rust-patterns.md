# Rust Package Design Patterns

## Module Visibility

Use `pub(crate)` for crate-internal APIs and re-export only stable types from `lib.rs`.

## Suggested Shape

```text
src/
  domain/
  application/
  adapters/
  infrastructure/
```

Use this only when it matches the project's architecture. Smaller crates may prefer feature-oriented modules.

## Cycles

Rust module cycles usually show up as ownership or visibility pressure. Break them by extracting stable domain types, ports, or events.
