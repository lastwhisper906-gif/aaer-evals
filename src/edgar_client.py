"""One door to EDGAR: the rate limit, the declared contact, compression, and a
cache of filed documents that refuses bytes it did not first store.

The first item of the build order in `docs/HEDGE_FUND_ANALYSIS.md` §5.1. The
owner's decision of 2026-10-28 is that the repository does not hold every
company's filings: a run fetches what it needs when it needs it. This module is
the door every such fetch is to go through. The fetchers written before it read
the same variable but fall back to `fetch_fixtures.DEFAULT_USER_AGENT`; they
move onto this client in the later items of the build order, and a workflow that
runs one of them from then on sets `EDGAR_USER_AGENT` itself.

The SEC's page on accessing EDGAR data (read 2026-10-28,
https://www.sec.gov/search-filings/edgar-search-assistance/accessing-edgar-data)
sets the terms, quoted:

    Current max request rate: 10 requests/second.
    User-Agent: Sample Company Name AdminContact@<sample company domain>.com
    Accept-Encoding: gzip, deflate

**The rate limit.** Requests start at least `MIN_INTERVAL` seconds apart, on one
clock for every host, so no one-second window holds more than ten. `throttle` is
shared by every client in the process: two clients built in one run, or threads
sharing one, still keep one pace.

**The declared contact.** The User-Agent is read from `EDGAR_USER_AGENT` and
from nowhere else, and it must have the page's shape: a name, then a contact
address. There is no default in this module, so no session declares someone
else's contact by copying one; an unset, blank or shapeless value is refused
before any request is made.

**Compression.** Requests ask for gzip and deflate, as the page's sample does;
a compressed answer is unpacked before anything reads or hashes it, so a hash is
always of the document as filed.

**Retries.** EDGAR answers a client over its rate with 403 as well as 429, so
403, 429 and the 5xx answers are retried after 1, 2 and 4 seconds before they
are believed; every other status is raised at once.

**The cache of filed documents.** An accession never changes once disseminated
(an amendment is a new accession), so a filed document is fetched once and kept
at `<root>/edgar/<cik>/<accession>/<name>` beside `<name>.sha256`. The root is
`AAER_CACHE`, default `~/.cache/aaer-evals`, never inside the repository. A
cached file is read only when its bytes still hash to what was stored with them;
one that does not, or a file or a hash standing without the other, is refused
with `CacheMismatch`, never fetched over and never repaired. When the caller
knows the sha256 the record expects (a fixture manifest's row), a fetched
document that differs is refused and nothing is written. The cache is speed;
what a run's agents saw is still committed in the run directory.

The submissions index and company facts change as a company files, so they are
not cached here; their readers (the next items of the build order) filter them
to a run's cutoff.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import os
import re
import threading
import time
import urllib.error
import urllib.request
import zlib
from pathlib import Path

USER_AGENT_VARIABLE = "EDGAR_USER_AGENT"
CACHE_VARIABLE = "AAER_CACHE"
DEFAULT_CACHE = Path.home() / ".cache" / "aaer-evals"
# ten requests a second at most, with room for the clock's own jitter
MIN_INTERVAL = 0.11
RETRIED = (403, 429, 500, 502, 503, 504)
BACKOFF_SECONDS = (1, 2, 4)
TIMEOUT_SECONDS = 60
ACCEPT_ENCODING = "gzip, deflate"
# the page's shape: a name, a space, then an address with a dotted domain
DECLARED_CONTACT = re.compile(r"\S.*\s[^\s@]+@[^\s@]+\.[^\s@]+")
ACCESSION = re.compile(r"\d{10}-\d{2}-\d{6}")
CIK = re.compile(r"\d{1,10}")
# a document's name inside its accession folder: no path, no parent
NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")


class EdgarError(Exception):
    """The client refused, or EDGAR did not answer with a document."""


class MissingContact(EdgarError):
    """`EDGAR_USER_AGENT` is unset, blank, or not a name and an address."""


class CacheMismatch(EdgarError):
    """Cached or fetched bytes are not the bytes on record."""


class Throttle:
    """The start of each request at least `interval` seconds after the last."""

    def __init__(self, interval: float = MIN_INTERVAL, clock=time.monotonic,
                 sleep=time.sleep) -> None:
        self.interval = interval
        self._clock = clock
        self._sleep = sleep
        self._last = None
        self._lock = threading.Lock()

    def wait(self) -> None:
        with self._lock:
            now = self._clock()
            if self._last is not None:
                gap = self._last + self.interval - now
                if gap > 0:
                    self._sleep(gap)
                    now = self._clock()
            self._last = now


throttle = Throttle()


def contact(environ=None) -> str:
    """The declared contact, from `EDGAR_USER_AGENT` only."""
    value = (os.environ if environ is None else environ).get(USER_AGENT_VARIABLE, "").strip()
    if not value:
        raise MissingContact(f"{USER_AGENT_VARIABLE} is not set: EDGAR refuses a request "
                             "with no declared contact, and this client fills in none")
    if not DECLARED_CONTACT.fullmatch(value):
        raise MissingContact(f"{USER_AGENT_VARIABLE} is not a name followed by a contact "
                             "address, the shape the SEC's page asks for")
    return value


def cache_root(environ=None) -> Path:
    value = (os.environ if environ is None else environ).get(CACHE_VARIABLE, "")
    return Path(value).expanduser() if value.strip() else DEFAULT_CACHE


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def unpacked(body: bytes, encoding: str) -> bytes:
    """The body as served before the transfer compressed it."""
    if encoding == "gzip":
        return gzip.decompress(body)
    if encoding == "deflate":
        # HTTP's deflate is zlib-wrapped; some servers send it raw
        try:
            return zlib.decompress(body)
        except zlib.error:
            return zlib.decompress(body, -zlib.MAX_WBITS)
    if encoding in ("", "identity"):
        return body
    raise EdgarError(f"an answer compressed as {encoding!r}, which was not asked for")


class EdgarClient:
    """Every EDGAR request of the pipeline goes through one of these."""

    def __init__(self, *, environ=None, pace: Throttle | None = None,
                 sleep=time.sleep, opener=None) -> None:
        self.user_agent = contact(environ)
        self.root = cache_root(environ)
        self.pace = pace or throttle
        self._sleep = sleep
        self._open = opener or urllib.request.urlopen

    def get(self, url: str) -> bytes:
        """The body EDGAR serves at `url`, unpacked, after at most three retries."""
        for attempt in range(len(BACKOFF_SECONDS) + 1):
            last = attempt == len(BACKOFF_SECONDS)
            self.pace.wait()
            request = urllib.request.Request(url, headers={
                "User-Agent": self.user_agent, "Accept-Encoding": ACCEPT_ENCODING})
            try:
                with self._open(request, timeout=TIMEOUT_SECONDS) as response:
                    body = response.read()
                    encoding = (response.headers.get("Content-Encoding") or "").strip().lower()
            except urllib.error.HTTPError as error:
                if error.code in RETRIED and not last:
                    self._sleep(BACKOFF_SECONDS[attempt])
                    continue
                raise EdgarError(f"{url}: HTTP {error.code}") from None
            except urllib.error.URLError as error:
                if not last:
                    self._sleep(BACKOFF_SECONDS[attempt])
                    continue
                raise EdgarError(f"{url}: {error.reason}") from None
            return unpacked(body, encoding)
        raise EdgarError(f"{url}: no answer")    # not reached

    def get_json(self, url: str):
        try:
            return json.loads(self.get(url))
        except ValueError:
            raise EdgarError(f"{url}: the answer is not JSON") from None

    def document(self, url: str, *, cik: str, accession: str, name: str,
                 expected_sha256: str | None = None) -> Path:
        """A filed document as a local file whose bytes are the ones on record.

        Read from the cache when it holds the document and its bytes still hash
        to what was stored (and to `expected_sha256`, when given); fetched and
        stored once otherwise. Anything else is refused, and nothing is written.
        """
        if not CIK.fullmatch(str(cik)) or not ACCESSION.fullmatch(accession) \
                or not NAME.fullmatch(name) or name.endswith(".sha256"):
            raise EdgarError(f"not a document address: {cik!r} {accession!r} {name!r}")
        folder = self.root / "edgar" / str(int(cik)) / accession
        path, stamp = folder / name, folder / f"{name}.sha256"
        if path.exists() or stamp.exists():
            recorded = stamp.read_text(encoding="ascii").strip() if stamp.exists() else ""
            actual = sha256(path.read_bytes()) if path.exists() else ""
            if not recorded or actual != recorded:
                raise CacheMismatch(f"{path}: the cached bytes hash to {actual or 'nothing'}, "
                                    f"not to the {recorded or 'missing'} hash stored with them")
            if expected_sha256 and actual != expected_sha256:
                raise CacheMismatch(f"{path}: cached as {actual}, the record expects "
                                    f"{expected_sha256}")
            return path
        body = self.get(url)
        actual = sha256(body)
        if expected_sha256 and actual != expected_sha256:
            raise CacheMismatch(f"{url}: EDGAR served {actual}, the record expects "
                                f"{expected_sha256}; nothing was stored")
        folder.mkdir(parents=True, exist_ok=True)
        partial = folder / f".{name}.partial"
        partial.write_bytes(body)
        partial.replace(path)
        stamp.write_text(actual + "\n", encoding="ascii")
        return path
