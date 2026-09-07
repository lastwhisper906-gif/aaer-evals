"""The gate between extract and predict. Four checks, one line each.

It reads an assembled bundle directory and nothing else, so it can be run on a
bundle a reader has downloaded as easily as on one this repository just made.
Every check prints a line whether it passes or fails; a failing run exits
non-zero and every failure line names its gate, because a check whose output
has to be interpreted is a check nobody runs.

The four are the ones that decide whether a bundle may be handed to a model:

1. **Schema** — the eight files are there, they parse, and they carry the keys
   the rest of the pipeline reads.
2. **Paragraph counts in range** — within ±20% of the counts recorded in
   `expected.json`. This is the extraction-drift check `docs/HOW_WE_WORK.md`
   runs weekly, in the form the pipeline runs every time. A count the record
   says is zero has to be zero: "±20% of nothing" is not a range.
3. **Cutoff violations = 0** — every document in the manifest was filed at or
   before the manifest's cutoff. Fail-closed: a document with no filing date, or
   a manifest with no cutoff, is a violation and not a pass.
4. **At least one TextBlock** — a bundle whose notes file has no note in it is
   an extraction failure. No filer has no notes.

    python3.12 -m src.extraction_checks /tmp/bundle
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

try:
    from src import assemble_bundle, cutoff_guard, interpreter_pin
except ImportError:  # invoked as a plain script
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import assemble_bundle, cutoff_guard, interpreter_pin

FAILED = 1
BAD_INPUT = 2

TOLERANCE = 0.20
COUNTED = ("paragraphs", "notes", "mdna", "note_history", "eight_k")
NOTE_HEADING = re.compile(r"^##\s+(\S*TextBlock)\s*$", re.MULTILINE)

REQUIRED_KEYS = {
    "input_numbers.json": ("ticker", "cutoff", "documents", "facts"),
    "input_trends.json": ("ticker", "quarters", "years", "coverage"),
    "input_manifest.json": ("ticker", "form", "accession", "cutoff", "rules_version",
                            "served_model", "documents", "paragraphs", "exclusions",
                            "counts", "files"),
}
MARKDOWN_FILES = ("input_notes.md", "input_notes_history.md", "input_mdna.md",
                  "input_8k.md", "input_prior_predictions.md")


class Result:
    """One gate's verdict, and the line it prints."""

    def __init__(self, gate: str) -> None:
        self.gate = gate
        self.failures: list[str] = []
        self.detail = ""

    def fail(self, message: str) -> None:
        self.failures.append(message)

    @property
    def passed(self) -> bool:
        return not self.failures

    def lines(self) -> list[str]:
        if self.passed:
            return [f"{self.gate}: pass — {self.detail}"]
        return [f"{self.gate}: FAIL — {message}" for message in self.failures]


def read_bundle(root: Path) -> dict:
    """Every file's text, by name. A file that is missing is missing here."""
    texts = {}
    for name in assemble_bundle.FILES:
        try:
            texts[name] = cutoff_guard.load_bundle_file(root, name)
        except cutoff_guard.CutoffGuardError:
            texts[name] = None
    return texts


# --- the four gates ---------------------------------------------------------

def check_schema(texts: dict) -> tuple[Result, dict]:
    result = Result("schema")
    parsed: dict = {}
    for name in assemble_bundle.FILES:
        if texts.get(name) is None:
            result.fail(f"{name} is not in the bundle")
    for name, keys in REQUIRED_KEYS.items():
        if texts.get(name) is None:
            continue
        try:
            payload = json.loads(texts[name])
        except ValueError as exc:
            result.fail(f"{name} does not parse as JSON: {exc}")
            continue
        parsed[name] = payload
        for key in keys:
            if key not in payload:
                result.fail(f'{name} has no "{key}"')
    for name in MARKDOWN_FILES:
        text = texts.get(name)
        if text is None:
            continue
        if not text.strip():
            result.fail(f"{name} is empty")
        elif not text.lstrip().startswith("#"):
            result.fail(f"{name} does not start with a heading")
    result.detail = (f"{sum(1 for name in assemble_bundle.FILES if texts.get(name))} "
                     f"of {len(assemble_bundle.FILES)} files, every required key present")
    return result, parsed


