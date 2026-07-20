# atlas/case_73.md — Genie Energy Ltd. (GNE) — holdout treatment

Authored by Claude Code, pending human audit (D15). Analytical document under D106 ② — not a scored output. 본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).

## 1. CASE HEADER

| field | value |
|---|---|
| Case ID (anonymized frame) | case_73 |
| Cohort | holdout |
| Outcome class | FN-provisional (main frame, flag at score ≥50; score 42 < 50; ground truth provisional, see tier row) |
| Ground-truth tier | provisional-4.02/restatement — NOT AAER-confirmed; upgrade monitoring until 2030-03-12 (`analysis/LABEL_REPORT.md` §3, `analysis/label_tags_holdout.json`) |
| Frozen score | score 42 (`runs/holdout/scores/case_73.json`, run `original-case_73-r1`, risk_tier "watch") |
| Grade record | `scoring/grades_holdout/case_73.json` (human_finalized: true, finalized 2026-07-09 via RP-13 workbench; dim1=0, dim2=0, dim3 mapped_genre "omission-estimate" / score null, dim4=3, memorization_suspect_condition2: false) |

Company: Genie Energy Ltd., CIK 0001528356, cutoff 2026-03-11 (`data/evaluatee/cases_holdout.json`
case_73) — the day before the 2026-03-12 Item 4.02 8-K. Redraws as recorded:
`runs/holdout/mainscore_redraw/draw_{2,3,4,5}/case_73.json` = score 32 / 30 / 32 / 38 (all
risk_tier "watch"); draw-to-draw range across main + redraws is score 30–42, every draw below the
50 flag threshold — the miss is stable across draws, not draw noise. Primary remains the main draw.
`analysis/error_analysis_wave2_holdout.md` §3 verdict: "(ii-a) 경계, error-like에 정합적 불확실
... 최경증".

## 2. ACTUAL EVENT

Provisional tier — no AAER exists for this event; the anchor document is the restatement 8-K,
accession `0001437749-26-007981` (8-K, filed 2026-03-12, items "4.02,9.01", reportDate
2026-03-09), verified in the sealed EDGAR submissions chronology
`~/aaer-data/GNE/edgar/CIK0001528356.json` (manifest-pinned,
`data/manifests/aaer_data_manifest.json`). `analysis/LABEL_REPORT.md` §1 tags the case **bigR**
(Item 4.02 non-reliance within revelation ±90d); `analysis/label_tags_holdout.json` case_73
records revelation_date 2026-03-12, neighborhood 2025-12-12 to 2026-06-10, cache snapshot through
2026-06-11 ("1일 마진" per LABEL_REPORT §1). One observation outside the neighborhood, not
hidden: an earlier 8-K dated 2017-11-02, accession `0001213900-17-011231`, items
"2.02,4.02,5.02,9.01" — per LABEL_REPORT §1 a "과거 별건" (separate past matter); tag unchanged.

Restatement mechanism as registered (`data/candidates/candidates_holdout.json` case_73
scheme_summary): "8-K Item 4.02 (2026-03-12): captive-insurance subsidiary liability accounting
error; FY2023-24 and prior quarters restated. G2 PROVISIONAL (non-reliance/restatement event,
error-like, NOT confirmed fraud)"; scheme_type "restatement_nonreliance;
liability_accounting_error". The sealed grade record concurs: "a captive-insurance subsidiary
LIABILITY accounting error affecting FY2023-24 and prior quarters (8-K Item 4.02, 2026-03-12)".
GAAP topic area implicated by that summary: insurance/claims liability measurement (ASC 944 /
ASC 450 area); ASC-level mapping from the primary 8-K text itself: **insufficient sealed
evidence** (the 8-K body text is not sealed locally — see §9). The answer key's genre_tag_row is
null: per the grade record, "G2 PROVISIONAL, error-like restatement, not confirmed fraud".
Provisional caveat (LABEL_REPORT learning note): a 4.02 non-reliance declaration "과거 재무제표를
쓰지 말라는 회사 자신의 판정일 뿐, 의도성(fraud)도 집행 가능성도 확정하지 않는다" — this entry
alleges nothing beyond the company's own disclosure posture.

