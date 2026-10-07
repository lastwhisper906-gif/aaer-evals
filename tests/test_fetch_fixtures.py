"""The fetcher's acceptance stamp.

EDGAR's `acceptanceDateTime` is projected onto every submissions row and every
filing's manifest row as `acceptance_datetime`: Eastern wall time with the
offset of that date written out, never a Z, never a bare date, and None where
the index gave nothing readable.

Every expected value here is worked by hand from the source: the raw index
rows committed as `tests/fixtures/acceptance_stamp/nvda_submissions_rows.json`
(EDGAR's own field names, read from data.sec.gov with the declared User-Agent
on 2026-10-07), the SGML submission headers committed beside the 10-K fixtures
(EDGAR's Eastern wall clock, held to each manifest's hash), and the clock
arithmetic written out beside each case. None was read off the code.
"""

from __future__ import annotations

import datetime as dt
import json
import re
from pathlib import Path

import pytest

from src import fetch_fixtures
from src.fetch_fixtures import eastern_stamp

FIXTURES = Path(__file__).resolve().parent / "fixtures"
# Beside the hash-held stores, not inside one: every file under a company's
# directory is a document its manifest lists (tests/test_fixtures.py).
RECORD = json.loads((FIXTURES / "acceptance_stamp" / "nvda_submissions_rows.json")
                    .read_text(encoding="utf-8"))

NVDA_ACCESSION = "0001045810-26-000075"
# The raw row, quoted: EDGAR stamps NVDA's 10-Q `2026-08-26T20:36:00.000Z` and
# dates it 2026-08-26.
NVDA_RAW = "2026-08-26T20:36:00.000Z"
# By hand: the Z is universal time. On 2026-08-26 New York is on daylight time,
# four hours behind, so 20:36 universal is 16:36 Eastern, offset -04:00. Held
# against the filing date on the same row: 16:36 is before EDGAR's half past
# five, so EDGAR dates the filing the 26th -- which the row says. Read as an
# Eastern wall clock instead, 20:36 is after half past five and EDGAR would have
# dated it the 27th, which the row does not say.
NVDA_EASTERN = "2026-08-26T16:36:00-04:00"


def test_the_committed_raw_row_is_the_one_quoted_here():
    """The record is EDGAR's row under EDGAR's names, with where it came from."""
    row = RECORD["row"]
    assert row["accessionNumber"] == NVDA_ACCESSION == RECORD["accession"]
    assert row["acceptanceDateTime"] == NVDA_RAW
    assert row["filingDate"] == "2026-08-26"
    assert row["form"] == "10-Q"
    assert RECORD["url"] == fetch_fixtures.SUBMISSIONS_URL.format(cik="0001045810")
    assert re.fullmatch(r"[0-9a-f]{64}", RECORD["index_sha256"])
    assert RECORD["index_bytes"] > 0


def test_nvda_raw_stamp_becomes_the_eastern_form():
    assert eastern_stamp(RECORD["row"]["acceptanceDateTime"]) == NVDA_EASTERN


# --- the evidence that the index's Z is universal time ---------------------------
#
# The source docs/needs_judgment.md named for the question: a filing's own SGML
# header, `{accession}-index-headers.html`, whose ACCEPTANCE-DATETIME is EDGAR's
# wall clock with no zone. The headers are committed fixtures, held to the
# manifests' hashes, and are read here with two regular expressions -- nothing
# from src/ parses them.

