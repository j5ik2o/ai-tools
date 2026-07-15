# Intent-Based Deduplication Details

## Principle

DRY applies to knowledge and intent, not visual similarity. Two snippets can look identical today and still need to change independently tomorrow.

## Analysis Questions

- Why does each copy exist?
- Who owns each behavior?
- What future changes are likely?
- Do both copies protect the same invariant?
- Would a shared abstraction have an honest domain or technical name?

## Decisions

| Same text | Same intent | Decision |
| --- | --- | --- |
| Yes | Yes | Merge |
| Yes | No | Keep separate |
| No | Yes | Consider unifying |
| No | No | Keep separate |

## Bad Abstraction Smells

Names like `handleCommonThing`, boolean flags controlling unrelated behavior, and shared helpers that change every time one caller changes.

## Safe Extraction

Mechanical helpers are acceptable when they do not pretend to be domain concepts and do not couple different change reasons.