## 3. SIGNALS AVAILABLE PRE-CUTOFF

Cutoff 2026-03-11. Sealed basis: the deck entry `data/evaluatee/cases_holdout.json` case_73
carries exactly five identity fields (case_id, ticker, cik, company_name, cutoff_date); the
frozen output's documents_used spans 58 filings, 2011-12-15 through 2025-11-06. From the sealed
companyfacts `~/aaer-data/GNE/xbrl/CIK0001528356.json` and the frozen output's cited values
(spot re-verified):

- **The account area later restated — captive-insurance liabilities — had a visible, tagged,
  fast-growing footprint in pre-cutoff filings**: AccruedInsuranceNoncurrent 44,945,000
  (2023-12-31, accn `0001213900-24-022573`) → 69,580,000 (2024-12-31, accn
  `0001213900-25-024009`), rising each quarter through 2024 (45,541,000 / 46,400,000 /
  47,271,000 at Q1–Q3, accns `0001213900-24-041190/-066525/-095312`); AccruedInsuranceCurrent
  143,000 (2023-12-31) → 9,120,000 (2024-12-31) (accn `0001213900-25-024009`);
  LiabilityForClaimsAndClaimsAdjustmentExpense 78,700,000 (2024-12-31) → 80,070,000
  (2025-09-30) per the 2025 10-Qs `0001437749-25-025334` / `0001437749-25-033534` — every
  accession named here appears in the frozen output's documents_used. The sealed companyfacts
  also carries insurer-style supplemental tags (PolicyholderBenefitsAndClaimsIncurredGross,
  GeneralInsuranceExpense) from those same 2025 10-Qs.
- **AR/allowance divergence (the signal the model chased)**:
  AllowanceForDoubtfulAccountsReceivableCurrent 6,139,000 (2021-12-31) → 4,826,000 (2022-12-31);
  AccountsReceivableNetCurrent 41,309,000 → 55,134,000 over the same year; Revenues 323,269,000
  (FY2021) vs 315,539,000 (FY2022) (accns `0001213900-23-020226`, `0001213900-24-022573`).
- **NI vs OCF and Q4 concentration**: FY2023 NetIncomeLoss 19,538,000 vs OCF 62,478,000; FY2024
  12,588,000 vs 70,742,000; OperatingIncomeLoss −34,175,000 (Q4 2023) and −20,797,000 (Q4 2024)
  (all accn `0001213900-25-024009`).
- **Filing chronology**: 10-Q/A dated 2017-11-16 (`0001213900-17-012239`), preceded by the
  2017-11-02 8-K with a 4.02 item (`0001213900-17-011231`, §2 — separate past matter); NT 10-K
  dated 2019-03-19 (`0001213900-19-004419`) filed the same day as the 10-K
  (`0001213900-19-004396`).

This section describes the information set — it does not re-score the case.

## 4. WHAT THE LLM CAUGHT

Frozen output `runs/holdout/scores/case_73.json`: `misstatement_probability`: 42 (legacy v1 key —
an uncalibrated ordinal score; see specs/RISK_SCORE_SEMANTICS.md) = score 42, risk_tier "watch" —
below the 50 threshold, hence the provisional-FN outcome. Checklist flags: CL1 (receivables vs
revenue), CL2 (soft-asset growth), CL3 (NI/OCF divergence), CL6 (allowance decline), CL7
(filing-chronology). The word "insurance" appears nowhere in the frozen output (grep count 0).

