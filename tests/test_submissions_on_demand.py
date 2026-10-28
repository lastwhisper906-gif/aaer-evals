"""Submissions on demand: every filing, overflow pages included, cut by `filingDate`.

The expected values are read off Apple's index as data.sec.gov served it on
2026-10-28, committed under `tests/fixtures/submissions_on_demand/` with each
file's URL and sha256 (`record.json`) and served here from a planted local
server. Each value below names where it stands in those files; none was read
off the reader under test.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from src import submissions
from src.edgar_client import EdgarClient, EdgarError
from tests.planted_edgar import DIRECT, SAMPLE_CONTACT, serve

STORE = Path(__file__).resolve().parent / "fixtures" / "submissions_on_demand"
RECORD = json.loads((STORE / "record.json").read_text(encoding="utf-8"))
CIK = "0000320193"
INDEX = "CIK0000320193.json"
OVERFLOW = "CIK0000320193-submissions-001.json"

# `filings.recent` lists 1,002 filings, the newest 0001140361-26-040540 on
# 2026-10-22 and the oldest on 2015-10-02; `filings.files` names one overflow
# page, `{"name": "CIK0000320193-submissions-001.json", "filingCount": 1268,
# "filingFrom": "1994-01-26", "filingTo": "2015-10-01"}`, whose arrays hold
# 1,268 filings from 1994-01-26 to 2015-09-18. No accession is on both.
RECENT_COUNT = 1002
OVERFLOW_COUNT = 1268
# the overflow page's last entry: the 10-Q 0000320193-94-000002 of 1994-01-26
OLDEST = {"accession": "0000320193-94-000002", "form": "10-Q", "filing_date": "1994-01-26"}

# Apple's earnings release, as the recent list gives it: form 8-K, items
# "2.02,9.01", filed 2026-07-30, `acceptanceDateTime` 2026-07-30T20:30:28.000Z.
# By hand: in July New York keeps daylight time, four hours behind universal
# time, so 20:30:28Z is 16:30:28 Eastern, offset -04:00.
RELEASE = {"accession": "0000320193-26-000018", "form": "8-K", "items": "2.02,9.01",
           "filing_date": "2026-07-30", "report_date": "2026-07-30",
           "primary_document": "aapl-20260730.htm",
           "acceptance_datetime": "2026-07-30T16:30:28-04:00"}

# A Form 4 the recent list dates 2026-10-22 and stamps 2026-10-22T22:32:20.000Z.
# By hand: daylight time runs to 2026-11-01, so that is 18:32:20 Eastern, after
# half past five. A filing date worked out from the five-thirty rule would be
# the next business day, the 23rd; EDGAR accepts Forms 3, 4 and 5 until ten at
# night and dates them that day, and the index says the 22nd.
FORM_FOUR = {"accession": "0001140361-26-040540", "form": "4", "filing_date": "2026-10-22",
             "acceptance_datetime": "2026-10-22T18:32:20-04:00"}


@pytest.fixture
def server():
    for planted in serve(default=None):
        for name in (INDEX, OVERFLOW):
            planted.bodies[f"/submissions/{name}"] = ((STORE / name).read_bytes(), "")
        yield planted


def client(tmp_path):
    return EdgarClient(environ={"EDGAR_USER_AGENT": SAMPLE_CONTACT, "AAER_CACHE": str(tmp_path)},
                       opener=DIRECT, sleep=lambda seconds: None)


def read(tmp_path, server, cutoff):
    return submissions.filings(client(tmp_path), CIK, cutoff=cutoff,
                               base=server.url + "/submissions/")


def row(rows, accession):
    [found] = [r for r in rows if r["accession"] == accession]
    return found


def test_the_committed_files_are_the_ones_recorded():
    for name, entry in RECORD["files"].items():
        data = (STORE / name).read_bytes()
        assert len(data) == entry["bytes"]
        assert hashlib.sha256(data).hexdigest() == entry["sha256"]
        assert entry["url"] == "https://data.sec.gov/submissions/" + name
    assert submissions.index_url(CIK) == RECORD["files"][INDEX]["url"]
    assert submissions.index_url(320193) == RECORD["files"][INDEX]["url"]


def test_every_filing_is_read_overflow_page_included(tmp_path, server):
    rows = read(tmp_path, server, "2026-10-22")
    assert len(rows) == RECENT_COUNT + OVERFLOW_COUNT
    assert len({r["accession"] for r in rows}) == len(rows)
    assert {k: rows[-1][k] for k in OLDEST} == OLDEST
    # the index, then the one page it names; nothing else is asked for
    assert [path for path, _ in server.seen] == [f"/submissions/{INDEX}",
                                                 f"/submissions/{OVERFLOW}"]
    assert all(headers["User-Agent"] == SAMPLE_CONTACT for _, headers in server.seen)


def test_the_release_row_carries_its_items_and_its_eastern_stamp(tmp_path, server):
    found = row(read(tmp_path, server, "2026-10-22"), RELEASE["accession"])
    assert {k: found[k] for k in RELEASE} == RELEASE


def test_the_cutoff_key_is_the_filing_date_the_index_gives(tmp_path, server):
    on_the_day = read(tmp_path, server, "2026-10-22")
    assert {k: row(on_the_day, FORM_FOUR["accession"])[k] for k in FORM_FOUR} == FORM_FOUR
    the_day_before = read(tmp_path, server, "2026-10-21")
    assert FORM_FOUR["accession"] not in {r["accession"] for r in the_day_before}
    assert len(the_day_before) == RECENT_COUNT - 1 + OVERFLOW_COUNT
    assert max(r["filing_date"] for r in the_day_before) <= "2026-10-21"


def test_a_cutoff_before_the_recent_list_reads_from_the_overflow_page_alone(tmp_path, server):
    rows = read(tmp_path, server, "2015-09-30")
    assert len(rows) == OVERFLOW_COUNT
    assert rows[0]["filing_date"] == "2015-09-18"
    assert {k: rows[-1][k] for k in OLDEST} == OLDEST


def test_rows_run_newest_first(tmp_path, server):
    rows = read(tmp_path, server, "2026-10-22")
    keys = [(r["filing_date"], r["accession"]) for r in rows]
    assert keys == sorted(keys, reverse=True)
    assert rows[0]["accession"] == FORM_FOUR["accession"]


@pytest.mark.parametrize("cutoff", ["2026-10", "20261022", "2026-10-22T16:00", ""])
def test_a_cutoff_that_is_not_a_date_is_refused_before_any_request(tmp_path, server, cutoff):
    with pytest.raises(EdgarError, match="a cutoff is a date"):
        read(tmp_path, server, cutoff)
    assert server.seen == []


def test_an_overflow_page_with_an_unexpected_name_is_not_fetched(tmp_path, server):
    index = json.loads((STORE / INDEX).read_bytes())
    index["filings"]["files"] = [{"name": "../../Archives/edgar/data/320193/x.json"}]
    server.bodies[f"/submissions/{INDEX}"] = (json.dumps(index).encode(), "")
    with pytest.raises(EdgarError, match="an overflow page named"):
        read(tmp_path, server, "2026-10-22")
    assert [path for path, _ in server.seen] == [f"/submissions/{INDEX}"]


def test_a_page_whose_arrays_disagree_is_refused(tmp_path, server):
    index = json.loads((STORE / INDEX).read_bytes())
    index["filings"]["recent"]["filingDate"].pop()
    server.bodies[f"/submissions/{INDEX}"] = (json.dumps(index).encode(), "")
    with pytest.raises(EdgarError, match="filingDate lists 1001 values for 1002 filings"):
        read(tmp_path, server, "2026-10-22")


def test_an_answer_that_is_not_json_is_refused(tmp_path, server):
    server.bodies[f"/submissions/{INDEX}"] = (b"<html>Request Rate Threshold Exceeded</html>", "")
    with pytest.raises(EdgarError, match="not JSON"):
        read(tmp_path, server, "2026-10-22")
