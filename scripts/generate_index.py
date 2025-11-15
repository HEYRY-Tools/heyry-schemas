#!/usr/bin/env python3
"""Generate index.json and index.html for the HEYRY Tools schema registry."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMAS_ROOT = REPO_ROOT / "schemas"
INDEX_JSON_PATH = REPO_ROOT / "index.json"
INDEX_HTML_PATH = REPO_ROOT / "index.html"
INDEX_SCHEMA_ID = "https://schemas.heyry.tools/registry/index/v1/index.schema.json"


def load_schema_metadata() -> list[dict[str, str]]:
  entries: list[dict[str, str]] = []
  for schema_path in sorted(SCHEMAS_ROOT.rglob("*.schema.json")):
    with schema_path.open("r", encoding="utf-8") as handle:
      data = json.load(handle)

    entry = {
      "id": data["$id"],
      "name": data["title"],
      "domain": data["domain"],
      "version": data["schema_version"],
      "status": data["status"],
      "path": str(schema_path.relative_to(REPO_ROOT).as_posix()),
      "description": data["description"],
    }
    entries.append(entry)

  entries.sort(key=lambda item: item["id"])
  return entries


def write_index_json(entries: list[dict[str, str]]) -> None:
  payload = {"$schema": INDEX_SCHEMA_ID, "schemas": entries}
  with INDEX_JSON_PATH.open("w", encoding="utf-8") as handle:
    json.dump(payload, handle, indent=2)
    handle.write("\n")


def write_index_html() -> None:
  html = """<!DOCTYPE html>\n<html lang=\"en\">\n  <head>\n    <meta charset=\"utf-8\">\n    <title>HEYRY Tools Schemas</title>\n  </head>\n  <body>\n    <h1>HEYRY Tools Schemas</h1>\n    <p>This site hosts the public JSON schema registry for HEYRY Tools.</p>\n    <p><a href=\"index.json\">View the schema index</a></p>\n  </body>\n</html>\n"""
  with INDEX_HTML_PATH.open("w", encoding="utf-8") as handle:
    handle.write(html)


def main() -> int:
  entries = load_schema_metadata()
  write_index_json(entries)
  write_index_html()
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
