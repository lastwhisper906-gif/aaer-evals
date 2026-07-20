# 실무자 브리프 — LLM 회계품질 스크린, SEC 집행 대비 백테스트

> **DRAFT — atlas/PATTERNS.md·CPA 판단 절의 소유자 확정 전. 외부 배포 금지.**
> (원문 유지: **DRAFT — pending owner finalization of atlas/PATTERNS.md and
> CPA judgment sections. Not for external distribution.**)
>
> Authored by Claude Code, pending human audit (D15). 포지션 없음 ·
> 교육·정보 목적 · 투자 조언 아님. 본 결과는 Claude 기반 단일 파이프라인에
> 한정된다 (PROJECT.md §5-5) — results are scoped to a single Claude-based
> pipeline and do not generalize to LLMs at large.
> 채점: Claude 보조 + 인간 최종 확정 (grading: Claude-assisted, human-finalized).
>
> 대상 독자: 포렌식 회계사, 내부감사인, 바이사이드 애널리스트.
> 이 브리프의 모든 수치는 동결된 저장소 산출물(부록)로 추적되며
> `tools/reproduce_analysis.py`가 재계산한다. 새 수치는 여기에 등장하지 않는다.

---

## 1면 — 문제

상장사 회계 품질에 대한 독립 신호는 구조적으로 희소하다. 감사인은 피감사인이
선임하고 보수를 지급한다. 셀사이드 커버리지는 커버 대상 발행사와 현재 또는
장래의 인수 관계가 있는 은행 안에 있다. 신용평가사는 발행사가 수수료를 낸다.
이들 각각이 재무제표 신뢰성에 대한 의견을 생산하지만, 각각이 그 재무제표를
판정받는 회사와 경제적 관계를 맺고 있다. 정정 공시 이후가 아니라 이전에,
이해상충 없는 회계 품질 2차 의견을 원하는 실무자에게 쓸 수 있는 도구는 많지
않다.

기존의 이해상충 없는 도구는 기계적 스크린 — Beneish M-score, Dechow F-score와
그 후속들 — 이다. 값싸고 재현 가능하지만, 대규모로 돌려 본 사람이라면 누구나
아는 실패 양상이 문서화되어 있다: 특정한 재무제표 입력 집합을 요구하므로
발행사의 공시나 태깅이 이를 제공하지 않으면 아예 계산이 불가능하고, 정적
공식이라 작정한 작성자가 공식에 맞춰 관리할 수 있으며, 공식 안의 비율만 읽을
뿐 그 주변의 제출 행태·공시 연대기·계정 수준 결을 읽지 못한다. 이 저장소는
그 도구 상자에 추가할 후보 하나 — 동결 프로토콜 아래에서 point-in-time 구조화
공시 데이터를 읽는 LLM — 를 SEC 집행(AAER) 사건, 매칭된 비집행 대조군, 그리고
훈련 컷오프-후 홀드아웃에 대해 백테스트한다.

## 2면 — 시스템

```
  SEC 공시 (point-in-time,           결정론적 Python 지표
  컷오프 가드: 각 케이스의       -->  (비율·추세·연대기;
  컷오프일 이후 문서 차단)           시드 고정, 벽시계 로직 없음)
              |                                   |
              v                                   v
  LLM 증거 추출: 동결 체크리스트 프롬프트, 구조화 JSON 스키마,
  원천 수치·accession 번호의 원문 인용 의무 (documents_used 필수)
              |
              v
  구조화 채점 루브릭 (점수 존재 전 동결)
  채점자 모델이 적용  -->  인간 CPA 최종 서명
                           (발행 채점 전건 human_finalized=true)
```

**Point-in-time 공시.** 모든 케이스에는 컷오프일(최초 공개 폭로 전일)이 있다.
모든 데이터 로딩은 컷오프 가드(`pipeline/cutoff_guard.py`)를 경유하며, 컷오프
이후 제출된 문서는 입력에 들어오지 않는다. 이는 문서를 통한 look-ahead를
차단한다 — 모델이 내부적으로 이미 아는 것까지는 차단하지 못하며, 그것이 3면의
오염 프로그램이 존재하는 이유다.

**결정론적 지표.** 모든 정량 계산은 시드 고정된 결정론적 Python이다 — 의미
있는 산술을 LLM이 하는 일은 없다. Beneish M과 Dechow F는 동일 입력으로 기계
베이스라인으로서 계산된다.

