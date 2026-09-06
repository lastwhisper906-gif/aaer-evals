# atlas/case_72.md — Weis Markets, Inc. (WMK) — holdout treatment

Authored by Claude Code, pending human audit (D15). Analytical document under D106 ② — not a scored output. 본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).

## 1. CASE HEADER

| field | value |
|---|---|
| Case ID (anonymized frame) | case_72 |
| Cohort | holdout |
| Outcome class | FN-provisional (main frame, flag at score ≥50; score 32 < 50; ground truth provisional, see tier row) |
| Ground-truth tier | provisional-4.02/restatement — NOT AAER-confirmed; upgrade monitoring until 2030-02-20 (`analysis/LABEL_REPORT.md` §3, `analysis/label_tags_holdout.json`) |
| Frozen score | score 32 (`runs/holdout/scores/case_72.json`, run `original-case_72-r1`, risk_tier "watch") |
| Grade record | `scoring/grades_holdout/case_72.json` (human_finalized: true, finalized 2026-07-09 via RP-13 workbench; dim1=0, dim2=0, dim3 mapped_genre "omission-estimate" / score null, dim4=3, memorization_suspect_condition2: false) |

Company: Weis Markets, Inc., CIK 0000105418, cutoff 2026-02-19 (`data/evaluatee/cases_holdout.json`
case_72) — the day before the 2026-02-20 Item 4.02 8-K. Redraws as recorded:
`runs/holdout/mainscore_redraw/draw_{2,3,4,5}/case_72.json` = score 28 / 42 / 32 / 40 (all
risk_tier "watch"); draw-to-draw range across main + redraws is score 28–42, every draw below the
50 flag threshold — the miss is stable across draws, not draw noise. Primary remains the main draw.
`analysis/error_analysis_wave2_holdout.md` §3 verdict: "(ii-a)/(iv) 혼합: 연결 수준에 비해 비중대".

## 2. ACTUAL EVENT

Provisional tier — no AAER exists for this event; the anchor document is the restatement 8-K,
accession `0000105418-26-000009` (8-K, filed 2026-02-20, items "4.02"), verified in the sealed
EDGAR submissions chronology `~/aaer-data/WMK/edgar/CIK0000105418.json` (manifest-pinned,
`data/manifests/aaer_data_manifest.json`). `analysis/LABEL_REPORT.md` §1 tags the case **bigR**
(Item 4.02 non-reliance within revelation ±90d); `analysis/label_tags_holdout.json` case_72
records revelation_date 2026-02-20, no observations outside the neighborhood, cache snapshot
through 2026-06-04.

Restatement mechanism as registered (`data/candidates/candidates_holdout.json` case_72
scheme_summary): "8-K Item 4.02 (2026-02-20): whistleblower-triggered; meat-processing plant
inventory overstated up to ~$22M cumulative (FY2022-2025). G2 PROVISIONAL
(non-reliance/restatement event, NOT confirmed fraud)"; scheme_type "restatement_nonreliance;
inventory_overstatement". The sealed grade record concurs: "Answer key mechanism is inventory
overstatement (~$22M cumulative, FY2022-2025, meat-processing plant)";
`analysis/error_analysis_wave2_holdout.md` §3: "정답 키: 육가공 공장 재고 과대 ~$22M
누적(FY2022-25), 내부고발". GAAP topic area implicated by that summary: inventory valuation
(ASC 330 area); ASC-level mapping from the primary 8-K text itself: **insufficient sealed
evidence** (the 8-K body text is not sealed locally — see §9). The answer key's genre_tag_row is
null: per the grade record, "G2 PROVISIONAL, non-reliance/restatement event, not confirmed
fraud". Provisional caveat (LABEL_REPORT learning note): a 4.02 non-reliance declaration "과거
재무제표를 쓰지 말라는 회사 자신의 판정일 뿐, 의도성(fraud)도 집행 가능성도 확정하지 않는다"
— this entry alleges nothing beyond the company's own disclosure posture.

## 3. SIGNALS AVAILABLE PRE-CUTOFF

Cutoff 2026-02-19. Sealed basis: the deck entry `data/evaluatee/cases_holdout.json` case_72
carries exactly five identity fields (case_id, ticker, cik, company_name, cutoff_date); the
frozen output's documents_used spans 58 filings, 2011-08-04 through 2025-11-06. From the sealed
companyfacts `~/aaer-data/WMK/xbrl/CIK0000105418.json` and the frozen output's cited values
(spot re-verified):

