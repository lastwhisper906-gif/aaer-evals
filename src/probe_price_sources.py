"""Ask the three candidate price sources for a delisted ticker's history.

Read-only. No credentials are sent and no account is opened.

The market module is built against a frozen price fixture because the price
source is unchosen, and it is unchosen because the question that decides it has
never been asked of the sources themselves: does a candidate serve the history
of a company that stopped trading? A universe drawn from a past date is full of
them. A source that quietly drops them turns a study of accounting failures into
a study of the survivors, and the drop is silent -- the request succeeds and the
rows are simply not there.

This script asks. It gathers the evidence; it does not pick the source.

The delisted ticker
-------------------

Lehman Brothers Holdings Inc., New York Stock Exchange ticker LEH. It filed its
petition under Chapter 11 on 2008-09-15. The Exchange suspended the securities
from trading on 2008-09-17 and applied to the Commission for their removal from
listing and registration; the common stock closed at fourteen cents on the day
of the suspension. A source that serves this history returns daily rows for LEH
that run into September 2008 and stop there. Rows that stop before that month
are reported as what they are -- rows came back and the history did not -- and
leave the exit status where it was.

Whether they come back is the source's answer and not this script's. The rows
are printed as they arrive and the exit status says whether any candidate
produced them.

The candidates, in the order the needs-judgment list gives them
--------------------------------------------------------------

1. the Stooq daily bulk file -- a file download rather than an API call, which
   is the reason it was thought to survive the block that stopped the scripted
   request.
2. WRDS with CRSP through a Stony Brook account -- delisting returns handled the
   way the literature handles them.
3. a low-cost provider -- EODHD and Tiingo.

The probe stops at the first candidate that returns the history.

What it will not do
-------------------

It sends no credentials. A candidate that needs an account is recorded as
needing one, and that is a finding rather than a failure of the probe.

It does not answer Stooq's browser check. That page asks the caller to find a
hash with four leading zeroes and post the nonce back, and a script that does
that is a tool for getting around a block the site put there on purpose. The
block is what gets reported.

    python3.12 src/probe_price_sources.py

Exit 0 the history came back and the report names the candidate that served it,
1 no candidate served it, 2 no source answered at all so nothing was learned,
3 the wrong interpreter.
"""

from __future__ import annotations

import dataclasses
import datetime
import itertools
import json
import math
import re
import sys
import tempfile
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

try:
    from src import interpreter_pin
except ImportError:  # invoked as a plain script: python3.12 src/probe_price_sources.py
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import interpreter_pin

TICKER = "LEH"
COMPANY = "Lehman Brothers Holdings Inc."
DELISTING = ("Chapter 11 petition 2008-09-15; the New York Stock Exchange "
             "suspended trading 2008-09-17 and applied to remove the securities "
             "from listing and registration")
# The month the rows have to reach, written the way a row dates itself. A
# source that answers with LEH rows ending in 2006 has not served the history of
# a company that traded until the suspension; the delisting fixes that month,
# not this probe.
LAST_MONTH_TRADED = "2008-09"

