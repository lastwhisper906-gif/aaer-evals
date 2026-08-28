"""~/aaer-data 무결성 매니페스트 — 생성(--write)·검증(기본)·자체점검(--schema-only).

배경: 2026-07-05 ~/aaer-data 전체가 조용히 소실된 사고 (daily_log/2026-07-05.md).
git 밖 원문 사본은 소실이 조용히 일어나므로, 커밋된 SHA-256 기준선과 대조해
복원본의 동일성을 기계로 확인한다. 매니페스트는 월요일 도시에 표본 점검의
참조본이기도 하다.

모드:
  --write        ~/aaer-data 전수 스캔 → data/manifests/aaer_data_manifest.json 생성.
                 source_url은 tools/fetch_primary_sources.py의 URL 로직(aaer_url,
                 EXTRA_DOCS, 저장된 HTML의 1-hop 링크, submissions 파일명)을 재사용해
                 역산한다. 로컬 파생물(.txt 추출본)은 source_url 없이 derived_from 기록.
  (기본)         디스크 전수 재해시 → 매니페스트와 대조. 누락/추가/해시 불일치 하나라도
                 있으면 exit 1 (fail-closed). ~/aaer-data 부재도 실패다 — 그게 사고다.
  --schema-only  매니페스트 파일 자체의 정합성만 점검 (CI용 — 러너에는 원본이 없다).

fetched_at은 파일 mtime(실제 수집 시각)의 기록이며 대조 항목이 아니다 —
복원 시 mtime은 달라져도 내용 해시가 같으면 동일본이다.
"""
import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fetch_primary_sources import (  # noqa: E402
    DATA_DIR,
    EXTRA_CIKS,
    EXTRA_DOCS,
    linked_litigation_docs,
    slug,
)

REPO = Path(__file__).resolve().parents[1]
MANIFEST = REPO / "data" / "manifests" / "aaer_data_manifest.json"
REQUIRED_KEYS = {"path", "size", "sha256", "fetched_at", "source_url"}

# reference/ = D36 가공 사명 충돌 스크린 전용 목록 (data/README.md) —
# .txt 파생물 규칙보다 먼저 판정해야 한다 (cik-lookup-data.txt는 원본이지 추출본이 아님).
REFERENCE_URLS = {
    "cik-lookup-data.txt": "https://www.sec.gov/Archives/edgar/cik-lookup-data.txt",
    "company_tickers.json": "https://www.sec.gov/files/company_tickers.json",
}


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def candidate_urls() -> dict[str, list[str]]:
    """ticker → 그 케이스에서 시도된 문서 URL 전부 (fetch 스크립트와 동일 로직)."""
    candidates = json.loads(
        (REPO / "data/candidates/candidates.json").read_text(encoding="utf-8")
    )["candidates"]
    by_ticker: dict[str, list[str]] = {}
    for c in candidates:
        ticker = c["ticker"].split("/")[0]
        urls = by_ticker.setdefault(ticker, [])
        if c.get("aaer_url"):
            urls.append(c["aaer_url"])
        urls += EXTRA_DOCS.get(c["case_id"], [])
    return by_ticker


def url_basenames(url: str) -> set[str]:
    """save_document의 확장자 보정을 역산 — url이 만들 수 있는 파일명 후보들."""
    base = slug(url)
    names = {base}
    if not base.lower().endswith(".pdf"):
        names.add(base + ".pdf")
    if not base.lower().endswith((".htm", ".html", ".json")):
        names.add(base + ".html")
    return names


CUSTODY_CLAIMS_KEY = "custody_claims"


def _custody_claims(data_dir: Path | None = None) -> set[str]:
    """수집 로그가 주장하는 경로 집합 — 가드와 같은 파서를 쓴다 (R13-5)."""
    root = data_dir or DATA_DIR
    import fetch_xbrl_facts  # noqa: PLC0415 — 지연 import (순환 없음)
    return fetch_xbrl_facts.logged_claims(root / "fetch_log.jsonl", root)