**LLM 증거 추출.** 피평가자 모델(핀 고정 `claude-sonnet-5`)은 덱에 대해 동결
체크리스트에 답하며 원문 수치와 사용 문서의 accession 번호를 반드시 인용해야
한다. 출력은 스키마 검증된 JSON이며, 열린 질문 프롬프트는 금지된다. 출력은
0–100 서수 점수와 증거 인용이 달린 순위형 가설들이다.

**구조화 루브릭, 그리고 인간 서명.** 채점자 모델이 동결 루브릭을 적용하고,
발행되는 모든 채점은 소유자 서명 아래 `human_finalized=true`를 단다(기록된
오버라이드 0건, 고무도장 점검 확인). 이 저장소의 어떤 것도 모델 권위만으로
발행되지 않는다.

## 3면 — 증거 규율 (무엇이 이것을 반증하는가)

이 설계는 독자의 첫 번째 반론 — *모델이 훈련 중에 이 사건들을 읽었다* — 을
전제한다. 아래 통제들은 그 위험의 경계를 정할 뿐 제거하지 못하며, 저장소는 그
사실을 첫 페이지에 명시한다.

**실행 전 동결.** 채점 기준, 임계값, 기계 결론 규칙(R1–R4 / H1–H3)은 어떤
점수도 존재하기 전에 커밋되었다 — 사전 등록은 git 커밋 타임스탬프로 증빙된다
(실험 계획, 커밋 `c1b85a7`). 사후 규칙 변경이 필요한 결과였다면 git 이력에
드러났을 것이며, 그런 변경은 없었다.

**오염은 가정으로 치우지 않고 측정한다.** 직접 outcome-knowledge 프로브에서
모델은 **wave-2 실험군 9케이스 중 8건(88.9%, CP95 [51.7%, 99.7%])의 집행/정정
사건을 상기하며, 대조군은 0/23**이다 — 있는 그대로 말하면, wave-2 정체-노출
프레임은 사건 지식이 광범위하게 가용한 상태로 작동했고, 모든 TASK 1 결과는
공개된 잔여 오염(L-1/L-5) 하의 판독이다. 이름 식별 프로브에서 익명화 페이로드
식별은 **wave-1에서 50%**, **wave-2에서 21.9%**다. 발행 후 고지는 추가로 v1
교란 프레임이 **부분 탈익명화**에 그쳤음(원본 accession 번호와 실제 제출
연대기 유지)을 공개한다.

**블라인드 채점, 컷오프-후 홀드아웃.** 실험군과 대조군은 하나의 프로토콜로
실행되며, 암기에 대한 구조적 답은 TASK 2 — 정정 사건이 모델 훈련 컷오프
이후에 발생한 3개 회사 — 다. 사전 커밋된 인지 게이트는 5회 프로브 draw에 걸쳐
**케이스당 knows_event 0/5**를 읽는다(양성대조 HTZ 재검증 True) — 이 사건들에
대해서는 암기가 단지 개연성이 낮은 것이 아니라 구조적으로 불가능하다.

**봉인, 전향.** 다음 단계는 전향적이다: 12개 회사 forward watchlist를
**2026-11-15**에 채점하고 암호학적으로 봉인할 예정이다(GitHub 서버 타임스탬프
+ OpenTimestamps 앵커) — 암기할 결과가 존재하기 전에
(`specs/FORWARD_WATCHLIST_V1.md`).

**원커맨드 재현.** `python tools/reproduce_analysis.py`가 커밋된 산출물에서
발행 수치 전건을 재계산한다, API 호출 0 — **100/100 체크** —
`tools/verify_blindness.py`·`tools/verify_manifest.py`와 함께. CI가 매 push마다
전부 실행한다. 이 브리프의 어떤 수치든 불신하는 독자는 몇 분 안에 직접
재계산할 수 있다.

## 4면 — 무엇을 찾았는가

가장 강한 결과 3건, 각각 태스크 층위와 동결 구간 병기:

- **[TASK 1] Wave-1, 교란(정체-가림) 프레임** (AAER 실험군 8 vs 대조군 22):
  분리 순열 p = **0.0021**, AUC **0.864 [0.722, 0.969]**, 사전 등록 점수 ≥50
  컷에서 실험군 4/8 플래그. 단서 L-5: 교란은 암기된 수치를 흩뜨릴 뿐 정체
  인지를 제거하지 못한다 — 이것은 *덜 오염된* 프레임이지 깨끗한 하한이
  아니다. (정체-노출 원본 프레임은 p = 0.00114로, 암기-얽힘 상한선이다.)
