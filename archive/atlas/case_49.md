# atlas/case_49.md — Iovance Biotherapeutics, Inc. (IOVA) — wave-2 control W04 (FALSE POSITIVE)

Authored by Claude Code, pending human audit (D15). Analytical document under D106 ② — not a scored output. 본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).

## 1. CASE HEADER

| field | value |
|---|---|
| Case ID (anonymized frame) | case_49 (scoring ID W04) |
| Cohort | wave-2 (23-control arm) |
| Outcome class | FP (main frame, flag at score ≥50); one of the 5/23 wave-2 control flags dissected in `analysis/error_analysis_wave2_holdout.md` §1 |
| Ground-truth tier | control (no adverse label) |
| Frozen score | score 58 (`runs/wave2/scores/case_49.json`, run `original-case_49-r1`, evaluatee claude-sonnet-5, 2026-07-07) |
| Grade record | `scoring/grades_wave2/case_49.json` (human_finalized: true, finalized 2026-07-09 via RP-13 workbench) — dim1=0 ("output's misstatement_probability=58, which is >=50 on a control case -> 0 per rubric" — legacy v1 key, an uncalibrated ordinal score; see specs/RISK_SCORE_SEMANTICS.md), dim2/dim3 null (control), dim4=3, memorization_suspect_condition2=false |

Company: Iovance Biotherapeutics, Inc. (IOVA), CIK 0001425205, SIC 2836,
cutoff 2015-11-05 — copied from matched treatment T19 (OSIR) per the
same-snapshot convention (`data/candidates/candidates_wave2.json` W04;
`runs/wave2/control_group_v2.json` T19 selection, rank 2). Sealed selection
record: rev_pit = 0, size matched on total assets instead (assets_pit
$114,739,592; size_flags "S1-매출 PIT 불능 → 총자산 대체") — a **pre-revenue**
registrant at cutoff. Sealed formerNames (submissions metadata and selection
record): "Lion Biotechnologies, Inc." (registrant name in the cutoff window),
"Genesis Biopharma, Inc", "FREIGHT MANAGEMENT CORP" — a reverse-merger
lineage. The deck entry (`data/evaluatee/cases_wave2.json` case_49) carries
identity metadata only; the payload reaches the model as XBRL series plus
filing chronology (frozen output CL8 coverage note). **This entry documents
a model error on a control company, not a company problem.**

## 2. ACTUAL EVENT

**No adverse event — control** (cleanliness basis per original selection
criteria; `docs/CONTROL_CRITERIA_v2.md`, which inherits v1's exclusion
screens: E4 AAER-index non-exposure — local index, 3,339 entries, AAER
987–4595, matched against current name **plus all formerNames** — and E5
zero 8-K Item 4.02 in [cutoff − 5y, cutoff + 3y]). Registered answer key
`data/candidates/candidates_wave2.json` W04: group "control",
scheme_summary null, scheme_type null. Additionally, the sealed submissions
metadata (`~/aaer-data/IOVA/edgar/CIK0001425205.json` and
`-submissions-001.json`, jointly 1,025 filings spanning 2008-01-29 →
2026-07-02) contains **zero 8-K filings with Item 4.02 in the entire
history**. Standing caveat as registered (`analysis/error_analysis_wave2_holdout.md`
§7): 대조군 라벨="비집행"(무결 아님) — non-enforcement is not proof of
cleanliness; an error in that direction lowers measured specificity, so the
FP finding is conservative on that axis.

## 3. SIGNALS AVAILABLE PRE-CUTOFF

Cutoff 2015-11-05. Sealed basis: the frozen output's quoted deck values,
`~/aaer-data/IOVA/xbrl/CIK0001425205.json` (companyfacts), and
`~/aaer-data/IOVA/edgar/` (submissions metadata). Filing narrative text
(MD&A, amendment explanatory notes, accrual footnotes) is not among the
sealed sources — filing-text quotes: **insufficient sealed evidence**. The
frozen output's `documents_used` spans accessions filed 2011-09-01 →
2015-08-10, all ≤ cutoff. The data points the model reacted to, all
verified genuine in the sealed record (§4):

