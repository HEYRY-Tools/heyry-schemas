#!/usr/bin/env python3
"""Validate all HEYRY Tools schema files against the schema metadata meta-schema."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft7Validator, ValidationError


REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMAS_ROOT = REPO_ROOT / "schemas"
META_SCHEMA_PATH = REPO_ROOT / "schemas" / "core" / "schema-metadata" / "v1" / "schema-metadata.schema.json"


def load_json(path: Path) -> dict:
  with path.open("r", encoding="utf-8") as handle:
    return json.load(handle)


def main() -> int:
  meta_schema = load_json(META_SCHEMA_PATH)
  validator = Draft7Validator(meta_schema)

  schema_files = sorted(SCHEMAS_ROOT.rglob("*.schema.json"))

  has_error = False
  for schema_path in schema_files:
    try:
      validator.validate(load_json(schema_path))
    except ValidationError as exc:
      has_error = True
      print(f"FAIL {schema_path.relative_to(REPO_ROOT)}: {exc.message}")
    else:
      print(f"PASS {schema_path.relative_to(REPO_ROOT)}")

  if has_error:
    return 1

  return 0


if __name__ == "__main__":
  sys.exit(main())
