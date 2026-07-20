# atlas/case_44.md — Adamas Trust, Inc. (ADAM) — wave-2 control W08 (FALSE POSITIVE)

Authored by Claude Code, pending human audit (D15). Analytical document under D106 ② — not a scored output. 본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).

## 1. CASE HEADER

| field | value |
|---|---|
| Case ID (anonymized frame) | case_44 (scoring ID W08) |
| Cohort | wave-2 (23-control arm) |
| Outcome class | FP (main frame, flag at score ≥50) |
| Ground-truth tier | control (no adverse label) |
| Frozen score | score 55 (`runs/wave2/scores/case_44.json`, run `original-case_44-r1`, risk_tier "elevated") |
| Grade record | `scoring/grades_wave2/case_44.json` (human_finalized: true, finalized 2026-07-09 via RP-13 workbench; dim1=0 "control rubric assigns 0 for p>=50", dim2/dim3 null (control), dim4=3, memorization_suspect_condition2=false) |

Company: Adamas Trust, Inc. (ADAM), CIK 0001273685, SIC 6798 (REIT), cutoff
2016-02-07 — copied from matched treatment T20 (BRX) per the same-snapshot
convention (`data/candidates/candidates_wave2.json` W08: group "control",
matched_treatment "T20", scheme fields all null). Identity frame: the deck
carries the registrant's real current EDGAR name — case_44 is not among the
nine fictional-name frames in `data/evaluatee/fict_names_wave2.json` (its
`names` block covers only wave-2 treatments); sealed submissions
(`~/aaer-data/ADAM/edgar/CIK0001273685.json`) record current name "ADAMAS
TRUST, INC.", formerNames "NEW YORK MORTGAGE TRUST, INC." (to 2025 —
post-cutoff real-world rename). **This entry documents a model error on a
control company, not a company problem.**

## 2. ACTUAL EVENT

**No adverse event — control** (cleanliness basis per original selection
criteria; see `docs/CONTROL_CRITERIA_v2.md`). Selection record
`runs/wave2/control_group_v2.json` (criteria = CONTROL_CRITERIA_v2.md,
criteria_sha256 f6cc67cb…, per its `_meta`): selected for T20 at rank 3 —
sic_pool "6798", sic_tier 0, assets_pit 9,361,810,000 (size_dist 0.0176,
size_basis "assets", flag "S1-매출 PIT 불능 → 총자산 대체"), fye 1231
(fye_month_dist 0). Cleanliness under v2 = the E4-v2 machine name-screen
against the AAER respondents index (current name + formerNames) plus the
owner external web screen (§6-v2) — a **non-enforcement** label, not a
purity claim (`analysis/error_analysis_wave2_holdout.md` header: 대조군
라벨="비집행"(무결 아님)). Honest-record note from sealed submissions
metadata: the full filing history contains exactly one 8-K carrying Item
4.02 (filed 2005-03-17, accn 0001273685-05-000012) — ~11 years before
cutoff, in the same early-history era as the 2006 10-K/A and 2007 NT
filings the model cited (§4); no enforcement or restatement document is
sealed for this registrant. GP-8-direction caveat: an error in the control
label would lower measured specificity, so the FP finding is conservative
on that axis.

## 3. SIGNALS AVAILABLE PRE-CUTOFF

Cutoff 2016-02-07. Sealed basis: the frozen output's quoted deck values,
`~/aaer-data/ADAM/xbrl/CIK0001273685.json` (companyfacts), and
`~/aaer-data/ADAM/edgar/` (submissions metadata; both manifest-pinned,
`data/manifests/aaer_data_manifest.json`). Filing narrative text (MD&A,
amendment explanatory notes) is not among the sealed sources — filing-text
quotes: **insufficient sealed evidence**. The data points the model reacted
to, all filed ≤ cutoff and all verified genuine (§4):

- NI vs CFO: ProfitLoss $28.182M / $68.955M / $136.191M (FY2012/13/14) vs
  NetCashProvidedByUsedInOperatingActivities $29.089M / $53.303M / $37.551M
  (all in the FY2014 10-K, accn 0001437749-15-003681).
