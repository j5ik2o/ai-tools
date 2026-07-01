# Eval workflow

Read this reference when creating or running skill evals, comparing a new skill
against a baseline, grading outputs, launching the review viewer, or iterating on
feedback.

## Overview

The eval loop is one continuous sequence:

1. Create an isolated workspace.
2. Spawn each eval with the skill and with the appropriate baseline in the same
   turn.
3. Draft expectations while runs are in progress.
4. Capture timing data as run notifications arrive.
5. Grade, aggregate, analyze, and launch the viewer.
6. Read user feedback and iterate.

Do not use `/skill-test` or another testing skill for this workflow.

## Workspace

Create an isolated workspace before any eval runs:

```bash
WORKSPACE=$(mktemp -d)
echo "Workspace: $WORKSPACE"
ls "$WORKSPACE"
```

Always display the workspace path to the user. If persistence is needed, use a
fixed eval-output path such as `.claude/skills-workspaces/<skill-name>/` for
Claude Code or `.codex/skills-workspaces/<skill-name>/` for Codex CLI. These are
only output workspaces; Codex skill discovery uses `.agents/skills`, not
`.codex/skills`.

Organize outputs by iteration and eval:

```text
iteration-1/
  eval-0-name/
    with_skill/
    without_skill/    # for a new skill baseline
    old_skill/        # for an existing skill baseline
```

## Spawn eval runs

For each test case, spawn both the with-skill run and baseline run in the same
turn so they complete on roughly the same schedule.

Each run must use an isolated working directory under the workspace, not the
skill source directory.

With-skill run:

```text
Execute this task:
- Skill path: <path-to-skill>
- Task: <eval prompt>
- Input files: <eval files if any, or "none">
- Working directory: <workspace>/iteration-<N>/<eval-name>/with_skill/
- Save outputs to: <workspace>/iteration-<N>/<eval-name>/with_skill/outputs/
- Outputs to save: <what the user cares about>
```

Baseline choices:

- New skill: use no skill. Save outputs under `without_skill/`.
- Existing skill: snapshot the old version before editing, then use the snapshot
  as the baseline. Save outputs under `old_skill/`.

Write an `eval_metadata.json` for each eval directory:

```json
{
  "eval_id": 0,
  "eval_name": "descriptive-name-here",
  "prompt": "The user's task prompt",
  "expectations": []
}
```

## Draft expectations

While eval runs are in progress, draft quantitative expectations and explain
them to the user. If `evals/evals.json` already contains expectations, review
them and explain what they check.

Good expectations are objective and descriptive. Subjective skills are better
evaluated qualitatively; do not force weak metrics onto work that needs human
judgment.

Update `eval_metadata.json` and `evals/evals.json` once expectations are drafted.
Writers must emit `expectations`; old hand-written `assertions` may be accepted
only as a legacy alias by readers.

## Capture timing

When each subagent task completes, save the notification's `total_tokens` and
`duration_ms` immediately to `timing.json` in that run directory:

```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.3
}
```

This data is not persisted elsewhere.

## Grade and aggregate

Grade each run by reading `agents/grader.md` and evaluating each expectation
against the outputs. Save `grading.json` in each run directory. The expectations
array must use `text`, `passed`, and `evidence`.

For programmatically checkable expectations, write and run a script instead of
eyeballing the output.

Aggregate from the skill-forge directory:

```bash
uv run python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name <name>
```

This produces `benchmark.json` and `benchmark.md`. If writing benchmark JSON
manually, use `references/schemas.md`.

Put each with-skill version before its baseline counterpart.

## Persist benchmark history

Copy the benchmark back to the skill folder:

```bash
mkdir -p <skill-dir>/evals/benchmarks
cp <workspace>/iteration-<N>/benchmark.json \
  <skill-dir>/evals/benchmarks/$(date +%Y-%m-%d)-iteration-<N>.json
```

Create or update `<skill-dir>/evals/benchmarks/README.md` with:

```markdown
| Iteration | Date | Pass Rate (with skill) | Pass Rate (baseline) | Avg Tokens | Avg Duration |
|-----------|------|------------------------|----------------------|------------|--------------|
```

## Analyze benchmark results

Read `agents/analyzer.md` and look for patterns aggregate stats can hide:

- Expectations that always pass regardless of skill.
- Evals with high variance or flaky results.
- Token/time tradeoffs.
- Cases where the baseline beats the skill.

## Launch the review viewer

Use the bundled viewer, not custom HTML:

```bash
nohup uv run --project <skill-forge-path> python <skill-forge-path>/eval-viewer/generate_review.py \
  <workspace>/iteration-N \
  --skill-name "my-skill" \
  --benchmark <workspace>/iteration-N/benchmark.json \
  > /dev/null 2>&1 &
VIEWER_PID=$!
```

For iteration 2+, add:

```bash
--previous-workspace <workspace>/iteration-<N-1>
```

Headless environments should use:

```bash
--static <output_path>
```

Tell the user the viewer has two tabs: **Outputs** for qualitative review and
**Benchmark** for quantitative comparison.

## Read feedback

When the user is done, read `feedback.json`:

```json
{
  "reviews": [
    {"run_id": "eval-0-with_skill", "feedback": "the chart is missing axis labels", "timestamp": "..."}
  ],
  "status": "complete"
}
```

Empty feedback means the output looked fine. Focus improvements on cases with
specific complaints.

Kill the viewer server when finished:

```bash
kill $VIEWER_PID 2>/dev/null
```

## Improve and iterate

After feedback:

1. Apply improvements to the skill.
2. Rerun all test cases into `iteration-<N+1>/`, including baselines.
3. Launch the viewer with `--previous-workspace`.
4. Wait for user review.
5. Read feedback and repeat.

Stop when the user is happy, feedback is empty, or changes are no longer making
meaningful progress.

When revising, generalize from feedback instead of overfitting to one eval. Read
transcripts, remove instructions that cause wasted work, and bundle helper
scripts when repeated work appears across evals.

## Blind comparison

For rigorous A/B comparison between two skill versions, read
`agents/comparator.md` and `agents/analyzer.md`. This requires subagents and is
optional for most workflows.
