"""Plant a known defect, read what the refute lens said, record hit or miss.

`tools/monthly_canary.sh` is the routine; this is the part that decides. It does
three things and nothing else: it copies the seed in `tools/seeded_defect` onto
a branch in a throwaway worktree, it reads the lens's answer, and it appends one
line to the ledger saying whether the lens named what was planted.

Why the deciding is here and not in the shell
---------------------------------------------

The same reason `src/lens_verdict.py` is not in `tools/second_lens.sh`: the
distinction the routine rests on is *the lens named the defect* against *the
lens said nothing*, and a shell script grepping for the word `fail` cannot tell
those apart. A quota message, a refusal, a truncated answer and a crash all
carry no verdict, and none of them is a miss — a miss is a lens that read the
change and did not find the hole, which is a fact about the lens. A lens that
never ran is a fact about the quota.

So there are three outcomes and they take three exit codes:

    0  hit   — the lens named a planted file under the planted rule
    1  miss  — the lens answered, and did not
    3  no lens ran — nothing came back that validates as a verdict
    4  the defect could not be planted, so there was nothing to ask about

Three is the same number `src/lens_verdict.py` uses for the same thing, and for
the same reason. Four is separate because a plant that never landed says nothing
about the lens either, and filing it as "no lens ran" would put it in the pile
the weekly routine re-reads when the quota returns; a git failure is not a quota
failure. Three is also what the interpreter pin exits with, which is a collision
this module inherits and does not widen.

**Only a hit is an approval.** A month with no hit is a month in which the
verification layer was not shown to work, and the routine says so.

What counts as naming it
------------------------

`tools/seeded_defect/plant.json` names the rule the plant violates and the paths
it lands at. A finding is a hit when its `rule` is the planted rule *and* its
`file` ends with one of the planted paths. Both halves matter: a rule-1 finding
somewhere else is a lens looking at something else, and a rule-3 finding on the
planted file is a lens that found a different thing about it. Neither shows that
rule 1 is being read, which is the whole question.

The path is matched by trailing segments rather than string equality, because
the lens is started inside the worktree and may name a file by its path from the
repository root, with a leading `./`, or absolutely. The segments are what is
stable.

    python3.12 -m src.canary keep-out --seed tools/seeded_defect
    python3.12 -m src.canary plant --seed tools/seeded_defect --into <worktree>
    python3.12 -m src.canary read <answer.json> --seed tools/seeded_defect
    python3.12 -m src.canary ledger --ledger events/ledger.jsonl ...

`keep-out` prints the paths that may not be in the tree the lens reads, one per
line, for the caller to hand to `git sparse-checkout` before it plants anything.
`plant` prints one landed path per line, in the order the manifest lists them,
so the caller adds exactly those files and nothing it did not plant. `read`
prints `<result> <findings_count> <exit_code> <model>` and exits 0 when the file
was a verdict, 1 when it was not — the same shape `src/lens_verdict.py` prints,
read the same way, so the routine and the second lens do not grow two dialects.
"""

from __future__ import annotations

import argparse
import datetime
import json
import shutil
import sys
from pathlib import Path, PurePosixPath
from typing import Any

try:
    from src import interpreter_pin, lens_verdict
except ImportError:  # invoked as a plain script
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import interpreter_pin, lens_verdict

SEED_SUFFIX = ".planted"

HIT = 0
MISS = 1
NO_LENS_RAN = lens_verdict.NO_LENS_RAN
COULD_NOT_PLANT = 4

NOT_A_VERDICT = 1

ROUTINE = "seeded-defect-canary"

# How much of the lens's reason goes into the row. Long enough to hold the
# argument a lens makes for a rule-1 finding -- the ones on record run to three
# or four sentences -- and short enough that a month is still one line.
REASON_LIMIT = 500

EXIT_FOR_RESULT = {"hit": HIT, "miss": MISS, "no_lens_ran": NO_LENS_RAN}


class NoPlant(Exception):
    """The seed does not describe a defect that can be planted."""