- Quarterly NetIncomeLoss 2013-2014 rising from $15.383M (Q1-2013) to
  $41.976M (Q4-2014), with one dip (Q2-2013 $11.900M).
- Two parallel interest-expense series in the same sealed companyfacts:
  quarterly `InterestExpense` in the tens of millions (e.g., Q4-2013
  $68.584M) alongside small annual `InterestExpense` values ($3.645M /
  $6.655M / $5.569M FY2012/13/14) — and annual `InterestExpenseBorrowings`
  of $105.926M / $231.178M / $301.010M in the **same accession** (§4).
- Filing chronology: NT 10-K 2007-03-16 and NT 10-Q 2007-05-09/08-10/11-09;
  10-K/A 2006-05-23 and 2012-07-09; 10-Q/A 2004-08-17, 2009-11-12,
  2012-09-06; Q3-2015 10-Q filed under self-prefixed accn
  0001273685-15-000007 (all verified in sealed submissions).
- Rapid balance-sheet scale-up: Assets $374.294M (2010-12-31, first in the
  Q2-2011 10-Q accn 0001437749-11-005485) → $10,540.005M (2014-12-31).

This section describes the information set — it does not re-score the case.

## 4. WHAT THE LLM CAUGHT (what the model asserted, and on what evidence)

Frozen output `runs/wave2/scores/case_44.json`: `misstatement_probability`:
55 (legacy v1 key — an uncalibrated ordinal score; see
specs/RISK_SCORE_SEMANTICS.md) = score 55, risk_tier "elevated". CL3, CL5,
CL7 flagged (all confidence "medium"); CL1/CL2/CL4/CL8 insufficient_data;
CL6 no_flag. Top hypothesis: "Possible understatement/mis-tagging of annual
interest expense relative to the much larger quarterly interest expense
figures reported for the same fiscal years". Every cited figure was
grep-verified against the sealed companyfacts/submissions:

| model claim (verbatim) | evidence genuine? (sealed record) | correspondence |
|---|---|---|
| "InterestExpense=68584000 (2013-10-01 to 2013-12-31) yet the FY2013 annual figure is InterestExpense=6655000 … an internally inconsistent, highly volatile expense series" (CL5/hyp 1; also FY2012 35,748,000 vs 3,645,000; FY2014 74,315,000 vs 5,569,000) | all six values genuine in `~/aaer-data/ADAM/xbrl/CIK0001273685.json`. But the same cited accession (0001437749-15-003681) also carries annual `InterestExpenseBorrowings` = 231,178,000 (FY2013), which **equals the four quarters exactly** (46,145+54,917+61,532+68,584); FY2014 likewise: 75,413+75,665+75,617+74,315 = 301,010,000 = InterestExpenseBorrowings FY2014. Earlier 10-Ks tagged the same totals under `InterestExpense` itself (FY2012 105,926,000 in 0001437749-13-003120). The "inconsistency" is a concept re-mapping across filings, not a contradiction in the statements | n/a — control |
| "ProfitLoss=136191000 … vs NetCashProvidedByUsedInOperatingActivities=37551000 … ratio ~3.63x, a marked widening" (CL3) | genuine — all six NI/CFO values at the cited dates/accession; ratios 0.97x/1.29x/3.63x recompute | n/a — control |
| "NetIncomeLoss=15383000 … 41976000 — a nearly monotonic quarterly climb" (CL5) | genuine — all eight quarterly values in sealed facts; each year's quarters sum exactly to the annual ProfitLoss (68,955,000; 136,191,000), so the "smooth" series is internally consistent; the series includes a Q2-2013 decline | n/a — control |
| "NT 10-K filed 2007-03-16 … repeated late-filing notifications" and "10-K/A filed 2006-05-23; 10-K/A filed 2012-07-09; 10-Q/A filed 2004-08-17; 10-Q/A filed 2009-11-12; 10-Q/A filed 2012-09-06" (CL7) | genuine — every date/form matches sealed submissions | n/a — control |
| "A Q3 2015 10-Q was filed under a self-prefixed accession number (0001273685-15-000007) rather than the usual filing-agent prefix … an unusual deviation in filing pattern" (CL7) | accession genuine. Sealed submissions show self-prefixed accessions already in 2004-2005 (e.g., 10-Q/A 0001273685-04-000010) and **every subsequent periodic filing** self-prefixed (10-K 2016-02-25 accn 0001273685-16-000021; all 2016 10-Qs) — post-cutoff sealed metadata consistent with a filer-agent transition, not a one-off anomaly | n/a — control |
| "Liabilities=9418009000 (2013-12-31) vs Assets=9898675000 … liabilities scaled roughly in proportion" (CL6, no_flag) | genuine — all four values at cited dates | n/a — control |

