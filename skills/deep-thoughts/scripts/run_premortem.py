#!/usr/bin/env python3
"""Interactive premortem scaffolder.

Prompts the user through the premortem template in `references/premortem-template.md`
and writes the result to a Markdown file. Intended for human use, not for the agent
itself; ships with the skill as a companion tool.

Usage:
    uv run python skills/deep-thoughts/scripts/run_premortem.py \\
        --decision "Ship v2 of the onboarding flow" \\
        --horizon "12 months" \\
        --output premortem.md
"""

from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path
from textwrap import dedent

CATEGORIES = [
    "Technical",
    "User",
    "Organizational",
    "Market / environment",
    "Legal / ethical",
    "Resource",
    "Narrative",
    "Nobody cared",
]


def build_template(decision: str, horizon: str) -> str:
    today = dt.date.today().isoformat()
    categories = "\n".join(f"- **{c}** — " for c in CATEGORIES)
    return (
        dedent(
            f"""
        # Premortem — {decision}

        **Date:** {today}
        **Imagined horizon:** {horizon}
        **Status:** draft — fill in each section, then rank

        ## 1. The imagined failure
        It is now {horizon} from today. This decision has clearly failed. Write 2–3
        sentences describing what "failure" looks like.

        > <fill in>

        ## 2. Failure modes (aim for ≥ 10 before pruning)

        {categories}

        ## 3. Ranked failure modes

        | # | Failure mode | P(occurs) L/M/H | Impact L/M/H | Category |
        |---|---|---|---|---|
        | 1 |  |  |  |  |
        | 2 |  |  |  |  |
        | 3 |  |  |  |  |

        ## 4. Mitigations for top 3

        | # | Mitigation | Owner | Trigger (observable) | Cost (time/$) |
        |---|---|---|---|---|
        | 1 |  |  |  |  |
        | 2 |  |  |  |  |
        | 3 |  |  |  |  |

        ## 5. Top insight

        The failure mode that was not obvious before this exercise:

        > <fill in>

        ## 6. Decision

        - [ ] Go
        - [ ] No-go
        - [ ] Modify — describe the modification:

        > <fill in>
        """
        ).strip()
        + "\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--decision", required=True, help="One-sentence decision.")
    parser.add_argument(
        "--horizon", default="12 months", help="Imagined horizon (e.g., '6 months')."
    )
    parser.add_argument(
        "--output",
        default="premortem.md",
        help="Output Markdown file path.",
    )
    args = parser.parse_args()

    content = build_template(args.decision, args.horizon)
    out_path = Path(args.output)
    out_path.write_text(content, encoding="utf-8")
    print(f"Wrote premortem scaffold → {out_path.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
