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

**The rate limit.** The SEC counts requests where they arrive, and a client can
only space what it sends; a connection that is slow to open would let a later
request catch up with it. So requests go **one at a time**: a request holds the
gate from before it is sent until its answer is read, and the next may start
only `MIN_INTERVAL` seconds after the last one started. A request arrives
before its answer is read, so it arrives before the next one starts, and eleven
requests in a row arrive across at least the nine gaps between the second and
the eleventh: 9 × 0.12 = 1.08 seconds, more than one. The gate is one per
machine, because the SEC counts by address: a thread lock inside the process
and a locked file (`GATE_FILE`, in the system's temporary directory) across
processes, so three runs fetching at once keep one pace between them. Every
attempt, retries included, takes the gate; a backoff waits outside it.

**No redirects.** EDGAR's documents and APIs are served where they are asked
for. A redirect is refused rather than followed: a followed hop would be a
request the gate never saw, and a document cached under one address would hold
another's bytes.

**The declared contact.** The User-Agent is read from `EDGAR_USER_AGENT` and
from nowhere else, and it must have the page's shape: a name, then a contact
address. There is no default in this module, so no session declares someone
else's contact by copying one; an unset, blank or shapeless value is refused
when the client is built.

**Compression.** Requests ask for gzip and deflate, as the page's sample does;
a compressed answer is unpacked before anything reads or hashes it, so a hash is
always of the document as filed. A compressed stream that ends early fails to
unpack, and a body shorter than its `Content-Length` is short; both are retried
like a refusal and never stored.

**Retries.** EDGAR answers a client over its rate with 403 as well as 429, so
403, 429 and the 5xx answers, a dropped connection and a short body are retried
after 1, 2 and 4 seconds before they are believed; every other status is raised
at once.

**The cache of filed documents.** An accession never changes once disseminated
(an amendment is a new accession), so a filed document is fetched once and kept
at `<root>/edgar/<cik>/<accession>/<name>` beside `<name>.sha256`. Its address
is the cache address: the URL is built from the CIK, the accession and the name,
never handed in. The root is `AAER_CACHE`, default `~/.cache/aaer-evals`, and a
root inside the repository is refused. One document is fetched and stored under
a lock, by one caller at a time; the bytes and the hash are each written whole
and renamed into place, and the file is hashed again before its path is handed
back. A cached file is read only when its bytes still hash to what was stored
with them; one that does not, or a file or a hash standing without the other, is
refused with `CacheMismatch`, never fetched over and never repaired. When the
caller knows the sha256 the record expects (a fixture manifest's row), a fetched
document that differs is refused and nothing is stored. A body whose length
nothing vouches for (no `Content-Length`, no chunked framing, no compression) is
not stored unless the caller knows its hash. The cache is speed; what a run's
agents saw is still committed in the run directory.

The submissions index and company facts change as a company files, so they are
not cached here; their readers (the next items of the build order) filter them
to a run's cutoff.
"""

from __future__ import annotations

import contextlib
import fcntl
import gzip
import hashlib
import http.client
import json
import os
import re
import tempfile
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import zlib
from pathlib import Path

USER_AGENT_VARIABLE = "EDGAR_USER_AGENT"
CACHE_VARIABLE = "AAER_CACHE"
DEFAULT_CACHE = Path.home() / ".cache" / "aaer-evals"
REPOSITORY = Path(__file__).resolve().parent.parent
ARCHIVES = "https://www.sec.gov/Archives/edgar/data/"
# one request at a time, each starting at least this long after the last began:
# eleven in a row then arrive across at least 9 x 0.12 = 1.08 seconds
MIN_INTERVAL = 0.12
GATE_FILE = Path(tempfile.gettempdir()) / "aaer-evals-edgar.gate"
# a recorded start further ahead of the clock than this is a clock that moved back
CLOCK_STEP = 1.0
RETRIED = (403, 429, 500, 502, 503, 504)
REDIRECTS = (301, 302, 303, 307, 308)
BACKOFF_SECONDS = (1, 2, 4)
TIMEOUT_SECONDS = 60
ACCEPT_ENCODING = "gzip, deflate"
# the page's shape: a name, a space, then an address with a dotted domain
DECLARED_CONTACT = re.compile(r"\S.*\s[^\s@]+@[^\s@]+\.[^\s@]+")
ACCESSION = re.compile(r"\d{10}-\d{2}-\d{6}", re.ASCII)
CIK = re.compile(r"\d{1,10}", re.ASCII)
# a document's name inside its accession folder: no path, no parent, no dot first
NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*", re.ASCII)


class EdgarError(Exception):
    """The client refused, or EDGAR did not answer with a document."""


class MissingContact(EdgarError):
    """`EDGAR_USER_AGENT` is unset, blank, or not a name and an address."""


class CacheMismatch(EdgarError):
    """Cached or fetched bytes are not the bytes on record."""


class _Short(Exception):
    """A body that ended before it said it would; retried, never stored."""


class Gate:
    """One request at a time, each starting `interval` after the last began.

    `path` is the file that carries the last start between processes; None
    keeps it in this object alone (the tests' turned clock).
    """

    def __init__(self, interval: float = MIN_INTERVAL, *, path: Path | None = GATE_FILE,
                 clock=time.time, sleep=time.sleep) -> None:
        self.interval = interval
        self.path = path
        self._clock = clock
        self._sleep = sleep
        self._last = None
        self._lock = threading.Lock()

    @contextlib.contextmanager
    def slot(self):
        """Held for the whole request: from before it is sent until its answer is read."""
        with self._lock, self._shared() as handle:
            last = self._read(handle)
            now = self._clock()
            if last is not None and last - now <= CLOCK_STEP:
                gap = last + self.interval - now
                if gap > 0:
                    self._sleep(gap)
                    now = self._clock()
            self._write(handle, now)
            yield

    @contextlib.contextmanager
    def _shared(self):
        if self.path is None:
            yield None
            return
        with open(self.path, "a+", encoding="ascii") as handle:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
            try:
                yield handle
            finally:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)

    def _read(self, handle):
        if handle is None:
            return self._last
        handle.seek(0)
        text = handle.read().strip()
        try:
            return float(text) if text else None
        except ValueError:
            return None

    def _write(self, handle, now: float) -> None:
        if handle is None:
            self._last = now
            return
        handle.seek(0)
        handle.truncate()
        handle.write(repr(now))
        handle.flush()


# the one gate of this machine, shared by every client of the process
machine_gate = Gate()


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
    """`AAER_CACHE`, or `~/.cache/aaer-evals`; never a folder inside the repository."""
    value = (os.environ if environ is None else environ).get(CACHE_VARIABLE, "")
    root = Path(value).expanduser() if value.strip() else DEFAULT_CACHE
    resolved = root.resolve()
    if resolved == REPOSITORY or REPOSITORY in resolved.parents:
        raise EdgarError(f"{CACHE_VARIABLE}={value!r} is inside the repository: the "
                         "documents are fetched on demand, not committed")
    return root


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def archive_url(cik, accession: str, name: str, base: str = ARCHIVES) -> str:
    return f"{base}{int(cik)}/{accession.replace('-', '')}/{name}"


def unpacked(body: bytes, encoding: str) -> bytes:
    """The body as served before the transfer compressed it."""
    try:
        if encoding == "gzip":
            return gzip.decompress(body)
        if encoding == "deflate":
            # HTTP's deflate is zlib-wrapped; some servers send it raw
            try:
                return zlib.decompress(body)
            except zlib.error:
                return zlib.decompress(body, -zlib.MAX_WBITS)
    except (EOFError, OSError, zlib.error) as error:
        raise _Short(f"a {encoding} stream that does not unpack: {error}") from None
    if encoding in ("", "identity"):
        return body
    raise EdgarError(f"an answer compressed as {encoding!r}, which was not asked for")


class _Refuse(urllib.request.HTTPRedirectHandler):
    """A redirect comes back as the HTTPError it is, not as a second request."""

    def redirect_request(self, *args, **kwargs):
        return None


def refusing_opener(proxies: dict | None = None):
    """urllib's opener without redirects; `proxies={}` goes direct (the tests' local server)."""
    handlers = [_Refuse()]
    if proxies is not None:
        handlers.append(urllib.request.ProxyHandler(proxies))
    return urllib.request.build_opener(*handlers).open


class EdgarClient:
    """Every EDGAR request of the pipeline goes through one of these."""

    def __init__(self, *, environ=None, gate: Gate | None = None, sleep=time.sleep,
                 opener=None, archives: str = ARCHIVES) -> None:
        self._user_agent = contact(environ)
        self.root = cache_root(environ)
        self.gate = gate or machine_gate
        self.archives = archives
        self._sleep = sleep
        self._open = opener or refusing_opener()

    @property
    def user_agent(self) -> str:
        return self._user_agent

    def _once(self, url: str) -> tuple[bytes, bool]:
        """One request through the gate: the body unpacked, and whether its length was vouched for."""
        request = urllib.request.Request(url, headers={
            "User-Agent": self._user_agent, "Accept-Encoding": ACCEPT_ENCODING})
        with self.gate.slot():
            with self._open(request, timeout=TIMEOUT_SECONDS) as response:
                headers = response.headers
                try:
                    body = response.read()
                except http.client.IncompleteRead as error:
                    raise _Short(f"{len(error.partial)} bytes of a body cut short") from None
        encoding = (headers.get("Content-Encoding") or "").strip().lower()
        declared = (headers.get("Content-Length") or "").strip()
        if declared.isdigit() and len(body) != int(declared):
            raise _Short(f"{len(body)} bytes where {declared} were declared")
        framed = declared.isdigit() or encoding in ("gzip", "deflate") \
            or "chunked" in (headers.get("Transfer-Encoding") or "").lower()
        return unpacked(body, encoding), framed

    def _get(self, url: str) -> tuple[bytes, bool]:
        for attempt in range(len(BACKOFF_SECONDS) + 1):
            last = attempt == len(BACKOFF_SECONDS)
            try:
                return self._once(url)
            except urllib.error.HTTPError as error:
                if error.code in REDIRECTS:
                    where = urllib.parse.urljoin(url, error.headers.get("Location") or "")
                    raise EdgarError(f"{url}: redirected to {where}, which is not followed") \
                        from None
                if error.code in RETRIED and not last:
                    self._sleep(BACKOFF_SECONDS[attempt])
                    continue
                raise EdgarError(f"{url}: HTTP {error.code}") from None
            except (urllib.error.URLError, http.client.HTTPException, ConnectionError,
                    TimeoutError, _Short) as error:
                if not last:
                    self._sleep(BACKOFF_SECONDS[attempt])
                    continue
                raise EdgarError(f"{url}: {getattr(error, 'reason', error)}") from None
        raise EdgarError(f"{url}: no answer")    # not reached

    def get(self, url: str) -> bytes:
        """The body EDGAR serves at `url`, unpacked, after at most three retries."""
        return self._get(url)[0]

    def get_json(self, url: str):
        try:
            return json.loads(self.get(url))
        except ValueError:
            raise EdgarError(f"{url}: the answer is not JSON") from None

    def document(self, *, cik: str, accession: str, name: str,
                 expected_sha256: str | None = None) -> Path:
        """A filed document as a local file whose bytes are the ones on record.

        Fetched from its own Archives address, once; read from the cache after
        that while its bytes still hash to what was stored (and to
        `expected_sha256`, when given). Anything else is refused, and nothing
        is stored.
        """
        if not CIK.fullmatch(str(cik)) or not ACCESSION.fullmatch(accession) \
                or not NAME.fullmatch(name) or name.lower().endswith(".sha256"):
            raise EdgarError(f"not a document address: {cik!r} {accession!r} {name!r}")
        folder = self.root / "edgar" / str(int(cik)) / accession
        path, stamp = folder / name, folder / f"{name}.sha256"
        folder.mkdir(parents=True, exist_ok=True)
        with open(folder / f".{name}.lock", "a", encoding="ascii") as lock:
            fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
            try:
                if path.exists() or stamp.exists():
                    return self._cached(path, stamp, expected_sha256)
                url = archive_url(cik, accession, name, self.archives)
                body, framed = self._get(url)
                actual = sha256(body)
                if expected_sha256 and actual != expected_sha256:
                    raise CacheMismatch(f"{url}: EDGAR served {actual}, the record expects "
                                        f"{expected_sha256}; nothing was stored")
                if not framed and not expected_sha256:
                    raise EdgarError(f"{url}: nothing vouches for the length of the "
                                     f"{len(body)} bytes served, and no hash was given; "
                                     "not stored")
                _write_whole(path, body)
                _write_whole(stamp, (actual + "\n").encode("ascii"))
                return self._cached(path, stamp, expected_sha256)
            finally:
                fcntl.flock(lock.fileno(), fcntl.LOCK_UN)

    @staticmethod
    def _cached(path: Path, stamp: Path, expected_sha256: str | None) -> Path:
        recorded = stamp.read_text(encoding="ascii").strip() if stamp.exists() else ""
        actual = sha256(path.read_bytes()) if path.exists() else ""
        if not recorded or actual != recorded:
            raise CacheMismatch(f"{path}: the cached bytes hash to {actual or 'nothing'}, "
                                f"not to the {recorded or 'missing'} hash stored with them")
        if expected_sha256 and actual != expected_sha256:
            raise CacheMismatch(f"{path}: cached as {actual}, the record expects "
                                f"{expected_sha256}")
        return path


def _write_whole(path: Path, data: bytes) -> None:
    """Written to a file of its own beside `path`, then renamed onto it."""
    handle, partial = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.")
    try:
        with os.fdopen(handle, "wb") as out:
            out.write(data)
            out.flush()
            os.fsync(out.fileno())
        os.replace(partial, path)
    except BaseException:
        with contextlib.suppress(FileNotFoundError):
            os.unlink(partial)
        raise
