# atlas/case_54.md — Levi Strauss & Co. (LEVI) — wave-2 control W21 (FALSE POSITIVE)

Authored by Claude Code, pending human audit (D15). Analytical document under D106 ② — not a scored output. 본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).

## 1. CASE HEADER

| field | value |
|---|---|
| Case ID (anonymized frame) | case_54 (scoring ID W21) |
| Cohort | wave-2 (23-control arm) |
| Outcome class | FP (main frame, flag at score ≥50) |
| Ground-truth tier | control (no adverse label) |
| Frozen score | score 55 (`runs/wave2/scores/case_54.json`, run `original-case_54-r1`, risk_tier "elevated") |
| Grade record | `scoring/grades_wave2/case_54.json` (human_finalized: true, finalized 2026-07-09 via RP-13 workbench; dim1=0 "Control banding: p>=50 -> 0", dim2/dim3 null (control), dim4=2, memorization_suspect_condition2=false) |

Company: LEVI STRAUSS & CO (LEVI), CIK 0000094845, SIC 2300 (apparel), FYE
1129, cutoff 2019-11-02 — copied from matched treatment T29 (UAA) per the
same-snapshot convention (`data/candidates/candidates_wave2.json` W21: group
"control", matched_treatment "T29", scheme fields all null). Identity frame:
real EDGAR name — case_54 is not in `data/evaluatee/fict_names_wave2.json`.
**This entry documents a model error on a control company, not a company
problem.**

## 2. ACTUAL EVENT

**No adverse event — control** (cleanliness basis per original selection
criteria; see `docs/CONTROL_CRITERIA_v2.md`). Selection record
`runs/wave2/control_group_v2.json` (criteria_sha256 f6cc67cb…, per its
`_meta`): selected for T29 at rank 1 — sic_pool "2300", sic_tier 0, rev_pit
5,575,440,000 (size_dist 0.071, size_basis "revenue", size_flags empty),
assets_pit 4,138,997,000, fye 1129 (fye_month_dist 1). Cleanliness under v2
= machine name-screen against the AAER respondents index + owner external
web screen — a **non-enforcement** label, not a purity claim
(`analysis/error_analysis_wave2_holdout.md` header: 대조군 라벨="비집행"(무결
아님)). Sealed submissions metadata (`~/aaer-data/LEVI/edgar/
CIK0000094845.json` and `-submissions-001.json`, jointly spanning filing
dates 2000-05-04 → 2026-06-15) contains **zero 8-K filings with Item 4.02**,
and no enforcement or restatement document is sealed for this registrant.
GP-8-direction caveat: a control-label error would lower measured
specificity — the FP finding is conservative on that axis.

## 3. SIGNALS AVAILABLE PRE-CUTOFF

Cutoff 2019-11-02. Sealed basis: the frozen output's quoted deck values,
`~/aaer-data/LEVI/xbrl/CIK0000094845.json` (companyfacts), and
`~/aaer-data/LEVI/edgar/` (submissions metadata; manifest-pinned,
`data/manifests/aaer_data_manifest.json`). Filing narrative text (MD&A, S-1
prospectus text, amendment notes) is not among the sealed sources —
filing-text quotes: **insufficient sealed evidence**. The data points the
model reacted to, all filed ≤ cutoff and verified genuine (§4):

- AR outran revenue in all three reported FY2019 quarters:
  AccountsReceivableNetCurrent 633,534,000 (2019-02-24) vs 428,469,000
  (2018-02-25) = +47.9%; 574,389,000 vs 342,322,000 = +67.8% (Q2);
  722,001,000 vs 487,240,000 = +48.2% (Q3) — while same-quarter revenue
  grew +6.75% / +5.4% / +3.8%. Sealed prior-year context: the divergence is
  new — Q3-end AR was +9.1% YoY at 2018-08-26 (487,240,000 vs 446,701,000)
  and +0.3% at 2017-08-27 (vs 445,238,000, 2016-08-28).
- AllowanceForDoubtfulAccountsReceivableCurrent 9,438,000 against net AR
  722,001,000 at 2019-08-25 (1.31%) vs 9,113,000/487,240,000 (1.87%) a year
  earlier. Sealed longer series: coverage has declined roughly monotonically
  for a decade — 24,617,000/553,385,000 = 4.45% (2010-11-28), 2.50%
  (2016-11-27), 2.42% (2017-11-26), 1.88% (2018-11-25), 1.31% (2019-08-25)
  — a trend predating the FY2019 AR surge by years.
