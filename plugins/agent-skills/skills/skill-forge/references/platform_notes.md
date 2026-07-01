# Platform notes

Read this reference when adapting skill-forge workflows to Claude.ai, Cowork, or
another environment where subagents, browsers, or local CLI behavior differ.

## Claude.ai

The core workflow is still draft, test, review, improve, and repeat. Because
Claude.ai does not have subagents, some mechanics change:

- Run test cases one at a time yourself after reading the skill's `SKILL.md`.
- Skip baseline runs.
- Skip quantitative benchmarking because baseline comparisons are not meaningful
  without independent runs.
- If a browser is unavailable, present results directly in the conversation.
- Save generated files to the filesystem and tell the user where they are.
- Ask for qualitative feedback inline.
- Description optimization requires `claude -p` or `codex exec`; use
  `--cli codex` when running with Codex. Skip it if no CLI is available.
- Blind comparison requires subagents, so skip it.
- `package_skill.py` still works anywhere with Python and a filesystem.

## Cowork

Cowork has subagents, so the main eval workflow works. If timeouts are severe,
running prompts in series is acceptable.

Cowork may not have a browser or display. Generate the eval viewer with
`--static <output_path>` so the user can open a standalone HTML file.

Always generate the eval viewer with `eval-viewer/generate_review.py` before
evaluating inputs yourself. Get the examples in front of the human quickly.

Feedback works differently in static mode: the viewer downloads `feedback.json`
when the user clicks "Submit All Reviews". Read that downloaded file before the
next iteration.

Packaging works normally. Description optimization should work because
`run_loop.py` and `run_eval.py` use CLI subprocesses rather than a browser.
