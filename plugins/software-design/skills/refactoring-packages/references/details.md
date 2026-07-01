# Refactoring Packages Details

## Goal

Improve dependency shape while preserving behavior. Structural refactoring should be easy to review and verify.

## Analysis Patterns

- Cycle: two packages import each other.
- God module: many unrelated change reasons.
- Leaky API: public types expose internals.
- Framework bleed: domain policy imports framework mechanisms.
- Wrong direction: stable policy depends on volatile detail.

## Execution Plan

1. Capture current checks.
2. Move one cohesive slice.
3. Update imports mechanically.
4. Run checks.
5. Repeat.

## Safety

Avoid renaming and moving unrelated concepts in the same commit. Avoid behavior changes unless they are required to preserve compilation after the move.

## Report

List the old location, new location, reason for move, affected imports, and verification result.
