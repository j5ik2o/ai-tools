# Skill creator comparison

Read this reference when updating skill-forge's platform assumptions, reviewing
whether it still matches Claude Code or Codex behavior, or deciding whether a
workflow belongs in the lean Codex creator path or the heavier eval loop.

This file compares:

- Anthropic's `skill-creator`
- OpenAI's Codex `skill-creator`
- skill-forge's deliberate extensions

## Primary sources to re-check

Re-check these links before making platform claims:

| Source | Link | Why it matters |
| --- | --- | --- |
| Anthropic Claude Code skills docs | https://docs.anthropic.com/en/docs/claude-code/skills | Claude Code skill format, locations, frontmatter, packaging, and creation guidance |
| Anthropic `skill-creator` | https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md | Upstream source for the heavy draft/eval/viewer/improve loop |
| OpenAI Codex skills docs | https://developers.openai.com/codex/skills | Codex skill discovery, invocation, `agents/openai.yaml`, and plugin distribution guidance |
| OpenAI `skill-creator` | https://github.com/openai/skills/blob/main/skills/.system/skill-creator/SKILL.md | Lean Codex creator workflow, `init_skill.py`, metadata generation, and validation guidance |
| Open agent skills specification | https://agentskills.io/specification | Cross-platform skill directory and `SKILL.md` baseline vocabulary |

## Creation flow comparison

| Step | Claude Code / Anthropic creator | Codex / OpenAI creator | skill-forge stance |
| --- | --- | --- | --- |
| Intent capture | Ask what the skill should enable Claude to do, when it should trigger, output format, and whether test cases are useful. | Understand concrete examples, then plan reusable scripts, references, and assets. | Keep both: start from conversation history, then ask only for missing examples, trigger boundary, output, platform target, and eval need. |
| Initial scaffold | Draft `SKILL.md` directly. | Run `scripts/init_skill.py <skill-name> --path <output-directory>`, optionally with resources and examples. | For Codex-first skills, prefer the OpenAI scaffold path. For existing skills or Claude-only edits, edit in place. |
| Frontmatter | `name` and `description` are required; capture compatibility requirements when useful, then verify against current Claude docs before adding platform-specific fields. | `name` and `description` only. OpenAI's creator explicitly says not to include other YAML frontmatter fields. | Validate by platform: Claude mode accepts Claude-specific fields; Codex mode keeps `name` and `description` strict and moves UI metadata to `agents/openai.yaml`. |
| Trigger guidance | Put all "when to use" information in `description`; body loads after trigger. | Same principle: Codex reads frontmatter `name` and `description` to decide when to use a skill. | Treat `description` as the shared trigger boundary; include true-positive triggers and near-miss exclusions there. |
| Progressive disclosure | Keep `SKILL.md` under roughly 500 lines and move branch-specific detail to referenced resources. | Keep `SKILL.md` lean, challenge every token, move detailed material to `references/`, scripts, or assets. | Keep `SKILL.md` under 500 lines and require each reference to be linked from the body with read conditions. |
| Bundled resources | Use `scripts/`, `references/`, and `assets/` as needed. | Same directories, plus stronger guidance to avoid auxiliary docs like README or changelog inside skills. | Use resources only when they directly support skill execution. Do not add user-facing docs unless the skill itself needs them. |

## Evaluation flow comparison

| Area | Claude Code / Anthropic creator | Codex / OpenAI creator | skill-forge stance |
| --- | --- | --- | --- |
| Built-in emphasis | Heavy eval loop: run with-skill and baseline subagents, draft checks, grade, aggregate, show viewer, iterate. | Lean loop: validate, use the skill on real tasks, notice struggles, update and test again. | Keep the heavy loop for high-risk or objectively verifiable skills; allow lean validation and real-usage iteration for small Codex skills. |
| Baseline | New skill baseline is no skill; existing skill baseline is old snapshot. | No formal baseline in the creator workflow. | Use baselines for benchmarkable changes. Skip baselines for quick authoring or Claude.ai-style manual checks. |
| Formal checks | Anthropic source used `assertions`; skill-forge now writes canonical `expectations`. | OpenAI creator does not prescribe a benchmark schema. | Writers emit `expectations`; readers may accept legacy `assertions` only as an alias. |
| Viewer | Anthropic creator uses `eval-viewer/generate_review.py` for qualitative and quantitative review. | No equivalent viewer requirement in OpenAI creator. | Use the viewer when running the heavy loop. Do not force it onto simple Codex skill creation. |
| Trigger optimization | Anthropic creator includes a description optimization loop based on trigger eval queries. | OpenAI creator emphasizes clear frontmatter and real usage iteration rather than an optimization harness. | Offer optimization after the skill body is stable; run it through Claude Code or Codex CLI according to platform. |

