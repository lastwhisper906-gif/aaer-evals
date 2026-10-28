"""A local stand-in for EDGAR that serves the bytes a test planted.

It counts and records every request it is sent, with the moment it arrived on
the machine's monotonic clock, answers with the statuses a test scripts for a
path (a redirect carries a `Location`), and serves a planted body, compressed as
the test says, with its length declared, or declared longer than what is sent
(`short`), or not declared at all (`unframed`); for a path nothing was planted
at, the default body, or 404 when the default is None. Tests reach it through
`DIRECT`, the client's own opener (no redirects followed) without the session's
proxy, which is for the outside world.
"""

from __future__ import annotations

import http.server
import threading
import time

from src.edgar_client import refusing_opener

# the SEC's sample declared User-Agent, with its placeholder domain filled in
# (https://www.sec.gov/search-filings/edgar-search-assistance/accessing-edgar-data)
SAMPLE_CONTACT = "Sample Company Name AdminContact@samplecompanydomain.com"

DIRECT = refusing_opener(proxies={})


class Planted(http.server.BaseHTTPRequestHandler):
    """Serves the test's bytes; counts and records every request it is sent."""

    def do_GET(self):  # noqa: N802 (the standard library's name)
        arrived = time.monotonic()
        server = self.server
        with server.lock:
            server.seen.append((self.path, dict(self.headers)))
            server.times.append(arrived)
            hits = server.hits[self.path] = server.hits.get(self.path, 0) + 1
        script = server.script.get(self.path)
        status = script[hits - 1] if script and hits <= len(script) else 200
        planted = server.bodies.get(self.path)
        if planted is None and server.default is not None:
            planted = (server.default, "")
        if planted is None and status == 200:
            status = 404
        if status != 200:
            self.send_response(status)
            if status in (301, 302, 303, 307, 308):
                self.send_header("Location", server.location.get(self.path, "/elsewhere"))
            self.send_header("Content-Length", "0")
            self.end_headers()
            return
        body, encoding = planted
        self.send_response(200)
        if encoding:
            self.send_header("Content-Encoding", encoding)
        if self.path in server.short:
            self.send_header("Content-Length", str(server.short[self.path]))
        elif self.path not in server.unframed:
            self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
        self.close_connection = True

    def log_message(self, *args):
        pass


def serve(default: bytes | None):
    """A running planted server, for a fixture to yield; shut down after."""
    planted = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Planted)
    planted.lock = threading.Lock()
    planted.seen, planted.times, planted.hits = [], [], {}
    planted.script, planted.bodies, planted.location = {}, {}, {}
    planted.short, planted.unframed = {}, set()
    planted.default = default
    thread = threading.Thread(target=planted.serve_forever, kwargs={"poll_interval": 0.05},
                              daemon=True)
    thread.start()
    planted.url = f"http://127.0.0.1:{planted.server_address[1]}"
    try:
        yield planted
    finally:
        planted.shutdown()
        planted.server_close()