- **[TASK 1] Wave-2, 덜 유명한 사건** (실험군 9 vs 대조군 23): standalone 순열
  p = **0.00116**, AUC **0.829 [0.616, 0.983]**, 7/9 플래그. 암기 규칙 R3는
  비발동(정체-vs-교란 dominance 3/9)이므로 사전 커밋된 판독은 R4 — 잔여
  능력이며, 벤치마크 정확도 비교 주장은 일절 불허.
- **[TASK 2] 컷오프-후 홀드아웃, per-case (N=3, 유의성 미주장)**: **HUBG 점수
  70** — 플래그, 5/5 독립 재추첨에서 점수 ≥50(밴드 58–76), 매칭 대조군 3사
  전부를 상회(RXO 42 · BCO 30 · XPO 20). WMK 32와 GNE 42는 플래그되지 않았고
  각자 대조군과의 분리도 없다; 정확 순열 p = 0.20은 맥락 참고 전용이다(N=3
  과소검정력 사전 선언 — 이것은 per-case 증거이지 통계적 주장이 아니다).
  홀드아웃 티어의 단일 최고점은 대조군 오탐이다(GridAI, GRDX, 점수 78).
  HUBG·WMK·GNE는 **잠정 Item 4.02 비신뢰 정정 라벨 — 확정 사기가 아니며 집행
  결과도 아니다.**

**[TASK 1] 동일 30사에 대한 기계 베이스라인**: Beneish M p = 0.498 / AUC
0.510, Dechow F p = 0.268 / AUC 0.573 — 이 표본에서 무분리; LLM 순위는 둘과
사실상 무상관이다. LLM 신호는 공식의 재구현이 아니다.

**오탐 해부** (`atlas/PATTERNS.md` §d — 티어별 오탐 플래그율, Clopper–Pearson
95% 구간 병기, 절대 합산 금지: [TASK 1] wave-1 FPR 3/22 = 13.6% [2.9%, 34.9%]
· [TASK 1] wave-2 FPR 5/23 = 21.7% [7.5%, 43.7%] · [TASK 2] 홀드아웃 매칭
대조군 2/9 = 22.2% [2.8%, 60.0%]). 오탐은 환각이 아니다 — 모든 FP 엔트리의
모든 인용 수치가 봉인된 사실과 대조 검증된다. 이는 **실재 수치의
과잉해석**이며, 리뷰어가 예상할 수 있는 반복 형태를 띤다:

- *곤경(distress)을 왜곡표시로 읽음*: 공개 공시된 영업권 손상을 이전
  장부가액이 허위였다는 증거로 받아들임(atlas case_30, 점수 65).
- *태그 재매핑·커버리지 아티팩트를 이상 징후로 읽음*: XBRL 개념 재매핑을
  "내부 비일관" 시계열로 제시(case_44); 현금흐름 태그 2개 간 부호
  불일치(case_49); 부채 재분류를 설명 없는 급증으로 채점(case_07).
- *수정 제출 연대기를 정정으로 승격*: 10-K/A·코멘트 레터 메타데이터를 결정적
  검정 — 제출본 간에 값이 실제로 바뀌었는가? — 없이 정정 증거로 읽음. 봉인된
  답은 매 건 '아니오'(case_10, 점수 58; case_48; hc_07).

**정직한 사용 경계.** 이것은 전문가 검토를 위한 가설 생성·트리아지 도구다 —
자동 의사결정 시스템이 아니고, 확률 엔진이 아니며, 독립 경보 피드가 아니다.
0–100 출력은 **비보정 서수 `misstatement_risk_score`**다(wave-2 ECE 0.179,
wave-1 0.209 — 확률 판독은 명시적으로 기각된다). `specs/RISK_SCORE_SEMANTICS.md`
원문: *"A score of 70 means stronger model-assessed risk than a score of 40
under the same frozen protocol. It does not mean a 70% probability of
misstatement."* (풀이: 같은 동결 프로토콜 아래에서 점수 70은 점수 40보다 강한
모델 평가 위험을 뜻한다. 왜곡표시의 70% 확률을 뜻하는 것이 아니다.) 임계값별
트레이드오프는 구간과 함께 `analysis/DECISION_TABLE.md`에 있다 — 그 문서의
헤드라인 자체가, E2 궤적 레이어에서는 어떤 단일 임계 LLM 전략도 지배하지
않는다는 것이다.

