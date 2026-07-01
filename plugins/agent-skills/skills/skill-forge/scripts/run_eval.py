#!/usr/bin/env python3
"""Run trigger evaluation for a skill description."""

import argparse
import json
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

from scripts.run_eval_claude import run_single_query_claude
from scripts.run_eval_codex import run_single_query_codex
from scripts.trigger_probe import TIMEOUT, TRIGGERED
from scripts.utils import (
    CLI_CLAUDE,
    CLI_CODEX,
    detect_cli,
    find_project_root,
    mask_installed_skill,
    parse_skill_md,
)


def run_single_query(
    query: str,
    skill_name: str,
    skill_description: str,
    timeout: int,
    project_root: str,
    model: str | None = None,
    cli_type: str = CLI_CLAUDE,
    cli_command: str | None = None,
    source_skill_dir: str | None = None,
) -> str:
    """Run a single query and return the trigger outcome.

    Dispatches to the appropriate CLI-specific implementation and returns
    TRIGGERED, COMPLETED, or TIMEOUT.
    """
    if cli_type == CLI_CODEX:
        return run_single_query_codex(
            query, skill_name, skill_description, timeout, project_root, model,
            cli_command,
        )
    return run_single_query_claude(
        query, skill_name, skill_description, timeout, project_root, model,
        cli_command, source_skill_dir=source_skill_dir,
    )


def run_eval(
    eval_set: list[dict],
    skill_name: str,
    description: str,
    num_workers: int,
    timeout: int,
    project_root: Path,
    runs_per_query: int = 1,
    trigger_threshold: float = 0.5,
    model: str | None = None,
    cli_type: str = CLI_CLAUDE,
    cli_command: str | None = None,
) -> dict:
    """Run the full eval set and return results.

    Results are keyed by eval-set position and returned in input order, so
    duplicate query texts stay independent.
    """
    run_outcomes: list[list[str]] = [[] for _ in eval_set]
    run_errors: list[list[str]] = [[] for _ in eval_set]

    with mask_installed_skill(cli_type, skill_name, project_root) as masked_skill_dir:
        source_skill_dir = str(masked_skill_dir) if masked_skill_dir else None
        with ProcessPoolExecutor(max_workers=num_workers) as executor:
            future_to_index = {}
            for index, item in enumerate(eval_set):
                for _ in range(runs_per_query):
                    future = executor.submit(
                        run_single_query,
                        item["query"],
                        skill_name,
                        description,
                        timeout,
                        str(project_root),
                        model,
                        cli_type,
                        cli_command,
                        source_skill_dir,
                    )
                    future_to_index[future] = index

            for future in as_completed(future_to_index):
                index = future_to_index[future]
                try:
                    run_outcomes[index].append(future.result())
                except Exception as e:
                    print(f"Error: query failed: {e}", file=sys.stderr)
                    run_errors[index].append(str(e))

    total_errors = sum(len(errs) for errs in run_errors)
    if total_errors > 0:
        print(
            f"Warning: {total_errors} query run(s) failed with errors. "
            f"Results may be unreliable.",
            file=sys.stderr,
        )

    total_timeouts = sum(outcomes.count(TIMEOUT) for outcomes in run_outcomes)
    if total_timeouts > 0:
        print(
            f"Warning: {total_timeouts} run(s) hit the {timeout}s timeout before "
            f"a decisive event and count as non-triggers. Raise --timeout if "
            f"should-trigger queries are affected.",
            file=sys.stderr,
        )

    results = []
    for item, outcomes, errors in zip(eval_set, run_outcomes, run_errors):
        query = item["query"]
        effective_runs = len(outcomes)
        triggers = outcomes.count(TRIGGERED)
        timeouts = outcomes.count(TIMEOUT)
        if effective_runs > 0:
            trigger_rate = triggers / effective_runs
        else:
            trigger_rate = 0.0
        should_trigger = item["should_trigger"]
        if should_trigger:
            did_pass = trigger_rate >= trigger_threshold
        else:
            did_pass = trigger_rate < trigger_threshold
        if effective_runs == 0:
            did_pass = False
        if effective_runs == 0 and errors:
            status = "error"
        elif effective_runs == 0:
            status = "not_run"
        elif errors:
            status = "partial_error"
        else:
            status = "ok"
        result_entry: dict = {
            "query": query,
            "should_trigger": should_trigger,
            "trigger_rate": trigger_rate,
            "triggers": triggers,
            "runs": effective_runs,
            "attempted_runs": runs_per_query,
            "status": status,
            "pass": did_pass,
        }
        if timeouts:
            result_entry["timeouts"] = timeouts
        if errors:
            result_entry["errors"] = errors
            result_entry["error_count"] = len(errors)
        results.append(result_entry)

    passed = sum(1 for r in results if r["pass"])
    total = len(results)

    return {
        "skill_name": skill_name,
        "description": description,
        "results": results,
        "summary": {
            "total": total,
            "passed": passed,
            "failed": total - passed,
            "errors": total_errors,
            "timeouts": total_timeouts,
        },
    }


