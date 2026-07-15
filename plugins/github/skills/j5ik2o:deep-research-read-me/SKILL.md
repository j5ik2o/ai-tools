---
name: j5ik2o:deep-research-read-me
description: >
  Create, improve, and review GitHub OSS README.md files. Organize information
  around What, Why, How to start, Help, and Maintainers, and make the shortest
  credible path to Quickstart and docs obvious. Use this skill for new README
  creation, README restructuring, README review, and deciding when detailed
  documentation should move out of the README. Trigger on README-related
  requests such as "create a README", "improve this README", "add a
  Quickstart", "make a GitHub README template", or "review this README".
---

# Deep Research Read Me

Shape a GitHub OSS README so readers quickly understand what the project does and how to start using it.

## Workflow

1. Confirm the context.
   - Identify the project type: library, CLI, web app, or GitHub Action.
   - Identify the target reader: user, evaluator, or contributor.
   - Identify the README goal: create, improve, or review.

2. Build the first view.
   - Put the project name in the H1.
   - State the value in one or two sentences before explaining the technology stack.
   - Provide the shortest path to Quickstart.
   - Include only essential links, such as Docs, Issues, and Releases.

3. Make Quickstart short.
   - Keep it to roughly three to six lines in this order: `Requirements`, `Install`, `Run`.
   - Keep only commands that can actually be run.
   - Move long OS-specific setup paths to `docs/installation.md`.

4. Finish the structure.
   - Use these sections as the default shape:
     - `Highlights`
     - `Quickstart`
     - `Usage`
     - `Documentation`
     - `Getting help`
     - `Contributing`
     - `License`
   - Move detailed explanations to `docs/` and keep only relative links in the README.

5. Run the final review.
   - Confirm a reader can get from discovery to first successful run within five minutes.
   - Check for broken links, version assumptions, and stale instructions.
   - Use [`references/readme-review-checklist.md`](references/readme-review-checklist.md) for coverage.

## Output Template

When drafting README content, prefer the template in [`references/readme-template.md`](references/readme-template.md).

## Review Policy

When reviewing an existing README, prioritize findings in this order.

1. Critical
   - Quickstart cannot be executed.
   - Required information is missing: What, How to start, or Help.
   - The README is so large that the start path is buried.

2. Warning
   - Section order does not match the reader's decision flow.
   - Links to docs are weak or hard to find.
   - Too many badges or links obscure the project's value.

3. Info
   - Wording can be simpler.
   - Examples would help, such as CLI examples or minimal code examples.
   - FAQ or troubleshooting links would help.

## Reference Files

- Practical checklist: [`references/readme-review-checklist.md`](references/readme-review-checklist.md)
- README template: [`references/readme-template.md`](references/readme-template.md)
