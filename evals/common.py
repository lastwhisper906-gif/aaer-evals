"""What every grader shares: finding runs, reading their files, and one result shape."""

from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass, field
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RUNS = REPO / "runs"

PASS, FAIL, NOT_APPLICABLE = "pass", "fail", "not_applicable"


@dataclass
class Result:
    grader: str          # e.g. "mechanical.quotes_resolve"
    run: str             # "<ticker>/<run directory>", or "code" for a check on src/
    status: str          # pass, fail or not_applicable
    detail: str = ""
    failures: list = field(default_factory=list)

    def as_dict(self) -> dict:
        return {"grader": self.grader, "run": self.run, "status": self.status,
                "detail": self.detail, "failures": self.failures[:20]}


def find_runs(paths: list[Path] | None = None) -> list[Path]:
    """Every analysed run under the given paths. A run is `runs/<ticker>/<directory>/`
    holding both `input_manifest.json` and `calculator.json`; a bare extraction is
    not a run, and an agent's own input directory one level down is not either."""
    found = set()
    for root in paths or [RUNS]:
        root = Path(root)
        root = root if root.is_absolute() else REPO / root
        root = root.resolve()
        if (root / "input_manifest.json").is_file():
            candidates = [root]
        elif root == RUNS.resolve():
            candidates = [p.parent for p in root.glob("*/*/input_manifest.json")]
        else:                                   # a ticker directory
            candidates = [p.parent for p in root.glob("*/input_manifest.json")]
        found.update(run for run in candidates if (run / "calculator.json").is_file())
    return sorted(found)


def run_name(run: Path) -> str:
    return f"{run.parent.name}/{run.name}"


def load(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


# --- the whitespace fold ------------------------------------------------------------------
# Unicode's White_Space property, each read as one ordinary space, one for one: the
# owner's decision of 2026-09-23. Written out here rather than imported, so the grader
# does not move when the gate does.
WHITE_SPACE = ("\u0009\u000a\u000b\u000c\u000d \u0085     "
               "            "
               "　")
_FOLD = {ord(ch): " " for ch in WHITE_SPACE}


def fold(text: str) -> str:
    return text.translate(_FOLD)


# --- calculator paths ---------------------------------------------------------------------

PLACEHOLDER = re.compile(r"\{([a-z0-9_.-]+)(?:\|(pct))?\}")


def resolve(tree, path: str):
    """The node a dotted path names in a calculator file, or KeyError. A list is
    indexed by a number in the path; a cell is the dictionary itself."""
    node = tree
    for part in path.split("."):
        if isinstance(node, list):
            try:
                node = node[int(part)]
            except (ValueError, IndexError):
                raise KeyError(path) from None
        elif isinstance(node, dict) and part in node:
            node = node[part]
        else:
            raise KeyError(path)
    return node


def number_at(tree, path: str):
    """The number a path stands for: the node itself, or its `value`."""
    node = resolve(tree, path)
    if isinstance(node, dict):
        node = node.get("value")
    return node


def finite(value) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def walk_strings(node, where: str = ""):
    """Every string in a JSON tree, with where it sits."""
    if isinstance(node, str):
        yield where, node
    elif isinstance(node, dict):
        for key, value in node.items():
            yield from walk_strings(value, f"{where}.{key}" if where else key)
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from walk_strings(value, f"{where}[{index}]")
