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


def _resolve_logged_path(value: str) -> Path:
    """portable_path의 역산 — 저장소 상대·`~/` 정박·구세대 절대 경로."""
    if value.startswith("~/"):
        return Path.home() / value[2:]
    p = Path(value)
    return p if p.is_absolute() else REPO / value


def _own_writes(dest: Path) -> set[str]:
    """R11-2: 이 사이클이 직접 쓴 파일 목록 (dest/fetch_log.jsonl 기준).

    DATA_DIR 상대 posix 표기로 정규화해 매니페스트 path와 같은 좌표계에 둔다.
    로그가 없거나 손상된 행은 조용히 무시한다 — 미상은 '내 것 아님'으로
    떨어져 가드가 강한 쪽(거부)으로 기운다."""
    own: set[str] = set()
    log_path = dest / "fetch_log.jsonl"
    if not log_path.is_file():
        return own
    for line in log_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            value = json.loads(line).get("path")
        except json.JSONDecodeError:
            continue
        if not value:
            continue
        try:
            own.add(_resolve_logged_path(str(value)).resolve()
                    .relative_to(DATA_DIR.resolve()).as_posix())
        except (ValueError, OSError):
            continue
    return own


def _sha256_bytes_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def assert_no_pinned_custody_conflict(universe: dict, dest: Path,
                                      allow_pinned: set[str]) -> list[str]:
    """R10-2/R11-2: 핀 고정 corpus 커스터디 가드 — 어떤 파일도 쓰기 전에 판정.

    SEC 아카이브는 누적형이라 게시된 회고 결과의 재현 증거인 핀 스냅샷
    바이트는 덮어쓰면 복구 불가다. 그러나 R10-2의 최초 구현은 경로 접두만
    보았기 때문에, 이 사이클이 직접 수집한 forward 파일이 매니페스트에
    등재된 순간(runbook 2b) 재수집·재시도·부분 실패 복구가 영구 차단됐다
    (R11-2). 그래서 판정 기준은 접두가 아니라 출처다:

      - 디스크에 없는 핀 경로       → 진행 (덮어쓸 바이트가 없다)
      - 이 사이클이 쓴 파일이고
        디스크 == 매니페스트 기록   → 진행 (내 것의 재수집)
      - 그 외 (온전한 회고 스냅샷,
        또는 기록과 어긋난 바이트)  → 거부 (fail-closed)

    소유자 명시 예외는 --allow-pinned (fetch_log.jsonl에 기록된다).
    반환값은 실제로 예외가 적용된 티커 목록 (로그 기록용)."""
    manifest_file = REPO / "data/manifests/aaer_data_manifest.json"
    if not manifest_file.is_file():
        return []
    try:
        dest_rel = dest.resolve().relative_to(DATA_DIR.resolve()).as_posix()
    except ValueError:
        return []  # 매니페스트 관할(~/aaer-data) 밖 dest — 충돌 불가
    prefix = "" if dest_rel == "." else dest_rel + "/"
    pinned = {f["path"]: f.get("sha256") for f in json.loads(
        manifest_file.read_text(encoding="utf-8"))["files"]}
    own = _own_writes(dest)
    blocked, overridden = {}, []
    for ticker in sorted({str(r["ticker"]).split("/")[0]
                          for r in universe["selected"]}):
        reasons = []
        for rel, recorded in pinned.items():
            if not rel.startswith(f"{prefix}{ticker}/"):
                continue
            disk = DATA_DIR / rel
            if not disk.is_file():
                continue
            if rel in own and recorded and _sha256_bytes_of(disk) == recorded:
                continue
            reasons.append(rel)
        if not reasons:
            continue
        if ticker in allow_pinned:
            overridden.append(ticker)
            print(f"WARN — {ticker}: 핀 경로 {len(reasons)}건을 소유자 명시 "
                  "--allow-pinned로 덮어쓴다 (fetch_log.jsonl에 기록)")
            continue
        blocked[ticker] = reasons
    if blocked:
        detail = "; ".join(f"{t}({len(v)}건: {v[0]}…)" for t, v in sorted(blocked.items()))
        raise SystemExit(
            f"FAIL — 매니페스트 핀 경로와 충돌 {sorted(blocked)}: {detail} — "
            "온전한 회고 스냅샷을 덮어쓸 수 있어 수집 거부 (R10-2/R11-2). "
            "정책 해소는 소유자 결정(D-P94); 의도적 덮어쓰기는 "
            "--allow-pinned TICKER[,...] 명시.")
    return overridden


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


def fetch_forward(universe_path: Path, dest: Path,
                  allow_pinned: set[str] | None = None) -> int:
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
    # R10-2/R11-2: 핀 고정 corpus 커스터디 가드 — 어떤 파일도 쓰기 전에.
    overridden = assert_no_pinned_custody_conflict(
        universe, dest, set(allow_pinned or ()))
    log_path = dest / "fetch_log.jsonl"
    dest.mkdir(parents=True, exist_ok=True)
    failures = []
    with log_path.open("a", encoding="utf-8") as log:
        if overridden:
            # R11-2: 소유자 예외는 수집 로그에 남는다 — source_manifest는
            # kind로 걸러 읽으므로 companyfacts 행 dedup에 섞이지 않는다.
            log.write(json.dumps({
                "kind": "pinned_override", "tickers": sorted(overridden),
                "retrieval_date": datetime.datetime.now(
                    datetime.timezone.utc).isoformat(timespec="seconds"),
            }, ensure_ascii=False) + "\n")
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
    ap.add_argument("--allow-pinned", default="",
                    help="R11-2: 매니페스트 핀 경로 덮어쓰기를 명시 허용할 "
                         "티커 (쉼표 구분) — 소유자 판단 전용, fetch_log에 기록")
    args = ap.parse_args()
    if args.universe:
        if not args.dest:
            ap.error("--universe에는 --dest가 필요하다")
        allow = {t.strip() for t in args.allow_pinned.split(",") if t.strip()}
        return fetch_forward(Path(args.universe), Path(args.dest), allow)

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
