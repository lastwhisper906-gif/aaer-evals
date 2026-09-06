# atlas/case_67.md — Brixmor Property Group Inc. (BRX) — wave-2 treatment T20

Authored by Claude Code, pending human audit (D15). Analytical document under D106 ② — not a scored output. 본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).

## 1. CASE HEADER

| field | value |
|---|---|
| Case ID (anonymized frame) | case_67 (scoring ID T20) |
| Cohort | wave-2 |
| Outcome class | FN (main frame, flag at score ≥50) |
| Ground-truth tier | AAER-confirmed (Exchange Act Rel. 34-86538, Aug 1, 2019 / AAER-4061, Admin. Proc. File No. 3-19300) |
| Frozen score | score 20 (`runs/wave2/scores/case_67.json`, run `original-case_67-r1`, risk_tier "watch") |
| Grade record | `scoring/grades_wave2/case_67.json` (human_finalized: true, finalized 2026-07-09 via RP-13 workbench; dim1=0, dim2=0, dim3=null/null (genre mapping recorded as ungradeable — "no mapping exists"), dim4=3) |

Company: Brixmor Property Group Inc., CIK 0001581068, cutoff 2016-02-07 — the day before the
February 8, 2016 Form 8-K disclosure (order ¶34). `analysis/error_analysis_wave2_holdout.md` §2
treats this case as "(iv) 구조적 미탐, 가장 깨끗한 (iv) 사례" (structural miss, the cleanest type-(iv) case).

## 2. ACTUAL EVENT

In the Matter of Brixmor Property Group Inc.; settled cease-and-desist order; sealed local text
`~/aaer-data/BRX/34-86538.pdf.txt` (manifest-pinned, `data/manifests/aaer_data_manifest.json`). ¶1
(lines 66-75): between 3Q 2013 and 3Q 2015 (the "Relevant Period"), Brixmor "manipulated and
falsely reported its 'Same Property Net Operating Income Growth Rate,' or 'SP NOI Growth Rate,' a
non-GAAP measure relied on by investors and analysts"; SP NOI is "an adjusted version of net
operating income ('NOI'), another non-GAAP measure" (¶3, lines 94-96). Three methods, all of which
"lacked any proper accounting justification" (¶13, lines 185-190):

- **Cookie-jar timing**: "an internal books and records account, the '2617 Account,' which was
  referred to internally as a 'cookie jar,' to improperly alter the timing of revenue recognition"
  (¶14, lines 194-195); CAO, October 2015: "we are emptying the cookie jar to get to the [SP NOI
  Growth Rate] for this qtr" (¶16, lines 221-222).
- **Lease-termination income (LSI) inclusion**, contrary to the stated exclusion policy (¶18,
  lines 237-239) — amortized into SP NOI (¶20) and reclassified: "improperly classified $425,000
  of a $1.3 million LSI payment as 'Other Income'" in 3Q 2014 (¶21, lines 254-256).
- **Lowering Comparison Period SP NOI**, "done outside of the accounting system, on a spreadsheet"
  (¶22, line 263): CFO "deducted $250,000 from the SP NOI of the Comparison Period", lifting the
  current quarter "from 3.27% to 3.39%" (¶24, lines 293-295); 3Q 2015 reversals of "$300,000 and
  $56,000" lifted it "from 3.4% to 3.6%" (¶25, lines 305-307).

