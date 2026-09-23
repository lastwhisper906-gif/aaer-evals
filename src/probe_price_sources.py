"""Ask the three candidate price sources for a delisted ticker's history.

Read-only, and no account is opened. The three candidates are sent no
credentials; the configured backends are sent whatever credential this
environment holds, and no credential value is ever printed -- every one this
environment holds is replaced by its variable's name before a backend's answer
is shown.

The market module is built against a frozen price fixture because the price
source is unchosen, and it is unchosen because the question that decides it has
never been asked of the sources themselves: does a candidate serve the history
of a company that stopped trading? A universe drawn from a past date is full of
them. A source that quietly drops them turns a study of accounting failures into
a study of the survivors, and the drop is silent -- the request succeeds and the
rows are simply not there.

This script asks. It gathers the evidence; it does not pick the source.

Two halves, and the second one was added when the source was picked
-------------------------------------------------------------------

The first half is unchanged: the three candidates asked with **no credentials**,
which is what a stranger can learn about them and is the evidence
`docs/needs_judgment.md` recorded. The second half asks the **configured
backends** in `src/prices/` -- crsp, tiingo, eodhd -- with whatever credential
the environment actually holds, and it asks about two delistings rather than
one, because one delisting cannot tell a source's coverage from its silence:

* **Lehman Brothers Holdings, LEH, 2008.** The Tiingo free tier is *documented*
  as starting its delisted history around 2015, so a refusal here is the answer
  the tier's own documentation predicts. It is recorded as an expected refusal
  and it is not a failure of the backend or of the probe. Recording it as a
  failure would be scoring a source against a claim it never made.
* **Activision Blizzard, ATVI, delisted 2023-10-13** on the Microsoft
  acquisition. This one is after 2015, so it is what the forward-track backend
  *does* claim, and a refusal here is the backend failing what it says it does.

That is the whole reason there are two: a backend is judged on what it claims,
and the only way to do that is to ask it one question inside its claim and one
outside it.

A backend with no credential in the environment is recorded as **unconfigured**.
That is a finding -- it says the switch is off and why -- and it is not a
failure. Nothing here ever writes a credential down: `src/secret_scan.py` fails
the gate if one reaches a file in this tree.

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

It sends the three candidates no credentials. A candidate that needs an account
is recorded as needing one, and that is a finding rather than a failure of the
probe.

It does not answer Stooq's browser check. That page asks the caller to find a
hash with four leading zeroes and post the nonce back, and a script that does
that is a tool for getting around a block the site put there on purpose. The
block is what gets reported.

    .venv/bin/python src/probe_price_sources.py

Exit 0 a delisted company's history came back -- rows reaching the month that
company stopped trading -- and the report names the ticker and the candidate
that served it, 1 no candidate served one, 2 no source answered at all so
nothing was learned, 3 the wrong interpreter. A backend that refused a delisting
it never claimed to carry does not move the status: an expected refusal is not a
failure, and a probe whose exit status cannot tell the two apart is a probe
nobody reads. Nor does a backend whose request never reached the source -- a
timeout or a refused connection on this machine says nothing about the source.
"""

from __future__ import annotations

import dataclasses
import datetime
import itertools
import json
import math
import os
import re
import sys
import tempfile
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

try:
    from src import interpreter_pin, secret_scan