The grade record concurs on evidence quality: "Evidence is specific and
grounded in provided data … all with accession numbers and period tags …
backed by cited data points rather than fabrication" (dim4=3), and names
the defect: "the main defect is calibration (p=55 on a clean company,
apparently driven by likely XBRL tagging artifacts in the InterestExpense
series)".

## 5. WHAT THE LLM MISSED

n/a — control: there is no adverse mechanism to miss. Notably the model
supplied its own hedges — the top hypothesis concedes "mis-tagging", CL8
candidly lists the coverage gaps, hypothesis 2 attributes the NI-CFO gap to
items "typical of mortgage REITs", CL6 read liabilities as proportionate —
yet still promoted the composite to score 55 / "elevated".

## 6. ERROR TAXONOMY

- **Interpretation (primary)** — registered classification
  `analysis/error_analysis_wave2_holdout.md` §1, ADAM row: (ii-c)+(ii-a) —
  the headline signal is called "분기·연간 스코프 XBRL 태깅 인공물"
  possibility, the model "자헤지하면서도 elevated", verdict "인공물을
  신호로 오독 (ii-c) + 양성 오독 (ii-a)". First-pass disposition
  `review_packets/RP-13_grading_workbench.md` case_44: "오탐이나 채점 d1=0
  정확 — trust boundary 데이터" (finalize proposed).
