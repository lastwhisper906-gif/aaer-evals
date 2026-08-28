"""봉인 후 무결성 재검증 (spec §9, D100).

usage: python tools/forward_verify_seal.py --cycle forward/cycle_001

MANIFEST.sha256 대비 현재 파일 해시를 전건 재계산 — 불일치·누락·추가를
보고하고 외부 검증 절차를 안내한다. 네트워크 0.
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from forward_common import REPO, manifest_text, sha256_text
from forward_seal import ABORT_MARKER

# OpenTimestamps 파일 매직 — 0바이트·절단 위조를 형식 단계에서 거른다 (R12-4)
OTS_MAGIC = b"\x00OpenTimestamps"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cycle", required=True)
    args = ap.parse_args()
    cycle = REPO / args.cycle
    manifest = cycle / "MANIFEST.sha256"
    if not manifest.exists():
        print("FAIL — MANIFEST.sha256 부재 (미봉인 사이클)")
        return 1

    recorded = manifest.read_text(encoding="utf-8")
    current = manifest_text(cycle)
    if recorded != current:
        rec = dict(line.split("  ", 1)[::-1] for line in recorded.splitlines() if "  " in line)
        cur = dict(line.split("  ", 1)[::-1] for line in current.splitlines() if "  " in line)
        print("FAIL — 봉인 무결성 위반:")
        for name in sorted(set(rec) | set(cur)):
            if name not in cur:
                print(f"  삭제됨: {name}")
            elif name not in rec:
                print(f"  봉인 후 추가됨: {name}")
            elif rec[name] != cur[name]:
                print(f"  변조됨: {name}")
        return 1

    print(f"PASS — 봉인 무결성 (manifest sha256 {sha256_text(recorded)})")

    # R11-3: OTS는 유일한 비가역 외부 앵커다 — tagger/committer 날짜는
    # 클라이언트 제출값이고 Events API 영수증은 ~90일 보존이다. 앵커 없는
    # 정규 봉인을 PASS로 통과시키면 "외부 검증 가능한 타임스탬프로 불변
    # 봉인"(spec §0)이라는 산출물 주장 자체가 빈다 — fail-closed.
    ots = manifest.with_suffix(".sha256.ots")
    # R12-4: abort 판정은 매니페스트가 해싱하는 evidence/ 마커에서 온다.
    # 종전에는 SEAL_RECORD.md의 부분문자열이었는데 그 파일은 미해시라,
    # 정규 봉인 기록에 `- status: ABORTED (?)` 한 줄을 끼워 넣으면 앵커 없는
    # 봉인이 통과했다. 이제 마커의 추가·삭제는 위 무결성 검사에서 먼저 잡힌다.
    aborted = (cycle / "evidence" / ABORT_MARKER).is_file()
    if not ots.exists():
        if aborted:
            print("NOTICE — abort 봉인(해시된 evidence 마커 기준): OTS 앵커 "
                  "부재 허용 (부분 상태 동결)")
            return 0
        print(f"FAIL — OTS 앵커 부재: {ots.name} 없음. 정규 봉인의 외부 시각 "
              "증거가 성립하지 않는다 — `ots stamp MANIFEST.sha256` "
              "(pip install opentimestamps-client) 실행 후 .ots를 커밋하라. "
              "태그·커밋 날짜는 클라이언트 제출값이므로 대체 증거가 아니다.")
        return 1

    # R12-4: 존재 확인만으로 "앵커 있음"을 단정하지 않는다 — 0바이트 위조
    # 파일도 통과했다. 형식(OTS 매직)을 보고, 클라이언트가 있으면 실제로
    # `ots verify`를 돌린 뒤, 무엇을 확인했고 무엇을 못 했는지 명시한다.
    head = ots.read_bytes()[:len(OTS_MAGIC)]
    if head != OTS_MAGIC:
        print(f"FAIL — OTS 앵커 형식 불일치: {ots.name}가 OpenTimestamps "
              f"파일이 아니다 ({len(ots.read_bytes())}바이트). 위조·절단 의심 "
              "— `ots stamp MANIFEST.sha256`로 다시 생성하라.")
        return 1
    ots_bin = shutil.which("ots")
    if ots_bin is None:
        print(f"외부 검증: {ots.name} 형식 확인까지만 수행했다 (ots 클라이언트 "
              "부재 — 앵커 내용은 **미검증**). `pip install "
              f"opentimestamps-client` 후 `ots verify {ots.name}`로 확인하라.")
        return 0
    r = subprocess.run([ots_bin, "verify", str(ots)], capture_output=True,
                       text=True)
    detail = (r.stdout + r.stderr).strip().splitlines()
    print(f"외부 검증: `ots verify {ots.name}` rc={r.returncode}"
          + (f" — {detail[-1][:160]}" if detail else ""))
    if r.returncode != 0:
        print("NOTICE — 앵커가 아직 pending이면 정상이다 (수 시간 후 "
              f"`ots upgrade {ots.name}` 뒤 재검증). 그 외 사유면 앵커 미성립.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
