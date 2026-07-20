# atlas/case_37.md — Rocky Brands, Inc. (RCKY) — wave-1 v2-controls V13 (FALSE POSITIVE)

Authored by Claude Code, pending human audit (D15). Analytical document under D106 ② — not a scored output. 본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).

## 1. CASE HEADER

| field | value |
|---|---|
| Case ID (anonymized frame) | case_37 (scoring ID V13) |
| Cohort | wave-1 v2-controls (22-control arm) |
| Outcome class | FP (main frame, flag at score ≥50); one of the three v2-control FPs analyzed in `analysis/error_analysis.md` §5 |
| Ground-truth tier | control (no adverse label) |
| Frozen score | score 55 (`runs/rp09/scores/case_37.json`, run `original-case_37-r1`, model claude-sonnet-5, 2026-07-07) |
| Grade record | `scoring/grades_v2/controls/case_37.json` (human_finalized: true, finalized 2026-07-09 via blanket, decisions_log 참조) — dim1=0 ("Output states misstatement_probability=55. Control rubric: p>=50 -> 0" — raw key `misstatement_probability` quoted verbatim from the record (legacy v1 key — an uncalibrated ordinal score; see specs/RISK_SCORE_SEMANTICS.md)), dim2/dim3 null (control), dim4=2, memorization_suspect_condition2=false |

