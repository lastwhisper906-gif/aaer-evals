"""SEC AAER 색인 전 페이지 수집 → ~/aaer-data/_aaer_index/aaer_index.json.

대조군 비집행 확인(D17 ③)의 기계 검증 축: 후보 사명이 이 색인에 없음 확인.
색인 커버리지(최고~최저 AAER 번호·날짜)를 함께 기록 — 커버리지 밖 시기는
2차 검색(웹)으로 보강해야 함을 명시.
"""
import datetime
import json
import re
import sys
from pathlib import Path

from fetch_primary_sources import DATA_DIR, fetch

BASE = "https://www.sec.gov/enforcement-litigation/accounting-auditing-enforcement-releases"
ROW_RE = re.compile(
    r"<tr[^>]*>\s*<td[^>]*>(.*?)</td>\s*<td[^>]*>(.*?)</td>", re.S)
TAG_RE = re.compile(r"<[^>]+>")
AAER_RE = re.compile(r"AAER-(\d+)")


def clean(s: str) -> str:
    return re.sub(r"\s+", " ", TAG_RE.sub(" ", s)).strip()


def main() -> int:
    entries = []
    page = 0
    while True:
        r = fetch(f"{BASE}?page={page}")
        rows = ROW_RE.findall(r.text)
        got = 0
        for date_html, resp_html in rows:
            date, resp = clean(date_html), clean(resp_html)
            m = AAER_RE.search(resp)
            if not m:
                continue
            entries.append({"date": date, "respondents": resp.split(" Release No.")[0].strip(),
                            "aaer_no": int(m.group(1))})
            got += 1
        print(f"page {page}: {got} entries")
        if got == 0:
            break
        page += 1
    out_dir = DATA_DIR / "_aaer_index"
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "fetched_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "source": BASE,
        "count": len(entries),
        "aaer_no_range": [min(e["aaer_no"] for e in entries), max(e["aaer_no"] for e in entries)],
        "date_range": [entries[-1]["date"], entries[0]["date"]],
        "entries": entries,
    }
    (out_dir / "aaer_index.json").write_text(json.dumps(payload, ensure_ascii=False, indent=1),
                                             encoding="utf-8")
    print(f"saved {len(entries)} entries, AAER {payload['aaer_no_range']}, dates {payload['date_range']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