- NetIncomeLoss 146,577,000 vs NetCashProvidedByUsedInOperatingActivities
  55,822,000 for the quarter 2018-11-26 → 2019-02-24; but FY2018 full-year
  NI 283,142,000 vs OCF 420,371,000 (OCF above NI).
- Filing chronology (sealed submissions): 10-K/A 2015-02-13 (accn
  0000094845-15-000011), one day after the original FY2014 10-K 2015-02-12
  (accn 0000094845-15-000008); second 10-K/A 2015-06-04 (accn
  0001193125-15-213503); also, uncited by the model, a 10-K/A 2009-04-21
  and two 10-Q/A 2002-09-19. NT 10-Q 2003-10-09 (accn 0001193125-03-059804).
  IPO footprint: S-1 2019-02-13, S-1/A ×3 (2019-03-06/11/20), 8-A12B
  2019-03-18, 424B4 2019-03-21 (accn 0001193125-19-082264); the registrant
  filed periodic reports well pre-IPO (sealed span starts 2000-05-04) —
  hence the pre-IPO 10-Ks/10-Qs in the deck.

This section describes the information set — it does not re-score the case.

## 4. WHAT THE LLM CAUGHT (what the model asserted, and on what evidence)

Frozen output `runs/wave2/scores/case_54.json`: `misstatement_probability`:
55 (legacy v1 key — an uncalibrated ordinal score; see
specs/RISK_SCORE_SEMANTICS.md) = score 55, risk_tier "elevated". CL1/CL6
flagged at confidence "high", CL7 at "medium"; CL2/CL3/CL4/CL5/CL8 no_flag.
Top hypothesis: "Potential premature/accelerated revenue recognition or
extension of unusually generous credit terms to wholesale customers (e.g.,
bill-and-hold, channel loading ahead of quarter-end, or delayed
collections)". Every cited figure was checked against the sealed record:

| model claim (verbatim) | evidence genuine? (sealed record) | correspondence |
|---|---|---|
| "AccountsReceivableNetCurrent=722001000 (end 2019-08-25) vs AccountsReceivableNetCurrent=487240000 (end 2018-08-26): +48.2% YoY" while revenue "+3.8% YoY" (CL1; parallel Q1 +47.9%/+6.75% and Q2 +67.8%/+5.4%) | genuine — all twelve AR/revenue values at the cited dates in sealed companyfacts; percentages recompute. Attribution nuance: the model sources the FY2018 comparatives to the FY2019 10-Q accessions; sealed facts attribute those observations to the FY2018 10-Qs (e.g., 2018-08-26 AR to accn 0000094845-18-000045) — identical values, both pre-cutoff | n/a — control |
| "AllowanceForDoubtfulAccountsReceivableCurrent=9438000 (2019-08-25) against AccountsReceivableNetCurrent=722001000 … 1.31%, down from 1.87% a year earlier (9113000/487240000)" (CL6) | genuine — all values in sealed facts; ratios recompute (allowance over net AR, as stated). Sealed context the output does not carry: the ratio has fallen from 4.45% (2010-11-28) across nine years — the FY2019 level extends a long trend rather than breaking one | n/a — control |
| "NetIncomeLoss=146577000 (quarter 2018-11-26 to 2019-02-24) vs NetCashProvidedByUsedInOperatingActivities=55822000" (hyp 3, echoed in CL3 evidence) | genuine — both values at accn 0000094845-19-000016. The same output's CL3 is no_flag, citing FY2018 OCF 420,371,000 above NI 283,142,000 ("not a red-flag direction") | n/a — control |
| "10-K/A filed 2015-02-13 (one day after the original 10-K filed 2015-02-12), followed by a second 10-K/A filed 2015-06-04" (CL7) | dates genuine in sealed submissions (accns §3). No numeric revision footprint: **zero XBRL facts in sealed companyfacts are attributed to either 2015 10-K/A accession**. The deterministic chronology baseline `analysis/results_b3.json` W21 W4 scores 0 with all indicators 0 (b_ka=0) — the amendments sit outside its 2018-11-02 → 2019-11-02 window | n/a — control |
| "NT 10-Q filed 2003-10-09 indicates a historical late-filing episode" — cited with source_accession_no "n/a" (CL7) | the world-fact is genuine: sealed submissions carry NT 10-Q 2003-10-09, accn 0001193125-03-059804 — 16 years before cutoff. The citation defect stands as graded: the grade record marks it "outside the provided document list, and … unverifiable (possible fabrication/irrelevance)", a driver of dim4=2 | n/a — control |
| "These signals emerged largely around/after the company's March 2019 IPO period, a time when incentives to present strong reported growth may be elevated" (top_signals[4]) | not sourced to any provided document (grade record); the sealed submissions nonetheless carry the IPO footprint (S-1 2019-02-13 → 424B4 2019-03-21), and the reference is pre-cutoff public fact per the grade record's memorization analysis | n/a — control |

