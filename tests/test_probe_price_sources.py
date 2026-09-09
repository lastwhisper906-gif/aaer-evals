"""The probe's reading of a price answer, judged against real answers.

Every body below was captured verbatim from the named source on 2026-09-09 by
the hand run that this probe was written around; the expected rows are read off
those bodies by eye and written out here. Nothing in this file is produced by the
code it judges.

No test here touches the network. The probe's whole point is the network, and its
answer changes with what the sources do -- what has to hold whatever they answer
is that a page of prices is read as prices and a page of refusal is not.
"""

from __future__ import annotations

import zipfile

from src import probe_price_sources as probe

# stooq.com/db/d/?b=d_us_txt and stooq.com/q/d/l/?s=leh.us&i=d, both user agents,
# 2026-09-09: 796 bytes, status 200. The challenge string and the nonce differ
# between requests; everything else is what came back.
STOOQ_BROWSER_CHECK = (
    b'<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="robots" '
    b'content="noindex,nofollow"></head><body><noscript>This site requires '
    b'JavaScript to verify your browser. Please enable JavaScript and reload.'
    b'</noscript><script nonce="lgWwOqa8PUr1ul9qYIY7uw">\n'
    b'(async()=>{const c="AAAAAGqhIEv5GTT9xm7T3CjImofxgDUOgvXABEDuPlp1wHOY",'
    b'd=4,t="0".repeat(d),e=new TextEncoder;let n=0;while(1){const h=await '
    b'crypto.subtle.digest("SHA-256",e.encode(c+n));n++}})();\n'
    b'</script></body></html>'
)

# eodhd.com/api/eod/AAPL.US?api_token=demo&fmt=csv&from=2024-01-02&to=2024-01-05
# on 2026-09-09. A real daily table from a real price source: the close is the
# fifth column and an adjusted close sits beside it, which is why the columns are
# found by name.
DAILY_TABLE = (
    b"Date,Open,High,Low,Close,Adjusted_close,Volume\n"
    b"2024-01-02,187.15,188.44,183.89,185.64,183.404,82488700\n"
    b"2024-01-03,184.22,185.88,183.43,184.25,182.0308,58414500\n"
    b"2024-01-04,182.15,183.09,180.88,181.91,179.7189,71983600\n"
    b"2024-01-05,181.99,182.76,180.17,181.18,178.9977,62379700\n"
)

# The same request with fmt=json, same day.
DAILY_OBJECTS = (
    b'[{"date":"2024-01-02","open":187.15,"high":188.44,"low":183.89,'
    b'"close":185.64,"adjusted_close":183.404,"volume":82488700},'
    b'{"date":"2024-01-03","open":184.22,"high":185.88,"low":183.43,'
    b'"close":184.25,"adjusted_close":182.0308,"volume":58414500},'
    b'{"date":"2024-01-04","open":182.15,"high":183.09,"low":180.88,'
    b'"close":181.91,"adjusted_close":179.7189,"volume":71983600}]'
)

# eodhd.com/api/eod/LEH.US on the demonstration token, 2026-09-09: status 403,
# nine bytes, this body.
EODHD_REFUSAL = b"Forbidden"

# api.tiingo.com/tiingo/daily/leh/prices with no token, 2026-09-09: status 403.
TIINGO_REFUSAL = b'{"detail":"Please supply a token"}'


def test_the_named_ticker_is_one_that_was_delisted():
    # Lehman Brothers Holdings Inc. filed under Chapter 11 on 2008-09-15; the
    # New York Stock Exchange suspended the securities on 2008-09-17 and applied
    # to remove them from listing and registration. The probe's whole question is
    # about a ticker that stopped trading, so the ticker and the date it stopped
    # are asserted rather than left in prose that can drift.
    assert probe.TICKER == "LEH"
    assert "Lehman Brothers" in probe.COMPANY
    assert "2008-09-15" in probe.DELISTING
    assert "2008-09-17" in probe.DELISTING
    assert probe.LAST_MONTH_TRADED == "September 2008"


def test_a_daily_table_is_read_as_prices():
    assert probe.history_rows(DAILY_TABLE) == [
        "2024-01-02 close 185.64",
        "2024-01-03 close 184.25",
        "2024-01-04 close 181.91",
        "2024-01-05 close 181.18",
    ]


