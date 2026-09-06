# ENGINE_DECISION.md — 도구 경로 엔진 판정 사전 등록 (roadmap 1.6, D51)

> **E2(조기성) 실행 전 커밋 — freeze-commit-then-run.** 판정은 E2 산출물로부터
> `analysis/engine_verdict.py`(본 스펙 후행 커밋, 픽스처 테스트)가 **기계적으로**
> 계산한다. 사후 재해석의 여지 0 — 스펙의 규칙이 전부이고, 규칙 밖 서사는
> 판정에 영향을 주지 못한다. 범위 한정(§5-5): Claude 기반 단일 파이프라인.

## 0. 결정 대상

운영 리포(`screener`)의 2단계 퍼널에서 **stage-2(미터링 LLM 딥분석)가 존재할
자격**이 있는가. 근거는 E2 조기성 실측 — "LLM이 결정론 규칙(B3)보다 몇 분기
먼저 신호를 켜는가."

## 1. 입력 (E2 산출물 → trajectories 어댑터)

- E2 동결 계획(`analysis/EARLINESS_PLAN.md`)의 출력 그대로: 케이스별 스냅샷
  궤적 (`case_NN_s{j}`, 케이스당 ≤8 스냅샷, 실험군 = detected fraud,
  대조군 = RP-01 8). **E2 스펙은 무변경** — 본 스펙은 소비자다.
- E2 완료 후 어댑터가 조립하는 `analysis/e2_trajectories.json` 스키마
  (buyer-metrics 빌더와 공유):

```json
{
  "flag_threshold_llm": 50,
  "flag_threshold_b3": 2,
  "cases": [
    {"case_id": "case_NN", "ticker": "XXX", "group": "treatment",
     "snapshots": [
       {"j": 0, "cutoff": "YYYY-MM-DD", "quarters_to_revelation": 1,
        "llm_p": 72, "b3_score": 1}
     ]}
  ]
}
```

- `llm_p` = 해당 스냅샷 미터링 점수 (j=0은 동결 본실행 점수 재사용 — E2 §2).
- `b3_score` = 동결 `b3_compute.b3_score(ticker, snapshot_cutoff, 730)` —
  스냅샷별 재계산 (결정론, 무비용).

## 2. 사전 고정 임계

- **LLM 플래그: p ≥ 50** (동결 FLAG=50, ANALYSIS_PLAN §1 — 재사용, 신규 아님).
- **B3 플래그: score ≥ 2** (신규 사전 등록 — 단일 지표는 NT 1건/정정 1건으로도
  점화되어 이벤트로서 과민; 2 = 연대기 이벤트 동시 발생. 민감도 보고: ≥1, ≥3
  리드타임을 괄호 열로 병기하되 **분기 판정에는 무가중**).

## 3. 리드타임 정의 (기계적)

- 케이스별: `lead = max{ quarters_to_revelation(s) : score(s) ≥ 임계 }`
  (가장 이른 임계 돌파 스냅샷의 t). 돌파 스냅샷 없음 → `lead = 0`.
- 집계: **실험군 케이스별 lead의 중위값** (LLM/B3 각각).
- AUC: **스냅샷 j=0 점수**로 실험군 vs 대조군 tie-aware AUC (동결
  `analysis/stats.py::auc` 의미론) — LLM/B3 각각. j=0 = 운영 스크리닝이 서는
  위치(최신 컷오프).

## 4. 판정 규칙 (순서 고정 · 전역 완전 — 이 순서대로 첫 일치가 판정)

| 순서 | 조건 | 판정 |
|---|---|---|
| 1 | `median_lead_llm ≤ 1` **AND** `median_lead_b3 ≤ 1` | **(c) 도구 경로 종료** — 어느 쪽도 폭로 직전 분기를 넘는 선행 신호 없음. screener 리포 아카이브, aaer-evals는 과학 산출물로 존속. stage-2 없음. |
| 2 | `median_lead_llm ≥ median_lead_b3 + 1` | **(a) LLM 엔진** — stage-2 활성 (top ~300 딥분석). LLM이 규칙 대비 온전한 1분기 이상의 리드로 미터링 비용을 정당화. |
| 3 | 그 외 전부 | **(b) 규칙 엔진** — stage-2 제거, LLM은 리포트 초안 보조로 강등. |

- 브랜치 3에는 두 하위 상황이 있고 verdict JSON에 구분 기록한다 (판정 무영향,
  서사 정직성용): `b_strict` = B3가 리드타임·AUC 모두 ≥ LLM (미션 문면의 (b)) ·
  `b_residual` = LLM 우위가 있으나 1분기 미만 (stage-2는 온전한 1분기 리드를
  벌어야 존재 — 미달 시 무료 규칙이 이긴다는 보수 기본값).
- 동률·경계는 위 부등호가 전부 결정한다 (≤, ≥ 문면 그대로). 중간 판정 없음.

## 5. 실행·기록 규약

