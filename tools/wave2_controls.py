"""Wave-2 대조군 선정 드라이버 — 동결 control_v2 순수 함수 재사용 (I3: runs/wave2/ 격리).

pre-registration: EXCLUSION.md §6 (동결 순수 함수 그대로, 케이스당 2-3, 기존 22 dedup).
ANALYSIS_PLAN_WAVE2 §7 (알파벳 순서). 이 드라이버는 control_v2.py를 **수정하지 않고**
모듈 전역만 재지향한다 (CASES_V2 = wave-2 9사, 출력 경로 → runs/wave2/). E1-E9 하드
스크린·E8b·S0/S1/S2 랭킹은 control_v2의 동결 함수가 verbatim 수행.

케이스 스펙 유도 (결정론·오프라인, 점수 독립):
  cik/cutoff        <- data/candidates/candidates.json (동결 킬스위치 폭로일=전일)
  sic_primary       <- EDGAR submissions meta.sic (객관 필드)
  fye_month         <- XBRL 연차 기간말 최빈월 (era-correct PIT — 현재값 한계 제거,
                       wave-1 대비 규율 개선; UAA 현재값 3월[FY 변경] → era 12월 교정)
  rev_pit/assets_pit<- 동결 rp08_common.pit_size (BRX는 REIT라 RealEstateRevenueNet 대체)
  sic_supp          <- 2-digit major group decade 코드 규칙 (wave-1 hand-declared 대체:
                       재량 제거·uniform; 빈 SIC는 무해 — control_v2 실증). primary 제외.

사용:  python3 tools/wave2_controls.py {fetch|validate|select}
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import control_v2 as cv

REPO = Path(__file__).resolve().parents[1]

# 유도 완료 스펙 (scratchpad/derive_wave2_specs.py 재현 — 점수 독립 1차 자료)
WAVE2_CASES = {
 "T02": {"ticker":"CSC","cik":"0000023082","cutoff":"2010-08-10","fye_month":4,
         "rev_pit":16128000000,"assets_pit":16455000000,"sic_primary":["7373"],
         "sic_supp":["7300","7310","7320","7330","7340","7350","7360","7370","7380","7390"]},
 "T04": {"ticker":"WFT","cik":"0001453090","cutoff":"2011-02-28","fye_month":12,
         "rev_pit":8826933000,"assets_pit":19884443000,"sic_primary":["1381"],
         "sic_supp":["1300","1310","1320","1330","1340","1350","1360","1370","1390"]},
 "T19": {"ticker":"OSIR","cik":"0001360886","cutoff":"2015-11-05","fye_month":12,
         "rev_pit":59867000,"assets_pit":103007000,"sic_primary":["2836"],
         "sic_supp":["2800","2810","2820","2830","2840","2850","2860","2870","2880","2890"]},
 "T20": {"ticker":"BRX","cik":"0001581068","cutoff":"2016-02-07","fye_month":12,
         "rev_pit":1236599000,"assets_pit":9527623000,"sic_primary":["6798"],
         "sic_supp":["6700","6710","6720","6730","6740","6750","6760","6770","6780","6790"]},
 "T22": {"ticker":"TNGO","cik":"0001182325","cutoff":"2016-03-06","fye_month":12,
         "rev_pit":212476000,"assets_pit":227672000,"sic_primary":["7372"],
         "sic_supp":["7300","7310","7320","7330","7340","7350","7360","7370","7380","7390"]},
 "T23": {"ticker":"HAIN","cik":"0000910406","cutoff":"2016-08-14","fye_month":6,
         "rev_pit":2688515000,"assets_pit":3231166000,"sic_primary":["2000"],
         "sic_supp":["2010","2020","2030","2040","2050","2060","2070","2080","2090"]},
 "T24": {"ticker":"CGI","cik":"0000865941","cutoff":"2017-04-04","fye_month":6,
         "rev_pit":1065356000,"assets_pit":981722000,"sic_primary":["4213"],
         "sic_supp":["4200","4210","4220","4230","4240","4250","4260","4270","4280","4290"]},
 "T26": {"ticker":"MDXG","cik":"0001376339","cutoff":"2016-12-14","fye_month":12,
         "rev_pit":187296000,"assets_pit":181665000,"sic_primary":["3841"],
         "sic_supp":["3800","3810","3820","3830","3840","3850","3860","3870","3880","3890"]},
 "T29": {"ticker":"UAA","cik":"0001336917","cutoff":"2019-11-02","fye_month":12,
         "rev_pit":5193185000,"assets_pit":4679908000,"sic_primary":["2300"],
         "sic_supp":["2310","2320","2330","2340","2350","2360","2370","2380","2390"]},
}

# I3: 출력 경로를 runs/wave2/로 재지향 (동결 runs/rp09/ 불침해)
RAW2 = REPO / "runs/wave2/control_pool_raw"
cv.RAW2 = RAW2
cv.PROV2 = RAW2 / "provenance.jsonl"
cv.MANIFEST2 = RAW2 / "MANIFEST.sha256"
cv.QUARANTINE2 = RAW2.parent / "quarantine/quarantine.json"
cv.OUT2 = RAW2.parent / "control_group_v2.json"
cv.CASES_V2 = WAVE2_CASES  # 동결 select/fetch가 이 전역을 읽는다


def main() -> int:
    cmds = {"fetch": cv.cmd_fetch, "validate": cv.cmd_validate, "select": cv.cmd_select}
    if len(sys.argv) != 2 or sys.argv[1] not in cmds:
        print("usage: wave2_controls.py {fetch|validate|select}", file=sys.stderr)
        return 2
    return cmds[sys.argv[1]]()


if __name__ == "__main__":
    sys.exit(main())
