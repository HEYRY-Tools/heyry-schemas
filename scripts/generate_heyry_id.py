#!/usr/bin/env python3
"""Generate HEYRY IDs that conform to the heyry-id core schema."""

from __future__ import annotations

import argparse
import hashlib
import secrets
from typing import Iterable

CHARSET = "ABCDEFGHJKLMNPRSTUVWXYZ0123456789"
BODY_LENGTH = 12
GROUP_SIZE = 4


def _generate_body() -> str:
  return "".join(secrets.choice(CHARSET) for _ in range(BODY_LENGTH))


def _checksum(body: str) -> str:
  digest = hashlib.sha256(body.encode("ascii", "strict")).hexdigest().upper()
  return digest[:2]


def _format(body: str) -> str:
  grouped = "-".join(body[i : i + GROUP_SIZE] for i in range(0, BODY_LENGTH, GROUP_SIZE))
  checksum = _checksum(body)
  return f"{grouped}-{checksum}"


def generate_heyry_ids(count: int) -> Iterable[str]:
  for _ in range(count):
    yield _format(_generate_body())


def parse_args() -> argparse.Namespace:
  parser = argparse.ArgumentParser(description="Generate HEYRY IDs.")
  parser.add_argument(
    "-n",
    "--count",
    type=int,
    default=1,
    help="Number of HEYRY IDs to generate (default: 1).",
  )
  return parser.parse_args()


def main() -> int:
  args = parse_args()
  count = max(1, args.count)

  for value in generate_heyry_ids(count):
    print(value)

  return 0


if __name__ == "__main__":
  raise SystemExit(main())