**입력 결측 케이스, 양면 모두.** [TASK 2] HUBG에 대해 기계 스크린은 계산조차
되지 않았다 — Beneish M과 Dechow F 모두 입력 결측으로 실패 — 그러나 LLM은
제출 연대기와 계정 추세로부터 이를 플래그했다(점수 70). 그리고 그 플래그는
**티어 적중이되 기제 빗나감**이다: 모델은 가설을 HUBG의 2018 정정 클러스터에
정박시켰지, 2026 비신뢰가 실제로 다루는 미기록 부채 기제에 두지 않았다
(`atlas/case_71.md`). 입력 공백을 견디는 리스크 스크리닝으로 읽어라 — 포렌식
기제 식별로 읽지 말라.

## 5면 — 판단의 분업

누가 무엇을 하며, 왜인가 (전체 표: `CONTRIBUTIONS.md`):

- **결정론적 코드**: 컷오프 집행, 모든 정량 지표, 기계 베이스라인 공식, 순열
  검정, 봉인 도구. 근거: 정확히 재현 가능해야 하고 서사적 표류에 면역이어야
  하는 것은 전부 코드이며, 시드 고정되고, CI로 검증된다.
- **모델**: 증거 추출과 가설 순위화만 — 원문 수치와 accession 번호 인용 강제,
  스키마 제약, 열린 질문 프롬프트 금지. 근거: 모델의 비교우위는 읽기 폭이며,
  알려진 실패 양상(실재 수치의 과잉해석, 4면)은 모든 주장을 인용
  대조-검증 가능하게 만들어 경계를 정한다.
- **인간**: 판단인 것은 전부. 연구 설계·임계값·결론 규칙은 어떤 점수도 있기
  전에 소유자가 선택하고 사전 등록했다; 발행되는 모든 채점은 인간 최종 서명을
  단다; atlas의 회계 판단은 소유자 감사 전까지 초안이다. 여기서 AI 산출물은
  소유자 서명 전까지 미감사 작업물이며 — 발행된 모든 주장의 최종 책임은
  소유자가 진다.

**이 전부를 규율하는 약속**: 봉인된 전향 사이클. 어떤 점수도 존재하기 전에
사전 동결 규칙으로 열거된 12개 회사를, 사전 등록된 정지 규칙(≥11/12 채점,
미달 시 사이클 중단·현상 보존), 무과금(zero-metered) 실행, 외부 검증 가능한
타임스탬프, 사전 등록된 검토 지평 아래 **2026-11-15**에 채점·봉인한다.
프로토콜은 `specs/FORWARD_WATCHLIST_V1.md`에서, 동결 유니버스는
`forward/cycle_001/`에서 검증하라. 그 사이클들이 성숙하기 전까지 이 저장소가
주장하는 것은 회고적 분리(TASK 1)와 per-case 증거(TASK 2)다 — 그 이상은 없다.

---

## 부록 — 수치-원천 지도

위의 모든 수치, 그 동결 원천, 검증 경로. 별도 표기 없는 한 모든 행은 `python
tools/reproduce_analysis.py`(100/100)로 재계산된다.