except ImportError:  # invoked as a plain script: python3.12 src/probe_price_sources.py
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import interpreter_pin, secret_scan

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

    `ticker` and `month` are the delisting this request asked about and the
    month its rows have to reach. The three candidates ask about LEH alone; the
    configured backends ask about two, and rows for Activision Blizzard judged
    against Lehman's month would be called short of a suspension they were
    never about.

    `never_reached` marks a request that was sent and got no answer -- a
    timeout, a refused connection. It is kept apart from a request never sent
    because no credential was configured: both leave `reached` False, and only
    the second says the switch is off.
    """

    url: str
    agent: str
    answer: str
    rows: list[str]
    reached: bool
    ticker: str = TICKER
    month: str = LAST_MONTH_TRADED
    never_reached: bool = False


@dataclasses.dataclass
class Finding:
    """What one candidate answered, and whether the history came back."""

    candidate: str
    attempts: list[Attempt]
    verdict: str

    @property
    def shown(self) -> Attempt | None:
        """The attempt the verdict speaks of.

        The first whose rows reach the month its own delisting stopped trading,
        or failing that the first that carried any rows at all -- so a candidate
        is never reported short of the delisting because an earlier request
        answered with less.
        """
        with_rows = [attempt for attempt in self.attempts if attempt.rows]
        for attempt in with_rows:
            if reached_the_delisting(attempt.rows, attempt.month):
                return attempt
        return with_rows[0] if with_rows else None

    @property
    def rows(self) -> list[str]:
        shown = self.shown
        return shown.rows if shown else []

    @property
    def served(self) -> bool:
        """A delisted ticker's history came back.

        Rows on their own are not enough. They have to reach the month that
        ticker's trading stopped, or they are not the history of a company that
        stopped trading.
        """
        shown = self.shown
        return shown is not None and reached_the_delisting(shown.rows, shown.month)

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


def reached_the_delisting(rows: list[str], month: str = LAST_MONTH_TRADED) -> bool:
    """True when the rows reach the month the ticker stopped trading."""
    return any(row.startswith(month) for row in rows)


def what_came_back(rows: list[str], month: str = LAST_MONTH_TRADED) -> str:
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
    if reached_the_delisting(rows, month):
        return f"the history came back: {span}"
    return (f"rows came back and the history did not: {span}, none of them in "
            f"{month}, the month the trading stopped")


def finish(candidate: str, attempts: list[Attempt], otherwise: str) -> Finding:
    """The finding for a candidate that is done being asked.

    What came back outranks any verdict written in advance: rows decide the
    verdict when rows came, and `otherwise` is what to say when none did.
    """
    finding = Finding(candidate, attempts, otherwise)
    shown = finding.shown
    if shown is None:
        return finding
    return dataclasses.replace(
        finding, verdict=what_came_back(shown.rows, shown.month))


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


# --- the configured backends ------------------------------------------------
#
# The half added when the source was picked. Everything above asks a stranger's
# question; everything below asks with whatever credential the environment
# holds.


@dataclasses.dataclass(frozen=True)
class Delisting:
    """One company that stopped trading, and the month its rows have to reach."""

    ticker: str
    company: str
    last_month_traded: str
    day: str
    note: str


DELISTINGS = (
    Delisting(
        ticker=TICKER,
        company=COMPANY,
        last_month_traded=LAST_MONTH_TRADED,
        day="2008-09-17",
        note=DELISTING,
    ),
    Delisting(
        ticker="ATVI",
        company="Activision Blizzard, Inc.",
        last_month_traded="2023-10",
        day="2023-10-13",
        note="acquired by Microsoft Corporation; the last trading day was "
             "2023-10-13 and the shares were removed from listing after it",
    ),
)

# What each backend says about each delisting, read off the provider's own
# documentation and not off a run. A refusal inside a claim is a failure of the
# backend; a refusal outside one is the documentation being right.
CLAIMS_TO_SERVE = {
    ("tiingo", "LEH"): False,
    ("tiingo", "ATVI"): True,
    ("eodhd", "LEH"): True,
    ("eodhd", "ATVI"): True,
    ("crsp", "LEH"): True,
    ("crsp", "ATVI"): True,
}

WHY_NOT_CLAIMED = ("the free tier's delisted history starts around 2015, so "
                   "this delisting is before anything it says it holds")


def claims_to_serve(backend_name: str, ticker: str) -> bool:
    """Whether that backend's own documentation says it carries that history."""
    return CLAIMS_TO_SERVE.get((backend_name, ticker), True)


def rows_of(frame: list[dict]) -> list[str]:
    """A price frame in the one row shape this report prints.

    The same shape every candidate above prints, so a reader compares a backend
    with a bare request without translating between two formats.
    """
    return [f"{entry['date'].isoformat()} close {entry['close']!r}" for entry in frame]


