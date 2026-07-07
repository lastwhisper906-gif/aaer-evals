# 오류 해부 — wave-2 (실험군 9 vs 대조군 23) + 홀드아웃 (HUBG·WMK·GNE)

> Authored by Claude Code, pending human audit (GA-001 (b)). 2026-07-08 (OWNER-GATE-E 세션, P1).
> 대상: 동결 채점 결과(`scoring/grades_wave2/`, `scoring/grades_holdout/`,
> human_finalized=false)의 오류 전수 해부. 인용은 전부 동결 산출물 verbatim
> (`runs/wave2/scores/`, `runs/holdout/scores/`) — 날조 인용 금지(§5-3).
> **범위 한정(§5-5)**: 본 결과는 Claude 기반 단일 파이프라인(피평가자
> claude-sonnet-5 핀)에 한정, 전체 LLM 일반화 아님. 대조군 라벨="비집행"(무결 아님).
> 홀드아웃 전원 **G2 provisional**(restatement/non-reliance) — "fraud"·"분식" 금지.
> **이 문서가 `wave2_summary.md` L52 스텁("후속 분류")을 해소한다.**

## §0. 분류 체계 (RP-10 Phase 3.1 계승, 4분류)

각 오류를 하나로 분류하되, 혼합이면 주분류 + 부기:

- **(i) 증거 부재(evidence-absent)**: 모델이 페이로드에 **없는** 사실을 지어냄(환각).
- **(ii) 추론 실패(reasoning-failure)**: 페이로드의 **실재** 수치를 잘못 해석 — 오독한
  구절을 인용한다. 하위형: (ii-a) 양성 오독(정상 패턴을 위험으로 승격), (ii-b)
  보정 실패(방향 맞으나 확신/임계 오배치), (ii-c) 데이터품질 인공물 오독(XBRL 태깅
  오류를 신호로).
- **(iii) 라벨 문제(label problem)**: 정답 키가 모호/오류.
- **(iv) 구조적 미탐(structurally undetectable)**: 신호가 제공 데이터(GAAP XBRL)에
  **애초에 없음** — 비-GAAP 지표·서브원장·비재무 사건.

## §1. 거짓양성 5/23 (대조군, p≥50) — **전건 환각 아님, 전건 (ii) 양성 오독**

| 대조군 | p | risk_tier | dim4(증거품질) | 주분류 |
|---|---|---|---|---|
| IOVA (Iovance) | 58 | elevated | 근거됨(consistency OK) | (ii-a) |
| ADAM (Adamas/모기지REIT) | 55 | elevated | 근거됨(no cap) | (ii-c)+(ii-a) |
| LEVI (Levi Strauss) | 55 | elevated | 근거됨(dim4=2) | (ii-a) |
| LPSN (LivePerson) | 55 | elevated | 근거됨(dim4=3) | (ii-a) |
| AORT (Artivion) | 50 | watch | 근거됨(dim4=3) | (ii-a) 경계 |

**핵심 발견 (L52 스텁 해소)**: 채점자 rationale이 **5건 전부** "evidence is
specific and grounded in provided data, arithmetically verifiable ... rather than
fabrication"으로 판정(dim4 상단). 즉 **오탐의 원인은 수치 날조(i)가 아니라 실재
수치의 과잉해석(ii-a)** — 정상적 구조/비율 발산을 위험으로 승격. 이는 파이프라인의
신뢰 경계가 **환각이 아니라 base-rate 무시·양성 설명 누락(보정)** 쪽에 있음을 뜻한다
(환각보다 원리상 교정 가능성이 높은 실패형).

- **IOVA (58)** — 페이로드 신호는 실재: `NetIncomeLoss=-25,381,363 vs OCF=-3,662,192`
  (2013). 그러나 모델 자신이 top 가설에서 원인을 "large non-cash charges ... **typical
  of reverse-merger micro-cap biotechs**"로 규정하고도 elevated로 승격 — **정의상 정상**
  (전임상 바이오텍은 대규모 비현금 손실↔현금유출 괴리가 구조적 정상)인 패턴을 위험으로
  읽음. (ii-a).
- **ADAM (55)** — 헤드라인 신호 "quarterly InterestExpense (Q4-2013 `68,584,000`) vs
  annual (`6,655,000`)"은 **분기·연간 스코프 XBRL 태깅 인공물** 가능성이 큼. 모델도
  "possible understatement/**mis-tagging**"로 자헤지하면서도 elevated. → 데이터품질
  인공물을 신호로 오독 (ii-c) + 양성 오독 (ii-a). *파이프라인 시사점*: 태깅 정합성
  사전검사가 이 오탐을 줄일 수 있음(수정 후보, 최대 2지점 제약 내).
