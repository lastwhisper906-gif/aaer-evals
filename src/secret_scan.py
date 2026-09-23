"""Name a credential that reached a file in this tree.

`src/prices/` reads three credentials and every one of them comes from outside
the repository: `$TIINGO_TOKEN`, `$EODHD_TOKEN`, and for CRSP the `~/.pgpass`
the `wrds` package already owns. Nothing here is supposed to hold one. This is
the check that says so out loud, because "we do not commit tokens" is a
sentence and this is a gate.

It is a sibling of `src/plain_name_check.py` and works the same way: the same
`--changed` list, the same `path:line:` report shape, the same exit codes. The
one place it deliberately differs is that it **reads source files**. The
plain-name check skips `.py` and `.sh` because code quotes other people's
vocabulary; a token in a Python file is not quoted vocabulary, it is the thing
this check exists for, and skipping source would leave the likeliest file
unread.

Three things it names
---------------------

1. **The credential itself.** For every variable in `CREDENTIAL_VARIABLES` that
   is set in this shell, the literal value is searched for, byte for byte, in
   every changed file. This is the only exact check here and it is the important
   one: it cannot be fooled by a shape it did not expect, and it fires on a
   token pasted into a note as readily as on one assigned in code. It can only
   run where the variable is set -- so a machine with no token cannot catch a
   token, and the two heuristics below are what stand there instead.

2. **A credential assigned to a name that says what it is.** `token = "..."`,
   `api_key: "..."`, `password = '...'`, with a literal of at least
   `SHORTEST_CREDENTIAL` characters. An environment lookup is not a literal, and
   a literal that is an environment variable's own name -- `"TIINGO_TOKEN"`,
   capitals and underscores -- is a name and not a value.

3. **A credential in a query string.** `?api_token=<literal>`, which is how
   EODHD's own interface takes one and therefore how a pasted command line
   carries one.

What it does not do
-------------------

It does not look for high entropy. An entropy threshold over a repository that
carries hashes, accession numbers and base-sixteen digests is a check that
either fires constantly or is tuned until it fires never, and a check that has
been tuned until it is quiet is the failure mode `docs/HOW_WE_WORK.md` names:
a verification layer that has never been shown to catch a defect is not known
to work. The three rules above fire on what a credential
*is called* and on what a credential *is*, and they are extended by adding a
variable name when one turns up, never by widening a pattern.

    python3.12 -m src.secret_scan --changed
    python3.12 src/secret_scan.py src docs

Exit 0 and no output when clean, 1 when it found one, 2 when it could not run,
3 on the wrong interpreter. One line per occurrence on stderr, in the shape grep
prints -- and **the value is never printed**, only its variable or its shape,
because a check that reports a leaked credential by quoting it has copied it
into one more log.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

try:
    from src import interpreter_pin, plain_name_check
except ImportError:  # invoked as a plain script
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import interpreter_pin, plain_name_check

FOUND = 1
CANNOT_RUN = 2

# The variables the price backends read. One line each, added when a backend is
# added -- this list is the check, and a backend whose credential is not on it
# is a backend nothing watches.
CREDENTIAL_VARIABLES = ("TIINGO_TOKEN", "EODHD_TOKEN")

# Shorter than this and a literal is not a credential; a real Tiingo token is
# forty characters and an EODHD one is twenty.
SHORTEST_CREDENTIAL = 16

# A name that says the value beside it is a credential.
NAMES = r"(?:api[_-]?token|api[_-]?key|access[_-]?token|auth[_-]?token|token|secret|password|passwd|apikey)"

ASSIGNED = re.compile(
    rf"""{NAMES}            # the name
         ['"]?               # its own closing quote, where the name is a key
         \s*[:=]\s*         # assigned, in code or in configuration
         (['"])             # opened
         (?P<value>[^'"\s]{{{SHORTEST_CREDENTIAL},}})
         \1                 # closed with the same quote
    """,
    re.IGNORECASE | re.VERBOSE,
)

IN_A_QUERY_STRING = re.compile(
    rf"[?&]{NAMES}=(?P<value>[^&\s'\"<>]{{{SHORTEST_CREDENTIAL},}})",
    re.IGNORECASE,
)

# A literal that is a variable's own name, not its value: capitals, digits and
# underscores only. `TOKEN_VARIABLE = "TIINGO_TOKEN"` names a variable.
A_VARIABLE_NAME = re.compile(r"^[A-Z][A-Z0-9_]*$")

# What a placeholder looks like when somebody writes the shape without the
# secret. Words, never shapes -- the same rule `src/plain_name_check.py` keeps.
PLACEHOLDERS = (
    "your",
    "xxx",
    "...",
    "example",
    "placeholder",
    "changeme",
    "redacted",
    "demo",
    "$",
    "{",
    "<",
    "os.environ",
    "getenv",
)

SKIP_DIRECTORIES = frozenset(
    {".git", ".venv", "__pycache__", ".pytest_cache", "node_modules", "archive", ".lens"}
)


def _is_placeholder(value: str) -> bool:
    lowered = value.lower()
    return any(mark in lowered for mark in PLACEHOLDERS) or bool(A_VARIABLE_NAME.match(value))


def credentials_in_the_environment(
    environ: dict[str, str] | None = None,
) -> dict[str, str]:
    """The credential values this shell actually holds, by variable name."""
    source = os.environ if environ is None else environ
    found = {}
    for name in CREDENTIAL_VARIABLES:
        value = source.get(name, "").strip()
        if len(value) >= SHORTEST_CREDENTIAL and not _is_placeholder(value):
            found[name] = value
    return found


def findings_in(line: str, secrets: dict[str, str]) -> list[str]:
    """What this one line gives away, named by variable or by shape.

    The value is never in the returned text. A report that quotes the credential
    it found has written it down one more time.
    """
    found = []
    for name, value in secrets.items():
        if value in line:
            found.append(f"the value of ${name}")
    for pattern, shape in ((ASSIGNED, "assigned to a credential name"),
                           (IN_A_QUERY_STRING, "in a query string")):
        for match in pattern.finditer(line):
            if not _is_placeholder(match.group("value")):
                found.append(f"a credential {shape}")
    return found


def skipped(path: Path) -> bool:
    return any(part in SKIP_DIRECTORIES for part in path.parts)


def occurrences(paths: list[Path], secrets: dict[str, str]) -> list[str]:
    """One report line per occurrence: path, line number, what it is."""
    found = []
    here = Path.cwd()
    for given in paths:
        for path in _files_under(given):
            if skipped(path) or not path.is_file():
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            shown = plain_name_check._shown(path, here)
            for number, line in enumerate(text.splitlines(), start=1):
                found.extend(f"{shown}:{number}: {what}" for what in findings_in(line, secrets))
    return found


def _files_under(path: Path) -> list[Path]:
    if not path.is_dir():
        return [path]
    found = []
    for parent, directories, names in os.walk(path):
        directories[:] = sorted(d for d in directories if d not in SKIP_DIRECTORIES)
        found.extend(Path(parent) / name for name in sorted(names))
    return found


def main(argv: list[str] | None = None) -> int:
    wrong_interpreter = interpreter_pin.enforce()
    if wrong_interpreter:
        return wrong_interpreter

    parser = argparse.ArgumentParser(
        description="Name a credential that reached a file in this tree."
    )
    parser.add_argument("paths", nargs="*", type=Path)
    parser.add_argument("--changed", action="store_true")
    parser.add_argument("--baseline", default="origin/main")
    args = parser.parse_args(argv)

    if args.changed == bool(args.paths):
        parser.error("give either --changed or one or more paths, not both and not neither")

    if args.changed:
        import subprocess

        try:
            paths = plain_name_check.changed_files(args.baseline)
        except subprocess.CalledProcessError:
            print(
                f"secret_scan: baseline ref {args.baseline!r} does not resolve against "
                "this branch. An unresolvable baseline is not a pass.",
                file=sys.stderr,
            )
            return CANNOT_RUN
    else:
        paths = args.paths

    missing = [path for path in paths if not path.exists()]
    if missing:
        for path in missing:
            print(f"secret_scan: {path} is not there", file=sys.stderr)
        return CANNOT_RUN

    found = occurrences(paths, credentials_in_the_environment())
    for line in found:
        print(line, file=sys.stderr)
    return FOUND if found else 0


if __name__ == "__main__":
    raise SystemExit(main())
