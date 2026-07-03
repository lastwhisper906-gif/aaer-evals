"""Fetch primary sources for candidate re-verification (dev/scoring-assistant tooling).

Downloads, per candidate in data/candidates/candidates.json:
  1. The AAER / litigation-release document (aaer_url), plus any complaint or
     admin-order PDFs linked from litigation-release pages.
  2. data.sec.gov submissions JSON for the CIK (including paginated older chunks).

Everything lands in ~/aaer-data/{ticker}/ per data/README.md (kept out of git).
PDF text is extracted alongside as .txt (pypdf); HTML pages get a tag-stripped .txt.

SEC fair-access: User-Agent identifies the requester; global rate limit < 5 req/s.

This is ground-truth collection by the scoring assistant, not pipeline case-data
loading, so it does not route through pipeline/cutoff_guard.py (which guards the
evaluatee's inputs). AAER documents are by nature post-cutoff ground truth.
"""

import json
import re
import sys
import time
from html.parser import HTMLParser
from pathlib import Path

import requests

REPO = Path(__file__).resolve().parents[1]
DATA_DIR = Path.home() / "aaer-data"
UA = {"User-Agent": "chaeper lastwhisper906@gmail.com"}
RATE_SECONDS = 0.25  # 4 req/s < 5 req/s cap

_last_request = [0.0]


def fetch(url: str, timeout: int = 60) -> requests.Response:
    wait = RATE_SECONDS - (time.monotonic() - _last_request[0])
    if wait > 0:
        time.sleep(wait)
    _last_request[0] = time.monotonic()
    resp = requests.get(url, headers=UA, timeout=timeout)
    resp.raise_for_status()
    return resp


class _TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.chunks = []
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self._skip += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self._skip:
            self._skip -= 1

    def handle_data(self, data):
        if not self._skip:
            self.chunks.append(data)


def html_to_text(html: str) -> str:
    p = _TextExtractor()
    p.feed(html)
    text = "".join(p.chunks)
    return re.sub(r"\n{3,}", "\n\n", re.sub(r"[ \t]+", " ", text))


def pdf_to_text(path: Path) -> str:
    from pypdf import PdfReader

    reader = PdfReader(str(path))
    return "\n\n".join(page.extract_text() or "" for page in reader.pages)


def slug(url: str) -> str:
    name = url.rstrip("/").split("/")[-1].split("?")[0]
    return re.sub(r"[^A-Za-z0-9._-]", "_", name) or "index"


