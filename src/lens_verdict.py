"""Read a second-lens verdict, or say the lens did not run.

`tools/second_lens.sh` runs two lenses over one change -- Codex first, Claude
Fable when Codex cannot run -- and both answer the same file,
`tools/lens_verdict.schema.json`. This module is the part that decides whether
what came back is a verdict at all, and it is separate from the shell script for
one reason: the distinction the whole design rests on is *the lens said pass*
against *the lens never ran*, and a shell script that greps for the word `pass`
cannot tell those apart. A truncated answer, a refusal, a quota message, an
empty file and a crash all contain no verdict, and all of them have to land in
the same place as a crash.

So: a file that validates against the schema is the lens's answer, whatever it
says. Anything else is the lens having failed to run, and a lens that failed to
run is never an approval.

Two wrappers, one shape
-----------------------

Codex writes its last message to the file named by `--output-last-message`, and
with `--output-schema` that message is the JSON object itself. Claude, asked for
`--output-format json`, writes an envelope whose `result` key holds the
assistant's final text; the verdict is inside that string. `read_claude` unwraps
one level and then reads the same shape, so the two lenses are compared on the
same bytes rather than on two dialects.

A fence, and prose around the object, are accepted on the Claude side and only
there. The instruction says one JSON object and nothing else; Codex runs under
`--output-schema`, so its last message *is* the object and cannot carry either,
and accepting one there would be accepting a violation. The Claude side has no
such constraint on it: the `result` string is free text, and a fence or a
sentence in front of the verdict is the commonest deviation from an otherwise
complete answer. Reading that as "the lens did not run" retires the fallback
over three backticks or one sentence -- and it did, on 2026-09-22, turning a
`fail` with three findings into `no_lens_ran`. `_verdict_in` is where that is
handled and why.

    python3.12 -m src.lens_verdict codex .lens/codex.json --lens codex
    python3.12 -m src.lens_verdict claude .lens/fable.json --lens claude-fable-fallback
    python3.12 -m src.lens_verdict ledger --ledger events/ledger.jsonl ...

`codex` and `claude` print `<verdict> <findings_count> <exit_code> <model>` on stdout
and exit 0 when the file is a verdict, and exit 1 with one line on stderr when
it is not. The third field is the status `tools/second_lens.sh` answers with,
printed here so the mapping from verdict to exit code lives in one file: two
copies of a number that decides whether a pull request merges is one copy too
many. `ledger` appends one line and exits 0, and a ledger line that could not be
written is not an approval either -- the script reads that status too. Exit 3 is
the wrong interpreter.

The `lens` key as the model wrote it is not trusted. The script knows which
binary it invoked; the model only knows what it was told. `normalise` puts the
caller's name in, and a disagreement is reported rather than silently kept,
because a fallback verdict filed under `codex` would make the weekly re-lens
routine skip exactly the rows it exists to re-read.
"""

from __future__ import annotations

import argparse
import datetime
import json
import sys
from pathlib import Path
from typing import Any

import jsonschema

try:
    from src import interpreter_pin
except ImportError:  # invoked as a plain script
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import interpreter_pin

SCHEMA_PATH = Path(__file__).resolve().parent.parent / "tools" / "lens_verdict.schema.json"

NOT_A_VERDICT = 1

# The exit codes `tools/second_lens.sh` answers with. Written here as well as
# there because the weekly routine and the build skill both read them, and a
# number that means "no lens ran" in one file and "fail" in another is worse
# than no number at all.
PASS = 0
FAIL = 1
NEEDS_JUDGMENT = 2
NO_LENS_RAN = 3

EXIT_FOR_VERDICT = {"pass": PASS, "fail": FAIL, "needs_judgment": NEEDS_JUDGMENT}


class NotAVerdict(Exception):
    """What came back is not a verdict, so the lens is recorded as not run."""