Company: ROCKY BRANDS, INC. (RCKY), CIK 0000895456, cutoff 2015-08-09 —
copied from matched treatment T16 ICON per GP-9 same-snapshot convention
(`data/candidates/candidates_v2_controls.json` V13; `data/evaluatee/cases_v2.json`
case_37, identity metadata only — the payload reaches the model as XBRL series
plus filing chronology, 17 documents from 10-Q filed 2011-07-29 through 10-Q
filed 2015-07-29 per the frozen output's `documents_used`). **This entry
documents a model error on a control company, not a company problem.**

## 2. ACTUAL EVENT

**No adverse event — control** (cleanliness basis per original selection
criteria; formalized at `docs/CONTROL_CRITERIA_v2.md`, which inherits the v1
non-enforcement screens — E4-v2 AAER-index name matching plus web-screen
backstop — and the v1 E5 no-restatement eligibility window). Selection record
`data/candidates/candidates_v2_controls.json` V13: group "control", ticker
RCKY, SIC 3140, rev_pit 286,242,169, cutoff 2015-08-09, matched_treatment T16;
selection mechanics in `runs/rp09/control_group_v2.json` (T16 block): rank 2 of
7 eligible, sic_tier 0 (primary SIC pool 3140, footwear), size_dist 0.4771
(revenue basis), fye_month_dist 0, size_flags [], former name "ROCKY SHOES &
BOOTS INC"; `review_packets/RP-09_control_v2_memo.md` T16 row: "신발 (3140,
1차) | ICON의 이중 정체(브랜드/신발) 중 신발 축". The company has **no
enforcement action and no restatement in the case window** per those criteria;
additionally, the sealed submissions metadata
(`~/aaer-data/RCKY/edgar/CIK0000895456.json` and `-submissions-001.json`,
jointly spanning filing dates 1996-05-14 → 2026-07-02) contains **zero 8-K
filings with Item 4.02** in their entire history and zero NT late-filing forms
in the recent file (2010-01-05 →). GP-8 caveat as recorded
(`analysis/error_analysis.md` §5 공통 노트): non-enforcement is not proof of
cleanliness — an error in that direction would lower measured specificity, so
the FP finding is conservative on that axis.

## 3. SIGNALS AVAILABLE PRE-CUTOFF

Cutoff 2015-08-09. Sealed basis: the frozen output's quoted deck values,
`~/aaer-data/RCKY/xbrl/CIK0000895456.json` (companyfacts), and
`~/aaer-data/RCKY/edgar/` (submissions metadata). Filing narrative text (MD&A,
inventory and cash-flow footnotes, amendment explanatory notes) is not among
the sealed sources — filing-text quotes: **insufficient sealed evidence**. The
data points the model reacted to, all filed ≤ cutoff and all verified genuine
(§4):

- FY2013 NetIncomeLoss $7,372,756 alongside
  NetCashProvidedByUsedInOperatingActivities −$2,453,218 (both first reported
  in the FY2013 10-K, accn 0001144204-14-013708); the adjacent years in the
  same sealed facts: OCF $17,993,553 (FY2012) and $12,980,048 (FY2014).
- InventoryNet $67,196,245 (2012-12-31) → $78,171,670 (2013-12-31), +16.4%,
  vs revenue +7.2%. The sealed quarterly series shows a repeating intra-year
  build-and-release shape: 2012: 64.1→74.0→73.0→67.2M; 2013:
  68.3→81.2→78.9→78.2M; 2014: 78.3→86.4→90.1→85.2M (Q1→Q4, companyfacts).
- Five-year NI in a $7.4M–$9.8M band vs revenue swinging −5% to +17% YoY and
  OCF from −$2.45M to +$18.0M.
- AccruedLiabilitiesCurrent ~$0.97M–$1.16M across 2011-2014 vs revenue growing
  to $286.2M.
- Amendment cluster: 10-Q/A filed 2012-08-06 (0001144204-12-042987), 10-Q/A
  filed 2012-10-31 (0001144204-12-058600), 10-K/A filed 2013-03-05
  (0001144204-13-012851) one day after the FY2012 10-K (0001144204-13-012622,
  filed 2013-03-04) — sealed submissions periods: 2012-06-30, 2012-09-30,
  2012-12-31 respectively (see §4 for the chronology the deck presented).
- FY2014: revenue +16.9% with AR +13.7% (AR slower than revenue) and positive
  OCF — the model's own CL1 read this as benign.

This section describes the information set — it does not re-score the case.

## 4. WHAT THE LLM CAUGHT (what the model asserted, and on what evidence)

Frozen output `runs/rp09/scores/case_37.json`: `misstatement_probability`: 55
(legacy v1 key — an uncalibrated ordinal score; see
specs/RISK_SCORE_SEMANTICS.md) = score 55, risk_tier "elevated"; CL3 flagged
(high), CL2/CL4/CL5/CL6/CL7 flagged (medium), CL1 no_flag, CL8
insufficient_data. Top hypothesis: "Possible aggressive channel loading /
inventory build reflected in FY2013 where reported net income remained
positive while operating cash flow turned negative". Verification against
sealed companyfacts/submissions:

| model claim (verbatim) | evidence genuine? (sealed record) | correspondence |
|---|---|---|
| "NetIncomeLoss=7,372,756 (FY2013)" vs "NetCashProvidedByUsedInOperatingActivities=-2,453,218 (FY2013)" (CL3) | genuine — both in `~/aaer-data/RCKY/xbrl/CIK0000895456.json` at 2013-12-31; so are the FY2012 ($17,993,553) and FY2014 ($12,980,048) OCF values the output also quotes | n/a — control |
| "InventoryNet=67,196,245 (2012-12-31); InventoryNet=78,171,670 (2013-12-31), a ~16.4% increase" vs revenue "~7.2%" (CL4) | genuine — values and ratios recompute; margin series recomputes too (FY2011 88,300,429/239,968,770 = 36.9%→"36.8%" per FY2014-10-K comparatives; FY2014 96,360,725/286,242,169 = 33.7%) | n/a — control |
| "NetIncomeLoss=7,683,732 (FY2010); 8,306,895 (FY2011); 8,854,765 (FY2012); 7,372,756 (FY2013); 9,845,298 (FY2014)" vs volatile revenue/OCF (CL5) | genuine — all fifteen series values verified at value+date level in sealed companyfacts | n/a — control |
| "AccruedLiabilitiesCurrent=970,806 (2011-12-31); 1,162,650 (2012-12-31); 1,083,196 (2013-12-31); 1,042,653 (2014-12-31) - essentially flat to declining" (CL6) | genuine values — but the base is ~$1M against $286M revenue (~0.4%), a magnitude the output does not confront | n/a — control |
| "10-Q/A filing_date=2012-08-06 (restating period ended 2011-06-30, filed over a year after the original)" (CL7) | accession and filing date genuine; the period claim is **contradicted by sealed submissions**: the /A's reportDate is 2012-06-30, filed 10 days after the original Q2-2012 10-Q (0001144204-12-041496, filed 2012-07-27 — absent from `documents_used`). Same for the second /A: reportDate 2012-09-30, original 10-Q 0001144204-12-058503 filed the **same day** (2012-10-31, also absent from the deck) | n/a — control |
| "10-K/A filing_date=2013-03-05, one day after original 10-K filed 2013-03-04" (CL7, hypotheses[2]) | the chronology fact is corroborated by sealed submissions (10-K/A 0001144204-13-012851, filed 2013-03-05, period 2012-12-31) — but the output cites accession 0001144204-13-012622, which is the **original 10-K**, and no 10-K/A appears in `documents_used`; the grade record flagged this citation as "unverifiable/possibly fabricated" from the deck-internal view. Sealed submissions resolve the existence question in the model's favor while confirming the citation error | n/a — control |

Value-level restatement footprint in sealed XBRL: the Q3-2012 original 10-Q
and its /A share 273 identical facts with **zero changed values**; the Q2-2012
original contributed no facts to companyfacts (superseded by its /A), and the
/A's 2011-06-30 comparatives differ from the original 2011 Q2 10-Q on only 4
facts (accrued-liability components and share counts, largest delta ~$0.36M).
The grade record concurs on evidence quality: "specific data points genuinely
support most claims, but the multi-point synthesis includes one unsupported
citation" (dim4=2).

## 5. WHAT THE LLM MISSED

n/a — control: there is no adverse mechanism to miss. Notably, the model's own
CL1 was benign (FY2014 AR +13.7% vs revenue +16.9% — "revenue growth exceeded
AR growth") and CL8 conceded the deck "excludes allowance for doubtful
accounts, tax detail, segment data, and restatement rationale" — the error is
confined to promoting the CL3/CL4/CL7 pattern into a misstatement narrative.

## 6. ERROR TAXONOMY

- **Interpretation (primary)** — `analysis/error_analysis.md` §5, RCKY entry
  (verbatim): "분류 (ii): 계절 재고 사이클의 과잉 해석 … 실제: 부츠 제조업의
  계절 재고 축적 패턴 (RCKY FY2013 10-K 재고·현금흐름 주석) — 수치는 실재하나
  'aggressive channel loading' 추론은 근거 초과." Common note (같은 §5): all
  three v2-control FPs quote genuine payload figures ("날조 없음"); the failure
  is the facts→inference step. 전건 인간 확정 대기.
- **Retrieval/data boundary (counter-argument on record from this entry's
  verification)** — the deck's `documents_used` includes both 10-Q/As but
  **omits the 2012 Q2/Q3 original 10-Qs they amend**, and the point-in-time
  deck attributes 2011-period comparative facts to the /A accessions; the
  model's false "restating period ended 2011-06-30, filed over a year after
  the original" chronology tracks that deck-construction artifact (R1 DATA
  direction under `scoring/error_taxonomy.md`; same axis as the Ryder
  10-K/A over-read in `atlas/case_10.md`). The wrong-accession 10-K/A citation,
  by contrast, is a model citation error. Owner call. **[OWNER REVIEW]**
- **Computation** — none found: every quoted figure verified at value+date
  level in sealed companyfacts (§4); growth rates and margins recompute.
- **Label-noise** — none within the design: control label per §2 criteria;
  GP-8 residual (non-enforcement ≠ clean) noted, direction conservative.
- **Suspected-memorization** — not indicated on the sealed draws.
  `scoring/probe_results_v2/recognition/case_37.json`: guess "Bridgford Foods
  Corporation", confidence "low" (same row in
  `analysis/name_probe_results.json`: truth_ticker "RCKY", recognized: false).
  `scoring/probe_results_v2ds_wave1/recognition/case_37.json`: guess "Superior
  Uniform Group, Inc. (now Superior Group of Companies)", confidence "low" —
  two sealed draws, both wrong-company at low confidence; probe verdicts vary
  across draws (L-5). Grade record: memorization_suspect_condition2=false
  ("mentions no post-cutoff facts"). Interpretive footnote: k=3 re-draws
  (`runs/draw_k3/w1_controls/draw_2/case_37.json`,
  `.../draw_3/case_37.json`) scored 52 ("elevated") and 48 ("watch") vs the
  frozen draw-1 score 55 — 2 of 3 draws at or above the flag threshold;
  scoring and attribution stay fixed to draw 1.

