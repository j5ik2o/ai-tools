# Trigger eval reliability boundaries

Use this reference when running or changing description-trigger evals.

Trigger evals estimate whether a skill description causes the target agent to consult the skill. They are regression signals, not a formal proof of product behavior.

## Result semantics

Each query result has these fields:

- `attempted_runs`: Number of runs requested for the query.
- `runs`: Number of runs that returned a trigger/non-trigger result without raising.
- `triggers`: Number of successful runs where the detector saw a trigger signal.
- `timeouts`: Number of runs where the observation window elapsed without a
  decisive event. Present only when non-zero. See "Timeouts" below.
- `trigger_rate`: `triggers / runs`, or `0.0` when `runs` is `0`.
- `status`: Execution status.
  - `ok`: At least one successful run and no run errors.
  - `partial_error`: At least one successful run and at least one failed run.
  - `error`: No successful runs and at least one run error.
  - `not_run`: No successful runs and no run errors, usually because `runs_per_query` was `0`.

A successful non-trigger is `status: "ok"`, `runs > 0`, and `triggers == 0`.

An eval infrastructure failure is `status: "error"` or `status: "not_run"` with `runs == 0`. Treat it as failed even when `should_trigger` is `false`.

## Timeouts

A run that reaches the `--timeout` window without a trigger signal counts as a
non-trigger run: trigger decisions happen early in a session, so a long
trigger-free window is treated as evidence of non-trigger rather than as an
error. The run still increments `runs` and keeps `status: "ok"`.

This is a bias to watch: a hung or slow CLI makes every `should_trigger`
query fail and every `should_not_trigger` query pass. When `timeouts` is
non-zero on failing positive queries, or `timeouts == runs` across the board,
raise `--timeout` or investigate the CLI before trusting the scores.

## Same-name skill masking

While an eval batch runs, `run_eval` temporarily moves a project-installed
skill with the same name (`.claude/skills/<name>` for Claude,
`.agents/skills/<name>` for Codex) into a sibling `skill-forge-masked-<pid>`
directory and restores it when the batch finishes. Without this, the installed
skill stays visible next to the temporary skill under test: the agent may
consult the installed copy, which carries the original description (and, for
Codex, no marker), contaminating the measurement.

If the process is killed hard mid-batch, the restore may not run. Recover by
moving the skill directory back from `skill-forge-masked-<pid>` to its
original location.

## Claude Code detector

The Claude path runs `claude -p <query> --output-format stream-json --verbose --include-partial-messages` with an isolated temporary Claude home.

The detector treats the skill as triggered when either event shape appears:

- Assistant message content item:
  - `type == "assistant"`
  - `message.content[].type == "tool_use"`
  - `name == "Skill"` and `input.skill == <skill-name>`
- Stream event content block:
  - `type == "stream_event"`
  - `event.type == "content_block_start"` with tool `Skill` or `Read`
  - `event.type == "content_block_delta"` with `delta.type == "input_json_delta"`
  - accumulated JSON matches either `{"skill": "<skill-name>"}` for `Skill`, or a `Read` `file_path` targeting `skills/<skill-name>/SKILL.md`

### Claude false positives

- A `Read` of the skill's `SKILL.md` counts as triggered. This matches the old practical trigger signal, but it can count manual or diagnostic reads as trigger use.
- A future Claude event schema that reuses the same fields for a non-invocation preview could be counted as a trigger.

### Claude false negatives

- If Claude consults a skill through a new event type, renamed tool, or non-JSON-delta payload, the detector returns non-trigger.
- If the CLI emits partial JSON that never becomes valid before the block stops, the detector returns non-trigger.
- If Claude uses skill content indirectly without a `Skill` tool call or `Read` of `SKILL.md`, the detector cannot see it.

## Codex CLI detector

The Codex path creates a temporary repository skill under `.agents/skills/<skill-name>-skill-<id>/`, keeps the visible SKILL.md `name` as the original skill name, and injects a unique marker into the skill body:

```text
[SKILL_TRIGGERED:<id>]
```

It runs `codex exec --json -s read-only -C <project-root> <query>`.

Codex runs execute serially regardless of `--num-workers`: all runs share the
repository `.agents/skills/`, so concurrent temp skills carry the same visible
name and a run may read another run's marker copy. Measured on a real batch,
8-way parallelism dropped the positive trigger rate from ~50% to ~4%.

Codex detection also needs the full response: the marker only becomes visible
in a completed `agent_message`, so a triggering run typically takes 1-3
minutes. Use `--timeout 240` or higher; the 30s default is claude-oriented and
would count almost every Codex run as a timeout non-trigger.

The detector treats the skill as triggered only when:

- `type` is `item.completed` or `item.updated`
- `item.type == "agent_message"`
- `item.text` contains the exact marker

`turn.completed` without the marker is a successful non-trigger.

### Codex marker false positives

- If the model quotes or guesses the marker without actually using the skill, the detector counts a trigger.
- The marker is random per run to make accidental matches unlikely, but it is still visible in the temporary skill body after the skill is read.

### Codex marker false negatives

- If Codex uses the skill but does not follow the marker instruction, the detector returns non-trigger.
- If Codex emits the marker in a new JSON event shape, such as a renamed message event or nested content field, the detector returns non-trigger until the parser is updated.
- If the marker appears only in tool output or a transcript field that is not `item.text` for an `agent_message`, the detector returns non-trigger.

## CLI JSON event risk

Both platform paths depend on observed CLI JSON event shapes. A CLI update can change event names, nesting, or payload field names.

When updating parsers, add tests for both:

- The accepted event shape that must trigger.
- A nearby changed event shape that must not silently become a trigger.

Do not broaden parsing to arbitrary text fields unless the false-positive tradeoff is explicit and tested.
