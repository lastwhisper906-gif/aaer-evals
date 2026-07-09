# RP-14 — Issue #2 서사 보강 diff 워크벤치 (D31 0-5, 소유자 서명대)

> Authored by Claude Code, pending human audit (GA-001 (b)). 2026-07-10.
> **용도**: `analysis/ISSUE_2_HOLDOUT_DRAFT.md` §3 crux 문단의 서사 보강 1건.
> 3차 외부 검토 지적 반영 — "signal weakens but does not collapse" 류 서사에는
> E1 이후의 증거 형상("단일 robust 케이스 의존")을 병기해야 한다.
> **본 diff는 미적용 상태다** (0-5 "present diffs only") — 서명 시 세션이 적용,
> 기각 시 사유를 overrides.md에 기록.

## DIFF-1 — §3 crux 문단 (ISSUE_2_HOLDOUT_DRAFT.md, "This is the honest crux" 문단)

```diff
 This is the honest crux: strip memorization entirely, and the score does not
 collapse to noise — the most misstatement-like case is still caught — but the signal
-is weaker than on memorized cases. That independently confirms Issue #0's R3 headline
+is weaker than on memorized cases. **After E1, the holdout evidence rests on a
+single robust case (HUBG — above all three matched controls, ≥50 in 5/5 redraws);
+the other two cases show no separation.** That independently confirms Issue #0's R3 headline
 ("separation is part memory, part analysis") on the axis where memory is impossible.
 N is tiny; this is directional existence evidence, not a capability estimate.
```

- **판단 근거 (데이터 포인트)**: E1 결과 `analysis/holdout_controls_results.json` —
  분리는 HUBG 1/3 케이스뿐 (WMK: GO 58에 하회 · GNE: GRDX 78에 하회). k=5 재추첨
  (D27) — HUBG 5/5 robust, WMK·GNE 0/5. 즉 "약화하되 붕괴 아님" 서사의 실체는
  단일 케이스 HUBG이며, 이를 명시하지 않으면 3케이스 전반의 신호 잔존으로
  오독될 수 있다 (3차 검토 지적).
- **학습 노트 (이 판단에서 알아야 할 것)**: 존재 증명(existence proof)의 증거
  단위는 "몇 케이스가 잡혔나"가 아니라 "잡힌 케이스가 얼마나 robust한가"다 —
  N=3에서 1건 robust는 존재 증명으로 유효하되, 서사가 그 1건 의존성을 숨기면
  과장이 된다.

## DIFF-2 — §2 recognition gate 문단에 k=5 band 병기 (D33, Phase 1 결과 반영)

Phase 1 (D32/D33) 결과: HUBG·WMK·GNE 각각 knows_event **0/5** (draws 1–5),
양성대조 HTZ 재검 True(high) — 결과 방향 (i), 자격 3/3 유지
(`analysis/gate_k5_results.json`, transcript `runs/holdout/recognition_k5/`).

```diff
 non-recognition only for the genuinely post-cutoff revelations. The critical
 nuance WMK makes explicit: the model **knows the company** (identity is available)
 but **not the revelation**. That is exactly the holdout premise — under this frame,
 identity now adds information rather than contamination.
+
+**Gate elevated to k=5 (2026-07-10; rules and interpretations pre-committed at
+`analysis/GATE_K5_PLAN.md` before any probe call).** Re-probing each admitted
+company four more times: knows_event **0/5 per case** (HUBG · WMK · GNE), with
+the Hertz positive control re-verified True at high confidence. Under the
+pre-committed rule (≥2/5 recognitions would have revoked eligibility), the
+admission of all three cases is **robust to draw noise**. The published gate
+value remains the draw-1 3/3; the k=5 band is co-reported, never a replacement.
```

- **판단 근거**: `analysis/gate_k5_results.json` — 전 draw knows_event=False,
  판정은 `gate_k5_analyze.py` 기계 적용 (사전 등록 규칙 §2, 해석 문장 (i)).
- **학습 노트**: 단발 게이트의 거짓음성 우려(≈34% 산술)는 k 승격으로만 좁혀진다
  — 0/5는 "인지 없음의 증명"이 아니라 "인지 확률 추정 상한의 하향"이다.

## 서명

- **서명 DIFF-1**: ☐ 적용 (diff 그대로)   ☐ 수정 적용 (문구: __________)   ☐ 기각 (사유: __________ → overrides.md)
- **서명 DIFF-2**: ☐ 적용 (diff 그대로)   ☐ 수정 적용 (문구: __________)   ☐ 기각 (사유: __________ → overrides.md)
- 연동: `docs/OWNER_QUEUE.md` Q-R01. Phase 1(k=5 gate) 결과가 HUBG 자격 상실로
  나오면 DIFF-1은 무효화되고 Q-R01의 긴급 항목이 우선한다 — **실측: 자격 유지
  (0/5×3), 긴급 항목 비발동.**
