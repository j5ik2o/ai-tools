---
name: j5ik2o:skill-forge
description: >-
  Create or improve Claude Code and Codex skills. Use only when the request is
  explicitly about the skill itself: creating a new skill, editing a SKILL.md
  file, testing a skill draft in .claude/skills/.../SKILL.md or
  .agents/skills/.../SKILL.md, improving an existing skill, debugging why a
  skill is not triggering, running evals or benchmarks for a skill, or turning
  an already-described workflow into a reusable skill. Trigger on phrases like
  existing skill, skill draft, SKILL.md, skill trigger, skill eval, make this
  into a skill, or turn this workflow into a skill. Do not use for ordinary
  implementation work unless the user explicitly mentions a skill, SKILL.md,
  or converting the task into a skill. That exclusion includes generic coding
  tasks, generic automation/workflow setup, CI setup, GitHub Actions
  workflows, debugging, code review, database migrations, schema changes, and
  production incident response when the user is just asking for help with the
  task itself.
---

# Skill Forge

Use this skill to create, test, improve, package, and maintain Claude Code and
Codex skills.

The default loop is:

1. Understand the intended skill boundary.
2. Draft or edit `SKILL.md`.
3. Create realistic eval prompts.
4. Run the skill and an appropriate baseline.
5. Grade, aggregate, and show the user the viewer.
6. Improve from feedback and repeat.
7. Optionally optimize the frontmatter description and package the skill.

If the user only wants brainstorming, skip evals and act as a design partner.
If the user already has a draft, start at validation, evals, or iteration.

## Progressive disclosure map

Read only the reference files needed for the current branch:

- `references/skill_authoring.md` - read before drafting, reviewing, or large
  refactoring a `SKILL.md`, especially when the body may approach 500 lines or
  existing skill knowledge is being shortened, reorganized, translated, or moved
  into references.
- `references/eval_workflow.md` - read before running test cases, benchmarks,
  grading, viewer generation, blind comparison, or iteration from feedback.
- `references/description_optimization.md` - read before optimizing or debugging
  a skill's trigger description. It requires you to read the target skill's `SKILL.md`,
  extracting `helps with` and `should not help with`, then reviewing trigger
  evals with the user.
- `references/openai_yaml.md` - read before generating or reviewing Codex
  `agents/openai.yaml` metadata.
- `references/skill_creator_comparison.md` - read before updating platform
  assumptions or comparing skill-forge against Anthropic/OpenAI creator flows.
- `references/trigger_eval_boundaries.md` - read before changing trigger eval
  parsing or interpreting surprising Claude Code / Codex CLI trigger results.
- `references/schemas.md` - read before writing or manually inspecting
  `evals.json`, `eval_metadata.json`, `grading.json`, or `benchmark.json`.
- `references/platform_notes.md` - read when running in Claude.ai, Cowork, or a
  headless environment.

The `agents/` directory contains specialized subagent instructions:

- `agents/grader.md` - how to evaluate expectations against outputs.
- `agents/comparator.md` - how to do blind A/B comparison.
- `agents/analyzer.md` - how to analyze benchmark results.

## Communicating with the user

Skill Forge may be used by people with very different levels of coding
familiarity. Match the user's vocabulary. In the default case, terms like
"evaluation" and "benchmark" are OK, while "JSON" and "expectation" may need a
short definition.

Explain tradeoffs plainly. Ask for confirmation before running an expensive eval
loop, changing trigger behavior, or packaging a skill.

## Creating or editing a skill

Start by extracting what the conversation already tells you. If the user says
"turn this into a skill", reuse the observed workflow, tools, corrections,
inputs, and outputs before asking more questions.

Clarify these points:

1. What should the skill enable the agent to do?
2. When should the skill trigger?
3. What output should it produce?
4. Should the skill be Claude-only, Codex-only, or compatible with both?
5. Should evals be added now?

When drafting, read `references/skill_authoring.md`. At minimum, produce:

- `name`: stable skill identifier.
- `description`: the trigger boundary. Put all "when to use" guidance here.
- `compatibility`: optional requirements, only when useful.
- Body instructions: the durable workflow and pointers to bundled resources.

Descriptions should be direct and a little pushy for true positives, because
skills can under-trigger. Also include explicit exclusions for near misses so the
skill does not hijack ordinary coding, docs, or operations work.

After editing `SKILL.md`, validate it and regenerate Codex metadata when present.

## Python environment setup

Before running scripts, ensure the Python environment is ready from the
j5ik2o:skill-forge directory. Because `:` cannot appear in a virtual-environment
path-list entry, keep the uv environment outside the namespaced skill directory:

```bash
export UV_PROJECT_ENVIRONMENT="${UV_PROJECT_ENVIRONMENT:-${TMPDIR:-/tmp}/j5ik2o-skill-forge-venv}"
uv sync --group dev
```

