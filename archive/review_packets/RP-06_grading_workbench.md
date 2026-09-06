# RP-06 채점 확정 워크벤치 — 소유자 서명대 (B1)

> Authored by Claude Code, pending human audit (GA-001 (b), D15). 2026-07-06.
> **용도**: 26건 채점(본 실행 16 + 교란 8 + 파일럿 2)의 인간 최종 확정 (§7).
> 각 케이스 = 2분 내 처리 목표. 읽는 법: 피평가자 p·가설 → 채점·rationale 발췌
> → (있으면) A2 교차 채점 delta → 귀속 태그 → 서명란.
> **루브릭 밴드 (참조)**: 실험군 p≥70→2 / 50–69→1 / <50→0 · 대조군 p≤30→2 /
> 31–49→1 / ≥50→0. d2: 0 무관/부재, 1 계정 영역, 2 +방향+처리 유형, 3 +케이스
> 특이 사실. **MODEL 귀속 5건에는 SKEPTICAL-REVIEW 플래그** — 자기변호(Claude가
> Claude를 채점) 위험 구역, 우선 검토.
> A2 교차 채점은 runs/hardening/regrade_opus/ (SPOT-CHECK 전용 — scoring/grades/
> 병합 금지). 서명 결과는 각 grade 파일 human_finalized=true 갱신 +
> 오버라이드는 scoring/overrides.md 기록.

## case_01 = Comscore, Inc. (SCOR, T21) — 부록(원본 실험군 — 상한 전용)