def schema() -> dict[str, Any]:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def validate(obj: Any) -> dict[str, Any]:
    """The object when it is a verdict; raise NotAVerdict when it is not.

    Two contradictions are refused here rather than in the schema, because a
    structured-output provider enforces types and enums and cannot enforce a
    relation between two fields:

    * **A `pass` carrying findings.** The lens said it could not break the
      change and then listed what broke. Whichever half is true, the object is
      not an answer, and the one reading that must never win by default is the
      half that exits 0.
    * **A `pass` with `reads` of zero.** `tools/lens_prompt.md` tells the lens
      that a pass with no reads is read as a lens that did not look. It was a
      sentence the model was trusted to obey until this refused it: a lens that
      opened no files has reviewed nothing, and "reviewed nothing" is the same
      outcome as "did not run" and takes the same exit code.

    Both land on `NotAVerdict`, so both reach exit 3, which is never an
    approval. A `fail` with no findings is left alone: it gives the builder
    nothing to fix, which is a poor verdict, but it blocks either way and
    turning it into exit 3 would lose the only signal in it.
    """
    try:
        jsonschema.validate(obj, schema())
    except jsonschema.ValidationError as error:
        raise NotAVerdict(f"does not match the verdict schema: {error.message}") from error
    if obj["verdict"] == "pass":
        if obj["findings"]:
            raise NotAVerdict(
                f"a pass carrying {len(obj['findings'])} finding(s) is a contradiction, "
                f"not a verdict"
            )
        if obj["reads"] <= 0:
            raise NotAVerdict(
                f"a pass claiming {obj['reads']} reads is a lens that did not look")
    return obj


def _load(path: Path) -> str:
    if not path.exists():
        raise NotAVerdict(f"{path} was not written")
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.strip():
        raise NotAVerdict(f"{path} is empty")
    return text


def _parse(text: str, where: str) -> Any:
    try:
        return json.loads(text)
    except json.JSONDecodeError as error:
        raise NotAVerdict(f"{where} is not JSON: {error}") from error


def read_codex(path: Path) -> dict[str, Any]:
    """The verdict Codex wrote, or NotAVerdict."""
    return validate(_parse(_load(path), str(path)))


def _validates(obj: Any) -> bool:
    try:
        validate(obj)
    except NotAVerdict:
        return False
    return True


def _objects_in(text: str) -> list[Any]:
    """Every JSON object that starts somewhere in a string, in start order.

    `raw_decode` is offered each `{` in turn, so a nested object is found as
    well as the one containing it. That is wanted: the caller keeps only what
    validates, and which bracket the verdict starts at is not something this
    can know in advance.
    """
    decoder = json.JSONDecoder()
    found: list[Any] = []
    for start, character in enumerate(text):
        if character != "{":
            continue
        try:
            obj, _ = decoder.raw_decode(text, start)
        except ValueError:
            continue
        found.append(obj)
    return found


def _verdict_in(text: str, where: str) -> dict[str, Any]:
    """The verdict, whatever the lens wrote around it.

    The prompt asks for one JSON object and nothing else, and a sentence the
    model is trusted to obey is not a check -- `lessons.md` carries that one
    already. On 2026-09-22 the fallback lens answered the lens design's own
    review with "Finishing up: I've read the full diff..." and then a
    schema-valid `fail` carrying three findings. The reader threw the whole
    answer away, the run recorded `no_lens_ran`, and a `fail` became silence.
    `tests/fixtures/lens/fable_prose_before_the_verdict.json` is that answer.

    That is the same mistake this module exists to refuse in the other
    direction: "a file that validates against the schema is the lens's answer,
    whatever it says". Judging the answer by the prose around it is judging by a
    string match, which is what the exit status was taken away for.

    This is the Claude side only. Codex answers under `--output-schema`, where
    the message is the object, so anything around it there is a violation and
    stays one -- `read_codex` is strict on purpose.

    Strict first, so an answer that is exactly one object is read exactly. Only
    when that fails is the text searched, and only an object that validates
    counts -- a JSON blob quoted out of the diff is not a verdict because it
    does not have the four keys.

    **Exactly one**, or nothing. The first version of this took the last one, on
    the reasoning that the verdict is what the lens ends on -- which is an
    assumption about model behaviour, in a function written because the model
    does not obey the one-object instruction. The next reading found what that
    costs: a lens reviewing a change to this project reads
    `tests/test_second_lens.py`, which carries a valid `pass` object verbatim,
    and a `fail` followed by a quotation of that object would have been read as
    a `pass` and exited 0. A same-family lens turning a non-approval into an
    approval by the shape of its output is the one path the design says cannot
    happen. Two answers are an ambiguous answer; ambiguous is exit 3, which is a
    person reading it, which is the right outcome.

    Identical repeats are one answer, not two -- a lens that restates its
    verdict has not given two.

    **And recovery never produces an approval.** Closing the two-object case
    left the one-object case open, which is the same hole with the quotation on
    its own: "I could not finish; the shape is {...a valid pass...}" carries
    exactly one validating object and would have been read as a `pass` at exit
    0 with auto-merge on. The risk is not symmetric -- reading an answer
    loosely can only ever let a change through, or only ever stop one,
    depending on what it says -- so the rule is not symmetric either. A `pass`
    has to be the whole answer, strictly parsed. A `fail` or a `needs_judgment`
    may be recovered from around the prose, because recovering one costs a
    person a reading and losing one costs the project the finding. Anything
    else is exit 3, which is where a quota sentence has always belonged.
    """
    try:
        return validate(_parse(_unfence(text), where))
    except NotAVerdict:
        answers = [obj for obj in _objects_in(text) if _validates(obj)]
        if not answers:
            raise
        distinct = {json.dumps(obj, sort_keys=True) for obj in answers}
        if len(distinct) > 1:
            raise NotAVerdict(
                f"{where} carries {len(distinct)} different verdicts, and an "
                "answer that says two things is not an answer")
        recovered = validate(answers[0])
        if EXIT_FOR_VERDICT[recovered["verdict"]] == PASS:
            raise NotAVerdict(
                f"{where} is prose around a `pass`, and an approval has to be "
                "the whole answer -- a quoted example reads exactly like one")
        return recovered