- 판정 스크립트: `analysis/engine_verdict.py` — 입력 `e2_trajectories.json`,
  출력 `analysis/engine_verdict.json` (판정 + 전 중간값 + 케이스별 lead 표).
  픽스처 테스트가 세 브랜치 전부를 커버한다.
- E2 완료 → 어댑터로 trajectories 조립 → verdict 실행 → 결과 커밋 → 신규
  D-엔트리로 판정 기록. **판정 후 screener 측 이행(FUNNEL.md §2)은 판정
  JSON을 인용**하며, 사람의 재량 판단이 낄 자리는 브랜치 3의 하위 구분
  서사뿐이다 (판정 자체는 불변).
- 본 판정의 개정은 E2 실행 전에만 가능 (freeze-commit-then-run — 실행 후
  변경은 이력 공개 의무, PROJECT.md §5-6).

## 6. 정직 조항

- (c)가 나오면 그대로 발행한다 — "도구가 안 된다"는 결과도 trust boundary
  데이터다 (PROJECT.md §10). (b)에서 LLM 강등도 동일.
- N(실험군 detected ~7–8)이 작아 중위 리드타임의 신뢰구간은 넓다 — verdict
  JSON에 케이스별 lead 전수 표를 동반해 독자가 재계산 가능하게 한다 (§2-4
  검증가능성).

## §4b B4 결합 조항 이행 (개정 1 — D58, 2026-07-13, E2 실행 전)

> specs/B4_short_interest.md §7(D55, 완화 금지 조항)이 등록한 결합을 본 판정
> 규칙에 기계적으로 이행한다. **E2 실행 전 개정** — §5 개정 조건 충족.
> 판정 코드(engine_verdict.py §4b 지원)는 이 개정 커밋에 후행한다.

- **입력 확장**: trajectories 스냅샷에 선택적 `b4_slope_aug` (float|None) —
  동결 `b4_score(ticker, snapshot_cutoff)`의 `score_slope_aug` (결정론, 무비용).
  부재/전건 None 허용 (커버리지 판정으로 귀결).
- **B4 플래그 임계 (기존 사전 등록 재사용, 신설 아님)**: `b4_slope_aug > 0` —
  screener FUNNEL §1 rank key·프로토콜 §2와 동일 임계.
- **비교 성립 조건 (B4 스펙 §7 문면 그대로)**: (i) 실험군 B4 커버리지 ≥ 70%
  (케이스가 커버 = ≥1 스냅샷에서 b4_slope_aug 비-None) AND (ii) 동일 산식의
  LLM 성능이 같은 데이터에 존재 (E2 궤적 자체가 이를 공급).
- **결합 규칙 (순서: §4 기본 판정 후 적용, 전역 완전)**:
  - 비교 불성립 → 기본 판정 그대로, verdict JSON에 `b4_comparison.valid=false`
    + 사유 기록.
  - 비교 성립 AND `median_lead_llm ≤ median_lead_b4` AND `auc_llm ≤ auc_b4`
    (둘 다, 경계 포함 — "성능 ≤"의 기계 번역) → **LLM ≤ B4 = E2 평결과 동일
    가중치**: 기본 판정이 (a)였다면 **(b) 규칙 엔진으로 강등**
    (`b_subcase="b4_dominated"`), (b)/(c)는 불변 (이미 stage-2 없음).
  - 비교 성립 AND LLM이 어느 한 축에서라도 우위 → 기본 판정 그대로,
    비교 전량 기록.
- **정직 조항**: B4 리드타임·AUC는 커버 케이스 부분집합에서 계산 — LLM 값도
  **같은 부분집합으로 재계산해 짝지어 비교**한다 (커버리지 편향 차단). 전체
  실험군 LLM 값과의 차이는 verdict JSON에 병기.

## §3 주석 — j=0 llm_p의 대조군 가용성 (D71, 2026-07-13, 어댑터·판정 출력 존재 전 커밋)

- **실측 사실**: E2 대조군(EARLINESS_PLAN §4 = RP-01 확정 v1 대조군)의 동결
  draw-1 점수는 **원본 프레임(runs/main)에만 존재**한다 — perturbed 프레임
  j=0 채점은 v1에서 실험군 8건만 수행되었다. E2 스냅샷(양 군)은 perturbed
  프레임이므로, 대조군 j=0에 원본 점수를 넣으면 프레임 혼합(정체 가시 vs
  익명)이 되어 j=0 AUC의 편향 방향을 서명할 수 없다.
- **규약 (fail-closed, 재량 0)**: 어댑터는 대조군 j=0에 `llm_p: null`을
  기록한다 (b3_score·b4_slope_aug는 결정론 재계산이라 정상 기록). 판정기는
  j=0 지표별로 null 케이스를 제외하고, **어느 그룹이든 0이 되면 해당 AUC =
  null + 플래그**를 기록한다. §4 하위 라벨(b_strict/b_residual)이 AUC를
  요구하는데 null이면 `b_auc_unavailable`로 기록한다 (하위 라벨은 판정
  무영향 — §4 본문 그대로).
