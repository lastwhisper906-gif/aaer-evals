"""The universe is a file, so adding a company is an edit and never a commit to `src/`.

Two things are judged here, and they are the two the item asked for:

* **The suite passes with `universe.json` unchanged.** That is every other test
  file, not this one -- the twelve came out of `src/fetch_fixtures.py` and into
  a file, and nothing that read them may have moved. This file asserts the
  narrower half of it: the twelve in the file are the twelve that were in the
  tuple, spelled the same way and in the same order.
* **A thirteenth row is a thirteenth company.** The test appends one and asks
  the fetcher what it plans. A module that snapshotted the list at import would
  answer twelve, which is the failure this file exists to catch: the point of
  the file is that it can be edited without restarting anything.

Where the expected values come from. The twelve tickers and their order are
read out of the commit that introduced them (`d182fcb`, 2026-09-07) and are the
same literal that stood in `src/fetch_fixtures.py`. Each CIK is the one in that
company's own committed `tests/fixtures/<ticker>/manifest.json`, which came
from EDGAR. Each SIC came from the SEC's own submissions record for that CIK --
`data.sec.gov/submissions/CIK<cik>.json`, the `sic` field -- fetched once and
written into the file. None of the three is a value this repository computed,
and none was read back out of `src/universe.py` to make this test agree with
it.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from src import universe

REPO_ROOT = Path(__file__).resolve().parent.parent

# The tuple as it stood in `src/fetch_fixtures.py` before this change, in its
# own order. Typed from the diff, not imported from the module under test.
THE_TWELVE = ("AAPL", "STX", "CSCO", "PANW", "CARR", "LFUS",
              "GNRC", "CIEN", "QCOM", "ESE", "TTMI", "NVDA")

# ticker -> (CIK from that company's committed manifest, SIC from the SEC's
# submissions record for that CIK).
FROM_THE_SOURCE = {
    "AAPL": ("0000320193", "3571"), "STX": ("0001137789", "3572"),
    "CSCO": ("0000858877", "3576"), "PANW": ("0001327567", "3577"),
    "CARR": ("0001783180", "3585"), "LFUS": ("0000889331", "3613"),
    "GNRC": ("0001474735", "3621"), "CIEN": ("0000936395", "3661"),
    "QCOM": ("0000804328", "3663"), "ESE": ("0000866706", "3669"),
    "TTMI": ("0001116942", "3672"), "NVDA": ("0001045810", "3674"),
}


def test_the_universe_file_is_at_the_repository_root() -> None:
    assert (REPO_ROOT / "universe.json").is_file(), (
        "the universe is a file at the root, and the item is not done without it"
    )


def test_the_file_holds_the_twelve_in_the_order_the_tuple_had() -> None:
    assert universe.tickers() == THE_TWELVE


def test_no_module_in_src_still_carries_the_list_as_a_literal() -> None:
    """The point of the change: the universe is not in the code any more."""
    offenders = []
    for path in sorted((REPO_ROOT / "src").glob("*.py")):
        if path.name == "universe.py":
            continue
        text = path.read_text(encoding="utf-8")
        # Three of the twelve together in one file is a copy of the list; one
        # ticker on its own is an example in a docstring.
        hits = [t for t in THE_TWELVE if f'"{t}"' in text or f"'{t}'" in text]
        if len(hits) >= 3:
            offenders.append(f"{path.name}: {', '.join(hits)}")
    assert offenders == [], (
        "a second copy of the universe lives in code, so adding a company is "
        f"still a code change: {offenders}"
    )


@pytest.mark.parametrize("ticker", THE_TWELVE)
def test_each_row_carries_the_cik_and_sic_the_source_gives(ticker: str) -> None:
    cik, sic = FROM_THE_SOURCE[ticker]
    assert universe.cik(ticker) == cik
    assert universe.sic(ticker) == sic
    manifest = json.loads(
        (REPO_ROOT / "tests" / "fixtures" / ticker / "manifest.json").read_text(
            encoding="utf-8"))
    assert manifest["cik"] == cik, (
        "the row disagrees with that company's own committed manifest"
    )


@pytest.mark.parametrize("ticker", THE_TWELVE)
def test_every_row_says_when_it_was_added(ticker: str) -> None:
    added = universe._one(ticker)["added_on"]
    assert len(added) == 10 and added[4] == added[7] == "-", added


def _universe_with_a_thirteenth(tmp_path: Path) -> Path:
    """The real file with one row appended, written where a run can read it."""
    root = tmp_path / "repo"
    root.mkdir()
    document = json.loads((REPO_ROOT / "universe.json").read_text(encoding="utf-8"))
    document["companies"].append({
        "ticker": "ZZZZ", "cik": "0000000013", "sic": "3674",
        "sic_description": "Semiconductors & Related Devices",
        "name": "A Thirteenth Company", "added_on": "2026-09-22",
    })
    path = root / "universe.json"
    path.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    return path


def test_a_thirteenth_row_is_a_thirteenth_company(tmp_path: Path) -> None:
    path = _universe_with_a_thirteenth(tmp_path)
    assert len(universe.tickers(path)) == 13
    assert universe.tickers(path)[-1] == "ZZZZ"
    assert universe.cik("ZZZZ", path) == "0000000013"


def test_the_fetcher_plans_thirteen_when_the_file_carries_thirteen(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys
) -> None:
    """The judge the item names: the file grows, and the fetcher plans for it.

    `main` is run with the network stubbed out, and what it *planned* is read
    off the companies it tried to fetch -- the plan is the thing this item
    changes, and a test that reached EDGAR would be judging the network. A
    module that read the file once at import answers twelve here, which is the
    whole failure this guards against; `TICKERS` is still the twelve in the
    same process, which is what makes that a real distinction and not a
    coincidence.
    """
    from src import fetch_fixtures

    path = _universe_with_a_thirteenth(tmp_path)
    monkeypatch.setattr(universe, "PATH", path)
    monkeypatch.setattr(
        fetch_fixtures, "cik_map",
        lambda fetcher: {t: universe.cik(t, path) for t in universe.tickers(path)})

    planned: list[str] = []

    def record(fetcher, ticker, cik, as_of, out):  # noqa: ANN001
        planned.append(ticker)
        return None, []

    monkeypatch.setattr(fetch_fixtures, "fetch_company", record)

    code = fetch_fixtures.main(["--out", str(tmp_path / "fixtures")])

    assert planned == list(THE_TWELVE) + ["ZZZZ"], (
        "the fetcher planned the import-time snapshot, so a row appended to the "
        "file is not a company until something restarts"
    )
    assert len(planned) == 13
    assert code == 0, capsys.readouterr().err
    assert fetch_fixtures.TICKERS == THE_TWELVE, (
        "the snapshot is untouched in this process, so the thirteen above came "
        "from the file and not from a mutated module global"
    )