| model claim (verbatim) | enforcement/restatement reference | match quality |
|---|---|---|
| Hypothesis 1 (top-ranked): FY2022 allowance cut "consistent with under-reserving for bad debts during a year of unusually high reported net income ... would understate bad debt expense and overstate net income and receivable carrying values" — allowance/AR/bad debt, "overstated" | Registered mechanism (§2): captive-insurance subsidiary liability accounting error, FY2023-24 and prior quarters — grade record: "Allowance for doubtful accounts (a receivables contra-asset) is not the insurance-liability account area ... and the highlighted period (FY2022 anomaly) does not match FY2023-24 either — unrelated accounts → 0" | unrelated |
| Hypothesis 2: "If costs that should be expensed ... are instead being capitalized into 'other assets,' this would understate expenses and overstate assets/earnings" — OtherAssetsNoncurrent, "overstated" | No counterpart in the registered restatement mechanism | unrelated |
| Hypothesis 3: recurring Q4 operating losses "suggesting possible deferral of impairment, legal/regulatory reserve, or valuation adjustments to year-end 'catch-up' entries" — AccruedLiabilitiesCurrent, "timing_shift", 2023-2024 | Grade record coverage note: "the third-ranked hypothesis (AccruedLiabilitiesCurrent, Q4 reserve/catch-up timing in 2023-2024) is materially closer to the true liability-accounting error and period, but the rubric restricts scoring to the top-ranked hypothesis" — liability/reserve area and period overlap, mechanism content does not | right account wrong mechanism |
| CL7 flag: "{\"form\": \"10-Q/A\", \"filing_date\": \"2017-11-16\"}" and same-day NT 10-K/10-K in 2019 — "past reporting-process irregularities" | Generic restatement-propensity signal; the 2017 10-Q/A follows the 2017 4.02 event LABEL_REPORT classifies as a separate past matter — no content about the 2026 mechanism | right direction only |
| CL6 flag: allowance 6,139,000 → 4,826,000 vs AR 41,309,000 → 55,134,000 | No counterpart in the registered restatement mechanism | unrelated |

dim1=0 (treatment case, score 42 < 50); dim2=0 grades the top-ranked hypothesis only (grade
rationale above); dim4=3 — "Evidence is specific and genuine: exact XBRL-style values with dates
and accession numbers", values re-verified in §3; consistency rule satisfied per the grade record (score 42 with
risk_tier "watch", no cap applied).

## 5. WHAT THE LLM MISSED

The core distinction for this FN runs opposite to case_72 (WMK): here the true account area
**was in the sealed information set with dedicated tags**, and the frozen output never touched it.

- **Missed signal (dominant on sealed evidence)**: the captive-insurance liability complex was
  separately tagged and moving fast pre-cutoff — AccruedInsuranceNoncurrent up ~55% in FY2024
  (44,945,000 → 69,580,000), a current insurance accrual appearing at 9,120,000 from 143,000, and
  a 78,700,000 claims liability with insurer-style supplemental disclosures in the two most
  recent 10-Qs (§3). Every carrying accession is listed in documents_used, yet the frozen output
  contains zero references to any insurance tag or the word "insurance". Unlike WMK's plant-level
  inventory (no disaggregated tag existed), this signal had a distinguishable XBRL footprint at
  the delivered altitude.
- **Qualifier — payload inclusion is not itself sealed**: the sealed artifacts establish that the
  insurance tags exist in the companyfacts cache and that their source filings were in
  documents_used; no sealed artifact records whether the payload build delivered those specific
  tags to the evaluatee. If the build filtered them out, the miss migrates from model to DATA
  (§6). **[OWNER REVIEW — see §7]**
- **Directional aim of the checklist (structural component)**: the checklist battery screens for
  income-overstatement patterns — CL6 asks whether reserves *declined* despite growth. GNE's
  insurance reserves grew sharply, which under that lens reads as conservatism, not risk; and the
  restated comparatives in §9 move income *up*, i.e., the as-filed statements carried the error
  in the direction the screens are not aimed at. Whether a growing self-insurance accrual "should"
  have been flag-worthy under a direction-symmetric screen is not decidable from sealed evidence
  alone. Note the registered mechanism says "liability accounting error" without stating
  direction; the direction reading here rests only on the §9 paired values.
