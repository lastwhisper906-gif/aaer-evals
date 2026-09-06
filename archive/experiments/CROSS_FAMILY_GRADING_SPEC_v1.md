# experiments/CROSS_FAMILY_GRADING_SPEC_v1.md — 차기 사이클 교차 패밀리 채점 프로토콜

> **Valid only if owner-signed before the next cycle's freeze date.**
> Authored by Claude Code, pending human audit (D15). Authority: D106 ⑦
> (GRADER_INDEPENDENCE_v1 — 실행 확약은 D106이 성립; 본 스펙이 그 companion
> 설계다). DESIGN ONLY — 본 문서는 어떤 실행·API 호출도 승인하지 않는다.
> 실행·과금은 전건 별도 소유자 spend gate (D103 선례). 기반:
> `specs/cross_grader.md` (n=20 스팟체크 — 본 스펙은 차기 사이클 전수
> 프로토콜로 확장; §3의 "실행 시점 모델 선정" 조항과의 차이는 §1에 명시).

## 1. DESIGN

- **범위**: 차기 봉인 사이클의 **전 케이스**를 두 채점자가 **독립** 채점:
  - (a) 현직 Claude 계열 채점자 (사이클 freeze에 핀 — 현행 규칙 D6 승계),
  - (b) **지명 비-Anthropic 채점자: `gpt-5.4`** (서명 시점 제공사 최신 안정
    버전 문자열로 핀; 실행 시 전 호출 `response.model` 실측 기록 — D6/SR
    11-7 관행. 서명 전 deprecated 시 폴백 규칙: 동일 제공사 차기 안정
    버전을 소유자가 서명란 비고에 기입).
  - **cross_grader.md §3과의 차이 (정직 기록)**: 스팟체크 스펙은 모델
    지명을 실행 시점 소유자 게이트로 미뤘다. 본 스펙은 F-요건(명명·버전
    핀)에 따라 지금 지명하되, **서명 전까지는 제안**이다 — 소유자는
    서명란에서 지명을 교체할 수 있고, 교체는 본 스펙의 다른 조항을
    무효화하지 않는다.
- 동일 루브릭(동결 앵커 프롬프트 원문 그대로, 재해석 금지) · 동일 블라인드
  입력 · **상호 접근 금지**: 어느 채점자도 상대의 출력·존재를 입력으로
  받지 않는다. 채점 순서 무작위화 불요 (독립 호출).

## 2. BLINDING

- **피평가자 정체 제거**: 채점 자료에서 피평가자 모델 문자열을 전부
  제거한다. 절차 (redaction layer, §6 hook):
  1. 채점 페이로드는 동결 출력 JSON에서 `model`·`pipeline_version`·
     `run_id`·`run_timestamp` 필드를 삭제한 사본으로 생성;
  2. 자유 텍스트 필드에 대해 패턴 스캔 `claude|sonnet|opus|haiku|anthropic`
     (대소문자 무시) → 히트 시 `[MODEL]`로 치환하고 치환 건수 기록;
  3. 케이스 ID는 중립 프레임(case_NN) 유지 (기존 블라인드 규약 승계).
- **카나리 검증**: redaction 후 페이로드 전건에 대해 위 패턴 재스캔 —
  히트 0이어야 실행 가능 (기계 게이트, 실패 시 중단). 추가로 채점자에게
  보내는 프롬프트 자체에도 동일 스캔 적용. 검증 로그는 run log에 포함.

## 3. METRICS (사전 등록 — 계산 전 고정, exact)

- **차원별 Cohen's κ**: dim2(mechanism-match, 3수준 unweighted) ·
  dim4(evidence-groundedness, 밴드, linear weighted). dim1(점수 밴드)은
  기계적 밴딩이므로 κ는 참고 병기.
