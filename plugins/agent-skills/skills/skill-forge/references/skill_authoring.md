# Skill authoring guide

Read this reference when drafting or reviewing a `SKILL.md`, especially when the
skill body is getting long or the trigger boundary is ambiguous.

## Anatomy of a skill

```text
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description required)
│   └── Markdown instructions
├── agents/
│   └── openai.yaml - Codex UI metadata, invocation policy, and tool dependencies
└── Bundled Resources (optional)
    ├── scripts/    - Executable code for deterministic/repetitive tasks
    ├── references/ - Docs loaded into context as needed
    └── assets/     - Files used in output (templates, icons, fonts)
```

## Progressive disclosure

Skills use a three-level loading system:

1. **Metadata** (`name` + `description`) - Always in context.
2. **SKILL.md body** - Loaded whenever the skill triggers. Keep this concise;
   under 500 lines is the target.
3. **Bundled resources** - Loaded as needed. Scripts can execute without loading
   all of their source into the model context.

Use bundled resources when:

- The `SKILL.md` body is approaching 500 lines.
- A section is only relevant for one branch, platform, framework, or advanced
  workflow.
- The content is mostly reference material, examples, schemas, or long commands.

Reference files must be discoverable from `SKILL.md`. Name the file and explain
when to read it. For large reference files, include a short table of contents.

When a skill supports multiple domains or frameworks, organize by variant:

```text
cloud-deploy/
├── SKILL.md
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```

The agent should read only the relevant reference file.

## Principle of lack of surprise

Skills must not contain malware, exploit code, hidden data exfiltration, or any
instruction that would surprise the user relative to the skill's stated purpose.
Do not create misleading skills or skills designed to facilitate unauthorized
access. Roleplay or style skills are fine when their behavior is transparent.

## Writing patterns

Prefer imperative instructions. Explain why a behavior matters instead of relying
on rigid all-caps rules.

For fixed report formats, give the exact template:

```markdown
## Report structure
ALWAYS use this exact template:
# [Title]
## Executive summary
## Key findings
## Recommendations
```

For examples, make the input/output relationship explicit:

```markdown
## Commit message format
**Example 1:**
Input: Added user authentication with JWT tokens
Output: feat(auth): implement JWT-based authentication
```

## Writing style

Start with a draft, then reread it with fresh eyes. The final skill should be
general enough to help with future tasks, not overfit to one example prompt.

Use the skill body for durable workflow instructions. Put trigger criteria in
frontmatter `description`, because the model decides whether to use a skill from
the name and description before it reads the body.

Avoid speculative flexibility. Prefer clear, concrete instructions, especially
around tools, file locations, outputs, and verification steps.

## Test cases

After writing a skill draft, propose 2-3 realistic test prompts and ask the user
whether they look right. Save test cases to `evals/evals.json` inside the skill
directory:

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "User's task prompt",
      "expected_output": "Description of expected result",
      "files": []
    }
  ]
}
```

Do not write expectations yet. Draft them while eval runs are in progress. See
`references/schemas.md` for the full schema, including the canonical
`expectations` field.
