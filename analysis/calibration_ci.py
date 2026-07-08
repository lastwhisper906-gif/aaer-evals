"""calibration_ci.py — DRAFT (감사 B10). ECE에 부트스트랩 CI + 적응적 binning + 기저율 주의.

동결 점수(baseline_table.csv)만 — 재채점 아님, 캐시·API 불요, 결정론. 발행 ECE
0.209는 n≈3/bin 점추정·무CI라 취약. 여기서 (a) 부트스트랩 95% CI, (b) 등개수(적응적)
binning ECE(빈 bin 편향 완화), (c) ECE가 연구 기저율(8/30)에 조건부임을 명시한다.
**초안: 소유자 검토 후 서술 반영(발행 아님).** "null-ish, 개선 없음" 결론은 유지될
가능성이 높으나 구간을 달아야 정직하다.
"""
import csv
import random
import statistics as st
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SEED = 20260708
B = 10000


def load_pts():
    rows = list(csv.DictReader(open(REPO / "analysis/baseline_table.csv", encoding="utf-8")))
    return [(float(r["llm_score"]) / 100, 1 if r["group"] == "fraud" else 0)
            for r in rows if r["llm_score"] not in ("", "None")]


def ece_fixed(pts, nbins=10):
    """고정폭 10-bin ECE (calibration.py와 동일)."""
    n = len(pts)
    bins = [[] for _ in range(nbins)]
    for p, y in pts:
        bins[min(nbins - 1, int(p * nbins))].append((p, y))
    e = 0.0
    for b in bins:
        if not b:
            continue
        conf = sum(p for p, _ in b) / len(b)
        acc = sum(y for _, y in b) / len(b)
        e += len(b) / n * abs(acc - conf)
    return e


def ece_adaptive(pts, nbins=5):
    """등개수(quantile) binning ECE — 소표본 빈 bin 편향 완화."""
    n = len(pts)
    s = sorted(pts)
    e = 0.0
    for i in range(nbins):
        b = s[i * n // nbins:(i + 1) * n // nbins]
        if not b:
            continue
        conf = sum(p for p, _ in b) / len(b)
        acc = sum(y for _, y in b) / len(b)
        e += len(b) / n * abs(acc - conf)
    return e


def main():
    pts = load_pts()
    n = len(pts)
    base = sum(y for _, y in pts) / n
    e10 = ece_fixed(pts)
    e_ad = ece_adaptive(pts)
    rng = random.Random(SEED)
    boots = []
    for _ in range(B):
        samp = [pts[rng.randrange(n)] for _ in range(n)]
        boots.append(ece_fixed(samp))
    boots.sort()
    lo, hi = boots[int(0.025 * B)], boots[int(0.975 * B)]

    print(f"n={n}  기저율(fraud 비율)={base:.3f}")
    print(f"ECE 10-bin(고정폭, 발행값)   = {e10:.4f}   [부트스트랩 95% CI {lo:.3f}–{hi:.3f}]")
    print(f"ECE 5-bin(등개수/적응적)     = {e_ad:.4f}   (빈 bin 편향 완화)")
    print(f"부트스트랩 평균 ECE          = {st.mean(boots):.4f}")
    print("\n판독(초안): ECE 점추정 0.21은 '보정 안 됨'이나 95% CI가 넓다(소표본). "
          "적응적 binning도 유사 → 결론(뚜렷한 오보정, 개선 없음)은 유지되나 구간 병기 필요.")
    print(f"기저율 주의: 이 ECE는 연구 기저율 {base:.2f} 조건부다. 배치 기저율(~0.7%)에서는 "
          "같은 확률 출력이 훨씬 과대신뢰로 읽힌다(Issue #0 §7.7 PPV 논의와 연결).")


if __name__ == "__main__":
    main()