- **Pre-revenue status**: Revenues = 0 for FY2013 and FY2014 (accn
  0001144204-15-016315); no receivables, inventory, or COGS concepts in the
  series. Consistent with rev_pit = 0 in the selection record.
- **Net-loss vs operating-cash-outflow gaps**: NetIncomeLoss −25,381,363 vs
  operating cash flow −3,662,192 (FY2013); −12,034,709 vs −8,633,247
  (FY2014, continuing-operations tag). Same filing also carries
  NetCashProvidedByUsedInOperatingActivities = **+8,633,247** for FY2014 —
  a genuine XBRL sign inconsistency between two cash-flow tags.
- **Accrual decline against rising R&D**: AccruedLiabilitiesCurrent
  1,518,225 (2013-12-31) → 327,847 (2014-12-31);
  ResearchAndDevelopmentExpense 1,329,367 (FY2013) → 2,704,597 (FY2014).
- **Filing chronology**: 11 NT 10-Q/NT 10-K notices 2010-11-16 → 2013-08-15;
  10-K/A 2011-05-04, 10-Q/A 2011-09-01 and 2012-09-10; 10-K/A 2015-04-20
  (accn 0001144204-15-023756) five weeks after the original FY2014 10-K
  (0001144204-15-016315, filed 2015-03-16); eight 8-K/A filings 2011-10-13
  → 2012-03-22 (sealed items 9.01/1.01/5.02 — none Item 4.02).
- **Shell-era balance sheet**: negative StockholdersEquity at every sealed
  measurement date 2009-12-31 (−13,488) → 2013-09-30 (−3,340,459); Assets
  29,413 (2012-12-31) → 19,873,649 (2013-12-31) → 46,506,847 (2014-12-31)
  — a recapitalization footprint.

This section describes the information set — it does not re-score the case.

## 4. WHAT THE LLM CAUGHT (what the model asserted, and on what evidence)

Frozen output `runs/wave2/scores/case_49.json`: `misstatement_probability`:
58 (legacy v1 key — an uncalibrated ordinal score; see
specs/RISK_SCORE_SEMANTICS.md) = score 58, risk_tier "elevated". CL3
(high), CL6 (medium), CL7 (high), CL8 (medium) flagged; CL1/CL2/CL4
insufficient_data; CL5 no_flag (annual loss series volatile, not smooth).
Top hypothesis: "Large non-cash charges (likely stock-based compensation,
warrant/derivative revaluation, or beneficial conversion features typical
of reverse-merger micro-cap biotechs)" driving the NI/OCF gap, direction
"timing_shift". Every cited figure was grep-verified against the sealed
companyfacts/submissions:

