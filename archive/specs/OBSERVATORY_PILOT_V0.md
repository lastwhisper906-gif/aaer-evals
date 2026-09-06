# OBSERVATORY_PILOT_V0 — cross-sectional model observatory

> **SPECIFICATION ONLY — no call-path code; execution requires owner signature per §8.**
>
> 본 결과는 Claude 기반 단일 파이프라인에 한정된다.
> 채점: Claude 보조 + 인간 최종 확정. 포지션 없음 · 교육·정보 목적 · 투자 조언 아님.

## 1. Question and claim

같은 동결 케이스와 같은 프로브를 훈련 컷오프가 다른 2–3개 모델에 적용할 때,
사건을 훈련 데이터로 알 수 있는 모델의 판단이 알 수 없는 모델보다 체계적으로
달라지는가? 사건일을 가로지르는 `knows / cannot-know` 셀에서만 방향이 맞는
판단 차이가 나타나면, 이는 **MODEL 수준의 memorization dose-response** 증거다.
이는 한 모델 안에서 표면 정보를 교란하는 perturbation 축의 횡단면 보완축이며,
`RESULTS.md` row 4의 name-ID 축과 `docs/methodology_limitations.md` L-5의
잔여 정체 인지 한계를 직접 겨냥한다. 셀이 없거나 방향 기준을 못 넘으면 그
주장을 하지 않는다.

## 2. Target cases and expected knowledge cells

### 2.1 Deterministic case roster

모집단을 임의 표본화하지 않는다. 아래 규칙이 고정 호출 명단이다.

1. `scoring/perturbed_cases.json`의 8건 전부: case_01 SCOR (2016-02-28),
   case_02 OFIX (2013-07-28), case_03 LOGI (2013-08-06), case_06 MON
   (2011-06-28), case_08 HTZ (2014-05-12), case_09 ICON (2015-08-09),
   case_12 KHC (2019-02-20), case_13 MRVL (2015-09-10).
2. `runs/wave2/perturbed/case_*.json`의 basename을
   `data/evaluatee/cases_wave2.json`에 inner-join한 9건 전부: case_39 OSIR
   (2015-11-05), case_40 TNGO (2016-03-06), case_52 CSC (2010-08-10),
   case_59 HAIN (2016-08-14), case_60 MDXG (2016-12-14), case_61 CGI
   (2017-04-04), case_65 WFT (2011-02-28), case_66 UAA (2019-11-02),
   case_67 BRX (2016-02-07).
3. `data/evaluatee/cases_holdout.json`의 3건 전부: case_71 HUBG
   (event 2026-02-05; cutoff 2026-02-04), case_72 WMK (event 2026-02-20;
   cutoff 2026-02-19), case_73 GNE (event 2026-03-12; cutoff 2026-03-11).
   이 세 이름은 레지스트리 `_meta.labels`에 따른 provisional
   restatement/non-reliance 사건의 재진술이며, 회사에 대한 추가 주장이나
   독립적 신뢰 근거가 아니다.

따라서 고정 roster는 wave 17 + holdout 3 = **20 cases**이다. 날짜는 위의
커밋 레지스트리에서 그대로 재계산한다. wave 사건은 모두 2010–2019이고,
holdout 사건은 모두 2026-02/03이다.

### 2.2 Case × documented model-cutoff matrix

`K`는 사건일이 문서화된 훈련 컷오프 이하, `C`는 사건일이 그 뒤임을 뜻한다.
옵션 B/C의 정확한 모델 ID와 vendor 문서 사본 경로는 서명 전 §8 체크박스에서
고정되며, 그 전에는 후보가 아니라 **조건부 roster slot**이다. 문서화된 날짜가
없는 모델은 roster에 들어갈 수 없다.

| case tier (event dates) | A: claude-sonnet-5, cutoff 2026-01 | B: second Claude subscription slot | C: subscription Codex GPT slot |
|---|---:|---:|---:|
| wave-1 8 (2011–2019, §2.1) | K | K if documented cutoff ≥2019-02-20; otherwise per-case date comparison | K if documented cutoff ≥2019-02-20; otherwise per-case date comparison |
| wave-2 9 (2010–2019, §2.1) | K | K if documented cutoff ≥2019-11-02; otherwise per-case date comparison | K if documented cutoff ≥2019-11-02; otherwise per-case date comparison |
| case_71, 2026-02-05 | C | `K iff documented_cutoff >= 2026-02-05` | `K iff documented_cutoff >= 2026-02-05` |
| case_72, 2026-02-20 | C | `K iff documented_cutoff >= 2026-02-20` | `K iff documented_cutoff >= 2026-02-20` |
| case_73, 2026-03-12 | C | `K iff documented_cutoff >= 2026-03-12` | `K iff documented_cutoff >= 2026-03-12` |