def delisting_returns_in(frame: list[dict]) -> list[str]:
    """One line per row that carried a delisting return, which is the whole point.

    A source that serves the rows and not the return is the survivorship
    problem one step further along: the history looks complete and the day that
    decides the study is flat. So the two are reported separately and a source
    is never credited with the second for having the first.
    """
    return [
        f"{entry['date'].isoformat()} delisting return {entry['delisting_return']!r}"
        f" code {entry['delisting_code']!r}"
        for entry in frame
        if entry.get("delisting_return") is not None
    ]


# A credential written into a query string, as EODHD takes its token. Matched by
# the same names `src/secret_scan.py` watches for.
QUERY_CREDENTIAL = re.compile(rf"([?&]{secret_scan.NAMES}=)[^&\s'\"<>]+",
                              re.IGNORECASE)


def redacted(text: str, environ: dict[str, str] | None = None) -> str:
    """Text with every credential this environment holds replaced by its name.

    A backend's error is printed, and an error can carry its request: EODHD
    takes its token in the query string, so a connection to it that fails is
    reported by `requests` with the address, token and all. Every value of a
    variable `src/secret_scan.py` watches is replaced by that variable's name,
    and whatever is left after a credential's name in a query string is replaced
    too -- `requests` percent-encodes the address, so a token carrying a
    character it encodes no longer matches its own value there. Both happen
    before the text is cut short, because half a token is not the value being
    looked for.
    """
    source = os.environ if environ is None else environ
    for name in secret_scan.CREDENTIAL_VARIABLES:
        value = source.get(name, "").strip()
        if value:
            text = text.replace(value, f"${name}")
    return QUERY_CREDENTIAL.sub(r"\1<redacted>", text)


def never_reached_the_source(error: BaseException) -> bool:
    """True when a request got no answer at all: a timeout, a refused connection.

    `requests` raises its own classes for both, and they are not the built-in
    ones. A body that would not decode is a `requests` exception too, and that
    one is an answer -- the source sent something that is not a price history --
    so the classes are named rather than caught by their common parent.

    What is not told apart: a WRDS connection that fails. The `wrds` package
    raises the same class for a refused password, which is the source's answer,
    as for a host that never answered, so a CRSP failure is counted as an answer.
    """
    try:
        from requests import exceptions
    except ImportError:
        wire: tuple[type[BaseException], ...] = ()
    else:
        wire = (exceptions.ConnectionError, exceptions.Timeout)
    return isinstance(error, wire + (ConnectionError, TimeoutError))


def ask_one_backend(module, delisting: Delisting) -> Attempt:
    """One backend, one delisting, and the one line this report has to say.

    Four outcomes, and they are not the same thing:

    * **unconfigured** -- no credential in this environment, so it was never
      asked. `reached` is False: nothing was learned about the source.
    * **never reached** -- asked, and no answer came: a timeout or a refused
      connection on this machine. `reached` is False, because that is a fact
      about this machine and not about the source.
    * **answered** -- rows came back, or a refusal did. `reached` is True either
      way, because a refusal from the source is a fact about the source.
    * **refused as documented** -- it answered, the history did not come, and
      its own documentation said it would not. Reported as expected.

    Whatever the backend said is passed through `redacted` before it is shown.
    """
    from src import prices

    name = module.NAME
    where = f"{name} asked for {delisting.ticker} through {delisting.day}"
    start = datetime.date(int(delisting.day[:4]) - 1, 1, 1)
    end = datetime.date.fromisoformat(delisting.day)
    about = {"ticker": delisting.ticker, "month": delisting.last_month_traded}
    expected = "" if claims_to_serve(name, delisting.ticker) else (
        f", which is expected: {WHY_NOT_CLAIMED}")
    try:
        frame = module.history(delisting.ticker, start, end)
    except prices.Unconfigured as reason:
        return Attempt(where, name, f"{where} -- unconfigured: {reason}", [], False,
                       **about)
    except Exception as error:  # a refusal, a timeout, a shape nobody expected
        said = f"{type(error).__name__}: {redacted(str(error))[:200]}"
        if never_reached_the_source(error):
            return Attempt(where, name, f"{where} -- no answer at all: {said}", [],
                           False, **about, never_reached=True)
        return Attempt(where, name, f"{where} -- {said}{expected}", [], True,
                       **about)
    rows = rows_of(frame)
    returns = delisting_returns_in(frame)
    answer = f"{where} -- {len(rows)} row(s)"
    if returns:
        answer = f"{answer}, {len(returns)} carrying a delisting return"
    else:
        answer = f"{answer}, none carrying a delisting return"
    if not reached_the_delisting(rows, delisting.last_month_traded):
        answer = (f"{answer}, none of them in {delisting.last_month_traded}, the "
                  f"month the trading stopped{expected}")
    return Attempt(where, name, answer, rows, True, **about)