| model claim (verbatim) | evidence genuine? (sealed record) | correspondence |
|---|---|---|
| "NetIncomeLoss=-25381363 (2013…) vs NetCashProvidedByUsedInOperatingActivities=-3662192 (2013…)" (CL3) | genuine — −3,662,192 sits under that tag in the FY2013 10-K (0001513160-14-000023) and under `…ContinuingOperations` in the cited FY2014 10-K (0001144204-15-016315) | n/a — control |
| "NetCashProvidedByUsedInOperatingActivities=8633247 … positive sign in same filing that also reports …ContinuingOperations=-8633247 for the identical period" (CL3) | genuine — both values present for FY2014 in 0001144204-15-016315; a real XBRL sign inconsistency between tags | n/a — control |
| "AccruedLiabilitiesCurrent=1518225 (2013-12-31) declined to … 327847 (2014-12-31)" + "ResearchAndDevelopmentExpense=1329367 (2013…) increased to … 2704597 (2014…)" (CL6) | genuine — all four values at the cited dates in sealed companyfacts | n/a — control |
| "AccountsPayableCurrent=1550865 (2013-09-30) fell sharply to … 412976 (2013-12-31) **as restated in the FY2014 10-K**" (CL6) | values and dates genuine, but the "as restated" characterization is not supported: the two figures are different balance dates (Q3 vs FY-end — an ordinary sequential decline), and 412,976 first appears in the **original** FY2013 10-K (0001513160-14-000023, filed 2014-03-28), identical in every later sealed filing — no revision footprint | n/a — control |
| "NT 10-Q filed 2010-11-16; … NT 10-Q filed 2013-08-15" (11 notices, CL7) | genuine — all 11 dates match sealed submissions exactly | n/a — control |
| "10-K/A filed 2015-04-20 (one month after the original 10-K filed 2015-03-16)" (CL7); hypotheses[2] reads the amendment history as "consistent with weak internal controls and elevated risk that as-filed statements required subsequent correction" | dates and accessions genuine. The inference is not corroborated in sealed facts: **zero** XBRL values in sealed companyfacts are sourced to the 2015 10-K/A (0001144204-15-023756) — no restated figure traces to it | n/a — control |
| "Numerous 8-K/A filings clustered in … 2011-2012 (8: 2011-10-13 … 2012-03-22)" (CL7) | genuine — all eight dates match sealed submissions; sealed items are 9.01/1.01/5.02 (none 4.02) | n/a — control |
| "Company history as a near-shell/reverse-merger entity with wild swings in Assets and StockholdersEquity (including negative equity for multiple years)" (top_signals[3]) | genuine — sealed formerNames lineage and the negative-equity/asset series in §3 | n/a — control |

The grade record concurs on evidence quality: "Evidence is specific and
grounded in provided data … Mechanism hypotheses on this control case are
supported by these cited data points rather than external facts" (dim4=3 —
unlike case_10's dim4=2, the grader found no over-conclusion penalty here;
the error is carried entirely by dim1=0).

## 5. WHAT THE LLM MISSED

n/a — control: there is no adverse mechanism to miss. Notably, the model
itself supplied the benign-side readings: CL5 no_flag (loss series volatile,
not artificially smooth), CL8's own concession that "Pre-revenue
clinical-stage status limits applicability of several standard misstatement
checks" (top_signals[4]), and the top hypothesis's own causal attribution to
non-cash charges "typical of reverse-merger micro-cap biotechs". The error
is confined to promoting the CL3/CL6/CL7 composite to "elevated".

## 6. ERROR TAXONOMY

- **Interpretation (primary)** — evidence-exists / reasoning-failure, benign
  over-reading: `analysis/error_analysis_wave2_holdout.md` §1 classifies
  IOVA as (ii-a): "모델 자신이 top 가설에서 원인을 'large non-cash charges
  ... typical of reverse-merger micro-cap biotechs'로 규정하고도 elevated로
  승격 — 정의상 정상 … 패턴을 위험으로 읽음". RP-13 workbench disposition
  (`review_packets/RP-13_grading_workbench.md` case_49): "finalize (오탐이나
  채점 d1=0 정확 — trust boundary 데이터. §1 오류해부 참조)" — MODEL-side
  under the R1→R3 order of `scoring/error_taxonomy.md` (signals existed in
  the provided data; the control rubric forces a unique verdict).
- **Computation** — none found: all quoted values verified at
  value+date+accession level (§4). The one defect found is
  characterization, not arithmetic (the CL6 "as restated" label on a
  cross-quarter comparison).
- **Label-noise** — none within the design: control status verified per §2
  screens (E4 formerNames-inclusive AAER match matters here given the
  three-name lineage); 비집행 ≠ 무결 residual noted, direction conservative.