def new_custody_claims(previous: dict | None,
                       data_dir: Path | None = None) -> list[str]:
    """R13-5: 이미 핀된 경로에 대한 **새** 출처 주장 — 재핀 거부 사유.

    fetch 가드(fetch_xbrl_facts.assert_no_pinned_custody_conflict)의 신뢰
    앵커는 "수집 로그가 자기 매니페스트 핀과 일치한다"이다. 그런데 그 핀을
    만드는 유일한 도구가 이 파일이고, --write는 보호 대상 트리를 무조건
    전수 재스캔해 로그의 새 해시를 그대로 재기록했다. 그래서 위조된 한 줄이
    가드가 스스로 인쇄한 복구 명령(2b) 한 번으로 세탁됐다 — 재핀 후 그 행은
    권위를 얻고, 가드는 온전한 동결 파일의 덮어쓰기를 허용한다 (R12-1-B
    작동 익스플로잇).

    구분 기준은 '주장의 신규성'이다. 정당한 흐름에서 새 주장이 향하는 경로는
    직전 매니페스트에 아직 핀되지 않은 경로(이번에 처음 수집)이거나, 직전
    재핀 때 이미 축복된 주장이다. 위조 행이 노리는 것은 정확히 그 반대 —
    이 사이클이 쓴 적 없는, 이미 핀된 회고 스냅샷이다.

    최초 생성(previous=None)에는 기준선이 없으므로 비교하지 않는다.
    """
    if previous is None:
        return []
    blessed = set(previous.get(CUSTODY_CLAIMS_KEY) or [])
    pinned = {f.get("path") for f in previous.get("files", [])}
    return sorted((_custody_claims(data_dir) - blessed) & pinned)


