# atlas/case_30.md — Liquidity Services, Inc. (LQDT) — wave-1 v2-controls V20 (FALSE POSITIVE)

Authored by Claude Code, pending human audit (D15). Analytical document under D106 ② — not a scored output. 본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).

## 1. CASE HEADER

| field | value |
|---|---|
| Case ID (anonymized frame) | case_30 (scoring ID V20) |
| Cohort | wave-1 v2-controls (22-control arm) |
| Outcome class | FP (main frame, flag at score ≥50); one of the three v2-control FPs analyzed in `analysis/error_analysis.md` §5 |
| Ground-truth tier | control (no adverse label) |
| Frozen score | score 65 (`runs/rp09/scores/case_30.json`, run `original-case_30-r1`, model claude-sonnet-5, 2026-07-07) |
| Grade record | `scoring/grades_v2/controls/case_30.json` (human_finalized: true, finalized 2026-07-09 via blanket, decisions_log 참조) — dim1=0 ("Answer key marks this a CONTROL case; output assigns misstatement_probability=65, which falls in the p>=50 band for controls -> 0" — raw key `misstatement_probability` quoted verbatim from the record (legacy v1 key — an uncalibrated ordinal score; see specs/RISK_SCORE_SEMANTICS.md)), dim2/dim3 null (control), dim4=3, memorization_suspect_condition2=false |