- **판정 불변 확인**: §4 브랜치 규칙은 실험군 median lead(LLM·B3)만 소비 —
  본 주석은 브랜치 결정에 어떤 입력도 바꾸지 않는다. b3 j=0 AUC는 양 군
  계산 가능(결정론)이라 영향 없음.
- **해소 경로 (소유자 게이트)**: v1 대조군 7건(E2 buildable)의 perturbed
  j=0 채점(7호출)이면 LLM j=0 AUC가 계산 가능해진다 — OWNER_QUEUE Q-M06
  등록, 본 주석은 그 실행 여부와 무관하게 유효.
- **타이밍 증거**: 본 주석 커밋 시점에 analysis/e2_trajectories.json ·
  engine_verdict.json 부재 (E2 호출 진행 중, 후처리 미실행) — 판정 산출물을
  보기 전의 규약임을 저장소 상태로 증명한다.

---

## v2 — FPR-matched comparison + control expansion (owner-signed 2026-08-06, D-P83; BN-10/Q-F12; English canonical per D114)

> Registered from `docs/ENGINE_DECISION_V2_OWNER_PACKET.md` under the owner's
> 2026-08-06 blanket signature (verbatim in D-P83). v1 sections above are
> preserved unchanged (INV-06 append-only spirit; E-001 parallel-path
> precedent). **v2 rules apply to forward (Cycle-2 sealed) predictions
> only** — see §C. Registration precedes Cycle-2 registration, satisfying
> the BN-10 resolution condition.

### §A. FPR-matched readout rules (owner option: (A) exact matching)

1. For every compared channel (LLM · B3 · B4), a **pre-registered threshold
   grid** is frozen by commit before Cycle-2 seal. No post-hoc grid
   additions.
2. Any lead-time or detection-rate comparison claim is valid **only at
   threshold pairs whose control-flag counts match exactly**. If no exact
   match exists, the comparison is recorded as "comparison not established"
   and the claim is omitted — fail-closed, isomorphic to §4b's
   comparison-validity condition.
3. Every cell carries its Clopper–Pearson 95% interval (DECISION_TABLE
   convention). Continuous-curve (ROC) claims remain prohibited.
4. Readout is computed mechanically by the v2 successor of
   `analysis/engine_verdict.py`; narrative outside the rules cannot affect
   the verdict (v1 §0 principle inherited).

Basis: the recorded E2 asymmetric-readout artifact — LLM flags were read at
a threshold carrying 71.4% (5/7) control false positives while the B3 gate
was read at 0/7 (packet §0; DIRECTION_CONTEXT "why FPR-matching is
non-negotiable").

### §B. Control-expansion selection protocol (owner option: size (B) n≈30)

1. Expanded controls follow the identical protocol (INV-04) and identical
   PIT discipline (INV-01) as existing controls; the selection rule inherits
   the `analysis/HOLDOUT_CONTROLS_PLAN.md` matching conventions, with any
   necessary deviation pre-stated in this section before use.
2. The selected roster (ticker list) is committed **standalone, before
   Cycle-2 seal and before any new grading** — freeze-commit-then-run.
3. Any new data fetch happens only in an owner-attended supervised session
   (INV-23).
4. **Target size: n≈30** (owner-signed under the 2026-08-06 delegation).
   Deterministic arithmetic recorded at signing: 0/30 → CP95 upper ≈11.6%
   (vs 0/7 → 41.0% today; 0/20 → ~16.8%; 0/50 → ~7.1%). n≈30 is the
   cost/precision knee: it brings a zero-FP result's upper bound below every
   measured FPR in RESULTS rows 8–10 while keeping procurement and
   matching-quality burden bounded. This signs the target size only —
   procurement, fetch sessions, and any metered grading remain separately
   gated (INV-22/INV-23, OWNER_LAUNCH_GATE).

### §C. Post-E2 history disclosure (owner option: (A) embedded; PROJECT.md §5-6)

1. **What was seen before v2 was drafted**: the E2 verdict artifacts,
   DECISION_TABLE (including the 71.4% asymmetry observation),
   buyer-metrics, and the [EXPLORATORY] combined-rule candidate (already
   disclosed as post-hoc in the published table).
2. **Binding scope**: v2 rules apply to forward (Cycle-2 sealed)
   predictions only. Retroactive readouts of v1/E2 frozen data under v2
   rules are not citable as performance claims (same discipline as
   DECISION_TABLE §5's warning text).
3. **v1 history preservation**: the v1 verdict rules and existing
   amendments (§4b, §3 annotation) above are preserved unmodified; v2 is
   registered as an additive section only.

> Scope limitation: results and plans are specific to a single Claude-based
> pipeline (PROJECT.md §5-5). Grading: Claude-assisted, human-finalized.
