# AAER Evals — 이해상충 없는 회계 품질 신호의 백테스트

> Authored by Claude Code, pending human audit (GA-001 (b), D15).
> 본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).
> **These controls BOUND memorization risk; they do not eliminate it.**

## 무엇인가

상장사 회계 품질에 대한 독립 신호는 구조적 공백이다: 감사인은 피감사인이
보수를 지급하고, 셀사이드는 거래 관계가 있으며, 신용평가사는 발행사가
수수료를 낸다. 이 저장소는 그 공백을 겨냥한 장치 — **LLM이 point-in-time
구조화 공시 데이터만으로 왜곡표시 위험을 스크리닝할 수 있는가** — 를 SEC
집행(AAER) 확정 사건 8건 + 매칭 비집행 대조군 8건으로 백테스트한 기록이다.
포지션 없음 · 교육·정보 목적 · 투자 조언 아님.

## 헤드라인 (교란 입력 우선 — 이 순서 그대로 읽을 것)

**익명화·재스케일된(교란) 실험군 입력 기준, 피평가자(claude-sonnet-5)의
판별력은 AUC 0.797 / one-sided rank-sum p=0.0226 / 중위값 분리 19.0pp였다 —
단, 같은 교란 입력에서 인지 프로브가 8사 중 6사의 실명을 지목(D7
CONTAMINATED)했고 재추첨에서도 5/8이 유지됐으므로(합집합 6/8), 교란은 암기된
수치를 흩뜨릴 뿐 **정체 인지를 제거하지 못하며** 모든 양성 결과는 잔여 오염
하의 상한이다** (RP-05 §1 · RP-06 A1, L-5).

- **표본 불확실성 (k=5 재추첨, RP-06 A3)**: p 0.0009–0.0226 / AUC 0.797–0.938 /
  중위 분리 9.0–26.5pp. 사전 등록 draw가 5회 중 최약 draw였다 — p·AUC는
  재추첨에 강건, **분리<10pp 실패 항목은 5회 중 1회 발동** (주장 강도는 이
  서열을 따른다). 케이스별 중위값 기준: p=0.0012 / AUC 0.922 / 분리 21.0pp.
- 원본(비교란) 입력 수치(AUC 0.844, p=0.0094)는 암기 기여 포함 상한으로
  부록에만 둔다 (RP-05 §1).
- 대조 기준선: 동일 케이스에서 Beneish M 0.571 / Dechow F 0.542 / Montier C
  0.571 / |Sloan| 0.589 — 정량 스크린은 이 표본에서 우연 수준.
- 채점: Claude 보조 + 인간 최종 확정 — 채점 26건은 현재 human_finalized=False
  (소유자 확정 대기: `review_packets/RP-06_grading_workbench.md`).

## 거버넌스 지도 (읽는 순서)

1. `PROJECT.md` — 단일 기준 문서 (방법론 규율 §5, 협업 모델 §7, 스코프 가드 §8)
2. `CLAUDE.md` — 세션 가드레일 (자동 로드 압축본)
3. `scoring/decisions_log.md` — 소유자 결정 대장 D1~D18 + freeze `82a7717` +
   개정·지시문 verbatim (지시문 원문이 감사 추적의 일부)
4. `GATE_PACKAGE.md` · `logs/run_log.md` — 실행 게이트와 판정표
5. `review_packets/INDEX.md` — 사후 감사 진입점 (재량 판단 J1~J23 전수 색인)

## 수치 재현 (제3자 검증)

```bash
pip install -r requirements.txt
python tools/reproduce_analysis.py   # RP-05 §1~§5 + RP-06 A3 발행 수치 전건 재계산 → PASS/FAIL
python tools/verify_blindness.py     # 채점 선행 이력 증명 · 실명/카나리 스캔 · runs/ sha256
```

둘 다 커밋 산출물만 사용한다 (API 호출 0, 원문 코퍼스 불요) — CI가 매 push
검증한다. 원시 데이터: `runs/` (sha256 매니페스트 포함) · `scoring/grades/` ·
`scoring/probe_results/` · `logs/run_*/` (호출별 서빙 모델·격리 플래그·freeze
해시).

## 한계 (전문: docs/methodology_limitations.md)

L-1 모델 내부 지식은 차단 불가 — 측정·공개만 가능. L-2 실행층은 Claude Code
하네스 v2.1.201 매개 (원시 API 아님). L-3 샘플링 파라미터 고정 불능 — 케이스
판정은 비결정론 표본의 점추정 (k=5로 정량화, 위 밴드). L-4 격리는 실행별
게이트로 검증. **L-5 교란은 수치 암기를 흩뜨릴 뿐 정체 인지를 제거하지
못한다** ("perturbation disrupts memorized NUMBERS, not IDENTITY
recognition"). 선택·생존 편향: 실험군은 "적발까지 간 사건"의 생존 표본이고
대조군 라벨은 "무결"이 아니라 "비집행"이다.

## 이것이 아닌 것

n=16(실험 8 + 대조 8)의 존재 증명 시도이지 성능 추정치가 아니다. 단일 분석자
(+AI)의 산출물이며 외부 재현·감사 전이다. 피평가자는 하네스 매개 호출이라
원시 API 재현과 다를 수 있다. 케이스 판정은 비결정론 표본이다 (케이스별
σ 2.1~13.2pp — RP-06 §3-2). 정밀도/재현율 % 헤드라인은 의도적으로 없다
(n=8 신뢰구간 ≈±35pp). 특정 기업에 대한 주장이 아니며 — 현재 기업 산출물에는
"분식/fraud/조작" 서술을 쓰지 않는다 (§6) — 투자 조언은 더더욱 아니다.
