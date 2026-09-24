"""Detect filing reads the universe file and makes one lookup per row.

`docs/HOW_WE_WORK.md` §3 gives the stage "daily: new filings for the twelve,
from the EDGAR submissions index" and "passes when 12 of 12 lookups succeed".
The judge hands the stage a stand-in fetcher answering planted submissions rows
for every company in a planted universe file.

Where the expected values come from: the planted rows below, read by hand. Each
company's latest 10-K, 10-Q and 8-K carrying item 2.02 is written out as a
literal next to the rows it was read from, and the lookup count is the number of
rows in the planted universe. Nothing here was produced by running the stage.
"""

from __future__ import annotations

import json
import urllib.error

import pytest

from src import detect_filing


def _company(ticker: str, cik: str) -> dict:
    return {"ticker": ticker, "cik": cik, "sic": "3571", "added_on": "2026-09-01"}


def _universe(tmp_path, companies) -> object:
    path = tmp_path / "universe.json"
    path.write_text(json.dumps({"companies": companies}), encoding="utf-8")
    return path


def _index(rows: list[tuple[str, str, str, str]]) -> dict:
    """EDGAR's parallel arrays, as `data.sec.gov/submissions` serves them.

    Each planted row is (accession, filing date, form, items).
    """
    return {"filings": {"recent": {
        "accessionNumber": [r[0] for r in rows],
        "filingDate": [r[1] for r in rows],
        "reportDate": ["" for _ in rows],
        "form": [r[2] for r in rows],
        "items": [r[3] for r in rows],
        "primaryDocument": [f"{r[0]}.htm" for r in rows],
        "primaryDocDescription": ["" for _ in rows],
    }}}


# Not in date order: the first company's older 10-Q and older 8-K come first, so
# "latest" has to be read by date and not by position.
PLANTED = {
    "0000000001": [
        ("0000000001-26-000005", "2026-05-01", "10-Q", ""),
        ("0000000001-26-000004", "2026-04-30", "8-K", "2.02"),
        ("0000000001-26-000009", "2026-09-20", "8-K", "5.02"),
        ("0000000001-26-000008", "2026-09-10", "10-Q", ""),
        ("0000000001-26-000007", "2026-08-01", "8-K", "2.02,9.01"),
        ("0000000001-26-000010", "2026-09-21", "10-K/A", ""),
        ("0000000001-25-000006", "2025-11-01", "10-K", ""),
    ],
    "0000000002": [
        ("0000000002-26-000003", "2026-09-22", "10-K", ""),
        ("0000000002-26-000002", "2026-09-22", "8-K", "2.02,9.01"),
        ("0000000002-26-000001", "2026-06-01", "10-Q", ""),
    ],
    "0000000003": [
        ("0000000003-26-000002", "2026-03-01", "10-Q", ""),
        ("0000000003-26-000001", "2026-02-01", "8-K", "12.02"),
    ],
}

# Read off PLANTED by hand.
EXPECTED_LATEST = {
    "AAA": {"10-K": "0000000001-25-000006", "10-Q": "0000000001-26-000008",
            "8-K item 2.02": "0000000001-26-000007"},
    "BBB": {"10-K": "0000000002-26-000003", "10-Q": "0000000002-26-000001",
            "8-K item 2.02": "0000000002-26-000002"},
    # No 10-K, and "12.02" is not item 2.02.
    "CCC": {"10-K": None, "10-Q": "0000000003-26-000002", "8-K item 2.02": None},
}


class StandIn:
    """Answers the planted index for each CIK and records every URL asked."""

    def __init__(self, failing: tuple[str, ...] = ()) -> None:
        self.asked: list[str] = []
        self.failing = failing

    def get_json(self, url: str):
        self.asked.append(url)
        for cik, rows in PLANTED.items():
            if f"CIK{cik}.json" in url:
                if cik in self.failing:
                    raise urllib.error.HTTPError(url, 403, "Forbidden", {}, None)
                return _index(rows)
        raise AssertionError(f"asked for a URL nothing planted: {url}")


@pytest.fixture
def three(tmp_path):
    return _universe(tmp_path, [_company("AAA", "0000000001"),
                                _company("BBB", "0000000002"),
                                _company("CCC", "0000000003")])


