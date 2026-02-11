#!/usr/bin/env python3
"""Validate example JSON documents against their declared HEYRY Tools schemas."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from jsonschema import Draft7Validator, ValidationError
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT7


REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMAS_ROOT = REPO_ROOT / "schemas"
EXAMPLES_ROOT = REPO_ROOT / "examples"
SCHEMA_BASE_URL = "https://schema.heyry.tools/"
EXAMPLE_VERSION_PATTERN = re.compile(r"^v\d+$")


def load_json(path: Path):
  with path.open("r", encoding="utf-8") as handle:
    return json.load(handle)


def validate_example_location(example_path: Path) -> str | None:
  relative_parts = example_path.relative_to(EXAMPLES_ROOT).parts
  if len(relative_parts) < 3:
    return "example path must follow examples/<domain>/<version>/<file>.json"

  version = relative_parts[1]
  if not EXAMPLE_VERSION_PATTERN.match(version):
    return "example path version directory must follow v<major>"

  return None


def build_schema_store() -> dict[str, dict]:
  store: dict[str, dict] = {}
  for schema_path in SCHEMAS_ROOT.rglob("*.schema.json"):
    schema_data = load_json(schema_path)
    schema_id = schema_data.get("$id")
    if schema_id:
      store[schema_id] = schema_data
  return store


def find_schema_path(schema_uri: str) -> Path:
  if not schema_uri.startswith(SCHEMA_BASE_URL):
    raise FileNotFoundError(f"Unsupported schema URI: {schema_uri}")
  relative = schema_uri.replace(SCHEMA_BASE_URL, "")
  return SCHEMAS_ROOT / relative


def main() -> int:
  schema_store = build_schema_store()
  registry = Registry().with_resources(
    [(schema_id, Resource.from_contents(schema, default_specification=DRAFT7)) for schema_id, schema in schema_store.items()]
  )
  example_files = sorted(EXAMPLES_ROOT.rglob("*.json"))

  has_error = False
  for example_path in example_files:
    location_error = validate_example_location(example_path)
    if location_error:
      has_error = True
      print(f"FAIL {example_path.relative_to(REPO_ROOT)}: {location_error}")
      continue

    try:
      example_data = load_json(example_path)
    except json.JSONDecodeError as exc:
      has_error = True
      print(f"FAIL {example_path.relative_to(REPO_ROOT)}: invalid JSON ({exc})")
      continue

    schema_uri = example_data.get("$schema")
    if not schema_uri:
      has_error = True
      print(f"FAIL {example_path.relative_to(REPO_ROOT)}: missing $schema property")
      continue

    try:
      schema_path = find_schema_path(schema_uri)
    except FileNotFoundError as exc:
      has_error = True
      print(f"FAIL {example_path.relative_to(REPO_ROOT)}: {exc}")
      continue

    if not schema_path.exists():
      has_error = True
      print(f"FAIL {example_path.relative_to(REPO_ROOT)}: schema not found at {schema_path.relative_to(REPO_ROOT)}")
      continue

    try:
      schema_data = load_json(schema_path)
    except json.JSONDecodeError as exc:
      has_error = True
      print(f"FAIL {example_path.relative_to(REPO_ROOT)}: invalid schema JSON ({exc})")
      continue

    validator = Draft7Validator(schema_data, registry=registry)

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