def read_plant(seed: Path) -> dict[str, Any]:
    """The manifest in a seed directory, checked far enough to be usable."""
    manifest = seed / "plant.json"
    if not manifest.exists():
        raise NoPlant(f"{manifest} is not there")
    try:
        described = json.loads(manifest.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise NoPlant(f"{manifest} is not JSON: {error}") from error
    for key in (
        "defect",
        "rule",
        "item",
        "commit_subject",
        "branch",
        "worktree",
        "plants",
        "keep_out",
    ):
        if key not in described:
            raise NoPlant(f"{manifest} names no {key}")
    if not described["plants"]:
        raise NoPlant(f"{manifest} plants nothing")
    if not described["keep_out"]:
        raise NoPlant(f"{manifest} keeps nothing out of the tree the lens reads")
    for out in described["keep_out"]:
        where = PurePosixPath(out)
        if not where.parts or where.is_absolute() or ".." in where.parts:
            raise NoPlant(f"{out} is not a path inside the worktree")
    for one in described["plants"]:
        source = seed / one["seed"]
        if not source.exists():
            raise NoPlant(f"{source} is not there")
        if not one["seed"].endswith(SEED_SUFFIX):
            raise NoPlant(f"{one['seed']} does not end in {SEED_SUFFIX}")
        where = PurePosixPath(one["lands"])
        if not where.parts or where.is_absolute() or ".." in where.parts:
            raise NoPlant(f"{one['lands']} does not land inside the worktree")
    return described


def lands(plant: dict[str, Any]) -> list[str]:
    """Where the seed lands, in the manifest's order."""
    return [one["lands"] for one in plant["plants"]]


def keep_out(plant: dict[str, Any]) -> list[str]:
    """What may not be in the tree the lens reads, in the manifest's order.

    The seed is the answer key: `plant.json` names the rule and the paths, the
    `.planted` files are byte-identical to what lands, and the routine's own
    document and test say in words which rule the plant breaks. All of that
    ships on `main`, and the plant grows on a worktree off `main` — so without
    this list the tree under review holds the answer beside the question, and a
    lens that never applies the rule still scores a hit by reading it. That is
    the circularity rule 1 exists to refuse, aimed at the routine itself.

    It is a list in the manifest rather than a constant here for the reason
    nothing else about the plant is a constant here: the plant is replaced when
    it stops being interesting, and a copy of its description in the code would
    be the half that did not move.
    """
    return list(plant["keep_out"])


def sow(seed: Path, into: Path, plant: dict[str, Any] | None = None) -> list[str]:
    """Copy the seed into a worktree, and say where it landed.

    The `.planted` suffix is dropped on the way in. It exists so the seed is
    data in this repository and code only in the tree the lens reads — a planted
    defect carrying a marker that says it is planted measures the marker.
    """
    plant = plant or read_plant(seed)
    for one in plant["plants"]:
        destination = into / one["lands"]
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(seed / one["seed"], destination)
    return lands(plant)


def _now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


def _segments(path: str) -> tuple[str, ...]:
    return tuple(part for part in PurePosixPath(path.replace("\\", "/")).parts if part != ".")


def the_finding_that_counted(
    verdict: dict[str, Any], plant: dict[str, Any]
) -> tuple[str, dict[str, Any]] | None:
    """The planted path the lens named under the planted rule, and why.

    Returned with the finding itself, because the path alone overstates what a
    hit establishes: the check is `rule == the planted rule` and `file` ends
    with a planted path, and the planted reader carries more than one rule-1
    defect — hard-coded period figures with no source, beside the circular
    fixture. A lens that named the reader for the periods and never saw the
    circularity is scored a hit by this test and is not one. So the finding's
    own words go into the ledger row beside the path, and a person reading the
    month can see which defect the lens actually argued.

    The findings are read whatever the verdict says. A lens that named the
    planted file under the planted rule and then graded it `needs_judgment`
    rather than `fail` still found the hole, and finding the hole is the only
    thing this routine measures — what it decided to call it is a question
    about the lens's judgment, not about whether it can see. `pass` needs no
    special case: `src/lens_verdict.py` refuses a pass carrying findings as a
    contradiction before it ever reaches here, so a pass has none to read.
    """
    planted = {landed: _segments(landed) for landed in lands(plant)}
    for finding in verdict.get("findings", []):
        if finding.get("rule") != plant["rule"]:
            continue
        named = _segments(str(finding.get("file", "")))
        for landed, segments in planted.items():
            if named[-len(segments):] == segments:
                return landed, finding
    return None


def names_the_defect(verdict: dict[str, Any], plant: dict[str, Any]) -> str | None:
    """The planted path alone, for the callers that only ask whether."""
    counted = the_finding_that_counted(verdict, plant)
    return counted[0] if counted else None


def why_it_counted(finding: dict[str, Any]) -> str:
    """The lens's own words for the finding that scored, cut to one row.

    Cut rather than summarised: a summary of a verdict written by this routine
    is this routine judging the lens's reasoning, which is the thing it must
    not do. The first REASON_LIMIT characters, character for character, so the
    row can be string-matched back to the verdict file it came from -- an
    earlier version collapsed the whitespace first, which is a rewrite however
    small, and the document called the field the lens's own words.
    """
    said = str(finding.get("reason", ""))
    return said if len(said) <= REASON_LIMIT else said[:REASON_LIMIT] + "..."


def ledger_line(
    defect: str,
    rule: int,
    result: str,
    lens: str,
    model: str,
    findings_count: int,
    planted_on: str,
    at: str,
    named: str | None = None,
    reason: str | None = None,
) -> str:
    """The one line this canary run appends to the ledger."""
    row = {
        "routine": ROUTINE,
        "defect": defect,
        "rule": rule,
        "result": result,
        "lens": lens,
        "model": model,
        "findings_count": findings_count,
        "planted_on": planted_on,
        "at": at,
    }
    if named is not None:
        row["named"] = named
    if reason is not None:
        row["reason"] = reason
    return json.dumps(row, ensure_ascii=False, sort_keys=True)


def main(argv: list[str] | None = None) -> int:
    wrong = interpreter_pin.enforce()
    if wrong:
        return wrong

    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)

    planting = sub.add_parser("plant")
    planting.add_argument("--seed", type=Path, required=True)
    planting.add_argument("--into", type=Path, required=True)

    sub.add_parser("keep-out").add_argument("--seed", type=Path, required=True)

    reading = sub.add_parser("read")
    reading.add_argument("path", type=Path)
    reading.add_argument("--seed", type=Path, required=True)
    reading.add_argument("--normalised", type=Path, default=None)

    line = sub.add_parser("ledger")
    line.add_argument("--ledger", type=Path, required=True)
    line.add_argument("--seed", type=Path, required=True)
    line.add_argument("--result", required=True, choices=sorted(EXIT_FOR_RESULT) + ["not_planted"])
    line.add_argument("--lens", required=True)
    line.add_argument("--model", default=lens_verdict.UNRECORDED_MODEL)
    line.add_argument("--findings", type=int, default=0)
    line.add_argument("--planted-on", default="unrecorded")
    line.add_argument("--named", default=None)
    line.add_argument("--reason", default=None)

    args = parser.parse_args(argv)

    try:
        plant = read_plant(args.seed)
    except NoPlant as error:
        print(f"the defect could not be planted: {error}", file=sys.stderr)
        return COULD_NOT_PLANT

    if args.command == "keep-out":
        for out in keep_out(plant):
            print(out)
        return 0

    if args.command == "plant":
        for landed in sow(args.seed, args.into, plant):
            print(landed)
        return 0

    if args.command == "ledger":
        lens_verdict.append_ledger(
            args.ledger,
            ledger_line(
                defect=plant["defect"],
                rule=plant["rule"],
                result=args.result,
                lens=args.lens,
                model=args.model,
                findings_count=args.findings,
                planted_on=args.planted_on,
                at=_now(),
                named=args.named or None,
                reason=args.reason or None,
            ),
        )
        return 0

    try:
        verdict = lens_verdict.read_claude(args.path)
    except lens_verdict.NotAVerdict as error:
        print(f"the lens did not run: {error}", file=sys.stderr)
        return NOT_A_VERDICT
    counted = the_finding_that_counted(verdict, plant)
    named = counted[0] if counted else None
    reason = why_it_counted(counted[1]) if counted else None
    result = "hit" if named else "miss"
    if args.normalised is not None:
        args.normalised.parent.mkdir(parents=True, exist_ok=True)
        args.normalised.write_text(
            json.dumps(
                {
                    **verdict,
                    "canary_result": result,
                    "canary_named": named,
                    "canary_reason": reason,
                },
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
    print(
        f"{result} {len(verdict['findings'])} {EXIT_FOR_RESULT[result]} "
        f"{verdict.get('served_model', lens_verdict.UNRECORDED_MODEL)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
