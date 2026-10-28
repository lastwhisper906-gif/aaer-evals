"""The EDGAR client: the rate limit, the declared contact, compression, retries,
and the cache that refuses bytes it did not store.

Expected values come from two places and neither is the code. The SEC's page on
accessing EDGAR data, read 2026-10-28
(https://www.sec.gov/search-filings/edgar-search-assistance/accessing-edgar-data),
quoted:

    Current max request rate: 10 requests/second.
    User-Agent: Sample Company Name AdminContact@<sample company domain>.com
    Accept-Encoding: gzip, deflate

and planted values: a local server that serves bytes the test wrote, stamps the
moment each request arrives and counts them per second, and answers with the
statuses the test scripts; connections the test makes slow to open; a cached
file whose bytes the test alters.
"""

from __future__ import annotations

import fcntl
import gzip
import hashlib
import os
import random
import socket
import subprocess
import sys
import threading
import time
import zlib
from pathlib import Path

import pytest

from src import edgar_client
from src.edgar_client import CacheMismatch, EdgarClient, EdgarError, Gate, MissingContact
from tests.planted_edgar import DIRECT, SAMPLE_CONTACT, serve

REPOSITORY = Path(__file__).resolve().parent.parent
# the page: "Current max request rate: 10 requests/second."
MAX_PER_SECOND = 10
# the page's sample header
SAMPLE_ACCEPT_ENCODING = "gzip, deflate"

FILED = b"<html><body>Item 2.02 Results of Operations and Financial Condition</body></html>\n"
CIK = "0000320193"
ACCESSION = "0000320193-26-000018"
# where the Archives keep it: the CIK without its zeros, the accession without dashes
ARCHIVED = "/320193/000032019326000018/filing.htm"


@pytest.fixture
def server():
    yield from serve(default=FILED)


def client(tmp_path, server=None, *, gate=None, sleep=None, opener=DIRECT, **environ):
    environ = {"EDGAR_USER_AGENT": SAMPLE_CONTACT, "AAER_CACHE": str(tmp_path), **environ}
    return EdgarClient(environ=environ, gate=gate, opener=opener,
                       archives=(server.url + "/") if server else edgar_client.ARCHIVES,
                       sleep=sleep if sleep is not None else (lambda seconds: None))


def busiest_second(stamps):
    """The most requests any one-second window holds."""
    stamps = sorted(stamps)
    return max(sum(1 for later in stamps[i:] if later - start < 1.0)
               for i, start in enumerate(stamps))


def slow_to_open(opener, seconds):
    """The opener, with each connection taking a while to open, as a slow network's do."""
    def open_(request, timeout):
        time.sleep(seconds())
        return opener(request, timeout=timeout)
    return open_


# --- the declared contact ---------------------------------------------------


@pytest.mark.parametrize("environ", [
    {},
    {"EDGAR_USER_AGENT": ""},
    {"EDGAR_USER_AGENT": "   "},
    {"EDGAR_USER_AGENT": "Sample Company Name"},                 # no address
    {"EDGAR_USER_AGENT": "AdminContact@samplecompanydomain.com"},  # no name
    {"EDGAR_USER_AGENT": "Sample Company Name AdminContact@localhost"},  # no domain
])
def test_a_missing_or_shapeless_contact_is_refused_when_the_client_is_built(environ):
    with pytest.raises(MissingContact):
        EdgarClient(environ=environ, opener=DIRECT)


def test_there_is_no_default_contact():
    with pytest.raises(MissingContact):
        edgar_client.contact({})


def test_the_contact_cannot_be_swapped_after_the_client_is_built(tmp_path):
    fetcher = client(tmp_path)
    with pytest.raises(AttributeError):
        fetcher.user_agent = "Someone Else other@example.com"


