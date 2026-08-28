"""봉인 후 무결성 재검증 (spec §9, D100).

usage: python tools/forward_verify_seal.py --cycle forward/cycle_001

MANIFEST.sha256 대비 현재 파일 해시를 전건 재계산 — 불일치·누락·추가를
보고하고 외부 검증 절차를 안내한다. 네트워크 0.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from forward_common import REPO, manifest_text, sha256_text


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
    record = cycle / "SEAL_RECORD.md"
    aborted = (record.is_file()
               and "status: ABORTED" in record.read_text(encoding="utf-8"))
    if not ots.exists():
        if aborted:
            print("NOTICE — abort 봉인: OTS 앵커 부재 허용 (부분 상태 동결)")
            return 0
        print(f"FAIL — OTS 앵커 부재: {ots.name} 없음. 정규 봉인의 외부 시각 "
              "증거가 성립하지 않는다 — `ots stamp MANIFEST.sha256` "
              "(pip install opentimestamps-client) 실행 후 .ots를 커밋하라. "
              "태그·커밋 날짜는 클라이언트 제출값이므로 대체 증거가 아니다.")
        return 1
    print(f"외부 검증: SEAL_RECORD.md §외부 검증 방법 — `ots verify {ots}` "
          "(+ push_event_*.json 보조 영수증)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
