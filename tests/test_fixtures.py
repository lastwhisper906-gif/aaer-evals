"""The fixtures are records: what is on disk must still be what EDGAR served.

Every acceptance test in the parser build reads these files, so a fixture that
drifts silently would move the answer key under the parsers. The manifest holds
the sha256 of the raw bytes; this checks it, and checks that all twelve
companies still carry the six documents the parsers are judged against.
"""

from __future__ import annotations

import gzip
import hashlib
import json
from pathlib import Path

import pytest

from src.fetch_fixtures import TICKERS

FIXTURES = Path(__file__).resolve().parent / "fixtures"

REQUIRED_ROLES = {
    ("10-K", "primary_html"), ("10-K", "xbrl_instance"),
    ("10-Q", "primary_html"), ("10-Q", "xbrl_instance"),
    ("8-K", "primary_html"), ("8-K", "exhibit_99_1"),
    # The submissions index: an 8-K's item codes are stated nowhere else.
    ("submissions", "submissions_index"),
}


def manifest(ticker: str) -> dict:
    return json.loads((FIXTURES / ticker / "manifest.json").read_text())


def raw_bytes(ticker: str, entry: dict) -> bytes:
    path = FIXTURES / ticker / entry["path"]
    data = path.read_bytes()
    return gzip.decompress(data) if entry["stored"] == "gzip" else data


@pytest.mark.parametrize("ticker", TICKERS)
def test_every_company_has_the_six_documents(ticker):
    have = {(e["form"], e["role"]) for e in manifest(ticker)["documents"]}
    assert REQUIRED_ROLES <= have, f"{ticker} is missing {sorted(REQUIRED_ROLES - have)}"


@pytest.mark.parametrize("ticker", TICKERS)
def test_the_bytes_on_disk_are_the_bytes_edgar_served(ticker):
    for entry in manifest(ticker)["documents"]:
        data = raw_bytes(ticker, entry)
        assert len(data) == entry["bytes"], f"{ticker} {entry['path']}: length changed"
        assert hashlib.sha256(data).hexdigest() == entry["sha256"], \
            f"{ticker} {entry['path']}: content changed"


@pytest.mark.parametrize("ticker", TICKERS)
def test_no_fixture_was_filed_after_the_cutoff(ticker):
    data = manifest(ticker)
    for entry in data["documents"]:
        assert entry["filing_date"] <= data["as_of"], \
            f"{ticker} {entry['path']} filed {entry['filing_date']}, after {data['as_of']}"


@pytest.mark.parametrize("ticker", TICKERS)
def test_the_8k_carries_item_2_02(ticker):
    for entry in manifest(ticker)["documents"]:
        if entry["form"] == "8-K":
            assert "2.02" in entry["items"], f"{ticker}: 8-K items are {entry['items']!r}"


# The manifest records filings. The three files beside them are this project's
# own: the manifest itself, the expected values with their provenance notes, and
# the extraction-drift baseline. None of them was served by EDGAR.
NOT_A_FILING = ("manifest.json", "expected_values.json", "expected.json")


def test_the_manifest_lists_every_file_that_is_there():
    """A file nobody recorded is not a record. Catches an untracked addition."""
    for ticker in TICKERS:
        listed = {(FIXTURES / ticker / e["path"]).resolve()
                  for e in manifest(ticker)["documents"]}
        on_disk = {p.resolve() for p in (FIXTURES / ticker).rglob("*")
                   if p.is_file() and p.name not in NOT_A_FILING}
        assert on_disk == listed, f"{ticker}: {sorted(on_disk ^ listed)}"
