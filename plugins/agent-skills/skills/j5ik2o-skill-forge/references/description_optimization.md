# Description optimization

Read this reference after creating or improving a skill when the user wants
better trigger accuracy, or when debugging why a skill triggers too often or not
often enough.

## Purpose

The `description` field in `SKILL.md` frontmatter is the primary trigger signal.
After the skill body is stable, offer to optimize the description.

## Generate trigger eval queries

Before drafting queries, read the target skill's `SKILL.md` and extract two
short lists:

- `helps with`: user intents and situations the skill is meant to handle.
- `should not help with`: adjacent requests or keywords that look similar but
  belong to a different skill or normal workflow.

Use those lists to anchor the eval set to the skill's real boundary.

Create 20 realistic eval queries as JSON:

```json
[
  {"query": "the user prompt", "should_trigger": true},
  {"query": "another prompt", "should_trigger": false}
]
```

Use a mix of long and short prompts, formal and casual phrasing, typos, file
paths, personal context, and near misses.

Good should-trigger cases cover different ways of asking for the same underlying
workflow. Good should-not-trigger cases are adjacent and tricky, not obviously
irrelevant.

Bad:

```text
"Format this data"
"Extract text from PDF"
"Create a chart"
```

Good:

```text
"ok so my boss just sent me this xlsx file (its in my downloads, called something like 'Q4 sales final FINAL v2.xlsx') and she wants me to add a column that shows the profit margin as a percentage. The revenue is in column C and costs are in column D i think"
```

## Review with the user

Use `assets/eval_review.html`:

1. Read the template.
2. Replace `__EVAL_DATA_PLACEHOLDER__` with the JSON array, without quotes.
3. Replace `__SKILL_NAME_PLACEHOLDER__` with the skill name.
4. Replace `__SKILL_DESCRIPTION_PLACEHOLDER__` with the current description.
5. Write to a temp file such as `/tmp/eval_review_<skill-name>.html`.
6. Open it with `open /tmp/eval_review_<skill-name>.html`.
7. After the user exports, read the newest `~/Downloads/eval_set*.json`.

This review matters because bad eval queries produce bad descriptions.

## Run the optimization loop

Tell the user the loop will take time and that you will check on it
periodically.

Before changing trigger eval parsing or interpreting surprising results, read
`references/trigger_eval_boundaries.md`. It documents Claude Code and Codex CLI
detector signals, false positives, false negatives, and the difference between a
successful non-trigger and zero successful runs.

Claude Code:

```bash
uv run python -m scripts.run_loop \
  --eval-set <path-to-trigger-eval.json> \
  --skill-path <path-to-skill> \
  --model <model-id-powering-this-session> \
  --max-iterations 5 \
  --verbose
```

Codex CLI:

```bash
uv run python -m scripts.run_loop \
  --eval-set <path-to-trigger-eval.json> \
  --skill-path <path-to-skill> \
  --model <model-id-powering-this-session> \
  --cli codex \
  --max-iterations 5 \
  --verbose
```

The `--cli` flag selects `claude` or `codex`. If omitted, the script auto-detects
from PATH. `SKILL_FORGE_EVAL_CLI` can also select the CLI.

Use the model ID from the current session so the eval matches the user's actual
experience. The same CLI selection is used for evaluation and description
improvement. No separate Anthropic API client setup is required for the
optimization loop.

While it runs, tail output and report iteration scores.

The loop splits evals into 60% train and 40% held-out test, evaluates each query
three times, proposes improvements, and selects `best_description` by held-out
test score to reduce overfitting.

If a query result has `status: "error"` or `status: "not_run"`, treat it as eval
infrastructure failure. A successful non-trigger has `status: "ok"`, `runs > 0`,
and `triggers == 0`.

## How skill triggering works

Claude Code skills appear in Claude's `available_skills` list with name and
description. Claude decides whether to consult a skill from that metadata.

Codex CLI discovers repository skills from `.agents/skills/` directories from
the current working directory up to the repository root. User skills live under
`$HOME/.agents/skills`, admin skills under `/etc/codex/skills`, and system
skills are bundled with Codex. Codex reads `SKILL.md` frontmatter `name` and
`description` to decide when to use a skill.

In both platforms, simple one-step tasks may not trigger a skill even if the
description matches because the agent can handle them directly. Trigger eval
queries should be substantive enough that the agent benefits from consulting the
skill.

## Apply the result

Take `best_description` from the JSON output and update the target skill's
`SKILL.md` frontmatter. Show the user before/after and report the scores.

If changing this skill-forge skill itself, regenerate `agents/openai.yaml` after
the `SKILL.md` edit.