def check_counts(manifest: dict | None, *, fixtures_root=cutoff_guard.FIXTURES) -> Result:
    result = Result("paragraph counts")
    if manifest is None:
        result.fail("no manifest to count")
        return result
    ticker, form = manifest.get("ticker"), manifest.get("form")
    try:
        recorded = cutoff_guard.expected_values(ticker, fixtures_root=fixtures_root)
    except cutoff_guard.CutoffGuardError as exc:
        result.fail(str(exc))
        return result
    reference = (recorded.get("bundle") or {}).get(form)
    if not reference:
        result.fail(f"expected.json records no bundle counts for {ticker} {form}")
        return result

    counts = manifest.get("counts") or {}
    checked = 0
    for key in COUNTED:
        if key not in reference:
            continue
        want, got = reference[key], counts.get(key)
        if got is None:
            result.fail(f"the manifest has no {key} count")
            continue
        checked += 1
        if want == 0:
            if got != 0:
                result.fail(f"{key} is {got}, and expected.json records none")
            continue
        low, high = want * (1 - TOLERANCE), want * (1 + TOLERANCE)
        if not low <= got <= high:
            result.fail(f"{key} is {got}, outside ±{int(TOLERANCE * 100)}% of "
                        f"the recorded {want} ({low:.0f}–{high:.0f})")
    result.detail = (f"{checked} counts within ±{int(TOLERANCE * 100)}% of "
                     f"expected.json for {ticker} {form}")
    return result


def _date(value, what: str) -> dt.date:
    if not value:
        raise ValueError(f"{what} has no date")
    return dt.date.fromisoformat(str(value))


def check_cutoff(manifest: dict | None) -> Result:
    """Fail-closed, the same rule as the loader: no date is a violation."""
    result = Result("cutoff")
    if manifest is None:
        result.fail("no manifest to check")
        return result
    try:
        cutoff = _date(manifest.get("cutoff"), "the manifest")
    except ValueError as exc:
        result.fail(f"unusable cutoff: {exc}")
        return result

    documents = manifest.get("documents")
    if not documents:
        result.fail("the manifest lists no documents at all")
        return result
    for row in documents:
        named = f"{row.get('form')} {row.get('role')} {row.get('accession')}"
        try:
            filed = _date(row.get("filing_date"), named)
        except ValueError as exc:
            result.fail(f"{named}: {exc} — refused, a document with no filing date "
                        f"cannot be shown to be inside the cutoff")
            continue
        if filed > cutoff:
            result.fail(f"{named} was filed {filed}, after the cutoff {cutoff}")
    result.detail = f"{len(documents)} documents, none filed after {cutoff}"
    return result


def check_notes(texts: dict) -> Result:
    result = Result("notes")
    text = texts.get("input_notes.md")
    if text is None:
        result.fail("input_notes.md is not in the bundle")
        return result
    found = NOTE_HEADING.findall(text)
    if not found:
        result.fail("input_notes.md carries no TextBlock section — a filing with no "
                    "notes is an extraction failure, not a company without notes")
    result.detail = f"{len(found)} TextBlock sections"
    return result


def run(root: Path, *, fixtures_root=cutoff_guard.FIXTURES) -> tuple[int, list[str]]:
    """Every gate, in order. The exit code and the lines to print."""
    texts = read_bundle(Path(root))
    schema, parsed = check_schema(texts)
    manifest = parsed.get("input_manifest.json")
    results = [schema,
               check_counts(manifest, fixtures_root=fixtures_root),
               check_cutoff(manifest),
               check_notes(texts)]
    lines = [line for result in results for line in result.lines()]
    return (0 if all(result.passed for result in results) else FAILED), lines


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="the four gates between extract and predict")
    parser.add_argument("bundle", help="the run directory to check")
    parser.add_argument("--fixtures", default=str(cutoff_guard.FIXTURES))
    args = parser.parse_args(argv)

    root = Path(args.bundle)
    if not root.is_dir():
        print(f"extraction_checks: {root} is not a directory", file=sys.stderr)
        return BAD_INPUT
    code, lines = run(root, fixtures_root=Path(args.fixtures))
    for line in lines:
        print(line, file=sys.stderr if code else sys.stdout)
    return code


if __name__ == "__main__":
    raise SystemExit(interpreter_pin.enforce() or main())