| 브리프의 수치 | 동결 원천 (검증 경로) |
|---|---|
| [TASK 1] wave-1 교란 순열 p = 0.0021 | `analysis/results_stats.json` → `secondary.perm_p_one_sided` (0.00207, 발행 반올림 0.0021) |
| [TASK 1] wave-1 교란 AUC 0.864 [0.722, 0.969] | `analysis/results_stats.json` → `secondary.auc`, `secondary.auc_boot95` |
| [TASK 1] wave-1 교란 플래그 4/8 (≥50) | `analysis/results_stats.json` → `secondary.fisher_2x2.tp`; `analysis/decision_table.json` → `layers.L1_wave1_perturbed` T=50 |
| [TASK 1] wave-1 정체-노출 p = 0.00114 | `analysis/results_stats.json` → `primary.perm_p_one_sided` |
| [TASK 1] wave-2 standalone p = 0.00116 | `analysis/wave2_results.json` → `original.perm_p` |
| [TASK 1] wave-2 AUC 0.829 [0.616, 0.983] | `analysis/wave2_results.json` → `original.auc`, `original.auc_ci` |
| [TASK 1] wave-2 플래그 7/9 | `analysis/wave2_results.json` → `flags.fraud` |
| [TASK 1] wave-2 outcome-recognition 8/9 = 88.9%, CP [51.7%, 99.7%]; 대조군 0/23 | `analysis/outcome_recognition_results.json` → `rates.treatment`, `rates.control` |
| [TASK 1] wave-1 name-ID 50% | `analysis/name_probe_results.json` → `rate_pct` |
| [TASK 1] wave-2 name-ID 21.9% (동결 name_match 규칙) | `analysis/synthesis.json` → `memorization_dose_response[wave2].name_id_pct` |
| [TASK 1] wave-2 정체-vs-교란 dominance 3/9 (R4) | `analysis/wave2_results.json` → `R3_memorization` |
| [TASK 2] 홀드아웃 knows_event 케이스당 0/5 (HUBG·WMK·GNE); 양성대조 HTZ True | `analysis/gate_k5_results.json` → `cases.*.band_true_of_5`, `positive_control_HTZ_knows_event`; 트랜스크립트 `runs/holdout/recognition_k5/` |
| [TASK 2] HUBG 점수 70 (플래그) | `runs/holdout/scores/case_71.json` (레거시 필드명 `misstatement_probability` — `specs/RISK_SCORE_SEMANTICS.md` §3에 따라 서수) |
| [TASK 2] HUBG 5/5 재추첨 ≥50, 밴드 58–76 | `analysis/holdout_redraw_results.json` → `per_case.HUBG` |
| [TASK 2] HUBG가 매칭 대조군 RXO 42 · BCO 30 · XPO 20 상회 | `analysis/holdout_controls_results.json` → `per_case_side_by_side.HUBG` |
| [TASK 2] WMK 32 · GNE 42 (비플래그) | `analysis/holdout_redraw_results.json` → `per_case.WMK`, `per_case.GNE` |
| [TASK 2] 홀드아웃 정확 순열 p = 0.20 (맥락 전용) | `analysis/holdout_controls_results.json` → `exact_perm_p_CONTEXT_ONLY` (0.2045) |
| [TASK 2] E1 대조군 플래그 2/9 = 22.2%, CP [2.8%, 60.0%] | `analysis/holdout_controls_results.json` → `control_fpr` |
| [TASK 2] GRDX 대조군 오탐, 점수 78 (홀드아웃 티어 최고점) | `analysis/holdout_controls_results.json` → `per_case_side_by_side.GNE.matched_controls.GRDX`; `atlas/hc_03.md` |
| [TASK 1] wave-1 FPR 3/22 = 13.6%, CP [2.9%, 34.9%] | `analysis/results_stats.json` → `primary.fpr` |
| [TASK 1] wave-2 FPR 5/23 = 21.7%, CP [7.5%, 43.7%] | `analysis/wave2_results.json` → `flags`; `analysis/decision_table.json` → `layers.L2_wave2` T=50 `fpr_ci95` |
| [TASK 1] Beneish M p = 0.498 / AUC 0.510 · Dechow F p = 0.268 / AUC 0.573 | `analysis/results_stats.json` → `baselines.beneish_m`, `baselines.dechow_f` |
| [TASK 2] HUBG Beneish M / Dechow F 계산 불능 (입력 결측) | `analysis/holdout_summary.md` §2 표 (계산불능/결측 행) |
| ECE wave-2 0.179 · wave-1 0.209 | `analysis/calibration_wave2.json` → `ece_10bin`; `analysis/calibration.json` → `ece_10bin` |
| FP atlas 점수: case_30 점수 65 · case_10 점수 58 | `atlas/case_30.md`, `atlas/case_10.md` (동결 점수 인용, RP-16/D91); 종합 `atlas/PATTERNS.md` §d |
| 사전 등록 커밋 `c1b85a7` (채점 전 계획 동결) | `README.md` (Extension experiments 절); `analysis/*_PLAN.md` git 이력 |
| 재현 100/100, API 호출 0 | `tools/reproduce_analysis.py` (직접 실행; CI 검증) |
| Forward 봉인일 2026-11-15 · 12사 유니버스 · ≥11/12 정지 규칙 | `specs/FORWARD_WATCHLIST_V1.md` §1–§3; `forward/cycle_001/universe.json` (`selected` = 12) |

*라벨: HUBG · WMK · GNE는 잠정 Item 4.02 비신뢰 정정 사건(G2)으로 업그레이드
모니터링 대상 — 확정 사기가 아니다. 대조군 회사는 "비집행"이지 무결 인증이
아니다(L-8: 발행된 거짓양성 비율은 원 대조군 선정 기준에 조건부). 한계 전문:
L-1부터 L-8, `docs/methodology_limitations.md`.*

*DRAFT — 소유자 확정 전. 채점: Claude 보조 + 인간 최종 확정.
포지션 없음 · 교육·정보 목적 · 투자 조언 아님.*
