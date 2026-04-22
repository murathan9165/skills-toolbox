#!/usr/bin/env python3
"""Developer CLI for validating skills locally.

Runs the same pytest suite that CI runs, but with a friendlier summary. Handy
when iterating on a new skill's description.

Usage:
    uv run python scripts/validate_skills.py
    uv run python scripts/validate_skills.py --skill deep-thoughts
"""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--skill",
        help="If given, filters tests to ids containing this skill name.",
    )
    args = parser.parse_args()

    cmd = ["uv", "run", "pytest", "tests/", "-v", "--tb=short"]
    if args.skill:
        cmd += ["-k", args.skill]

    result = subprocess.run(cmd, cwd=REPO_ROOT, check=False)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
