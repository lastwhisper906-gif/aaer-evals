"""An empty cutoff is refused by every reader that takes one.

`cutoff or cutoff_guard.default_cutoff(ticker)` was the shape at ten call sites
across eight modules, and `or` cannot tell *absent* from *empty*. That is not a
harmless conflation here. The fixture set's own as-of date is months after most
triggers, so `--cutoff ""` was not a missing cutoff that failed -- it was a
**later** cutoff that passed, and the documents it swept in are the proof. A
reader handed an empty string read filings its trigger could never have seen and
said nothing about it, which is the cutoff rule in `CLAUDE.md` broken silently.

Where the expected value comes from: `src/restatement_trace.py`, which has
refused the empty string since the day the two companyfacts readers disagreed
about what `--cutoff ""` meant, and said why in a comment at the line. The
expected behaviour is read off that sibling rather than invented here, and the
rule now lives in one function, `cutoff_guard.resolve_cutoff`, which all eleven
sites call. There is nothing to recompute: the expected result is a refusal.

Every entry point below is listed by hand, from `grep` over the modules the task
list names. The last test asserts that the list is complete -- it re-greps the
source for the shared call and fails if a site exists that no test here plants
an empty string into, so a reader added tomorrow cannot quietly not be covered.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from src import (
    clean_text,
    cutoff_guard,
    diff_periods,
    exhibits,
    extract_notes,
    extract_numbers,
    note_history,
    parse_8k,
    restatement_trace,
    split_sections,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC = REPO_ROOT / "src"

# A company on record, so the reader gets as far as the cutoff and no further.
TICKER = "AAPL"

# Every entry point that takes a cutoff, and how to call it with one.
READERS = {
    "diff_periods.extract": lambda cutoff: diff_periods.extract(TICKER, cutoff=cutoff),
    "exhibits.extract": lambda cutoff: exhibits.extract(TICKER, cutoff=cutoff),
    "exhibits.extract_on_trigger": lambda cutoff: exhibits.extract_on_trigger(
        TICKER, cutoff=cutoff
    ),
    "extract_numbers.extract": lambda cutoff: extract_numbers.extract(TICKER, cutoff=cutoff),
    "extract_notes.extract": lambda cutoff: extract_notes.extract(TICKER, cutoff=cutoff),
    "parse_8k.extract": lambda cutoff: parse_8k.extract(TICKER, cutoff=cutoff),
    "note_history.history": lambda cutoff: note_history.history(TICKER, cutoff=cutoff),
    "split_sections.extract": lambda cutoff: split_sections.extract(
        TICKER, "10-K", "mdna", cutoff=cutoff
    ),
    "split_sections.risk_factors": lambda cutoff: split_sections.risk_factors(
        TICKER, cutoff=cutoff
    ),
    "restatement_trace.scan": lambda cutoff: restatement_trace.scan(TICKER, cutoff=cutoff),
}

# The strings that are not a date and are not an absent cutoff either.
NOT_A_CUTOFF = ("", "   ", "\t")


@pytest.mark.parametrize("name", sorted(READERS))
@pytest.mark.parametrize("given", NOT_A_CUTOFF)
def test_an_empty_cutoff_is_refused_by_every_reader(name: str, given: str) -> None:
    with pytest.raises(cutoff_guard.CutoffGuardError, match="cutoff is missing"):
        READERS[name](given)


@pytest.mark.parametrize("name", sorted(READERS))
def test_a_cutoff_that_is_not_a_date_is_refused_rather_than_guessed(name: str) -> None:
    with pytest.raises(cutoff_guard.CutoffGuardError, match="not an ISO date"):
        READERS[name]("last Tuesday")


def test_the_command_line_refuses_an_empty_cutoff(tmp_path: Path, capsys) -> None:
    """`--cutoff ""` is the shape a caller actually types.

    A command line does not raise at its caller, it exits: `clean_text.main`
    catches `CutoffGuardError`, prints it and returns `BAD_INPUT`. So the
    refusal is read off the exit code, the message, and the output file that was
    never written -- an empty cutoff that swept documents in would leave one.
    """
    out = tmp_path / "out.json"
    code = clean_text.main(["--ticker", TICKER, "--cutoff", "", "--out", str(out)])

    assert code == clean_text.BAD_INPUT
    assert code != 0, "a refused cutoff that exits zero is a pass"
    assert "cutoff is missing" in capsys.readouterr().err
    assert not out.exists(), "a refused run wrote a reading anyway"


def test_an_absent_cutoff_still_means_the_default() -> None:
    """The conflation is fixed in one direction only; the other still works."""
    default = cutoff_guard.default_cutoff(TICKER)
    assert cutoff_guard.resolve_cutoff(None, TICKER) == default


def test_a_date_given_is_the_date_used() -> None:
    import datetime as dt

    assert cutoff_guard.resolve_cutoff("2024-01-31", TICKER) == dt.date(2024, 1, 31)
    assert cutoff_guard.resolve_cutoff(dt.date(2024, 1, 31), TICKER) == dt.date(2024, 1, 31)


def _called_name(node: ast.expr) -> str:
    """`default_cutoff` out of either `default_cutoff` or `mod.default_cutoff`."""
    if isinstance(node, ast.Attribute):
        return node.attr
    if isinstance(node, ast.Name):
        return node.id
    return ""


def test_the_rule_is_written_once_and_every_site_calls_it() -> None:
    """The ten sites had ten copies of `cutoff or default`. They have none now.

    Read off the syntax tree rather than off the text: `resolve_cutoff`'s own
    docstring quotes the old shape on purpose, to say what it replaced, and a
    grep cannot tell that prose from a line that runs. An `or` whose right side
    calls `default_cutoff` is the defect itself, in any spelling and across any
    line break, and it does not exist in a docstring.
    """
    stale = []
    for path in sorted(SRC.glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(node, ast.BoolOp) or not isinstance(node.op, ast.Or):
                continue
            for value in node.values:
                if isinstance(value, ast.Call) and _called_name(value.func) == "default_cutoff":
                    stale.append(f"{path.name}:{node.lineno}")
    assert stale == [], f"a call site still reads the empty string as the default: {stale}"


def test_every_call_site_in_the_source_has_a_reader_in_this_file() -> None:
    """A reader added tomorrow cannot quietly go uncovered.

    The set on the left is re-greped out of `src/` on every run; the set on the
    right is the table above. A new module calling `resolve_cutoff` with no
    entry here turns this red, which is the only way a list written by hand
    stays honest.
    """
    calling = {
        path.stem
        for path in sorted(SRC.glob("*.py"))
        if "cutoff_guard.resolve_cutoff(" in path.read_text(encoding="utf-8")
        and path.stem != "cutoff_guard"
    }
    covered = {name.split(".")[0] for name in READERS}
    # `clean_text` is reached through its command line, which has its own test.
    covered.add("clean_text")
    assert calling == covered, f"not planted into: {sorted(calling - covered)}"


def test_the_shared_rule_is_the_one_the_sibling_wrote() -> None:
    """`src/restatement_trace.py` is where the expected behaviour comes from."""
    source = (SRC / "restatement_trace.py").read_text(encoding="utf-8")
    assert "cutoff_guard.resolve_cutoff(" in source
    assert "cutoff or cutoff_guard.default_cutoff" not in source