- **Suspected-memorization** — not indicated on the sealed draws. Both
  sealed recognition probes return company_guess "unknown", confidence
  "low" (`scoring/probe_results_wave2/recognition/case_49.json`;
  `scoring/probe_results_v2ds_wave2/recognition/case_49.json`) — two draws,
  both non-recognitions; probe verdicts vary across draws (L-5). Grade
  record: memorization_suspect_condition2=false ("mentions no post-cutoff
  facts (no revelation/enforcement/outcome references)").

## 7. CPA JUDGMENT — human_finalized: false

Draft, unaudited work product until owner sign-off (PROJECT.md §7). Why each
flagged pattern is explainable in benign terms:

- **A pre-revenue clinical-stage biotech is the wrong prior for the NI/OCF
  test.** With Revenues = 0 in every sealed period, a large net loss
  composed substantially of non-cash charges alongside a much smaller
  operating cash outflow is the structurally ordinary shape of a
  development-stage issuer financed through equity instruments — the frozen
  output names that exact benign cause itself, then scores against it. The
  checklist's revenue-anchored axes (CL1/CL2/CL4) all returned
  insufficient_data, so the composite rested entirely on the axes least
  informative for this issuer class. **[OWNER REVIEW]**
- **The accrual decline is a hypothesis without a corroborating event.**
  Under-accrual of CRO/clinical-trial costs is a genuine biotech estimation
  risk area, but the sealed record contains no catch-up, correction, or
  Item 4.02 event in the subsequent history that would evidence it; a
  $1.19M absolute decline at a newly recapitalized company also admits
  ordinary explanations (payment timing after the 2013-2014 financing) the
  output did not weigh. Footnote text that could settle this is not among
  the sealed sources. **[OWNER REVIEW]**
- **The chronology signals date to the shell era.** All 11 NT notices and
  the 2011-2012 amendment/8-K/A cluster fall in 2010-2013 — the period of
  negative equity and near-zero assets — and precede the recapitalized
  entity the model was asked to assess at the 2015-11-05 cutoff. Real
  historical control-weakness evidence, but stale relative to the scoring
  window. **[OWNER REVIEW]**
- **10-K/A ≠ restatement (same decisive test as case_10).** The 2015
  amendment five weeks after the original 10-K contributes zero values to
  sealed companyfacts, and every spot-checked figure is identical across
  original and later filings. The question the output skipped: do any
  values actually change? Sealed answer: no change found. **[OWNER REVIEW]**
- **Net shape of the error**: genuine, individually explainable signals
  (structural non-cash loss + small accrual decline + shell-era chronology)
  compounded into an adverse composite — the same over-reading axis as
  Ryder (atlas/case_10.md) and the wave-2 (ii-a) family, where all 5/23
  control flags were grounded-but-over-read, not fabricated
  (`analysis/error_analysis_wave2_holdout.md` §1). **[OWNER REVIEW]**

## 8. AUDIT TRANSLATION

Procedures the flag would motivate (procedures, not conclusions):

- Read the 2015 10-K/A and diff against the original FY2014 10-K: identify
  amended items (cover/Part III/exhibits vs financial statements); confirm
  absence of any ASC 250 restatement or Item 4.02 disclosure.
- Search the 8-K record for Item 4.02 and auditor-change items (sealed
  metadata already answers 4.02: zero in history; two shell-era 8-K/A carry
  Item 4.01 — read those auditor-change filings).
- Test completeness of accrued clinical/vendor liabilities: CRO contract
  confirmations, search for unrecorded liabilities, subsequent-disbursement
  testing across the 2014-12-31 balance date.
- Recompute the FY2013-FY2014 non-cash reconciling items (stock-based
  compensation, warrant/derivative revaluations) against grant and
  instrument documentation — the judgment-heavy items the top hypothesis
  names.
- Resolve the FY2014 operating-cash-flow XBRL sign inconsistency against
  the HTML statement of cash flows; evaluate going-concern/liquidity
  disclosures across the recapitalization.

## 9. FINANCIAL STATEMENT IMPACT

n/a — no restatement (control). No restated line items exist; the sealed
record contains no Item 4.02 8-K in the registrant's entire filing history
and no enforcement or restatement document under `~/aaer-data/IOVA/` (§2).

---
*Entry status: drafted (sections 7–9 pending owner finalization).*
*채점: Claude 보조 + 인간 최종 확정. 교육·정보 목적, 투자 자문 아님.*