## Distribution flow comparison

| Area | Claude Code / Anthropic creator | Codex / OpenAI creator | skill-forge stance |
| --- | --- | --- | --- |
| Local authoring location | Claude Code uses Claude skill locations documented by Anthropic. | Codex discovers repo skills from `.agents/skills` up to repo root, user skills from `$HOME/.agents/skills`, admin skills from `/etc/codex/skills`, and bundled system skills. | Use `.agents/skills` for Codex eval/discovery paths and Claude-compatible skill folders for Claude tests. Keep eval output workspaces separate from discovery paths. |
| Metadata | `SKILL.md` is the primary artifact. | `agents/openai.yaml` is optional but recommended for Codex UI metadata, invocation policy, and tool dependencies. | Generate and validate `agents/openai.yaml` for Codex-compatible skills; keep it out of Claude-only assumptions. |
| Packaging | Anthropic creator packages `.skill` files when presentation/download is available. | Codex docs recommend plugins as the installable distribution unit for reusable skills and app integrations. | Package `.skill` when the user needs Claude-style export; prefer plugins for reusable Codex distribution. |
| Validation | Anthropic creator relies on its bundled scripts and eval loop. | OpenAI creator runs `scripts/quick_validate.py`; Codex docs also emphasize trigger behavior and optional metadata. | Run `quick_validate.py` with `--platform claude` or `--platform codex`; use `--strict-openai-yaml` before publishing Codex metadata. |

## OpenAI skill-creator differences

OpenAI's official creator is intentionally leaner than skill-forge:

- It frames skills as concise onboarding guides for Codex, not as a benchmark
  harness.
- It recommends creating new skills through `scripts/init_skill.py`.
- It treats `agents/openai.yaml` as the place for UI metadata and invocation
  policy.
- It says `name` and `description` are the only `SKILL.md` frontmatter fields
  Codex uses for triggering.
- It avoids formal eval schemas, benchmark viewers, and blind comparison loops.
- It uses real task iteration as the default improvement path.

skill-forge intentionally adds:

- Claude Code and Codex platform branches in one workflow.
- Platform-aware validation modes.
- `agents/openai.yaml` generation with stale source-hash detection.
- Isolated eval workspaces for Claude and Codex CLI trigger tests.
- Benchmark aggregation, viewer generation, grader/analyzer/comparator agents,
  and trigger optimization loops.
- Canonical `expectations` schema with legacy `assertions` read compatibility.

## Anthropic-derived functionality

These skill-forge capabilities come directly from or are close adaptations of
Anthropic's `skill-creator`:

- Draft, test, review, improve, repeat as the main creative loop.
- With-skill versus baseline runs for each eval.
- Drafting objective checks while runs are in progress.
- Capturing timing and token data from subagent notifications.
- Grading outputs, aggregating benchmarks, and launching the review viewer.
- Blind comparison through comparator/analyzer agents.
- Description trigger optimization based on realistic should-trigger and
  should-not-trigger queries.
- Claude.ai and Cowork environment adaptations.

## skill-forge-specific extensions

These are not inherited directly from either official creator and should be
maintained as skill-forge design choices:

- Cross-platform Claude Code and Codex support in one skill.
- Codex CLI trigger evals using repo-local `.agents/skills`.
- Claude Code trigger evals using real temporary `skills/<name>/SKILL.md`
  layout instead of command shims.
- `uv`-managed Python environment setup.
- `quick_validate.py --platform auto|claude|codex`.
- `quick_validate.py --strict-openai-yaml`.
- `scripts/generate_openai_yaml.py` source-hash stamping.
- `references/trigger_eval_boundaries.md` for detector false positives,
  false negatives, `status`, and `attempted_runs`.
- `references/openai_yaml.md` for Codex metadata authoring constraints.

## Maintenance rules

- When Anthropic changes Claude Code skill frontmatter, locations, packaging, or
  creator workflow, update the Claude columns and Claude validation branch.
- When OpenAI changes Codex skill discovery, `agents/openai.yaml`, plugin
  distribution, or the built-in `skill-creator`, update the Codex columns and
  Codex validation branch.
- When skill-forge intentionally diverges from either official creator, record
  the divergence here before changing scripts or schemas.
- Do not copy large upstream text into this repository. Keep short summaries and
  links to primary sources.
