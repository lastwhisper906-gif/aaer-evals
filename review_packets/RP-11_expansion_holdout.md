# RP-11 — Wave 2 확장 + Temporal Holdout Tier 1 게이트 패킷

> Authored by Claude Code, pending human audit (GA-001 (b)). 2026-07-07.
> 대상: wave-2 로스터 확장(N 8→~17 시도)과 컷오프-후 홀드아웃 Tier 1. **발행
> 행위 없음.** 동결 wave-1(8v22) 결과·기준 불침해 (RESULT IMMUTABILITY). 본
> 결과는 Claude 단일 파이프라인 한정(§5-5).
>
> **이 세션의 성격**: 사전 커밋(pre-registration) 2건 + 게이트 실행 2건을
> 완료했고, **채점 발사(wave-2 실험군/대조군, 홀드아웃)는 INCOMPLETE**로
> 남긴다. 시간·컨텍스트 예산에서 사전 고정 순서(알파벳)로 절단했으므로
> INCOMPLETE는 결과 독립적이다(선택 아님). 불변 검사·사전커밋-선행·완료분
> freeze는 절단하지 않았다.

## 0. 한 줄 요약

- **사전 커밋 잠금(발사 전 타임스탬프)**: wave-2 분석계획·로스터규칙·교란규칙·
  채점순서(`9438b0c`), 홀드아웃 기준(`62d2fda`).
- **wave-2 로스터 = 규칙+게이트가 확정**: A형 23 − 채점 8 − 오염 2 − G-XBRL 실패
  4 = **생존 9** (`190783b`).
- **wave-2 전 파이프라인 실행 완료 → 발동 규칙 R4 (능력 시연)**: 채점 32(9v23)
  +교란 9+프로브 64+채점자 32 동결. 순열 p=0.00116, AUC 0.829, R1/R2/R3 전부
  비발동. wave-1(R3 암기)과 대조되는 결과 (§2.4).
- **홀드아웃 RECOGNITION GATE 실행·freeze**: 후보 3/3 **비인지 실증** → N=3,
  H3-STOP 비발동 (`0d64a7a`). 계기는 양성 대조 2건으로 검증.
- **INCOMPLETE**: 홀드아웃 채점(H1/H2) — 컷오프 후 3사+대조군 채점 (§3.4).
  wave-2는 완료.
- make verify **green** (reproduce 100/100 · blindness PASS · manifest 396 ·
  pytest 76).

## 1. P0 저장소 무결성 (완료)

README.md 헤드라인·상태를 RP-05 잔재(AUC 0.797/p=0.0226/대조 8/
human_finalized=False)에서 RP-10 정합으로 교체 (`67523af`): R3 헤드라인,
대조군 22, 순열 p=0.00114(원본)/0.0021(교란), AUC 0.824[0.599,0.983], FP 3/22
CP[2.9%,34.9%], 채점 26 human_finalized=true, 교란-우선 읽는순서·bounds-not-
eliminate 유지, ISSUE_0 포인터. 동결 파일 무변경. baseline green 확인 후 작업.

## 2. P1 Wave 2 — 로스터 확정 (규칙+게이트), 채점 INCOMPLETE

### 2.1 사전 커밋 (발사 전, `9438b0c`)
`EXCLUSION.md`(로스터 규칙·오염 제외·게이트 정의·폭로일 절차·대조군 순수함수·
memorization_risk 태그) + `analysis/ANALYSIS_PLAN_WAVE2.md`(동결 R1-R4·순열
100k·Fisher p≥50·rule-of-three FPR 그대로 재적용 · standalone 1차 / pooled
2차 병기전용 · 교란 draw 1회 = 열화 사다리 1순위 · 알파벳 채점순서).