def test_daily_objects_are_read_as_prices():
    assert probe.history_rows(DAILY_OBJECTS) == [
        "2024-01-02 close 185.64",
        "2024-01-03 close 184.25",
        "2024-01-04 close 181.91",
    ]


def test_the_columns_are_found_by_name_and_not_by_position():
    # Constructed, not captured: the two candidates that publish a table do not
    # agree on column order, and a probe that read the fifth field would report a
    # volume as a price. Same four closes as the captured table, moved.
    reordered = (
        b"Volume,Close,Date,Open\n"
        b"82488700,185.64,2024-01-02,187.15\n"
        b"58414500,184.25,2024-01-03,184.22\n"
    )
    assert probe.history_rows(reordered) == [
        "2024-01-02 close 185.64",
        "2024-01-03 close 184.25",
    ]


def test_the_browser_check_is_recognised_and_yields_no_prices():
    assert probe.is_browser_check(STOOQ_BROWSER_CHECK) is True
    assert probe.history_rows(STOOQ_BROWSER_CHECK) == []


def test_a_refusal_yields_no_prices():
    assert probe.history_rows(EODHD_REFUSAL) == []
    assert probe.history_rows(TIINGO_REFUSAL) == []
    assert probe.is_browser_check(EODHD_REFUSAL) is False
    assert probe.is_browser_check(TIINGO_REFUSAL) is False


def test_a_page_carrying_a_date_and_no_prices_yields_no_prices():
    # The failure that would matter: a block page or an error carrying a date is
    # read as a history, and the probe exits green on nothing.
    assert probe.history_rows(b"<html>Suspended 2008-09-17. No data.</html>") == []
    assert probe.history_rows(b'{"date":"2008-09-17","message":"no access"}') == []
    assert probe.history_rows(b'{"detail":"2008-09-17"}') == []
    assert probe.history_rows(b"") == []


def test_an_empty_table_under_a_real_header_yields_no_prices():
    # A source that answers 200 with a header and nothing under it has not served
    # the history, and must not be read as having served it.
    assert probe.history_rows(b"Date,Open,High,Low,Close,Volume\n") == []


def test_the_control_ticker_is_not_mistaken_for_the_delisted_one():
    # The demonstration token serves a listed ticker and refuses the delisted
    # one. Counting the control's rows would exit green on the wrong question.
    assert probe.asks_for_the_delisted_ticker(
        "https://eodhd.com/api/eod/LEH.US?api_token=demo&fmt=json") is True
    assert probe.asks_for_the_delisted_ticker(
        "https://api.tiingo.com/tiingo/daily/leh/prices?startDate=2008-01-01") is True
    assert probe.asks_for_the_delisted_ticker(
        "https://eodhd.com/api/eod/AAPL.US?api_token=demo&fmt=json") is False


def _an_archive(tmp_path, members: dict[str, bytes]) -> probe.Reply:
    path = tmp_path / "bulk.zip"
    with zipfile.ZipFile(path, "w") as archive:
        for name, content in members.items():
            archive.writestr(name, content)
    return probe.Reply("https://stooq.com/db/d/?b=d_us_txt", 200,
                       "https://stooq.com/db/d/?b=d_us_txt", {}, path,
                       path.stat().st_size, None)


def test_the_ticker_is_found_inside_a_bulk_archive(tmp_path):
    # Constructed. The archive's real layout cannot be captured while the source
    # is blocked, so what this fixes is the part that does not depend on it: a
    # member is found by the ticker's name wherever it sits, and its columns are
    # read by their header. Of the numbers below only the fourteen cents is real
    # -- it is what the common stock closed at on the day of the suspension --
    # and the rest is filler, because a probe that never got the file has nothing
    # else to copy.
    reply = _an_archive(tmp_path, {
        "data/daily/us/nyse stocks/1/leh.us.txt":
            b"Date,Open,High,Low,Close,Volume\n"
            b"2008-09-16,7.25,7.55,3.11,3.65,468818000\n"
            b"2008-09-17,3.20,3.35,0.11,0.14,142559000\n",
        "data/daily/us/nasdaq stocks/1/aapl.us.txt":
            b"Date,Open,High,Low,Close,Volume\n2008-09-17,20.0,20.0,20.0,20.0,1\n",
    })
    note, rows = probe.rows_from_archive(reply)
    assert note == ("data/daily/us/nyse stocks/1/leh.us.txt, inside an archive "
                    "of 2 files")
    assert rows == ["2008-09-16 close 3.65", "2008-09-17 close 0.14"]