def _unfence(text: str) -> str:
    """The body of a single fenced block, or the text unchanged."""
    stripped = text.strip()
    if not stripped.startswith("```"):
        return stripped
    lines = stripped.split("\n")
    if len(lines) < 3 or not lines[-1].strip().startswith("```"):
        return stripped
    return "\n".join(lines[1:-1])


UNRECORDED_MODEL = "unrecorded"


def served_model(envelope: Any) -> str:
    """The model that actually answered, out of the envelope's usage record.

    The lens name and the model are two different facts. `LENS_FALLBACK_MODEL`
    can put a different model behind the name `claude-fable-fallback`, and a
    ledger that carried only the name would not show it -- so the name comes
    from the script, which knows what it invoked, and the model comes from here,
    which knows what answered.
    """
    if not isinstance(envelope, dict):
        return UNRECORDED_MODEL
    usage = envelope.get("modelUsage")
    if isinstance(usage, dict) and usage:
        return ", ".join(sorted(str(name) for name in usage))
    return UNRECORDED_MODEL


def read_claude(path: Path) -> dict[str, Any]:
    """The verdict inside a `claude -p --output-format json` envelope."""
    envelope = _parse(_load(path), str(path))
    if isinstance(envelope, dict) and "result" not in envelope:
        # Already the bare object, which is what a future output format may give.
        return validate(envelope)
    if not isinstance(envelope, dict):
        raise NotAVerdict(f"{path} is not an object")
    result = envelope.get("result")
    if envelope.get("is_error"):
        raise NotAVerdict(f"{path} reports an error: {str(result)[:200]}")
    if not isinstance(result, str):
        raise NotAVerdict(f"{path} carries no result text")
    verdict = _verdict_in(result, f"the result text in {path}")
    return {**verdict, "served_model": served_model(envelope)}


def normalise(verdict: dict[str, Any], lens: str) -> dict[str, Any]:
    """The verdict with the lens that actually ran named in it."""
    written = verdict.get("lens")
    out = dict(verdict)
    out["lens"] = lens
    if written != lens:
        out["lens_as_written"] = written
    return out


# `main` when the judge was pinned out of the agreed ref, which is the ordinary
# case; `tree` when the change under review is the one that builds the lens and
# the pinned ref has no copy to take. The weekly routine reads the rows that say
# `tree` for the same reason it reads the fallback rows.
JUDGE_FROM_TREE = "tree"

# And `lens_from`, the same question asked about `tools/second_lens.sh` itself.
# The script cannot materialise itself out of the pinned ref -- it is already
# running -- so all it can do is say whether it differs from that ref. A branch
# that replaces the script can delete the line that says so, which is why
# `docs/HOW_WE_WORK.md` names this as a trust root a person closes by reading
# one diff, rather than a hole this field covers. What the field does cover is
# the ordinary case: the script edited for some other reason, recorded, and
# re-read next week alongside the fallback and `judge_from` rows.