- **LEVI (55)** — "AR grew 40–68% YoY ... while revenue grew only 3.8–6.8%"는 산술
  검증됨(`722,001,000` vs `487,240,000`=+48.2%). 그러나 **Levi Strauss는 2019-03
  IPO** — FY2019 매출채권 급증은 상장 직후 도매 확장/계절성의 양성 설명. 모델이 그
  대안을 저울질하지 않음. (ii-a).
- **LPSN (55)** — "allowance flat at $708,000 for seven quarter-ends ... AR +84%,
  then 65% catch-up" + SEC comment letters. 실재하나 양성(코멘트레터≠부정, allowance
  catch-up 흔함). (ii-a).
- **AORT (50)** — p=50은 **플래그 임계 정확히 위**. 모델 스스로 "watch"만 선언. 1점
  차이로 뒤집히는 **경계 인공물** — 5건 중 최경증. (ii-a, 경계).

**FPR 비교 (wave-1 3/22 vs wave-2 5/23)** — 악화했으나 **입증 불가**:
- wave-1: 13.6%, Clopper-Pearson 95% **[2.9%, 34.9%]**
- wave-2: 21.7%, Clopper-Pearson 95% **[7.5%, 43.7%]**
- wave-2 점추정 21.7%는 wave-1 구간 [2.9%, 34.9%] **내부**에 있고 두 CP 구간이 크게
  겹친다 → "**worse-but-not-provably**"(N~22–23에서 구별 불가). 0% 헤드라인 금지 준수.

## §2. 미탐 2/9 — **정반대 두 유형** (평균화 금지)

