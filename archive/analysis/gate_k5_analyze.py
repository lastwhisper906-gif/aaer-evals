"""recognition gate k=5 기계 판정 (GATE_K5_PLAN §2 — 결정론, 재해석 없음).

입력: runs/holdout/recognition/{T}.json (draw-1, 동결) +
      runs/holdout/recognition_k5/draw_{2..5}/{T}.json +
      runs/holdout/recognition_k5/positive_control/HTZ.json
출력: analysis/gate_k5_results.json — 케이스별 band(x/5)·판정·결과 방향(i/ii/iii)
규칙(사전 고정, D32): band ≥2/5 → INELIGIBLE(홀드아웃 자격 상실) · ≤1/5 → ELIGIBLE.
HTZ knows_event=False → SENSITIVITY_FAIL (전체 해석 불능 — exit 2).
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CASES = ["HUBG", "WMK", "GNE"]
DRAW1_DIR = REPO / "runs/holdout/recognition"
K5_DIR = REPO / "runs/holdout/recognition_k5"
OUT = REPO / "analysis/gate_k5_results.json"

RULE = {"ineligible_min_true": 2, "k": 5}


def load(path: Path) -> bool:
    d = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(d.get("knows_event"), bool):
        raise SystemExit(f"malformed transcript (knows_event 아님): {path}")
    return d["knows_event"]


def main() -> int:
    missing = []
    draws = {}  # ticker -> [draw1..draw5] knows_event bool
    for t in CASES:
        seq = []
        p1 = DRAW1_DIR / f"{t}.json"
        if not p1.exists():
            missing.append(str(p1))
        else:
            seq.append(load(p1))
        for n in range(2, 6):
            pn = K5_DIR / f"draw_{n}" / f"{t}.json"
            if not pn.exists():
                missing.append(str(pn))
            else:
                seq.append(load(pn))
        draws[t] = seq
    htz_path = K5_DIR / "positive_control" / "HTZ.json"
    if not htz_path.exists():
        missing.append(str(htz_path))
    if missing:
        print("FAIL — transcript 미완 (판정은 전량 존재 시에만):")
        for m in missing:
            print("  ", m)
        return 1

    htz_ok = load(htz_path)
    result = {
        "rule": RULE,
        "positive_control_HTZ_knows_event": htz_ok,
        "cases": {},
    }
    if not htz_ok:
        result["verdict"] = "SENSITIVITY_FAIL"
        result["note"] = ("양성대조 HTZ가 knows_event=False — 계기 무감 가능성, "
                          "0/5 결과 해석 금지 (GATE_K5_PLAN §2). OWNER_QUEUE 이관.")
        OUT.write_text(json.dumps(result, ensure_ascii=False, indent=1) + "\n",
                       encoding="utf-8")
        print("SENSITIVITY_FAIL — HTZ knows_event=False. 해석 불능, OWNER_QUEUE 이관.")
        return 2

    bands = {}
    for t in CASES:
        n_true = sum(draws[t])
        bands[t] = n_true
        result["cases"][t] = {
            "draws_knows_event": draws[t],
            "band_true_of_5": n_true,
            "verdict": ("INELIGIBLE" if n_true >= RULE["ineligible_min_true"]
                        else "ELIGIBLE"),
        }

    inel = [t for t in CASES if result["cases"][t]["verdict"] == "INELIGIBLE"]
    if all(b == 0 for b in bands.values()):
        direction = "i"
    elif bands["HUBG"] >= 2 and bands["WMK"] < 2 and bands["GNE"] < 2:
        direction = "ii"
    else:
        direction = "iii"
    result["outcome_direction"] = direction
    result["ineligible"] = inel
    result["hold_issue2"] = "HUBG" in inel  # (ii) 또는 HUBG 포함 (iii)

    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=1) + "\n",
                   encoding="utf-8")
    for t in CASES:
        c = result["cases"][t]
        print(f"{t}: band {c['band_true_of_5']}/5 → {c['verdict']}"
              f"  (draws {c['draws_knows_event']})")
    print(f"outcome direction: ({direction}) — 해석 문장은 GATE_K5_PLAN §3 사전 등록분만.")
    if result["hold_issue2"]:
        print("!! HUBG INELIGIBLE — OWNER_QUEUE 긴급: Issue #2 발행 보류 (§2).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