def probe_configured_backends(workspace: Path) -> Finding:
    """Every backend in `src/prices/`, put to both delistings.

    `workspace` is unused: a backend writes nothing to disk. It is in the
    signature so this reads like every other candidate and can stand in the same
    list.
    """
    from src import prices

    attempts = [
        ask_one_backend(prices.backend(name), delisting)
        for name in prices.BACKENDS
        for delisting in DELISTINGS
    ]
    asked = sorted({
        attempt.agent for attempt in attempts
        if attempt.reached or attempt.never_reached
    })
    if not asked:
        otherwise = ("no backend is configured in this environment, so nothing "
                     "was asked and nothing was learned about any of them; the "
                     "line for each backend above says why")
    else:
        otherwise = (f"asked: {', '.join(asked)}. None served a delisting's "
                     f"history to the month the trading stopped")
    finding = finish("the configured backends in src/prices", attempts, otherwise)
    shown = finding.shown
    if shown is None:
        return finding
    return dataclasses.replace(
        finding, verdict=f"{shown.agent} for {shown.ticker}: {finding.verdict}")


CANDIDATES = (probe_stooq_bulk_file, probe_wrds_crsp,
              probe_low_cost_provider, probe_configured_backends)


def report(finding: Finding) -> None:
    print(f"\n{finding.candidate}")
    user_agents = {label for label, _ in AGENTS}
    for attempt in finding.attempts:
        # A bare request is labelled by the user agent it went out under; a
        # configured backend by its own name, which is not a user agent.
        who = (f"{attempt.agent} user agent" if attempt.agent in user_agents
               else attempt.agent)
        print(f"  {attempt.url}")
        print(f"    [{who}] {attempt.answer}")
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
    print("The three candidates are asked with no credentials at all, which is "
          "what a stranger can learn about them. The configured backends in "
          "src/prices are then asked with whatever credential this environment "
          "holds, about two delistings rather than one -- LEH in 2008 and "
          "Activision Blizzard, ATVI, on 2023-10-13 -- so a backend is judged "
          "on what it claims rather than on what it never claimed. A backend "
          "with no credential here is recorded as unconfigured, which is a "
          "finding and not a failure.")
    print("The candidates are asked in order and the probe stops at the first "
          "that serves the history.")

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
        print(f"{served[0].shown.ticker} history came back from "
              f"{served[0].candidate}. "
              f"{len(CANDIDATES) - len(findings)} candidate(s) not probed.")
        return 0
    if not any(finding.answered for finding in findings):
        print("No candidate answered at all -- this machine reached none of "
              "them, so the probe learned nothing about any source.")
        return NOTHING_ANSWERED
    later = ", ".join(one.ticker for one in DELISTINGS if one.ticker != TICKER)
    print(f"No candidate served {TICKER}'s history, and no configured backend "
          f"served {later}'s. Each verdict above is what the source itself "
          f"answered, or says that it was never asked.")
    return NO_HISTORY


if __name__ == "__main__":
    sys.exit(main())
