"""The probe's reading of a price answer, judged against real answers.

Each captured body below is committed byte for byte, with the request that
produced it named above it, and the expected rows are read off it by eye.
Nothing in this file is produced by the code it judges. Two bodies are
constructed rather than captured -- the delisted ticker's own file, which no
source served, and a table with its columns moved -- and each says so where it
sits.

No test here touches the network. The probe's whole point is the network, and its
answer changes with what the sources do -- what has to hold whatever they answer
is that a page of prices is read as prices and a page of refusal is not.
"""

from __future__ import annotations

import zipfile

from src import probe_price_sources as probe

# https://stooq.com/q/d/l/?s=leh.us&i=d asked with the plain user agent on
# 2026-09-09: status 200, 796 bytes, this body whole. The bulk file's download
# link and the browser user agent all answer with the same page; the challenge
# string and the nonce differ between requests.
STOOQ_BROWSER_CHECK = (
    b'<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="robot'
    b's" content="noindex,nofollow"></head><body><noscript>This site req'
    b'uires JavaScript to verify your browser. Please enable JavaScript '
    b'and reload.</noscript><script nonce="or2wtmNuIOPCQaX76paCpQ">\n(as'
    b'ync()=>{const c="AAAAAGqhKo_s3NBME4tD5H1VweYY3jazgvXABKWjUwblUr_qI'
    b'8PtHp9FRjA",d=4,t="0".repeat(d),e=new TextEncoder;let n=0;while(1)'
    b'{const h=await crypto.subtle.digest("SHA-256",e.encode(c+n)),x=Arr'
    b'ay.from(new Uint8Array(h)).map(b=>b.toString(16).padStart(2,"0")).'
    b'join("");if(x.startsWith(t))break;n++}const r=await fetch("/__veri'
    b'fy",{method:"POST",headers:{"Content-Type":"application/x-www-form'
    b'-urlencoded"},body:"c="+encodeURIComponent(c)+"&n="+n,credentials:'
    b'"same-origin"});if(r.ok)location.reload()})();\n</script></body></'
    b'html>\n'
)

# A member of Stooq's daily bulk archive for the United States, in the layout its
# members carry. Stooq's own copy cannot be fetched while the browser check
# stands, so this one comes from a public copy of it:
# raw.githubusercontent.com/satrajitghosh183/The-Market-Whisperer/master/data/abi.us.txt
# fetched 2026-09-09, status 200, 815 bytes, committed whole. The layout is the
# one a published converter of stooq.com's ticker files documents -- column names
# inside angle brackets, a period column, and a date written 20250627 rather than
# 2025-06-27 -- which is why the parser has to read both date forms.
#
# The close is the eighth column and the low the seventh, and the two differ on
# the row dated 20250723, so a probe reading by position would report 25.07 there
# where the close is 25.075.
STOOQ_BULK_MEMBER = (
    b'<TICKER>,<PER>,<DATE>,<TIME>,<OPEN>,<HIGH>,<LOW>,<CLOSE>,<VOL>,<OP'
    b'ENINT>\nABI.US,D,20250627,000000,25.05,25.05,25.05,25.05,6,0\nABI.'
    b'US,D,20250701,000000,25.07,25.07,25.06,25.06,1060003,0\nABI.US,D,2'
    b'0250709,000000,25.05,25.05,25.04,25.04,400003,0\nABI.US,D,20250723'
    b',000000,25.07,25.075,25.07,25.075,320202,0\nABI.US,D,20250724,0000'
    b'00,25.06,25.07,25.06,25.07,280413,0\nABI.US,D,20250725,000000,25.0'
    b'9,25.12,25.08,25.095,2046,0\nABI.US,D,20250729,000000,25.13,25.13,'
    b'25.13,25.13,399,0\nABI.US,D,20250808,000000,25.14,25.145,25.1399,2'
    b'5.145,1006,0\nABI.US,D,20250811,000000,25.14,25.14,25.14,25.14,360'
    b'5,0\nABI.US,D,20250812,000000,25.15,25.15,25.15,25.15,100187,0\nAB'
    b'I.US,D,20250814,000000,25.15,25.15,25.15,25.15,160,0\nABI.US,D,202'
    b'50818,000000,25.18,25.27,25.17,25.17,3613,0\nABI.US,D,20250916,000'
    b'000,25.07,25.07,25.055,25.055,111,0\n'
)

# The captured member's header, written out once so that the constructed
# members below wear the layout it came in rather than one of their own.
BULK_HEADER = (
    b"<TICKER>,<PER>,<DATE>,<TIME>,<OPEN>,<HIGH>,<LOW>,<CLOSE>,<VOL>,<OPENINT>\n"
)

# Constructed, because no source served the delisted ticker's own file. Of the
# numbers only the close is real: Lehman's 8-K of 2008-09-23 says the common
# stock closed at fourteen cents on 2008-09-17, the day the Exchange suspended
# it. The open, high, low and volume are filler -- a probe that never got the
# file has nothing else to copy.
LEH_BULK_MEMBER = BULK_HEADER + b"LEH.US,D,20080917,000000,0.30,0.35,0.10,0.14,1,0\n"

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
    assert probe.LAST_MONTH_TRADED == "2008-09"


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