- **As-filed consolidated inventory through the misstated period**: InventoryNet 293,274,000
  (2022-12-31, accn `0000105418-23-000008`) → 296,157,000 (2023-12-30, accn
  `0000105418-24-000015`) → 308,895,000 (2024-12-28, accn `0000105418-25-000014`) →
  323,375,000 (2025-09-27, accn `0000105418-25-000045`, 10-Q filed 2025-11-06 — the last filing
  in documents_used). Revenue over the same span was roughly flat:
  RevenueFromContractWithCustomerExcludingAssessedTax 4,713,986,000 (FY2022) → 4,714,573,000
  (FY2023) → 4,791,730,000 (FY2024) (all accn `0000105418-25-000014`). Per the registered
  mechanism (§2), the overstated amounts sat **inside** these reported balances; the sealed
  companyfacts carries inventory at consolidated level only (InventoryNet, LIFO-related tags) —
  no plant- or category-level disaggregation exists in the sealed data.
- **Receivables divergence** (the signal the model chased): AccountsReceivableNetCurrent
  50,863,000 (2022-12-31, accn `0000105418-23-000008`) → 65,092,000 (2023-12-30, accn
  `0000105418-24-000015`) → 81,567,000 (2024-12-28, accn `0000105418-25-000014`) against the
  flat revenue above.
- **Accrued liabilities decline**: AccruedLiabilitiesCurrent 57,431,000 (2022-12-31) →
  42,676,000 (2023-12-30) → 34,196,000 (2024-12-28) (same accessions as above).
- **NI vs OCF, unremarkable**: FY2022 NetIncomeLoss 125,196,000 vs OCF 218,024,000; FY2024
  109,941,000 vs 187,467,000 (accns `0000105418-23-000008`, `0000105418-25-000014`).
- **Filing chronology**: per the frozen output's filing_chronology quotes — NT 10-K notices
  dated 2014-03-14, 2015-03-13, 2016-03-10; NT 10-Q 2015-11-05; an 8-K/A dated 2025-02-10.

This section describes the information set — it does not re-score the case.

## 4. WHAT THE LLM CAUGHT

Frozen output `runs/holdout/scores/case_72.json`: `misstatement_probability`: 32 (legacy v1 key —
an uncalibrated ordinal score; see specs/RISK_SCORE_SEMANTICS.md) = score 32, risk_tier "watch" —
below the 50 threshold, hence the provisional-FN outcome. Checklist flags: CL1 (receivables vs
revenue), CL6 (liability/reserve decline), CL7 (filing-chronology, confidence low). CL4 examined
inventory directly and returned **no_flag**. Top signal (verbatim): "Accounts receivable grew
~28% (FY2022 to FY2023) and ~25% (FY2023 to FY2024) while revenue was roughly flat to
low-single-digit growth, indicating a widening receivables-to-revenue ratio (DSO rising from
~3.9 days in 2022 to ~6.2 days in 2024)."

| model claim (verbatim) | enforcement/restatement reference | match quality |
|---|---|---|
| Hypothesis 1: "Possible slower recognition of allowance for doubtful accounts or expansion of receivable-generating programs ... that outpaced core revenue growth, potentially inflating current assets relative to underlying sales activity in FY2023-FY2024" — AccountsReceivableNetCurrent/Revenues "overstated" | Registered mechanism (§2): meat-processing plant inventory overstated ~$22M cumulative FY2022-2025 — grade record: "an unrelated account area"; only the coarse direction (current assets overstated) coincides | unrelated |
| Hypothesis 2: accrued-liabilities decline "could reflect release or under-accrual of reserves ... that would modestly benefit reported net income" — AccruedLiabilitiesCurrent/NetIncomeLoss "understated" | Grade record: "Second hypothesis (accrued liabilities/NetIncomeLoss) also does not match; coverage of the true mechanism is zero" | unrelated |
| CL1 flag: AR 50,863,000 → 65,092,000 → 81,567,000 vs flat revenue | No counterpart in the registered restatement mechanism | unrelated |
| CL6 flag: AccruedLiabilitiesCurrent 57,431,000 → 34,196,000 decline vs growing revenue | No counterpart in the registered restatement mechanism | unrelated |
| CL7 flag (confidence low): "NT 10-K, filing_date=2014-03-14 / 2015-03-13 / 2016-03-10", "NT 10-Q, filing_date=2015-11-05", "8-K/A, filing_date=2025-02-10" | Generic restatement-propensity signal pointing at non-reliance risk in the abstract; no content about the 2026 mechanism, period, or account | right direction only |

