#!/usr/bin/env python3
"""Generate index.json and index.html for the HEYRY Tools schema registry."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from textwrap import dedent

REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMAS_ROOT = REPO_ROOT / "schemas"
INDEX_JSON_PATH = REPO_ROOT / "index.json"
INDEX_HTML_PATH = REPO_ROOT / "index.html"
INDEX_SCHEMA_ID = "https://schema.heyry.tools/registry/index/v1/index.schema.json"


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


def build_index_json(entries: list[dict[str, str]]) -> str:
  payload = {"$schema": INDEX_SCHEMA_ID, "schemas": entries}
  return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"


def build_index_html() -> str:
  return dedent(
    """
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>HEYRY Tools Schema Registry</title>
        <style>
          :root {
            color-scheme: light dark;
            font-family: "Inter", "Segoe UI", system-ui, -apple-system, BlinkMacSystemFont, "Helvetica Neue", sans-serif;
            --page-bg: #0f1115;
            --page-fg: #f5f7fb;
            --card-bg: #181b21;
            --border: #2a2f3a;
            --accent: #63b3ed;
            --muted: #8b93a7;
            --draft: #f6ad55;
            --approved: #68d391;
          }

          @media (prefers-color-scheme: light) {
            :root {
              --page-bg: #f6f8fb;
              --page-fg: #0e1729;
              --card-bg: #ffffff;
              --border: #dce1ec;
              --accent: #2563eb;
              --muted: #5f6b87;
              --draft: #dd6b20;
              --approved: #2f855a;
            }
          }

          * {
            box-sizing: border-box;
          }

          body {
            margin: 0;
            min-height: 100vh;
            background: var(--page-bg);
            color: var(--page-fg);
          }

          header {
            padding: 3rem 1.5rem 1rem;
            text-align: center;
          }

          header h1 {
            margin: 0 0 0.5rem;
            font-size: clamp(2rem, 4vw, 3rem);
          }

          header p {
            margin: 0 auto 1rem;
            max-width: 48rem;
            color: var(--muted);
            line-height: 1.6;
          }

          header a.cta {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            background: var(--accent);
            color: #fff;
            padding: 0.65rem 1.2rem;
            border-radius: 999px;
            text-decoration: none;
            font-weight: 600;
          }

          main {
            padding: 1rem 1.5rem 3rem;
            max-width: 1200px;
            margin: 0 auto;
          }

          .panel {
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 1.25rem;
            padding: 1.5rem;
            box-shadow: 0 25px 50px rgba(15, 17, 21, 0.35);
          }

          .panel h2 {
            margin: 0;
          }

          .panel p.meta {
            color: var(--muted);
            margin-top: 0.35rem;
          }

          .status-legend {
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
            margin-top: 1rem;
            color: var(--muted);
            font-size: 0.9rem;
          }

          .status-pill {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            padding: 0.2rem 0.75rem;
            border-radius: 999px;
            border: 1px solid var(--border);
          }

          .status-dot {
            width: 0.5rem;
            height: 0.5rem;
            border-radius: 50%;
          }

          .status-dot.draft {
            background: var(--draft);
          }

          .status-dot.approved {
            background: var(--approved);
          }

          .table-wrapper {
            overflow-x: auto;
            margin-top: 1.5rem;
            border-radius: 1rem;
            border: 1px solid var(--border);
          }

          table {
            width: 100%;
            border-collapse: collapse;
            min-width: 640px;
          }

          thead {
            background: rgba(99, 179, 237, 0.08);
          }

          th,
          td {
            padding: 0.85rem 1rem;
            text-align: left;
          }

          th {
            text-transform: uppercase;
            font-size: 0.75rem;
            letter-spacing: 0.08em;
            color: var(--muted);
          }

          tbody tr:nth-child(even) {
            background: rgba(255, 255, 255, 0.02);
          }

          tbody tr:hover {
            background: rgba(99, 179, 237, 0.08);
          }

          td a {
            color: var(--accent);
            font-weight: 600;
            text-decoration: none;
          }

          td .status {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            padding: 0.2rem 0.65rem;
            border-radius: 999px;
            font-size: 0.85rem;
            font-weight: 600;
            background: rgba(255, 255, 255, 0.08);
          }

          td .status.draft {
            color: var(--draft);
          }

          td .status.approved {
            color: var(--approved);
          }

          .state-message {
            margin-top: 1.5rem;
            padding: 1rem;
            border-radius: 0.75rem;
            border: 1px dashed var(--border);
            color: var(--muted);
          }

          .state-message.error {
            border-color: #f56565;
            color: #fed7d7;
            background: rgba(245, 101, 101, 0.15);
          }

          .hidden {
            display: none;
          }
        </style>
      </head>
      <body>
        <header>
          <h1>HEYRY Tools Schema Registry</h1>
          <p>Browse every published HEYRY JSON Schema, track ownership domains, and review approval status directly from the canonical registry index.</p>
          <a class="cta" href="index.json" rel="noopener">Open index.json</a>
        </header>
        <main>
          <section class="panel">
            <h2>Schema Catalog</h2>
            <p class="meta">Data served from the generated <code>index.json</code> file.</p>
            <div class="status-legend">
              <span class="status-pill"><span class="status-dot approved"></span>Approved</span>
              <span class="status-pill"><span class="status-dot draft"></span>Draft</span>
            </div>
            <div id="loading" class="state-message">Loading schema catalog…</div>
            <div id="error" class="state-message error hidden">Unable to load <code>index.json</code>. Confirm the file exists and is valid.</div>
            <div class="table-wrapper hidden" id="table-wrapper">
              <table aria-describedby="table-caption">
                <caption id="table-caption" class="hidden">HEYRY Tools schema catalog</caption>
                <thead>
                  <tr>
                    <th scope="col">Domain</th>
                    <th scope="col">Schema</th>
                    <th scope="col">Version</th>
                    <th scope="col">Status</th>
                    <th scope="col">Description</th>
                  </tr>
                </thead>
                <tbody id="schema-rows"></tbody>
              </table>
            </div>
          </section>
        </main>
        <script>
          const loading = document.getElementById("loading");
          const errorBox = document.getElementById("error");
          const tableWrapper = document.getElementById("table-wrapper");
          const tableBody = document.getElementById("schema-rows");

          function renderStatus(status) {
            const span = document.createElement("span");
            span.className = `status ${status}`;
            span.textContent = status.replace(/\\b\\w/g, (letter) => letter.toUpperCase());
            return span;
          }

          function renderRow(entry) {
            const row = document.createElement("tr");
            const domain = document.createElement("td");
            domain.textContent = entry.domain;

            const name = document.createElement("td");
            const link = document.createElement("a");
            link.href = entry.id;
            link.textContent = entry.name;
            link.target = "_blank";
            link.rel = "noopener";
            name.appendChild(link);
            const path = document.createElement("div");
            path.textContent = entry.path;
            path.style.fontSize = "0.8rem";
            path.style.color = "var(--muted)";
            name.appendChild(path);

            const version = document.createElement("td");
            version.textContent = entry.version;

            const status = document.createElement("td");
            status.appendChild(renderStatus(entry.status));

            const description = document.createElement("td");
            description.textContent = entry.description;

            row.append(domain, name, version, status, description);
            return row;
          }

          async function loadRegistry() {
            try {
              const response = await fetch("index.json", { cache: "no-store" });
              if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
              }
              const payload = await response.json();
              const schemas = payload.schemas || [];
              if (!schemas.length) {
                const empty = document.createElement("div");
                empty.className = "state-message";
                empty.textContent = "The registry is empty.";
                loading.replaceWith(empty);
                return;
              }

              schemas.forEach((schema) => {
                tableBody.appendChild(renderRow(schema));
              });
              tableWrapper.classList.remove("hidden");
              loading.classList.add("hidden");
            } catch (err) {
              console.error("Failed to load index.json", err);
              loading.classList.add("hidden");
              errorBox.classList.remove("hidden");
            }
          }

          loadRegistry();
        </script>
      </body>
    </html>
    """
  )


def write_or_check(path: Path, content: str, check_only: bool) -> None:
  if check_only:
    if not path.exists():
      raise SystemExit(f"{path} is missing. Run python scripts/generate_index.py to create it.")

    existing = path.read_text(encoding="utf-8")
    if existing != content:
      raise SystemExit(
        f"{path} is out of date. Run python scripts/generate_index.py to regenerate the registry index."
      )
    return

  path.write_text(content, encoding="utf-8")


def main() -> int:
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument(
    "--check",
    action="store_true",
    help="Validate that index.json and index.html match the generated output without writing changes.",
  )
  args = parser.parse_args()

  entries = load_schema_metadata()
  index_json = build_index_json(entries)
  index_html = build_index_html()

  write_or_check(INDEX_JSON_PATH, index_json, args.check)
  write_or_check(INDEX_HTML_PATH, index_html, args.check)
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
