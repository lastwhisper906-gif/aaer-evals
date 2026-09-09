"""Name every letter-number code in the files this branch changed.

`CLAUDE.md` says: plain names, no letter-number codes, machine keys are readable
slugs. `docs/HOW_WE_WORK.md` says where it bites -- a code in a report, a ledger,
an issue title, a filename or a commit message is a bug. The rule was written
because the archived project ran on codes. Counted with the two patterns below
over `archive/**/*.md`, which is frozen at a tag and so cannot drift, `B3`
appears 168 times, `B4` 148, `GA-001` 100, `RP-05` 84, `D15` 77 and `INV-03` 68;
the commit subjects in this repository's own history carry `D-P83`, `E-003`,
`PKT-R2`, `INV11` and `TASK_P6A`. A reader had to hold a lookup table in their
head to read a sentence. Nothing enforced the rule, so this does.

    python3.12 -m src.plain_name_check --changed
    python3.12 src/plain_name_check.py docs CITATION.cff

Exit 0 and no output when clean, 1 when it found a code, 2 when it could not run
-- the baseline ref does not resolve, or a path given to it is not there -- and 3
on the wrong interpreter. Silence about a file it never opened reads exactly like
silence about a file with nothing in it, so it does not exit 0 for either.

One line per occurrence, on stderr, in the shape grep prints: `path:line: CODE`.
A code in the file's own name is reported at line 0, because a name sits on no
line of the file it names.

Standard library only, and it stays that way. The post-write hook in
`.claude/settings.json` runs it under bare `python3.12`, which on this machine
has no site-packages for this project, so one third-party import makes the hook
inert -- and a hook that cannot run reports green by saying nothing, which is the
exact failure this file exists to end.

What `--changed` means
----------------------

Everything this branch touched and did not delete: the diff between the working
tree and the merge base with the baseline ref (`origin/main` by default), plus
untracked files. Committed, staged and unsaved edits all land in that list
exactly once, and a file the branch never touched stays out of it however many
codes it carries -- `CITATION.cff` carries three today, and they are not this
branch's to answer for. An unresolvable baseline is not a pass: it exits 2.

Where the line is
-----------------

A letter-number code is a short uppercase tag bound to a number, standing in for
a name. The archived project wrote it in two shapes and this check reads both:

* dashed, whole -- `RP-09`, `GA-001`, `INV-06`, `INV-03`, `E-003`, `C-8`, `W-8`.
* undashed, as one separated part of a longer name -- `B2`, `B3`, `D15`, `INV11`,
  and the tail of `D-P83`, `Q-R03`, `TASK_P6A`, `PKT-INV11`, `P4c`.

The undashed shape is the one that matters most: it is the commoner of the two
in the archive, it is what a writer reaches for without noticing, and it is what
this repository actually got wrong -- `B1` and `B2` reached
`docs/structure_changes.md` on 2026-09-06 and had to be taken out again. A check
that read the dashed shape alone would have passed that line.

Most of the vocabulary this repository has to keep is safe on shape alone,
because a code leads with capitals and the vocabulary does not:

* EDGAR report names lead with digits -- 10-K, 10-Q, 8-K -- as do item numbers
  (2.02, 4.02), Item 1A and Item 7A, accession numbers (0000320193-26-000001)
  and dates (2026-09-09).
* Versions, standards and file names are lowercase -- v0.1, archive-v1, sha256,
  utf-8, item_9a, aapl-20250927.htm, harness/cycle-020.
* `us-gaap:Revenues` and `MANIFEST.sha256` have no capital tag standing against
  a number; `Exhibit 21` has a space; `CC-BY-4.0` and `COVID-19` have a tag too
  long or a number too far from it to read as a serial.
* `AAPL_10K` is a ticker and a form, and its number leads its part, so it reads
  as a name and stays silent.

Some kept vocabulary does take the shape, and it is exempted **as words, not as
shapes**:

* `EX-` -- exhibit names, `EX-99.1` and its siblings, matched on in
  `src/fetch_fixtures.py`.
* `SHA-`, `UTF-`, `ISO-` -- hash, encoding and character-set standards. These
  are the one entry not read out of this repository, which writes them lowercase
  (`sha256`, `utf-8`) and is silent on them by shape. They are kept because a
  standard's name belongs to the body that set it, not to whoever cites it.
* `Q1` to `Q4` -- the fiscal quarter, which `docs/INPUT_SPEC.md` derives.
* a capital tag on a four-digit year, 1900 to 2099 -- `FY2025`, `FY2021`.
* `CC0` -- the licence named in the Creative Commons text at `LICENSE-docs`
  line 397. It is the one word the first sweep of this repository turned up.

One kind is not on that list yet and is worth naming: an SEC enforcement release
is `AAER-1232`, the shape exactly, and the number is the SEC's rather than ours.
It appears in `archive/` only, which is not read, so it gets a kept word on the
day a document here cites one, and not before.

The list grows by adding a word when one actually turns up, never by widening
the pattern. A shape carve-out is how a check becomes a quiet no-op: the
tempting one here is "let a single capital and one digit through, those are
EDGAR registration forms" -- and the archived project numbered nine of its own
families with exactly that shape, so the carve-out would buy silence on `S-1`
and `S-8`, which this repository never reads, at the price of `B2`, `D15`,
`C-8` and `W-8`, which it wrote.

Which files it reads
--------------------

Every changed file's own name, whatever it is. Its contents too, unless:

* it is source -- `.py`, `.sh`. Code quotes other people's vocabulary and gets
  reported for it: `Q-0` and `Q-1` are period offsets in `src/trends.py`,
  `BLE001` is a linter's rule in a `noqa` comment, and this check's own test
  plants real codes on purpose. The hook runs on every write, and a check
  that fires on green code the first day is a check that is off by the second.
  The cost is stated rather than hidden: a code in a Python comment is left to
  review. Reports, ledgers, predictions, documents and configuration -- where
  the rule says a code is a bug -- are all read.
* it is under `archive/` -- frozen at a tag, not ours to correct, and 3,847
  files of the old vocabulary would drown every real finding.
* it is under a directory named `fixtures` -- the committed filings are verbatim
  source documents, and the verbatim rule forbids editing them anyway.
* its name begins with `input_` -- the text handed to an agent, committed as
  what the agent saw. Correcting a code inside one would falsify the record.
* it is `.git`, `.venv`, `__pycache__`, `.pytest_cache`, `node_modules`, or does
  not decode as UTF-8.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

try:
    from src import interpreter_pin
except ImportError:  # invoked as a plain script: python3.12 src/plain_name_check.py
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import interpreter_pin

# A word, with the separators a name carries inside it. Reported whole, so the
# line names what is written -- `D-P83`, not the `P83` that gave it away.
TOKEN = re.compile(r"(?<![A-Za-z0-9])[A-Za-z0-9]+(?:[-_.][A-Za-z0-9]+)*")

# The dashed family shape. The lookbehind refuses a run that is the tail of a
# longer dashed token, so the `BY-4` inside CC-BY-4.0 does not read as a code;
# the lookahead refuses a trailing letter or digit, so a word is never cut in
# half.
DASHED = re.compile(r"(?<![A-Za-z0-9-])[A-Z]{1,4}-[0-9]{1,4}(?![0-9A-Za-z])")

# The undashed shape, standing as a whole part of a name: B2, D15, INV11, P6A.
UNDASHED = re.compile(r"(?<![A-Za-z0-9])[A-Z]{1,4}[0-9]{1,4}[A-Za-z]?(?![A-Za-z0-9])")

# Kept vocabulary. Words, never shapes. Add one when it turns up in the
# repository; do not widen the patterns above.
KEPT_PREFIXES = ("EX-", "SHA-", "UTF-", "ISO-")
KEPT_WORDS = frozenset({"CC0"})
FISCAL_QUARTER = re.compile(r"Q[1-4]")
YEAR = re.compile(r"[A-Z]{1,4}(?:19|20)[0-9]{2}")

SKIP_DIRECTORIES = frozenset(
    {".git", ".venv", "__pycache__", ".pytest_cache", "node_modules", "archive", "fixtures"}
)
VERBATIM_INPUT_PREFIX = "input_"
SOURCE_SUFFIXES = frozenset({".py", ".sh"})

FOUND = 1
CANNOT_RUN = 2
NAME_HAS_NO_LINE = 0


def _kept(found: str) -> bool:
    """True for vocabulary that takes the shape and is not ours to rename."""
    return (
        found.startswith(KEPT_PREFIXES)
        or found in KEPT_WORDS
        or FISCAL_QUARTER.fullmatch(found) is not None
        or YEAR.fullmatch(found) is not None
    )


def _is_code(token: str) -> bool:
    return any(
        not _kept(found.group(0))
        for pattern in (DASHED, UNDASHED)
        for found in pattern.finditer(token)
    )


def codes_in(line: str) -> list[str]:
    """Every token in one line that reads as a letter-number code, in order."""
    return [token.group(0) for token in TOKEN.finditer(line) if _is_code(token.group(0))]


def skipped(path: Path) -> bool:
    """True for a file whose text is not this project's to write or correct."""
    if any(part in SKIP_DIRECTORIES for part in path.parts[:-1]):
        return True
    return path.name.startswith(VERBATIM_INPUT_PREFIX)


