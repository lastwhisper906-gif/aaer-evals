"""The EDGAR client: the rate limit, the declared contact, compression, retries,
and the cache that refuses bytes it did not store.

Expected values come from two places and neither is the code. The SEC's page on
accessing EDGAR data, read 2026-10-28
(https://www.sec.gov/search-filings/edgar-search-assistance/accessing-edgar-data),
quoted:

    Current max request rate: 10 requests/second.
    User-Agent: Sample Company Name AdminContact@<sample company domain>.com
    Accept-Encoding: gzip, deflate

and planted values: a local server that serves bytes the test wrote, counts every
request it is sent and answers with the statuses the test scripts; a cached file
whose bytes the test alters.
"""

from __future__ import annotations

import gzip
import hashlib
import socket
import threading
import time
import zlib

import pytest

from src import edgar_client
from src.edgar_client import CacheMismatch, EdgarClient, EdgarError, MissingContact, Throttle
from tests.planted_edgar import DIRECT, SAMPLE_CONTACT, serve

# the page: "Current max request rate: 10 requests/second."
MAX_PER_SECOND = 10
# the page's sample header
SAMPLE_ACCEPT_ENCODING = "gzip, deflate"

FILED = b"<html><body>Item 2.02 Results of Operations and Financial Condition</body></html>\n"
CIK = "0000320193"
ACCESSION = "0000320193-26-000018"


@pytest.fixture
def server():
    yield from serve(default=FILED)


def client(tmp_path, *, pace=None, sleep=None, opener=DIRECT, **environ):
    environ = {"EDGAR_USER_AGENT": SAMPLE_CONTACT, "AAER_CACHE": str(tmp_path), **environ}
    return EdgarClient(environ=environ, pace=pace, opener=opener,
                       sleep=sleep if sleep is not None else (lambda seconds: None))


def stamped(opener, stamps, lock=None):
    """The opener, with the moment each request leaves the client written down."""
    lock = lock or threading.Lock()

    def open_(request, timeout):
        with lock:
            stamps.append(time.monotonic())
        return opener(request, timeout=timeout)
    return open_


def busiest_second(stamps):
    """The most request starts any one-second window holds."""
    stamps = sorted(stamps)
    return max(sum(1 for later in stamps[i:] if later - start < 1.0)
               for i, start in enumerate(stamps))


# --- the declared contact ---------------------------------------------------


@pytest.mark.parametrize("environ", [
    {},
    {"EDGAR_USER_AGENT": ""},
    {"EDGAR_USER_AGENT": "   "},
    {"EDGAR_USER_AGENT": "Sample Company Name"},                 # no address
    {"EDGAR_USER_AGENT": "AdminContact@samplecompanydomain.com"},  # no name
    {"EDGAR_USER_AGENT": "Sample Company Name AdminContact@localhost"},  # no domain
])
def test_a_missing_or_shapeless_contact_is_refused_before_any_request(environ, server):
    with pytest.raises(MissingContact):
        EdgarClient(environ=environ, opener=DIRECT)
    assert server.seen == []


def test_there_is_no_default_contact():
    with pytest.raises(MissingContact):
        edgar_client.contact({})


def test_the_declared_contact_and_the_pages_encodings_are_what_is_sent(tmp_path, server):
    client(tmp_path).get(server.url + "/filing.htm")
    [(path, headers)] = server.seen
    assert path == "/filing.htm"
    assert headers["User-Agent"] == SAMPLE_CONTACT
    assert headers["Accept-Encoding"] == SAMPLE_ACCEPT_ENCODING


# --- the rate limit -----------------------------------------------------------


def test_the_throttle_spaces_starts_so_no_second_holds_more_than_ten():
    """On a clock the test turns: a burst of thirty asks at one instant."""
    now = [100.0]
    starts = []
    pace = Throttle(clock=lambda: now[0],
                    sleep=lambda seconds: now.__setitem__(0, now[0] + seconds))
    for _ in range(30):
        pace.wait()
        starts.append(now[0])
    assert busiest_second(starts) <= MAX_PER_SECOND
    assert all(b - a >= 0.1 for a, b in zip(starts, starts[1:]))


def test_the_throttle_does_not_wait_when_the_caller_was_already_slow():
    now = [0.0]
    slept = []
    pace = Throttle(clock=lambda: now[0], sleep=slept.append)
    pace.wait()
    now[0] += 5.0
    pace.wait()
    assert slept == []


def test_a_local_server_counts_no_more_than_ten_requests_in_any_second(tmp_path, server):
    """Twenty-five requests as fast as the client allows.

    The server counts what arrived; the window is read off the moment each
    request leaves the client, which is the rate the SEC's rule governs (an
    arrival stamp would add this machine's thread scheduling to it).
    """
    stamps = []
    fetcher = client(tmp_path, opener=stamped(DIRECT, stamps))
    for _ in range(25):
        fetcher.get(server.url + "/filing.htm")
    assert server.hits["/filing.htm"] == 25 == len(stamps)
    assert busiest_second(stamps) <= MAX_PER_SECOND


def test_two_clients_in_one_process_keep_one_pace(tmp_path, server):
    stamps = []
    lock = threading.Lock()
    first = client(tmp_path, opener=stamped(DIRECT, stamps, lock))
    second = client(tmp_path, opener=stamped(DIRECT, stamps, lock))
    for _ in range(12):
        first.get(server.url + "/a.htm")
        second.get(server.url + "/b.htm")
    assert server.hits == {"/a.htm": 12, "/b.htm": 12}
    assert busiest_second(stamps) <= MAX_PER_SECOND