## 7. CPA JUDGMENT — human_finalized: false

Draft, unaudited work product until owner sign-off (PROJECT.md §7). Why each
flagged pattern is explainable in benign terms:

- **Seasonal inventory build ≠ channel loading.** The sealed quarterly series
  (§3) shows the same intra-year build-to-Q2/Q3, release-into-winter shape in
  every year 2012-2014 — the working-capital signature of a boot manufacturer
  stocking ahead of the fall/winter season, which is the explanation
  error_analysis records from the FY2013 10-K inventory/cash-flow notes (the
  narrative text itself is not sealed here — insufficient sealed evidence for
  a direct quote). The FY2013 year-end step ($67.2M→$78.2M) preceded FY2014
  revenue growth of +16.9% — build ahead of realized demand, the opposite
  shape from inventory that fails to sell through. **[OWNER REVIEW]**
- **One negative-OCF year is timing, not persistent divergence.** CL3's own
  evidence shows OCF far exceeding NI in FY2012 (+$18.0M) and positive OCF in
  FY2014 (+$13.0M); the checklist question asks for a *persistent* NI/OCF
  divergence, and a single inventory-driven year does not meet the question
  the model itself was answering — yet CL3 carried the only "high"
  confidence in the output. **[OWNER REVIEW]**
- **The accrual base is too small to smooth anything.** AccruedLiabilitiesCurrent
  of ~$1.0M-$1.2M against NI of $7.4M-$9.8M and revenue of $228M-$286M cannot
  mechanically dampen the earnings path the smoothing hypothesis describes;
  the under-accrual reading (hypotheses[1]) lacks magnitude. **[OWNER REVIEW]**