HEADER_ACCEPTED = re.compile(r"^<ACCEPTANCE-DATETIME>(\d{14})$", re.MULTILINE)
HEADER_FILED = re.compile(r"^<FILING-DATE>(\d{8})$", re.MULTILINE)
HEADERS = sorted(FIXTURES.glob("*/*/*/*-index-headers.html"))
EDGAR_CLOSE = dt.time(17, 30)
# Regulation S-T Rule 13 dates a direct transmission by when it began, not by when
# EDGAR accepted it, so an acceptance a few seconds past the close can still carry
# the day. One committed header does, read off it: ACCEPTANCE-DATETIME
# 20241118173003 and FILING-DATE 20241118, three seconds past half past five and
# dated that day. Each such header is named here by accession, with its seconds,
# rather than the rule widened for every header: an acceptance minutes past the
# close that keeps the day would be a different question, and fails below.
ACCEPTED_SECONDS_PAST_THE_CLOSE_SAME_DAY = {"0001048695-24-000185": 3}


def _header(path: Path) -> tuple[dt.datetime, dt.date]:
    text = path.read_text(encoding="utf-8")
    accepted = HEADER_ACCEPTED.search(text).group(1)
    filed = HEADER_FILED.search(text).group(1)
    return (dt.datetime.strptime(accepted, "%Y%m%d%H%M%S"),
            dt.datetime.strptime(filed, "%Y%m%d").date())


def test_the_committed_headers_keep_edgars_eastern_clock():
    """EDGAR dates a filing the day it accepted it, or past half past five in the
    evening Eastern the next business day. Every committed header obeys that
    rule read as an Eastern wall clock. Read as universal time, the five
    accepted after half past five would be early-afternoon Eastern (ANET's
    19:50:17 on 2025-02-18 is 14:50:17 standard time) and dated a day late."""
    assert len(HEADERS) >= 43           # the twenty companies' headers on 2026-10-07
    late, boundary = [], []
    for path in HEADERS:
        accepted, filed = _header(path)
        accession = path.parts[-2]
        if accepted.time() < EDGAR_CLOSE:
            assert filed == accepted.date(), path
        elif accession in ACCEPTED_SECONDS_PAST_THE_CLOSE_SAME_DAY:
            seconds = (accepted - dt.datetime.combine(accepted.date(), EDGAR_CLOSE)).seconds
            assert filed == accepted.date(), path
            assert seconds == ACCEPTED_SECONDS_PAST_THE_CLOSE_SAME_DAY[accession], path
            boundary.append(accession)
        else:
            assert filed > accepted.date(), path
            late.append(path.parts[-4])
    assert len(late) >= 5 and {"ANET", "FTNT", "TTMI", "WDC"} <= set(late)
    # every header the list names is committed and was read, so the list cannot go stale
    assert sorted(boundary) == sorted(ACCEPTED_SECONDS_PAST_THE_CLOSE_SAME_DAY)


# NVDA's two 10-Ks, from their committed headers. Each is Eastern standard time
# in February, five hours behind universal time, so the index stamp the fetcher
# reads should be the header's clock plus five hours, and its Eastern form the
# header's clock with -05:00 written after it.
TEN_K_HEADERS = {
    "0001045810-26-000021": "20260225164219",
    "0001045810-25-000023": "20250226164833",
}


def test_nvdas_index_stamps_are_the_headers_instants_in_universal_time():
    rows = {row["accessionNumber"]: row for row in RECORD["rows_beside_committed_headers"]}
    assert sorted(rows) == sorted(TEN_K_HEADERS)
    for accession, clock in TEN_K_HEADERS.items():
        header = FIXTURES / "NVDA" / "10-K" / accession / f"{accession}-index-headers.html"
        accepted, filed = _header(header)
        assert accepted.strftime("%Y%m%d%H%M%S") == clock
        row = rows[accession]
        assert row["filingDate"] == filed.isoformat()
        # header 16:42:19 Eastern standard + 5 h = 21:42:19 universal (and 16:48:33 -> 21:48:33)
        assert row["acceptanceDateTime"] == (
            (accepted + dt.timedelta(hours=5)).strftime("%Y-%m-%dT%H:%M:%S") + ".000Z")
        assert eastern_stamp(row["acceptanceDateTime"]) == (
            accepted.strftime("%Y-%m-%dT%H:%M:%S") + "-05:00")
        # the decorative-Z reading puts the 10-K after half past five, which the
        # index's own filing date refutes
        wall = dt.datetime.fromisoformat(row["acceptanceDateTime"][:19])
        assert wall.time() > EDGAR_CLOSE and row["filingDate"] == wall.date().isoformat()


