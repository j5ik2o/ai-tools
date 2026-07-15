# Package Design Principles

## Information Hiding

Hide decisions that are likely to change: persistence choices, external APIs, algorithms, policies, and framework details.

## Change Reasons

Packages should group code that changes together and separate code that changes for different reasons.

## Dependency Direction

Stable policy should not depend on volatile mechanisms. Use interfaces, ports, or events where a stable package must coordinate with a volatile one.

## Public API

The public API is the package contract. Keep it small, named in domain language, and tested.

## Migration

Move in vertical slices. Preserve behavior, update imports mechanically, and run checks after each batch.
