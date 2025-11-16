"""Invoke tasks for HEYRY schema registry."""

from __future__ import annotations

from invoke import task

VALIDATION_SCRIPTS = (
  "scripts/validate_schema_metadata.py",
  "scripts/validate_pretty_format.py",
  "scripts/validate_examples.py",
  "scripts/generate_index.py --check",
)


def _run_script(ctx, script: str) -> None:
  ctx.run(f"python {script}", pty=False)


@task(help={"scripts": "Comma-separated list of validation scripts to run instead of the defaults."})
def check(ctx, scripts: str | None = None) -> None:
  """Run all validation scripts (or a provided subset)."""
  targets = (
    tuple(script.strip() for script in scripts.split(",") if script.strip())
    if scripts
    else VALIDATION_SCRIPTS
  )

  if not targets:
    raise ValueError("No validation scripts specified.")

  for script in targets:
    _run_script(ctx, script)