- 피평가자: **p=55** · tier=elevated · 가설 (확신 순):
  1. [overstated] AccountsReceivableNetCurrent, Revenues, AllowanceForDoubtfulAccountsReceivableCurrent — Potential premature/aggressive revenue recognition or delayed write-off of receivables in FY2013, evidenced by accounts receivable growing ~31.8% (AccountsReceivableNetCurrent=68,348,000 (2012-12-31) to 90,040,000 …
  2. [timing_shift] AccountsPayableCurrent, AccountsReceivableNetCurrent (Q1 2013 balance sheet) — A quick amendment to the Q1 2013 Form 10-Q (original filed 2013-05-03, amended 10-Q/A filed 2013-05-13, only 10 days later) suggests an error was identified and corrected shortly after original issuance, indicating …
  3. [understated] NetIncomeLoss, NetCashProvidedByUsedInOperatingActivities, DeferredRevenueCurrent — Persistent GAAP net losses each year 2010-2014 alongside strong and growing operating cash flow (e.g., NetIncomeLoss=-9,903,000 (FY2014) vs NetCashProvidedByUsedInOperatingActivities=49,497,000 (FY2014)) could reflect …
- 채점 (claude-fable-5): **d1=1** · d2=1 · d3=mixed/1 · d4=3 · mem2=F
- 채점 rationale 발췌 (≤5줄):
> DIM1 (band=1): Treatment case; output gives misstatement_probability=55, which falls in 50<=p<70 → 1 per rubric.
> DIM2 (=1): Top-ranked hypothesis targets Revenues/AccountsReceivableNetCurrent/Allowance with direction 'overstated' — correct account area (revenue overstatement matches the key's 'overstated revenue by approximately $50 million'). However, the proposed treatment type is 'premature/aggressive revenue recognition or delayed write-off of receivables' inferred from AR-vs-revenue divergence; the …
> DIM3 (mixed vs active → 1): The top hypothesis narrative blends an active scheme (premature/aggressive revenue recognition) with an omission/estimate element (delayed write-off of receivables; allowance not scaling with AR). Mapped genre = mixed; answer-key genre = active(revenue); one-sided-vs-mixed → 1.
> DIM4 (=3): Evidence citations are concrete provided data points with accession numbers that genuinely support the claims (e.g., AR 68,348,000→90,040,000 vs Revenues 255,193,000→286,860,000 for the DSO divergence; NetIncomeLoss vs operating cash flow for FY2011/FY2012/FY2014; the 10-day 10-Q→10-Q/A gap in May 2013; $0 allowance quarters in 2015 against $77-98M AR). The reasoning coherently …
- 오류 귀속 (1차): — (본 분석 오류 단위 아님)
- **서명**: ☐ finalize   ☐ override (사유: ______________________ → overrides.md 기록)

## case_02 = Orthofix International N.V. (OFIX, T11) — 부록(원본 실험군 — 상한 전용)

- 피평가자: **p=60** · tier=elevated · 가설 (확신 순):
  1. [overstated] SalesRevenueNet, AccountsReceivableNetCurrent, AllowanceForDoubtfulAccountsReceivableCurrent — Possible premature/aggressive revenue recognition (e.g., channel stuffing to distributors) inflating sales and receivables in FY2012 even as reported revenue declined, followed by a sharp build-up in the bad-debt …
  2. [overstated] NetIncomeLoss, NetCashProvidedByUsedInOperatingActivitiesContinuingOperations — Accrual-heavy earnings recognition in FY2012 not supported by cash generation, consistent with either aggressive revenue/expense timing or use of accrued reserves/estimates that inflate reported net income relative to …
  3. [overstated] InventoryNet, CostOfGoodsAndServicesSold, GrossProfit — Potential under-provisioning for excess/obsolete inventory or capitalization of costs into inventory, allowing gross margin to expand (80.3%->81.3%) even as revenue declined and inventory grew faster than sales.
- 채점 (claude-fable-5): **d1=1** · d2=2 · d3=active/2 · d4=3 · mem2=F
- 채점 rationale 발췌 (≤5줄):
> DIM1=1: Treatment case; output states misstatement_probability=60, which falls in the 50<=p<70 band -> 1.
> DIM2=2: Top-ranked hypothesis targets SalesRevenueNet/AccountsReceivableNetCurrent, direction 'overstated', treatment 'premature/aggressive revenue recognition (e.g., channel stuffing to distributors)'. Answer key (AAER-3845/33-10281) describes materially overstated distributor revenue via improper recognition on contingent/return-eligible distributor sales. Account area, direction, and …
> DIM3: Top hypothesis narrative (channel stuffing/premature revenue recognition inflating sales) maps to 'active'; answer-key genre is active(revenue) -> exact match -> 2.
> DIM4=3: Evidence consists of specific provided data points with values, dates, and accession numbers that genuinely support the claims: AR +13.2% (132,828k->150,316k) vs revenue -1.7% (470,121k->462,320k); doubtful-account allowance +72.6% (9,376k->16,188k); NI/OCF inversion (FY2011 NI -1,073k vs OCF 64,781k; FY2012 NI 51,295k vs OCF 11,206k); goodwill restated between the 2012 and 2013 10-Ks; …
- 오류 귀속 (1차): — (본 분석 오류 단위 아님)
- **서명**: ☐ finalize   ☐ override (사유: ______________________ → overrides.md 기록)

## case_03 = Logitech International S.A. (LOGI, T12) — 부록(원본 실험군 — 상한 전용)

- 피평가자: **p=42** · tier=watch · 가설 (확신 순):
  1. [overstated] Goodwill, OperatingIncomeLoss, NetIncomeLoss — Possible delayed/insufficiently conservative goodwill impairment testing in FY2010-FY2012, allowing goodwill to remain at elevated carrying value (Goodwill=560523000 at 2012-03-31; Goodwill=561080000 at 2012-09-30) …
  2. [understated] AllowanceForDoubtfulAccountsReceivableCurrent, AccountsReceivableNetCurrent, NetIncomeLoss — Reduction of bad debt allowance as a percentage of gross receivables (from ~3.0% to ~1.2% over FY2010-FY2013) could reflect reserve releases that modestly understate the allowance for doubtful accounts, thereby …
  3. [timing_shift] InventoryNet, CostOfGoodsAndServicesSold, GrossProfit — Inventory build-up in FY2012 (InventoryNet=297072000 at 2012-03-31 vs 280814000 at 2011-03-31) despite a revenue decline (SalesRevenueNet=2316203000 FY2012 vs 2362886000 FY2011) could indicate delayed recognition of …
- 채점 (claude-fable-5): **d1=0** · d2=1 · d3=omission-estimate/2 · d4=3 · mem2=F
- 채점 rationale 발췌 (≤5줄):
> DIM1 (0): Treatment case (LOGI, AAER-3765 / 34-77644). Output gives misstatement_probability=42, which is <50 → band score 0 per treatment rule.
> DIM2 (1, borderline — flag for auditor): Rubric requires grading the TOP-RANKED hypothesis only. Top hypothesis = delayed/insufficiently conservative GOODWILL impairment testing FY2010–FY2012 (Goodwill 560.5M→345.3M in Q3 FY2013), direction overstated. Ground-truth mechanisms are (a) delayed ~$30.7M LCM write-down of Revue INVENTORY in FY2011, (b) understated FY12–13 WARRANTY liabilities, (c) …
> DIM3 (omission-estimate, 2): The top-ranked narrative is failure to timely record an estimate-based impairment charge (delayed impairment testing / "big bath"), which maps to omission-estimate — no fabricated transactions, purely omitted/mistimed estimates. Answer-key genre for T12/LOGI is omission-estimate ("write-down... warranty liabilities... failure to correct known error" — 추정 시점 조작). …
> DIM4 (3): Consistency rule: p=42 falls in 40≤p<70 → tier must be watch/elevated; declared tier is "watch" → no cap. Evidence is specific and internally verifiable from provided series: multi-year goodwill trajectory (553.5M/547.2M/560.5M/340.1M, plus quarterly 561.1M at 2012-09-30 → 345.3M at 2012-12-31 tied to OperatingIncomeLoss=-180.0M in Q3 FY2013), allowance-coverage ratio computed across …
> MEMORIZATION_SUSPECT_CONDITION2 (false): Reasoning is anchored throughout in concrete provided data content (specific XBRL tag values with dates and accession numbers), not bare document lists. No mention of the SEC enforcement action, the AAER, the Revue-specific revelation, or any fact public only after the cutoff; the Q3 FY2013 goodwill impairment and 2013-01-24 8-K are within the provided …
- 오류 귀속 (1차): — (본 분석 오류 단위 아님)
- **서명**: ☐ finalize   ☐ override (사유: ______________________ → overrides.md 기록)

## case_04 = General Mills, Inc. (GIS, C08) — 본 분석 채점

- 피평가자: **p=25** · tier=watch · 가설 (확신 순):
  1. [overstated] Goodwill, IntangibleAssetsNetExcludingGoodwill, ReceivablesNetCurrent, InventoryNet — Large step-changes in goodwill, intangibles, receivables and inventory coincide with the Blue Buffalo acquisition (closed FY2018, evidenced by Assets jumping from 22,240,600,000 (2018-02-25) to 30,624,000,000 …
  2. [understated] AllowanceForDoubtfulAccountsReceivableCurrent, ReceivablesNetCurrent, SellingGeneralAndAdministrativeExpense — A one-year decline in the bad-debt allowance (FY2016 to FY2017) while gross receivables grew could indicate under-provisioning of doubtful-account reserves, modestly understating bad-debt expense and overstating net …
- 채점 (claude-fable-5): **d1=2** · d2=None · d3=None/None · d4=3 · mem2=F
- 채점 rationale 발췌 (≤5줄):
> Control case (answer key: T28 KHC control, SIC 2040, rev=15,740,400,000, FYE 0530 — matches output's cited GIS FY2018 figures).
> dim1: output gives misstatement_probability=25; control band p<=30 -> 2.
> dim2/dim3: control -> null per rubric.
> dim4: consistency rule satisfied (p=25 <40 with tier 'watch', allowed clear/watch — no cap). Evidence is specific and multi-point/multi-year: goodwill 8,747.2M->14,065M and intangibles 4,530.4M->7,445.1M vs revenue +0.8% (15,619.8M->15,740.4M), NI-vs-OCF comparisons for FY2015 and FY2018 (1,221.3M vs 2,542.8M; 2,131M vs 2,841M), allowance decline 29.6M->24.3M against receivables growth …
- **A2 교차 채점 (claude-opus-4-8, SPOT-CHECK)**: 일치 (opus: d1=2 d2=None d3=None d4=3)
- 오류 귀속 (1차): — (본 분석 오류 단위 아님)
- **서명**: ☐ finalize   ☐ override (사유: ______________________ → overrides.md 기록)

## case_05 = Perry Ellis International, Inc. (PERY, C05) — 본 분석 채점

- 피평가자: **p=48** · tier=watch · 가설 (확신 순):
  1. [overstated] AccountsReceivableNetCurrent, AllowanceForDoubtfulAccountsReceivableCurrent, Revenues/SalesRevenueNet — Potential aggressive revenue recognition / channel stuffing near period-end combined with an under-provisioned allowance for doubtful accounts, causing receivables to grow faster than sales in a declining-revenue …
  2. [overstated] InventoryNet, CostOfGoodsSold, GrossProfit — Inventory buildup outpacing declining sales suggests possible delayed markdown/obsolescence reserve recognition, which could overstate inventory value and understate cost of goods sold/inflate gross margin in the near …
  3. [timing_shift] Goodwill, IntangibleAssetsNetExcludingGoodwill, NetIncomeLoss — Large, sudden goodwill/intangible impairments recorded in FY2013 (rather than gradual amortization/earlier recognition) suggest previously overstated carrying values on these 'soft' assets that were later written down, …
- 채점 (claude-fable-5): **d1=1** · d2=None · d3=None/None · d4=3 · mem2=F
- 채점 rationale 발췌 (≤5줄):
> Control case (answer key: control match for T16 ICON, SIC 2320).
> Dim1: misstatement_probability=48 falls in the control band 30<p<50 -> 1 (not <=30, so not 2).
> Dim2/Dim3: null per rubric for control cases.
> Dim4: risk_tier='watch' is consistent with p=48 (40<=p<70 => watch/elevated), so no cap. Evidence is specific and verifiable: exact values with accession numbers and dates (e.g., AR 145,563,000 (2012-01-28) -> 174,484,000 (2013-02-02) from 0001193125-14-143835; SalesRevenueNet 955,549,000 FY2011 -> 942,451,000 FY2012; allowance/AR ratio 19.1%->14.8%->14.6%; NetIncomeLoss -22,779,000 vs CFO …
- 오류 귀속 (1차): — (본 분석 오류 단위 아님)
- **서명**: ☐ finalize   ☐ override (사유: ______________________ → overrides.md 기록)

## case_06 = Monsanto Company (MON, T07) — 부록(원본 실험군 — 상한 전용)

- 피평가자: **p=28** · tier=watch · 가설 (확신 순):
  - (가설 없음 — p<40)
- 채점 (claude-fable-5): **d1=0** · d2=0 · d3=None/0 · d4=3 · mem2=F
- 채점 rationale 발췌 (≤5줄):
> dim1=0: This is a treatment case (answer key: Monsanto rebate-cost deferral/misclassification, AAER-3741, FY2009-2011) but the output gives misstatement_probability=28, which falls in the p<50 band for treatment -> 0.
> dim2=0: mechanism_hypotheses is an empty list. Because p=28<40 a hypothesis was not strictly required by the rubric, but with no top-ranked hypothesis there is nothing that matches the enforcement-order mechanism (deferred rebate costs / rebates booked as SG&A instead of revenue reductions), so no credit above 0 can be given on a treatment case; null is reserved for control. Notably, CL4 did …
> dim3: no top-ranked hypothesis narrative exists to map, so mapped_genre=null and score=0 against the answer-key genre active(cost).
> dim4=3: evidence citations are specific, plausible XBRL data points with accessions and periods (e.g., AR 1,590M (2010-08-31) -> 2,377M (2011-02-28) vs allowance 143M -> 111M in CL6; FY2009 revenue 11,724M / gross profit 6,762M vs FY2010 10,502M / 5,086M in CL4; quarterly NI/OCF seasonality series in CL3/CL5), and the top_signals combine multi-year and multi-point trends coherently (allowance …
- 오류 귀속 (1차): — (본 분석 오류 단위 아님)
- **서명**: ☐ finalize   ☐ override (사유: ______________________ → overrides.md 기록)

## case_07 = Xilinx, Inc. (XLNX, C06) — 본 분석 채점

- 피평가자: **p=25** · tier=watch · 가설 (확신 순):
  - (가설 없음 — p<40)
- 채점 (claude-fable-5): **d1=2** · d2=None · d3=None/None · d4=3 · mem2=F
- 채점 rationale 발췌 (≤5줄):
> Answer key marks this as a CONTROL case (matched control for T17 MRVL; SIC 3674, no scheme).
> dim1: output gives misstatement_probability=25, which for a control case falls in the p<=30 band → 2.
> dim2: control case → null per rubric; note the output correctly provides an empty mechanism_hypotheses list, consistent with p=25 (no hypothesis required below 40).
> dim3: control case → nulls per rubric.
> dim4: consistency rule check — p=25 (<40) requires clear/watch; declared risk_tier='watch', so no cap. The evidence is specific and grounded in provided data: CL1 pairs exact revenue and AR values with accession numbers (e.g., SalesRevenueNet=2382531000 FY2014 vs AccountsReceivableNetCurrent=267833000, computing AR +16.9% vs revenue +9.9%); CL3 contrasts NetIncomeLoss=648216000 with operating …
- 오류 귀속 (1차): — (본 분석 오류 단위 아님)
- **서명**: ☐ finalize   ☐ override (사유: ______________________ → overrides.md 기록)

## case_08 = Hertz Global Holdings, Inc. (HTZ, T13) — 부록(원본 실험군 — 상한 전용)

- 피평가자: **p=78** · tier=elevated · 가설 (확신 순):
  1. [overstated] Goodwill, IntangibleAssetsNetExcludingGoodwill, Assets, Liabilities — Purchase price allocation / capitalization adjustments related to the Dollar Thrifty acquisition (closed Nov 2012) appear to have been substantially revised between the originally reported interim/annual figures and …
  2. [overstated] AccountsReceivableNet, Revenues — Receivables appear to have grown faster than revenue in 2011-2012 (potential overstatement/aggressive revenue-related receivable recognition or delayed write-offs), followed by an unusual sharp reversal in 2013 where …
  3. [timing_shift] Multiple - annual report line items generally — Recurring inability to file annual reports on time (three NT 10-K notifications across 2009, 2013, and 2014) combined with an unprecedented one-day-later 10-K/A amendment in March 2014 indicates a pattern of internal …
- 채점 (claude-fable-5): **d1=2** · d2=0 · d3=omission-estimate/2 · d4=2 · mem2=F
- 채점 rationale 발췌 (≤5줄):
> Dim1=2: treatment case, p=78 >= 70.
> Dim2=0: top-ranked hypothesis targets Goodwill/IntangibleAssets via Dollar Thrifty PPA/capitalization revisions; answer key (AAER-4012) pinpoints allowance/reserve estimation errors, expense timing, and extended rental-fleet holding periods lowering depreciation. Acquisition goodwill/intangibles are unrelated accounts to all three truth mechanisms, and the cited goodwill jump (454.7M -> 1,329.3M …
> Dim3=2: top narrative (PPA estimate revisions/corrections of capitalized balances) maps to omission-estimate, matching the key's omission-estimate genre exactly; auditor note - an 'active improper capitalization' reading would instead score 0.
> Dim4=2: evidence cites specific provided data (exact goodwill/intangible/AR/revenue values FY2011-2013, NT 10-K dates 2009/2013/2014, 10-K 2014-03-19 followed by 10-K/A 2014-03-20) that genuinely support an elevated-risk claim; risk_tier 'elevated' is consistent with p=78 (no cap). Not 3 because the multi-point combination is partly incoherent: the flagship goodwill/intangible signal is self- …
- 오류 귀속 (1차): — (본 분석 오류 단위 아님)
- **서명**: ☐ finalize   ☐ override (사유: ______________________ → overrides.md 기록)

## case_09 = Iconix Brand Group, Inc. (ICON, T16) — 부록(원본 실험군 — 상한 전용)

- 피평가자: **p=65** · tier=elevated · 가설 (확신 순):
  1. [overstated] Revenues, AccountsReceivableNetCurrent, DeferredRevenueCurrent — Acceleration/front-loading of licensing revenue recognition (e.g., recognizing minimum guaranteed royalties or upfront license fees before cash collection or before the earnings process is complete), evidenced by …
  2. [overstated] NetIncomeLoss, OperatingIncomeLoss, SellingGeneralAndAdministrativeExpense — Possible use of non-operating gains or deferral of expense recognition to sustain earnings/margins as core licensing revenue decelerated/declined, evidenced by net margin spiking to ~66% in Q1 2015 …
  3. [overstated] OtherAssetsNoncurrent, IntangibleAssetsNetExcludingGoodwill — Capitalization of costs (e.g., deferred transaction/licensing costs, capitalized items) onto the balance sheet at a pace far exceeding revenue growth, potentially deferring expense recognition rather than expensing …
- 채점 (claude-fable-5): **d1=1** · d2=1 · d3=active/1 · d4=3 · mem2=F
- 채점 rationale 발췌 (≤5줄):
> DIM1=1: Treatment case with misstatement_probability=65; 50<=65<70 -> 1.
> DIM2=1: Top-ranked hypothesis = overstated licensing Revenues via acceleration/front-loading of recognition (AR +30.8% vs revenue +6.6% FY2014; deferred revenue shrinking). Best-match truth axis is 'fabricated licensing revenue in 2014' (revenue_recognition): account area (licensing revenue) and direction (overstated) match, but treatment type (premature recognition of real royalties) does not …
> DIM3=1: Top-ranked narrative (actively pulling revenue forward) maps to 'active'; answer-key genre is 'mixed' (active(gains) 우세 + omission-estimate impairment axis). One-sided active vs mixed key -> 1. Auditor note: key's '채점 분해 시 active(gains) 우세' caveat could arguably justify 2, but the output's active narrative is revenue front-loading, not gains recognition, so the mechanical one-sided-vs- …
> DIM4=3: Evidence cites specific, dated provided data points with accession numbers (AR 90,777k->118,774k; Revenues 432,626k->461,243k; DeferredRevenueCurrent 29,126k->22,470k; OtherAssetsNoncurrent 24,082k->63,334k; Q1-2015 ~66% net margin on 18% revenue decline; annual 10-K/A amendments 2011-2015 and CORRESP/UPLOAD chronology) that genuinely support the claims and are combined coherently across …
- 오류 귀속 (1차): — (본 분석 오류 단위 아님)
- **서명**: ☐ finalize   ☐ override (사유: ______________________ → overrides.md 기록)

## case_10 = Ryder System, Inc. (R, C04) — 본 분석 채점

**⚑ SKEPTICAL-REVIEW (MODEL 귀속 1/5)**: 자기변호형이라면: 오탐(p=58, 대조군)을 '합리적 추론'으로 감싸 d4를 3으로 올렸을 것 — 채점자는 d4=2로 눌렀다. 역방향 심사 지점: 이 오탐의 귀속이 MODEL이 맞나? 모델이 과대 해석한 10-K/A 출처 연대기는 파이프라인의 point-in-time 재구성이 주입한 메타데이터다 — DATA(설계) 재귀속 논거도 성립. 귀속 플립 시 MODEL 5→4, DATA 1→2 (trust boundary 표의 방향은 불변).

- 피평가자: **p=58** · tier=elevated · 가설 (확신 순):
  1. [understated] Goodwill, IntangibleAssetsNetExcludingGoodwill, Assets, DebtAndCapitalLeaseObligations, NetIncomeLoss (quarterly 2010), PropertyPlantAndEquipmentGross/Net — A 10-K/A (accession 0001193125-12-121535) filed 2012-03-19, only ~1 month after the original FY2011 10-K, was used as the reporting source for a broad swath of FY2008-FY2011 balance sheet and income statement figures …
  2. [timing_shift] NetIncomeLoss, StockholdersEquity, Liabilities, Assets — Broad restatement of prior period financial statement line items across FY2008-FY2011 (evidenced by extensive re-sourcing of historical data to the 2012-03-19 10-K/A rather than original filings), suggesting a …
  3. [understated] AllowanceForDoubtfulAccountsReceivableCurrent, ReceivablesNetCurrent — Allowance for doubtful accounts as a percentage of gross receivables declined modestly over 2009-2013 despite receivables growth, potentially reflecting an under-provisioned bad debt reserve relative to a growing …
- 채점 (claude-fable-5): **d1=0** · d2=None · d3=None/None · d4=2 · mem2=F
- 채점 rationale 발췌 (≤5줄):
> Control case (answer key: control comp for T13 HTZ, SIC 7510, rev 6,419,285,000, FYE 1231).
> dim1=0: output p=58, which is >=50 on a control -> 0 per rubric (false positive on clean company).
> dim2=null and dim3=nulls: control case, mechanism/genre not graded.
> dim4=2: no consistency cap (p=58 with risk_tier 'elevated' satisfies 40<=p<70 => watch/elevated). Citations are specific and traceable to provided data: Revenues FY2011 6,050,534,000 vs FY2010 5,136,435,000 (+17.8%) vs receivables +22.7%; Goodwill 216,444,000 -> 355,842,000 (+64.4%) vs revenue +5.1%; allowance/receivables 2.31% -> 2.18%; NI 61,945,000 vs CFO 984,956,000 correctly attributed to …
- **A2 교차 채점 (claude-opus-4-8, SPOT-CHECK)**: 차이: d4 2→3 (opus: d1=0 d2=None d3=None d4=3)
- 오류 귀속 (1차): MODEL (d1 오탐 — 10-K/A 연대기 과대 해석)
- **서명**: ☐ finalize   ☐ override (사유: ______________________ → overrides.md 기록)

## case_11 = NuVasive, Inc. (NUVA, C02) — 본 분석 채점

- 피평가자: **p=45** · tier=watch · 가설 (확신 순):
  1. [understated] Allowance for doubtful accounts, Accounts receivable, net, Bad debt expense, Accrued liabilities — Potential under-reserving: allowance for doubtful accounts as a percentage of gross receivables fell from ~7.1% (2009) to ~3.1% (2012) even as receivables grew, and accrued liabilities fell in absolute terms (from …
  2. [timing_shift] Net income (loss), Operating cash flow, Litigation/legal accrual (other liabilities), Other income/expense — Large divergence between reported net income and operating cash flow (e.g., FY2011 net loss of -$69.85M vs positive operating cash flow of $62.97M; FY2012 net income of only $3.14M vs operating cash flow of $130.08M) …
  3. [overstated] Net income (quarterly), Other/non-operating income, Goodwill, Other noncurrent assets — Unusually large one-time swings in quarterly net income (a $61.93M spike in Q4 2010 versus normal quarterly income in the low single-digit millions, followed by a -$67.55M loss in Q3 2011) not proportionate to revenue …
- 채점 (claude-fable-5): **d1=1** · d2=None · d3=None/None · d4=3 · mem2=F
- 채점 rationale 발췌 (≤5줄):
> Dim1: Answer key group=control; output p=45 falls in 30<p<50 control band -> 1 (not <=30, so misses top score).
> Dim2/Dim3: control case -> null per rubric.
> Dim4: consistency rule satisfied (p=45 with risk_tier=watch, in [40,70) => watch/elevated allowed; no cap). Evidence is specific and verifiably drawn from provided data: FY2012 SalesRevenueGoodsNet=620,255,000 exactly matches the answer key's point-in-time rev=620255000, supporting authenticity. Claims are backed by coherent multi-year, multi-point combinations: allowance/AR ratio decline 7.1% …
- 오류 귀속 (1차): — (본 분석 오류 단위 아님)
- **서명**: ☐ finalize   ☐ override (사유: ______________________ → overrides.md 기록)

## case_12 = The Kraft Heinz Company (KHC, T28) — 부록(원본 실험군 — 상한 전용)

- 피평가자: **p=68** · tier=elevated · 가설 (확신 순):
  1. [overstated] AccountsReceivableNetCurrent, Revenues, AllowanceForDoubtfulAccountsReceivableCurrent — Potential premature revenue recognition, extended customer payment terms, or use of receivables factoring/securitization not matched by a corresponding rise in bad-debt reserves, causing accounts receivable to grow far …
  2. [understated] AllowanceForDoubtfulAccountsReceivableCurrent, AccountsReceivableNetCurrent — Reserve coverage ratio for doubtful accounts declined from ~3.7% to ~2.6% of gross receivables between early and late 2016, and no further allowance disclosure accompanies the much larger 2018 receivables balances, …
  3. [timing_shift] NetIncomeLoss, NetCashProvidedByUsedInOperatingActivities, IncomeTaxExpenseBenefit (implied) — A large non-cash deferred tax remeasurement benefit (consistent with U.S. tax reform) drove Q4 2017 net income to $8.0B, pushing FY2017 net income to $10.999B even as operating cash flow fell to $527M from $2.649B in …
- 채점 (claude-fable-5): **d1=1** · d2=0 · d3=mixed/1 · d4=3 · mem2=F
- 채점 rationale 발췌 (≤5줄):
> Dim1: Treatment case; p=68 falls in 50<=p<70 band -> 1.
> Dim2: Answer key (AAER-4248) specifies a procurement 'expense management' scheme understating COGS via premature recognition of unearned supplier discounts/rebates (prebate/clawback/price-phasing) and false supplier contracts. The TOP-RANKED hypothesis instead alleges premature REVENUE recognition/receivables factoring affecting AccountsReceivableNetCurrent, Revenues, and …
> Dim3: Key genre = active(cost). Top hypothesis narrative blends active elements (premature revenue recognition, factoring transactions) with omission-estimate elements (bad-debt reserves 'not matched by a corresponding rise', allowance among affected items) -> mapped 'mixed'; mixed vs one-sided active -> 1.
> Dim4: Evidence is specific and multi-point: AR 1,044M->1,950M->2,032M across 2018 10-Qs (0001637459-18-000099/-116/-124) vs ~6% revenue growth; FY2017 NI $10.999B vs CFO $527M vs FY2016 CFO $2.649B (0001637459-18-000015); allowance 32M->20M in 2016 (0001637459-17-000007); same-day 10-Q/A x2 plus Q3 2017 10-Q chronology (0001637459-17-000116/117/118); CL8 flags the dual-basis 2014 year-end (8-K …
- 오류 귀속 (1차): — (본 분석 오류 단위 아님)
- **서명**: ☐ finalize   ☐ override (사유: ______________________ → overrides.md 기록)

## case_13 = Marvell Technology Group, Ltd. (MRVL, T17) — 부록(원본 실험군 — 상한 전용)

- 피평가자: **p=55** · tier=watch · 가설 (확신 순):
  1. [understated] GeneralAndAdministrativeExpense, StockholdersEquity, NetIncomeLoss (historical periods) — Improper stock option grant-date/exercise-price accounting (backdating-type issue) requiring restatement, evidenced by a cluster of NT 10-Q, NT 10-Q/A, NT 10-K delinquency notices (2006-2007) and a 10-K/A and 10-Q/A …
  2. [overstated] AccountsReceivableNetCurrent, InventoryNet, Revenues — Possible premature revenue recognition, extended payment terms, or channel stuffing near FY2013 (fiscal year ended 2014-02-01), where receivables and inventory grew far faster than revenue, consistent with pulling …
  3. [overstated] AllowanceForDoubtfulAccountsReceivableCurrent, AccountsReceivableNetCurrent, Bad debt expense (not separately reported) — Under-reserving for doubtful accounts as receivable allowance fell 63.9% (from $7.37M to $2.66M) while gross receivables declined only modestly, potentially overstating net receivables/net income in FY2011-FY2012
- 채점 (claude-fable-5): **d1=1** · d2=0 · d3=active/2 · d4=3 · mem2=F
- 채점 rationale 발췌 (≤5줄):
> DIM1=1: Treatment case; output gives misstatement_probability=55, which falls in 50<=p<70 band.
> DIM2=0: Rubric grades TOP-RANKED hypothesis only. Top hypothesis is stock-option backdating affecting GeneralAndAdministrativeExpense/StockholdersEquity with understated direction, tied to 2006-2007 NT filings and a 2009 G&A spike — unrelated accounts vs. the answer key's pull-in revenue-acceleration scheme (revenue recognition + nondisclosure, period 2014-11~2015-05). Coverage note for auditor: …
> DIM3=2: Top-ranked narrative (backdating/misdating option grants requiring restatement) is active manipulation of accounting inputs → mapped 'active'; answer-key genre_tag_row is active(revenue) → exact genre match despite wrong account area (dim3 is genre-only).
> DIM4=3: Consistency rule satisfied (p=55 with risk_tier='watch', watch/elevated required — no cap). Evidence cites specific provided data points that genuinely support claims: AR 330,238k(2013-02-02)→453,496k(2014-02-01) +37.3% vs revenue +7.4%; InventoryNet +38.9%; allowance 7,366k→2,663k (-63.9%) vs modest AR decline; NT 10-Q/NT 10-K/amendment cluster 2006-2007 from filing_chronology; G&A …
- 오류 귀속 (1차): — (본 분석 오류 단위 아님)
- **서명**: ☐ finalize   ☐ override (사유: ______________________ → overrides.md 기록)

## case_14 = Garmin Ltd. (GRMN, C03) — 본 분석 채점

- 피평가자: **p=32** · tier=watch · 가설 (확신 순):
  - (가설 없음 — p<40)
- 채점 (claude-fable-5): **d1=1** · d2=None · d3=None/None · d4=3 · mem2=F
- 채점 rationale 발췌 (≤5줄):
> CONTROL case (answer key: control for T12 LOGI, SIC 3812, FYE 1226, rev=2715675000).
> dim1: output gives misstatement_probability=32; control band 30<p<50 → 1 (misses the p<=30 band for a 2 by a small margin).
> dim2: control case → null per rubric; note the output correctly provides an empty mechanism_hypotheses list, which is appropriate for p=32 (<40, no hypothesis required).
> dim3: control → nulls.
> dim4: evidence is specific and genuinely tied to provided data — e.g., CL6 cites a coherent multi-year warranty accrual decline (87424000 FY2009 → 37301000 FY2012) against stable revenue in the 2.7–2.9B range; CL3 cites NI vs OCF for FY2009 and FY2012; CL4 combines inventory, revenue, and gross-margin points across FY2009–FY2012; the cited FY2012 revenue (2715675000) exactly matches the answer …
- 오류 귀속 (1차): — (본 분석 오류 단위 아님)
- **서명**: ☐ finalize   ☐ override (사유: ______________________ → overrides.md 기록)

## case_15 = Forrester Research, Inc. (FORR, C07) — 본 분석 채점

- 피평가자: **p=22** · tier=watch · 가설 (확신 순):
  - (가설 없음 — p<40)
- 채점 (claude-fable-5): **d1=2** · d2=None · d3=None/None · d4=3 · mem2=F
- 채점 rationale 발췌 (≤5줄):
> Dim1: Answer key group=control; output misstatement_probability=22, which satisfies p<=30 -> 2.
> Dim2: control case -> null per rubric (output correctly lists no mechanism hypotheses).
> Dim3: control -> nulls.
> Dim4: Consistency check passes (p=22 <40 with risk_tier='watch', within clear/watch band, so no cap at 1). Evidence is specific and data-grounded: CL1 cites AR 73,574k (2010-12-31) vs 67,429k (2014-12-31) against revenue 250,726k (2010) vs 312,062k (2014), showing AR shrinking while revenue grew; CL3 cites paired NI/OCF figures for 2009 (18,866k vs 43,099k) and 2014 (10,865k vs 28,795k); CL5 …
- 오류 귀속 (1차): — (본 분석 오류 단위 아님)
- **서명**: ☐ finalize   ☐ override (사유: ______________________ → overrides.md 기록)

## case_16 = The Mosaic Company (MOS, C01) — 본 분석 채점

- 피평가자: **p=30** · tier=watch · 가설 (확신 순):
  - (가설 없음 — p<40)
- 채점 (claude-fable-5): **d1=2** · d2=None · d3=None/None · d4=3 · mem2=F
- 채점 rationale 발췌 (≤5줄):
> CONTROL case (answer key: control match for T07 MON, SIC 2870, assets 14,699,100,000 — the output's cited Assets=14699100000 at 2011-02-28 confirms case identity).
> dim1=2: misstatement_probability=30, and for controls p<=30 earns 2 (30 is exactly at the band edge, inclusive per rubric 'p<=30').
> dim2=null and dim3=nulls: per rubric these are treatment-only dimensions; the output correctly submits an empty mechanism_hypotheses list, so there is no top-ranked hypothesis to grade and nothing to map.
> dim4=3: citations point at concrete, verifiable provided data points that arithmetically support the claims — e.g., CL1 receivables 651.0M→777.9M (+19.5%) vs revenue 2674.8M→2214.3M (-17.2%) between the Nov-2010 and Feb-2011 10-Qs; CL4 gross margin computed correctly (504.7/2188.3≈23.1%, 853.6/2214.3≈38.5%) with a three-point inventory series (1045.3M→816.9M→1133.6M); CL5 assembles a six-quarter …
- 오류 귀속 (1차): — (본 분석 오류 단위 아님)
- **서명**: ☐ finalize   ☐ override (사유: ______________________ → overrides.md 기록)

## case_01 = Comscore, Inc. (SCOR, T21) — 본 분석 채점 · 교란 변형

**⚑ SKEPTICAL-REVIEW (MODEL 귀속 2/5)**: 자기변호형 채점이라면: p=45를 '밴드 경계 5pp 미달일 뿐 기제는 맞췄다'로 서술해 d1=0의 무게를 희석하고, barter/사이드 계약(정답 특이 기제)과 'channel stuffing' 일반론의 불일치를 d2=1이 아니라 2로 올려 적었을 것 — 검증 지점: AAER-4091의 비화폐 데이터 교환 문언 vs 가설 문언 직접 대조.

- 피평가자: **p=45** · tier=watch · 가설 (확신 순):
  1. [overstated] AccountsReceivableNetCurrent, Revenues — Potential premature or aggressive revenue recognition (or extended payment terms) in FY2013, evidenced by accounts receivable growing ~32% year-over-year while revenue grew only ~12% over the same period, and a …
  2. [understated] AllowanceForDoubtfulAccountsReceivableCurrent, AccountsReceivableNetCurrent, NetIncomeLoss — Under-reserving for doubtful accounts: the allowance for doubtful accounts was reported as exactly $0 at two separate quarter-ends (Q1 2015 and Q3 2015) despite accounts receivable balances of roughly $96-103 million, …
  3. [understated] NetIncomeLoss, OperatingIncomeLoss, NetCashProvidedByUsedInOperatingActivities — Persistent and widening divergence between reported net losses and strongly positive, growing operating cash flow (gap grew from roughly $52M in 2011 to over $70M in 2014) raises the possibility that operating expenses …
- 채점 (claude-fable-5): **d1=0** · d2=1 · d3=active/2 · d4=3 · mem2=F
- 채점 rationale 발췌 (≤5줄):
> DIM1 (treatment, p=45): Answer key marks this a treatment case (SEC Order 33-10692/AAER-4091, revenue overstated ~$50M). Output's misstatement_probability=45 < 50, so per treatment banding p<50 -> 0.
> DIM2 (top-ranked hypothesis only): Top hypothesis targets ["AccountsReceivableNetCurrent","Revenues"], direction "overstated", treatment "premature or aggressive revenue recognition... channel stuffing, bill-and-hold arrangements, or extended payment terms." Account area (revenue) and direction (overstated) match the key's revenue_recognition/overstatement scheme, but the treatment type does not …
> DIM3: Top hypothesis narrative (premature/aggressive revenue recognition, channel stuffing, bill-and-hold) is an active fabrication/inflation scheme -> maps to "active". Answer-key genre tag row: "active(revenue)". Exact match -> 2.
> DIM4: Evidence citations are specific provided data points with accession numbers and dates that genuinely support the claims: AR $84.6M (2012-12-31) vs $111.5M (2013-12-31) against revenue $315.9M -> $355.1M (~32% vs ~12% growth); allowance $2.57M (2014-12-31) dropping to $0.0 at 2015-03-31 and 2015-09-30 against $96-103M AR; NI/OCF divergence tracked across 2011, 2012, and 2014 (e.g., -$12.26M …
> MEMORIZATION_SUSPECT_CONDITION2: false. The reasoning points at concrete provided data content (specific XBRL values, period ends, accession numbers) rather than merely listing documents, and mentions no post-cutoff facts (no reference to the SEC order, restatement, revelation, or outcome).
- **A2 교차 채점 (claude-opus-4-8, SPOT-CHECK)**: 차이: d2 1→2 (opus: d1=0 d2=2 d3=2 d4=3)
- 오류 귀속 (1차): MODEL (d1 — 교란 p=45, 밴드 경계 5pp 미달; d2=1로 기제 영역은 식별)
- **서명**: ☐ finalize   ☐ override (사유: ______________________ → overrides.md 기록)

## case_02 = Orthofix International N.V. (OFIX, T11) — 본 분석 채점 · 교란 변형

**⚑ SKEPTICAL-REVIEW (MODEL 귀속 3/5)**: 자기변호형이라면: '기제 실질 일치(d2=2)'를 근거로 d1 실패를 보정 문제로 축소했을 것. 또한 d2=2 자체가 관대할 수 있다 — 'premature recognition' 일반론이 AAER-3845의 '반품 가능·조건부 유통사 매출' 특이 구조와 '실질 일치'인지가 심사 지점 (일치 아니면 d2=1로 강등).

- 피평가자: **p=45** · tier=watch · 가설 (확신 순):
  1. [overstated] AccountsReceivableNetCurrent, SalesRevenueNet, NetCashProvidedByUsedInOperatingActivitiesContinuingOperations — Potential premature or aggressive revenue recognition / extended customer credit terms: accounts receivable grew ~13% in FY2012 while revenue declined ~1.7% and operating cash flow (6.7M) fell far short of net income …
  2. [timing_shift] NetIncomeLoss, NetCashProvidedByUsedInOperatingActivitiesContinuingOperations — Non-cash charges/gains or working-capital timing differences causing a persistent inverse relationship between reported earnings and operating cash generation (loss year with strong cash flow in 2011, followed by a …
  3. [overstated] InventoryNet, GrossProfit, SalesRevenueNet — Possible under-provisioning for slow-moving/obsolete inventory or capitalization of costs into inventory, as inventory balances grew (and grew further into Q1 2013) even as revenue declined meaningfully year-over-year, …
- 채점 (claude-fable-5): **d1=0** · d2=2 · d3=active/2 · d4=3 · mem2=F
- 채점 rationale 발췌 (≤5줄):
> DIM1 (0): Treatment case; output gives misstatement_probability=45, which is <50, so per the treatment band rule (p>=70→2; 50<=p<70→1; p<50→0) it scores 0 despite the fraud being real.
> DIM2 (2): Top-ranked hypothesis targets SalesRevenueNet/AccountsReceivableNetCurrent with direction 'overstated' via 'premature or aggressive revenue recognition ... sales being booked ahead of cash collection.' Answer key (AAER-3845/33-10281) describes overstated distributor revenue via improper recognition on contingent/return-eligible sales — account area (revenue), direction (overstated), …
> DIM3 (2): Top hypothesis narrative (actively booking revenue prematurely, overstating revenue/AR) maps to 'active'; answer-key genre row is 'active(revenue)' — exact match → 2.
> DIM4 (3): Evidence cites concrete provided data points that genuinely support claims: AR 79.7M→90.2M (+13%) while revenue 282.2M→277.5M (-1.7%); NI vs OCF divergence in both FY2011 (-0.64M NI vs +38.9M OCF) and FY2012 (30.8M NI vs 6.7M OCF); inventory 53.3M→55.3M into Q1 2013 against -13.6% YoY Q1 revenue; goodwill inconsistency 107.9M vs 43.9M flagged with accession numbers. This is a coherent …
- **A2 교차 채점 (claude-opus-4-8, SPOT-CHECK)**: 일치 (opus: d1=0 d2=2 d3=2 d4=3)
- 오류 귀속 (1차): MODEL (d1 — d2=2인데 p=45: 기제를 맞추고도 과소 확신)
- **서명**: ☐ finalize   ☐ override (사유: ______________________ → overrides.md 기록)

## case_03 = Logitech International S.A. (LOGI, T12) — 본 분석 채점 · 교란 변형

**⚑ SKEPTICAL-REVIEW (MODEL 귀속 4/5)**: 자기변호형이라면: 3순위 가설(재고 +5.8% vs 매출 −2.0%)이 정답 기제를 커버함을 들어 d2를 올렸을 것 — 루브릭은 최상위 가설 전용이고 채점자는 이를 지켰는지, d4=3의 인용(InventoryNet 등)이 실제 페이로드 값인지 확인.

- 피평가자: **p=45** · tier=watch · 가설 (확신 순):
  1. [overstated] Goodwill, OperatingIncomeLoss, NetIncomeLoss, Assets — Goodwill carried at prior levels (~$610-625M) through FY2011 and most of FY2012 was suddenly written down by roughly $240M within a single quarter (Q3 FY2013), coinciding with a large operating loss. This pattern of an …
  2. [overstated] AccountsReceivableNetCurrent, AllowanceForDoubtfulAccountsReceivableCurrent, Bad debt expense (implied) — The allowance for doubtful accounts as a percentage of gross receivables declined steadily from roughly 3.0% (2010-03-31) to about 1.2% (2013-03-31), even during a period (FY2011) when receivables grew faster than …
  3. [overstated] InventoryNet, CostOfGoodsAndServicesSold — Inventory increased 5.8% (InventoryNet=313075520.85 at 2011-03-31 to InventoryNet=331201333.02 at 2012-03-31) while annual revenue declined 2.0% (SalesRevenueNet=2634347878.53 FY2011 to SalesRevenueNet=2582301668.08 …
- 채점 (claude-fable-5): **d1=0** · d2=1 · d3=omission-estimate/2 · d4=3 · mem2=F
- 채점 rationale 발췌 (≤5줄):
> DIM1 (0): Treatment case with misstatement_probability=45. Rubric: treatment p<50 -> 0. Mechanical.
> DIM2 (1): Top-ranked hypothesis is delayed goodwill/intangible impairment ("Goodwill carried at prior levels... suddenly written down by roughly $240M... Q3 FY2013... carrying values may have been overstated"). Answer key (AAER-3765): core scheme is delayed ~$30.7M LCM write-down of Revue set-top-box INVENTORY in FY11, plus understated warranty liabilities, failure to amortize acquired …
> DIM3 (2): Top hypothesis narrative = failure to take/timely record an impairment estimate (delayed write-down of carrying values) -> maps to omission-estimate. Answer key genre for T12/LOGI = omission-estimate. Exact match -> 2.
> DIM4 (3): Evidence quotes are concrete provided data points with values, dates, and accession numbers that genuinely support each claim: goodwill 625,540,084.32 (2012-09-30) -> 384,984,535.43 (2012-12-31) alongside OperatingIncomeLoss -200,698,384.12 in the same quarter; allowance coverage decline 6.54M/217.7M (2010) -> 2.40M/200.2M (2013); inventory 313.1M->331.2M vs revenue 2,634.3M->2,582.3M. …
> MEMORIZATION_SUSPECT_CONDITION2 (false): Reasoning is anchored throughout in concrete provided data content (specific XBRL-style values and periods), not bare document lists; no post-cutoff facts (no mention of SEC order, AAER, Revue by name, restatement outcome, or enforcement).
- **A2 교차 채점 (claude-opus-4-8, SPOT-CHECK)**: 일치 (opus: d1=0 d2=1 d3=2 d4=3)
- 오류 귀속 (1차): MODEL (d1 — 양 변형 놓침; 재고 신호 제공 실측, 모델은 goodwill 서사 선택)
- **서명**: ☐ finalize   ☐ override (사유: ______________________ → overrides.md 기록)

## case_06 = Monsanto Company (MON, T07) — 본 분석 채점 · 교란 변형

- 피평가자: **p=58** · tier=elevated · 가설 (확신 순):
  1. [overstated] AllowanceForDoubtfulAccountsReceivableCurrent, AccountsReceivableNetCurrent, NetIncomeLoss, SellingGeneralAndAdministrativeExpense — Under-reserving for bad debts: allowance for doubtful accounts declined steadily (AllowanceForDoubtfulAccountsReceivableCurrent=294103304.69 at 2007-08-31 to 150439939.27 at 2011-02-28) even as gross receivables grew …
  2. [overstated] AccountsReceivableNetCurrent, SalesRevenueNet, SalesRevenueGoodsNet — Receivables outpacing revenue and an unexplained AR spike (AccountsReceivableNetCurrent=4381732645.52 at 2010-05-31 versus 2836673809.8 at 2010-02-28 and 2154950481.41 at 2010-08-31, with no corresponding jump in …
  3. [timing_shift] CostOfGoodsSold, GrossProfit, SellingGeneralAndAdministrativeExpense — A large, hard-to-explain gross margin swing (57.7% FY2009 to 48.4% FY2010) occurring in the same window that the company filed 8-Ks recasting FY2007-2010 financial statements (immediately preceding a securities …
- 채점 (claude-fable-5): **d1=1** · d2=0 · d3=omission-estimate/0 · d4=3 · mem2=F
- 채점 rationale 발췌 (≤5줄):
> dim1=1: treatment case with p=58, which falls in the 50<=p<70 band.
> dim2=0: top-ranked hypothesis is bad-debt under-reserving (AllowanceForDoubtfulAccountsReceivableCurrent vs AR growth); ground truth is deferred rebate-cost recognition (incl. side agreements) and rebates misclassified as SG&A rather than revenue reductions (AAER-3741). The doubtful-accounts allowance is not the correct account area for either truth mechanism (rebate accruals/revenue …
> dim3=0: top hypothesis maps to omission-estimate (reserve release/under-accrual); answer-key genre is active(cost); wrong genre.
> dim4=3: evidence quotes specific provided data points with values, accessions, and locations (allowance trend 2007-08-31 294.1M -> 2011-02-28 150.4M; AR 2.11B -> 3.22B; FY2009/FY2010 gross margin 57.7% vs 48.4%; 2010-05-31 AR spike 4.38B vs adjacent quarters; recast 8-Ks of 2011-04-08 followed by 424B5/FWP/424B2 on 2011-04-12/13), combined coherently across multiple years and statement lines. …
- 오류 귀속 (1차): DATA(설계) (d2 — 리베이트 부채가 AccruedLiabilitiesCurrent 집계에 매몰, J10 태그 분해능)
- **서명**: ☐ finalize   ☐ override (사유: ______________________ → overrides.md 기록)

## case_08 = Hertz Global Holdings, Inc. (HTZ, T13) — 본 분석 채점 · 교란 변형

- 피평가자: **p=55** · tier=elevated · 가설 (확신 순):
  1. [overstated] AccountsReceivableNet, Revenues — Potential premature/aggressive revenue recognition or delayed write-off of receivables in 2011-2012, evidenced by AR growing at roughly 2x the rate of revenue in consecutive years, followed by an abrupt reversal (AR …
  2. [overstated] Goodwill, IntangibleAssetsNetExcludingGoodwill, Assets — Purchase price allocation from a Q4-2012 acquisition (evidenced by concurrent SC TO-T tender offer filings) may have allocated disproportionate value to goodwill/intangibles relative to fair value, inflating total …
  3. [understated] NetIncomeLoss, NetCashProvidedByUsedInOperatingActivities, PropertyPlantAndEquipmentGross — Persistent and widening gap between reported net income and operating cash flow (OCF several multiples of NI in every period) is consistent with heavy non-cash D&A/interest add-backs or possible capitalization of costs …
- 채점 (claude-fable-5): **d1=1** · d2=1 · d3=mixed/1 · d4=3 · mem2=F
- 채점 rationale 발췌 (≤5줄):
> DIM1 (=1): Treatment case (HTZ, AAER-4012). Output gives misstatement_probability=55, which falls in the 50<=p<70 band -> 1.
> DIM2 (=1): Top-ranked hypothesis targets AccountsReceivableNet/Revenues, direction 'overstated', treatment 'premature/aggressive revenue recognition or delayed write-off of receivables'. Ground truth is understated allowance/reserve expenses via inappropriate estimation, expense-timing manipulation, and extended rental-fleet holding periods lowering depreciation. The 'delayed write-off of …
> DIM3 (mixed, =1): The top hypothesis narrative combines an active scheme (premature revenue recognition) with an omission/estimate scheme (delayed write-off of receivables), mapping to 'mixed'. Answer-key genre is 'omission-estimate' (management-estimate accounts, understated allowance expenses). Mixed vs one-sided omission-estimate -> 1.
> DIM4 (=3): Evidence cites specific provided data points with accession numbers and periods (e.g., AR +19.1% vs revenue +9.7% in 2011 from 0001445305-13-000446; AR +16.3% vs revenue +8.7% in 2012 and the 2013 AR reversal from 0001364479-14-000008; Goodwill 853.9M -> 2,496.5M in Q4-2012; NI vs OCF gaps for 2008/2009/2013), and these genuinely support the claims. The analysis coherently combines …
- 오류 귀속 (1차): — (본 분석 오류 단위 아님)
- **서명**: ☐ finalize   ☐ override (사유: ______________________ → overrides.md 기록)

## case_09 = Iconix Brand Group, Inc. (ICON, T16) — 본 분석 채점 · 교란 변형

- 피평가자: **p=55** · tier=elevated · 가설 (확신 순):
  1. [overstated] AccountsReceivableNetCurrent, Revenues — Potential premature/aggressive revenue recognition or extended customer payment terms causing receivables to build up faster than sales growth, which could mean revenue is recognized ahead of collectible cash or bad- …
  2. [overstated] IntangibleAssetsNetExcludingGoodwill, Goodwill, Assets, OperatingIncomeLoss — Large debt-funded acquisitions have built an intangible asset base (~853M at 2014-12-31) that is roughly 4.4x annual revenue (194M); if underlying acquired royalty/IP cash flows underperform, impairment charges may be …
  3. [timing_shift] LiabilitiesCurrent, LongTermDebtCurrent, LongTermDebtNoncurrent — Possible misclassification or technical covenant/maturity reclassification of long-term debt to current liabilities in a single quarter, later reversed, which could reflect either an accounting error, a covenant breach …
- 채점 (claude-fable-5): **d1=1** · d2=2 · d3=active/2 · d4=3 · mem2=F
- 채점 rationale 발췌 (≤5줄):
> DIM1=1: Treatment case, p=55 falls in 50<=p<70 band.
> DIM2=2: Top-ranked hypothesis names Revenues/AR overstated via 'premature/aggressive revenue recognition' with the 2014 AR-vs-revenue divergence (+30.9% vs +6.6%) — account (revenue), direction (overstated), and treatment type (improper revenue recognition inflating 2014 results) substantially match the enforcement description of fabricated 2014 licensing revenue; not a 3 because no case- …
> DIM3=2: Top hypothesis narrative (recognizing revenue ahead of collectible cash) maps to active; answer key tags mixed but explicitly directs scoring as active(gains)-dominant ('채점 분해 시 active(gains) 우세로 취급'), so active = exact match. If the auditor instead treats the key genre strictly as mixed, this would drop to 1 (one-sided-vs-mixed).
> DIM4=3: risk_tier 'elevated' is consistent with p=55 (40<=p<70 => watch/elevated), so no cap; evidence cites specific provided data points with accession numbers (AR 38.26M→50.06M vs Rev 182.3M→194.4M; intangibles 528.8M→853.3M with LTD 246.3M→626.4M; LiabilitiesCurrent spike 57.3M→308.5M→60.1M at 2014-06-30; 10-K/A every year 2010-2015 plus dense CORRESP/UPLOAD chronology) that genuinely …
- 오류 귀속 (1차): — (본 분석 오류 단위 아님)
- **서명**: ☐ finalize   ☐ override (사유: ______________________ → overrides.md 기록)

## case_12 = The Kraft Heinz Company (KHC, T28) — 본 분석 채점 · 교란 변형

**⚑ SKEPTICAL-REVIEW (MODEL 귀속 5/5)**: 자기변호형이라면: d3=2(장르 exact)를 전면에 세워 d2=0(계정 전혀 다름)을 가렸을 것. 심사 지점: 계정이 완전히 틀렸는데(revenue/AR vs COGS/리베이트) 장르 점수 2가 루브릭 3×3 표의 기계 적용인지 재확인 — 표상 맞음(active 서사).

- 피평가자: **p=68** · tier=elevated · 가설 (확신 순):
  1. [overstated] AccountsReceivableNetCurrent, Revenues/SalesRevenueGoodsNet — Possible premature revenue recognition, extended customer credit terms, or channel stuffing that inflates trade receivables well beyond the pace of reported net sales, potentially overstating revenue and/or …
  2. [overstated] NetIncomeLoss, NetCashProvidedByUsedInOperatingActivities — A large non-cash or one-time gain (e.g., deferred tax remeasurement, bargain-purchase gain, or other non-operating item tied to the fiscal-2017 period) appears to have driven reported net income far above cash …
  3. [understated] AllowanceForDoubtfulAccountsReceivableCurrent, AccountsReceivableNetCurrent — Reduction of the bad-debt/doubtful-accounts allowance (reserve release) during a period of receivables volatility could understate credit-loss reserves relative to receivable risk, inflating net receivables and net …
- 채점 (claude-fable-5): **d1=1** · d2=0 · d3=active/2 · d4=3 · mem2=F
- 채점 rationale 발췌 (≤5줄):
> Dim1=1: treatment case, output misstatement_probability=68, which falls in 50<=p<70 band.
> Dim2=0: top-ranked hypothesis names AccountsReceivableNetCurrent and Revenues/SalesRevenueGoodsNet with 'premature revenue recognition... or channel stuffing'; answer key (AAER-4248) describes a procurement expense-management scheme understating COST OF GOODS SOLD via prematurely recognized supplier discounts/rebates (prebate/clawback/price-phasing). Revenue/AR is an unrelated account area to …
> Dim3=2: top-ranked narrative (premature revenue recognition/channel stuffing) maps to 'active'; answer-key genre is active(cost) — exact match at the active/omission-estimate/mixed level, despite the wrong account.
> Dim4=3: evidence cites specific provided data points with accessions and values (e.g., AR 2,024,782,503 on 2018-03-31 vs 3,781,921,342 on 2018-06-30 against ~6% revenue growth; FY2017 NetIncomeLoss 21,331,975,819 vs OCF 1,022,088,486; two 10-Q/A amendments 0001637459-17-000116/-117 filed same day as 10-Q -118), which genuinely support the claims and are combined coherently across multiple years …
- **A2 교차 채점 (claude-opus-4-8, SPOT-CHECK)**: 일치 (opus: d1=1 d2=0 d3=2 d4=3)
- 오류 귀속 (1차): MODEL (d2 — GrossProfit/COGS 시계열 제공에도 AR 서사 선택)
- **서명**: ☐ finalize   ☐ override (사유: ______________________ → overrides.md 기록)

## case_13 = Marvell Technology Group, Ltd. (MRVL, T17) — 본 분석 채점 · 교란 변형

- 피평가자: **p=42** · tier=watch · 가설 (확신 순):
  1. [overstated] AllowanceForDoubtfulAccountsReceivableCurrent, AccountsReceivableNetCurrent, NetIncomeLoss (bad debt expense) — Disproportionate release/reduction of the allowance for doubtful accounts relative to the modest decline in gross receivables, potentially reducing bad debt expense and inflating net receivables and earnings in FY2011 …
  2. [overstated] InventoryNet, CostOfGoodsSold, GrossProfit — Inventory build-up outpacing revenue growth in periods of declining/compressing gross margin (FY2011 and FY2013) suggests possible delayed recognition of markdown/obsolescence reserves, temporarily overstating …
  3. [overstated] AccountsReceivableNetCurrent, Revenues — Receivables grew substantially faster than revenue in FY2009 (receivables +60.6% vs revenue -4.8%) and FY2013 (receivables +37.3% vs revenue +7.4%), consistent with either aggressive revenue recognition, extended …
- 채점 (claude-fable-5): **d1=0** · d2=0 · d3=omission-estimate/0 · d4=3 · mem2=F
- 채점 rationale 발췌 (≤5줄):
> dim1=0: Treatment case (answer key: MRVL undisclosed 'pull-in' revenue scheme per AAER-4076), but output gives misstatement_probability=42 (<50) -> 0 per treatment band.
> dim2=0: Top-ranked hypothesis is a disproportionate release of AllowanceForDoubtfulAccountsReceivableCurrent (17.93M -> 6.48M) reducing bad-debt expense in FY2011 (period ended 2012-01-28). Ground truth is revenue_recognition (acceleration of future-quarter sales into the current quarter) plus disclosure omission during 2014-11 to 2015-05. Reserve/allowance accounts are not the revenue account …
> dim3=0: Top-ranked narrative (allowance release / under-reserving = estimate manipulation) maps to omission-estimate; answer-key genre is active(revenue) (timing manipulation of real sales) -> wrong genre.
> dim4=3: Evidence quotes are specific provided data points that genuinely support each claim (allowance -64% vs AR -11.4% FY2011->FY2012; inventory +44.3% vs revenue -6.1% FY2010->FY2011; gross margin ~59.8% Q1 FY2010 vs ~48.4% Q1 FY2014; AR +60.6% vs revenue -4.8% FY2008->FY2009; NI vs OCF FY2010/FY2014; NT 10-Q/NT 10-K filings 2006-2007 from filing_chronology), and they are combined coherently …
- 오류 귀속 (1차): UNCLASSIFIED ×2 (d1·d2 — pull-in은 제공 집계 데이터에 발자국 없음, R3 전제 불성립)
- **[PROPOSAL — 소유자 결정 대상]** UNCLASSIFIED 2건(d1·d2)의 분류 제안: **DATA(설계)**. 근거 발췌: ① 정답 기제 = 분기 내 매출 가속(pull-in) + 공시 누락 (AAER-4076, 창 2015-01~07) — 분기 **집계** XBRL에는 분기 내부의 시점 이동이 원리적으로 나타나지 않는다 (스냅샷 해상도 한계). ② 채점 rationale 실측: '3순위 가설(FY2013 AR +37.3% vs 매출 +7.4%)이 진실 기제에 실질 근접'이나 그 신호는 조작 창보다 ~3년 앞선 기간의 것 — 창 내 신호가 입력에 존재하지 않았다는 방증. ③ MON d2의 DATA(설계) 선례(태그 분해능 한계)와 동형: 수집 버그가 아니라 입력 공간의 설계 한계. 대안(기각 사유 병기): MODEL — 'p=42로 40을 넘겼으니 신호를 봤다'는 논거가 있으나, 그 신호 자체가 창 밖 데이터라 '입력 충분' 전제(R3)를 회복시키지 못함.
- **서명**: ☐ finalize   ☐ override (사유: ______________________ → overrides.md 기록)

## case_90 = Valeant Pharmaceuticals International, Inc. (VRX, 파일럿 T18) — 파일럿 (본 분석 비산입 — J19 호출 회계용)

- 피평가자: **p=60** · tier=elevated · 가설 (확신 순):
  1. [overstated] Revenues, AccountsReceivableNetCurrent, ReceivablesNetCurrent, AllowanceForDoubtfulAccountsReceivableCurrent — Revenue recognized on shipments to distributors/pharmacies with extended payment terms or rights of return, growing receivables faster than sales (AR growth ~60-83% vs revenue growth ~43-66% in 2012-2013) while the …
  2. [overstated] Goodwill, IntangibleAssetsNetExcludingGoodwill, Assets, OperatingIncomeLoss, NetIncomeLoss — Aggressive purchase price allocation in serial debt-funded acquisitions (Medicis, Bausch & Lomb, Salix) directing disproportionate value to goodwill/indefinite-lived intangibles rather than amortizable/depreciable …
  3. [timing_shift] NetIncomeLoss, OperatingIncomeLoss, NetCashProvidedByUsedInOperatingActivities, DepreciationAndAmortization — Heavy non-cash charges (D&A, in-process R&D write-offs, restructuring, contingent consideration remeasurement) tied to acquisition accounting drove large GAAP net losses in 2012-2013 even as operating cash flow grew …
- 채점 (claude-fable-5): **d1=1** · d2=2 · d3=active/2 · d4=3 · mem2=F
- 채점 rationale 발췌 (≤5줄):
> DIM1=1: Treatment case, misstatement_probability=60 falls in 50<=p<70 band.
> DIM2=2: Top-ranked hypothesis affects Revenues/AR, direction=overstated, treatment='Revenue recognized on shipments to distributors/pharmacies with extended payment terms or rights of return' — account area, direction, and treatment type (premature revenue recognition on shipments into a pharmacy channel) substantially match the AAER-4153 description of improper revenue recognition on sales to …
> DIM3=2: Top hypothesis narrative is active manipulation (overstated revenue via improper recognition timing) -> 'active'; answer-key genre tag is 'active(revenue)' (omission axis noted as subordinate) -> exact match.
> DIM4=3: All citations are concrete provided XBRL data points with accession numbers; arithmetic verifies (AR 913,835k vs 569,268k = +60.5% vs revenue +43.4% FY2012; allowance ratio 6,692/234,020≈2.9%... stated ~2.4% vs 12,485/(769,469+12,485)≈1.6%... stated ~1.35% — directionally correct decline; goodwill+intangibles 22,600.3M/27,970.8M≈81% and 40,382.8M/48,343.2M≈83.5%; NI -863.6M vs OCF …
- 오류 귀속 (1차): — (본 분석 오류 단위 아님)
- **서명**: ☐ finalize   ☐ override (사유: ______________________ → overrides.md 기록)

## case_91 = General Electric Company (GE, 파일럿 T25) — 파일럿 (본 분석 비산입 — J19 호출 회계용)

- 피평가자: **p=55** · tier=elevated · 가설 (확신 순):
  1. [timing_shift] NetIncomeLoss (quarterly), OperatingIncomeLoss, Revenues (timing) — Discretionary timing of gains (asset/business sales, insurance-related reserve releases, discrete tax benefits) concentrated in Q4 each year to smooth or boost annual results, a pattern long associated with GE's …
  2. [overstated] AccountsReceivableNetCurrent, InventoryNet, Revenues — Accounts receivable and inventory (working-capital 'soft' assets) grew far faster than revenue in FY2015, consistent with potential aggressive revenue recognition on long-term service/equipment contracts (percentage- …
  3. [overstated] Goodwill, IntangibleAssetsNetExcludingGoodwill, Assets — Large step-up in goodwill and acquired intangibles (largely Alstom-related) without commensurate revenue growth increases risk that acquired asset values are overstated or insufficiently tested for impairment, …
- 채점 (claude-fable-5): **d1=1** · d2=1 · d3=mixed/1 · d4=3 · mem2=F
- 채점 rationale 발췌 (≤5줄):
> DIM1=1: Treatment case with misstatement_probability=55, which falls in the 50<=p<70 band.
> DIM2=1: Top-ranked hypothesis is 'discretionary timing of gains (asset/business sales, insurance-related reserve releases, discrete tax benefits) concentrated in Q4' affecting NetIncomeLoss/OperatingIncomeLoss. Best match against the multi-mechanism truth is the reserves/estimate leg (LTC insurance reserves; Power profit growth from reductions in prior cost estimates). 'Insurance-related reserve …
> DIM3=1: Top hypothesis mixes real-transaction timing (asset/business sale gains = active) with estimate-driven income (reserve releases = omission-estimate), so mapped_genre=mixed; answer-key genre is omission-estimate, giving one-sided-vs-mixed = 1.
> DIM4=3: Evidence cites specific provided data points with accessions that genuinely support the claims (Q4 2010 NI 4,535M vs Q1-Q3 avg ~2,370M; Q4 2014 5,152M vs ~3,360M; Q4 2015 6,301M after Q1 -13,573M; FY2015 AR +16.3%/inventory +27.3% vs revenue +0.17%; FY2015 net loss -5,795M vs OCF +11,856M; goodwill +23%/intangibles +35%), and combines them coherently across multiple years and statement …
- 오류 귀속 (1차): — (본 분석 오류 단위 아님)
- **서명**: ☐ finalize   ☐ override (사유: ______________________ → overrides.md 기록)
