"""Fetch data.sec.gov XBRL companyfacts for baseline screens (scoring-side collection).

Usage: python tools/fetch_xbrl_facts.py T07 T11 ...   (no args = all candidates)
Forward mode (R3-4, OWNER_LAUNCH_GATE §4 (2) — 소유자 입회 세션 전용, INV-23):
       python tools/fetch_xbrl_facts.py --universe forward/cycle_001/universe.json \
           --dest <data-dir>
       universe.selected 전건의 companyfacts를 <dest>/{ticker}/xbrl/에,
       submissions(main+청크)를 <dest>/{ticker}/edgar/에 저장한다 — 러너
       (pipeline/cutoff_guard.py)가 읽는 corpus 배치 그대로 (R7-2).
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


def portable_path(path: Path, *, repo: Path | None = None,
                  home: Path | None = None) -> str:
    """R4-7(d): fetch_log에 절대 경로를 굽지 않는다 — 저장소/홈 정박 표기."""
    resolved = path.resolve()
    for anchor, prefix in (((repo or REPO).resolve(), ""),
                           ((home or Path.home()).resolve(), "~/")):
        try:
            return prefix + resolved.relative_to(anchor).as_posix()
        except ValueError:
            continue
    return str(resolved)


def _log_row(log, *, kind: str, rid: str, cik10: str, url: str,
             content: bytes, out: Path) -> None:
    """R8-1: fetch_forward가 디스크에 쓰는 모든 파일의 출처 행 — kind 구분.

    submissions 인덱스는 cutoff_guard가 허용성(admissibility)을 판정하는
    바로 그 파일이므로 sha256 기록이 없으면 사후 변조가 검출 불가.
    forward_source_manifest.build_sources는 kind=companyfacts 행만 소비한다
    (record_id 키 최신-행 dedup이 submissions 행에 클로버되지 않도록)."""
    log.write(json.dumps({
        "record_id": rid, "kind": kind, "cik": cik10, "url": url,
        "retrieval_date": datetime.datetime.now(
            datetime.timezone.utc).isoformat(timespec="seconds"),
        "sha256": hashlib.sha256(content).hexdigest(),
        "path": portable_path(out),
    }, ensure_ascii=False) + "\n")


def fetch_forward_submissions(rid: str, cik10: str, dest_dir: Path,
                              log) -> list[tuple[str, str]]:
    """R7-2: forward 회사의 submissions JSON(main + 구세대 청크) 수집.

    cutoff_guard._submissions가 {ticker}/edgar/CIK*.json을 hard-require하고
    companyfacts의 모든 accession을 이 인덱스와 교차 대조한다 — companyfacts만
    수집하면 러너가 fail-closed. fetch_primary_sources.fetch_submissions와 동형이되
    실패를 반환값으로 집계한다 (침묵 skip 금지). R8-1: 쓰는 파일마다 로그 행."""
    main_url = f"https://data.sec.gov/submissions/CIK{cik10}.json"
    try:
        resp = fetch(main_url)
        # R8-6: 파싱을 쓰기 전에 — 200에 절단 본문이 오면 (a) 손상 바이트가
        # 디스크에 남고 (b) 다회사 수집 전체가 traceback으로 중단됐다.
        # 함수 계약(침묵 skip 금지, 실패 집계)대로 집계하고 쓰지 않는다.
        doc = json.loads(resp.content)
    except Exception as e:  # noqa: BLE001
        print(f"{rid} FAIL {main_url}: {e}")
        return [(rid, main_url)]
    dest_dir.mkdir(parents=True, exist_ok=True)
    out = dest_dir / f"CIK{cik10}.json"
    out.write_bytes(resp.content)
    _log_row(log, kind="submissions", rid=rid, cik10=cik10, url=main_url,
             content=resp.content, out=out)
    failures = []
    for item in doc.get("filings", {}).get("files", []):
        name = item["name"]
        url = f"https://data.sec.gov/submissions/{name}"
        try:
            r2 = fetch(url)
        except Exception as e:  # noqa: BLE001
            print(f"{rid} FAIL {url}: {e}")
            failures.append((rid, url))
            continue
        chunk_out = dest_dir / name
        chunk_out.write_bytes(r2.content)
        _log_row(log, kind="submissions", rid=rid, cik10=cik10, url=url,
                 content=r2.content, out=chunk_out)
    return failures


def fetch_forward(universe_path: Path, dest: Path) -> int:
    """R3-4: universe 기반 파라미터화 수집 — 회고 경로(candidates.json) 무접촉.

    R7-2: 배치는 러너가 읽는 형태 그대로 — {ticker}/xbrl/CIK*.json(companyfacts)
    + {ticker}/edgar/CIK*.json(submissions). record_id 키 배치는 cutoff_guard가
    읽지 못한다(창 안 코드 수정 유발)."""
    universe = json.loads(universe_path.read_text(encoding="utf-8"))
    # R8-3: 1차 티커 충돌 = 두 회사의 corpus가 한 {ticker}/ 디렉토리에 침묵
    # 병합 (cutoff_guard는 glob-merge) — 어떤 파일도 쓰기 전에 fail-closed.
    primaries = [str(r["ticker"]).split("/")[0] for r in universe["selected"]]
    dups = {t for t in primaries if primaries.count(t) > 1}
    if dups:
        raise SystemExit(f"FAIL — universe.selected 1차 티커 충돌 {sorted(dups)}: "
                         "corpus 디렉토리 병합 위험, 수집 거부 (R8-3)")
    log_path = dest / "fetch_log.jsonl"
    dest.mkdir(parents=True, exist_ok=True)
    failures = []
    with log_path.open("a", encoding="utf-8") as log:
        for r in universe["selected"]:
            rid, cik10 = r["record_id"], str(r["cik"]).zfill(10)
            ticker = str(r["ticker"]).split("/")[0]
            failures.extend(
                fetch_forward_submissions(rid, cik10, dest / ticker / "edgar",
                                          log))
            url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik10}.json"
            try:
                resp = fetch(url)
            except Exception as e:  # noqa: BLE001
                print(f"{rid} FAIL {url}: {e}")
                failures.append((rid, url))
                continue
            out = dest / ticker / "xbrl" / f"CIK{cik10}.json"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(resp.content)
            _log_row(log, kind="companyfacts", rid=rid, cik10=cik10, url=url,
                     content=resp.content, out=out)
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
