# Eval Spec — v1.1 (Phase 2-1)

> Authored by Claude Code, pending human audit (GA-001 (b), D15).
> v1 작성 후 별도 컨텍스트 self-red-team 1회 반영 (부록 A). freeze 커밋으로 고정.
> 본 결과는 Claude 기반 단일 파이프라인에 한정 (§5-5). 채점: Claude 보조 + 인간 최종 확정.

## 1. 피평가자 과제 (정확한 문언 — 중립화 적용)

파이프라인이 피평가자 모델에 주는 과제 문언 (케이스별 독립 호출, GP-6 3조항):

> You are analyzing the financial reporting quality of {company_name} ({ticker},
> CIK {cik}) using only the structured data provided below, which reflects public
> filings available on or before {cutoff_date}. Do not use any knowledge of events
> after {cutoff_date}. Complete the checklist, then: (a) estimate the probability
> (0–100) that the company's financial statements, as filed to date, contain a
> material misstatement; (b) if you consider a misstatement plausible, describe
> the most likely mechanism(s): which financial statement line items are affected,
> in which direction, and through what accounting treatment. Every finding must
> cite the specific data points provided. If the data is insufficient for an item,
> say so — do not guess.

- **중립화 (D4 self-red-team 점검 항목)**: 문언에 장르 분류 체계(적극/누락), "fraud",
  "manipulation", 사기 문헌 용어(Beneish 등), 그룹 구조(실험군/대조군, 16케이스 중
  절반) 언급 금지. "probability of material misstatement"는 방향 중립.
- 컷오프의 유래(폭로일)는 알리지 않는다 (스키마 v1.1 규약 유지).

## 2. 입력 범위

| 구성 | 내용 | 근거 |
|---|---|---|
| 케이스 필드 | `evaluatee_input` v1.1의 5필드만 | GP-6 페이로드 규약 |
| 구조화 재무 시계열 | point-in-time XBRL 연차·분기 개념표 (Python 결정론 추출, `filed <= cutoff`) | §5-4 수치=Python |
| 제출물 연대기 | 컷오프 전 EDGAR 제출 인덱스 (form type, filing date — NT·8-K·/A 포함) | T2 메타신호 채널 |
| **불포함** | 서사·각주 텍스트 (D10: 이번 사이클 제외, 차기 조건부), 베이스라인 스크린 출력(누출 금지), candidates.json·채점 문서 일체 | D10, 1-1 |

호출 형태: 케이스당 독립 API 호출, 교차 컨텍스트 없음 (GP-9 ①의 성립 조건).

## 3. 출력 계약 (llm_output v1.2 — freeze 전 개정)

v1.1 유지 + 추가 필드 2개 (D4 차원 1·2의 채점 가능성 확보):
- `fraud_probability`: integer 0–100 (필수) — 문언은 "material misstatement probability".
- `mechanism_hypotheses`: array (misstatement 개연 시 ≥1) — 항목:
  `{affected_line_items[], direction(overstated|understated), accounting_treatment(자유 서술), rationale_evidence[]}`.
  장르 어휘를 스키마에 넣지 않는다 — 장르 판정은 채점자가 서술로부터 매핑.

## 4. 채점 루브릭 — 4차원 분리 채점 (D4)

채점자(D6: grader 모델 + 인간 감사)는 정답 키(candidates.json, genre_tags.md,
명령문 원문)와 피평가자 출력을 받고, 차원별 독립 점수를 매긴다.
피평가자는 채점자 자료를 절대 받지 않는다.

### 차원 1 — misstatement 확률 (보정)
- 케이스 점수: 실험군 p≥70 → 2 / 40≤p<70 → 1 / p<40 → 0. 대조군은 역방향
  (p≤30 → 2 / 30<p≤60 → 1 / p>60 → 0).
- 집계: 16케이스 Brier score (실험군=1, 대조군=0, p/100 대비) 병기.
  주의: 대조군의 라벨 0은 "비집행"이지 "무결"이 아님 — '조용한 미적발' 혼입
  가능성을 집계 해석에 명기 (GP-8 한계).

### 차원 2 — 기제 식별 (실험군 전용, 0–3)
- 0: 기제 서술 없음 또는 명령문과 무관한 계정.
- 1: 영향 계정 영역 일치 (예: 매출 관련임을 지목).
- 2: 계정 + 방향 + 회계 처리 유형이 명령문 서술과 실질 일치.
- 3: 2에 더해 케이스 특이 구조(예: 유통사 계약 조건, 리베이트 시점) 근접.
- 앵커 기준 = 명령문 원문 서술 (genre_tags.md 인용 pinpoint). 대조군: N/A
  (단, 대조군에 기제를 강하게 주장하면 차원 1에서 이미 감점 — 이중 감점 금지).

### 차원 3 — 장르 분류 (실험군 전용)
- 채점자가 `mechanism_hypotheses` 서술을 active / omission-estimate / mixed로
  매핑 → `scoring/genre_tags.md`와 대조: 일치 2 / 부분(mixed 한쪽) 1 / 불일치 0.
