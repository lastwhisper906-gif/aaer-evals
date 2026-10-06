"""The analysis-grader's score, recomputed from its own items with the rubric's formula.

The grader writes a `score`; nothing should rest on a number the grader both chose
and computed. This recomputes it from `items` and `dealbreakers` (rubric.md): an item
scores 1 supported, 0.5 unclear, 0 unsupported or when a dealbreaker names its id; the run's
score is the mean weighted 3 for high severity, 2 medium, 1 low. `make eval` reports
the recomputed score, and says where the grader's own differs.
"""

from __future__ import annotations

VERDICT = {"supported": 1.0, "unclear": 0.5, "unsupported": 0.0}
WEIGHT = {"high": 3, "medium": 2, "low": 1}


def unreadable(grade: dict) -> list[str]:
    """Every item the rubric's formula cannot score: no id, verdict or severity it names."""
    out = []
    for index, item in enumerate(grade.get("items") or []):
        if not isinstance(item, dict):
            out.append(f"items[{index}]: not an object")
        elif not isinstance(item.get("id"), str) or not item["id"]:
            out.append(f"items[{index}]: no id")
        elif item.get("verdict") not in VERDICT:
            out.append(f"items[{index}]: verdict {item.get('verdict')!r}")
        elif item.get("severity") not in WEIGHT:
            out.append(f"items[{index}]: severity {item.get('severity')!r}")
    if not isinstance(grade.get("items"), list):
        out.append("no items list")
    return out


def recompute(grade: dict) -> float | None:
    """None when any item cannot be scored: a grade the formula cannot read is no grade."""
    if unreadable(grade):
        return None
    broken = {item.get("id") for item in grade.get("dealbreakers") or []
              if isinstance(item, dict) and item.get("id")}
    total = weight = 0.0
    for item in grade.get("items") or []:
        w = WEIGHT[item["severity"]]
        value = 0.0 if item.get("id") in broken else VERDICT[item["verdict"]]
        total += w * value
        weight += w
    return total / weight if weight else None


def check(grade: dict) -> dict:
    mine = recompute(grade)
    theirs = grade.get("score")
    agrees = (mine is None and theirs is None) or (
        isinstance(theirs, (int, float)) and mine is not None and abs(mine - theirs) < 1e-6)
    return {"score": mine, "grader_wrote": theirs, "agrees": agrees,
            "unreadable": unreadable(grade)}
