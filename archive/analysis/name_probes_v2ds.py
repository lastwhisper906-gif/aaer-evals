"""Q-F05 v2 date-shift name-ID 판정 — 사전 등록 엔드포인트 (specs/perturb_v2.md §5).

판정 = 동결 scoring/probe_verdict.name_match 규칙 그대로 (재해석 금지 — Q-E02(A)
규약 유지: DAR형 구명 경계는 규칙 판정이 1차, 사람 판독은 각주 병기 대상).

입력: scoring/probe_results_v2ds_wave1/recognition/ (30 = 8 treatment + 22 control)
      scoring/probe_results_v2ds_wave2/recognition/ (32)
비교 기준선 (동결 v1, 사전 등록): wave-1 50% [15/30] · wave-2 21.9% [7/32].
출력: analysis/name_probe_results_v2ds_rev2.json

R7-11 (rev2, disclose-don't-revise — INV-03/06): 원 산출물
analysis/name_probe_results_v2ds.json은 동결 보존 — cp95_pct 라벨이 k=0에서
stats.fpr_bound의 rule-of-three(300/n)를 실었다 (wave-2 0/32 → 9.4, 정확
CP95 상한은 10.9). rev2는 전 k에서 정확 Clopper-Pearson(양측 95%,
holdout_controls_analyze.clopper_pearson — RESULTS 행 4와 동일 규칙)을 쓰고
신규 병행 경로에 기록한다. 공개: DECISIONS_PENDING.md D-P92 (D84 참조).

실행: .venv/bin/python analysis/name_probes_v2ds.py   (무호출·결정론)
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scoring"))
sys.path.insert(0, str(REPO / "analysis"))
from probe_verdict import name_match  # noqa: E402 (동결 판정 규칙)
from aaer_eval.manifest import load_experiment  # noqa: E402
from holdout_controls_analyze import clopper_pearson  # noqa: E402 (정확 CP — R7-11)

V1_FROZEN = {"wave1": {"rate_pct": 50.0, "count": "15/30"},
             "wave2": {"rate_pct": 21.9, "count": "7/32"}}
W1_DIR = REPO / "scoring" / "probe_results_v2ds_wave1" / "recognition"
W2_DIR = REPO / "scoring" / "probe_results_v2ds_wave2" / "recognition"


def wave1_rows() -> list[dict]:
    """wave-1 30사 — 진실 매핑은 name_probes.py(동결 분석)와 동일 경로."""
    m1 = json.loads((REPO / "scoring/id_mapping.json").read_text())["mapping"]
    m2 = json.loads((REPO / "scoring/id_mapping_v2.json").read_text())["mapping"]
    cands1 = {c["case_id"]: c for c in json.loads(
        (REPO / "data/candidates/candidates.json").read_text())["candidates"]}
    cands2 = {c["case_id"]: c for c in json.loads(
        (REPO / "data/candidates/candidates_v2_controls.json").read_text())["candidates"]}
    rows = []
    for entry in load_experiment("main/name_probe_v2ds_wave1").values():
        p = entry.path
        j = json.loads(p.read_text(encoding="utf-8"))
        cid = p.stem
        num = int(cid.split("_")[1])
        mapping, cands, grp = (m1, cands1, "fraud") if num <= 16 else (m2, cands2, "control")
        truth = cands[mapping[cid]]
        rows.append({"case_id": cid, "group": grp,
                     "truth_ticker": truth["ticker"].split("/")[0],
                     "guess": j["company_guess"], "confidence": j["confidence"],
                     "recognized": bool(name_match(j["company_guess"],
                                                   truth["company_name"]))})
    return rows


def wave2_rows() -> list[dict]:
    cases = {c["case_id"]: c for c in json.loads(
        (REPO / "data/evaluatee/cases_wave2.json").read_text())["cases"]}
    rows = []
    for entry in load_experiment("wave2/name_probe_v2ds_wave2").values():
        p = entry.path
        j = json.loads(p.read_text(encoding="utf-8"))
        c = cases[p.stem]
        rows.append({"case_id": p.stem, "truth_ticker": c["ticker"],
                     "guess": j["company_guess"], "confidence": j["confidence"],
                     "recognized": bool(name_match(j["company_guess"],
                                                   c["company_name"]))})
    return rows


def frame(rows: list[dict], expect_n: int, tier: str) -> dict:
    if len(rows) != expect_n:
        raise SystemExit(f"{tier}: {len(rows)}/{expect_n} — 프로브 미완, 판정 보류")
    k = sum(r["recognized"] for r in rows)
    # R7-11: 전 k(0·n 극점 포함)에서 정확 Clopper-Pearson 양측 95% — 라벨과
    # 계산 일치. (구판 stats.fpr_bound는 k=0에서 rule-of-three로 낙하 —
    # 0/32 → 9.4는 정확 CP95 10.9보다 반보수적, 방법 라벨 불일치.)
    lo, hi = clopper_pearson(k, len(rows))
    return {"n": len(rows), "recognized": k,
            "rate_pct": round(100 * k / len(rows), 1),
            "cp95_pct": [round(100 * lo, 1), round(100 * hi, 1)],
            "v1_frozen": V1_FROZEN[tier], "rows": rows}


def main() -> int:
    out = {"spec": "specs/perturb_v2.md §5 (사전 등록 엔드포인트)",
           "verdict_rule": "동결 scoring/probe_verdict.name_match — 재해석 금지",
           "wave1": frame(wave1_rows(), 30, "wave1"),
           "wave2": frame(wave2_rows(), 32, "wave2")}
    for tier in ("wave1", "wave2"):
        f = out[tier]
        f["delta_vs_v1_pp"] = round(f["rate_pct"] - f["v1_frozen"]["rate_pct"], 1)
    out["reading_guard"] = (
        "사전 등록 비교는 rate 병기까지 — v2가 낮으면 '날짜 지문 제거가 name-ID "
        "채널을 추가로 좁혔다', 같으면 '날짜 외 지문(수치 자체)이 지배'. 인과 "
        "서술은 이 두 문장 밖으로 나가지 않는다 (원인 분해는 소유자 검토 대상).")
    # R7-11: 원 경로는 동결 — rev2는 병행 신규 경로에만 기록 (INV-06)
    p = REPO / "analysis" / "name_probe_results_v2ds_rev2.json"
    p.write_text(json.dumps(out, ensure_ascii=False, sort_keys=True, indent=1) + "\n",
                 encoding="utf-8")
    print(f"wave-1 v2ds {out['wave1']['recognized']}/30 = {out['wave1']['rate_pct']}% "
          f"(v1 50%) · wave-2 {out['wave2']['recognized']}/32 = "
          f"{out['wave2']['rate_pct']}% (v1 21.9%) → {p.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