def _files_under(path: Path) -> list[Path]:
    if not path.is_dir():
        return [path]
    found = []
    for parent, directories, names in os.walk(path):
        directories[:] = sorted(d for d in directories if d not in SKIP_DIRECTORIES)
        found.extend(Path(parent) / name for name in sorted(names))
    return found


def _shown(path: Path) -> str:
    try:
        return str(path.relative_to(Path.cwd()))
    except ValueError:
        return str(path)


def occurrences(paths: list[Path]) -> list[str]:
    """One report line per offending occurrence: path, line number, code."""
    found = []
    for given in paths:
        for path in _files_under(given):
            if skipped(path) or not path.is_file():
                continue
            shown = _shown(path)
            found.extend(f"{shown}:{NAME_HAS_NO_LINE}: {code}" for code in codes_in(path.name))
            if path.suffix in SOURCE_SUFFIXES:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue  # not text this project wrote
            for number, line in enumerate(text.splitlines(), start=1):
                found.extend(f"{shown}:{number}: {code}" for code in codes_in(line))
    return found


def _git(*args: str) -> str:
    return subprocess.run(
        ("git", *args), capture_output=True, text=True, check=True
    ).stdout


def changed_files(baseline: str = "origin/main") -> list[Path]:
    """Everything this branch touched: the merge-base diff, staged, untracked.

    `git diff <merge-base>` compares that commit with the working tree, so a
    change that is committed, staged or neither is in the list exactly once.
    Deletions are dropped -- there is no file left to read.
    """
    root = Path(_git("rev-parse", "--show-toplevel").strip())
    base = _git("merge-base", baseline, "HEAD").strip()
    names = set(_git("diff", "--name-only", "--diff-filter=d", base).splitlines())
    names |= set(_git("ls-files", "--others", "--exclude-standard").splitlines())
    return sorted(root / name for name in names if name)


