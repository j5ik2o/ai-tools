# DDD Module Language Guides

## TypeScript

Use package exports or index files to expose a narrow API. Keep internals outside exported paths. Avoid barrel files that expose everything.

## Java And Kotlin

Use packages by bounded context or domain concept. Keep constructors, entities, and mappers package-private where possible. Use application services as module entry points.

## Scala

Use packages, `private[context]`, opaque types, and companion objects to control construction and visibility.

## Rust

Use `mod`, `pub(crate)`, and re-exports from `mod.rs` or `lib.rs` to expose stable APIs while hiding internal modules.

## Python

Use package boundaries and leading underscores for internals, but document that privacy is conventional. Keep domain APIs small and tested.
