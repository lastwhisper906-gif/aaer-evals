# RP-14 — Issue #1/#2 서사 보강 diff 워크벤치 (D31 0-5 + D39 A-1, 소유자 서명대)

> Authored by Claude Code, pending human audit (GA-001 (b)). 2026-07-10 (DIFF-1/2) ·
> 2026-07-11 (DIFF-3).
> **용도**: `analysis/ISSUE_2_HOLDOUT_DRAFT.md` §3 crux 문단 서사 보강(DIFF-1) ·
> §2 gate k=5 병기(DIFF-2) · `analysis/ISSUE_1_WAVE2_DRAFT.md` §5 논증 사슬
> 재배선(DIFF-3). 3차 외부 검토 지적 반영 — DIFF-1: "signal weakens but does not
> collapse" 류 서사에는 E1 이후의 증거 형상("단일 robust 케이스 의존")을 병기 ·
> DIFF-3: "덜 유명 → 덜 암기 → 잔여 능력" 사슬은 Phase 2 실측(outcome-knowledge
> 8/9)과 모순 — 발행 전 필수 재배선.
> **본 diff들은 미적용 상태다** (0-5 "present diffs only") — 서명 시 세션이 적용,
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

## DIFF-3 — Issue #1 §5 논증 사슬 재배선 (D39 A-1, 발행 전 필수 — 3차 외부 검토)

대상: `analysis/ISSUE_1_WAVE2_DRAFT.md` §5 "The contrast is the finding" 문단.
현행 논증 사슬 "덜 유명 → 덜 암기 → 잔여 능력"은 Phase 2 실측(직접 프로브
outcome-knowledge **8/9 = 88.9%**, D35)과 모순 — "덜 암기" 전제는 name-ID
계기에서만 성립하는 서사다. 잔여 능력 주장의 근거를 유명도 감소가 아니라
세 갈래 독립 관찰 (a)(b)(c)로 재배선한다.

```diff
-**The contrast is the finding.** Wave-1's famous cases fired R3 (memorization
-entangled). Wave-2's less-famous cases fire R4 — the separation survives both the
-memorization check and the mechanical-baseline check, and the name-prediction probe
-identifies only **25%** of wave-2 firms (vs wave-1's 50%), confirming weaker
-memorization. Two misses (CSC, BRX) are themselves memorization-crossed cases.
+**The contrast is the finding — but "less memorized" needs precise scoping.**
+Wave-1's famous cases fired R3 (memorization entangled); wave-2 fires R4. The
+name-prediction probe identifies only **25%** of wave-2 firms (vs wave-1's 50%)
+— but that "less memorized" premise is **strictly confined to the name-ID
+instrument**. On the direct instrument, wave-2 outcome-knowledge is high: the
+model recalls the enforcement/restatement event for **8 of 9** treatment cases
+(direct probe, 88.9%, CP [51.7%, 99.7%]). The basis for the residual-capability
+claim is therefore **not** reduced fame, but three independent observations:
+(a) **identity-masked scores do not collapse** — identity-perturbation
+dominance 3/9 single-draw and 4/9 median across E3 redraws, both below the
+pre-registered 5/9 bar; (b) **scores do not respond to identity manipulation**
+— the pre-registered 3-arm experiment reads a≈b≈c, median(b−a) = +6.0pp,
+under the 10pp bar (the clean b−a contrast; the c−b arm is confounded by
+scale restoration, and inter-arm deltas carry draw noise — `synthesis.md` §1b);
+(c) **detection persists in the un-memorizable holdout** — recognition gate
+robust at k=5 (knows_event 0/5 per case). In one sentence: **knowledge exists
+(8/9), but the evidence of it functioning as a score falls short of every
+pre-registered bar** — directional evidence only; causality is not declared
+confirmed. Two misses (CSC, BRX) are themselves memorization-crossed cases.
```

- **판단 근거 (데이터 포인트)**: ① D35 — `analysis/outcome_recognition_results.json`
  실험군 knows_event 8/9=88.9% CP[51.7%,99.7%] (유일 미인지 OSIR): "덜 암기"가
  사실이려면 직접 계기에서도 낮아야 하나 실측은 높음 — 서사는 name-ID 축(21.9–25%)
  에서만 성립. ② (a)의 근거 — wave-2 dominance 3/9 (`wave2_results.json`) + E3
  재추첨 median 4/9 (`e3_results.json`), 사전 등록 바 5/9 미달. ③ (b)의 근거 —
  `identity_3arm_results.json` median(b−a)=+6.0pp·median(c−b)=−2.0pp, 분류 (ii).
  ④ (c)의 근거 — `gate_k5_results.json` HUBG·WMK·GNE 전건 0/5 (D33).
- **학습 노트 (이 판단에서 알아야 할 것)**: "덜 암기됐다"는 주장은 계기 의존적이다
  — 같은 표본이 name-ID 계기로는 덜 암기(21.9%), outcome-knowledge 계기로는 광범위
  암기(88.9%)로 읽힌다. 잔여 능력 주장은 암기의 *부재*가 아니라 암기가 *점수로
  기능한다는 증거의 부재*(세 갈래 바 미달)에 얹어야 무너지지 않는다.

## 서명

- **서명 DIFF-1**: ☐ 적용 (diff 그대로)   ☐ 수정 적용 (문구: __________)   ☐ 기각 (사유: __________ → overrides.md)
- **서명 DIFF-2**: ☐ 적용 (diff 그대로)   ☐ 수정 적용 (문구: __________)   ☐ 기각 (사유: __________ → overrides.md)
- **서명 DIFF-3**: ☐ 적용 (diff 그대로)   ☐ 수정 적용 (문구: __________)   ☐ 기각 (사유: __________ → overrides.md)
- 연동: `docs/OWNER_QUEUE.md` Q-R01 (범위 = DIFF-1/2/3). Phase 1(k=5 gate) 결과가
  HUBG 자격 상실로 나오면 DIFF-1은 무효화되고 Q-R01의 긴급 항목이 우선한다 —
  **실측: 자격 유지 (0/5×3), 긴급 항목 비발동.**
- DIFF-3은 Issue #1 발행에 선행하는 **발행 전 필수(3차 외부 검토)** 항목이다 —
  기각 시 Issue #1 발행은 논증 사슬 모순을 안은 채 나가게 되므로, 기각이면
  대체 문안 확정까지 Issue #1 발행 보류를 권고.