- **Amendment mechanics contradict the restatement reading.** Per sealed
  submissions the /As amend the same-quarter 2012 filings 10 days later (Q2)
  and the same day (Q3), and the 10-K/A follows the 10-K by one day — the
  chronological shape of technical/exhibit corrections, not year-late
  restatements; sealed XBRL shows zero changed values Q3-original→/A. The
  model's "restating period ended 2011-06-30, filed over a year after the
  original" premise is factually wrong (§4). The amendments' stated rationale
  is not sealed — insufficient sealed evidence on the "why". **[OWNER REVIEW]**
- **Net shape of the error**: genuine, individually weak benign-side signals
  (seasonal working capital + tiny accrual base + amendment chronology
  misread through deck metadata) were compounded into an adverse composite —
  the same over-reading axis as case_10 (Ryder) and case_30 (LQDT).
  **[OWNER REVIEW]**

## 8. AUDIT TRANSLATION

Procedures that would have cleared the flag (procedures, not conclusions):

- Read the two 10-Q/As and the 10-K/A explanatory notes; diff against the
  originals to identify amended items and confirm absence of any ASC 250
  restatement or Item 4.02 disclosure (sealed metadata already answers: zero
  Item 4.02 8-Ks in history; zero changed XBRL values on the Q3 pair).
- Observe physical inventory and roll forward by quarter; test
  lower-of-cost-or-market reserves against post-year-end sell-through of the
  FY2013 build (seasonality test: intra-year quarterly shape across years).
- Recompute the FY2013 NI→OCF bridge (inventory, AR, AP deltas) to attribute
  the negative OCF year to identified working-capital movements.
- Test completeness of accrued liabilities: search for unrecorded liabilities,
  examine subsequent disbursements, and reconcile the ~$1M accrual base to
  payroll/incentive/warranty obligations of a $286M-revenue manufacturer.
- Test distributor/retailer terms, return rights, and quarter-end shipment
  cutoff — the direct test of the output's channel-loading hypothesis.
- Confirm continuity of auditor opinions and ICFR conclusions across the
  2012-2013 amendment period.

## 9. FINANCIAL STATEMENT IMPACT

n/a — no restatement (control). No restated line items exist; the sealed
record contains no Item 4.02 8-K in the registrant's entire submissions
history and no enforcement or restatement document in `~/aaer-data/RCKY/`
(§2), and the answer key carries null scheme fields
(`data/candidates/candidates_v2_controls.json` V13).

---
*Entry status: drafted (sections 7–9 pending owner finalization).*
*채점: Claude 보조 + 인간 최종 확정. 교육·정보 목적, 투자 자문 아님.*