def test_the_hand_written_nvda_stamp_and_the_fetchers_give_one_day_zero():
    """`NVDA_ACCEPTED` in tests/test_run_analysis.py was written by hand from this
    same index row before the fetch kept the stamp, with no zone: the Eastern
    wall-clock reading, 20:36. It stays as written. The fetcher's value is the
    same EDGAR stamp read as universal time, 16:36 Eastern, which the headers
    above show is the instant EDGAR meant. Both are on the 26th and after the
    four o'clock close, so the window that test works out -- day zero Thursday
    the 27th -- is the same under either."""
    from tests.test_run_analysis import NVDA_ACCEPTED
    hand = dt.datetime.fromisoformat(NVDA_ACCEPTED)
    fetched = dt.datetime.fromisoformat(eastern_stamp(RECORD["row"]["acceptanceDateTime"]))
    four = dt.time(16, 0)
    for when in (hand, fetched):
        assert when.date() == dt.date(2026, 8, 26) and when.time() >= four


@pytest.mark.parametrize("raw, eastern", [
    # February: standard time, five hours behind; 21:31:25 less five hours.
    ("2026-02-25T21:31:25.000Z", "2026-02-25T16:31:25-05:00"),
    # Just after midnight universal is the evening before in New York:
    # 00:14:03 less four hours is 20:14:03 on the 20th.
    ("2026-03-21T00:14:03.000Z", "2026-03-20T20:14:03-04:00"),
    # Daylight time begins on 2026-03-08 at 02:00 standard, which is 07:00
    # universal: a second before, the clock is standard, five hours behind ...
    ("2026-03-08T06:59:59.000Z", "2026-03-08T01:59:59-05:00"),
    # ... and at 07:00 it jumps to 03:00 daylight, four hours behind.
    ("2026-03-08T07:00:00.000Z", "2026-03-08T03:00:00-04:00"),
    # Daylight time ends on 2026-11-01 at 02:00 daylight, 06:00 universal.
    ("2026-11-01T05:59:59.000Z", "2026-11-01T01:59:59-04:00"),
    ("2026-11-01T06:00:00.000Z", "2026-11-01T01:00:00-05:00"),
])
def test_the_offset_is_the_dates_own_standard_or_daylight(raw, eastern):
    out = eastern_stamp(raw)
    assert out == eastern
    assert not out.endswith("Z")
    assert "T" in out and out[-6] in "+-"


@pytest.mark.parametrize("raw", [
    None, "", 12345,
    "2026-08-26",                     # a date alone: no time of day
    "2026-08-26T20:36:00",            # no zone letter: the zone is not stated, so not guessed
    "2026-08-26T16:36:00-04:00",      # already an offset: not the shape EDGAR writes
    "20260826203600",                 # the index-headers shape, not the index's
    " 2026-08-26T20:36:00.000Z",      # padded
    "2026-13-01T20:36:00.000Z",       # month 13
    "2026-08-26T25:00:00.000Z",       # hour 25
    "2026-08-26T20:36:00.000Z extra",
    "2026-08-26T20:36:00.000Z\n",    # a trailing newline
])
def test_a_missing_or_malformed_raw_value_is_none_never_a_guess(raw):
    assert eastern_stamp(raw) is None


# --- the projection onto the submissions rows and the manifest rows ------------

def _raw(accession, filed, form, stamp, *, report="2026-07-26", items="",
         primary="doc.htm"):
    row = {"accessionNumber": accession, "filingDate": filed, "reportDate": report,
           "form": form, "items": items, "primaryDocument": primary,
           "primaryDocDescription": form}
    if stamp is not None:
        row["acceptanceDateTime"] = stamp
    return row


