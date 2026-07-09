# E5 사전 등록 — wave-2 본채점 재추첨 (안정성 밴드, 최저 우선순위)

> Authored by Claude Code, pending human audit (GA-001 (b)). 2026-07-08, OWNER-GATE-E.
> **E5 첫 채점 전 커밋 (freeze-then-run).** 불변. **최저 우선순위 — E1–E4·P-phase가
> 궤도에 있고 quota 잔여 시에만.** 범위 한정(§5-5): Claude 단일 파이프라인.

## 0. 동기

wave-2 본채점(9v23, identity frame)은 draw-1 단일이다. E5는 **+1 전체 재추첨**으로
p·AUC·median-gap의 draw 간 범위(안정성 밴드)를 보고한다. wave-1 A3(k=5) 축소판(k=2).

## 1. 설계

- **wave-2 32사(실험군 9 + 대조군 23) 전체 +1 draw** (identity frame 본채점 재실행,
  draw-2). 동결 draw-1 불침해. **32 채점 호출** + 채점자 동수.
- draw-2는 모델 확률성만 다르다(동일 페이로드·프롬프트·스키마·핀). perturb 아님 —
  본채점 재현성 측정.
- 산출: `runs/wave2/mainscore_redraw/draw_2/case_NN.json`. cutoff_guard·forbid·pin 전건.

## 2. 지표 (사전 지정)

- draw-1·draw-2 각각: 평균차·순열 p·AUC·median-gap(fraud median − control median).
- **범위 보고**: 각 통계의 [draw-1, draw-2] 범위(밴드). 케이스별 |p_draw2 − p_draw1|
  분포(중위·최대) — 본채점 draw σ 추정.
- 플래그 안정성: p≥50 판정이 draw 간 뒤집힌 케이스 수(경계 케이스 식별 —
  특히 AORT p=50, CSC p=40 등).

## 3. 결론 처리 (사전 명시 — 교체 아님)

- **발행 standalone 수치는 사전 등록된 draw-1 그대로 유지.** E5는 **안정성 밴드**이지
  draw-1 교체가 아니다 (wave-1 A3 선례: 원본 draw가 published, 재추첨은 밴드).
- wave2_summary·Issue #1에 "draw σ 밴드" 병기 (예: "AUC 0.829 [draw 범위 __–__]").
- draw 간 결론 규칙(R4) 전환은 **없음** — E5는 R1–R4 재판정 대상 아님(E3가 교란
  dominance 재판정 담당). E5는 본채점 확률 잡음만 측정.

## 4. 채점 순서 (사전 고정)

case_NN 오름차순(=알파벳 발사순 승계). 케이스 경계마다 freeze·commit·push. 절단 시
완료분까지 부분 밴드 보고(draw-2 부분 = "n/32 재추첨분 밴드", 미완 명시).

## 5. 호출 추정

32 채점 + 32 채점자 = **≈ 64 호출**. 미션 "32 calls"는 채점 기준. 전역 320 cap 계상.
**우선순위 최저** — E1–E4 + P-phase 이후 quota 잔여 시에만(OWNER_QUEUE Q-E01 (C) 승인 하).

## 6. 면책

단일 Claude 파이프라인, k=2. draw-1 published 불변. 발행 안 함(소유자 게이트).

## 7. 로그된 개정 #1 (§5-6 이력 공개) — 2026-07-09: 홀드아웃 본채점 재추첨 arm 추가

> Authored by Claude Code, pending human audit (GA-001 (b)). 본 arm의 어떤 호출도
> 이 개정 커밋 **이후**에만 발사된다 — 사전 등록 조건 충족. 이하 §7 불변.

### 7-1. 동기

홀드아웃 per-case 판정(HUBG 70 · GNE 42 · WMK 32)은 draw-1 단일이다. L-3(비결정론
점추정)을 홀드아웃 자신에게 적용하면, H2의 핵심 근거(HUBG 플래그)가 draw 잡음에
견디는지 측정하지 않고는 headline로 세울 수 없다. wave-1 A3(k=5) 방식을 홀드아웃에
승계한다.

### 7-2. 설계

- **홀드아웃 3사(HUBG·WMK·GNE) × 총 k=5 draw**: draw-1 = 동결 `runs/holdout/scores`
  (불침해, published 유지) + 신규 draw-2..5 (identity frame 본채점 재실행).
- **피평가자 호출만 12건, 채점자 0건** (E3 선례 — 아래 판정 규칙은
  `misstatement_probability`만 사용, d1~d4 채점 불요).
- 산출: `runs/holdout/mainscore_redraw/draw_{2,3,4,5}/case_NN.json`.
  cutoff_guard·forbid·pin(claude-sonnet-5) 전건. draw 경계마다
  `verify_blindness --write-manifest`·commit·push.

### 7-3. 판정 규칙 (사전 커밋)

- **1차 규칙**: HUBG **p≥50 이 5 draw 중 ≥4** (draw-1 포함) → "H2 탐지는 draw 잡음에
  강건(robust)". **≤3/5 → draw-민감으로 보고, 표현 완화 없음.**
- **2차 (밴드 전용, 유의성 주장 없음)**: 3사 각각 5-draw 중위값 + [min, max] 밴드.
  WMK·GNE 는 sub-50 예상 — **≥2 draw에서 p≥50으로 뒤집히면 '불안정'으로 보고**하며
  신규 탐지로 승격하지 않는다.
- **H1(순열 유의성)은 N=3에서 계속 미주장** (E1 사전 등록 §0과 동일).
- **발행 per-case 수치는 draw-1 그대로** (§3 원칙 승계: 재추첨은 밴드이지 교체가 아니다).

### 7-4. 순서·절단

GNE → WMK → HUBG 오름차순 아님 — **case_71(HUBG) → 72 → 73 케이스 순, draw 단위 발사**
(draw-2 전건 → draw-3 전건 → …). 절단 시 완료 draw까지의 부분 밴드 보고("k=n/5", 미완 명시).

### 7-5. 호출 추정·우선순위

12 호출(전역 cap 계상). 본 arm은 **wave-2 +1 draw(§1)와 독립** — wave-2 arm의 최저
우선순위 지위는 불변이며, 본 arm은 OWNER-GATE-E 승인 및 소유자 일정 지시(2026-07-09,
"E1 감독 실행·홀드아웃 k=5 최우선")에 따라 E1 직후 실행한다.

### 7-6. 분석·보고

`analysis/holdout_redraw_analyze.py` (신규, e3_analyze.py 패턴) →
`analysis/holdout_redraw_results.json` + `analysis/holdout_summary.md`·Issue #2 초안에
밴드 병기 (예: "HUBG p=70 [5-draw 범위 __–__, ≥50 판정 _/5]").
