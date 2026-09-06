# specs/calibration_scope.md — 보정(calibration) 주장 재범위화 (WS-4 / F-7)

> **범위 선언**: 본 워크스트림은 **주장 표면(claim surface)**만 다룬다.
> 동결 데이터·점수·ECE 수치는 무변경. 발행 표면 수정은 diff-only
> (`review_packets/RP-16_calibration_language_diff.md`, 게이트 Q-F04).
> **`schemas/llm_output.json`의 `misstatement_probability` 필드는 개명하지
> 않는다** — 개명은 커밋된 출력의 재현을 깨뜨린다. 개명은 §4의 Cycle-2
> 등록 항목이다.

## 1. 발행 점수의 해석 규약 (선언)

발행된 0–100 점수는 **서수(ordinal) 량**으로 해석한다 — 순위·플래그
(임계 50) 기능은 검증되었으나(분리 p=0.00114/0.00116, AUC 0.82/0.83),
**확률로서는 기능하지 않는다**: ECE 0.209(wave-1)·0.179(wave-2), 개선 없음.
"score of 70" ≠ "70% 확률". 발행 표면의 확률 함의 언어는 diff로 정리한다.

## 2. 재보정(recalibration)을 하지 않는 근거 (사전 등록)

- N ≈ 30–60에서 Platt scaling·isotonic regression은 **비닝/적합 노이즈가
  지배**한다 — 보정 곡선 추정 자체가 표본 특이성의 재서술이 된다.
- 소표본 ECE는 그 자체가 **불안정 추정량**이다 (10-bin에 케이스 30개면
  bin당 평균 3개). 따라서 ECE는 **진단 병기(co-report) 전용**으로 유지하고,
  이를 근거로 한 재보정·보정 개선 주장을 모두 배제한다.
- 재보정 시도는 §4의 표본 하한 충족 후에만 재개한다.

## 3. 기대 행동 주석 (파이프라인 결함 아님)

Verbalized-confidence 문헌의 일관 발견: LLM이 말로 표명하는 확신도는
체계적으로 과확신(overconfident)이다. 관측된 과확신형 미보정은 **기대되는
모델 행동**이며 파이프라인 결함의 증거가 아니다 — 신뢰 경계 데이터로
기록한다 (나쁜 결과 미화 금지 원칙과 양립: "보정 안 됨"은 그대로 보고).

## 4. Cycle-2 등록 (이번 사이클 실행 금지)

1. **스키마 필드 개명**: `misstatement_probability` → `misstatement_score`
   — Cycle-2 프레임 재동결 시에만 (커밋 출력 재현성 때문에 소급 불가).
2. **재보정 재개 하한**: 라벨 케이스 **N ≥ 150** 축적 시 재보정(Platt/
   isotonic) 재검토 가능 — 하한은 지금 사전 고정한다.

## 5. 산출물

- 본 스펙 + `review_packets/RP-16_calibration_language_diff.md`
  (발행 표면 `probability` 전수 히트 목록 + 교체안, 직접 수정 0)
  + OWNER_QUEUE Q-F04.

*본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).*
