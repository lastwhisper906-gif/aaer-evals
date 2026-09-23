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
from EDGAR. Each SIC, SIC description and name is read here out of the SEC's
submissions header for that CIK, committed at
`tests/fixtures/universe/<ticker>.json` with the sha256 of the document as
served. Each added-on date is that company's manifest `as_of`: the twelve
entered with the fixture set pinned to 2026-09-01, which the item's own
acceptance line names. None of them is typed into this file, and none was read
back out of `src/universe.py` to make this test agree with it.
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

HEADERS = REPO_ROOT / "tests" / "fixtures" / "universe"


def _manifest(ticker: str) -> dict:
    return json.loads((REPO_ROOT / "tests" / "fixtures" / ticker / "manifest.json")
                      .read_text(encoding="utf-8"))


def _header(ticker: str) -> dict:
    return json.loads((HEADERS / f"{ticker}.json").read_text(encoding="utf-8"))


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
def test_each_rows_cik_is_the_one_in_that_companys_manifest(ticker: str) -> None:
    assert universe.cik(ticker) == _manifest(ticker)["cik"], (
        "the row disagrees with that company's own committed manifest"
    )


def test_every_row_has_a_committed_sec_header_behind_it() -> None:
    """A row with nothing committed behind its SIC is a typed SIC."""
    missing = [t for t in universe.tickers() if not (HEADERS / f"{t}.json").is_file()]
    assert missing == [], (
        f"no SEC header at tests/fixtures/universe/ for {missing}; "
        "run python3.12 -m src.fetch_universe_source"
    )


@pytest.mark.parametrize("ticker", THE_TWELVE)
def test_each_rows_sic_is_the_one_the_sec_header_gives(ticker: str) -> None:
    record = _header(ticker)
    header = record["header"]
    row = universe._one(ticker)
    assert record["url"].endswith(f"CIK{row['cik']}.json")
    assert f"{int(header['cik']):010d}" == row["cik"]
    assert ticker in header["tickers"]
    assert row["sic"] == header["sic"]
    assert row["sic_description"] == header["sicDescription"]
    assert row["name"] == header["name"]
    assert len(record["served_sha256"]) == 64 and record["served_bytes"] > 0
    assert "filings" not in header, "the header must not carry post-cutoff filings"


@pytest.mark.parametrize("ticker", THE_TWELVE)
def test_each_row_was_added_on_its_fixture_sets_as_of(ticker: str) -> None:
    assert universe._one(ticker)["added_on"] == _manifest(ticker)["as_of"]


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

    planned: list[str] = []
    ciks: dict[str, str] = {}

    def record(fetcher, ticker, cik, as_of, out):  # noqa: ANN001
        planned.append(ticker)
        ciks[ticker] = cik
        return None, []

    monkeypatch.setattr(fetch_fixtures, "fetch_company", record)

    code = fetch_fixtures.main(["--out", str(tmp_path / "fixtures")])

    assert planned == list(THE_TWELVE) + ["ZZZZ"], (
        "the fetcher planned the import-time snapshot, so a row appended to the "
        "file is not a company until something restarts"
    )
    assert len(planned) == 13
    # The CIK the fetcher uses is the file's. ZZZZ is in no EDGAR ticker map,
    # so a fetcher that still resolved CIKs there would not have planned it.
    assert ciks["ZZZZ"] == "0000000013"
    assert all(ciks[t] == _manifest(t)["cik"] for t in THE_TWELVE)
    assert code == 0, capsys.readouterr().err
    assert fetch_fixtures.TICKERS == THE_TWELVE, (
        "the snapshot is untouched in this process, so the thirteen above came "
        "from the file and not from a mutated module global"
    )


def test_the_fetcher_refuses_a_ticker_the_file_does_not_carry(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys
) -> None:
    from src import fetch_fixtures

    def unreachable(*args, **kwargs):  # noqa: ANN002, ANN003
        raise AssertionError("a ticker outside the universe reached EDGAR")

    monkeypatch.setattr(fetch_fixtures, "fetch_company", unreachable)
    code = fetch_fixtures.main(["--ticker", "NOTINFILE",
                                "--out", str(tmp_path / "fixtures")])
    assert code == fetch_fixtures.FETCH_FAILED
    assert "NOTINFILE is not in the universe" in capsys.readouterr().err


# --- a malformed file is refused, not read ------------------------------------

GOOD = {"ticker": "ZZZZ", "cik": "0000000013", "sic": "3674", "added_on": "2026-09-22"}


def _write(tmp_path: Path, companies) -> Path:  # noqa: ANN001
    path = tmp_path / "universe.json"
    path.write_text(json.dumps({"companies": companies}), encoding="utf-8")
    return path


@pytest.mark.parametrize("key", ["ticker", "cik", "sic", "added_on"])
def test_a_row_missing_a_field_is_refused(tmp_path: Path, key: str) -> None:
    row = {k: v for k, v in GOOD.items() if k != key}
    with pytest.raises(universe.UniverseError, match=f"{key} is missing"):
        universe.rows(_write(tmp_path, [row]))


@pytest.mark.parametrize("key", ["ticker", "cik", "sic", "added_on"])
def test_a_null_field_is_refused_and_not_read_as_the_string_none(
        tmp_path: Path, key: str) -> None:
    with pytest.raises(universe.UniverseError, match=f"{key} is None"):
        universe.rows(_write(tmp_path, [{**GOOD, key: None}]))


@pytest.mark.parametrize("key", ["ticker", "cik", "sic", "added_on"])
def test_an_empty_field_is_refused(tmp_path: Path, key: str) -> None:
    with pytest.raises(universe.UniverseError, match=f"{key} is empty"):
        universe.rows(_write(tmp_path, [{**GOOD, key: "  "}]))


def test_a_number_where_a_string_belongs_is_refused(tmp_path: Path) -> None:
    # 320193 as a JSON number has lost the leading zeroes the CIK is written with.
    with pytest.raises(universe.UniverseError, match="not a string"):
        universe.rows(_write(tmp_path, [{**GOOD, "cik": 320193}]))


@pytest.mark.parametrize("field,value,says", [
    ("cik", "320193", "not ten digits"),
    ("sic", "36741", "not four digits"),
    ("added_on", "22 Sept 2026", "not a YYYY-MM-DD date"),
])
def test_a_field_that_is_not_what_it_names_is_refused(
        tmp_path: Path, field: str, value: str, says: str) -> None:
    with pytest.raises(universe.UniverseError, match=says):
        universe.rows(_write(tmp_path, [{**GOOD, field: value}]))


def test_a_duplicate_ticker_is_refused_whatever_its_case(tmp_path: Path) -> None:
    with pytest.raises(universe.UniverseError, match="appears twice"):
        universe.rows(_write(tmp_path, [GOOD, {**GOOD, "ticker": "zzzz"}]))


def test_an_empty_universe_is_refused(tmp_path: Path) -> None:
    with pytest.raises(universe.UniverseError, match="lists no companies"):
        universe.rows(_write(tmp_path, []))


def test_a_row_that_is_not_an_object_is_refused(tmp_path: Path) -> None:
    with pytest.raises(universe.UniverseError, match="is not an object"):
        universe.rows(_write(tmp_path, ["ZZZZ"]))


def test_a_file_with_no_companies_list_is_refused(tmp_path: Path) -> None:
    path = tmp_path / "universe.json"
    path.write_text(json.dumps({"companies": {"ZZZZ": GOOD}}), encoding="utf-8")
    with pytest.raises(universe.UniverseError, match="no `companies` list"):
        universe.rows(path)