- **CSC (Computer Sciences, p=40 → 미플래그) — (ii-b) 보정 near-miss, 탐지내용은 맞음**
  - 정답 키(AAER-3662): UK NHS 계약 POC 과대 + 호주 cookie-jar 준비금 + Nordic
    prepaid 비용 부당 자본화·자산 과대.
  - 모델 top 가설: "continued capitalization of costs ... under-impairment"로
    `OtherAssetsNoncurrent +25.7%` (매출 −3.7% 동시)를 지목 → 채점자 **dim2=2**
    ("substantially matches ... expense_capitalization / asset_overstatement, direction
    (overstated), treatment type"). **즉 계정영역·방향·기법이 실질 일치**.
  - **미탐의 실체는 탐지 실패가 아니라 확신 부족**: 옳은 기제를 봤으나 p=40으로 임계
    50 미달. **10점 상향이면 플래그**. 유형 (ii-b) 보정 실패 — 파이프라인이 옳은 것을
    봤다. (reserves_smoothing 축은 CL6=insufficient_data로 미커버.)
- **BRX (Brixmor, p=20 → 미탐, dim2=0) — (iv) 구조적 미탐, 가장 깨끗한 (iv) 사례**
  - 정답 키(AAER-4061): **비-GAAP 'same property NOI(SP NOI)' 성장률**을 '2617' cookie-
    jar 원장으로 분기 간 평활 + lease-termination income 타이밍. → 조작이 **GAAP 연결
    재무제표 라인에 없음**(비-GAAP 운영지표 + 내부 서브원장).
  - 모델은 NI/OCF 괴리를 "**largely explained by substantial real estate depreciation
    ... a normal REIT characteristic**"로 정확히 기각하고, 스스로 "**Missing key data
    (revenue, intangible assets, allowance/reserve balances) prevents full
    evaluation**"로 데이터 공백을 명시. mechanism_hypotheses=빈 리스트.
  - **XBRL-재무제표 전용 파이프라인은 비-GAAP 지표 조작을 구조적으로 탐지 불가.** 이것이
    trust boundary의 경계 사례다(능력 부족 아님 — 입력에 신호 부재). 유형 (iv).

**시사**: 9건 중 **구조적으로 파이프라인 사거리 밖은 BRX 1건뿐**. CSC는 보정 near-miss
(옳은 기제, 임계 미달). "미탐 2"를 뭉뚱그리면 이 비대칭이 사라진다.

## §3. 홀드아웃 (암기 불가, identity frame) — per-case

- **HUBG (70, 플래그 ✔, dim1=2 / dim2=1) — 점수는 맞고 기제는 빗나감**
  - 정답 키: 매입운송비 ~$77M 과소·미기록 AP, FY2023-24 10-K 오기재, CFO·COO 해임
    (8-K Item 4.02, 2026-02-05).
  - 모델 top 가설·신호는 **과거 2018-01-05 정정 클러스터**(10-K/A FY2015 + 3×10-Q/A)
    와 goodwill `262.4M→733.7M(+178%)` 손상 위험에 정박 — 채점자 dim2=1: "TOP-ranked
    hypothesis instead centers on the **historical 2018-01-05 amendment cluster** ...
    not [the 2026 event]". **즉 옳은 회사·옳은 tier를 옳은 이유로 잡지 못함**.
  - **정직한 프레이밍**: HUBG "적중"은 *리스크 스크리닝* 능력의 증거(정정 이력+goodwill
    bloat 있는 회사를 elevated로)이지 *2026 기제의 forensic 탐지* 증거가 아니다. H2의
    "HUBG를 잡았다"는 서사는 **tier 적중/기제 빗나감**으로 한정해야 한다. (부분 (ii-b):
    옳은 방향의 리스크 신호, 특정 사건 기제는 미상.)
- **WMK (32, 미탐, dim2=0) — (ii-a)/(iv) 혼합: 연결 수준에 비해 비중대**
  - 정답 키: 육가공 공장 재고 과대 ~$22M 누적(FY2022-25), 내부고발.
  - 모델은 AR/DSO 발산(`AR +28%/+25%` vs 매출 flat, "DSO ~3.9→6.2 days")을 추격 —
    **엉뚱한 계정영역**. 채점자: "CL4 examined inventory" 했으나 무플래그. → 단일 육가공
    공장의 4년 누적 $22M 과대는 **식료품 체인 연결 재고에서 비율 신호를 남기지 않음**
    (신호<잡음). 유형 (ii-a) 대체신호 추격 + (iv) 연결 수준 비중대성.
- **GNE (42, 경계, dim2=0) — (ii-a) 경계, error-like에 정합적 불확실**
  - 정답 키: 캡티브보험 부채 오류(error-like, non-fraud).
  - 모델은 allowance/AR 커버리지 급락(14.9%→8.8%)을 지목 — 계정영역 빗나감. 그러나
    p=42 "watch"는 error-like 사건에 **정합적 불확실**(과확신 아님). 최경증.

## §4. 보정 (calibration) — wave-2 ECE **0.179** vs wave-1 0.209 (null-ish)

`analysis/calibration_wave2.py` → `calibration_wave2.json` (동결 점수 재사용, 정의는
동결 `calibration.py`와 동일: 10-bin ECE, 확신=|p−50|/50).

- **ECE 0.179** (wave-1 0.209, Δ−0.03) — **동일 차수, 실질 개선 없음**. 여전히 ~0.18
  미보정. "보정이 좋아지지 않았다"는 **null-ish 결과이며 보고 대상**(§자기미화 금지).
- 확신→정오 AUROC 0.746, 임계 정확도 25/32(=7오류: 미탐2+오탐5). 확신에 정보는 있으나
  절대 보정은 나쁨 — §1의 "실패는 환각이 아니라 보정"과 정합.

## §5. Trust boundary 종합 (오류 귀속 §5-3)

1. **오탐(5/23)은 환각(i)이 아니라 양성 오독(ii-a)** — 전건 근거됨(dim4 상단). 신뢰
   경계는 base-rate/양성설명 축. 파이프라인 수정 후보: ADAM류 태깅 인공물 사전검사(ii-c).
2. **미탐은 CSC(보정 near-miss, 옳은 기제 임계미달)와 BRX(구조적 (iv), 비-GAAP)로
   비대칭** — 사거리 밖은 1건.
3. **홀드아웃 적중(HUBG)은 tier 맞고 기제 빗나감** — 리스크 스크리닝 ≠ forensic 기제
   탐지. H2 서사를 이 강도로 한정.
4. 보정은 wave-1 대비 개선 없음(ECE~0.18).

**이 판단에서 알아야 할 것(학습 노트, §10)**: "적중/미탐"의 이진 집계는 **오류의 종류**를
지운다 — 같은 미탐도 (ii-b 보정 near-miss)와 (iv 구조적 미탐)은 파이프라인 함의가
정반대고(전자는 임계/보정 손질, 후자는 입력 확장 아니면 불가), 같은 적중도 기제 정합
없는 tier 적중은 forensic 주장을 지탱하지 못한다. **오탐이 전건 근거됨**이라는 사실은
이 파이프라인의 실패가 "지어내기"가 아니라 "과잉해석"임을 말하며, 이는 신뢰 경계의
성격(교정 가능성)을 규정한다.

## §6. 미완 / 후속

- **E1 대조군 오탐 해부**: E1(홀드아웃 매칭 대조군) 미실행 → 대조군 오탐 발생 시 본
  문서 §1에 동형 편입(placeholder). 사전 등록: `analysis/HOLDOUT_CONTROLS_PLAN.md`.
- ADAM 태깅 인공물(ii-c) 사전검사 = 파이프라인 수정 후보(≤2지점 제약, 별도 게이트).

## §7. 면책

단일 Claude 파이프라인(claude-sonnet-5 핀) 한정, 채점 Claude 보조 + 인간 최종 확정
대기(human_finalized=false). 대조군="비집행" 라벨(무결 아님). 홀드아웃 G2 provisional
— 공개 8-K(Item 4.02) 근거 의견이며 SEC 확정 부정 아님. 포지션 없음, 비공개 정보 미사용.