def test_the_bulk_archive_layout_is_read_as_prices():
    # The layout the first candidate would answer in. Angle-bracketed column
    # names and a date with no dashes in it: a parser written for the other two
    # shapes reads this file as no prices at all, and the probe would then report
    # a downloaded file with the company missing from it.
    assert STOOQ_BULK_MEMBER.startswith(BULK_HEADER)
    assert probe.history_rows(STOOQ_BULK_MEMBER) == [
        "2025-06-27 close 25.05",
        "2025-07-01 close 25.06",
        "2025-07-09 close 25.04",
        "2025-07-23 close 25.075",
        "2025-07-24 close 25.07",
        "2025-07-25 close 25.095",
        "2025-07-29 close 25.13",
        "2025-08-08 close 25.145",
        "2025-08-11 close 25.14",
        "2025-08-12 close 25.15",
        "2025-08-14 close 25.15",
        "2025-08-18 close 25.17",
        "2025-09-16 close 25.055",
    ]


def test_the_columns_are_found_by_name_and_not_by_position():
    # Constructed, not captured: the candidates that publish a table do not agree
    # on column order, and a probe that read the fifth field would report a
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


def test_a_close_that_is_not_a_number_is_not_a_price():
    # The same failure one step further in: an error payload shaped like a price
    # row, dated correctly, carrying a message where the close belongs. It has
    # served no history and must not be read as having served one.
    assert probe.history_rows(b'[{"date":"2008-09-17","close":"unavailable"}]') == []
    assert probe.history_rows(b"Date,Close\n2008-09-17,unavailable\n") == []
    assert probe.history_rows(b"Date,Close\n2008-09-17,\n") == []
    assert probe.history_rows(b'[{"date":"2008-09-17","close":"NaN"}]') == []
    # And the mirror of it: a real close on something that is not a date.
    assert probe.history_rows(b"Date,Close\n2008-13-45,0.14\n") == []


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


def test_rows_short_of_the_month_the_trading_stopped_are_not_the_history():
    # A source could carry the ticker and stop before the suspension. Rows came
    # back and the history did not, and the verdict has to say which of the two
    # happened rather than reading the same for both.
    short = ["2007-12-31 close 65.44"]
    assert probe.reached_the_delisting(short) is False
    assert probe.what_came_back(short) == (
        "rows came back and the history did not: 1 row dated 2007-12-31 to "
        "2007-12-31, none of them in 2008-09, the month the trading stopped")

    reaching = ["2008-09-16 close 3.65", "2008-09-17 close 0.14"]
    assert probe.reached_the_delisting(reaching) is True
    assert probe.what_came_back(reaching) == (
        "the history came back: 2 rows dated 2008-09-16 to 2008-09-17")


def _an_archive(tmp_path, members: dict[str, bytes]) -> probe.Reply:
    path = tmp_path / "bulk.zip"
    with zipfile.ZipFile(path, "w") as archive:
        for name, content in members.items():
            archive.writestr(name, content)
    return probe.Reply("https://stooq.com/db/d/?b=d_us_txt", 200,
                       "https://stooq.com/db/d/?b=d_us_txt", {}, path,
                       path.stat().st_size, None)


def test_the_ticker_is_found_inside_a_bulk_archive(tmp_path):
    # A member is found by the ticker's name wherever it sits in the archive, and
    # its columns are read by their header.
    reply = _an_archive(tmp_path, {
        "data/daily/us/nyse stocks/1/leh.us.txt": LEH_BULK_MEMBER,
        "data/daily/us/nasdaq stocks/1/abi.us.txt": STOOQ_BULK_MEMBER,
    })
    note, rows = probe.rows_from_archive(reply)
    assert note == ("data/daily/us/nyse stocks/1/leh.us.txt, inside an archive "
                    "of 2 files")
    assert rows == ["2008-09-17 close 0.14"]


def test_an_archive_without_the_ticker_is_reported_and_not_passed_over(tmp_path):
    # The finding the bulk file exists to produce: the download worked and the
    # delisted company is not in it. It must reach the report, not be dropped
    # because no rows came with it.
    reply = _an_archive(tmp_path, {
        "data/daily/us/nasdaq stocks/1/abi.us.txt": STOOQ_BULK_MEMBER,
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
        "data/daily/us/nasdaq stocks/1/abi.us.txt": STOOQ_BULK_MEMBER,
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
    # the delisted ticker come back, reaching the month it stopped trading, and
    # the probe stops asking.
    archive = _an_archive(tmp_path, {
        "data/daily/us/nyse stocks/1/leh.us.txt": LEH_BULK_MEMBER,
    })
    monkeypatch.setattr(probe, "fetch", _always(archive))
    finding = probe.probe_stooq_bulk_file(tmp_path)
    assert finding.served is True
    assert finding.rows == ["2008-09-17 close 0.14"]
    assert finding.verdict == ("the history came back: 1 row dated 2008-09-17 "
                               "to 2008-09-17")
    assert len(finding.attempts) == 1


def test_a_file_that_stops_before_the_suspension_does_not_stop_the_probe(
        tmp_path, monkeypatch):
    # The row below is filler on a real date. What is being judged is that rows
    # short of the suspension neither end the questioning nor turn the exit
    # status green, and that the verdict names what did come back.
    archive = _an_archive(tmp_path, {
        "data/daily/us/nyse stocks/1/leh.us.txt":
            BULK_HEADER + b"LEH.US,D,20071231,000000,65.0,65.5,64.5,65.44,1,0\n",
    })
    monkeypatch.setattr(probe, "fetch", _always(archive))
    finding = probe.probe_stooq_bulk_file(tmp_path)
    assert finding.served is False
    assert finding.rows == ["2007-12-31 close 65.44"]
    assert finding.verdict == (
        "rows came back and the history did not: 1 row dated 2007-12-31 to "
        "2007-12-31, none of them in 2008-09, the month the trading stopped")
    assert len(finding.attempts) == 6


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