def build_manifest() -> dict:
    if not DATA_DIR.is_dir():
        sys.exit(f"FAIL: {DATA_DIR} 부재 — 생성할 대상이 없다")

    # 1) 티커별 직접 URL + 저장된 HTML에서 1-hop 링크 복원 → 파일명 후보 → URL 매핑
    by_ticker = candidate_urls()
    for ticker, urls in by_ticker.items():
        for html in sorted((DATA_DIR / ticker).glob("*.htm*")):
            for u in linked_litigation_docs(
                html.read_text(encoding="utf-8", errors="replace")
            ):
                if u not in urls:
                    urls.append(u)

    files = []
    unattributed = []
    for path in sorted(DATA_DIR.rglob("*")):
        if not path.is_file() or path.name == ".DS_Store":
            continue
        rel = path.relative_to(DATA_DIR)
        ticker = rel.parts[0]
        if ticker == "_rp08":  # 자체 매니페스트 관할 (verify()의 주석 참조)
            continue
        entry = {
            "path": str(rel),
            "size": path.stat().st_size,
            "sha256": sha256_of(path),
            "fetched_at": datetime.fromtimestamp(
                path.stat().st_mtime, tz=timezone.utc
            ).isoformat(timespec="seconds"),
            "source_url": None,
        }
        if len(rel.parts) == 1 and path.name == "fetch_log.jsonl":
            # R10-2: forward 수집 로그 (fetch_xbrl_facts --universe가 루트에
            # 기록) — checksums.log와 동일한 파생물 관용구. 귀속이 없으면
            # --write 재생성 매니페스트가 자신의 check_schema에서 실패한다.
            entry["derived_from"] = "~/aaer-data (forward 수집 로그 — tools/fetch_xbrl_facts.py --universe)"
        elif ticker == "reference":
            entry["source_url"] = REFERENCE_URLS.get(path.name)
            if entry["source_url"] is None:
                unattributed.append(str(rel))
        elif ticker == "short_interest":
            # B4 아카이브 (D55) — 파일명이 URL을 결정 (shrtYYYYMMDD.csv)
            if path.name.startswith("shrt") and path.suffix == ".csv":
                entry["source_url"] = ("https://cdn.finra.org/equity/otcmarket/"
                                       f"biweekly/{path.name}")
            elif path.name == "checksums.log":
                entry["derived_from"] = "short_interest/ (수집 로그)"
            else:
                unattributed.append(str(rel))
        elif ticker == "finra_schedules":
            # 공표일 일정표 Wayback 아카이브 (Q-M02 구현) — 정본 URL 표는
            # tools/dissemination_schedules.SNAPSHOTS (사전 등록 목록)
            from dissemination_schedules import SNAPSHOTS
            if path.name in SNAPSHOTS:
                entry["source_url"] = SNAPSHOTS[path.name]
            elif path.name == "checksums.log":
                entry["derived_from"] = "finra_schedules/ (수집 로그)"
            else:
                unattributed.append(str(rel))
        elif path.suffix == ".txt":  # pdf/html에서 로컬 추출한 파생물
            entry["derived_from"] = str(rel)[: -len(".txt")]
        elif ticker == "_aaer_index":
            entry["source_url"] = ("https://www.sec.gov/enforcement-litigation/"
                                   "accounting-auditing-enforcement-releases")
        elif ticker == "_controls" or (len(rel.parts) > 2 and rel.parts[1] in ("edgar", "xbrl")):
            # data.sec.gov 계열: 파일명이 URL을 결정한다 (fetch_xbrl_facts/control_screening 규약)
            name = path.name
            if name.startswith("companyfacts_"):
                entry["source_url"] = f"https://data.sec.gov/api/xbrl/companyfacts/{name[len('companyfacts_'):]}"
            elif len(rel.parts) > 2 and rel.parts[1] == "xbrl":
                entry["source_url"] = f"https://data.sec.gov/api/xbrl/companyfacts/{name}"
            else:
                entry["source_url"] = f"https://data.sec.gov/submissions/{name}"
        else:
            for u in by_ticker.get(ticker, []):
                if path.name in url_basenames(u):
                    entry["source_url"] = u
                    break
            if entry["source_url"] is None:
                unattributed.append(str(rel))
        files.append(entry)

    if unattributed:  # 출처 불명 파일은 조용히 넘기지 않는다
        print(f"WARN: source_url 역산 실패 {len(unattributed)}건:", file=sys.stderr)
        for p in unattributed:
            print(f"  {p}", file=sys.stderr)

    return {
        "manifest_version": 1,
        "root": "~/aaer-data",
        # R13-5: 이 재핀 시점에 축복된 출처 주장 집합. 다음 재핀은 이것과
        # 대조해 '이미 핀된 경로에 대한 새 주장'을 거부한다 — 매니페스트는
        # git 안에 있으므로 이 집합의 증가는 diff에도 드러난다.
        CUSTODY_CLAIMS_KEY: sorted(_custody_claims()),
        "generated_at": datetime.now(tz=timezone.utc).isoformat(timespec="seconds"),
        "generated_by": "tools/verify_manifest.py --write",
        "file_count": len(files),
        "total_bytes": sum(f["size"] for f in files),
        "files": files,
    }


def load_manifest() -> dict:
    if not MANIFEST.is_file():
        sys.exit(f"FAIL: {MANIFEST.relative_to(REPO)} 부재 — 먼저 --write로 생성")
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def check_schema(m: dict) -> list[str]:
    """매니페스트 자체 정합성 (원본 디스크 없이 가능한 점검)."""
    errors = []
    if m.get("manifest_version") != 1:
        errors.append(f"manifest_version != 1: {m.get('manifest_version')}")
    files = m.get("files", [])
    if m.get("file_count") != len(files):
        errors.append(f"file_count {m.get('file_count')} != files {len(files)}")
    if m.get("total_bytes") != sum(f.get("size", 0) for f in files):
        errors.append("total_bytes가 size 합과 불일치")
    seen = set()
    for f in files:
        missing = REQUIRED_KEYS - f.keys()
        if missing:
            errors.append(f"{f.get('path', '?')}: 필수 키 누락 {sorted(missing)}")
        if not isinstance(f.get("sha256"), str) or len(f.get("sha256", "")) != 64:
            errors.append(f"{f.get('path', '?')}: sha256 형식 오류")
        if f.get("path") in seen:
            errors.append(f"중복 path: {f['path']}")
        seen.add(f.get("path"))
        if f.get("source_url") is None and "derived_from" not in f:
            errors.append(f"{f.get('path', '?')}: source_url도 derived_from도 없음")
    return errors


