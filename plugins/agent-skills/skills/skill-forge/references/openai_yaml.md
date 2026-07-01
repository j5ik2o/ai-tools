# Codex agents/openai.yaml metadata

Use this reference when creating or improving a Codex-compatible skill.

## Purpose

`agents/openai.yaml` is optional Codex metadata for UI presentation, invocation policy, and tool dependency declarations. Codex still uses `SKILL.md` frontmatter `name` and `description` for skill discovery and triggering.

Add `agents/openai.yaml` when a skill is intended for Codex users, plugins, or marketplace-style distribution.

## Generate metadata

Run this from the `skill-forge` skill directory:

```bash
uv run python scripts/generate_openai_yaml.py <skill-dir>
```

Override interface fields when the generated defaults are too generic:

```bash
uv run python scripts/generate_openai_yaml.py <skill-dir> \
  --interface display_name="PDF Toolkit" \
  --interface short_description="Create and verify PDF files" \
  --interface default_prompt="Use $pdf-toolkit to inspect this PDF."
```

After changing `SKILL.md`, regenerate `agents/openai.yaml`.

## Validate metadata

Use strict validation before publishing a Codex skill:

```bash
uv run python scripts/quick_validate.py <skill-dir> --platform codex --strict-openai-yaml
```

Strict validation checks that:

- `agents/openai.yaml` exists.
- `agents/openai.yaml` contains the generated `SKILL.md` source hash.
- The generated source hash still matches the current `SKILL.md`.
- `interface.display_name`, `interface.short_description`, and `interface.default_prompt` are present and non-empty.
- `interface.short_description` is 25-64 characters.
- `interface.default_prompt` explicitly mentions the skill as `$skill-name`.
- Optional `policy.allow_implicit_invocation` is a boolean.
- Optional `dependencies.tools[]` entries use supported string fields.

Non-strict validation remains compatible with existing OpenAI bundled skills that omit some strict authoring constraints.

## Field constraints

### `interface.display_name`

Human-facing title shown in Codex skill lists and chips.

Use title case or the product's official capitalization. Keep it concise enough for UI labels.

### `interface.short_description`

Human-facing UI blurb for quick scanning.

Use 25-64 characters. State the job, not trigger logic. Examples:

- `Create and verify PDF files`
- `Draft and refine GitHub PRs`
- `Build spreadsheet workflows`

### `interface.default_prompt`

Prompt snippet inserted when invoking the skill.

Use one short sentence. Mention the skill explicitly as `$skill-name`, for example:

```yaml
default_prompt: "Use $pdf-toolkit to inspect this PDF."
```

### `policy.allow_implicit_invocation`

When `false`, Codex does not implicitly invoke the skill from a matching prompt. Explicit `$skill-name` invocation still works. Defaults to `true` when omitted.

### `dependencies.tools[]`

Declare external tool dependencies for UI and setup clarity.

Supported fields:

- `type`
- `value`
- `description`
- `transport`
- `url`

Only `type: "mcp"` is supported for now.

## Difference from OpenAI skill-creator

OpenAI's built-in `skill-creator`:

- Recommends `agents/openai.yaml` for UI metadata.
- Provides `references/openai_yaml.md`.
- Provides `scripts/generate_openai_yaml.py`.
- Treats `display_name`, `short_description`, and `default_prompt` as generated human-facing interface values.

skill-forge follows that shape, with two deliberate differences:

- `quick_validate.py` has a compatibility mode by default and a stricter `--strict-openai-yaml` mode for publishing.
- Strict validation detects stale metadata by comparing a generated `SKILL.md` source hash in `agents/openai.yaml`, so authors can catch forgotten regeneration after editing `SKILL.md` without relying on filesystem timestamps.
