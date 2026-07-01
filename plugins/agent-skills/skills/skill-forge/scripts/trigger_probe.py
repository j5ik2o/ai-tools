"""Shared subprocess JSON-event streaming for trigger evaluations.

Both CLI runners stream newline-delimited JSON events from a child process
and classify them into a trigger outcome. This module owns that loop so the
buffering, timeout, and process-cleanup behavior stays identical across CLIs.
"""

import json
import os
import select
import time

# Trigger probe outcomes.
TRIGGERED = "triggered"  # the detector saw the skill being consulted
COMPLETED = "completed"  # the run finished without a trigger signal
TIMEOUT = "timeout"  # the observation window elapsed without a decisive event


def _classify_line(line: str, classify) -> str | None:
    line = line.strip()
    if not line:
        return None
    try:
        event = json.loads(line)
    except json.JSONDecodeError:
        return None
    return classify(event)


def watch_process(process, timeout: int, classify, label: str, stderr_sink=None) -> str:
    """Stream JSON-line events from process stdout and classify them.

    `classify(event)` returns TRIGGERED, COMPLETED, or None to keep reading.
    Returns the outcome: TRIGGERED, COMPLETED (decisive end or process exit
    without a trigger), or TIMEOUT when the window elapses first.

    Raises RuntimeError when the process exits non-zero without triggering;
    `stderr_sink` (a file object the caller wired as the process stderr) is
    read for the error message.
    """
    outcome = None
    buffer = ""
    deadline = time.monotonic() + timeout

    try:
        while outcome is None:
            if time.monotonic() >= deadline:
                outcome = TIMEOUT
                break

            exited = process.poll() is not None
            if exited:
                remaining = process.stdout.read()
                if remaining:
                    buffer += remaining.decode("utf-8", errors="replace")
            else:
                ready, _, _ = select.select([process.stdout], [], [], 1.0)
                if not ready:
                    continue
                chunk = os.read(process.stdout.fileno(), 8192)
                if chunk:
                    buffer += chunk.decode("utf-8", errors="replace")
                else:
                    exited = True

            while outcome is None and "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                outcome = _classify_line(line, classify)

            if outcome is None and exited:
                # Classify a trailing line without a newline before concluding.
                outcome = _classify_line(buffer, classify) or COMPLETED
    finally:
        killed = False
        if process.poll() is None:
            process.kill()
            process.wait()
            killed = True
        if outcome != TRIGGERED and not killed and process.returncode:
            stderr_text = ""
            if stderr_sink is not None:
                try:
                    stderr_sink.seek(0)
                    stderr_text = stderr_sink.read().decode("utf-8", errors="replace")
                except (OSError, ValueError):
                    stderr_text = ""
            raise RuntimeError(
                f"{label} exited with code {process.returncode}: {stderr_text[:500]}"
            )

    return outcome
