"""Fetch data.sec.gov XBRL companyfacts for baseline screens (scoring-side collection).

Usage: python tools/fetch_xbrl_facts.py T07 T11 ...   (no args = all candidates)
Forward mode (R3-4, OWNER_LAUNCH_GATE §4 (2) — 소유자 입회 세션 전용, INV-23):
       python tools/fetch_xbrl_facts.py --universe forward/cycle_001/universe.json \
           --dest <data-dir>
       universe.selected 전건의 companyfacts를 <dest>/{record_id}/xbrl/에 저장하고
       <dest>/fetch_log.jsonl에 url·retrieval_date·sha256를 기록한다
       (tools/forward_source_manifest.py의 입력).

Saves to ~/aaer-data/{ticker}/xbrl/CIK{cik10}.json. Like fetch_primary_sources.py,
this is scoring-assistant ground-truth collection, not evaluatee data loading —
point-in-time filtering (filed <= cutoff) happens in scoring/baselines/screens.py,
because companyfacts is a cumulative archive whose entries each carry their own
'filed' date. Multi-CIK issuers reuse the predecessor map from fetch_primary_sources.
"""
import argparse
import datetime
import hashlib
import json
import sys
from pathlib import Path

from fetch_primary_sources import DATA_DIR, EXTRA_CIKS, fetch

REPO = Path(__file__).resolve().parents[1]


def fetch_forward(universe_path: Path, dest: Path) -> int:
    """R3-4: universe 기반 파라미터화 수집 — 회고 경로(candidates.json) 무접촉."""
    universe = json.loads(universe_path.read_text(encoding="utf-8"))
    log_path = dest / "fetch_log.jsonl"
    dest.mkdir(parents=True, exist_ok=True)
    failures = []
    with log_path.open("a", encoding="utf-8") as log:
        for r in universe["selected"]:
            rid, cik10 = r["record_id"], str(r["cik"]).zfill(10)
            url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik10}.json"
            try:
                resp = fetch(url)
            except Exception as e:  # noqa: BLE001
                print(f"{rid} FAIL {url}: {e}")
                failures.append((rid, url))
                continue
            out = dest / rid / "xbrl" / f"CIK{cik10}.json"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(resp.content)
            log.write(json.dumps({
                "record_id": rid, "cik": cik10, "url": url,
                "retrieval_date": datetime.datetime.now(
                    datetime.timezone.utc).isoformat(timespec="seconds"),
                "sha256": hashlib.sha256(resp.content).hexdigest(),
                "path": str(out),
            }, ensure_ascii=False) + "\n")
            print(f"{rid} saved {out} ({len(resp.content):,} bytes)")
    print(f"\n{len(failures)} failures" if failures else "\nall fetches succeeded")
    return 1 if failures else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("case_ids", nargs="*", help="회고 모드: 후보 case_id 필터")
    ap.add_argument("--universe", help="forward 모드: universe.json 경로")
    ap.add_argument("--dest", help="forward 모드: 저장 루트 (fetch_log.jsonl 포함)")
    args = ap.parse_args()
    if args.universe:
        if not args.dest:
            ap.error("--universe에는 --dest가 필요하다")
        return fetch_forward(Path(args.universe), Path(args.dest))

    candidates = json.loads(
        (REPO / "data/candidates/candidates.json").read_text(encoding="utf-8")
    )["candidates"]
    only = set(args.case_ids)
    failures = []
    for c in candidates:
        cid, ticker = c["case_id"], c["ticker"].split("/")[0]
        if only and cid not in only:
            continue
        dest = DATA_DIR / ticker / "xbrl"
        dest.mkdir(parents=True, exist_ok=True)
        for cik in [c["cik"], *EXTRA_CIKS.get(cid, [])]:
            cik10 = cik.zfill(10)
            url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik10}.json"
            try:
                resp = fetch(url)
            except Exception as e:  # noqa: BLE001
                print(f"{cid} FAIL {url}: {e}")
                failures.append((cid, url))
                continue
            out = dest / f"CIK{cik10}.json"
            out.write_bytes(resp.content)
            print(f"{cid} saved {out.relative_to(DATA_DIR)} ({len(resp.content):,} bytes)")
    print(f"\n{len(failures)} failures" if failures else "\nall fetches succeeded")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