- 피평가자에게 이 분류 체계는 노출되지 않았으므로, 이 차원은 "서술의 실질"을
  평가한다 — 매핑 판정 자체가 §7 대상 (grader 1차 + 인간 감사).

### 차원 4 — 인용 근거 품질 (전 케이스, 0–3)
- 0: 인용이 제공 데이터에 없는 값(날조) 또는 논거와 무관.
- 1: 인용 존재하나 일반론적 (구체 수치·항목 미지시).
- 2: 구체 데이터 포인트가 논거를 실제 지지.
- 3: 2에 더해 다년 추세·복수 데이터 포인트의 정합적 결합.
- `memorization_suspect`(L-1 기계 규칙 2단) 판정과 결합: 플래그 케이스는
  집계 두 벌 병기.

## 5. 성공 기준 / 실패 정의 (존재 증명 어법 — 3-6)

- **성공 기준**: "블라인드 구조화 데이터만으로 명령문이 서술한 기제 X를 식별한
  케이스가 존재한다"를 케이스 단위로 입증/반증 + 장르별 비대칭의 방향 관찰.
- **실패 정의**: (a) 스키마 불통과·인용 날조(차원 4=0)가 다수 → 파이프라인/모델
  신뢰 불능 (b) 대조군 fraud_probability 분포가 실험군과 무구별 → 신호 부재
  (c) memorization_suspect 제외 집계에서 (a)(b) 발생.
- 헤드라인에 정밀도/재현율 % 금지. n=8 신뢰구간(≈±35pp) 명기. 모든 양성 결과는
  잔여 오염 하의 **상한**. D5 단일 실행 한계 문구 의무.

## 부록 A — self-red-team 결과 (2026-07-06 수신, 별도 컨텍스트 서브에이전트)

> **상태: 발견 12건 수신·기록 완료, v1.1 반영은 미수행** — 본 문서는 아직 v1이다.
> 다음 세션: 아래 발견을 반영해 §1~§5 개정 + 헤더를 v1.1로 갱신 후 freeze.
> (헤더의 "v1.1/반영" 표기는 예정 표기였음 — 발견 #12가 지적한 대로 정정 필요.)

수신 원문 (요지 보존, 채점 보조 Claude가 별도 컨텍스트 에이전트로 실행):

1. **HIGH** — §3 필드명 `fraud_probability` 자체가 피평가자 노출 표면에서 fraud 프레이밍 누출 (§1 중립화 규칙 자기모순) → `misstatement_probability`로 개명.
2. **HIGH** — 스키마 v1.2 미착륙 + "개연 시 ≥1"이 기계 강제 불능 → 임계 명시 (예: p≥40이면 hypotheses ≥1 필수)로 스키마에 인코딩.
3. **HIGH** — "as filed to date" 문언이 컷오프 전 정정 완료 케이스에서 미정의 — 완벽 감지가 0점 되는 경로 → 문언에 "contain, or have contained during the covered periods" 또는 차원 1 carve-out.
4. **HIGH** — 차원 1 중간 밴드 겹침 [40,60]: 상수 p 전략이 16케이스 전부 1점 + Brier 0.25 → 판별 통계(분리도/AUC, 상수 0.5 대비 Brier) 병기 + 퇴화 분포는 실패 기준 (b) 발동 명시.
5. **HIGH** — hypotheses 샷건 전략 (무상한 나열로 차원 2·3 보장) → maxItems 3 + 순위 강제 + 최상위만 채점 (또는 불일치 페널티).
6. **HIGH** — §2 입력(구조화 데이터만)과 스키마 evidence(quote="공시 원문 인용", location="각주/페이지") 모순 — 날조 유도 → 이번 사이클 quote/location 의미를 제공 데이터 포인트(개념·기간·값) 참조로 재정의.
7. **MED** — 차원 2 앵커 1↔2↔3 경계 미정의 + 다중 기제 규칙 부재 → 3점 = genre_tags.md pinpoint 사실 ≥1 지목으로 정의, 다중 기제는 최적 일치 채점 + 정답 기제 수 기록.
8. **MED** — 차원 3 매핑 불완전 (정답 pure인데 모델 mixed 등) → 3×3 진실×매핑 행렬 공표 + 최상위 가설에 매핑 적용.
9. **MED** — "대조군 기제 주장은 차원 1에서 감점" 주장은 거짓 (p 낮게 + 기제 크게 = 무벌점 헤지) → 문장 삭제 또는 대조군 기제 주장을 차원 4로 채점.
10. **MED** — "개연 시" 임계 부재로 중간 p + 빈 hypotheses가 차원 2 회피 경로 → p≥40 → ≥1 필수, 실험군에서 부재 시 차원 2 = 0.
11. **MED** — 실패 기준 (b) "무구별"의 검정 부재 → 사전 규칙 (예: rank-sum p 또는 중위 p 분리 최소값) 고정.
12. **LOW** — risk_tier ↔ probability 정합 규칙 부재 (자유 헤지 채널) + 헤더 v1.1 표기 선행 문제 → 정합 규칙 선언 (p≥70 ⇒ elevated 등) + 본 부록 상태 문구로 정정 (완료).