A의 날짜 근거는 `docs/HOLDOUT_CRITERIA.md` header와
`docs/FUTURE_HOLDOUT_CANDIDATES.md` header이다. B/C는 서명 시 커밋할 vendor
model card 또는 공식 문서의 URL, 조회일, 그대로의 cutoff 문구를
`docs/FREEZE_REV_OBSERVATORY_DRAFT.md`에 기록해야 한다. 이는 날짜를 추정해
채우는 것을 금지하는 fail-closed 규칙이다.

**Feasibility honesty:** 현재 구조에서 wave는 모든 현실적 후보의 knows-era이고,
holdout은 claude-sonnet-5의 2026-01 cutoff 뒤이며 현재 구독 가능한 다른 후보도
뒤일 가능성이 높다. 따라서 같은 사건에 K와 C가 공존하는 off-diagonal contrast
cell은 오늘 **0일 수 있다**. §5 gate가 이 공백을 실행 전에 판정한다.

## 3. Reused probes, frozen AS-IS

새 프로브를 설계하지 않는다.

- name-ID/recognition과 verbatim probes: `pipeline/probe_runner.py`의
  `RECOG_TASK`, `VERBATIM_TASK`, 각 폐쇄 스키마를 그대로 사용한다. name-ID는
  `scoring/probe_verdict.py:name_match`의 동결 판정만 사용한다.
- outcome recognition: `tools/holdout_probe.py`의 `knows_event` 계기와 스키마를
  그대로 사용한다. admission/판독은 `analysis/HOLDOUT_CONTROLS_PLAN.md` §2의
  gate rule(`knows_event=False`만 admit) 및 반복 draw가 있으면
  `analysis/GATE_K5_PLAN.md`의 ≤1/5 규칙을 바꾸지 않는다.
- perturbation delta: 이미 커밋된 `runs/main/`, `runs/perturbed/`,
  `runs/wave2/scores/`, `runs/wave2/perturbed/` arms와 L-5 판독만 재사용한다.

프롬프트, 스키마, 판정 threshold, 새 arm은 추가하지 않는다.

## 4. Judgment-delta measurement: per-tier matrix

| tier | permitted measurements per model | forbidden |
|---|---|---|
| wave-1 8 | original score `O`, perturbed score `P`, `D=O-P`, name-ID `N∈{0,1}`, verbatim frozen result | 새 perturbation 또는 recognition arm |
| wave-2 9 | original score `O`, perturbed score `P`, `D=O-P`, name-ID `N∈{0,1}`, verbatim frozen result | 새 perturbation 또는 recognition arm |
| holdout 3 | identity-visible PRIMARY score `S`, `knows_event E∈{0,1}` only | perturbed score, name-ID 또는 새 probe arm |

holdout에 perturbed arm이 없는 이유는 `docs/HOLDOUT_CRITERIA.md` (f)에 따라
identity-visible PRIMARY가 의도된 설계이고, post-cutoff 사건 암기는 이미
구조적으로 불가능하기 때문이다.

모델 `m`, `n` 및 두 모델의 상태가 다른 사건들의 집합 `X_mn`에 대해, wave
cross-model contrast는 각 케이스별 `ΔD_i(m,n)=D_im-D_in`과
`ΔN_i(m,n)=N_im-N_in`; holdout contrast는 `ΔS_i(m,n)=S_im-S_in`과
`ΔE_i(m,n)=E_im-E_in`이다. 표의 방향은 항상 **K model minus C model**로
재정렬한다. tier별 요약은 `mean(ΔD)`와 `mean(ΔS)`, 그리고 정수
`sum(ΔN)`, `sum(ΔE)`이며 분모 `|X_mn|`를 함께 쓴다. 빈 집합에는 수치를
계산하지 않고 `EMPTY`로 출력한다. tier 간 pooling은 금지한다.

## 5. Pre-registered go/no-go and effect sizes

### 5.1 Contrast-cell feasibility gate