def verify(m: dict) -> list[str]:
    """디스크 전수 재해시 대조. 누락/추가/불일치 전부 보고 (fail-closed)."""
    errors = check_schema(m)
    if not DATA_DIR.is_dir():
        return errors + [f"{DATA_DIR} 부재 — 원본 디렉터리 소실"]
    on_disk = {
        str(p.relative_to(DATA_DIR)): p
        for p in DATA_DIR.rglob("*")
        if p.is_file() and p.name != ".DS_Store"
        # _rp08(RP-08 대조군 풀 원시)은 자체 기준선이 별도 커밋됨 —
        # runs/rp08/control_pool_raw/MANIFEST.sha256 (validate_control_input 층2가
        # 전수 재해시 검증). 이중 관할을 피하기 위해 이 매니페스트의 스코프 밖.
        and p.relative_to(DATA_DIR).parts[0] != "_rp08"
    }
    recorded = {f["path"]: f for f in m["files"]}
    for path in sorted(recorded.keys() - on_disk.keys()):
        errors.append(f"MISSING: {path} (매니페스트에 있으나 디스크에 없음)")
    for path in sorted(on_disk.keys() - recorded.keys()):
        errors.append(f"EXTRA: {path} (디스크에 있으나 매니페스트에 없음)")
    for path in sorted(recorded.keys() & on_disk.keys()):
        f, p = recorded[path], on_disk[path]
        if p.stat().st_size != f["size"]:
            errors.append(f"SIZE MISMATCH: {path} {p.stat().st_size} != {f['size']}")
        elif sha256_of(p) != f["sha256"]:
            errors.append(f"HASH MISMATCH: {path}")
    return errors


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true", help="매니페스트 생성")
    mode.add_argument("--schema-only", action="store_true", help="자체 정합성만 (CI)")
    ap.add_argument("--allow-new-custody-claims", action="store_true",
                    help="R13-5: 이미 핀된 경로에 대한 새 출처 주장을 소유자가 "
                         "명시 승인 (자동화·runbook에서 쓰지 않는다)")
    args = ap.parse_args()

    if args.write:
        previous = (json.loads(MANIFEST.read_text(encoding="utf-8"))
                    if MANIFEST.is_file() else None)
        offending = new_custody_claims(previous)
        if offending and not args.allow_new_custody_claims:
            print(f"FAIL — 재핀 거부 (R13-5): 수집 로그가 이미 핀된 경로 "
                  f"{len(offending)}건을 새로 '내가 썼다'고 주장한다:",
                  file=sys.stderr)
            for path in offending[:10]:
                print(f"  {path}", file=sys.stderr)
            print("  재핀하면 그 주장이 핀의 권위를 얻어 fetch 가드가 온전한 "
                  "동결 바이트의 덮어쓰기를 허용한다 — 위조 행 한 줄이 복구 "
                  "명령 한 번으로 세탁되는 경로다 (R12-1-B 실측).\n"
                  "  이 사이클이 실제로 그 경로를 수집한 것이 맞다면 소유자가 "
                  "--allow-new-custody-claims 로 명시 승인한다. 그 판단 없이 "
                  "자동화·runbook·CI에서 이 플래그를 쓰지 않는다.", file=sys.stderr)
            return 1
        m = build_manifest()
        MANIFEST.parent.mkdir(parents=True, exist_ok=True)
        MANIFEST.write_text(
            json.dumps(m, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        # 저장소 밖 경로(테스트 픽스처)에서도 표시로 죽지 않는다
        shown = MANIFEST.relative_to(REPO) if MANIFEST.is_relative_to(REPO) else MANIFEST
        print(f"wrote {shown}: {m['file_count']} files, "
              f"{m['total_bytes']:,} bytes")
        return 0

    m = load_manifest()
    errors = check_schema(m) if args.schema_only else verify(m)
    label = "schema-only" if args.schema_only else "full verify"
    if errors:
        print(f"FAIL ({label}) — {len(errors)}건:", file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        return 1
    print(f"PASS ({label}): {m['file_count']} files, {m['total_bytes']:,} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
