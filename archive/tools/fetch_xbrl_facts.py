"""Fetch data.sec.gov XBRL companyfacts for baseline screens (scoring-side collection).

Usage: python tools/fetch_xbrl_facts.py T07 T11 ...   (no args = all candidates)
Forward mode (R3-4, OWNER_LAUNCH_GATE §4 (2) — 소유자 입회 세션 전용, INV-23):
       python tools/fetch_xbrl_facts.py --universe forward/cycle_001/universe.json \
           --dest <data-dir>
       universe.selected 전건의 companyfacts를 <dest>/{ticker}/xbrl/에,
       submissions(main+청크)를 <dest>/{ticker}/edgar/에 저장한다 — 러너
       (pipeline/cutoff_guard.py)가 읽는 corpus 배치 그대로 (R7-2).
       data/provenance/fetch_log.jsonl(정본·git 관리)에 url·retrieval_date·
       sha256를 기록한다 (tools/forward_source_manifest.py의 입력). 로그는
       보호 대상 트리(DATA_DIR) 밖에 있고 --dest에서 파생되지 않는다 (R15-1).

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
import subprocess
import sys
from pathlib import Path

from fetch_primary_sources import DATA_DIR, EXTRA_CIKS, fetch

REPO = Path(__file__).resolve().parents[1]

# R15-1: 수집 로그의 **정본 위치** — `--dest`를 비롯한 어떤 호출자 인자에서도
# 파생하지 않고, 보호 대상 corpus 트리(DATA_DIR) 밖의 git 관리 경로 하나로
# 고정한다. R11-2 → R12-1 → R13-5 → R14-5로 네 번 재발한 결함 클래스
# ("두 경로·두 파서·두 파일")를 기제가 아니라 **속성**으로 없앤다: 보호 트리
# 안으로의 어떤 쓰기도 가드가 신뢰하는 출처 주장을 만들거나 늘릴 수 없다.
# 앵커는 매니페스트 핀이 아니라 git diff이며, 도구가 스스로 인쇄하는 복구
# 명령으로 세탁될 수 없다.
FETCH_LOG_REL = "data/provenance/fetch_log.jsonl"

# 테스트 격리 seam (R15-1): None이면 정본(REPO). 픽스처가 임시 루트를 꽂으면
# writer·가드·source_manifest가 **함께** 옮겨간다 — 한쪽만 옮길 수 없는 것이
# 이 설계의 요점이므로 seam도 단일 지점이다. 프로덕션 경로는 이 값을 쓰지
# 않는다 (tools/conftest.py의 autouse 픽스처가 유일한 설정자).
FETCH_LOG_ROOT: Path | None = None


def fetch_log_path() -> Path:
    """정본 수집 로그 — writer·가드·source_manifest의 단일 출처."""
    return (FETCH_LOG_ROOT or REPO) / FETCH_LOG_REL


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


def _anchor_repo_root() -> Path | None:
    """커스터디 권위를 답하는 저장소의 루트 — 없거나 미상이면 None (fail-closed).

    R17-3: 이 값이 **공격자가 만들 수 있는 경로에서 유도되지 않는다**는 것이
    통제의 전부다. 출발점은 로그 파일의 위치가 아니라 모듈이 자기 `__file__`
    에서 계산한 저장소(REPO) — 테스트에서는 seam이 꽂은 FETCH_LOG_ROOT — 이고,
    거기서 위로 올라가며 찾은 toplevel이 답한다. 보호 대상(핀된 코퍼스 바이트)을
    핀하는 매니페스트가 사는 저장소가 곧 그 저장소다."""
    base = FETCH_LOG_ROOT or REPO
    try:
        proc = subprocess.run(
            ["git", "-C", str(base), "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, check=False)
    except (OSError, ValueError):
        return None
    if proc.returncode != 0 or not proc.stdout.strip():
        return None
    root = Path(proc.stdout.strip())
    return root if root.is_dir() else None


def committed_log_lines(log_path: Path) -> list[str]:
    """HEAD에 **커밋된** 정본 로그의 행. 작업 트리 내용이 아니다.

    R16-2: R15-1은 신뢰 근원을 corpus 안에서 git 관리 경로로 **옮겼지만**,
    옮긴 자리에 아무 인증도 놓지 않았다 — 작업 트리 파일에 위조 행 한 줄을
    덧붙이면 온전한 핀 스냅샷이 아무 플래그 없이 덮어써졌다 (R15-1 lens B
    재현 익스플로잇). 설계가 전제한 앵커("행의 신설은 git diff에 드러난다")를
    실제 게이트로 만든다: 가드가 **의지하는 행**은 HEAD에 있어야 한다.

    저장소가 아니거나 파일이 추적되지 않거나 git이 없으면 빈 리스트 —
    fail-closed. 미상은 '내 것 아님'으로 떨어져 가드가 거부 쪽으로 기운다.
    작업 트리 전체가 깨끗할 것을 요구하지 않는다: 새로 수집한(아직 커밋 전)
    행은 의지 대상이 아니므로 fetch → 2b → 재수집 루프는 그대로 돈다.

    R17-3: 어느 저장소가 답하는지를 **공격자가 고를 수 없다**. 종전 게이트는
    `git -C <로그가 사는 디렉토리>`였고, 위조 행을 덧붙일 수 있는 주체는 같은
    자리에 `git init`도 할 수 있다 — 중첩 저장소가 바깥 저장소를 가려
    `HEAD:./fetch_log.jsonl`이 위조본을 돌려줬고, 바깥 이력에는 아무 흔적도
    남지 않은 채 핀된 동결 바이트가 덮어써졌다. 이제 앵커 저장소는 데이터에
    적힌 어떤 경로도 아닌 **모듈 자신의 설치 위치**(REPO, 테스트 seam은
    FETCH_LOG_ROOT)에서 `rev-parse --show-toplevel`로 얻고, 조회는 저장소
    루트 상대 pathspec으로 한다."""
    root = _anchor_repo_root()
    if root is None:
        return []
    try:
        rel = log_path.resolve().relative_to(root.resolve())
    except (ValueError, OSError):
        # 로그가 앵커 저장소 밖을 가리킨다 (심볼릭 링크 등) — fail-closed
        return []
    try:
        proc = subprocess.run(
            ["git", "-C", str(root), "show", f"HEAD:{rel.as_posix()}"],
            capture_output=True, text=True, check=False)
    except (OSError, ValueError):
        return []
    return proc.stdout.splitlines() if proc.returncode == 0 else []


def claims_from_lines(lines, data_dir: Path) -> set[str]:
    """행 목록 → 로그가 '내가 썼다'고 주장하는 경로 집합. 파싱의 단일 지점.

    R13-5: 재핀 검사와 가드가 **같은 파싱**을 봐야 한다 — 규칙이 갈라지면 한쪽이
    축복한 주장을 다른 쪽이 다르게 읽는다. 그래서 파싱은 여기 한 곳뿐이고,
    '어느 행을 신뢰할 것인가'(권위)는 호출자가 정한다 (R16-2: HEAD 판).

    data_dir 상대 posix 표기로 정규화해 매니페스트 path와 같은 좌표계에 둔다.
    손상된 행은 조용히 무시한다 — 미상은 '내 것 아님'으로 떨어져 가드가
    강한 쪽(거부)으로 기운다."""
    own: set[str] = set()
    for line in lines:
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        # R12-1(d): 유효 JSON 비객체 행(`123`)에서 죽지 않는다 — 독스트링이
        # 약속한 침묵 스킵을 실제로 이행한다.
        value = row.get("path") if isinstance(row, dict) else None
        if not value:
            continue
        try:
            own.add(_resolve_logged_path(str(value)).resolve()
                    .relative_to(data_dir.resolve()).as_posix())
        except (ValueError, OSError):
            continue
    return own


def _own_writes() -> set[str]:
    """R11-2/R15-1: 이 사이클이 직접 쓴 파일 목록 — 정본 로그만 읽는다.

    R12-1의 앵커("로그가 자기 매니페스트 핀과 바이트 일치")는 로그가 DATA_DIR
    **안**에 산다는 전제에서만 성립했고, 바로 그 전제가 네 번 뚫린 자리였다 —
    마지막(R14-5/R15-1)에는 기본값 아닌 --dest 하나로 가드(`dest/…`)와
    재핀(`DATA_DIR/…`)이 서로 다른 파일을 읽었다. 로그를 트리 밖 git 관리
    정본 한 곳으로 옮기면 권위 판정 자체가 필요 없어진다: 보호 트리 안에는
    신뢰되는 주장을 담을 수 있는 파일이 아예 없다. 인자를 받지 않는 것이
    이 함수의 계약이다 — 호출자가 경로를 고를 수 있으면 클래스가 되살아난다.

    R16-2: 정본 로그의 **HEAD 판**만 읽는다. 작업 트리에 덧붙인 행은 커밋되기
    전까지 아무 권위도 갖지 않으므로, 위조는 git 이력에 남지 않고서는 성립할
    수 없다 — R15-1이 앵커라고 선언했지만 강제하지 않았던 바로 그 성질."""
    return claims_from_lines(committed_log_lines(fetch_log_path()), DATA_DIR)


def _sha256_bytes_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def pinned_conflicts(universe: dict, prefix: str, pinned: dict,
                     own: set[str], exists) -> dict[str, list[str]]:
    """티커 → 이 수집이 열 수 없는 핀 경로 목록. 가드 판정의 순수 함수부.

    R16-4: 가드 자신은 `exists`로 디스크를 묻지만, **커밋된 산출물만** 보고
    같은 판정을 재생하려면 매니페스트가 곧 '그 바이트는 핀되어 있다'는 진실
    이어야 한다 — 그래야 판정이 로컬 corpus 유무에 흔들리지 않는다. 소유자
    결정(Q-F21) 전에 판정 규칙을 바꾸지 않으려고 술어만 주입 가능하게 했다."""
    blocked: dict[str, list[str]] = {}
    for ticker in sorted({str(r["ticker"]).split("/")[0]
                          for r in universe["selected"]}):
        reasons = []
        for rel, recorded in pinned.items():
            if not rel.startswith(f"{prefix}{ticker}/"):
                continue
            if not exists(rel):
                continue
            disk = DATA_DIR / rel
            if (rel in own and recorded and disk.is_file()
                    and _sha256_bytes_of(disk) == recorded):
                continue
            reasons.append(rel)
        if reasons:
            blocked[ticker] = reasons
    return blocked


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

    R15-1: '이 사이클이 쓴'의 근거는 정본 수집 로그(FETCH_LOG_REL) 하나뿐
    이고, 그 파일은 보호 대상 트리 밖의 git 관리 경로다 — dest·--dest에서
    파생되지 않으므로 가드와 다른 소비자가 서로 다른 파일을 볼 수 없고,
    트리 안으로 쓰는 어떤 것도 주장을 만들 수 없다. R12-1의 매니페스트 핀
    앵커는 그 전제(로그가 트리 안에 산다)에서만 필요했으므로 함께 사라졌다.

    R16-2: 그러나 옮겨간 신뢰 근원 자체는 인증되지 않은 채였다 — 작업 트리의
    로그에 위조 행 한 줄이면 온전한 핀 스냅샷이 열렸다. 이제 근거는 로그의
    **HEAD 판**이다 (committed_log_lines). 작업 트리 전체의 청결을 요구하지
    않으므로 정당한 재수집 루프는 그대로다.

    소유자 명시 예외는 --allow-pinned (정본 로그에 기록된다).
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
    own = _own_writes()
    blocked, overridden = {}, []
    for ticker, reasons in pinned_conflicts(
            universe, prefix, pinned, own,
            lambda rel: (DATA_DIR / rel).is_file()).items():
        if ticker in allow_pinned:
            overridden.append(ticker)
            print(f"WARN — {ticker}: 핀 경로 {len(reasons)}건을 소유자 명시 "
                  f"--allow-pinned로 덮어쓴다 ({FETCH_LOG_REL}에 기록)")
            continue
        blocked[ticker] = reasons
    if blocked:
        detail = "; ".join(f"{t}({len(v)}건: {v[0]}…)" for t, v in sorted(blocked.items()))
        remedy = ("\n  이 사이클이 실제로 그 파일을 썼다면 정본 수집 로그"
                  f"({FETCH_LOG_REL})의 **HEAD 판**에 그 행이 있어야 한다 — "
                  "방금 수집했다면 runbook 2b에서 그 로그를 커밋하라 "
                  f"(git add {FETCH_LOG_REL} && git commit). 행이 작업 트리에만 "
                  "있으면 권위가 없다 (R16-2): 위조가 git 이력에 남지 않고 "
                  "성립할 수 없게 하는 것이 앵커의 전부다. 커밋해도 그 행이 "
                  "이 수집의 것이 아니라면 이 수집은 그 경로의 출처가 아니며, "
                  "그래도 덮어써야 한다면 --allow-pinned가 유일한 길이고 "
                  "소유자 판단이다.")
        raise SystemExit(
            f"FAIL — 매니페스트 핀 경로와 충돌 {sorted(blocked)}: {detail} — "
            "온전한 회고 스냅샷을 덮어쓸 수 있어 수집 거부 (R10-2/R11-2). "
            "정책 해소는 소유자 결정(D-P94); 의도적 덮어쓰기는 "
            "--allow-pinned TICKER[,...] 명시." + remedy)
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
    log_path = fetch_log_path()
    log_path.parent.mkdir(parents=True, exist_ok=True)
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
    print(f"NOTE — 출처 기록이 {FETCH_LOG_REL}에 추가됐다. 이 파일이 커스터디 "
          "주장의 정본이며 앵커는 git 이력이므로, 수집 직후 커밋하라 (R15-1). "
          "이 커밋은 권고가 아니라 절차의 일부다 (R16-2): 가드는 저장소 HEAD에 "
          "있는 행만 신뢰하므로, 커밋하지 않으면 다음 재수집이 방금 쓴 핀 "
          "경로에서 거부된다. (작업 트리 **전체**의 청결은 요구하지 않는다 — "
          "가드가 요구하는 것은 자신이 의지하는 행이 커밋돼 있을 것뿐이라, "
          "fetch → 2b → 재수집 루프는 그대로 돈다.)")
    return 1 if failures else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("case_ids", nargs="*", help="회고 모드: 후보 case_id 필터")
    ap.add_argument("--universe", help="forward 모드: universe.json 경로")
    ap.add_argument("--dest", help="forward 모드: corpus 저장 루트 (수집 로그는 "
                                   "여기가 아니라 정본 경로에 쓴다 — R15-1)")
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