The dim2=0 grade is the miss in numeric form: "Notably, CL4 examined inventory directly
(InventoryNet 293,274K in 2022 vs 308,895K in 2024) and returned no_flag, i.e., the true
mechanism's account was checked and cleared." dim1=0 (treatment case, score 32 < 50); dim4=3
(evidence cited to accessions and values verified above; consistency rule score-32/"watch"
satisfied — per the grade record, "dim4 grades evidence quality, not mechanism correctness").

## 5. WHAT THE LLM MISSED

The account was examined; the anomaly was not visible at the delivered altitude. Distinguishing
the two failure kinds within §3's sealed information set:

- **Signal not in the information set (dominant)**: the mechanism is plant-level — a single
  meat-processing facility, ~$22M cumulative over four fiscal years, whistleblower-triggered
  (§2). The sealed input contains consolidated InventoryNet only (§3); no pre-cutoff filing or
  XBRL tag in the sealed cache disaggregates inventory by plant, and the whistleblower channel
  is by nature outside the filing record. `analysis/error_analysis_wave2_holdout.md` §3: "단일
  육가공 공장의 4년 누적 $22M 과대는 **식료품 체인 연결 재고에서 비율 신호를 남기지 않음**
  (신호<잡음). 유형 (ii-a) 대체신호 추격 + (iv) 연결 수준 비중대성." Against a ~$293–323M
  consolidated balance and ~$4.7B revenue base, the annual increment sits below trend noise.
- **Under-weighted signal (secondary, judgment call)**: the as-filed series the model was given
  did contain a monotonic inventory build against flat revenue — 293,274,000 (FY2022) →
  308,895,000 (FY2024) → 323,375,000 (2025-09-27, accn `0000105418-25-000045`, in
  documents_used). CL4 compared only the FY2022 and FY2024 endpoints and returned no_flag; the
  frozen output nowhere cites a 2025 interim inventory value, so the most recent leg of the
  build (308,895,000 → 323,375,000 in nine months) went unexamined. Whether that leg constitutes
  a flag-worthy signal or ordinary grocery-chain seasonality is not decidable from sealed
  evidence alone — flagged for owner judgment in §7. No sealed artifact demonstrates any other
  pre-cutoff trace of the registered mechanism.

## 6. ERROR TAXONOMY

Per `scoring/error_taxonomy.md` (R1→R2→R3), atlas vocabulary:

- **R1 (DATA-first)**: the answer-key signal (plant-level inventory overstatement) was not
  present in the delivered data as a distinguishable anomaly, and that absence is a fact of the
  world (public filings do not disaggregate inventory by facility), not a collection/build
  defect — so R1 does not assign DATA; proceed. R2: dim1/dim2 anchors applied mechanically; no
  criteria ambiguity identified. R3: to the extent an attributable reasoning error exists, it is
  **interpretation** — chasing the AR/DSO divergence as the top hypothesis while clearing the
  true account on a two-endpoint comparison (§5). The sealed analysis classifies the miss as a
  mix: "(ii-a) 대체신호 추격 + (iv) 연결 수준 비중대성" — the (iv) component is structural
  (below signal floor at consolidated altitude), which caps how much of this FN is a model
  error at all.
- **Computation / retrieval**: none identified — dim4=3; cited accessions and values re-verified
  against sealed companyfacts (§3).
- **Label-noise**: inherent to the tier — provisional-4.02/restatement, not AAER-confirmed;
  LABEL_REPORT §2 records the base-rate caveat and §3 the symmetric upgrade/expiry protocol
  (monitoring until 2030-02-20). Not an error in this entry, a known uncertainty of the label.
- **Suspected-memorization**: no. `analysis/gate_k5_results.json` WMK: draws_knows_event
  [false ×5], band_true_of_5 = 0, verdict "ELIGIBLE" (positive control HTZ knows_event true).
  Main draw `runs/holdout/recognition/WMK.json`: knows_event false, confidence "none" — "I have
  no knowledge of Weis Markets, Inc. (WMK) ever having announced an accounting restatement";
  draws 2–5 `runs/holdout/recognition_k5/draw_{2,3,4,5}/WMK.json`: knows_event false, confidence
  "low" each. Grade memorization_suspect_condition2: false — "no post-cutoff facts
  (whistleblower, 8-K Item 4.02, restatement, plant) appear anywhere in the output".

## 7. CPA JUDGMENT — human_finalized: false

Draft, unaudited work product until owner sign-off (PROJECT.md §7).

- This FN is best read as an altitude problem, not an attention problem: the model looked at the
  right account (CL4) and answered the question the checklist asks — is consolidated inventory
  out of line with revenue? — defensibly in the negative. A localized overstatement accreting
  ~$22M across four years inside a ~$300M consolidated balance is the kind of misstatement
  ratio screening at issuer level is structurally poor at surfacing; detection realistically
  requires disaggregated data (plant/category margins) or a non-financial channel (the
  whistleblower that in fact triggered the 4.02). **[OWNER REVIEW]**