- **Retrieval/data boundary (counter-argument on record)** — the
  disambiguating `InterestExpenseBorrowings` series sits in the sealed
  companyfacts in the very accession the model cited, but the frozen output
  never mentions the concept; whether it was in the payload's concept set is
  not determinable from sealed artifacts (the output's CL1 quote shows the
  deck's concept list was limited). error_analysis §1/§6 registers the
  DATA-direction fix candidate — a tagging-consistency pre-check: "이
  오탐을 줄일 수 있음(수정 후보, 최대 2지점 제약 내)". Owner call.
- **Computation** — none found: all quoted values verified at
  value+date+accession level (§4); ratio arithmetic recomputes; quarterly
  sums tie to annuals exactly.
- **Label-noise** — none within the design: control label per §2 (v2
  machine name-screen + owner web screen); the 2005-era history in sealed
  metadata is ~11 years pre-cutoff; non-enforcement ≠ pristine, direction
  conservative.
- **Suspected-memorization** — not indicated on the sealed draws.
  `scoring/probe_results_wave2/recognition/case_44.json`: guess "unknown",
  confidence "low"; `scoring/probe_results_v2ds_wave2/recognition/case_44.json`:
  same; `scoring/probe_results_wave2/verbatim/case_44.json`: known: false,
  all recall fields null; `analysis/name_probe_results_v2ds.json` case_44:
  recognized: false; `analysis/outcome_recognition_results.json` W08:
  knows_event: false, confidence "none" — one sealed draw each; probe
  verdicts vary across draws (L-5). Grade record:
  memorization_suspect_condition2=false. Draw stability
  (`analysis/draw_k3_results.json` case_44): draws 55, 55, 45 (median 55,
  band 45-55) — flag_draw1 and flag_median3 both true, so unlike the wave-1
  Ryder FP this flag is not a max-of-draws artifact.

## 7. CPA JUDGMENT — human_finalized: false

Draft, unaudited work product until owner sign-off (PROJECT.md §7). Why each
flagged pattern is explainable in benign terms:

- **The interest-expense "inconsistency" is a tag-mapping artifact, not an
  accounting inconsistency.** In the FY2014 10-K XBRL, the borrowings
  interest total moved to `InterestExpenseBorrowings` ($231.178M FY2013,
  $301.010M FY2014) while the reused `InterestExpense` tag carried a small
  residual item; earlier 10-Ks had tagged the same totals as
  `InterestExpense` ($105.926M FY2012). Quarterly figures tie to the
  borrowings totals to the dollar. The decisive test the model skipped: look
  for an alternative interest concept whose annual value equals the
  quarterly sum. Its own top hypothesis named "mis-tagging" and elevated
  anyway. **[OWNER REVIEW]**
- **The NI-CFO gap is the fair-value accounting shape of a mortgage REIT.**
  Sealed FY2014 facts include UnrealizedGainLossOnInvestments $56.931M and
  recurring fair-value changes (assets +$390.371M / liabilities −$333.440M)
  — non-cash income statement items that do not run through CFO. The model's
  hypothesis 2 itself calls the pattern "typical of mortgage REITs" — the
  same self-hedge-then-elevate shape error_analysis assigns to IOVA.
  **[OWNER REVIEW]**
- **Rising quarterly earnings on a scaling portfolio are not "unusually
  smooth".** Assets grew $374.294M (2010) → $10,540.005M (2014); a levered
  spread portfolio scaling up produces rising NI mechanically; the series
  is not monotonic (Q2-2013 dip) and each year's quarters sum exactly to the
  annual figure. **[OWNER REVIEW]**
- **The chronology signals are stale or benign.** The NT/amendment cluster
  is 2004-2012 history, far outside the 2013-2015 window the quantitative
  flags target; the self-prefixed Q3-2015 accession reads as a filer-agent
  transition — sealed metadata (partly post-cutoff) shows every subsequent
  periodic filing self-prefixed, and self-prefixed accessions already
  existed in 2004-2005. **[OWNER REVIEW]**
- **Net shape of the error**: genuine, individually explainable signals — a
  tagging artifact, a structural fair-value NI/CFO gap, growth-driven
  earnings, stale chronology — compounded into "elevated" at score 55, five
  points over the flag threshold. Consistent with the wave-2 finding that
  FPs are grounded over-reading, not fabrication (error_analysis §1).
  **[OWNER REVIEW]**

## 8. AUDIT TRANSLATION

Procedures that would have cleared the flag (procedures, not conclusions):

- Reconcile the XBRL interest-expense tags to the printed income statement
  in the FY2014 10-K; confirm which concept maps to the face line and that
  quarterly amounts roll forward to the annual total.
- Recompute quarterly-to-annual tie-outs for net income and interest
  expense (sealed answer: both tie exactly via the borrowings concept).
- Obtain the cash flow statement's non-cash reconciling items (unrealized
  fair-value gains, premium amortization) and size them against the NI-CFO
  gap.
- Read the 10-Q/A (2012-09-06) and 10-K/A (2012-07-09) and diff against the
  originals to identify what was amended; confirm absence of any ASC 250
  restatement disclosure in the signal window.
- Search the 8-K record for Item 4.02 and auditor-change items in the case
  window (sealed metadata: the single 4.02-item 8-K is dated 2005-03-17).
- Inquire into the filing-agent change behind the self-prefixed Q3-2015
  accession; confirm continuity of subsequent periodic filings.

## 9. FINANCIAL STATEMENT IMPACT

n/a — no restatement (control). No restated line items exist for the case
window; no enforcement or restatement document is sealed for this
registrant, and the one Item 4.02 8-K in sealed submissions metadata
(2005-03-17) predates the cutoff by ~11 years and the flagged 2013-2015
signal window entirely (§2).

---
*Entry status: drafted (sections 7–9 pending owner finalization).*
*채점: Claude 보조 + 인간 최종 확정. 교육·정보 목적, 투자 자문 아님.*
