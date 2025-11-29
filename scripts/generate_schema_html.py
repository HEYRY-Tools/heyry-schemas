#!/usr/bin/env python3
"""Generate HTML renderings of every HEYRY JSON Schema."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from textwrap import dedent

REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMAS_ROOT = REPO_ROOT / "schemas"

HTML_TEMPLATE = dedent(
  """
  <!DOCTYPE html>
  <html lang=\"en\">
    <head>
      <meta charset=\"utf-8\" />
      <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
      <title>{title}</title>
      <style>
        :root {{
          color-scheme: light dark;
          font-family: "Inter", "Segoe UI", system-ui, -apple-system, BlinkMacSystemFont, "Helvetica Neue", sans-serif;
          --page-bg: #0f1115;
          --page-fg: #f5f7fb;
          --card-bg: #181b21;
          --border: #2a2f3a;
          --muted: #8b93a7;
        }}

        @media (prefers-color-scheme: light) {{
          :root {{
            --page-bg: #f6f8fb;
            --page-fg: #0e1729;
            --card-bg: #ffffff;
            --border: #dce1ec;
            --muted: #5f6b87;
          }}
        }}

        * {{
          box-sizing: border-box;
        }}

        body {{
          margin: 0;
          min-height: 100vh;
          background: var(--page-bg);
          color: var(--page-fg);
          display: flex;
          justify-content: center;
          align-items: flex-start;
          padding: 2.5rem 1.5rem 3rem;
        }}

        main {{
          width: min(1100px, 100%);
          background: var(--card-bg);
          border: 1px solid var(--border);
          border-radius: 1.25rem;
          padding: 1.5rem;
          box-shadow: 0 25px 50px rgba(15, 17, 21, 0.35);
        }}

        h1 {{
          margin: 0 0 0.35rem;
          font-size: clamp(1.5rem, 4vw, 2.25rem);
        }}

        p.meta {{
          margin: 0 0 1rem;
          color: var(--muted);
        }}

        pre {{
          margin: 0;
          padding: 1.25rem;
          background: rgba(255, 255, 255, 0.06);
          border: 1px solid var(--border);
          border-radius: 0.85rem;
          overflow-x: auto;
          white-space: pre-wrap;
        }}
      </style>
    </head>
    <body>
      <main>
        <h1>{title}</h1>
        <p class=\"meta\">Source: {source}</p>
        <pre>{content}</pre>
      </main>
    </body>
  </html>
  """
)


def build_html(schema_path: Path, schema: dict[str, object], formatted_json: str) -> str:
  title = str(schema.get("title", schema_path.stem))
  escaped_json = html.escape(formatted_json)
  source = schema_path.as_posix()
  return HTML_TEMPLATE.format(title=title, content=escaped_json, source=source)


def generate_html(schema_path: Path, output_root: Path) -> None:
  with schema_path.open("r", encoding="utf-8") as handle:
    schema = json.load(handle)

  formatted_json = json.dumps(schema, ensure_ascii=False, indent=2) + "\n"
  html_content = build_html(schema_path, schema, formatted_json)

  relative = schema_path.relative_to(SCHEMAS_ROOT)
  output_path = output_root / relative
  output_path = output_path.with_suffix(".schema.html")
  output_path.parent.mkdir(parents=True, exist_ok=True)
  output_path.write_text(html_content, encoding="utf-8")


def generate_all(output_root: Path) -> int:
  for schema_path in sorted(SCHEMAS_ROOT.rglob("*.schema.json")):
    generate_html(schema_path, output_root)
  return 0


def parse_args() -> argparse.Namespace:
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument(
    "--output-dir",
    type=Path,
    default=REPO_ROOT / "site",
    help="Directory where HTML renderings should be written (mirrors the schemas directory).",
  )
  return parser.parse_args()


def main() -> int:
  args = parse_args()
  output_root = args.output_dir / "schemas"
  output_root.mkdir(parents=True, exist_ok=True)
  return generate_all(output_root)


if __name__ == "__main__":
  raise SystemExit(main())