def test_the_declared_contact_and_the_pages_encodings_are_what_is_sent(tmp_path, server):
    client(tmp_path).get(server.url + "/filing.htm")
    [(path, headers)] = server.seen
    assert path == "/filing.htm"
    assert headers["User-Agent"] == SAMPLE_CONTACT
    assert headers["Accept-Encoding"] == SAMPLE_ACCEPT_ENCODING


# --- the rate limit -----------------------------------------------------------


def test_the_gate_spaces_starts_so_no_second_holds_more_than_ten():
    """On a clock the test turns: a burst of thirty asks at one instant."""
    now = [100.0]
    starts = []
    gate = Gate(path=None, clock=lambda: now[0],
                sleep=lambda seconds: now.__setitem__(0, now[0] + seconds))
    for _ in range(30):
        with gate.slot():
            starts.append(now[0])
    assert busiest_second(starts) <= MAX_PER_SECOND
    # eleven in a row span nine gaps past the first's answer: more than a second
    assert all(starts[i + 10] - starts[i + 1] >= 1.0 for i in range(len(starts) - 10))


def test_the_gate_does_not_wait_when_the_caller_was_already_slow():
    now = [0.0]
    slept = []
    gate = Gate(path=None, clock=lambda: now[0], sleep=slept.append)
    with gate.slot():
        pass
    now[0] += 5.0
    with gate.slot():
        pass
    assert slept == []


def test_the_server_counts_no_more_than_ten_requests_in_any_second(tmp_path, server):
    """Twenty-five requests as fast as the client allows, counted where they arrive."""
    fetcher = client(tmp_path)
    for _ in range(25):
        fetcher.get(server.url + "/filing.htm")
    assert server.hits["/filing.htm"] == 25 == len(server.times)
    assert busiest_second(server.times) <= MAX_PER_SECOND


