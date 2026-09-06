"""RP-14 서명 diff 적용기 (D40) — 소유자 서명 결과를 Issue 초안에 반영한다.

서명 (2026-07-11, 소유자 대화형 세션 — decisions_log D40):
  - DIFF-1 (ISSUE_2 §3 crux, HUBG 단일 robust 케이스 병기): 적용 (원문 그대로)
  - DIFF-2 (ISSUE_2 §2 gate k=5 band 병기): 적용 (원문 그대로)
  - DIFF-3 (ISSUE_1 §5 논증 사슬 재배선): **수정 적용** — Q-E02(A) 정합으로
    name-ID 값을 25% → 21.9%(동결 name_match 규칙, 7/32) 1차 + 25%
    rename-aware 사람 판독(DAR 경계 케이스) 병기로 치환. 그 외 문구는
    RP-14 diff 원문 그대로.

동작:
  - 각 diff는 대상 파일의 앵커 문자열 완전 일치(exact match)로만 적용.
  - 멱등: 적용 후 문자열이 이미 존재하면 건너뛴다.
  - 앵커가 없고 적용 흔적도 없으면 실패(exit 1) — 수기 개입 요구.

사용:  python tools/apply_rp14_diffs.py [--dry-run]
"""
import argparse
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ISSUE_1 = os.path.join(ROOT, "analysis", "ISSUE_1_WAVE2_DRAFT.md")
ISSUE_2 = os.path.join(ROOT, "analysis", "ISSUE_2_HOLDOUT_DRAFT.md")

# ---------------------------------------------------------------- DIFF-1
DIFF1_OLD = """is weaker than on memorized cases. That independently confirms Issue #0's R3 headline
("separation is part memory, part analysis") on the axis where memory is impossible."""

DIFF1_NEW = """is weaker than on memorized cases. **After E1, the holdout evidence rests on a
single robust case (HUBG — above all three matched controls, ≥50 in 5/5 redraws);
the other two cases show no separation.** That independently confirms Issue #0's R3 headline
("separation is part memory, part analysis") on the axis where memory is impossible."""

# ---------------------------------------------------------------- DIFF-2
DIFF2_OLD = """identity now adds information rather than contamination."""

DIFF2_NEW = """identity now adds information rather than contamination.

**Gate elevated to k=5 (2026-07-10; rules and interpretations pre-committed at
`analysis/GATE_K5_PLAN.md` before any probe call).** Re-probing each admitted
company four more times: knows_event **0/5 per case** (HUBG · WMK · GNE), with
the Hertz positive control re-verified True at high confidence. Under the
pre-committed rule (≥2/5 recognitions would have revoked eligibility), the
admission of all three cases is **robust to draw noise**. The published gate
value remains the draw-1 3/3; the k=5 band is co-reported, never a replacement."""

# ---------------------------------------------------------------- DIFF-3 (수정 적용 — Q-E02(A) 정합)
DIFF3_OLD = """**The contrast is the finding.** Wave-1's famous cases fired R3 (memorization
entangled). Wave-2's less-famous cases fire R4 — the separation survives both the
memorization check and the mechanical-baseline check, and the name-prediction probe
identifies only **25%** of wave-2 firms (vs wave-1's 50%), confirming weaker
memorization. Two misses (CSC, BRX) are themselves memorization-crossed cases."""

DIFF3_NEW = """**The contrast is the finding — but "less memorized" needs precise scoping.**
Wave-1's famous cases fired R3 (memorization entangled); wave-2 fires R4. The
name-prediction probe identifies only **21.9%** of wave-2 firms (frozen
name_match rule, 7/32; 25% under a rename-aware human reading — the DAR
boundary case) (vs wave-1's 50%) — but that "less memorized" premise is
**strictly confined to the name-ID instrument**. On the direct instrument,
wave-2 outcome-knowledge is high: the model recalls the
enforcement/restatement event for **8 of 9** treatment cases (direct probe,
88.9%, CP [51.7%, 99.7%]). The basis for the residual-capability claim is
therefore **not** reduced fame, but three independent observations:
(a) **identity-masked scores do not collapse** — identity-perturbation
dominance 3/9 single-draw and 4/9 median across E3 redraws, both below the
pre-registered 5/9 bar; (b) **scores do not respond to identity manipulation**
— the pre-registered 3-arm experiment reads a≈b≈c, median(b−a) = +6.0pp,
under the 10pp bar (the clean b−a contrast; the c−b arm is confounded by
scale restoration, and inter-arm deltas carry draw noise — `synthesis.md` §1b);
(c) **detection persists in the un-memorizable holdout** — recognition gate
robust at k=5 (knows_event 0/5 per case). In one sentence: **knowledge exists
(8/9), but the evidence of it functioning as a score falls short of every
pre-registered bar** — directional evidence only; causality is not declared
confirmed. Two misses (CSC, BRX) are themselves memorization-crossed cases."""

DIFFS = [
    ("DIFF-1", ISSUE_2, DIFF1_OLD, DIFF1_NEW),
    ("DIFF-2", ISSUE_2, DIFF2_OLD, DIFF2_NEW),
    ("DIFF-3", ISSUE_1, DIFF3_OLD, DIFF3_NEW),
]


def apply_one(name, path, old, new, dry_run):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    if new in text:
        print(f"{name}: SKIP (이미 적용됨) — {os.path.relpath(path, ROOT)}")
        return True
    if old not in text:
        print(f"{name}: FAIL — 앵커 문자열 없음 (적용 흔적도 없음): {os.path.relpath(path, ROOT)}")
        return False
    if text.count(old) != 1:
        print(f"{name}: FAIL — 앵커가 유일하지 않음 ({text.count(old)}회)")
        return False
    if dry_run:
        print(f"{name}: WOULD APPLY — {os.path.relpath(path, ROOT)}")
        return True
    with open(path, "w", encoding="utf-8") as f:
        f.write(text.replace(old, new, 1))
    print(f"{name}: APPLIED — {os.path.relpath(path, ROOT)}")
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    ok = all(apply_one(*d, dry_run=args.dry_run) for d in DIFFS)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
