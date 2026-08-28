"""forward 사이클 봉인 (spec §9, D100) — 매니페스트·봉인 기록·OTS·push 명령.

usage: python tools/forward_seal.py --cycle forward/cycle_001

- 검증(forward_validate) 통과 후에만 봉인한다.
- MANIFEST.sha256 (결정론 순서) + SEAL_RECORD.md 생성.
- OpenTimestamps: `ots stamp MANIFEST.sha256` 시도 (무료·무계정). ots 부재
  시 정확한 설치·실행 명령을 SEAL_RECORD와 stdout에 기록 (봉인은 유효하되
  OTS 앵커 pending으로 표시).
- GitHub push는 소유자 자격증명 작업 — 정확한 명령을 방출한다 (§9-1).
- 재봉인 금지: MANIFEST.sha256 존재 시 거부 (교정은 새 사이클 — spec §3-5).
"""
import argparse
import datetime
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from forward_common import (ET, REPO, EXECUTION_WINDOW_END,
                            assert_subscription_only, is_sealed, manifest_text,
                            parse_date, sha256_text, fail,
                            unshippable_sealed_files)
from forward_validate import validate

# R10-6: ots 달력 서버 불통 시 무한 대기 금지 — 한도 초과면 pending 기록
OTS_TIMEOUT_S = 120


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cycle", required=True)
    ap.add_argument("--abort", action="store_true",
                    help="R3-9: 중단 봉인 — 현재 부분 상태를 그대로 동결하고 "
                         "SEAL_RECORD를 aborted로 기록 (조용한 연장 금지, INV-22)")
    ap.add_argument("--reason", help="--abort 사유 (필수)")
    ap.add_argument("--past-window", action="store_true",
                    help=f"창 종료({EXECUTION_WINDOW_END}) 후의 정규 봉인 명시 허용 "
                         "— 무플래그 봉인은 거부된다 (R3-9)")
    ap.add_argument("--runs", default=None,
                    help="R5-1: 러너 출력 디렉토리 (기본 규약 runs/forward/<cycle명>) "
                         "— 정규 봉인은 이 디렉토리 실측 재해시 없이는 불가")
    args = ap.parse_args()
    assert_subscription_only()
    cycle = REPO / args.cycle
    runs_dir = REPO / (args.runs or f"runs/forward/{cycle.name}")
    tag = f"forward-{cycle.name.replace('_', '-')}-seal"

    # R6-7(a): SEAL_RECORD는 게시·공유 표면 — 절대 로컬 경로(사용자명)를
    # 굽지 않는다. 저장소 상대 표기, 저장소 밖(픽스처)은 이름만.
    def _display(path_arg, resolved: Path, default: str) -> str:
        if path_arg is None:
            return default
        if not Path(path_arg).is_absolute():
            return path_arg
        try:
            return resolved.relative_to(REPO).as_posix()
        except ValueError:
            return resolved.name

    cycle_display = _display(args.cycle, cycle, cycle.name)
    runs_display = _display(args.runs, runs_dir, f"runs/forward/{cycle.name}")

    manifest = cycle / "MANIFEST.sha256"
    record = cycle / "SEAL_RECORD.md"
    if is_sealed(cycle):
        fail(f"{manifest} 이미 존재 — 재봉인 금지 (spec §3-5: "
             "교정은 새 사이클에서. aborted 처리는 SEAL_RECORD.md에 일자 기입)")
    if manifest.exists():
        # R10-6: MANIFEST만 있고 SEAL_RECORD가 없는 상태는 완결 봉인이 아니라
        # 중단 잔여물(ots 지연·SIGHUP·터미널 종료)이다 — 이어서 완결한다.
        # R11-8: 종전의 "잔여물이 현재 트리와 바이트 일치할 때만" 조건은
        # 삭제했다. 정규 경로는 어차피 validate()를 다시 돌리고 매니페스트를
        # 다시 쓰므로 새 봉인이 주지 않는 보호를 하나도 주지 못하면서,
        # 재개된 러너 출력으로 트리가 바뀐 정당한 경우(11/12 → 12/12)에
        # 유일한 출구를 막아 수동 rm 외에 길이 없는 상태를 만들었다.
        print("NOTE — 중단된 봉인 재개 (R10-6/R11-8): SEAL_RECORD 부재 — "
              "현재 트리로 검증·매니페스트 재작성 후 봉인을 완결한다")
    if args.abort:
        if not args.reason:
            ap.error("--abort에는 --reason이 필요하다 (중단 사유 기록 의무)")
    else:
        # R10-8: 창은 ET 정의 — UTC 날짜로 판정하면 마지막 창일 19:00 ET
        # 이후의 정규 봉인이 --past-window로 오낙인된다 (SEAL_RECORD 영구 기록).
        today = datetime.datetime.now(ET).date()
        if today > parse_date(EXECUTION_WINDOW_END) and not args.past_window:
            fail(f"실행 창 종료({EXECUTION_WINDOW_END}) 이후의 정규 봉인 — "
                 "조용한 연장 금지 (INV-22: abort 마감 + 새 사이클이 규칙). "
                 "그래도 봉인하려면 --past-window 명시 (SEAL_RECORD에 남는다).")
        # R5-1: 봉인 머신은 러너 출력을 가진 바로 그 머신 — 정규 봉인에서
        # run_output_sha256 실측 재해시 leg를 건너뛸 사유가 없다 (fail-closed).
        if not runs_dir.is_dir():
            fail(f"runs 디렉토리 부재({runs_dir}) — 정규 봉인은 러너 출력 실측 "
                 "재해시 없이는 불가 (R5-1; 부분 상태 동결은 --abort 경로)")
        errs = validate(cycle, runs_dir=runs_dir)
        if errs:
            fail("봉인 전 검증 위반 — forward_validate 참조:\n  " + "\n  ".join(errs))

    # R11-6: 매니페스트에 적히지만 git이 실어 나르지 못하는 파일이 있으면
    # 봉인 순간 되돌릴 수 없이 깨진다 (클론마다 manifest_text 한 줄 부족).
    # abort 봉인도 같은 방식으로 커밋되므로 두 경로 모두에 적용한다.
    unshippable = unshippable_sealed_files(cycle)
    if unshippable:
        fail("봉인 대상에 git이 커밋하지 못하는 파일 존재 — "
             f"{unshippable}: 해시는 매니페스트에 실리지만 `git add`가 건너뛰어 "
             "모든 클론에서 봉인 검증이 영구 실패한다 (재봉인 금지·매니페스트 "
             "불변이므로 사후 교정 불가). 해당 파일을 제거하거나(.DS_Store 류), "
             "실어야 할 증거라면 무시 규칙에서 예외 처리한 뒤 다시 봉인하라.")

    text = manifest_text(cycle)
    manifest.write_text(text, encoding="utf-8")
    mhash = sha256_text(text)
    now = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO,
                          capture_output=True, text=True).stdout.strip()

    ots_bin = shutil.which("ots")
    ots_status = "pending — ots 클라이언트 부재"
    if ots_bin:
        # R10-6: stamp 미완이 봉인 자체를 wedging하지 않는다 — pending으로
        # 기록하고 완결한다 (.ots는 사후 stamp 가능, 형식은 pending 지원).
        try:
            r = subprocess.run([ots_bin, "stamp", str(manifest)],
                               capture_output=True, text=True,
                               timeout=OTS_TIMEOUT_S)
            ots_status = ("stamped — MANIFEST.sha256.ots 생성" if r.returncode == 0
                          else f"실패({r.returncode}): {r.stderr.strip()[:120]}")
        except (subprocess.TimeoutExpired, KeyboardInterrupt):
            ots_status = (f"pending — stamp 미완 (시간초과/중단, {OTS_TIMEOUT_S}s "
                          "한도); 사후 실행: `ots stamp MANIFEST.sha256` 후 .ots 커밋")

    seal_kind = "ABORTED" if args.abort else "sealed"
    # R5-1: 재해시 leg의 실행 여부를 SEAL_RECORD에 명시 (abort는 부분 상태
    # 동결이 목적이므로 skip-with-notice 유지)
    rehash_line = (f"- run_output re-hash: SKIPPED — abort 봉인 (부분 상태; "
                   f"runs dir {'있음' if runs_dir.is_dir() else '부재'})\n"
                   if args.abort else
                   f"- run_output re-hash: verified against `{runs_display}` "
                   "(forward_validate --runs leg)\n")
    # R11-3: OTS는 유일하게 남는 비가역 앵커다 (GitHub Events는 ~90일 보존,
    # tagger/committer 날짜는 클라이언트 제공값) — pending을 OTS 줄에만
    # 적으면 status만 읽는 독자에게 앵커 부재가 보이지 않는다.
    ots_pending = not ots_status.startswith("stamped")
    pending_mark = (" — **OTS 앵커 pending** (봉인 유효하되 외부 시각 증거 "
                    "미완: `ots stamp MANIFEST.sha256` 후 .ots 커밋 필요)"
                    if ots_pending else "")
    status_lines = (f"- **status: ABORTED** — 부분 상태 동결 (spec §3-2)\n"
                    f"- abort_reason: {args.reason}\n" if args.abort else
                    (f"- status: sealed (past-window — --past-window 명시 실행)"
                     f"{pending_mark}\n" if args.past_window else
                     f"- status: sealed{pending_mark}\n"))
    status_lines += rehash_line
    # R7-16: runs 출력·호출 로그(logs/run_* — served_models/pin_ok 증거)를
    # 봉인 커밋에 함께 staging — 없으면 클론 검증자의 re-hash leg가
    # skip-with-notice로 격하된다. 부재 경로는 넣지 않는다 (git add 오류).
    stage_extra = ""
    if runs_dir.is_dir():
        stage_extra += f" {runs_display}"
    if sorted((REPO / "logs").glob("run_*")):
        stage_extra += " logs/run_*"
    # R10-3: 봉인 커밋은 runs/forward 출력을 staging하므로 블라인드 매니페스트
    # 재생성·staging 없이는 push된 봉인 커밋 자체가 정본 CI를 붉힌다.
    owner_cmds = (
        f"python tools/verify_blindness.py --write-manifest\n"
        f"git add runs/MANIFEST.sha256 {cycle_display}{stage_extra} && "
        f"git commit -m 'SEAL{'(ABORT)' if args.abort else ''}: {cycle.name} forward watchlist'\n"
        f"git tag -a {tag} -m 'forward {seal_kind} {now} manifest sha256 {mhash}'\n"
        f"git push origin main --tags\n"
        # R11-3: 서버가 기록한 시각은 push 이벤트뿐이다 (tag/commit 날짜는
        # 클라이언트 제공값). Events API는 ~90일 보존이므로 push 직후에
        # 받아 파일로 남긴다 — 봉인 대상(SEALED_FILES) 밖의 보조 증거.
        f"curl -sS https://api.github.com/repos/lastwhisper906-gif/aaer-evals/events "
        f"> {cycle_display}/push_event_{now[:10]}.json && "
        f"git add {cycle_display}/push_event_{now[:10]}.json && "
        f"git commit -m 'SEAL: push event receipt' && git push")
    record.write_text(f"""# SEAL_RECORD.md — {cycle.name}

{status_lines}- sealed_at (UTC): {now}
- MANIFEST.sha256 자체의 sha256: `{mhash}`
- 봉인 시점 git HEAD (매니페스트 커밋 이전): `{head}`
- OpenTimestamps: {ots_status}
- 지연/중단 기록: (해당 시 일자 기입 — spec §3)

## 소유자 봉인 명령 (즉시 실행 — OTS 앵커 + push 이벤트 영수증이 외부 증거)

```bash
{owner_cmds}
```

## 외부 검증 방법 (제3자용)

1. **OpenTimestamps — 유일한 비가역 앵커** (무료·무계정):
   `ots verify MANIFEST.sha256.ots` (클라이언트:
   `pip install opentimestamps-client`). 앵커 pending이면 수 시간 후
   `ots upgrade MANIFEST.sha256.ots` 후 재검증. **.ots 부재는 검증 실패로
   취급한다** (`forward_verify_seal.py`가 정규 봉인에서 exit 1).
2. **GitHub push 이벤트 영수증** (보조): `push_event_*.json` — 봉인 push
   직후 Events API에서 받은 서버 기록. 주의: 태그·커밋의 `tagger.date`/
   `committer.date`는 **클라이언트가 제출한 값**이며(`GIT_COMMITTER_DATE`로
   설정 가능) 서버 기록 시각이 아니다 — 저자 소급 조작을 배제하지 못하므로
   앵커로 인용하지 않는다. Events API 보존은 약 90일이라 그 이후 독립
   확인은 위 (1)에 의존한다.
3. **로컬 무결성**: `python tools/forward_verify_seal.py --cycle {cycle_display}`
4. **run-output 사슬** (R6-7 — runs/ 출력 보유 검증자): `python
   tools/forward_validate.py --cycle {cycle_display} --runs {runs_display}`
   — scores.json의 `run_output_sha256`를 러너 출력 실측 재해시로 대조.
""", encoding="utf-8")
    if ots_bin is None:
        print("NOTE — ots 부재: `pip install opentimestamps-client` 후 "
              f"`ots stamp {manifest}` 실행, .ots 파일 커밋 (무료)")
    print(f"{'ABORT-' if args.abort else ''}SEALED — manifest {mhash}\n"
          f"소유자 명령:\n{owner_cmds}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