def main(argv: list[str] | None = None) -> int:
    # The pin comes first, before argument parsing and before any git call: a
    # result from an unpinned interpreter is not worth producing. It is here and
    # not at import time so the module stays importable on whatever is running.
    wrong_interpreter = interpreter_pin.enforce()
    if wrong_interpreter:
        return wrong_interpreter

    parser = argparse.ArgumentParser(
        description="Name every letter-number code in the files given, or changed."
    )
    parser.add_argument("paths", nargs="*", type=Path, help="files or directories")
    parser.add_argument(
        "--changed",
        action="store_true",
        help="check what this branch changed against the baseline instead",
    )
    parser.add_argument("--baseline", default="origin/main")
    args = parser.parse_args(argv)

    if args.changed == bool(args.paths):
        parser.error("give either --changed or one or more paths, not both and not neither")

    if args.changed:
        try:
            paths = changed_files(args.baseline)
        except subprocess.CalledProcessError:
            print(
                f"plain_name_check: baseline ref {args.baseline!r} does not resolve "
                "against this branch. Fetch it before running -- an unresolvable "
                "baseline is not a pass.",
                file=sys.stderr,
            )
            return CANNOT_RUN
    else:
        paths = args.paths
        missing = [path for path in paths if not path.exists()]
        if missing:
            # Reporting "clean" for a path that is not there is the same silence
            # a broken pattern gives, and reads the same way.
            for path in missing:
                print(f"plain_name_check: {path} is not there", file=sys.stderr)
            return CANNOT_RUN

    found = occurrences(paths)
    for line in found:
        print(line, file=sys.stderr)
    return FOUND if found else 0


if __name__ == "__main__":
    raise SystemExit(main())
