"""E1 홀드아웃 대조군 드라이버 — 동결 control_v2 순수 함수 재사용 (I3: runs/holdout/controls/ 격리).

pre-registration: analysis/HOLDOUT_CONTROLS_PLAN.md §1 (CONTROL_CRITERIA_v2 + E8b +
S0-v2, 케이스당 2–3, 수기 지명 금지). wave2_controls.py 패턴 verbatim — control_v2.py를
**수정하지 않고** 모듈 전역만 재지향한다. E1-E9 하드 스크린·E8b·S0/S1/S2 랭킹은
control_v2의 동결 함수가 그대로 수행. fetch는 **감독 하에서만** (Q-E03 RESOLVED:
2026-era 신규 fetch는 look-ahead 위험 — 소유자 입회 필수, §5-1).

케이스 스펙 유도 (결정론·오프라인, 점수 독립 — scratchpad/derive_holdout_specs.py 재현):
  cik/cutoff        <- data/candidates/candidates_holdout.json (동결, 컷오프=폭로 전일)
  sic_primary       <- EDGAR submissions meta.sic (HUBG 4731 / WMK 5411 / GNE 4931)
  fye_month         <- XBRL 연차(340–400d) 기간말 최빈월, filed<=cutoff (전건 12월)
  rev_pit/assets_pit<- 동결 rp08_common.pit_size
  sic_supp          <- 2-digit major group decade 코드 규칙 (wave2_controls와 동일),
                       exact primary 제외

사용:  python3 tools/holdout_controls.py {fetch|validate|select}
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import control_v2 as cv

REPO = Path(__file__).resolve().parents[1]

# 유도 완료 스펙 (2026-07-09 유도 — 점수 독립 1차 자료. HOLDOUT_CONTROLS_PLAN §1
# 프로파일과 정합: HUBG 물류 ~$4B / WMK 식료품 ~$4.8B / GNE 에너지 소매 ~$0.4B)
HOLDOUT_CASES = {
 "case_71": {"ticker":"HUBG","cik":"0000940942","cutoff":"2026-02-04","fye_month":12,
             "rev_pit":3946390000,"assets_pit":2900721000,"sic_primary":["4731"],
             "sic_supp":["4700","4710","4720","4730","4740","4750","4760","4770","4780","4790"]},
 "case_72": {"ticker":"WMK","cik":"0000105418","cutoff":"2026-02-19","fye_month":12,
             "rev_pit":4791730000,"assets_pit":2017813000,"sic_primary":["5411"],
             "sic_supp":["5400","5410","5420","5430","5440","5450","5460","5470","5480","5490"]},
 "case_73": {"ticker":"GNE","cik":"0001528356","cutoff":"2026-03-11","fye_month":12,
             "rev_pit":425202000,"assets_pit":394122000,"sic_primary":["4931"],
             "sic_supp":["4900","4910","4920","4930","4940","4950","4960","4970","4980","4990"]},
}

# I3: 출력 경로를 runs/holdout/controls/로 재지향 (동결 runs/rp09/·runs/wave2/ 불침해)
RAW2 = REPO / "runs/holdout/controls/pool_raw"
cv.RAW2 = RAW2
cv.PROV2 = RAW2 / "provenance.jsonl"
cv.MANIFEST2 = RAW2 / "MANIFEST.sha256"
cv.QUARANTINE2 = RAW2.parent / "quarantine/quarantine.json"
cv.OUT2 = RAW2.parent / "control_group_holdout.json"
cv.CASES_V2 = HOLDOUT_CASES  # 동결 select/fetch가 이 전역을 읽는다


def main() -> int:
    cmds = {"fetch": cv.cmd_fetch, "validate": cv.cmd_validate, "select": cv.cmd_select}
    if len(sys.argv) != 2 or sys.argv[1] not in cmds:
        print("usage: holdout_controls.py {fetch|validate|select}", file=sys.stderr)
        return 2
    return cmds[sys.argv[1]]()


if __name__ == "__main__":
    sys.exit(main())