모든 §6 roster option에 §2.2의 날짜 비교를 먼저 적용한다. 적어도 한 사건에서
동일 사건에 K 모델과 C 모델이 함께 존재하지 않으면 cross-sectional contrast는
**NO-GO**다. 이 경우 소유자는 실행을 포기하거나, 이 pilot을 **LONGITUDINAL
observatory의 baseline leg**로 명시적으로 재서명해야 한다. baseline leg는
holdout의 all-cannot-know `S,E`를 지금 측정하고, 훈련 컷오프가 2026-03을
넘는 미래 모델이 나온 뒤 같은 동결 3건의 contrast를 추가한다. 이는
`specs/POSTCUTOFF_ACCUMULATION.md` §2의 3건/약 5개월, 약 0.6건/월 누적 산술과
같이 시간이 공급을 만든다는 전제다. 측정할 contrast가 없는 상태를 GO로
서명하지 않는다.

### 5.2 GO effect-size rule

off-diagonal `X_mn`이 있을 때만 GO이며, memorization dose-response의 최소
효과는 사전 고정한다.

- holdout: `mean(ΔS) >= 10` score points **and** `sum(ΔE) >= 1`.
  예를 들어 `|X|=1`이면 K−C score가 최소 10이고 E가 0→1이어야 한다;
  `|X|=2`이면 score 차 합이 최소 20이고 E 순증가가 최소 1이어야 한다.
- wave: `abs(mean(ΔD)) >= 10` score points **and** `abs(sum(ΔN)) >= 1`.
  예를 들어 `|X|=2`이면 perturbation-delta 차 합의 절댓값이 최소 20이고
  name-ID 순차가 최소 1이어야 한다. 방향은 관측 전에 특정하지 않되 부호를
  그대로 보고한다.
- 어느 tier도 단독 기준을 넘지 못하면 dose-response claim은 NO-GO다.
  서로 다른 tier의 작은 효과를 합쳐 threshold를 넘길 수 없다.

N은 최대 wave 17, holdout 3이며 off-diagonal은 그보다 작다. 따라서 산출은
per-case evidence와 기술 효과크기뿐이고 p-value, 유의성, 모집단 성능 주장을
하지 않는다. `docs/POWER_ANALYSIS.md`의 가까운 AUC contrast에 대한 낮은 검정력
(wave-1 0.285, wave-2 0.320)은 이 소표본 한계의 관련 근거이지 본 threshold의
검정력 계산이 아니다.

## 6. Candidate roster — unresolved OWNER DECISIONS

아래 항목은 모두 미해결이며 소유자만 선택한다.

### Decision R1 — roster size and vehicles

- **Options:** (A) claude-sonnet-5 + subscription Codex GPT, 2 models;
  (B) claude-sonnet-5 + second Claude subscription CLI, 2 models;
  (C) 세 vehicle 모두, 3 models.
- **Rationale:** claude-sonnet-5는 이미 pinned되어 INV-21 compliant이고 새 pin
  결정이 없다. second Claude는 subscription CLI를 쓰되 INV-21 pin revision과
  FREEZE_REV entry가 필요하다. GPT는 D-P48 예외가 이미 발효했고
  `pipeline/crossmodel_gpt.py`가 존재하지만 live tranche는 D-P49에서 PARKED다.
- **Default:** (A), 단 §5.1 off-diagonal이 없으면 실행 NO-GO 및 R2를 별도 서명.
- **Status:** UNRESOLVED — owner signature required.

Gemini는 subscription path가 없어 제외한다. INV-20상 metered credential 경로는
선택지가 아니다.

### Decision R2 — empty-cell disposition

- **Options:** (A) defer all calls; (B) LONGITUDINAL baseline leg만 실행하고 미래
  cutoff-crossing model을 기다림.
- **Rationale:** 현재 후보로 off-diagonal이 없을 수 있으며, 빈 contrast를
  cross-sectional evidence로 포장할 수 없다. (B)는 §5.1의 all-cannot-know
  기준선을 보존한다.
- **Default:** (A) defer.
- **Status:** UNRESOLVED — owner signature required.

### Decision R3 — invariant revisions

- **Options:** (A) D-P48 범위의 GPT만 허용하고 INV-12/INV-20 무변경;
  (B) second Claude를 위한 INV-21 FREEZE_REV pin revision만 승인.
- **Rationale:** GPT subscription 예외는 이미 유효하다. 다른 vehicle이나
  metered route를 허용하는 INV-12/INV-20 확대는 이 spec의 범위가 아니다.