- No other pre-cutoff trace of the registered mechanism is identifiable from sealed evidence.

## 6. ERROR TAXONOMY

Per `scoring/error_taxonomy.md` (R1→R2→R3), atlas vocabulary:

- **R1 (DATA-first)**: the answer-key account area is present in the sealed companyfacts, sourced
  from filings within documents_used (§3) — so the absence-of-signal branch does not fire on
  sealed evidence. The one undetermined link is payload delivery of the insurance tags (§5); if
  the owner establishes a build-side filter, this reclassifies to DATA. R2: dim1/dim2 anchors
  applied mechanically; the grade record itself surfaces the borderline (hypothesis-3 coverage
  note) without finding rubric ambiguity. R3: on the current record the attributable component is
  **interpretation** — the model ranked an FY2022 receivables story over the liability/reserve
  story its own third hypothesis gestured at, and never examined the tagged insurance accrual.
  Sealed classification: "(ii-a) 경계" with the mitigation that score 42 "watch" is "error-like
  사건에 **정합적 불확실**(과확신 아님). 최경증" (`analysis/error_analysis_wave2_holdout.md` §3).
- **Computation / retrieval**: none identified — dim4=3; cited accessions and values re-verified
  against sealed companyfacts (§3).
- **Label-noise**: inherent to the tier — provisional-4.02/restatement, not AAER-confirmed;
  LABEL_REPORT §2 records the base-rate caveat and §3 the symmetric upgrade/expiry protocol
  (monitoring until 2030-03-12). Not an error in this entry, a known uncertainty of the label.
- **Suspected-memorization**: no. `analysis/gate_k5_results.json` GNE: draws_knows_event
  [false ×5], band_true_of_5 = 0, verdict "ELIGIBLE" (positive control HTZ knows_event true).
  Main draw `runs/holdout/recognition/GNE.json`: knows_event false, confidence "none" — "I have
  no specific knowledge of Genie Energy Ltd. (GNE) ever announcing an accounting restatement";
  draws 2–5 `runs/holdout/recognition_k5/draw_{2,3,4,5}/GNE.json`: knows_event false, confidence
  "low" each. Grade memorization_suspect_condition2: false — "nothing references post-cutoff
  facts — no mention of the 2026-03-12 Item 4.02 8-K, the captive-insurance subsidiary, the
  non-reliance determination, or any restatement of FY2023-24".

## 7. CPA JUDGMENT — human_finalized: false

Draft, unaudited work product until owner sign-off (PROJECT.md §7).

- Score 42 "watch" on an error-like, non-fraud restatement event is arguably the right ordinal
  posture wrongly binarized: the sealed analysis calls it "정합적 불확실(과확신 아님)" and the
  mildest of the misses. The FN label is a threshold artifact of the ≥50 frame; the redraw band
  (30–42, all "watch") shows the model consistently placing this issuer above control-typical
  levels but below flag. **[OWNER REVIEW]**
- The substantive miss is account selection, not evidence quality: a captive-insurance accrual
  growing ~55% in a year, with a new current-portion accrual and insurer-grade claim disclosures
  appearing in the latest 10-Qs, is exactly the estimate-heavy, management-judgment balance a
  reviewer should interrogate — and it went unexamined while three hypotheses were spent on
  receivables, capitalization, and generic Q4 catch-ups. Ranking, not detection bandwidth,
  produced dim2=0 (the third hypothesis was "materially closer" per the grade record).
  **[OWNER REVIEW]**
- The checklist's directional asymmetry deserves a design decision: every screen targets
  overstated earnings, so a liability-overstatement / income-understatement error (the direction
  the §9 paired values indicate) sits outside the battery's aim. Whether to add a
  direction-symmetric estimate-volatility screen is a pipeline question, not a re-score.
  **[OWNER REVIEW]**
