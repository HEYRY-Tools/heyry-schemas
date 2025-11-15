#!/usr/bin/env python3
"""Validate all HEYRY Tools schema files against the schema metadata meta-schema."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft7Validator, RefResolver, ValidationError


REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMAS_ROOT = REPO_ROOT / "schemas"
META_SCHEMA_PATH = REPO_ROOT / "schemas" / "core" / "schema-metadata" / "v1" / "schema-metadata.schema.json"
HEYRY_ID_SCHEMA_PATH = REPO_ROOT / "schemas" / "core" / "heyry-id" / "v1" / "heyry-id.schema.json"
SEMVER_SCHEMA_PATH = REPO_ROOT / "schemas" / "core" / "semantic-version" / "v1" / "semantic-version.schema.json"
SCHEMA_BASE_URL = "https://schema.heyry.tools"
DRAFT_07_URI = "https://json-schema.org/draft-07/schema#"
HEYRY_ID_SCHEMA_ID = "https://schema.heyry.tools/core/heyry-id/v1/heyry-id.schema.json"
SEMVER_SCHEMA_ID = "https://schema.heyry.tools/core/semantic-version/v1/semantic-version.schema.json"


def load_json(path: Path) -> dict:
  with path.open("r", encoding="utf-8") as handle:
    return json.load(handle)


def main() -> int:
  meta_schema = load_json(META_SCHEMA_PATH)
  heyr_id_schema = load_json(HEYRY_ID_SCHEMA_PATH)
  semver_schema = load_json(SEMVER_SCHEMA_PATH)
  resolver = RefResolver.from_schema(
    meta_schema,
    store={
      HEYRY_ID_SCHEMA_ID: heyr_id_schema,
      SEMVER_SCHEMA_ID: semver_schema,
    },
  )
  validator = Draft7Validator(meta_schema, resolver=resolver)

  schema_files = sorted(SCHEMAS_ROOT.rglob("*.schema.json"))

  has_error = False
  for schema_path in schema_files:
    schema_data = load_json(schema_path)

    try:
      validator.validate(schema_data)
    except ValidationError as exc:
      has_error = True
      print(f"FAIL {schema_path.relative_to(REPO_ROOT)}: {exc.message}")
      continue

    if schema_data.get("$schema") != DRAFT_07_URI:
      has_error = True
      print(
        "FAIL",
        schema_path.relative_to(REPO_ROOT),
        f": $schema must be {DRAFT_07_URI}",
      )
      continue

    relative_parts = schema_path.relative_to(SCHEMAS_ROOT).parts
    if len(relative_parts) < 4:
      has_error = True
      print(
        "FAIL",
        schema_path.relative_to(REPO_ROOT),
        ": schema path must follow schemas/<domain>/<schema-name>/v<major>/<schema-name>.schema.json",
      )
      continue

    domain, schema_name, version_dir = relative_parts[:3]
    expected_filename = f"{schema_name}.schema.json"
    if relative_parts[3] != expected_filename:
      has_error = True
      print(
        "FAIL",
        schema_path.relative_to(REPO_ROOT),
        f": schema file must be named {expected_filename}",
      )
      continue

    expected_id = f"{SCHEMA_BASE_URL}/{domain}/{schema_name}/{version_dir}/{expected_filename}"
    actual_id = schema_data.get("$id")
    if actual_id != expected_id:
      has_error = True
      print(
        "FAIL",
        schema_path.relative_to(REPO_ROOT),
        f": $id must be {expected_id} (found {actual_id})",
      )
      continue

    print(f"PASS {schema_path.relative_to(REPO_ROOT)}")

  if has_error:
    return 1

  return 0


if __name__ == "__main__":
  sys.exit(main())
