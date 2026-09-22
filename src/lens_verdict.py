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

A fenced block is accepted on the Claude side and only there. The instruction
says one JSON object and nothing else, and Codex's structured output cannot
carry a fence, so accepting one there would be accepting a violation. On the
Claude side the fence is the commonest deviation from an otherwise complete
answer, and reading it as "the lens did not run" would retire the fallback over
three backticks.

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
    verdict = validate(_parse(_unfence(result), f"the result text in {path}"))
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


def ledger_line(
    item: str,
    lens: str,
    verdict: str,
    findings_count: int,
    at: str,
    model: str = UNRECORDED_MODEL,
    judge_from: str = JUDGE_FROM_TREE,
) -> str:
    """The one line this lens run appends to the ledger."""
    return json.dumps(
        {
            "item": item,
            "lens": lens,
            "model": model,
            "judge_from": judge_from,
            "verdict": verdict,
            "findings_count": findings_count,
            "at": at,
        },
        ensure_ascii=False,
        sort_keys=True,
    )


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

    args = parser.parse_args(argv)

    if args.command == "ledger":
        append_ledger(
            args.ledger,
            ledger_line(
                args.item, args.lens, args.verdict, args.findings, _now(), args.model,
                args.judge_from,
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