- **Default:** (A).
- **Status:** UNRESOLVED — owner signature required.

## 7. Exact calls, cost, and time

신규 모델 하나의 완전 leg는 wave 17 × (2 score arms + name-ID 1 + verbatim 1)
= **68 calls**, holdout 3 × (PRIMARY score 1 + knows_event 1) = **6 calls**,
합계 **74 calls/model**이다. incumbent의 커밋 산출물을 재사용하므로 R1(A/B)는
신규 1 model × 74 = **74 new calls**, R1(C)는 신규 2 models × 74 =
**148 new calls**이다. 만약 소유자가 incumbent도 동일 시점에 재실행하도록
별도 승인하면 총량은 2×74=**148** 또는 3×74=**222**이며, 이는 기본안이 아니다.

R2(B) baseline-only는 신규 모델 하나당 holdout 3×2=**6 calls**이다. 모든
vehicle은 subscription pool만 사용하므로 metered API cost는 **$0**이고,
이는 zero-metered framing이지 구독료가 없다는 뜻은 아니다. Wall time은
호출당 1–3분, concurrency 3을 가정해 74-call leg당 **25–75분 ESTIMATE**,
148 calls는 **50–150분 ESTIMATE**다.

## 8. Execution preconditions — owner-signature activation order

이 문서 자체는 어떤 실행도 승인하지 않는다. 아래 순서가 모두 체크된 뒤에만
서명된 option의 정확한 호출 수가 활성화된다.

- [ ] `specs/OBSERVATORY_PILOT_V0.md` §6의 R1, R2, R3 각각에 owner 서명과
  선택 option을 기록한다. 그 D-entry에는 다음 disclosure line을 그대로 넣는다:
  `보호 경로 공개: specs/OBSERVATORY_PILOT_V0.md (.protected-paths) — D-P50 Phase 2 #9 서명 스코프`.
- [ ] `docs/FREEZE_REV_OBSERVATORY_DRAFT.md`를 작성·서명한다: exact model ID,
  vehicle, documented training-cutoff 원문·URL·조회일, CLI version pin,
  served-model fail-closed 규칙, §2.1의 20 case IDs, §3 probe commit hashes.
- [ ] second Claude 선택 시 위 FREEZE_REV에서 `pipeline/cli_client.py`의 pin
  revision을 서명한다. GPT 선택 시 D-P48/D-P49 park 해제와 D-P48 분리경로를
  같은 owner entry에 서명한다. INV-12/INV-20의 추가 개정은 허용하지 않는다.
- [ ] `docs/OWNER_LAUNCH_GATE_OBSERVATORY.md`에 §5.1의 기계 판정(`GO` 또는
  `NO-GO/LONGITUDINAL BASELINE`)과 §7 exact call count를 기입하고 서명한다.
- [ ] 출력 경로를 충돌 없이 고정한다: Claude는
  `runs/observatory/<model_id>/{wave1,wave2,holdout}/`, GPT는 D-P48 패턴의
  `runs/crossmodel_gpt/observatory/<model_id>/{wave1,wave2,holdout}/`.
- [ ] 실행 직전 `./.venv/bin/python tools/verify_blindness.py`를 RC=0으로
  기록하고 metered credential 부재 및 subscription authentication을 확인한다.
- [ ] 서명된 GPT arm만 기존 명령 형태
  `./.venv/bin/python pipeline/crossmodel_gpt.py --cases <signed-registry> --frame <original|perturbed> --out <signed-output-path>`로 실행한다.
  second Claude용 call path는 현재 없으므로 코드 review, tests, FREEZE_REV 선행
  없이 실행할 수 없다. 이 spec은 그 코드를 생성하거나 승인하지 않는다.
- [ ] 완료 후 새 산출물은 manifest/blindness 검증과 인간 최종 채점을 거치며,
  게시 수치는 별도 owner gate 전까지 unpublished로 둔다.

## 9. Relationship to the sealed forward cycle

이 observatory는 커밋된 retrospective frozen cases만 다룬다. INV-22의
`forward/cycle_XXX/` 아래 파일, seal, OWNER_LAUNCH_GATE 또는 2026-11 window를
읽기 입력이나 쓰기 대상으로 삼지 않으며 그 일정과 호출 quota를 변경하지 않는다.
forward cycle과 observatory 산출물은 병합하지 않는다.