- Open verification item for owner: confirm from build logs whether AccruedInsurance* /
  LiabilityForClaimsAndClaimsAdjustmentExpense tags were in the delivered payload; the §6
  classification (interpretation vs DATA) hinges on it. **[OWNER REVIEW]**

## 8. AUDIT TRANSLATION

Substantive procedures a watch-tier interest in this profile would motivate — procedures, not
conclusions:

- Actuarial specialist involvement over the captive subsidiary's loss reserves: independent
  recomputation or corridor testing of case reserves and IBNR, review of loss-development
  triangles and actuarial method/assumption changes period over period.
- Testing of the captive structure itself: retention levels, reinsurance/stop-loss contracts,
  premium-setting and intercompany eliminations between the captive and affiliated energy
  entities; completeness and accuracy of claims data feeding the reserve estimate.
- Roll-forward and retrospective review of AccruedInsuranceCurrent/Noncurrent and the claims
  liability: prior-year development (favorable/unfavorable), subsequent claim settlements versus
  the recorded balance, cutoff of claim incurrence around period end.
- Controls testing over the estimation process (management review controls, data transfers
  between claims administrators, the captive, and consolidation).
- Given the model's own flags: receivables confirmation and subsequent-cash testing over the
  allowance judgment; capitalization testing of additions to other noncurrent assets and PP&E;
  review of the composition and recurrence of Q4 adjustments — flagged series remain legitimate
  audit interest even though they were not this event's mechanism.

## 9. FINANCIAL STATEMENT IMPACT

Partially determinable from sealed source documents; the 8-K itself is not quotable. The Item
4.02 8-K `0001437749-26-007981` is sealed locally only at metadata level —
`~/aaer-data/GNE/edgar/CIK0001528356.json` records form, date, and items ("4.02,9.01"), but the
8-K body text is not present under `~/aaer-data/GNE/` (manifest entries: one edgar JSON + one
xbrl JSON). No dollar impact is quoted from it, and no figures are estimated or computed here.

What the sealed companyfacts does record: the FY2025 10-K (accn `0001437749-26-014294`, filed
2026-05-01, post-cutoff, within the sealed cache) reports comparative figures that differ from
the as-filed values at every overlapping period:

| line item | period | as-filed (accn) | per FY2025 10-K `0001437749-26-014294` |
|---|---|---|---|
| NetIncomeLoss | FY2023 | 19,538,000 (`0001213900-24-022573`) | 52,243,000 |
| NetIncomeLoss | FY2024 | 12,588,000 (`0001213900-25-024009`) | 35,509,000 |
| OperatingIncomeLoss | FY2023 | 10,009,000 (`0001213900-24-022573`) | 55,097,000 |
| OperatingIncomeLoss | FY2024 | 11,290,000 (`0001213900-25-024009`) | 44,902,000 |
| Liabilities | 2024-12-31 | 191,724,000 (`0001213900-25-024009`) | 134,666,000 |
| StockholdersEquity | 2024-12-31 | 190,508,000 (`0001213900-25-024009`) | 246,134,000 |
| RetainedEarningsAccumulatedDeficit | 2023-12-31 | 60,196,000 (`0001213900-24-022573`) | 92,901,000 |
| NetCashProvidedByUsedInOperatingActivities | FY2023 | 62,478,000 (`0001213900-24-022573`) | 62,478,000 (unchanged) |

Direction: total liabilities lower, and operating income, net income, retained earnings, and
equity higher under the restated comparatives; operating cash flow unchanged — consistent with
correction of an overstated liability, per the registered "liability accounting error" (§2).
Attribution of these revisions to the 4.02 event specifically, the identity of the restated
liability line(s), and any per-period restatement schedule would require the 8-K/10-K narrative
text: **not determinable** from sealed sources beyond the paired values above.

---
*Entry status: drafted (sections 7–9 pending owner finalization).*
*채점: Claude 보조 + 인간 최종 확정. 교육·정보 목적, 투자 자문 아님.*