# Session 1 found the block under both of these. The pair is kept because the
# open question is the bulk file rather than the user agent, and an answer that
# differs between the two would say so on the spot.
AGENTS = (
    ("plain", "aaer-evals price source probe"),
    ("browser", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"),
)

TIMEOUT_SECONDS = 90
# The daily bulk file is tens of megabytes. The cap is what keeps a redirect to
# something enormous from filling the disk, not a limit on the real file.
MAX_DOWNLOAD_BYTES = 600 * 1024 * 1024
READ_CHUNK = 1 << 20
# Enough of a body to recognise what it is. The browser check names itself 190
# bytes in, so a window that only just clears it would be a window that stops
# clearing it the day the page gains an attribute.
PEEK_BYTES = 4096
# A body this small is quoted whole in the report; anything longer is described.
SHOWN_BYTES = 200

NO_HISTORY = 1
NOTHING_ANSWERED = 2

BROWSER_CHECK = re.compile(
    rb"requires JavaScript to verify your browser|crypto\.subtle\.digest")
DATE_FIELDS = ("date", "Date", "priceDate")
CLOSE_FIELDS = ("close", "Close", "adjusted_close", "adjClose")


@dataclasses.dataclass
class Reply:
    """What came back from one request, before anyone reads it."""

    url: str
    status: int | None
    final_url: str
    headers: dict[str, str]
    path: Path | None
    size: int
    error: str | None


@dataclasses.dataclass
class Attempt:
    """One request and the one line this report has to say about it.

    `reached` is whether the source answered at all, refusal included. A machine
    with no network refuses every request too, and a probe that could not tell
    the two apart would report a block that nobody imposed.
    """

    url: str
    agent: str
    answer: str
    rows: list[str]
    reached: bool


@dataclasses.dataclass
class Finding:
    """What one candidate answered, and whether the history came back."""

    candidate: str
    attempts: list[Attempt]
    verdict: str

    @property
    def rows(self) -> list[str]:
        for attempt in self.attempts:
            if attempt.rows:
                return attempt.rows
        return []

    @property
    def served(self) -> bool:
        """The delisted ticker's history came back.

        Rows on their own are not enough. They have to reach the month the
        trading stopped, or they are not the history of a company that stopped
        trading.
        """
        return reached_the_delisting(self.rows)

    @property
    def answered(self) -> bool:
        return any(attempt.reached for attempt in self.attempts)


def spill(stream, workspace: Path) -> tuple[Path, int]:
    """Write a response body to a file under workspace. Returns the path and size."""
    handle = tempfile.NamedTemporaryFile(dir=workspace, delete=False, suffix=".body")
    size = 0
    with handle:
        while size < MAX_DOWNLOAD_BYTES:
            chunk = stream.read(READ_CHUNK)
            if not chunk:
                break
            handle.write(chunk)
            size += len(chunk)
    return Path(handle.name), size


def fetch(url: str, agent: str, workspace: Path) -> Reply:
    """One request. An HTTP error is an answer and is recorded as one."""
    request = urllib.request.Request(
        url, headers={"User-Agent": agent, "Accept-Encoding": "identity"})
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            path, size = spill(response, workspace)
            return Reply(url, response.status, response.url,
                         dict(response.headers), path, size, None)
    except urllib.error.HTTPError as error:
        path, size = spill(error, workspace)
        return Reply(url, error.code, error.url, dict(error.headers),
                     path, size, None)
    except (urllib.error.URLError, OSError) as error:
        return Reply(url, None, url, {}, None, 0, str(error))


def head(reply: Reply, limit: int = PEEK_BYTES) -> bytes:
    """The first bytes of a body, enough to tell prices from a refusal."""
    if reply.path is None:
        return b""
    with reply.path.open("rb") as handle:
        return handle.read(limit)


def body(reply: Reply, limit: int = 8 * 1024 * 1024) -> bytes:
    """A whole body, when it is small enough to parse in memory."""
    if reply.path is None or reply.size > limit:
        return b""
    return reply.path.read_bytes()


def is_browser_check(text: bytes) -> bool:
    """True for the page that asks the caller to solve a hash puzzle first."""
    return bool(BROWSER_CHECK.search(text))


def history_rows(text: bytes) -> list[str]:
    """The dated daily rows in a price answer, whatever shape it arrived in.

    Three shapes turn up. Stooq's bulk members head their columns
    <TICKER>,<PER>,<DATE>,<TIME>,<OPEN>,<HIGH>,<LOW>,<CLOSE>,<VOL>,<OPENINT>
    and date a row 20080917; its per-ticker download and a csv from EODHD head
    them Date,Open,High,Low,Close and date a row 2008-09-17; EODHD and Tiingo
    also serve a list of objects each carrying a date and a close. All three are
    read here because the probe has to say the same thing about each: these are
    the rows that came back.

    The columns are found by their names in the header rather than by position,
    so a source that orders them its own way is still read correctly. A body
    carrying dates and no prices yields nothing, which is the answer that
    matters: a block page with a copyright year, an error object whose message
    is a date, a row whose close reads "unavailable".
    """
    decoded = text.decode("utf-8", "replace")
    rows = _rows_from_objects(decoded)
    if rows:
        return rows
    return _rows_from_table(decoded)


def _rows_from_objects(text: str) -> list[str]:
    try:
        parsed = json.loads(text)
    except (ValueError, RecursionError):
        return []
    if not isinstance(parsed, list):
        return []
    rows = []
    for entry in parsed:
        if not isinstance(entry, dict):
            continue
        row = _row(_first(entry, DATE_FIELDS), _first(entry, CLOSE_FIELDS))
        if row:
            rows.append(row)
    return rows


def _first(entry: dict, names: tuple[str, ...]):
    for name in names:
        if entry.get(name) is not None:
            return entry[name]
    return None


def _rows_from_table(text: str) -> list[str]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    for index, line in enumerate(lines):
        columns = [_column(name) for name in line.split(",")]
        if "date" not in columns or "close" not in columns:
            continue
        day_at, close_at = columns.index("date"), columns.index("close")
        rows = []
        for row in lines[index + 1:]:
            fields = [field.strip() for field in row.split(",")]
            if len(fields) != len(columns):
                continue
            row = _row(fields[day_at], fields[close_at])
            if row:
                rows.append(row)
        return rows
    return []


def _column(name: str) -> str:
    """A header name as the columns are matched.

    Stooq's bulk file writes its column names inside angle brackets: <DATE>,
    <CLOSE>. Everyone else writes them plainly, in whatever case they like.
    """
    return name.strip().strip("<>").lower()


def _row(day, close) -> str | None:
    """One daily row, or None when the pair is not a dated price.

    Both halves have to be real, and this is the one place that says so: a date
    with a message where the price belongs is not a row, and neither is a price
    on something that is not a date.
    """
    day, close = _day(day), _price(close)
    return f"{day} close {close}" if day and close else None


def _day(value) -> str | None:
    """A trading date written 2008-09-17, or None when the field is not a date.

    Stooq's bulk file dates a row 20080917, Tiingo dates it with a time after
    it, and the rest write the date alone. All of them come back in one form, so
    a row reads the same whichever source sent it.
    """
    if value is None:
        return None
    try:
        return datetime.date.fromisoformat(str(value).strip()[:10]).isoformat()
    except ValueError:
        return None


def _price(value) -> str | None:
    """A close as the source wrote it, or None when it is not a number.

    A payload shaped like a price row but carrying no price -- a date beside a
    close reading "unavailable" -- would otherwise be counted as history, and
    the probe would exit green on an error message.
    """
    if value is None:
        return None
    text = str(value).strip()
    try:
        number = float(text)
    except ValueError:
        return None
    return text if math.isfinite(number) else None


def reached_the_delisting(rows: list[str]) -> bool:
    """True when the rows reach the month the ticker stopped trading."""
    return any(row.startswith(LAST_MONTH_TRADED) for row in rows)


def what_came_back(rows: list[str]) -> str:
    """The verdict for a candidate that returned rows: how many, over what span.

    A source that answers with three days has not served fifteen years, and a
    verdict reading only "the history came back" would say the same for both.
    Whether a span is enough for a study is not this probe's question and is not
    answered here -- the span is reported. The one part of it the delisting
    itself fixes is answered: rows that never reach the month the trading
    stopped are not the history of a company that stopped trading.
    """
    days = sorted(row.split()[0] for row in rows)
    count = f"{len(rows)} row" if len(rows) == 1 else f"{len(rows)} rows"
    span = f"{count} dated {days[0]} to {days[-1]}"
    if reached_the_delisting(rows):
        return f"the history came back: {span}"
    return (f"rows came back and the history did not: {span}, none of them in "
            f"{LAST_MONTH_TRADED}, the month the trading stopped")


def finish(candidate: str, attempts: list[Attempt], otherwise: str) -> Finding:
    """The finding for a candidate that is done being asked.

    What came back outranks any verdict written in advance: rows decide the
    verdict when rows came, and `otherwise` is what to say when none did.
    """
    finding = Finding(candidate, attempts, otherwise)
    if not finding.rows:
        return finding
    return dataclasses.replace(finding, verdict=what_came_back(finding.rows))


def describe(reply: Reply) -> str:
    """One line naming what came back, plainly enough to be quoted in a report."""
    if reply.status is None:
        return f"no answer at all: {reply.error}"
    parts = [f"status {reply.status}", f"{reply.size} bytes"]
    if reply.final_url != reply.url:
        parts.append(f"redirected to {reply.final_url}")
    challenge = next((value for name, value in reply.headers.items()
                      if name.lower() == "www-authenticate"), None)
    if challenge:
        parts.append(f"asks for a password: {challenge}")
    peek = head(reply)
    if is_browser_check(peek):
        parts.append("the browser check page, a hash puzzle to answer before "
                     "anything is served")
    elif peek and reply.size <= SHOWN_BYTES:
        parts.append(f"body: {peek.decode('utf-8', 'replace').strip()}")
    return ", ".join(parts)


def asks_for_the_delisted_ticker(url: str) -> bool:
    """True when this request asks for the delisted ticker rather than a control.

    The control on a demonstration token is a listed ticker, and its rows are not
    the history this probe is looking for. Counting them would answer the wrong
    question with a green exit status, so the two are told apart here, where a
    test can reach it, rather than inside the loop that fetches them.
    """
    return f"/{TICKER}." in url or f"/{TICKER.lower()}/" in url


def rows_from_archive(reply: Reply) -> tuple[str | None, list[str]]:
    """The ticker's member of a downloaded archive, and one line about it.

    The note is None when the body is not an archive at all. When it is one and
    the ticker is missing from it, that is the finding the bulk file exists to
    answer -- the download worked and the delisted company is not in it -- so the
    note is kept and reported whether or not any rows came with it.
    """
    if reply.path is None or not zipfile.is_zipfile(reply.path):
        return None, []
    wanted = f"{TICKER.lower()}.us.txt"
    with zipfile.ZipFile(reply.path) as archive:
        names = archive.namelist()
        mine = [name for name in names if name.lower().endswith(wanted)]
        if not mine:
            return f"an archive of {len(names)} files, none named {wanted}", []
        return (f"{mine[0]}, inside an archive of {len(names)} files",
                history_rows(archive.read(mine[0])))


def probe_stooq_bulk_file(workspace: Path) -> Finding:
    """The daily bulk file, then the per-ticker request the block already stopped."""
    targets = (
        ("the bulk file's download link", "https://stooq.com/db/d/?b=d_us_txt"),
        ("the bulk file on the static host",
         "https://static.stooq.com/db/h/d_us_txt.zip"),
        (f"the per-ticker daily history for {TICKER}, the request session 1 probed",
         f"https://stooq.com/q/d/l/?s={TICKER.lower()}.us&i=d"),
    )
    attempts = []
    archives = []
    for (what, url), (label, agent) in itertools.product(targets, AGENTS):
        reply = fetch(url, agent, workspace)
        answer = f"{what} -- {describe(reply)}"
        rows = []
        if reply.status == 200:
            note, rows = rows_from_archive(reply)
            if note is not None:
                answer = f"{answer}, {note}"
                archives.append(note)
            elif not is_browser_check(head(reply)):
                rows = history_rows(body(reply))
        attempts.append(Attempt(url, label, answer, rows,
                                reply.status is not None))
        if reached_the_delisting(rows):
            break
    # A download that worked with the ticker missing from it is a different
    # answer from a block, and a verdict fixed in advance would have called it
    # one.
    verdict_if_nothing_came = (
        f"the file downloaded and {TICKER} is not in it: {archives[-1]}"
        if archives else
        "blocked before any data: the file download meets the same browser "
        "check as the scripted request, and the static host asks for a password")
    return finish("the Stooq daily bulk file", attempts, verdict_if_nothing_came)


def probe_wrds_crsp(workspace: Path) -> Finding:
    """WRDS with CRSP. No credentials are sent, so this can only find the door."""
    attempts = []
    for what, url in (
        ("the WRDS front door", "https://wrds-www.wharton.upenn.edu/"),
        ("the CRSP data page",
         "https://wrds-www.wharton.upenn.edu/pages/get-data/"
         "center-research-security-prices-crsp/"),
        ("the Stony Brook guide listing what the university subscribes to",
         "https://guides.library.stonybrook.edu/c.php?g=35362&p=10268260"),
    ):
        reply = fetch(url, AGENTS[1][1], workspace)
        answer = f"{what} -- {describe(reply)}"
        text = body(reply)
        if "stonybrook" in url and b"CRSP" in text:
            answer = f"{answer}, names CRSP among the sources available to its users"
        attempts.append(Attempt(url, AGENTS[1][0], answer, [],
                                reply.status is not None))
    return finish(
        "WRDS with CRSP through a Stony Brook account", attempts,
        "needs an account the owner must open: the data page redirects to a "
        "login, and no history can be requested without one")


def probe_low_cost_provider(workspace: Path) -> Finding:
    """EODHD and Tiingo, on the free credentials a stranger has -- which is none."""
    targets = (
        (f"EODHD asked for {TICKER} on its demonstration token",
         f"https://eodhd.com/api/eod/{TICKER}.US"
         "?api_token=demo&fmt=json&from=2008-01-01&to=2008-09-30"),
        ("EODHD asked for a listed ticker on the same token, to show the "
         "endpoint itself answers",
         "https://eodhd.com/api/eod/AAPL.US"
         "?api_token=demo&fmt=json&from=2024-01-02&to=2024-01-05"),
        (f"Tiingo asked for {TICKER} with no token",
         f"https://api.tiingo.com/tiingo/daily/{TICKER.lower()}/prices"
         "?startDate=2008-01-01&endDate=2008-09-30"),
    )
    attempts = []
    for what, url in targets:
        reply = fetch(url, AGENTS[0][1], workspace)
        rows = history_rows(body(reply)) if reply.status == 200 else []
        answer = f"{what} -- {describe(reply)}"
        if rows and not asks_for_the_delisted_ticker(url):
            # The control's rows say the endpoint answers. They are not the
            # history this probe asked for, and counting them would answer the
            # wrong question with a green exit status.
            answer, rows = f"{answer}, {len(rows)} rows", []
        attempts.append(Attempt(url, AGENTS[0][0], answer, rows,
                                reply.status is not None))
        if reached_the_delisting(rows):
            break
    return finish(
        "a low-cost provider", attempts,
        "needs an account the owner must open: the demonstration token is "
        "restricted to a fixed list of listed tickers and Tiingo serves nothing "
        "without one")


CANDIDATES = (probe_stooq_bulk_file, probe_wrds_crsp, probe_low_cost_provider)


def report(finding: Finding) -> None:
    print(f"\n{finding.candidate}")
    for attempt in finding.attempts:
        print(f"  {attempt.url}")
        print(f"    [{attempt.agent} user agent] {attempt.answer}")
    rows = finding.rows
    if rows:
        # Few enough rows to print whole is itself worth seeing: a source that
        # answers with three days has not served fifteen years. The count and
        # the span are in the verdict below.
        shown = rows if len(rows) <= 6 else rows[:3] + ["..."] + rows[-3:]
        for row in shown:
            print(f"    {row}")
    print(f"  verdict: {finding.verdict}")


def main() -> int:
    wrong_interpreter = interpreter_pin.enforce()
    if wrong_interpreter:
        return wrong_interpreter

    print(f"Probing for the price history of {COMPANY}, ticker {TICKER}.")
    print(f"Delisted: {DELISTING}.")
    print(f"A source that serves it returns daily rows reaching "
          f"{LAST_MONTH_TRADED}, the month the trading stopped.")
    print("No credentials are sent. The candidates are asked in order and the "
          "probe stops at the first that serves the history.")

    findings = []
    with tempfile.TemporaryDirectory(prefix="price-source-probe-") as directory:
        workspace = Path(directory)
        for candidate in CANDIDATES:
            finding = candidate(workspace)
            findings.append(finding)
            report(finding)
            if finding.served:
                break

    served = [finding for finding in findings if finding.served]
    print()
    if served:
        print(f"{TICKER} history came back from {served[0].candidate}. "
              f"{len(CANDIDATES) - len(findings)} candidate(s) not probed.")
        return 0
    if not any(finding.answered for finding in findings):
        print("No candidate answered at all -- this machine reached none of "
              "them, so the probe learned nothing about any source.")
        return NOTHING_ANSWERED
    print(f"No candidate served {TICKER}'s history. Each verdict above is what "
          f"the source itself answered.")
    return NO_HISTORY


if __name__ == "__main__":
    sys.exit(main())
