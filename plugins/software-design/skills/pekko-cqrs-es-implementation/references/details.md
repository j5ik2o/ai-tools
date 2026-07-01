# Pekko CQRS/ES Implementation Details

## Scope

This guide is for Scala 3, Apache Pekko, CQRS, and Event Sourcing implementation work. Do not apply it to generic CQRS theory or non-Pekko stacks.

## Architecture

Separate the domain model from the actor shell. The actor receives commands, delegates domain decisions, persists events, and applies events to state. The domain model should be testable without Pekko.

## Command Handling

Command handling should:

1. Validate current state and command data.
2. Return domain errors for rejected commands.
3. Emit one or more past-tense events for accepted commands.
4. Avoid direct state mutation before persistence succeeds.

## State Transitions

Apply events through pure functions. Recovery must produce the same state as live command processing.

## Serialization

Persisted events are long-lived contracts. Use Protocol Buffers schemas with stable field numbers, explicit versioning strategy, and compatibility tests.

## Use Cases

Keep ZIO/application services responsible for orchestration, authorization, transactions outside the event-sourced entity, and integration with repositories or actor refs.

## Projections

Read-model updaters must be idempotent and retry-safe. Store projection offsets and handle duplicate events.