### 2.2 로스터 규칙의 기계 판정
A형 23 (동결 `candidates.json`, 전건 서명) − wave-1 채점 8 (MON·OFIX·LOGI·HTZ·
ICON·MRVL·SCOR·KHC) = 15 − worked-example 오염 2 (**VRX·GE** — 채점 기준을 이
케이스 정답키로 구성, 결과 가치 보호) = 13 → 게이트.

### 2.3 게이트 실행 (`190783b`, 점수 독립)
`fetch_xbrl_facts.py`로 companyfacts 조회 + 동결 `build_payload.load_pit_series`
로 컷오프-전 PIT 커버리지 측정 (오프라인·결정론). **사전 판단 없이 게이트가
결정.**

| 최종 | 티커 | 근거 |
|---|---|---|
| **생존 9** | BRX CGI CSC HAIN MDXG OSIR TNGO UAA WFT | 컷오프-전 PIT 시계열 사용 가능 (커버리지 표 EXCLUSION §4) |
| 실패 | **PUDA** | companyfacts 404 (中 RTO, XBRL 무등록) |
| 실패 | **MILL** | 최초 us-gaap 사실 filed = 컷오프+70일 (XBRL 채택이 폭로 후) |
| 실패 | **DMND** | 최초 사실 filed = 컷오프+1년 ("수기 비용" 실증) |
| 실패 | **PWE** | 캐나다 40-F/IFRS (us-gaap 2018 이후만) |

- 기대 생존 9와 일치하나 **게이트가 근거**(기대는 비구속). China-RTO
  memorization_risk 사전 태그 해당자 0 (유일 China-RTO인 PUDA가 G-XBRL 탈락).
- **커버리지 주석**: BRX = 표준 Revenues 태그 부재(REIT 임대수익) — NI+자산으로
  통과, 페이로드는 표준 매출 결측. OSIR = NI 분기 커버리지 얕음(rev로 통과). 둘
  다 채점 해석 시 참조.
- WFT 전신 CIK(0001170565) companyfacts 404 — XBRL 시대 이전, 주 CIK가 커버.

### 2.4 발동 결론 규칙 (실행 완료 — **R4 발동**)
소유자 발사 승인 후 전 파이프라인 실행 완료: 대조군 선정 23 → 채점 32(실험군
9+대조군 23) → 교란 draw 9 → 인지 프로브 32 → verbatim 프로브 32 → 채점자 32
(human_finalized=false). 전건 동결. 분석 `analysis/wave2_summary.md` +
`wave2_results.json` (`python analysis/wave2_analyze.py` 재현):

- **R1 비발동**: 순열 p = **0.00116** (평균차 +20.6pp, fraud 55.2 vs control 34.7).
- **R2 비발동**: ρ(LLM,M)=0.337 · ρ(LLM,F)=0.265 (< 0.7).
- **R3 비발동**: 정체-교란 초과 **3/9** (CSC·BRX·UAA) — 과반 미달 (wave-1 5/8 대조).
- ⇒ **R4 발동 (능력 시연)**. Cliff δ 0.657 · AUC 0.829 [0.616, 0.983] · Fisher
  7/9 vs 5/23 · FPR 21.7% CP[7.5%, 43.7%]. 이름 프로브 정답률 **25%**(wave-1
  50%의 절반 — 덜 유명한 표본, 암기 약함 → R3 비발동과 정합).
- **pooled 2차 (17 vs 45, 병기 전용)**: p = 3.0e-05 · AUC 0.831 (wave-1 동결
  재사용·재채점 없음; standalone R4가 헤드라인).

**핵심**: wave-1(유명 사건)=R3(암기 얽힘) → wave-2(덜 유명)=R4(잔여 능력). 컷오프
후 홀드아웃이 능력 질문의 독립 검증. N=9 단일 파이프라인 한정 (R4 프레이밍 제약).

