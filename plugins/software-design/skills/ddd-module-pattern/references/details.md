# DDD Module Pattern Details

## Goal

Modules should create a language boundary. They hide internal representation and expose commands, queries, ports, and domain types that other modules are allowed to use.

## Grouping

Prefer grouping by bounded context, subdomain, or domain concept. Avoid splitting a cohesive domain concept across technical folders that force callers to know internals.

## Public API

The public module API should be smaller than the internal implementation. Re-export only stable concepts. Hide constructors when factories protect invariants.

## Dependency Direction

Domain modules should not depend on adapters. Application modules can depend on domain modules and ports. Adapter modules implement ports and translate external data.

## Shared Kernel

Use shared kernels sparingly. Shared domain primitives and common abstractions must be stable because every consumer inherits their changes.

## Language Enforcement

Use package-private visibility, module exports, `pub(crate)`, companion objects, or underscore conventions depending on language.