- The residual model-attributable question is the 2025 interim leg (308,895,000 → 323,375,000)
  that CL4's two-endpoint comparison skipped (§5). Had the model cited it, the honest reading is
  still "watch," not "flag": a ~4.7% nine-month build in a perishables-heavy retailer is weak
  evidence. Whether checklist wording should force most-recent-interim comparison is a pipeline
  design question, not a re-score. **[OWNER REVIEW]**
- The two hypotheses the model did rank (AR/allowance; accrual releases) are internally coherent
  readings of real series movements — consistent with the wave-level finding that this
  pipeline's failures are "과잉해석" of genuine data, not fabrication
  (`analysis/error_analysis_wave2_holdout.md` §5). But coherence on the wrong account produced
  zero coverage of the true mechanism (dim2=0). **[OWNER REVIEW]**
- Score stability (28–42 across five draws, all "watch", all sub-threshold) indicates the miss
  is driven by the information set, not sampling variance — consistent with classifying the
  dominant component as (iv) structural rather than a correctable near-miss. **[OWNER REVIEW]**

## 8. AUDIT TRANSLATION

Substantive procedures a watch-tier interest in this profile would motivate — procedures, not
conclusions:

- Physical inventory observation at individual facilities — including manufacturing/processing
  plants, not only distribution centers and stores — with independent test counts reconciled to
  perpetual records and book-to-physical adjustments reviewed for direction and recurrence.
- Standard-cost and overhead-absorption testing at processing facilities (yield assumptions,
  scrap/shrink factors, intercompany transfer pricing of plant output to stores).
- Gross-margin and inventory-turnover analytics disaggregated below the consolidated level (by
  facility, category, or supply-chain node) — the consolidated ratios in §3 are the wrong
  altitude for a localized misstatement.
- NRV and obsolescence testing for perishables; cutoff testing of receipts and plant-to-store
  transfers around period end.
- Journal-entry testing over inventory capitalization and top-side adjustments; review of
  whistleblower-hotline logs and their disposition (the registered mechanism's actual
  revelation channel).
- Given the model's own flags: receivables confirmation/subsequent-cash testing and search for
  unrecorded liabilities over the declining accrual balances — flagged series remain legitimate
  audit interest even though they were not this event's mechanism.

## 9. FINANCIAL STATEMENT IMPACT

Partially determinable from sealed source documents; the 8-K itself is not quotable. The Item
4.02 8-K `0000105418-26-000009` is sealed locally only at metadata level —
`~/aaer-data/WMK/edgar/CIK0000105418.json` records form, date, and items ("4.02"), but the 8-K
body text is not present under `~/aaer-data/WMK/` (manifest entries: one edgar JSON + one xbrl
JSON). No dollar impact is quoted from it, and no figures are estimated or computed here.

What the sealed companyfacts does record: the FY2025 10-K (accn `0000105418-26-000024`, filed
2026-03-12, post-cutoff, within the sealed cache) reports comparative figures **lower** than the
as-filed values at every overlapping date — direction consistent with the registered inventory
overstatement:

| line item | period end | as-filed (accn) | per FY2025 10-K `0000105418-26-000024` |
|---|---|---|---|
| InventoryNet | 2022-12-31 | 293,274,000 (`0000105418-23-000008`) | 285,792,000 |
| InventoryNet | 2023-12-30 | 296,157,000 (`0000105418-24-000015`) | 284,630,000 |
| InventoryNet | 2024-12-28 | 308,895,000 (`0000105418-25-000014`) | 292,037,000 |
| InventoryNet | 2025-09-27 | 323,375,000 (`0000105418-25-000045`) | 301,747,000 |
| NetIncomeLoss | FY2023 | 103,828,000 (`0000105418-24-000015`) | 100,854,000 |
| NetIncomeLoss | FY2024 | 109,941,000 (`0000105418-25-000014`) | 106,024,000 |
| GrossProfit | FY2024 | 1,204,079,000 (`0000105418-25-000014`) | 1,198,750,000 |

Direction: inventory, gross profit, and net income lower under the restated comparatives.
Attribution of these revisions to the 4.02 event specifically, and any per-period restatement
schedule, would require the 8-K/10-K narrative text: **not determinable** from sealed sources
beyond the paired values above.

---
*Entry status: drafted (sections 7–9 pending owner finalization).*
*채점: Claude 보조 + 인간 최종 확정. 교육·정보 목적, 투자 자문 아님.*
