"""Wave-2 보정 — RP-13/P1. 동결 calibration.py(wave-1)의 정의를 그대로 wave-2에 적용.

정의 (calibration.py와 동일, 사전 명시):
  예측 확률 = misstatement_probability/100, 라벨 = fraud 1 / control 0.
  ECE = 10-bin, 확신 = |p−50|/50, 정오 = 임계(p>=50) 판정의 정오.
입력: analysis/wave2_results.json (동결 wave-2 점수, 재채점 없음).
출력: analysis/calibration_wave2.json
비교: wave-1 ECE 0.209 (analysis/calibration.json) — "개선 없음(여전히 미보정)"도
      보고 대상 발견(null-ish)이다.
결정론·네트워크 없음. `python analysis/calibration_wave2.py`.
"""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def main() -> int:
    r = json.load(open(REPO / "analysis/wave2_results.json", encoding="utf-8"))["original"]
    pts = [(s / 100, 1) for s in r["fraud_scores"]] + [(s / 100, 0) for s in r["control_scores"]]
    n = len(pts)

    bins = [[] for _ in range(10)]
    for p, y in pts:
        bins[min(int(p * 10), 9)].append((p, y))
    ece = 0.0
    diagram = []
    for b in bins:
        if not b:
            diagram.append(None)
            continue
        mp = sum(p for p, _ in b) / len(b)
        my = sum(y for _, y in b) / len(b)
        ece += (len(b) / n) * abs(mp - my)
        diagram.append({"n": len(b), "mean_pred": round(mp, 3), "frac_pos": round(my, 3)})

    conf = [abs(p * 100 - 50) / 50 for p, _ in pts]
    corr = [1 if ((p * 100 >= 50) == bool(y)) else 0 for p, y in pts]
    pos = [conf[i] for i in range(n) if corr[i]]
    neg = [conf[i] for i in range(n) if not corr[i]]
    auroc = (sum((a > b) + 0.5 * (a == b) for a in pos for b in neg)
             / (len(pos) * len(neg))) if pos and neg else None

    out = {
        "n": n, "n_fraud": 9, "n_control": 23,
        "ece_10bin": round(ece, 3),
        "wave1_ece_10bin_reference": 0.209,
        "delta_vs_wave1": round(ece - 0.209, 3),
        "confidence_correctness_auroc": round(auroc, 3) if auroc is not None else None,
        "threshold_accuracy": f"{sum(corr)}/{n}",
        "reliability_diagram_10bin": diagram,
        "interpretation": ("ECE 0.179 vs wave-1 0.209 — 동일 차수. 보정이 실질적으로 "
                           "개선되지 않았다(여전히 ~0.18 미보정). null-ish, 보고 대상."),
        "note": "동결 wave-2 점수 재사용, 재채점 없음. 정의는 calibration.py와 동일.",
    }
    (REPO / "analysis/calibration_wave2.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wave-2 ECE={out['ece_10bin']} (wave-1 {out['wave1_ece_10bin_reference']}, "
          f"Δ{out['delta_vs_wave1']:+}) · conf-AUROC={out['confidence_correctness_auroc']} · "
          f"acc={out['threshold_accuracy']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