- **Spearman ρ**: 두 채점자의 케이스 점수(밴드 중점) 순위 상관.
- **방향성 동일-계열 관대(leniency) 검정**: 조작화 — 케이스별
  d_i = (Claude 채점자 점수) − (외부 채점자 점수). **기계 차원(dim1)의
  평균 오프셋 d̄₁을 계기 기준선**으로 두고, 주관 차원(dim2·dim4 환산
  점수)의 평균 오프셋 d̄₂₄가 d̄₁을 **초과**하는지 단측 부호 검정
  (Wilcoxon signed-rank, α=0.05). 초과 = Claude 채점자가 Claude 출력을
  동일 자료에서 평균 오프셋 이상으로 후하게 채점하는 방향의 증거.
  **한계 (사전 기록)**: 비-Claude 피평가자 팔이 없어 완전한 2×2 대비가
  아니다 — 이 검정은 방향성 증거이며, 2×2 확장(외부 모델 피평가자 팔)은
  선택 확장으로 소유자 예산 게이트에 등재만 한다.
- **판독 규칙 (기존 채점 결과의 신뢰 등급 조정 — 사전 고정)**:
  - 양 주관 차원 κ ≥ 0.6 → 기존 human_finalized 결과에
    "cross-family-consistent" 병기 가능 (상향).
  - 0.4 ≤ κ < 0.6 (어느 한 차원) → 해당 차원 주장에 "grader-dependent,
    human-arbitrated" 한정 문구 의무 (유지·한정).
  - κ < 0.4 (어느 한 차원) → 해당 차원의 발행 주장을 기계 차원 기반으로
    재범위화하고 한계 문서에 L-엔트리 (하향). 기존 동결 수치 자체는
    불변 — 바뀌는 것은 주장 표면뿐 (calibration_scope 선례).

## 4. DISAGREEMENT PROTOCOL

- **트리거 (임계 사전 고정)**: dim2 차이 ≥ 2수준, 또는 dim4 밴드 차이
  ≥ 2, 또는 dim1 밴드 차이 ≥ 2.
- 트리거 건은 adjudication log에 등재하고 **소유자가 채점자 정체 블라인드
  상태로** 판정한다 (두 채점을 무작위 순서 A/B로 제시, 어느 쪽이 어느
  모델인지 비공개; 판정 후 개봉).
- **로그 스키마** (`experiments/adjudication_log.jsonl`, 1건 1줄):

```json
{"case_id": "", "dimension": "dim2|dim4|dim1", "grader_A": {"value": "", "rationale_excerpt": ""},
 "grader_B": {"value": "", "rationale_excerpt": ""}, "presentation_order_seed": 0,
 "owner_verdict": "A|B|split|neither", "owner_rationale": "", "verdict_ts": "",
 "unblinded_after_verdict": {"A": "", "B": ""}}
```

## 5. FAILURE MODES (사전 확약)

- **합치 수치는 결과와 무관하게 발행한다** — κ·ρ·leniency 검정 전부.
  "채점자 간 불일치가 커서 채점 지표 자체가 신뢰 불가"라는 결과도 그대로
  발행하며, 그 경우 §3 판독 규칙의 하향 경로가 자동 적용된다. 좋은 결과
  선별(selective reporting) 금지 — freeze-commit-then-run이 본 스펙에도
  적용된다 (이 문서의 서명·커밋이 사전 등록 증거).
- 외부 채점자 호출 실패·정책 거부 등으로 커버리지가 깨지면: 실측 커버리지
  n/N을 그대로 보고하고, N 미달 상태의 κ는 CI와 함께 보고 (은폐 금지).

## 6. HOOKS (목록만 — 구현하지 않는다)

1. 외부 채점자 어댑터 (`pipeline/cli_client.py` 대응물 — 제공사 API,
   소유자 자격 증명·과금).
2. Redaction layer + 카나리 스캔 (§2의 기계 게이트).
3. 합치 계산의 `tools/reproduce_analysis.py` 편입 (κ/ρ/leniency 재계산이
   동결 아티팩트에서 결정론 재현되도록).

## 서명란

CROSS_FAMILY_GRADING_SPEC_v1: PENDING (owner, date: ______, grader pin
confirmed/replaced: ______)

*본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).*
