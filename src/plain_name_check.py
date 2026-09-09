"""Name every letter-number code in the files this branch changed.

`CLAUDE.md` says: plain names, no letter-number codes, machine keys are readable
slugs. `docs/HOW_WE_WORK.md` says a code in a report, a ledger, an issue title, a
filename or a commit message is a bug. The rule was written because the archived
project ran on codes -- a two- or three-letter tag bound to a serial number, one
family per kind of thing, a dozen families in the end -- and a reader had to hold
a lookup table in their head to read a sentence. Nothing enforced it, so this
check does.

    python3.12 -m src.plain_name_check --changed
    python3.12 -m src.plain_name_check docs src/trends.py

One line per offending occurrence, on stderr, in the shape grep prints:
`path:line: CODE`. Exit 0 and no output when clean, 1 when it found any, 2 when
the baseline ref does not resolve, 3 on the wrong interpreter.

Standard library only, and it stays that way. The post-write hook in
`.claude/settings.json` runs it under bare `python3.12`, which on this machine
has no pytest and no site-packages for this project, so one third-party import
makes the hook inert -- and a hook that cannot run reports green by saying
nothing, which is the exact failure this file exists to end.

Where the line is
-----------------

A letter-number code is an **identifier**: a short uppercase tag, a dash, and a
serial number, standing in for a name, so that people refer to the thing by the
code instead of by what it is. That is the shape every family the old project
invented took, whether the tag was one letter or three and whether the serial was
padded with zeros or not. So the check looks for exactly that: one to four
uppercase letters, a dash, digits, standing on its own.

Most of the vocabulary this repository has to keep is safe on shape alone,
because it is not that shape:

* EDGAR periodic and current report names put the digits first -- 10-K, 10-Q,
  8-K -- and end on a letter, so they never match.
* Item numbers are digits and dots with no dash at all: item 2.02, 4.01, 4.02,
  1.01, 5.02. So are Item 1A and Item 7A, which end on a letter.
* Exhibit 21 and Exhibit 10 are a word and a number with a space between them.
* XBRL and us-gaap tag names are letters and colons -- `us-gaap:Revenues` --
  with no digits behind a dash.
* Accession numbers and dates begin with digits: 0000320193-26-000001,
  2026-09-09.
* Version and standard strings mostly have no dash: Python 3.12, v0.1, sha256,
  ISO 8601, rule 10-b5 (digits first again).
* Ticker symbols are letters. Paths and file names are lowercase here, and the
  check reads uppercase tags only -- `harness/cycle-020` and
  `aapl-20250927.htm` are names, not codes, and both stay silent.

Four pieces of kept vocabulary do take the shape, and they are exempted **as
words, not as shapes**: `EX-` (exhibit names, EX-99.1 and its siblings, which
`src/fetch_fixtures.py` matches on), `SHA-`, `UTF-` and `ISO-` (hash, encoding
and character-set standards). The list grows by adding a word when one actually
turns up, never by widening the pattern. A shape carve-out is how a check becomes
a quiet no-op: the tempting one here is "let a single letter and one digit
through, those are EDGAR registration forms" -- and the archived project numbered
one of its own families with that same single letter and that same shape, so the
carve-out would have let a whole family through to buy silence on form names this
repository never reads. It reads periodic reports, current reports and exhibits.

What it deliberately does not catch
-----------------------------------

The undashed form. The old project also numbered documents and tables that way,
a letter or two run straight into digits, and those exist. They are left to
review, because the tokens that shape produces are overwhelmingly legitimate --
fiscal years, quarters, hash and encoding names -- and a check that reports those
on every write is one that gets turned off within a week. Stated here rather than
hidden: this check is the floor, not the ceiling.

Lowercase tags, for the same reason. Lowercase letters, a dash and digits is the
shape of file names, branch names, model names and readable slugs, which is what
the rule asks for rather than what it forbids.

Tags longer than four letters. Past four the tag has stopped abbreviating and
started spelling: ALPHA and COVID read as words, and the families the old project
invented were one to four letters, never more. Widening the tag buys a certain
false positive against a hypothetical code.

Which files it reads
--------------------

Only text this project wrote. It skips, silently:

* `archive/` -- frozen at a tag, not ours to correct, and 3,847 files of the old
  vocabulary would drown every real finding.
* any directory named `fixtures` -- text quoted verbatim from somewhere else. The
  committed filings are the bulk of it: a single one of them carries thousands of
  `c-1` style HTML class attributes, and the verbatim rule forbids editing them
  anyway. The list of the old project's code families that this check's own test
  plants is quoted there too, for the same reason and one more -- the hook reads
  everything a branch changed, so a test carrying those codes as literals would
  make the hook report that test on every write, for good.
* any file whose name begins with `input_` -- the text and data handed to an
  agent, committed as what the agent saw. Correcting a code inside one would
  falsify the record.
* `.git`, `.venv`, `__pycache__`, `.pytest_cache`, `node_modules`, and anything
  that does not decode as UTF-8.

Reports, ledgers, predictions, code, documents and configuration are all read.

Neither this file nor its test names a code of its own, on purpose: the hook runs
on every write over everything a branch changed, and a check that reports itself
every time it is edited is a check somebody turns off. Both are asserted by tests
rather than left to care.
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

# One to four uppercase letters, a dash, digits. The lookbehind refuses a run
# that is itself the tail of a longer dashed token, so the licence name
# CC-BY-4.0 and the second half of ISO-8859-1 do not read as codes. The
# lookahead refuses a trailing letter or digit, so a word is never cut in half.
CODE = re.compile(r"(?<![A-Za-z0-9-])[A-Z]{1,4}-[0-9]+(?![0-9A-Za-z])")

# Kept vocabulary that happens to take the shape. Words, never shapes. Add one
# when it turns up in the repository; do not widen CODE.
KEPT = ("EX-", "SHA-", "UTF-", "ISO-")

SKIP_DIRECTORIES = frozenset(
    {".git", ".venv", "__pycache__", ".pytest_cache", "node_modules", "archive", "fixtures"}
)
VERBATIM_INPUT_PREFIX = "input_"

FOUND = 1
UNRESOLVABLE_BASELINE = 2


def _git(*args: str) -> str:
    return subprocess.run(
        ("git", *args), capture_output=True, text=True, check=True
    ).stdout


def codes_in(line: str) -> list[str]:
    """Every letter-number code in one line, in the order it reads."""
    return [m.group(0) for m in CODE.finditer(line) if not m.group(0).startswith(KEPT)]


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
            try:
                text = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue  # not text this project wrote
            for number, line in enumerate(text.splitlines(), start=1):
                for code in codes_in(line):
                    found.append(f"{_shown(path)}:{number}: {code}")
    return found


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
            return UNRESOLVABLE_BASELINE
    else:
        paths = args.paths

    found = occurrences(paths)
    for line in found:
        print(line, file=sys.stderr)
    return FOUND if found else 0


if __name__ == "__main__":
    # The pin comes first, as in src/append_check.py: a result from an unpinned
    # interpreter is not worth producing. It sits here rather than inside main()
    # so main() stays importable and testable on whatever runs the tests.
    raise SystemExit(interpreter_pin.enforce() or main())