Grade record: "These specific data points genuinely support the stated
claims … I withheld 3 … because of citation-quality defects" (dim4=2).

## 5. WHAT THE LLM MISSED

n/a — control: there is no adverse mechanism to miss. Notably the model
supplied its own benign readings on five axes — CL2 (goodwill "essentially
flat over ~3 years"), CL3 (FY2018 OCF above NI), CL4 (inventory flat,
gross margin stable), CL5 (a −19,012,000 loss quarter, "genuine earnings
volatility rather than smoothing"), CL8 (coverage adequate) — yet promoted
the CL1/CL6 composite to score 55 / "elevated".

## 6. ERROR TAXONOMY

- **Interpretation (primary)** — registered classification
  `analysis/error_analysis_wave2_holdout.md` §1, LEVI row: "(ii-a)" — "'AR
  grew 40–68% YoY ... while revenue grew only 3.8–6.8%'는 산술 검증됨
  (`722,001,000` vs `487,240,000`=+48.2%). 그러나 **Levi Strauss는 2019-03
  IPO** — FY2019 매출채권 급증은 상장 직후 도매 확장/계절성의 양성 설명.
  모델이 그 대안을 저울질하지 않음. (ii-a)". First-pass disposition
  `review_packets/RP-13_grading_workbench.md` case_54: "오탐이나 채점 d1=0
  정확 — trust boundary 데이터" (finalize signed). MECE R1 corroboration:
  every CL1/CL6 figure verifies in sealed facts, while the chronology
  baseline (`analysis/results_b3.json` W21 W4, score 0, all indicators 0)
  confirms no in-window chronology signal — the flag rests entirely on how
  the genuine divergence was read.
- **Citation-discipline defect (recorded, not hallucination)** — the two
  dim4 flaws (NT 10-Q with accession "n/a"; unsourced IPO reference) are
  both genuine world-facts in the sealed record (accn 0001193125-03-059804;
  S-1/424B4 footprint §3) — not evidence-absent fabrication; the defect is
  sourcing discipline, as graded (dim4=2, not 3).
- **Computation** — none found: all quoted values verified at value+date
  level against sealed companyfacts (§4); growth and ratio arithmetic
  recomputes; one source-attribution nuance (§4 row 1), values unaffected.
- **Label-noise** — none within the design: control label per §2 (v2
  machine name-screen + owner web screen); zero Item 4.02 in the sealed
  filing span; non-enforcement ≠ pristine, direction conservative.
- **Suspected-memorization** — name recognition with approximate figure
  recall but no event knowledge (as a control there is no adverse outcome
  to recall). `scoring/probe_results_wave2/recognition/case_54.json`: guess
  "Levi Strauss & Co.", confidence "medium";
  `scoring/probe_results_v2ds_wave2/recognition/case_54.json`: "unknown" /
  "low". `scoring/probe_results_wave2/verbatim/case_54.json`: known: true,
  recalling filing_date 2019-01-29, net_income 284,400,000, revenue
  5,575,200,000 — near but not equal to the sealed FY2018 values (10-K
  filed 2019-02-05; NI 283,142,000; SalesRevenueNet 5,575,440,000).
  `analysis/outcome_recognition_results.json` W21: name_id_recognized_frozen
  true, **knows_event false**, confidence "low" — one sealed draw each;
  verdicts vary across draws (L-5). Grade record:
  memorization_suspect_condition2=false ("the March 2019 IPO reference was
  public before the last provided filing (2019-10-08)"). Draw stability
  (`analysis/draw_k3_results.json` case_54): draws 55, 58, 50 (median3 55,
  band 50-58), flag_draw1 and flag_median3 both true — unlike the wave-1
  Ryder FP, not a max-of-draws artifact.

## 7. CPA JUDGMENT — human_finalized: false

Draft, unaudited work product until owner sign-off (PROJECT.md §7). Why each
flagged pattern is explainable in benign terms:

- **The AR divergence is real and new — and coincides with the registered
  benign alternative.** The FY2019 AR surge (+48-68% vs +9.1% and +0.3% in
  the two prior Q3 comparisons, §3) sits astride the March-2019 IPO
  transition in sealed submissions (S-1 → 424B4), which the registered
  analysis reads as post-IPO wholesale expansion/seasonality (error_analysis
  §1); the model surfaced the IPO (top_signals[4]) but weighed it only as an
  incentive amplifier, never as the operating explanation for a changed
  working-capital shape. **[OWNER REVIEW]**
- **The allowance ratio is a decade trend, not an FY2019 innovation.**
  Coverage on net AR fell 4.45% → 1.31% over nine years in sealed facts
  (§3); the one-year frame (1.87% → 1.31%) presents the tail of a long
  estimation trajectory as reserve growth "lagging risk exposure". At ~$9.4M
  against ~$1.45B quarterly revenue, the balance is also a small lever on
  income in either direction. **[OWNER REVIEW]**
- **One quarter of NI above OCF is not a cash-conversion break.** The
  model's own CL3 is no_flag on the full-year FY2018 pair (OCF above NI)
  and its hyp 3 concedes the working-capital reading; one Nov-FYE Q1 with
  seasonal receivables build does not set the adverse direction.
  **[OWNER REVIEW]**
- **The 2015 amendments and 2003 NT 10-Q have no misstatement footprint on
  this sealed record.** Zero XBRL facts attribute to either 2015 10-K/A
  accession, no Item 4.02 exists in history, and the NT 10-Q is 16 years
  pre-cutoff — the same CL7 metadata-over-reading axis as the wave-1 Ryder
  FP (`atlas/case_10.md` §7) and LPSN (`atlas/case_48.md` §7), here at
  least held to confidence "medium". **[OWNER REVIEW]**
- **Net shape of the error**: arithmetically genuine, individually
  benign-explainable signals (IPO-coincident AR build + tail of a long
  allowance trend + one seasonal quarter + stale chronology items)
  compounded into "elevated" at score 55, five points over the flag
  threshold — the wave-2 pattern of FPs as grounded over-reading, not
  fabrication (error_analysis §1). **[OWNER REVIEW]**

## 8. AUDIT TRANSLATION

Procedures the flag would motivate (procedures, not conclusions):

- Confirm FY2019 wholesale receivables with major customers; test
  subsequent cash receipts; sales cutoff testing around 2019-02-24 /
  2019-05-26 / 2019-08-25 (shipment terms, side agreements, post-period
  returns) against the channel-loading hypothesis.
- Analyze DSO by channel/geography across the IPO transition; read the
  S-1/prospectus working-capital and credit-terms disclosures (not sealed
  here) for the benign expansion explanation.
- Recompute the allowance on gross receivables with aging and charge-off
  history, sized against the nine-year coverage trend.
- Reconcile the Q1 FY2019 NI-OCF gap to working-capital movements against
  prior-year Q1 seasonality.
- Read the two 2015 10-K/As, diff against the original FY2014 10-K, and
  confirm absence of any ASC 250 restatement or Item 4.02 disclosure
  (sealed metadata already answers: zero 4.02).

## 9. FINANCIAL STATEMENT IMPACT

n/a — no restatement (control). No restated line items exist; the sealed
record contains no Item 4.02 8-K, no enforcement or restatement document,
and no XBRL fact attributed to either 2015 10-K/A accession — no numeric
revision footprint in the sealed companyfacts (§2, §4).

---
*Entry status: drafted (sections 7–9 pending owner finalization).*
*채점: Claude 보조 + 인간 최종 확정. 교육·정보 목적, 투자 자문 아님.*
