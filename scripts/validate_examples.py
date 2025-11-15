#!/usr/bin/env python3
"""Validate example JSON documents against their declared HEYRY Tools schemas."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft7Validator, RefResolver, ValidationError


REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMAS_ROOT = REPO_ROOT / "schemas"
EXAMPLES_ROOT = REPO_ROOT / "examples"


def load_json(path: Path):
  with path.open("r", encoding="utf-8") as handle:
    return json.load(handle)


def build_schema_store() -> dict[str, dict]:
  store: dict[str, dict] = {}
  for schema_path in SCHEMAS_ROOT.rglob("*.schema.json"):
    schema_data = load_json(schema_path)
    schema_id = schema_data.get("$id")
    if schema_id:
      store[schema_id] = schema_data
  return store


def find_schema_path(schema_uri: str) -> Path:
  if not schema_uri.startswith("https://schemas.heyry.tools/"):
    raise FileNotFoundError(f"Unsupported schema URI: {schema_uri}")
  relative = schema_uri.replace("https://schemas.heyry.tools/", "")
  return SCHEMAS_ROOT / relative


def main() -> int:
  schema_store = build_schema_store()
  example_files = sorted(EXAMPLES_ROOT.rglob("*.json"))

  has_error = False
  for example_path in example_files:
    example_data = load_json(example_path)
    schema_uri = example_data.get("$schema")
    if not schema_uri:
      has_error = True
      print(f"FAIL {example_path.relative_to(REPO_ROOT)}: missing $schema property")
      continue

    schema_path = find_schema_path(schema_uri)
    if not schema_path.exists():
      has_error = True
      print(f"FAIL {example_path.relative_to(REPO_ROOT)}: schema not found at {schema_path.relative_to(REPO_ROOT)}")
      continue

    schema_data = load_json(schema_path)
    resolver = RefResolver(base_uri=schema_uri, referrer=schema_data, store=schema_store)
    validator = Draft7Validator(schema_data, resolver=resolver)

    try:
      validator.validate(example_data)
    except ValidationError as exc:
      has_error = True
      print(f"FAIL {example_path.relative_to(REPO_ROOT)}: {exc.message}")
    else:
      print(f"PASS {example_path.relative_to(REPO_ROOT)}")

  if has_error:
    return 1

  return 0


if __name__ == "__main__":
  sys.exit(main())