def save_document(url: str, dest_dir: Path) -> Path | None:
    """Fetch url into dest_dir; write extracted text alongside. Returns saved path."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    base = slug(url)
    try:
        resp = fetch(url)
    except Exception as e:  # noqa: BLE001 - report and continue, never silently skip
        print(f"  FAIL {url} -> {e}")
        return None
    content = resp.content
    is_pdf = content[:5] == b"%PDF-" or url.lower().endswith(".pdf")
    if is_pdf and not base.lower().endswith(".pdf"):
        base += ".pdf"
    if not is_pdf and not base.lower().endswith((".htm", ".html", ".json")):
        base += ".html"
    out = dest_dir / base
    out.write_bytes(content)
    txt = out.with_suffix(out.suffix + ".txt")
    try:
        if is_pdf:
            txt.write_text(pdf_to_text(out), encoding="utf-8")
        elif not base.endswith(".json"):
            txt.write_text(html_to_text(content.decode("utf-8", "replace")), encoding="utf-8")
    except Exception as e:  # noqa: BLE001
        print(f"  text-extract FAIL {out.name}: {e}")
    print(f"  saved {out.name} ({len(content):,} bytes)")
    return out


LINK_RE = re.compile(
    r'href="([^"]*(?:/litigation/(?:complaints|admin|litreleases)/[^"]+|'
    r'/files/litigation/[^"]+\.pdf))"',
    re.IGNORECASE,
)


def linked_litigation_docs(html: str) -> list[str]:
    urls = []
    for href in LINK_RE.findall(html):
        if href.startswith("/"):
            href = "https://www.sec.gov" + href
        if href not in urls:
            urls.append(href)
    return urls


# Extra primary documents beyond aaer_url, per case (complaints, companion orders,
# litigation releases for the null-AAER cases). Compiled from candidates.json notes.
EXTRA_DOCS = {
    "T09": ["https://www.sec.gov/newsroom/press-releases/2014-47"],
    "T10": ["https://www.sec.gov/litigation/admin/2014/33-9508.pdf"],
    "T14": [
        "https://www.sec.gov/enforcement-litigation/litigation-releases/lr-24195",
        "https://www.sec.gov/enforcement-litigation/litigation-releases/lr-23993",
    ],
    "T16": [
        "https://www.sec.gov/enforcement-litigation/litigation-releases/lr-24682",
    ],
    "T22": ["https://www.sec.gov/enforcement-litigation/litigation-releases/lr-24255"],
    "T24": ["https://www.sec.gov/enforcement-litigation/litigation-releases/lr-24459"],
    "T26": ["https://www.sec.gov/enforcement-litigation/litigation-releases/lr-24678"],
    "T27": ["https://www.sec.gov/newsroom/press-releases/2021-23"],
    "T30": ["https://www.sec.gov/enforcement-litigation/litigation-releases/lr-24987"],
}

# Additional registrant CIKs whose filings belong to a case (multi-CIK issuers).
EXTRA_CIKS = {
    "T13": ["0001364479"],  # predecessor Hertz Global Holdings (now Herc), filed the misstated 10-Ks
}


def fetch_submissions(cik: str, dest_dir: Path) -> None:
    dest_dir.mkdir(parents=True, exist_ok=True)
    cik10 = cik.zfill(10)
    main = f"https://data.sec.gov/submissions/CIK{cik10}.json"
    try:
        resp = fetch(main)
    except Exception as e:  # noqa: BLE001
        print(f"  FAIL submissions {cik10}: {e}")
        return
    out = dest_dir / f"CIK{cik10}.json"
    out.write_bytes(resp.content)
    j = resp.json()
    extra = [f["name"] for f in j.get("filings", {}).get("files", [])]
    print(f"  saved {out.name} ({len(resp.content):,} bytes, +{len(extra)} older chunks)")
    for name in extra:
        try:
            r2 = fetch(f"https://data.sec.gov/submissions/{name}")
            (dest_dir / name).write_bytes(r2.content)
            print(f"  saved {name} ({len(r2.content):,} bytes)")
        except Exception as e:  # noqa: BLE001
            print(f"  FAIL {name}: {e}")


def main() -> int:
    candidates = json.loads(
        (REPO / "data/candidates/candidates.json").read_text(encoding="utf-8")
    )["candidates"]

    only = set(sys.argv[1:])  # optional case_id filter, e.g. T04 T27
    failures = []
    for c in candidates:
        cid, ticker = c["case_id"], c["ticker"].split("/")[0]
        if only and cid not in only:
            continue
        dest = DATA_DIR / ticker
        print(f"\n=== {cid} {ticker} ===")
        urls = []
        if c.get("aaer_url"):
            urls.append(c["aaer_url"])
        urls += EXTRA_DOCS.get(cid, [])
        fetched_html = []
        for u in urls:
            p = save_document(u, dest)
            if p is None:
                failures.append((cid, u))
            elif p.suffix in (".html", ".htm"):
                fetched_html.append(p)
        # follow complaint/admin/LR links found on fetched pages (one hop)
        seen = set(urls)
        for p in fetched_html:
            for u in linked_litigation_docs(p.read_text(encoding="utf-8", errors="replace")):
                if u in seen:
                    continue
                seen.add(u)
                if save_document(u, dest) is None:
                    failures.append((cid, u))
        for cik in [c["cik"], *EXTRA_CIKS.get(cid, [])]:
            fetch_submissions(cik, dest / "edgar")

    print("\n==== SUMMARY ====")
    if failures:
        print(f"{len(failures)} fetch failures:")
        for cid, u in failures:
            print(f"  {cid}: {u}")
    else:
        print("all fetches succeeded")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