Charges (¶30-32, lines 461-478): Exchange Act §10(b) and Rule 10b-5; §13(a) and Rules 12b-20,
13a-1, 13a-11, 13a-13; and Rule 100(b) of Regulation G ("prohibits registrants from making public
a non-GAAP financial measure that contains an untrue statement of material fact"). GAAP topics:
the order maps none; it states the 2617 practice "disregarded GAAP" as to revenue-recognition
timing (¶16, line 208) while the misstated metric itself was non-GAAP. Sanction: cease-and-desist,
undertakings, and a "civil money penalty in the amount of $7,000,000" (Section IV.C, lines
614-615). Registered summary: `data/candidates/candidates_wave2.json` T20 `scheme_summary`;
`scheme_type`: reserves_smoothing; manipulation period 2013-07 to 2015-09.

## 3. SIGNALS AVAILABLE PRE-CUTOFF

Cutoff 2016-02-07. Sealed basis: the deck entry `data/evaluatee/cases_wave2.json` case_67 carries
exactly five identity fields (case_id, ticker, cik, company_name, cutoff_date) per the whitelist
contract `schemas/evaluatee_input.json` (additionalProperties: false); the numeric set is the XBRL
companyfacts `~/aaer-data/BRX/xbrl/CIK0001581068.json` and submissions chronology
`~/aaer-data/BRX/edgar/CIK0001581068.json` (manifest-pinned). At accession level (spot re-verified
in sealed companyfacts):

- NetIncomeLoss -160,713,000, OCF 268,847,000, DepreciationAndAmortization 488,524,000 (all
  FY2012); NetIncomeLoss 132,851,000, OCF 479,210,000 (FY2014) — accn 0001581068-15-000028 (10-K
  FY2014, filed 2015-02-19).
- Liabilities 7,305,908,000, ReceivablesNetCurrent 156,944,000 (2012-12-31) — accn
  0001581068-13-000007 (10-Q, 2013-12-03); Assets 9,527,623,000 (2015-09-30) — accn
  0001581068-15-000092 (10-Q, 2015-10-26).

**Structurally absent from this information set**: SP NOI and the SP NOI Growth Rate. The
sealed companyfacts file contains 321 us-gaap concepts (plus 2 dei, 2 srt); zero concepts match
"NOI," "SameProperty," or "NetOperatingIncome" — the manipulated quantity is a non-GAAP
supplemental measure, not XBRL-tagged in companyfacts. It lived in 10-Q/10-K narrative and 8-K
press-release supplemental disclosure (¶6, ¶29), which the pipeline payload does not carry. The
December 23, 2015 whistleblower complaint was internal (¶33) — not public pre-cutoff. The frozen
output's CL8 records the delivered series' limits (quoted in §4). This section describes the
information set — it does not re-score the case.

## 4. WHAT THE LLM CAUGHT

Frozen output `runs/wave2/scores/case_67.json`: `misstatement_probability`: 20 (legacy v1 key — an
uncalibrated ordinal score; see specs/RISK_SCORE_SEMANTICS.md) = score 20, risk_tier "watch" —
below the flag threshold of 50, hence FN. mechanism_hypotheses: empty list — no misstatement
mechanism asserted. What the model did assert, sub-threshold:

| model claim (verbatim) | enforcement/restatement reference | match quality |
|---|---|---|
| CL3 flag: "NetIncomeLoss=-160713000 ... NetCashProvidedByUsedInOperatingActivities=268847000" (FY2012), then dismissed in top_signals as "largely explained by substantial real estate depreciation ... a normal REIT characteristic rather than an earnings-quality red flag" | No counterpart — the order's findings run entirely on SP NOI / SP NOI Growth Rate (¶1, ¶13), not on any NI-vs-OCF relation | unrelated |
| CL5 no_flag (smoothness): "NetIncomeLoss=-160713000 (2012 annual); NetIncomeLoss=-118883000 (2013 annual); NetIncomeLoss=132851000 (2014 annual)" — GAAP earnings not unusually smooth | The truth IS smoothing — "'smoothed' income items, both up and down, between quarters" (¶34, line 500) — but of the non-GAAP SP NOI Growth Rate, a series not in the model's inputs | unrelated |
| CL6 no_flag: "Liabilities=7305908000 (2012-12-31); Liabilities=6595936000 (2015-09-30)" read with equity growth as "IPO/follow-on offerings" | No counterpart — the order contains no balance-sheet or leverage finding | unrelated |
| CL8 insufficient_data: "No Revenues, IntangibleAssets, OtherAssets, Inventory, or AllowanceForDoubtfulAccounts concepts included in the provided financial_series_point_in_time dataset" | Not a claim about the company — a correct self-diagnosis of the information set (see §5) | unrelated |

Grade notes (`scoring/grades_wave2/case_67.json`): dim1=0 (score 20, below-50 band on a treatment
case); dim2=0 ("the reserves_smoothing mechanism was entirely missed"); dim4=3 ("the GAAP-based
no_flag conclusions are internally well-evidenced even though the case-level conclusion is wrong;
dim4 grades evidence quality, not outcome").

## 5. WHAT THE LLM MISSED

The distinction this entry turns on: **"missed signal" vs "signal not in the information set."**
This FN is the latter. The manipulated quantity — the non-GAAP SP NOI Growth Rate — was
structurally absent from the input schema and payload: the deck entry is identifiers-plus-cutoff
only (`schemas/evaluatee_input.json`, five whitelisted fields, additionalProperties: false); the
sealed companyfacts contains no NOI, SameProperty, or NetOperatingIncome concept among its 321
us-gaap concepts (§3) — an absence that is a fact of the source data (non-GAAP measures are not
tagged in companyfacts), not an extraction defect; and two of the three methods left no
GAAP-ledger trace reachable by this pipeline — Comparison Period adjustments were made "outside of
the accounting system, on a spreadsheet" (¶22, line 263), and the 2617/LSI timing moves are in the
$56,000-$425,000 range (¶21, ¶24, ¶25) against consolidated GAAP income in the hundreds of
millions.

`analysis/error_analysis_wave2_holdout.md` §2: "XBRL-재무제표 전용 파이프라인은 비-GAAP 지표 조작을 구조적으로 탐지 불가" —
an XBRL-financial-statements-only pipeline structurally cannot detect non-GAAP metric
manipulation; "능력 부족 아님 — 입력에 신호 부재" (not a capability deficit — the signal is absent from the
input). Within the sealed §3 information set, missed signals: **none identified from sealed
evidence**. Residual nuance: companyfacts does contain revenue-family concepts (e.g.,
RealEstateRevenueNet) while CL8 reports no revenue series delivered — a coverage gap on a
secondary axis; a revenue series would not have exposed SP NOI smoothing for the reasons above.

## 6. ERROR TAXONOMY

Per `scoring/error_taxonomy.md` (R1→R2→R3), atlas vocabulary:

- **R1 (DATA-first)**: the signal the answer key rests on (SP NOI Growth Rate) did not exist in
  the data provided to the evaluatee, and the absence is a fact of the world (non-GAAP measure,
  not XBRL-tagged — verified against the sealed source, §3/§5), not a collection defect — R1's
  DATA bucket does not fire; R2: the dim1 band rule is mechanical (score 20 below 50 on a
  treatment case → 0), no criteria ambiguity; R3's premise (signal present in provided data)
  fails, so no MODEL attribution is available for the case-level miss. The sealed analysis
  classifies it type (iv) structural miss (`error_analysis_wave2_holdout.md` §2).
- **Computation / retrieval**: none identified — dim4=3; all eight §3 values spot re-verified as
  present in sealed companyfacts under the cited accessions.
- **Interpretation**: none identified at case level from sealed evidence — the grade record reads
  the REIT-depreciation explanation of the NI/OCF gap as internally well-evidenced (dim4
  rationale, §4); the wrong case-level conclusion traces to the information set.
- **Label-noise**: none — AAER-confirmed tier (settled Commission order, AAER-4061).
- **Suspected-memorization**: recognition probe (single stored draw,
  `scoring/probe_results_wave2/recognition/case_67.json`): company_guess "unknown", confidence
  "low". Verbatim probe (single stored draw, `scoring/probe_results_wave2/verbatim/case_67.json`):
  known: false, all recall fields null. Grade memorization_suspect_condition2: false — "no mention
  of the revelation, the SEC order, restatement, or any other post-cutoff fact appears anywhere".

## 7. CPA JUDGMENT — human_finalized: false

Draft, unaudited work product until owner sign-off (PROJECT.md §7).

- The FN is an information-set ceiling, not a reasoning failure: on the only axes the model had
  (GAAP series), its conclusions were correct — real-estate D&A does explain a REIT's NI/OCF gap,
  and consolidated GAAP earnings were in fact not smooth. Whether the atlas counts this FN against
  model capability at all, versus pipeline scope, is the central call. **[OWNER REVIEW]**
- CL5 asked exactly the right question ("Is the earnings trajectory unusually smooth...?") and
  answered no_flag correctly at the GAAP level, while the scheme was smoothing — of a metric one
  level removed. Detection would require ingesting non-GAAP supplemental disclosure (SP NOI tables
  and guidance ranges in 8-K press releases) and re-deriving the growth-rate-vs-guidance fit
  visible in the order's ¶26-28 charts — an input-scope expansion decision, not a model fix.
  **[OWNER REVIEW]**
- The revenue-series coverage gap (RealEstateRevenueNet present in companyfacts, no revenue
  series delivered per CL8) merits a pipeline check though not causal for this FN.
  **[OWNER REVIEW]**
- Score 20 with an empty hypothesis list is arguably the honest output given the inputs — the
  model flagged its own data insufficiency (CL8) rather than confabulating a mechanism; whether
  that is the desired trust-boundary behavior deserves a rubric note. **[OWNER REVIEW]**

## 8. AUDIT TRANSLATION

Procedures the (missed) flag would motivate — procedures, not conclusions:

- Re-perform SP NOI and its growth rate from property-level ledgers against the published
  definition (¶4, ¶18); trace adjustments on the "Reconciliation Spreadsheet" (¶23) and any
  off-system adjustments to Comparison Period figures (¶22) to support.
- Test suspense/deferral accounts of the 2617 type: aging, GAAP support for deferral and release
  timing, quarter-end release concentration, correlation with internal guidance targets (¶12, ¶16).
- Test LSI treatment against the stated exclusion policy (¶18), including reclassifications to
  "Other Income" (¶21); Regulation G definition-vs-application consistency across filings.
- Journal-entry testing on management-directed quarter-end income entries; accounting-staff
  interviews; whistleblower-channel log review (¶33).

## 9. FINANCIAL STATEMENT IMPACT

Determinable from the sealed order text (`~/aaer-data/BRX/34-86538.pdf.txt`): the misstatement
sits in the non-GAAP SP NOI Growth Rate, "in all but one of its quarterly filings (Forms 10-Q),
each of its two annual filings (Forms 10-K), and its related Forms 8-K" (¶29; ¶1). Order summary
table (lines 370-459): reported rates "3.5% 3.9% 4.0% 3.8% 3.8% 3.9% 3.9% 3.9% 3.4% 3.6% 3.6%"
(line 424) versus actual "4.3% 2.8% 3.8% 3.8% 3.5% 2.6% 4.8% 3.7% 3.3% 4.2% 3.5%" (line 428),
misstated by "-18.6% 39.3% 5.3% 0.0% 8.6% 50.0%
-18.8% 5.4% 3.0% -14.3% 2.9%" (line 457) — including downward manipulation "in three of
the nine quarters" to "hide stronger-than-expected growth" (¶28). Correction vehicle: the February
8, 2016 Form 8-K "set forth revised SP NOI Growth Rates for each of the quarters of the Relevant
Period" (¶34, line 503). Restated GAAP financial-statement line items and directions:
**not determinable** — the sealed order describes no GAAP restatement.

---
*Entry status: drafted (sections 7–9 pending owner finalization).*
*채점: Claude 보조 + 인간 최종 확정. 교육·정보 목적, 투자 자문 아님.*