### 2.5 wave-2 대조군 (게이트 확정)
동결 `control_v2` 순수 함수(드라이버 `tools/wave2_controls.py`, 케이스 스펙 유도
+ decade sic_supp) → **23 선정** (2-3/케이스, 우수한 산업 매칭: CGI→Saia·Marten
트럭 · HAIN→Flowers·Darling 식품 · UAA→Levi·Ralph Lauren 의류 · BRX→REIT 3사).
런북 `tools/run_wave2_scoring.py` (동결 파이프라인 무수정 재사용, WFT 폭로-후
사명 누출 수정). 발사 중 레이트리밋 1회 → 멱등 재개.

## 3. P2 Holdout — RECOGNITION GATE 실행·admit, 채점 INCOMPLETE

### 3.1 사전 커밋 (`62d2fda`)
`docs/HOLDOUT_CRITERIA.md`: Universe(HUBG·WMK·GNE 1차) · 라벨 티어(전원 **G2
PROVISIONAL** → "restatement/non-reliance event"만, "fraud"·"분식" 금지) ·
RECOGNITION GATE(척추) · 대조군 non-recognition · 정체=PRIMARY 프레임 · 결론
규칙 H1/H2/H3.

### 3.2 RECOGNITION GATE 실행·freeze (`0d64a7a`) — 이 세션의 핵심 실측
동결 `cli_client` 경로(claude-sonnet-5 핀 검증, 격리 tempdir, 구독 OAuth)로
직접 최근사 스크린 5호출 (누출 없는 개방형 질문 — 폭로 사건을 프롬프트에
명시하지 않음). 전건 pin_ok=True.

| 티커 | 종류 | knows_event | conf | 판정 |
|---|---|---|---|---|
| HUBG | 후보 | **False** | none | ADMIT (비인지) |
| WMK | 후보 | **False** | none | ADMIT — "Pennsylvania 슈퍼마켓"으로 정체는 알되 회계 사건 미암기 = 이상적 신호 |
| GNE | 후보 | **False** | none | ADMIT (비인지) |
| HTZ | 양성대조 | **True** | high | 계기 검증 — 2014 재작성·Frissora 사임·$16M SEC를 사실 정확히 서술 |
| KHC | 양성대조 | **True** | high | 계기 검증 — 2018 소환·~$200M COGS·Item 4.02·2021 합의를 사실 정확히 서술 |

**해석**: 계기는 비자명하다(양성 대조에서 실제 컷오프-전 사건을 고정밀 재현).
후보 3/3의 비인지는 "모르는 척"이 아니라 컷오프-후 폭로의 구조적 미암기.
정체 프레임이 유효(정체는 알되 폭로는 모름) → 홀드아웃 설계의 핵심 전제 실증.

### 3.3 H-규칙 판정
- **H3(N<3 STOP) 비발동**: 게이트 통과 후보 N=**3** ≥ 3.
- **H1/H2 미결(INCOMPLETE)**: 홀드아웃 채점(fraud vs control 순열, 케이스별
  점수) 미발사. HUBG(컷오프 +5일 경계)는 §d 직접 최근사 스크린을 이미 통과했다
  (본 게이트가 그 스크린). 대조군 non-recognition 게이트 + 채점은 재개 대상.
- 프로즈 제약 유지: 세 사 전부 **G2 = PROVISIONAL**, "restatement/non-reliance
  event"로만 서술.

### 3.4 INCOMPLETE 명세 (홀드아웃)
HUBG·WMK·GNE + 대조군 페이로드 빌드(EDGAR/XBRL, 컷오프=폭로 전일) · 대조군
non-recognition 게이트 · 채점 + 프로브 + 채점자 · P2.2 소규모-N exact 순열·
M/F 기준선. **미발사.** sec.gov egress는 이 환경에서 가용(HTTP 200 실측) —
차단 아니므로 fetch manifest 대신 직접 조회 재개 가능.

## 4. 호출 회계 (참고 비용 — 구독 흡수)