def test_an_archive_without_the_ticker_is_reported_and_not_passed_over(tmp_path):
    # The finding the bulk file exists to produce: the download worked and the
    # delisted company is not in it. It must reach the report, not be dropped
    # because no rows came with it.
    reply = _an_archive(tmp_path, {
        "data/daily/us/nasdaq stocks/1/aapl.us.txt":
            b"Date,Open,High,Low,Close,Volume\n2024-01-02,1,1,1,185.64,1\n",
    })
    note, rows = probe.rows_from_archive(reply)
    assert note == "an archive of 1 files, none named leh.us.txt"
    assert rows == []


def test_a_body_that_is_not_an_archive_says_so_with_no_note(tmp_path):
    path = tmp_path / "page.html"
    path.write_bytes(STOOQ_BROWSER_CHECK)
    reply = probe.Reply("https://stooq.com/db/d/?b=d_us_txt", 200,
                        "https://stooq.com/db/d/?b=d_us_txt", {}, path,
                        path.stat().st_size, None)
    assert probe.rows_from_archive(reply) == (None, [])


def _always(reply: probe.Reply):
    return lambda url, agent, workspace: reply


def test_the_verdict_says_the_file_arrived_without_the_ticker_when_it_did(
        tmp_path, monkeypatch):
    # The verdict has to follow the evidence. A downloaded file that does not
    # carry the delisted company is a different answer from a block, and a
    # verdict fixed in advance reports the wrong one.
    archive = _an_archive(tmp_path, {
        "data/daily/us/nasdaq stocks/1/aapl.us.txt":
            b"Date,Close\n2024-01-02,185.64\n",
    })
    monkeypatch.setattr(probe, "fetch", _always(archive))
    finding = probe.probe_stooq_bulk_file(tmp_path)
    assert finding.served is False
    assert finding.verdict == ("the file downloaded and LEH is not in it: an "
                               "archive of 1 files, none named leh.us.txt")


def test_the_verdict_says_blocked_when_the_file_never_arrived(
        tmp_path, monkeypatch):
    page = tmp_path / "page.html"
    page.write_bytes(STOOQ_BROWSER_CHECK)
    monkeypatch.setattr(probe, "fetch", _always(probe.Reply(
        "https://stooq.com/db/d/?b=d_us_txt", 200,
        "https://stooq.com/db/d/?b=d_us_txt", {}, page,
        page.stat().st_size, None)))
    finding = probe.probe_stooq_bulk_file(tmp_path)
    assert finding.served is False
    assert finding.verdict.startswith("blocked before any data")
    assert finding.answered is True


def test_a_file_carrying_the_ticker_serves_the_history(tmp_path, monkeypatch):
    # The green path, which no source took on the day this was written: rows for
    # the delisted ticker come back and the probe stops asking.
    archive = _an_archive(tmp_path, {
        "data/daily/us/nyse stocks/1/leh.us.txt":
            b"Date,Open,High,Low,Close,Volume\n"
            b"2008-09-17,3.20,3.35,0.11,0.14,142559000\n",
    })
    monkeypatch.setattr(probe, "fetch", _always(archive))
    finding = probe.probe_stooq_bulk_file(tmp_path)
    assert finding.served is True
    assert finding.verdict == "the history came back"
    assert finding.rows == ["2008-09-17 close 0.14"]
    assert len(finding.attempts) == 1


def test_a_candidate_with_no_rows_has_not_served_the_history():
    blocked = probe.Finding(
        "the Stooq daily bulk file",
        [probe.Attempt("https://stooq.com/db/d/?b=d_us_txt", "plain",
                       "status 200, 796 bytes, the browser check page", [], True)],
        "blocked before any data")
    assert blocked.served is False
    assert blocked.answered is True

    # A source that refused and a machine that reached nothing must not read the
    # same: the first is a finding about the source, the second is a finding
    # about this laptop.
    unreachable = probe.Finding(
        "a low-cost provider",
        [probe.Attempt("https://eodhd.com/api/eod/LEH.US", "plain",
                       "no answer at all: [Errno 8] nodename nor servname provided",
                       [], False)],
        "no answer")
    assert unreachable.served is False
    assert unreachable.answered is False