def test_one_lookup_per_universe_row(three, tmp_path):
    fetcher = StandIn()
    found = detect_filing.detect(fetcher, since="2026-09-01", universe_path=three,
                                 runs_root=tmp_path / "runs")
    assert fetcher.asked == [
        "https://data.sec.gov/submissions/CIK0000000001.json",
        "https://data.sec.gov/submissions/CIK0000000002.json",
        "https://data.sec.gov/submissions/CIK0000000003.json",
    ]
    assert found["lookups"] == {"succeeded": 3, "of": 3}
    assert found["passed"] is True
    assert [c["ticker"] for c in found["companies"]] == ["AAA", "BBB", "CCC"]


def test_the_latest_filing_per_form_is_read_off_the_rows(three, tmp_path):
    found = detect_filing.detect(StandIn(), since="2026-09-01", universe_path=three,
                                 runs_root=tmp_path / "runs")
    got = {c["ticker"]: {k: (v["accession"] if v else None)
                         for k, v in c["latest"].items()}
           for c in found["companies"]}
    assert got == EXPECTED_LATEST


def test_a_thirteenth_row_is_a_thirteenth_lookup(tmp_path):
    # Thirteen distinct tickers, X to XXXXXXXXXXXXX, all on one planted CIK.
    rows = [_company("X" * (n + 1), "0000000001") for n in range(13)]
    path = _universe(tmp_path, rows)
    fetcher = StandIn()
    found = detect_filing.detect(fetcher, since="2026-09-01", universe_path=path,
                                 runs_root=tmp_path / "runs")
    assert len(fetcher.asked) == 13
    assert found["lookups"] == {"succeeded": 13, "of": 13}


def test_a_failed_lookup_is_named_and_fails_the_stage(three, tmp_path):
    found = detect_filing.detect(StandIn(failing=("0000000002",)), since="2026-09-01",
                                 universe_path=three, runs_root=tmp_path / "runs")
    assert found["lookups"] == {"succeeded": 2, "of": 3}
    assert found["passed"] is False
    failed = [c for c in found["companies"] if c["lookup"] == "failed"]
    assert [c["ticker"] for c in failed] == ["BBB"]
    assert "403" in failed[0]["reason"]
    # A company that did not answer is not a company with no filings.
    assert failed[0]["latest"] is None


def test_new_is_on_or_after_since_and_not_already_run(three, tmp_path):
    runs = tmp_path / "runs"
    (runs / "BBB" / "0000000002-26-000003").mkdir(parents=True)
    found = detect_filing.detect(StandIn(), since="2026-09-10", universe_path=three,
                                 runs_root=runs)
    new = {c["ticker"]: [(e["kind"], e["accession"]) for e in c["new"]]
           for c in found["companies"]}
    # AAA: the 10-Q of 2026-09-10 is on the day, so new; the 8-K of 09-20 is
    # item 5.02 and the 10-K/A is an amendment, so neither is one of the three.
    # BBB: the 10-K has a run already; the 8-K 2.02 of the same day does not.
    assert new == {"AAA": [("10-Q", "0000000001-26-000008")],
                   "BBB": [("8-K item 2.02", "0000000002-26-000002")],
                   "CCC": []}


def test_main_exits_two_when_a_lookup_fails(three, tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(detect_filing.fetch_fixtures, "Fetcher",
                        lambda _agent: StandIn(failing=("0000000003",)))
    out = tmp_path / "detect.json"
    code = detect_filing.main(["--since", "2026-09-01", "--universe", str(three),
                               "--runs", str(tmp_path / "runs"), "--out", str(out)])
    assert code == detect_filing.LOOKUP_FAILED
    assert json.loads(out.read_text())["lookups"] == {"succeeded": 2, "of": 3}
    assert "2 of 3 lookups succeeded" in capsys.readouterr().err


def test_main_exits_zero_when_every_lookup_succeeds(three, tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(detect_filing.fetch_fixtures, "Fetcher", lambda _agent: StandIn())
    code = detect_filing.main(["--since", "2026-09-01", "--universe", str(three),
                               "--runs", str(tmp_path / "runs")])
    assert code == 0
    assert "3 of 3 lookups succeeded" in capsys.readouterr().err