| 스트림 | 호출 | 결과 |
|---|---|---|
| 홀드아웃 recognition gate | 5 (후보 3 + 양성대조 2) | ok 5/5 · pin_ok 5/5 · $0.0593 ref |
| 하네스 스모크(비산입, 격리 확인) | 2 | sonnet-5 핀 확인 (isolation env로 하우스키핑 haiku 억제 실증) |

wave-2·홀드아웃 채점 호출 = 0 (INCOMPLETE). 하네스 핀 실측: HARNESS_PIN 코드값
2.1.201 vs 설치 2.1.202 — 참고 기록 불일치일 뿐 게이트는 서빙 모델(sonnet-5)로
판정(pin_ok=True).

## 5. Degradation-ladder 로그 (사용됨)

시간·컨텍스트 예산에서 사다리를 적용:
1. (미적용) wave-2 교란 draw drop — 채점 자체가 미발사라 무의미.
2. (미적용) 홀드아웃 대조군 2/케이스 축소.
3. **(적용) 미채점 케이스 INCOMPLETE 표기** — wave-2 채점 전건 + 홀드아웃 채점.
   사전 고정 알파벳 순서라 절단은 결과 독립적. 절단 지점: 로스터 확정·
   recognition gate 완료 후, 대조군 선정·채점 발사 전.

**never-cut 준수**: 불변 검사(BLINDNESS·CUTOFF·RESULT IMMUTABILITY), 사전커밋-
선행(2건 모두 발사 전 커밋), 완료분 freeze(recognition gate + 매니페스트) 전부
유지.

## 6. 소유자 재개 명령 (사전 고정 순서대로)

**wave-2 채점** (생존 9 XBRL·사전커밋 완료 상태에서):
1. 대조군 선정(순수함수, 생존 9 대상) → 페이로드 빌드 → `data/evaluatee/
   cases_wave2.json` (알파벳 순서, 중립 ID case_31.. 비겹침).
2. clean tree 커밋 후: `runner.py --cases … --out runs/wave2/scores` →
   `probe_runner.py --recognition/--verbatim` → 이름 프로브 → `grader_runner.py`
   (human_finalized=**false**). 병렬 3, retry-once-then-INCOMPLETE.
3. freeze: `verify_blindness.py --write-manifest` **포함** 커밋 (runs/ 규율).
4. 분석: `ANALYSIS_PLAN_WAVE2` — standalone 1차 발동 규칙 + pooled 2차 병기.

**홀드아웃 채점**:
1. HUBG·WMK·GNE + 대조군 EDGAR/XBRL fetch (컷오프=폭로 전일) → 페이로드.
2. 대조군 non-recognition 게이트(본 세션 스크립트 재사용) → 통과분만.
3. 채점 + 프로브 + 채점자(human_finalized=false) → freeze → P2.2 분석.
4. H1(p<0.05→분석적 탐지 주장, G2 캐비앳)/H2(wave-1 병기, no pool) 판정.

## 7. 산출물 커밋 지도

`67523af` README · `9438b0c` wave-2 사전커밋 · `62d2fda` 홀드아웃 사전커밋 ·
`190783b` 게이트→로스터 확정 · `0d64a7a` recognition gate+freeze.

## 8. 소유자 액션

1. RP-11 통독 + `EXCLUSION.md`·`docs/HOLDOUT_CRITERIA.md`·`ANALYSIS_PLAN_WAVE2`
   사전 커밋 검토 (발사 전 타임스탬프 확인).
2. recognition gate transcript(`runs/holdout/recognition/*.json`) 판독 —
   특히 후보 3사 비인지 + 양성대조 정확도.
3. wave-2/홀드아웃 채점 발사 승인 여부 (§6 재개). 채점자 grades는 소유자만
   human_finalized=true.
4. Issue #0 발행 결정(불변) — 이제 companion 증거(홀드아웃 admit) 손에 두고.

**본 세션은 여기서 정지 — 발행 행위 없음. 채점 발사는 소유자 게이트.**
</content>