def test_submissions_rows_carry_the_stamp_and_none_where_the_index_gave_none():
    filings = [RECORD["row"],
               _raw("0001045810-26-000061", "2026-05-28", "10-Q", None)]
    record, raw = fetch_fixtures.submissions_record("NVDA", "0001045810", "2026-09-01",
                                                    filings)
    by_accession = {row["accession"]: row for row in record["filings"]}
    assert by_accession[NVDA_ACCESSION]["acceptance_datetime"] == NVDA_EASTERN
    assert by_accession["0001045810-26-000061"]["acceptance_datetime"] is None
    # what is written is what was returned
    written = json.loads(raw)["filings"]
    assert [row["acceptance_datetime"] for row in written] == [NVDA_EASTERN, None]


class _IndexPages:
    """A submissions index as EDGAR's parallel arrays: the recent page and one older."""

    def __init__(self, recent: dict, older: dict | None = None):
        self.recent, self.older = recent, older

    def get_json(self, url):
        if url == fetch_fixtures.SUBMISSIONS_URL.format(cik="0001045810"):
            files = [] if self.older is None else [{"name": "CIK0001045810-older.json"}]
            return {"filings": {"recent": self.recent, "files": files}}
        if url == fetch_fixtures.OLDER_URL.format(name="CIK0001045810-older.json"):
            return self.older
        raise AssertionError(url)


def _arrays(*rows: dict, with_stamp: bool = True) -> dict:
    fields = ["accessionNumber", "filingDate", "reportDate", "form", "items",
              "primaryDocument", "primaryDocDescription", "isXBRL"]
    if with_stamp:
        fields.append("acceptanceDateTime")
    return {field: [row.get(field) for row in rows] for field in fields}


def test_recent_filings_projects_the_raw_field_under_edgars_name():
    rows = fetch_fixtures.recent_filings(_IndexPages(_arrays(RECORD["row"])), "0001045810")
    assert rows[0]["acceptanceDateTime"] == NVDA_RAW
    assert rows[0]["accessionNumber"] == NVDA_ACCESSION


def test_an_index_served_without_the_field_gives_none_on_every_row():
    pages = _IndexPages(_arrays(RECORD["row"], with_stamp=False))
    assert fetch_fixtures.recent_filings(pages, "0001045810")[0]["acceptanceDateTime"] is None


def test_every_filing_projects_the_raw_field_on_the_recent_and_the_older_page():
    older = _raw("0001045810-20-000010", "2020-08-20", "10-Q", "2020-08-20T20:30:00.000Z")
    rows = fetch_fixtures.every_filing(
        _IndexPages(_arrays(RECORD["row"]), _arrays(older)), "0001045810")
    assert [row["acceptanceDateTime"] for row in rows] == [NVDA_RAW, "2020-08-20T20:30:00.000Z"]


class _Archive:
    """EDGAR's archive for the four filings below: each has a primary document
    and, for the quarterly and annual reports, an instance beside it; the 8-K's
    header names its exhibit 99.1."""

    def get(self, url):
        name = url.rsplit("/", 1)[1]
        if name.endswith("-index-headers.html"):
            return b"<TYPE>8-K\n<FILENAME>k.htm\n<TYPE>EX-99.1\n<FILENAME>release.htm\n"
        return b"<html>" + name.encode() + b"</html>"

    def get_json(self, url):
        assert url.endswith("/index.json"), url
        return {"directory": {"item": [{"name": n} for n in
                                       ("doc.htm", "doc_htm.xml", "k.htm", "release.htm")]}}


# Four filings with hand-chosen raw stamps, and the Eastern form of each by the
# arithmetic above: four hours behind from March 8 to November 1, five outside.
ANNUAL = ("0001045810-26-000010", "2026-02-25", "2026-02-25T21:31:25.000Z",
          "2026-02-25T16:31:25-05:00")