def main():
    parser = argparse.ArgumentParser(description="Run trigger evaluation for a skill description")
    parser.add_argument("--eval-set", required=True, help="Path to eval set JSON file")
    parser.add_argument("--skill-path", required=True, help="Path to skill directory")
    parser.add_argument("--description", default=None, help="Override description to test")
    parser.add_argument("--num-workers", type=int, default=10, help="Number of parallel workers")
    parser.add_argument("--timeout", type=int, default=30, help="Timeout per query in seconds")
    parser.add_argument("--runs-per-query", type=int, default=3, help="Number of runs per query")
    parser.add_argument("--trigger-threshold", type=float, default=0.5, help="Trigger rate threshold")
    parser.add_argument("--model", default=None, help="Model to use (default: CLI's configured model)")
    parser.add_argument("--cli", default=None, choices=["claude", "codex"], help="CLI to use (default: auto-detect)")
    parser.add_argument("--cli-command", default=None, help="Path to CLI binary (e.g. /usr/local/bin/claude)")
    parser.add_argument("--verbose", action="store_true", help="Print progress to stderr")
    args = parser.parse_args()

    cli_type = detect_cli(args.cli)

    eval_set = json.loads(Path(args.eval_set).read_text())
    skill_path = Path(args.skill_path)

    if not (skill_path / "SKILL.md").exists():
        print(f"Error: No SKILL.md found at {skill_path}", file=sys.stderr)
        sys.exit(1)

    name, original_description, content = parse_skill_md(skill_path)
    description = args.description or original_description
    project_root = find_project_root(cli_type)

    if args.verbose:
        print(f"CLI: {cli_type}", file=sys.stderr)
        print(f"Evaluating: {description}", file=sys.stderr)

    output = run_eval(
        eval_set=eval_set,
        skill_name=name,
        description=description,
        num_workers=args.num_workers,
        timeout=args.timeout,
        project_root=project_root,
        runs_per_query=args.runs_per_query,
        trigger_threshold=args.trigger_threshold,
        model=args.model,
        cli_type=cli_type,
        cli_command=args.cli_command,
    )

    if args.verbose:
        summary = output["summary"]
        print(f"Results: {summary['passed']}/{summary['total']} passed", file=sys.stderr)
        for r in output["results"]:
            status = "PASS" if r["pass"] else "FAIL"
            rate_str = f"{r['triggers']}/{r['runs']}"
            print(f"  [{status}] rate={rate_str} expected={r['should_trigger']}: {r['query'][:70]}", file=sys.stderr)

    print(json.dumps(output, indent=2))
    if output["summary"]["total"] > 0 and all(result["runs"] == 0 for result in output["results"]):
        sys.exit(1)


if __name__ == "__main__":
    main()