Use `uv run` for every script call. If `uv` is missing, direct the user to
https://docs.astral.sh/uv/.

## Validating skills

For Codex-compatible skills, read `references/openai_yaml.md` before generating
or reviewing `agents/openai.yaml`.

Generate Codex UI metadata after the target skill has stable `SKILL.md`
frontmatter:

```bash
uv run python -m scripts.generate_openai_yaml <skill-dir>
```

Run validation before packaging or publishing:

```bash
uv run python -m scripts.quick_validate <skill-dir>
uv run python -m scripts.quick_validate <skill-dir> --platform claude
uv run python -m scripts.quick_validate <skill-dir> --platform codex
uv run python -m scripts.quick_validate <skill-dir> --platform codex --strict-openai-yaml
```

Use `--platform claude` for Claude Code-only frontmatter such as
`disable-model-invocation`, `user-invocable`, or `when_to_use`. Use
`--platform codex` for Codex skills and `agents/openai.yaml`. Use
`--strict-openai-yaml` before publishing Codex metadata; it requires
`display_name`, `short_description`, and `default_prompt`, and detects stale
metadata after `SKILL.md` changes.

## Evals and benchmarks

Before running evals, read `references/eval_workflow.md`.

Core rules:

- Create an isolated workspace and show the path to the user.
- For each test case, start the with-skill run and baseline run in the same turn.
- Run each task in its own working directory under the workspace.
- Write `eval_metadata.json` for each test case; new files start with
  `"expectations": []`.
- Draft expectations while runs are in progress.
- Save timing data as run notifications arrive.
- Grade using `agents/grader.md`.
- Aggregate with `scripts.aggregate_benchmark`.
- Generate the human review UI with `eval-viewer/generate_review.py`; do not
  write custom viewer HTML.
- Read user feedback before revising the skill again.

For schema details, read `references/schemas.md`. Writers must emit
`expectations`; old `assertions` are only a legacy alias for readers.

## Improving a skill

Improve from evidence, not from vibes alone:

- For large refactors of existing skills, run the preservation pass in
  `references/skill_authoring.md` before editing and before final validation.
  Do not treat "shorten", "organize", "Englishize", or "move to references" as
  permission to discard behavior-shaping skill knowledge.
- Generalize from user feedback instead of overfitting to one eval prompt.
- Read transcripts when outputs are surprising.
- Remove instructions that cause repeated wasted work.
- Bundle helper scripts when multiple evals reinvent the same deterministic
  helper.
- Rerun the eval workflow after meaningful changes.

For blind A/B comparison, read `agents/comparator.md` and `agents/analyzer.md`.

## Description optimization

After the skill body is stable, offer trigger optimization. Read
`references/description_optimization.md` before starting.

Minimum workflow:

1. Read the target skill's `SKILL.md`.
2. Extract `helps with` and `should not help with`.
3. Draft should-trigger and should-not-trigger queries.
4. Let the user review the query set with `assets/eval_review.html`.
5. Run `scripts.run_loop` with the right CLI.
6. Apply `best_description`, show before/after, and report scores.

Claude Code example:

```bash
uv run python -m scripts.run_loop \
  --eval-set <path-to-trigger-eval.json> \
  --skill-path <path-to-skill> \
  --model <model-id-powering-this-session> \
  --max-iterations 5 \
  --verbose
```

Codex CLI example:

```bash
uv run python -m scripts.run_loop \
  --eval-set <path-to-trigger-eval.json> \
  --skill-path <path-to-skill> \
  --model <model-id-powering-this-session> \
  --cli codex \
  --max-iterations 5 \
  --verbose
```

No separate Anthropic API client setup is required for the optimization loop.
Before interpreting `status: "error"` or `status: "not_run"`, read
`references/trigger_eval_boundaries.md`.

## Platform-specific branches

For Claude.ai, Cowork, and headless environments, read
`references/platform_notes.md` before adapting the workflow.

Short version:

- Claude.ai has no subagents, so run test cases yourself, skip baselines, and
  focus on qualitative review.
- Cowork has subagents but may lack a browser; generate a static viewer with
  `eval-viewer/generate_review.py --static <output_path>`.
- Description optimization requires `claude -p` or `codex exec`; skip it when no
  suitable CLI is available.

## Package and present

If a file presentation tool is available, package the final skill:

```bash
uv run python -m scripts.package_skill <path/to/skill-folder>
```

Otherwise, return the generated `.skill` path to the user.

## Final checklist

- Skill boundary is clear in frontmatter `description`.
- `SKILL.md` stays lean and points to references for branch-specific detail.
- Claude and Codex validation paths are explicit.
- Codex metadata is regenerated after `SKILL.md` changes.
- Evals, expectations, grading, benchmark, and viewer artifacts use the schemas
  in `references/schemas.md`.
- User feedback is incorporated before packaging.