QUARTER = (NVDA_ACCESSION, "2026-08-26", NVDA_RAW, NVDA_EASTERN)
PRIOR = ("0001045810-26-000061", "2026-05-28", "2026-05-28T20:40:10.000Z",
         "2026-05-28T16:40:10-04:00")
RELEASE = ("0001045810-26-000073", "2026-08-26", "2026-08-26T20:21:19.000Z",
           "2026-08-26T16:21:19-04:00")


def test_every_filings_manifest_row_carries_the_stamp_and_the_index_row_none(tmp_path):
    filings = [_raw(ANNUAL[0], ANNUAL[1], "10-K", ANNUAL[2]),
               _raw(QUARTER[0], QUARTER[1], "10-Q", QUARTER[2]),
               _raw(PRIOR[0], PRIOR[1], "10-Q", PRIOR[2]),
               _raw(RELEASE[0], RELEASE[1], "8-K", RELEASE[2], items="2.02,9.01",
                    primary="k.htm")]
    manifest, problems = fetch_fixtures.fetch_company(
        _Archive(), "NVDA", "0001045810", "2026-09-01", tmp_path, filings=filings)
    assert problems == []
    stamps = {(row["form"], row["role"]): row.get("acceptance_datetime", "absent")
              for row in manifest["documents"]}
    assert stamps == {
        ("10-K", "primary_html"): ANNUAL[3], ("10-K", "xbrl_instance"): ANNUAL[3],
        ("10-Q", "primary_html"): QUARTER[3], ("10-Q", "xbrl_instance"): QUARTER[3],
        ("10-Q", "prior_period"): PRIOR[3], ("10-Q", "prior_period_xbrl_instance"): PRIOR[3],
        ("8-K", "primary_html"): RELEASE[3], ("8-K", "exhibit_99_1"): RELEASE[3],
        # the index is not a filing and has no acceptance, as it has no filing date
        ("submissions", "submissions_index"): "absent",
    }
    # the stamp sits beside the filing date, on disk as in memory
    on_disk = json.loads((tmp_path / "NVDA" / "manifest.json").read_text(encoding="utf-8"))
    quarter = next(row for row in on_disk["documents"]
                   if row["form"] == "10-Q" and row["role"] == "primary_html")
    assert (quarter["filing_date"], quarter["acceptance_datetime"]) == (QUARTER[1], QUARTER[3])
    index = json.loads((tmp_path / "NVDA" / "submissions.json").read_text(encoding="utf-8"))
    assert {row["accession"]: row["acceptance_datetime"] for row in index["filings"]} == {
        ANNUAL[0]: ANNUAL[3], QUARTER[0]: QUARTER[3], PRIOR[0]: PRIOR[3], RELEASE[0]: RELEASE[3]}


def test_a_filing_the_index_stamped_unreadably_is_recorded_with_none(tmp_path):
    filings = [_raw(ANNUAL[0], ANNUAL[1], "10-K", "2026-02-25T21:31:25"),
               _raw(QUARTER[0], QUARTER[1], "10-Q", None),
               _raw(PRIOR[0], PRIOR[1], "10-Q", PRIOR[2]),
               _raw(RELEASE[0], RELEASE[1], "8-K", RELEASE[2], items="2.02,9.01",
                    primary="k.htm")]
    manifest, problems = fetch_fixtures.fetch_company(
        _Archive(), "NVDA", "0001045810", "2026-09-01", tmp_path, filings=filings)
    assert problems == []
    stamps = {(row["form"], row["role"]): row["acceptance_datetime"]
              for row in manifest["documents"] if row["form"] != "submissions"}
    assert stamps[("10-K", "primary_html")] is None
    assert stamps[("10-Q", "primary_html")] is None
    assert stamps[("10-Q", "prior_period")] == PRIOR[3]

