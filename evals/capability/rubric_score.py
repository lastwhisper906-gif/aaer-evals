"""The analysis-grader's score, recomputed from its own items with the rubric's formula.

The grader writes a `score`; nothing should rest on a number the grader both chose
and computed. This recomputes it from `items` and `dealbreakers` (rubric.md): an item
scores 1 supported, 0.5 unclear, 0 unsupported or under a dealbreaker; the run's
score is the mean weighted 3 for high severity, 2 medium, 1 low. `make eval` reports
the recomputed score, and says where the grader's own differs.
"""

from __future__ import annotations

VERDICT = {"supported": 1.0, "unclear": 0.5, "unsupported": 0.0}
WEIGHT = {"high": 3, "medium": 2, "low": 1}


def recompute(grade: dict) -> float | None:
    broken = set()
    for item in grade.get("dealbreakers") or []:
        where = str(item.get("where") or "")
        broken.add(item.get("id") or where)
    total = weight = 0.0
    for item in grade.get("items") or []:
        if not isinstance(item, dict) or item.get("verdict") not in VERDICT \
                or item.get("severity") not in WEIGHT:
            continue
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
    return {"score": mine, "grader_wrote": theirs, "agrees": agrees}
