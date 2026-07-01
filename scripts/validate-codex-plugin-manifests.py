#!/usr/bin/env python3
"""Validate repo-local Codex plugin manifests.

This checks the manifest contract documented in the Codex plugin build guide:
each plugin has `.codex-plugin/plugin.json`, a `skills` path that resolves to
`skills/`, and the UI metadata Codex expects for plugin presentation.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


SEMVER_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:[-+].*)?$")
REQUIRED_INTERFACE_FIELDS = (
    "displayName",
    "shortDescription",
    "longDescription",
    "developerName",
    "category",
    "capabilities",
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Codex plugin manifests")
    parser.add_argument(
        "plugin_paths",
        nargs="*",
        type=Path,
        help="Plugin directories to validate. Defaults to plugins/* with .codex-plugin.",
    )
    args = parser.parse_args()

    plugin_paths = args.plugin_paths or discover_plugins(Path("plugins"))
    if not plugin_paths:
        print("No Codex plugin manifests found", file=sys.stderr)
        return 1

    failures: list[str] = []
    for plugin_path in plugin_paths:
        failures.extend(validate_plugin(plugin_path))

    if failures:
        print("Codex plugin manifest validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    for plugin_path in plugin_paths:
        print(f"OK: {plugin_path}")
    return 0


def discover_plugins(root: Path) -> list[Path]:
    if not root.is_dir():
        return []
    return sorted(
        path
        for path in root.iterdir()
        if path.is_dir() and (path / ".codex-plugin" / "plugin.json").is_file()
    )


def validate_plugin(plugin_path: Path) -> list[str]:
    manifest_path = plugin_path / ".codex-plugin" / "plugin.json"
    label = plugin_path.as_posix()
    failures: list[str] = []

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return [f"{label}: missing .codex-plugin/plugin.json"]
    except json.JSONDecodeError as exc:
        return [f"{label}: plugin.json is invalid JSON: {exc}"]

    if not isinstance(manifest, dict):
        return [f"{label}: plugin.json must be a JSON object"]

    for field in ("name", "version", "description", "skills"):
        require_non_empty_string(manifest, field, label, failures)

    name = manifest.get("name")
    if isinstance(name, str) and name != plugin_path.name:
        failures.append(f"{label}: name must match plugin directory name")

    version = manifest.get("version")
    if isinstance(version, str) and SEMVER_RE.fullmatch(version) is None:
        failures.append(f"{label}: version must be semver")

    skills_path = manifest.get("skills")
    if skills_path != "./skills/":
        failures.append(f"{label}: skills must be ./skills/")
    elif not (plugin_path / "skills").is_dir():
        failures.append(f"{label}: skills path points to missing directory")

    author = manifest.get("author")
    if not isinstance(author, dict):
        failures.append(f"{label}: author must be an object")
    else:
        require_non_empty_string(author, "name", f"{label}.author", failures)

    interface = manifest.get("interface")
    if not isinstance(interface, dict):
        failures.append(f"{label}: interface must be an object")
    else:
        validate_interface(interface, label, failures)

    return failures


def validate_interface(interface: dict[str, Any], label: str, failures: list[str]) -> None:
    for field in REQUIRED_INTERFACE_FIELDS:
        if field == "capabilities":
            capabilities = interface.get(field)
            if not isinstance(capabilities, list) or not capabilities or not all(
                isinstance(value, str) and value.strip() for value in capabilities
            ):
                failures.append(f"{label}: interface.capabilities must be a non-empty string list")
            continue
        require_non_empty_string(interface, field, f"{label}.interface", failures)

    default_prompt = interface.get("defaultPrompt")
    if not isinstance(default_prompt, list) or not default_prompt or not all(
        isinstance(value, str) and value.strip() for value in default_prompt
    ):
        failures.append(f"{label}: interface.defaultPrompt must be a non-empty string list")


def require_non_empty_string(
    payload: dict[str, Any],
    field: str,
    label: str,
    failures: list[str],
) -> None:
    value = payload.get(field)
    if not isinstance(value, str) or not value.strip():
        failures.append(f"{label}: {field} must be a non-empty string")


if __name__ == "__main__":
    raise SystemExit(main())