def test_threads_with_slow_connections_keep_one_pace(tmp_path, server):
    """Four threads share a client; each connection takes 0 to 0.3 seconds to open."""
    jitter = random.Random(20261028)
    lock = threading.Lock()

    def delay():
        with lock:
            return jitter.uniform(0.0, 0.3)
    fetcher = client(tmp_path, opener=slow_to_open(DIRECT, delay))

    def fetch_six():
        for _ in range(6):
            fetcher.get(server.url + "/filing.htm")

    threads = [threading.Thread(target=fetch_six) for _ in range(4)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    assert server.hits["/filing.htm"] == 24
    assert busiest_second(server.times) <= MAX_PER_SECOND


def test_two_clients_in_one_process_keep_one_pace(tmp_path, server):
    first, second = client(tmp_path), client(tmp_path)
    for _ in range(12):
        first.get(server.url + "/a.htm")
        second.get(server.url + "/b.htm")
    assert server.hits == {"/a.htm": 12, "/b.htm": 12}
    assert busiest_second(server.times) <= MAX_PER_SECOND


def test_three_processes_on_one_machine_keep_one_pace(tmp_path, server):
    """Three runs fetching at once, each its own Python, each eight requests."""
    script = (
        "import sys\n"
        "from src.edgar_client import EdgarClient, refusing_opener\n"
        "c = EdgarClient(environ={'EDGAR_USER_AGENT': sys.argv[1], 'AAER_CACHE': sys.argv[2]},\n"
        "                opener=refusing_opener(proxies={}))\n"
        "for _ in range(8):\n"
        "    c.get(sys.argv[3])\n")
    runs = [subprocess.Popen([sys.executable, "-c", script, SAMPLE_CONTACT, str(tmp_path),
                              server.url + f"/run{n}.htm"], cwd=REPOSITORY)
            for n in range(3)]
    assert [run.wait(timeout=120) for run in runs] == [0, 0, 0]
    assert sum(server.hits.values()) == 24
    assert busiest_second(server.times) <= MAX_PER_SECOND


def test_a_clock_behind_the_recorded_start_waits_the_whole_interval():
    """A start recorded ahead of the clock (a reboot since) is not a reason to skip."""
    now = [5.0]
    slept = []
    gate = Gate(path=None, clock=lambda: now[0], sleep=slept.append)
    gate._last = 100.0
    with gate.slot():
        pass
    assert slept == [edgar_client.MIN_INTERVAL]


def test_the_gate_is_one_path_whatever_tmpdir_a_process_has(tmp_path):
    script = "from src import edgar_client; print(edgar_client.GATE_FILE)"
    seen = {subprocess.run([sys.executable, "-c", script], cwd=REPOSITORY, check=True,
                           capture_output=True, text=True,
                           env={"PATH": "/usr/bin:/bin", **({"TMPDIR": str(tmp_path)} if t else {})}
                           ).stdout.strip() for t in (True, False)}
    assert seen == {"/tmp/aaer-evals-edgar.gate"}


def test_an_unreadable_gate_file_is_rewritten_not_fatal(tmp_path):
    path = tmp_path / "gate"
    path.write_bytes(b"\xff\xfe not a time")
    gate = Gate(path=path, sleep=lambda seconds: None)
    for _ in range(2):
        with gate.slot():
            pass
    assert float(path.read_text()) > 0


def test_the_gate_file_is_writable_by_every_user(tmp_path):
    path = tmp_path / "gate"
    path.write_text("")
    path.chmod(0o644)
    with Gate(path=path).slot():
        pass
    assert path.stat().st_mode & 0o777 == 0o666


def test_a_gate_held_too_long_by_another_process_is_reported(tmp_path):
    path = tmp_path / "gate"
    path.write_text("")
    holder = os.open(path, os.O_RDWR)
    fcntl.flock(holder, fcntl.LOCK_EX)
    try:
        with pytest.raises(EdgarError, match="held for over"):
            with Gate(path=path, patience=0.3).slot():
                pass
    finally:
        fcntl.flock(holder, fcntl.LOCK_UN)
        os.close(holder)


def test_a_body_slow_to_arrive_does_not_hold_the_gate(tmp_path, server):
    """Planted: one document sends half, pauses two seconds, then the rest. A
    second request made meanwhile is answered before the slow one ends."""
    server.bodies["/slow.htm"] = (FILED * 1000, "")
    server.trickle["/slow.htm"] = 2.0
    done = {}

    def slow():
        client(tmp_path).get(server.url + "/slow.htm")
        done["slow"] = time.monotonic()
    worker = threading.Thread(target=slow)
    worker.start()
    time.sleep(0.5)
    client(tmp_path).get(server.url + "/quick.htm")
    done["quick"] = time.monotonic()
    worker.join()
    assert done["quick"] < done["slow"]


def test_the_default_opener_refuses_redirects(tmp_path, server, monkeypatch):
    for name in ("http_proxy", "HTTP_PROXY", "https_proxy", "HTTPS_PROXY",
                 "all_proxy", "ALL_PROXY"):
        monkeypatch.delenv(name, raising=False)
    fetcher = EdgarClient(environ={"EDGAR_USER_AGENT": SAMPLE_CONTACT,
                                   "AAER_CACHE": str(tmp_path)}, sleep=lambda seconds: None)
    server.script["/moved.htm"] = [302]
    with pytest.raises(EdgarError, match="redirected"):
        fetcher.get(server.url + "/moved.htm")
    assert [path for path, _ in server.seen] == ["/moved.htm"]


def test_every_retry_takes_the_gate(tmp_path, server):
    class Counted(Gate):
        slots = 0

        def slot(self):
            Counted.slots += 1
            return super().slot()
    server.script["/busy.htm"] = [503, 503, 503]
    client(tmp_path, gate=Counted(path=None)).get(server.url + "/busy.htm")
    assert Counted.slots == server.hits["/busy.htm"] == 4


def test_a_redirect_is_refused_not_followed(tmp_path, server):
    server.script["/moved.htm"] = [301]
    server.location["/moved.htm"] = "/filing.htm"
    with pytest.raises(EdgarError, match="redirected to .*/filing.htm"):
        client(tmp_path).get(server.url + "/moved.htm")
    assert [path for path, _ in server.seen] == ["/moved.htm"]


# --- compression and short bodies ----------------------------------------------


@pytest.mark.parametrize("encoding, pack", [
    ("gzip", gzip.compress),
    ("GZIP", gzip.compress),
    ("deflate", zlib.compress),
    ("deflate", lambda data: zlib.compress(data)[2:-4]),     # raw deflate, no zlib wrapper
])
def test_a_compressed_answer_is_unpacked_before_it_is_read(tmp_path, server, encoding, pack):
    server.bodies["/packed.htm"] = (pack(FILED), encoding)
    assert client(tmp_path).get(server.url + "/packed.htm") == FILED


def test_a_compressed_document_is_stored_and_hashed_as_filed(tmp_path, server):
    server.bodies[ARCHIVED] = (gzip.compress(FILED), "gzip")
    path = client(tmp_path, server).document(cik=CIK, accession=ACCESSION, name="filing.htm")
    assert path.read_bytes() == FILED
    assert (path.parent / "filing.htm.sha256").read_text().strip() \
        == hashlib.sha256(FILED).hexdigest()


def test_an_encoding_that_was_not_asked_for_is_refused(tmp_path, server):
    server.bodies["/br.htm"] = (FILED, "br")
    with pytest.raises(EdgarError, match="br"):
        client(tmp_path).get(server.url + "/br.htm")


def test_a_body_shorter_than_its_declared_length_is_retried_then_refused(tmp_path, server):
    """Planted: a length of 5013 declared, 100 bytes sent, every time."""
    server.bodies[ARCHIVED] = (FILED[:100], "")
    server.short[ARCHIVED] = 5013
    slept = []
    with pytest.raises(EdgarError):
        client(tmp_path, server, sleep=slept.append).document(
            cik=CIK, accession=ACCESSION, name="filing.htm")
    assert server.hits[ARCHIVED] == 4 and slept == [1, 2, 4]
    assert not (tmp_path / "edgar" / "320193" / ACCESSION / "filing.htm").exists()


def test_a_compressed_stream_that_ends_early_is_retried_then_refused(tmp_path, server):
    packed = gzip.compress(FILED * 50)
    server.bodies[ARCHIVED] = (packed[:len(packed) // 2], "gzip")
    with pytest.raises(EdgarError):
        client(tmp_path, server).document(cik=CIK, accession=ACCESSION, name="filing.htm")
    assert server.hits[ARCHIVED] == 4
    assert not (tmp_path / "edgar" / "320193" / ACCESSION / "filing.htm").exists()


def test_a_body_nothing_vouches_for_is_stored_only_against_a_known_hash(tmp_path, server):
    """Planted: no length declared, no chunks, no compression; the connection's
    close is the only end, and a close can come early."""
    server.unframed.add(ARCHIVED)
    with pytest.raises(EdgarError, match="nothing vouches for the length"):
        client(tmp_path, server).document(cik=CIK, accession=ACCESSION, name="filing.htm")
    assert not (tmp_path / "edgar" / "320193" / ACCESSION / "filing.htm").exists()
    path = client(tmp_path, server).document(cik=CIK, accession=ACCESSION, name="filing.htm",
                                             expected_sha256=hashlib.sha256(FILED).hexdigest())
    assert path.read_bytes() == FILED


# --- retries --------------------------------------------------------------------


@pytest.mark.parametrize("status", [403, 429, 500, 502, 503, 504])
def test_a_rate_or_gateway_answer_is_retried_after_one_two_and_four_seconds(
        tmp_path, server, status):
    server.script["/busy.htm"] = [status, status, status]
    slept = []
    assert client(tmp_path, sleep=slept.append).get(server.url + "/busy.htm") == FILED
    assert server.hits["/busy.htm"] == 4
    assert slept == [1, 2, 4]


def test_a_fourth_refusal_is_believed(tmp_path, server):
    server.script["/down.htm"] = [503, 503, 503, 503]
    slept = []
    with pytest.raises(EdgarError, match="HTTP 503"):
        client(tmp_path, sleep=slept.append).get(server.url + "/down.htm")
    assert server.hits["/down.htm"] == 4
    assert slept == [1, 2, 4]


def test_a_missing_document_is_not_retried(tmp_path, server):
    server.script["/gone.htm"] = [404]
    slept = []
    with pytest.raises(EdgarError, match="HTTP 404"):
        client(tmp_path, sleep=slept.append).get(server.url + "/gone.htm")
    assert server.hits["/gone.htm"] == 1
    assert slept == []


def test_a_host_that_does_not_answer_is_retried_then_refused(tmp_path):
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        port = probe.getsockname()[1]
    slept = []
    with pytest.raises(EdgarError):
        client(tmp_path, sleep=slept.append).get(f"http://127.0.0.1:{port}/filing.htm")
    assert slept == [1, 2, 4]


# --- the cache of filed documents ----------------------------------------------


def fetch(fetcher, **expected):
    return fetcher.document(cik=CIK, accession=ACCESSION, name="filing.htm", **expected)


def test_a_document_is_fetched_once_from_its_own_archive_address(tmp_path, server):
    fetcher = client(tmp_path, server)
    first = fetch(fetcher)
    second = fetch(fetcher)
    assert first == second == tmp_path / "edgar" / "320193" / ACCESSION / "filing.htm"
    assert first.read_bytes() == FILED
    assert (first.parent / "filing.htm.sha256").read_text() \
        == hashlib.sha256(FILED).hexdigest() + "\n"
    assert [path for path, _ in server.seen] == [ARCHIVED]


def test_the_archive_address_is_edgars():
    assert edgar_client.archive_url(CIK, ACCESSION, "aapl-20260730.htm") == \
        "https://www.sec.gov/Archives/edgar/data/320193/000032019326000018/aapl-20260730.htm"


def test_two_callers_fetching_one_document_at_once_get_whole_bytes(tmp_path, server):
    big = FILED * 200000      # about sixteen megabytes
    server.bodies[ARCHIVED] = (big, "")
    results, errors = [], []

    def one():
        try:
            path = fetch(client(tmp_path, server))
            results.append(hashlib.sha256(path.read_bytes()).hexdigest())
        except Exception as error:      # noqa: BLE001 (the test reports what it caught)
            errors.append(repr(error))

    threads = [threading.Thread(target=one) for _ in range(3)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    assert errors == []
    assert results == [hashlib.sha256(big).hexdigest()] * 3
    assert server.hits[ARCHIVED] == 1


def test_the_cache_root_defaults_outside_the_repository(monkeypatch):
    monkeypatch.delenv("AAER_CACHE", raising=False)
    root = edgar_client.cache_root({})
    assert root == Path.home() / ".cache" / "aaer-evals"
    assert REPOSITORY not in root.resolve().parents


@pytest.mark.parametrize("inside", ["", "tests/fixtures", "runs/cache"])
def test_a_cache_root_inside_the_repository_is_refused(inside):
    with pytest.raises(EdgarError, match="inside the repository"):
        edgar_client.cache_root({"AAER_CACHE": str(REPOSITORY / inside)})


@pytest.mark.parametrize("alter", [
    lambda data: data.replace(b"2.02", b"2.03"),
    lambda data: data + b" ",
    lambda data: b"",
])
def test_a_cached_file_whose_bytes_were_altered_is_refused(tmp_path, server, alter):
    fetcher = client(tmp_path, server)
    path = fetch(fetcher)
    altered = alter(path.read_bytes())
    path.write_bytes(altered)
    with pytest.raises(CacheMismatch):
        fetch(fetcher)
    # refused, not repaired: the altered bytes stay and EDGAR is not asked again
    assert path.read_bytes() == altered
    assert server.hits[ARCHIVED] == 1


def test_a_cached_file_without_its_hash_is_refused(tmp_path, server):
    fetcher = client(tmp_path, server)
    path = fetch(fetcher)
    (path.parent / "filing.htm.sha256").unlink()
    with pytest.raises(CacheMismatch):
        fetch(fetcher)
    assert server.hits[ARCHIVED] == 1


def test_a_hash_without_its_file_is_a_stopped_store_finished_against_that_hash(
        tmp_path, server):
    """The hash is written first, the bytes second: a hash alone is a store that
    stopped between the two. The document is fetched again and kept only if it
    hashes to what was stored."""
    fetcher = client(tmp_path, server)
    path = fetch(fetcher)
    path.unlink()
    assert fetch(fetcher).read_bytes() == FILED
    assert server.hits[ARCHIVED] == 2


def test_a_hash_without_its_file_refuses_bytes_unlike_it(tmp_path, server):
    fetcher = client(tmp_path, server)
    path = fetch(fetcher)
    path.unlink()
    server.bodies[ARCHIVED] = (FILED.replace(b"2.02", b"2.03"), "")
    with pytest.raises(CacheMismatch):
        fetch(fetcher)
    assert not path.exists()
    assert (path.parent / "filing.htm.sha256").read_text().strip() == \
        hashlib.sha256(FILED).hexdigest()


def test_the_stored_file_is_hashed_again_before_it_is_handed_back(tmp_path, server, monkeypatch):
    """Planted: the write puts other bytes on disk than the ones fetched."""
    real = edgar_client._write_whole

    def wrong(path, data):
        real(path, data if path.name.endswith(".sha256") else data + b"x")
    monkeypatch.setattr(edgar_client, "_write_whole", wrong)
    with pytest.raises(CacheMismatch):
        fetch(client(tmp_path, server))


def test_a_fetched_document_unlike_the_record_is_refused_and_nothing_is_stored(tmp_path, server):
    other = hashlib.sha256(b"the bytes a manifest recorded").hexdigest()
    with pytest.raises(CacheMismatch):
        fetch(client(tmp_path, server), expected_sha256=other)
    assert not (tmp_path / "edgar" / "320193" / ACCESSION / "filing.htm").exists()
    assert not (tmp_path / "edgar" / "320193" / ACCESSION / "filing.htm.sha256").exists()


def test_a_fetched_document_like_the_record_is_kept(tmp_path, server):
    path = fetch(client(tmp_path, server), expected_sha256=hashlib.sha256(FILED).hexdigest())
    assert path.read_bytes() == FILED


def test_a_cached_document_unlike_the_record_is_refused(tmp_path, server):
    fetcher = client(tmp_path, server)
    fetch(fetcher)
    other = hashlib.sha256(b"the bytes a manifest recorded").hexdigest()
    with pytest.raises(CacheMismatch):
        fetch(fetcher, expected_sha256=other)
    assert server.hits[ARCHIVED] == 1


@pytest.mark.parametrize("cik, accession, name", [
    (CIK, ACCESSION, "../filing.htm"),
    (CIK, ACCESSION, "a/filing.htm"),
    (CIK, ACCESSION, ".filing.htm"),
    (CIK, ACCESSION, "filing.htm.sha256"),
    (CIK, ACCESSION, "filing.htm.SHA256"),
    (CIK, "0000320193-26-18", "filing.htm"),
    ("Apple", ACCESSION, "filing.htm"),
])
def test_an_address_that_is_not_a_filed_document_is_refused_before_any_request(
        tmp_path, server, cik, accession, name):
    with pytest.raises(EdgarError, match="not a document address"):
        client(tmp_path, server).document(cik=cik, accession=accession, name=name)
    assert server.seen == []
