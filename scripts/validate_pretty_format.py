#!/usr/bin/env python3
"""Validate that repository JSON files use canonical pretty formatting."""

from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
JSON_DIRECTORIES = ("schemas", "examples")
JSON_FILES = ("index.json",)


def iter_json_files() -> list[Path]:
    files: list[Path] = []
    for directory in JSON_DIRECTORIES:
        dir_path = ROOT / directory
        if dir_path.exists():
            files.extend(sorted(dir_path.rglob("*.json")))
    for filename in JSON_FILES:
        file_path = ROOT / filename
        if file_path.exists():
            files.append(file_path)
    return files


def validate_file(path: Path) -> tuple[bool, str | None]:
    current = path.read_text(encoding="utf-8")
    try:
        data = json.loads(current)
    except json.JSONDecodeError as exc:  # pragma: no cover - deterministic reporting only
        return False, f"{path.relative_to(ROOT)}: invalid JSON ({exc})"

    formatted = json.dumps(data, indent=2, ensure_ascii=False)
    formatted += "\n"
    if current != formatted:
        return False, f"{path.relative_to(ROOT)}: not pretty-formatted"
    return True, None


def main() -> int:
    files = iter_json_files()
    mismatches: list[str] = []
    for file_path in files:
        ok, message = validate_file(file_path)
        if not ok and message is not None:
            mismatches.append(message)

    if mismatches:
        for message in mismatches:
            print(message)
        print(f"{len(mismatches)} file(s) require pretty-formatting.")
        return 1

    print("All JSON files are properly formatted.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