Company: LIQUIDITY SERVICES INC (LQDT), CIK 0001235468, cutoff 2016-02-28 —
copied from matched treatment T21 SCOR per GP-9 same-snapshot convention
(`data/candidates/candidates_v2_controls.json` V20; `data/evaluatee/cases_v2.json`
case_30, identity metadata only — the payload reaches the model as XBRL series
plus filing chronology, 19 documents from 10-K filed 2011-12-09 through 10-Q
filed 2016-02-05 per the frozen output's `documents_used`). **This entry
documents a model error on a control company, not a company problem.**

## 2. ACTUAL EVENT

**No adverse event — control** (cleanliness basis per original selection
criteria; formalized at `docs/CONTROL_CRITERIA_v2.md`, which inherits the v1
non-enforcement screens — E4-v2 AAER-index name matching plus web-screen
backstop — and the v1 no-restatement eligibility window). Selection record
`data/candidates/candidates_v2_controls.json` V20: group "control", ticker
LQDT, SIC 7389, rev_pit 397,125,000, cutoff 2016-02-28, matched_treatment T21;
selection mechanics in `runs/rp09/control_group_v2.json` (T21 block): rank 3 of
18 eligible, sic_tier 0 (primary SIC pool 7389 — same 4-digit industry as the
matched treatment), size_dist 0.1877 (revenue basis), fye_month_dist 3,
size_flags []. The company has **no enforcement action and no restatement in
the case window** per those criteria; additionally, the sealed submissions
metadata (`~/aaer-data/LQDT/edgar/CIK0001235468.json` and
`-submissions-001.json`, jointly spanning filing dates 2003-05-22 →
2026-06-30) contains **zero 8-K filings with Item 4.02** in their entire
history and exactly one 10-K/A (filed 2010-01-28). GP-8 caveat as recorded
(`analysis/error_analysis.md` §5 공통 노트): non-enforcement is not proof of
cleanliness — an error in that direction would lower measured specificity,
so the FP finding is conservative on that axis.

## 3. SIGNALS AVAILABLE PRE-CUTOFF

Cutoff 2016-02-28. Sealed basis: the frozen output's quoted deck values,
`~/aaer-data/LQDT/xbrl/CIK0001235468.json` (companyfacts), and
`~/aaer-data/LQDT/edgar/` (submissions metadata). Filing narrative text
(MD&A, impairment footnotes, segment discussion) is not among the sealed
sources — filing-text quotes: **insufficient sealed evidence**. The data
points the model reacted to, all filed ≤ cutoff and all verified genuine (§4),
together with the sealed tags that carry their disclosed explanation:

- Goodwill $40.549M (2011-09-30) → $150.768M (2011-12-31) → $209.656M
  (2014-09-30) → $122.640M (2014-12-31) → $64.073M (2015-09-30). The build is
  tagged as acquired goodwill: GoodwillAcquiredDuringPeriod = $144.378M FY2012
  (10-K accn 0001047469-12-010864, filed 2012-11-29) and $27.009M FY2013 (10-K
  0001047469-13-010744). The decline is tagged as disclosed impairment:
  GoodwillImpairmentLoss −$85.071M Q1 FY2015 (10-Q 0001104659-15-007267,
  filed 2015-02-06), −$51.2M Q4 FY2015 and −$136.248M FY2015 total, with
  GoodwillAndIntangibleAssetImpairment $147.414M FY2015 (10-K
  0001047469-15-008919, filed 2015-11-23); AssetImpairmentCharges $96.238M Q1
  FY2015 (same 10-Q). All of these accessions are in the model's own
  `documents_used`.
- InventoryNet $35.771M (2013-12-31) → $71.640M (2014-03-31) → $78.478M
  (2014-09-30) → $25.510M (2015-09-30), against revenue $505.856M (FY2013) →
  $495.661M (FY2014) → $397.125M (FY2015).
- NI $30.390M vs OCF $11.856M (FY2014); NI −$104.815M vs OCF +$43.491M
  (FY2015) — the FY2015 sign pattern coinciding with the non-cash impairment
  charges above.
- Allowance for doubtful accounts $2.396M (2015-06-30) → $0.471M (2015-09-30)
  while net AR fell $10.041M → $6.194M.
- Chronology: one 10-K/A filed 2010-01-28 (original 10-K accn
  0001047469-09-010688 filed 2009-12-11 — sealed submissions); an 8-K/A filed
  2013-07-16 the same day as an 8-K with items 2.02/9.01.

This section describes the information set — it does not re-score the case.

## 4. WHAT THE LLM CAUGHT (what the model asserted, and on what evidence)

Frozen output `runs/rp09/scores/case_30.json`: `misstatement_probability`: 65
(legacy v1 key — an uncalibrated ordinal score; see
specs/RISK_SCORE_SEMANTICS.md) = score 65, risk_tier "elevated"; CL1 (medium),
CL2 (high), CL3 (medium), CL4 (high), CL6 (medium), CL7 (low) flagged; CL5/CL8
no_flag. Top hypothesis: goodwill balances "were carried at levels not
supported by the underlying businesses' cash-generating ability" and were
"subsequently corrected via large non-cash impairment charges recorded in two
separate quarters". Every cited figure was grep-verified against sealed
companyfacts/submissions:

| model claim (verbatim) | evidence genuine? (sealed record) | correspondence |
|---|---|---|
| "Goodwill=40549000 (2011-09-30)" … "Goodwill=150768000 (2011-12-31)" … "Goodwill=209656000 (2014-09-30)" … "Goodwill=122640000 (2014-12-31)" … "Goodwill=64073000 (2015-09-30)" (CL2, hypotheses[0]) | genuine — all five values at the cited dates and cited accessions in `~/aaer-data/LQDT/xbrl/CIK0001235468.json`; the build matches tagged acquired goodwill (ASC 805) and the fall matches tagged, disclosed impairment charges (§3) | n/a — control |
| "InventoryNet=35771000 (2013-12-31)" → "InventoryNet=71640000 (2014-03-31)" → "InventoryNet=78478000 (2014-09-30)" → "InventoryNet=25510000 (2015-09-30)" vs "SalesRevenueNet=495661000 FY2014 vs SalesRevenueNet=505856000 FY2013" (CL4, hypotheses[1]) | genuine — all values and accession attributions verified | n/a — control |
| "NetIncomeLossAvailableToCommonStockholdersBasic=30390000 (FY2014…)" vs "…OperatingActivitiesContinuingOperations=11856000 (FY2014…)"; "=-104815000 (FY2015…)" vs "=43491000 (FY2015…)" (CL3) | genuine — all four values in the FY2015 10-K (0001047469-15-008919) as cited | n/a — control |
| "AllowanceForDoubtfulAccountsReceivableCurrent=2396000 (2015-06-30)" → "=471000 (2015-09-30)"; "AccountsReceivableNetCurrent=10041000 (2015-06-30)" → "=6194000 (2015-09-30)" (CL6, hypotheses[2]) | genuine — values and accessions verified | n/a — control |
| "AccountsReceivableNetCurrent=4386000 (2010-09-30)" vs "=24050000 (2013-09-30)"; "SalesRevenueNet=273015000 (FY2010…)" vs "=505856000 (FY2013…)" (CL1) | genuine — all four verified; the AR base is small in absolute terms (≈1.6% → ≈4.8% of revenue) | n/a — control |
| "10-K/A filing_date=2010-01-28 (amending 10-K filed 2009-12-11)"; "8-K/A filing_date=2013-07-16 (same day as 8-K filing_date=2013-07-16)" (CL7) | genuine — sealed submissions confirm both dates; it is the only 10-K/A in the filing history and the record holds zero Item 4.02 8-Ks | n/a — control |

Unlike case_10 (Ryder), no accession misattribution was found: every checked
value appears in the accession the model cited (comparative-period
presentation). The grade record concurs on evidence quality: "the
misstatement inference is wrong for a control firm, which is penalized in
dim1, but the evidence quality itself is high" (dim4=3).

## 5. WHAT THE LLM MISSED

n/a — control: there is no adverse mechanism to miss. The model itself read
CL5 benignly (citing the swing from OperatingIncomeLoss $82.166M FY2012 to
−$144.215M FY2015) — the error is confined to promoting disclosed-impairment/
distress patterns into a prior-period overstatement narrative.

## 6. ERROR TAXONOMY

- **Interpretation (primary)** — evidence-exists / reasoning-failure
  over-reading, `analysis/error_analysis.md` §5 분류 (ii): "실제 부진·손상의
  과잉 해석 … 인수 후 사업 부진과 **합법적 손상 인식**의 궤적이다 …
  곤경(distress)과 분식(misstatement)의 혼동 — RP-05의 Ryder 오탐과 같은
  축의 추론 실패." Under `scoring/error_taxonomy.md` MECE R1→R3 this is a
  MODEL-bucket shape (data present, output over-concludes) — 1차 분류는
  Claude, 확정은 인간 (전건 인간 감사 플래그).
- **Computation** — none found: all quoted values verified at
  value+date+accession level against sealed companyfacts (§4).
- **Retrieval/data boundary** — none found: no misattributed accessions; the
  disclosed impairment tags carrying the benign explanation were in the same
  accessions the model listed in `documents_used`.
- **Label-noise** — none within the design: control label per §2 criteria;
  GP-8 residual (non-enforcement ≠ clean) noted, direction conservative.
- **Suspected-memorization** — not indicated on the sealed draws.
  `analysis/name_probe_results.json` row case_30 (truth_ticker "LQDT"): guess
  "unknown", confidence "low", recognized: false — one sealed draw.
  `scoring/probe_results_v2/recognition/case_30.json` and
  `scoring/probe_results_v2ds_wave1/recognition/case_30.json`: company_guess
  "unknown", confidence "low" (one draw each; no case_30 file in the
  draw_2/draw_3 probe subdirectories). Probe verdicts vary across draws (L-5).
  Grade record: memorization_suspect_condition2=false ("the reasoning anchors
  on concrete provided data values throughout … and mentions no post-cutoff
  facts"). Sealed re-draws `runs/draw_k3/w1_controls/draw_2/case_30.json`
  score 55 and `.../draw_3/case_30.json` score 52 (both "elevated"): with the
  frozen draw-1 score 65, range 52-65, 3/3 draws ≥50 — the FP is draw-stable
  (contrast case_10, 4/5 re-draws below 50); scoring stays fixed to draw 1.

## 7. CPA JUDGMENT — human_finalized: false

Draft, unaudited work product until owner sign-off (PROJECT.md §7). Why each
flagged pattern is explainable in benign terms:

- **Disclosed impairment ≠ evidence of prior misstatement.** The goodwill
  trajectory the model leads with is, on the sealed tags, an ASC 805
  acquisition build (acquired goodwill $144.378M FY2012, $27.009M FY2013)
  followed by openly disclosed ASC 350 impairment charges ($85.1M Q1 FY2015,
  $51.2M Q4 FY2015). Recognizing impairment when post-acquisition performance
  deteriorates is the impairment model working as designed; treating the
  charge itself as proof that FY2012-FY2014 carrying values "overstated the
  true economic value" is hindsight reasoning — ASC 350 tests carrying value
  against conditions at each test date, and the sealed record contains no
  revision of any prior period. The model's own hypothesis text describes the
  disclosed accounting ("subsequently corrected via large non-cash impairment
  charges") and then reads it as the adverse scenario. **[OWNER REVIEW]**
- **The FY2015 NI/OCF sign split is the arithmetic signature of non-cash
  charges.** NI −$104.8M against OCF +$43.5M in the year of $147.4M
  goodwill-and-intangible impairment is what large non-cash write-downs do to
  that comparison; the model's own top_signals text acknowledges "heavy
  non-cash charges swinging reported earnings without matching cash impact",
  then counts the pattern toward an elevated tier anyway. The FY2014 gap
  (NI $30.4M vs OCF $11.9M) coincides with the $42.7M inventory build —
  working-capital consumption, not an accrual divergence requiring a
  misstatement explanation. **[OWNER REVIEW]**
- **Inventory build-then-liquidation is a purchased-inventory operating
  pattern, not per se delayed write-down.** The NRV-timing hypothesis would
  need margin or write-down evidence the output does not cite; the sealed
  quantitative record shows the build and the wind-down but nothing
  determining that cost recognition was untimely. Filing-text support either
  way: insufficient sealed evidence. **[OWNER REVIEW]**
- **Allowance falling with receivables is write-off mechanics.** A
  charge-off against an established allowance reduces the allowance and
  gross AR together with no income-statement effect at that date; a $2.4M →
  $0.5M allowance move against a ~$400M-revenue business is also small in
  magnitude. The model flagged the co-movement (CL6 "medium") and promoted
  it into hypotheses[2] as possibly "delayed from earlier periods" without
  evidence on timing. **[OWNER REVIEW]**
- **Chronology signals are thin and self-rated low.** One 10-K/A in the
  sealed filing history (filed ~7 weeks after the 2009-12-11 10-K) and a
  same-day 8-K/A on an earnings 8-K (items 2.02/9.01), with zero Item 4.02
  filings ever — the model kept CL7 at confidence "low" and built no
  hypothesis on it; this axis did not drive the error. **[OWNER REVIEW]**
- **Net shape of the error**: genuine figures faithfully quoted (dim4=3), but
  disclosed distress — acquisition underperformance recognized through
  impairment — was read as prior-period overstatement; the Ryder FP's axis
  (error_analysis §5), here draw-stable. **[OWNER REVIEW]**

## 8. AUDIT TRANSLATION

Procedures that would have cleared the flag (procedures, not conclusions):

- Read the FY2015 impairment footnote and the Q1 FY2015 10-Q disclosure:
  triggering events, reporting units, and valuation methods for the $85.1M
  and $51.2M charges; assess whether triggers arose in the period of the
  charge or demonstrably earlier.
- Vouch the FY2012-FY2013 goodwill additions to the purchase agreements and
  ASC 805 purchase-price allocations (acquired-goodwill tags §3), and review
  the FY2013-FY2014 annual goodwill tests (assumptions, headroom) to evaluate
  timeliness directly rather than by hindsight from the later charge.
- Test inventory NRV in the build-up quarters against subsequent selling
  prices and margins; examine any obsolescence reserve roll-forward.
- Examine the FY2015 AR allowance roll-forward: confirm the $2.4M → $0.5M
  move is charge-off against the allowance vs release into income.
- Read the 2010 10-K/A and diff against the original 10-K; search the 8-K
  record for Item 4.02 (sealed metadata already answers: zero in history).

## 9. FINANCIAL STATEMENT IMPACT

n/a — no restatement (control). No restated line items exist; the sealed
record contains no Item 4.02 8-K and no enforcement or restatement document
for this registrant (§2).

---
*Entry status: drafted (sections 7–9 pending owner finalization).*
*채점: Claude 보조 + 인간 최종 확정. 교육·정보 목적, 투자 자문 아님.*