def test_threads_sharing_a_client_keep_one_pace(tmp_path, server):
    stamps = []
    fetcher = client(tmp_path, opener=stamped(DIRECT, stamps))

    def fetch_six():
        for _ in range(6):
            fetcher.get(server.url + "/filing.htm")

    threads = [threading.Thread(target=fetch_six) for _ in range(4)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    assert server.hits["/filing.htm"] == 24 == len(stamps)
    assert busiest_second(stamps) <= MAX_PER_SECOND


# --- compression --------------------------------------------------------------


@pytest.mark.parametrize("encoding, pack", [
    ("gzip", gzip.compress),
    ("deflate", zlib.compress),
    ("deflate", lambda data: zlib.compress(data)[2:-4]),     # raw deflate, no zlib wrapper
])
def test_a_compressed_answer_is_unpacked_before_it_is_read(tmp_path, server, encoding, pack):
    server.bodies["/packed.htm"] = (pack(FILED), encoding)
    assert client(tmp_path).get(server.url + "/packed.htm") == FILED


def test_a_compressed_document_is_stored_and_hashed_as_filed(tmp_path, server):
    server.bodies["/packed.htm"] = (gzip.compress(FILED), "gzip")
    path = client(tmp_path).document(server.url + "/packed.htm", cik=CIK,
                                     accession=ACCESSION, name="packed.htm")
    assert path.read_bytes() == FILED
    assert (path.parent / "packed.htm.sha256").read_text().strip() \
        == hashlib.sha256(FILED).hexdigest()


def test_an_encoding_that_was_not_asked_for_is_refused(tmp_path, server):
    server.bodies["/br.htm"] = (FILED, "br")
    with pytest.raises(EdgarError, match="br"):
        client(tmp_path).get(server.url + "/br.htm")


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


def fetch(fetcher, server, name="filing.htm", **expected):
    return fetcher.document(server.url + "/" + name, cik=CIK, accession=ACCESSION,
                            name=name, **expected)


def test_a_document_is_fetched_once_and_kept_where_the_archive_keeps_it(tmp_path, server):
    fetcher = client(tmp_path)
    first = fetch(fetcher, server)
    second = fetch(fetcher, server)
    assert first == second == tmp_path / "edgar" / "320193" / ACCESSION / "filing.htm"
    assert first.read_bytes() == FILED
    assert (first.parent / "filing.htm.sha256").read_text() \
        == hashlib.sha256(FILED).hexdigest() + "\n"
    assert server.hits["/filing.htm"] == 1


def test_the_cache_root_defaults_outside_the_repository(monkeypatch):
    monkeypatch.delenv("AAER_CACHE", raising=False)
    assert edgar_client.cache_root({}) == edgar_client.Path.home() / ".cache" / "aaer-evals"


@pytest.mark.parametrize("alter", [
    lambda data: data.replace(b"2.02", b"2.03"),
    lambda data: data + b" ",
    lambda data: b"",
])
def test_a_cached_file_whose_bytes_were_altered_is_refused(tmp_path, server, alter):
    fetcher = client(tmp_path)
    path = fetch(fetcher, server)
    altered = alter(path.read_bytes())
    path.write_bytes(altered)
    with pytest.raises(CacheMismatch):
        fetch(fetcher, server)
    # refused, not repaired: the altered bytes stay and EDGAR is not asked again
    assert path.read_bytes() == altered
    assert server.hits["/filing.htm"] == 1


def test_a_cached_file_without_its_hash_is_refused(tmp_path, server):
    fetcher = client(tmp_path)
    path = fetch(fetcher, server)
    (path.parent / "filing.htm.sha256").unlink()
    with pytest.raises(CacheMismatch):
        fetch(fetcher, server)
    assert server.hits["/filing.htm"] == 1


def test_a_hash_without_its_file_is_refused(tmp_path, server):
    fetcher = client(tmp_path)
    path = fetch(fetcher, server)
    path.unlink()
    with pytest.raises(CacheMismatch):
        fetch(fetcher, server)
    assert not path.exists()
    assert server.hits["/filing.htm"] == 1


def test_a_fetched_document_unlike_the_record_is_refused_and_nothing_is_written(
        tmp_path, server):
    other = hashlib.sha256(b"the bytes a manifest recorded").hexdigest()
    with pytest.raises(CacheMismatch):
        fetch(client(tmp_path), server, expected_sha256=other)
    assert not (tmp_path / "edgar" / "320193" / ACCESSION / "filing.htm").exists()
    assert not (tmp_path / "edgar" / "320193" / ACCESSION / "filing.htm.sha256").exists()


def test_a_fetched_document_like_the_record_is_kept(tmp_path, server):
    path = fetch(client(tmp_path), server, expected_sha256=hashlib.sha256(FILED).hexdigest())
    assert path.read_bytes() == FILED


def test_a_cached_document_unlike_the_record_is_refused(tmp_path, server):
    fetcher = client(tmp_path)
    fetch(fetcher, server)
    other = hashlib.sha256(b"the bytes a manifest recorded").hexdigest()
    with pytest.raises(CacheMismatch):
        fetch(fetcher, server, expected_sha256=other)
    assert server.hits["/filing.htm"] == 1


@pytest.mark.parametrize("cik, accession, name", [
    (CIK, ACCESSION, "../filing.htm"),
    (CIK, ACCESSION, "a/filing.htm"),
    (CIK, ACCESSION, ".filing.htm"),
    (CIK, ACCESSION, "filing.htm.sha256"),
    (CIK, "0000320193-26-18", "filing.htm"),
    ("Apple", ACCESSION, "filing.htm"),
])
def test_an_address_that_is_not_a_filed_document_is_refused_before_any_request(
        tmp_path, server, cik, accession, name):
    with pytest.raises(EdgarError, match="not a document address"):
        client(tmp_path).document(server.url + "/filing.htm", cik=cik,
                                  accession=accession, name=name)
    assert server.seen == []
