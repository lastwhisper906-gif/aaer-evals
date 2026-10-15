"""The analysis gate, read to an analyst the moment it writes its file.

The owner's decision of 2026-10-15 (`docs/structure_changes.md`). Over the
fifteen runs of 2026-10-14, the gate dropped 414 items, 400 of them for a digit
in the analyst's own words, most of them a figure quoted inline from a report.
The gate was right to drop them, and the analyst never heard why. This hook is
handed to each analyst's session with `--settings` (a restricted session reads
no project settings), so when the session writes its one file, Python runs the
same gate on it (`run_analysis.check_analysis`) and hands every drop and its
reason back to the session, which may rewrite the file before it ends.

Nothing here judges: the gate is the judge, and it runs again on the file the
session leaves, exactly as before. What the session was told is text the model
saw, so each message is appended to a file outside the record and then put on
the agent's manifest entry under `gate_feedback` (`run_analysis.run_agent`).
After `MAX_FEEDBACK` messages in one call the hook goes quiet, so a session that
cannot fix an item is not held writing the same file.

Exit 2 is the code Claude Code hands back to the session; 0 says nothing.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from src import agent_inputs

# The agents the gate reads, and the kind it reads each one's file as.
GATED = {"accounting-analyst": "accounting", "financial-analyst": "financial",
         "valuation-analyst": "assumptions", "valuation-analyst-second-pass": "valuation"}
MAX_FEEDBACK = 3
HAND_BACK = 2
HEADER = ("Python ran the analysis gate on the file you just wrote. It would drop "
          "the items below, each with its reason. Rewrite each one so it stands, "
          "or leave it and it is dropped and counted. A figure the filing prints "
          "belongs in the item's `quote` field, never in your sentences.")


def message(checked: dict) -> str:
    """What the session is told: every drop, where it is and why."""
    lines = [HEADER]
    for row in checked.get("dropped_items") or []:
        lines.append(f"- {row.get('where')}: {row.get('reason')}")
    return "\n".join(lines)


def told(feedback: Path) -> int:
    """How many messages this call has already been handed."""
    try:
        return sum(1 for line in feedback.read_text(encoding="utf-8").splitlines() if line)
    except OSError:
        return 0


def respond(event: dict, *, run: Path, agent: str, feedback: Path) -> tuple[int, str]:
    """The exit code and the text for one write the session made."""
    written = Path(str((event.get("tool_input") or {}).get("file_path") or "")).name
    if agent not in GATED or written != agent_inputs.AGENTS[agent].writes:
        return 0, ""
    if told(feedback) >= MAX_FEEDBACK:
        return 0, ""
    from src import analysis_check, run_analysis   # lazy: run_analysis builds this hook's command
    try:
        checked = run_analysis.check_analysis(run, agent, GATED[agent])
    except (ValueError, OSError, analysis_check.AnalysisInputError) as exc:
        # json.JSONDecodeError is a ValueError
        text = f"The gate cannot read the file you just wrote, so nothing in it can stand: {exc}"
        dropped = None
    else:
        if not checked.get("dropped_count"):
            return 0, ""
        text, dropped = message(checked), checked["dropped_count"]
    with feedback.open("a", encoding="utf-8") as out:
        out.write(json.dumps({"dropped_count": dropped, "text": text},
                             ensure_ascii=False) + "\n")
    return HAND_BACK, text


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="the analysis gate, at write time")
    parser.add_argument("--run", required=True)
    parser.add_argument("--agent", required=True)
    parser.add_argument("--feedback", required=True)
    args = parser.parse_args(argv)
    try:
        event = json.load(sys.stdin)
    except ValueError:
        return 0
    code, text = respond(event, run=Path(args.run), agent=args.agent,
                         feedback=Path(args.feedback))
    if text:
        print(text, file=sys.stderr)
    return code


if __name__ == "__main__":
    sys.exit(main())