def ledger_line(
    item: str,
    lens: str,
    verdict: str,
    findings_count: int,
    at: str,
    model: str = UNRECORDED_MODEL,
    judge_from: str = JUDGE_FROM_TREE,
    lens_from: str = JUDGE_FROM_TREE,
) -> str:
    """The one line this lens run appends to the ledger."""
    return json.dumps(
        {
            "item": item,
            "lens": lens,
            "model": model,
            "judge_from": judge_from,
            "lens_from": lens_from,
            "verdict": verdict,
            "findings_count": findings_count,
            "at": at,
        },
        ensure_ascii=False,
        sort_keys=True,
    )


def correction_line(item: str, corrects: str, note: str, at: str) -> str:
    """One line retiring an item title the ledger can never close.

    `CLAUDE.md`: "Append-only under runs/ · rules/ · events/ ... A correction is
    a new file plus one ledger line." This is that line. It carries no `lens`
    key, so everything that greps for one steps over it, and the weekly queue
    reads `corrects` to know that an item is no longer open.

    The case it was written for: a run recorded under a title that is not a row
    in `docs/next_cycle_tasks.md`. The script refuses such a title now, which is
    exactly why the row it left behind can never be closed -- no later run can
    append under that name, the queue keys on the item, and a queue that cannot
    be emptied reports the same phantom every week. Retiring it is a fact about
    the record, so it goes in the record.
    """
    return json.dumps(
        {"at": at, "corrects": corrects, "item": item, "note": note},
        ensure_ascii=False, sort_keys=True)


def append_ledger(path: Path, line: str) -> None:
    """Append one line. The file grows by design; nothing already in it moves."""
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    separator = "" if not existing or existing.endswith("\n") else "\n"
    with path.open("a", encoding="utf-8") as handle:
        handle.write(f"{separator}{line}\n")


def _now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


def main(argv: list[str] | None = None) -> int:
    wrong = interpreter_pin.enforce()
    if wrong:
        return wrong

    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)

    for name in ("codex", "claude"):
        one = sub.add_parser(name)
        one.add_argument("path", type=Path)
        one.add_argument("--lens", required=True)
        one.add_argument("--normalised", type=Path, default=None)

    line = sub.add_parser("ledger")
    line.add_argument("--ledger", type=Path, required=True)
    line.add_argument("--item", required=True)
    line.add_argument("--lens", required=True)
    line.add_argument("--verdict", required=True)
    line.add_argument("--findings", type=int, default=0)
    line.add_argument("--model", default=UNRECORDED_MODEL)
    line.add_argument("--judge-from", default=JUDGE_FROM_TREE)
    line.add_argument("--lens-from", default=JUDGE_FROM_TREE)

    sub.add_parser(
        "where",
        help="print the file this module was imported from, so a caller can "
             "check which copy of it actually ran rather than assume",
    )

    args = parser.parse_args(argv)

    if args.command == "where":
        print(Path(__file__).resolve())
        return 0

    if args.command == "ledger":
        append_ledger(
            args.ledger,
            ledger_line(
                args.item, args.lens, args.verdict, args.findings, _now(), args.model,
                args.judge_from, args.lens_from,
            ),
        )
        return 0

    reader = read_codex if args.command == "codex" else read_claude
    try:
        verdict = normalise(reader(args.path), args.lens)
    except NotAVerdict as error:
        print(f"{args.lens} did not run: {error}", file=sys.stderr)
        return NOT_A_VERDICT
    if args.normalised is not None:
        args.normalised.parent.mkdir(parents=True, exist_ok=True)
        args.normalised.write_text(
            json.dumps(verdict, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    # Three fields, and the third is the exit code the script answers with. The
    # script used to carry its own copy of the mapping; two copies of a number
    # that decides whether a pull request merges is one copy too many.
    print(
        f"{verdict['verdict']} {len(verdict['findings'])} "
        f"{EXIT_FOR_VERDICT[verdict['verdict']]} "
        f"{verdict.get('served_model', UNRECORDED_MODEL)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
