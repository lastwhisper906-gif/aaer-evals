# atlas/case_01.md — Comscore, Inc. (SCOR) — wave-1 treatment T21

Authored by Claude Code, pending human audit (D15). Analytical document under D106 ② — not a scored output. 본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).

## 1. CASE HEADER

| field | value |
|---|---|
| Case ID (anonymized frame) | case_01 (scoring ID T21) |
| Cohort | wave-1 |
| Outcome class | TP (main frame, flag at score ≥50) |
| Ground-truth tier | AAER-confirmed (AAER-4091 / Rel. 33-10692 / 34-87069, File 3-19499) |
| Frozen score | score 55 (`runs/main/case_01.json`, run `original-case_01-r1`); perturbed frame score 45 (`runs/perturbed/case_01.json`, run `perturbed-case_01-r1`) |
| Grade record | `scoring/grades/main/case_01.json` and `scoring/grades/perturbed/case_01.json` (human_finalized: true, RP-09 Stage 0, commit 986a893, 2026-07-07) |

Company: Comscore, Inc., CIK 0001158172, cutoff 2016-02-28
(`data/candidates/candidates.json` T21; `data/evaluatee/cases.json` case_01).
Perturbation delta: score 55 → 45 (−10). Per D8 the delta measures memorization
contribution — not a robustness pass/fail. As a recorded fact, the perturbed-frame
score falls below the ≥50 flag band (perturbed grade DIM1=0).

## 2. ACTUAL EVENT

SEC Order Instituting Cease-and-Desist Proceedings, In the Matter of Comscore, Inc.,
Securities Act Rel. 33-10692 / Exchange Act Rel. 34-87069 / AAER-4091 (September 24,
2019), settled without admitting or denying. Sealed local text:
`~/aaer-data/SCOR/33-10692.pdf.txt` (manifest-pinned, `data/manifests/aaer_data_manifest.json`).

Per the order: Comscore filings "materially overstated revenue by approximately $50
million as result of a fraudulent scheme and improper accounting involving the
manipulation of non-monetary and monetary contracts" during February 2014-February
2016, enabling it to "artificially exceed its analysts' consensus revenue target in
seven consecutive quarters" (¶1). Two legs: (a) non-monetary data-exchange
transactions ("NMTs") improperly valued at fair value — revenue "overstated by over
$34.5 million during the Relevant Period" (¶2); (b) monetary transactions —
undisclosed related/linked contracts "overstating revenue by approximately $12
million in 2015", plus side agreements letting Comscore "recognize all of the revenue
associated with the transaction in that quarter rather than defer some or all of the
revenue to subsequent quarters" (¶3). The order also covers false/misleading
customer-count and vCE metric disclosures (¶4).

Registered summary (`data/candidates/candidates.json`, T21 `scheme_summary`): revenue
overstated ~$50M ($34.5M NMT valuation + ~$12M linked/side-agreement contracts) to
beat consensus for seven straight quarters; `scheme_type`: revenue_recognition;
manipulation period 2014-02 to 2016-02.

GAAP topics, as cited by the order (non-monetary/barter revenue era): ASC 845 —
"Since the data transferred had recorded amounts of zero, no revenue should have been
recognized for Comscore's NMTs during the Relevant Period" (¶16, citing ASC
845-10-30-1 through 30-3); commercial substance, ASC 845-10-30-4 (¶17); best estimate
of selling price ("BESP") "pursuant to ASC 605-25-30-2" (order, line 320). No other
ASC topics attributed from sealed evidence.

## 3. SIGNALS AVAILABLE PRE-CUTOFF

Cutoff 2016-02-28 (`data/evaluatee/cases.json`, case_01). Sealed deck basis:
`~/aaer-data/SCOR/xbrl/CIK0001158172.json` (XBRL company facts) and
`~/aaer-data/SCOR/edgar/CIK0001158172*.json` (filing chronology). Pre-cutoff, at
accession level:

- **Receivables outrunning revenue (FY2013)**: AccountsReceivableNetCurrent $68,348K
  at 2012-12-31 (accn 0001158172-13-000004) → $90,040K at 2013-12-31 (accn
  0001158172-14-000004), ~+32%, against Revenues $255,193K (FY2012) → $286,860K
  (FY2013), ~+12% (accns 0001158172-13-000004, 0001158172-14-000004).
- **Allowance anomalies**: AllowanceForDoubtfulAccountsReceivableCurrent $1,667K at
  2013-12-31 (accn 0001158172-14-000004); reported $0 at 2015-03-31 (accn
  0001158172-15-000051) and $0 at 2015-09-30 (accn 0001158172-15-000109).
- **Net loss vs operating cash flow divergence**: FY2014 NetIncomeLoss −$9,903K vs
  NetCashProvidedByUsedInOperatingActivities $49,497K (both accn 0001158172-15-000020),
  a pattern recurring across FY2011-FY2014.
- **Deferred revenue build**: DeferredRevenueCurrent $92,013K at 2014-12-31 (accn
  0001158172-15-000020).
- **Filing-chronology friction**: 10-Q/A filed 2013-05-13 (accn 0001158172-13-000034)
  ten days after the original Q1-2013 10-Q; a 10-K/A each spring 2008-2015 (e.g.,
  0000950133-08-001688 on 2008-04-29 through 0001158172-15-000044 on 2015-04-24)
  (`~/aaer-data/SCOR/edgar/CIK0001158172-submissions-001.json` and
  `CIK0001158172.json`, filings). The NT 10-K of 2016-02-29 (accn 0001193125-16-485483)
  is the revelation event and post-dates the cutoff — not part of the information set.

This section describes the information set — it does not re-score the case.

## 4. WHAT THE LLM CAUGHT

Frozen output `runs/main/case_01.json`: `misstatement_probability`: 55 (legacy v1 key
— an uncalibrated ordinal score; see specs/RISK_SCORE_SEMANTICS.md) = score 55,
risk_tier "elevated"; CL1 (AR vs revenue), CL3 (NI vs OCF), CL6 (allowance), CL7
(chronology) flagged. Original frame primary; quotes grep-verified in the frozen
output, cited values verified against the sealed XBRL facts file.

| model claim (verbatim) | enforcement/restatement reference | match quality |
|---|---|---|
| "Potential premature/aggressive revenue recognition or delayed write-off of receivables in FY2013, evidenced by accounts receivable growing ~31.8% … versus revenue growth of only ~12.5%" (hypothesis 1, Revenues/AR, direction "overstated") | 33-10692.pdf.txt ¶1-2: revenue "materially overstated … by approximately $50 million" via "manipulation of non-monetary and monetary contracts", NMTs "for the purpose of improperly increasing revenue recognition" | right account wrong mechanism |
| "A quick amendment to the Q1 2013 Form 10-Q … suggests an error was identified and corrected shortly after original issuance, indicating weaker internal controls around period-end balance sheet closing" (hypothesis 2, direction "timing_shift") | No counterpart mechanism in 33-10692.pdf.txt (the 2013 10-Q/A is not mentioned); ¶37 does acknowledge "several material weaknesses in Comscore's internal control over financial reporting" | unrelated |
| "Persistent GAAP net losses each year 2010-2014 alongside strong and growing operating cash flow … could mean revenue/expense timing via deferred revenue build-up … is being used to manage the pace of recognized revenue" (hypothesis 3, direction "understated") | No counterpart; the order's deferral element runs the other way — side agreements let Comscore recognize revenue "rather than defer some or all of the revenue to subsequent quarters" (¶3) | unrelated |
| "Anomalous allowance-for-doubtful-accounts reporting showing $0 in two separate 2015 quarters despite AR balances of $77-98 million" (overall.top_signals) | No allowance/reserve allegation in 33-10692.pdf.txt | unrelated |

Row 1 carries the grade: correct account area (revenue) and direction (overstated),
but the treatment type — premature recognition inferred from DSO divergence — does not
match the barter-valuation ($34.5M NMT) + side-agreement (~$12M) scheme; no
hypothesis names non-monetary exchanges (DIM2=1, both grade records).
Perturbed-frame differences (`runs/perturbed/case_01.json`): score 45, risk_tier
"watch"; top hypothesis adds "channel stuffing, bill-and-hold arrangements, or
extended payment terms" and grades genre "active", an exact genre match (perturbed
DIM3=2) versus the main frame's "mixed" (DIM3=1); same flagged checklist items on
perturbation-scaled values.

## 5. WHAT THE LLM MISSED

From the sealed §3 information set: none identified — the frozen checklist surfaced
the AR/revenue, allowance, NI/OCF, deferred-revenue, and chronology signals the
sealed deck supports. The scheme's distinguishing features (NMT/barter valuation,
linked contracts, side agreements, customer-count methodology) left no distinct
pre-cutoff footprint in the XBRL-only deck — insufficient sealed evidence to name a
missed signal for those legs. The top hypothesis anchors on FY2013 AR growth,
largely before the registered window (2014-02 to 2016-02); see §7.

## 6. ERROR TAXONOMY

Outcome is TP; taxonomy applies to residual gaps (`scoring/error_taxonomy.md`
buckets, atlas vocabulary):

- **Computation / Retrieval**: none found — checklist and hypothesis values verified
  at value+date+accession level against `~/aaer-data/SCOR/xbrl/CIK0001158172.json` (§3).
- **Interpretation**: (a) DIM2=1 — mechanism family missed: DSO-inferred premature
  recognition vs actual NMT valuation + side agreements
  (`scoring/grades/main/case_01.json` rationale); the NMT composition was not
  visible in the XBRL-only deck, so the DATA-vs-MODEL bucket split under R1 is an
  owner call. (b) Main-frame DIM3=1 — hypothesis 1 blends active recognition with an
  estimate-omission element (allowance not scaling), mapping "mixed" against the
  key's "active(revenue)". (c) Cross-frame score divergence (55 vs 45) straddles the
  flag band; the perturbed grade records DIM1=0.
- **Label-noise**: none — AAER-confirmed tier, settled order with $5,000,000 civil
  penalty (33-10692.pdf.txt §IV.B).
- **Suspected-memorization**: the two sealed probe draws disagree for this case
  (L-5: probe verdicts vary across draws). Draw 1,
  `scoring/probe_results/recognition/case_01.json`: company_guess "comScore, Inc.",
  confidence "high". Draw 2, `analysis/name_probe_results.json` row case_01: guess
  "SolarWinds, Inc.", confidence "medium", recognized: false. Both grade records set
  memorization_suspect_condition2: false. The −10 perturbation delta is the D8
  memorization-contribution measurement; no pass/fail reading is applied.

`analysis/error_analysis.md` context: §2 table — "SCOR | 55 | 1 | 계정 영역(매출/AR)·
방향 일치, 특이 기제(barter $34.5M)는 미포착"; §3 — revenue-recognition cases 4/4
detected; §4 — decisive evidence first/complete at the 2015-02 10-K, 4 quarters
pre-revelation.

## 7. CPA JUDGMENT — human_finalized: false

Draft, unaudited work product until owner sign-off (PROJECT.md §7).

- The flag landed for a directionally right but mechanically generic reason:
  revenue overstated with receivables outrunning sales. NMT/barter valuation abuse
  is quantitatively quiet — fabricated revenue enters at a self-defined "fair value"
  with no cash trail — so an XBRL-only analyst plausibly cannot get closer than
  "revenue-side overstatement". **[OWNER REVIEW]**
- The grader notes the FY2013 anchor "predates the manipulation window (2014-02 to
  2016-02)". The order softens this: the first NMT was "effective December 20, 2013"
  (¶12) and the Restatement covered FY2013 (¶5), so the FY2013 year-end divergence
  is not clearly outside the affected periods — a criteria-side question for the
  DIM2 coverage note. **[OWNER REVIEW]**
- Hypothesis 3's "understated" direction reads as over-reach against a company the
  order describes as inflating revenue to beat consensus (¶1, ¶9); it also dragged
  the main-frame genre mapping to "mixed" (DIM3=1). **[OWNER REVIEW]**
- Score 55 vs 45 straddles the threshold; per D8 the delta is evidence about
  memorization contribution, and with the two probe draws split (comScore/high vs
  SolarWinds/false), the recognition picture is unresolved. **[OWNER REVIEW]**

## 8. AUDIT TRANSLATION

Procedures the flag would motivate (framed as procedures, not conclusions):

- Examine all non-monetary / data-exchange agreements: fair-value support within
  reasonable limits and commercial-substance analyses (ASC 845-10-30-3/-30-4);
  corroborate counterparty use of and interest in the data received.
- Counterparty confirmations covering the full contract population, including
  related/linked contracts, side agreements, and post-quarter delivery obligations.
- Revenue cutoff testing at quarter-ends against delivery evidence; deferred-revenue
  timing and multiple-element allocation (BESP) testing.
- Recompute the allowance for doubtful accounts against an AR aging; investigate the
  $0 allowance quarters against $77-98M receivables.
- Analytics on the consensus-vs-reported revenue gap by quarter; inquiry into
  incentive plans tied to revenue targets; management-override controls over
  disclosed performance metrics (customer count, vCE).

## 9. FINANCIAL STATEMENT IMPACT

From the enforcement text actually read (33-10692.pdf.txt): the FY2017 Form 10-K
filed March 23, 2018 "included a restatement (the 'Restatement')" providing
"restated and corrected financial information for the years ended December 31, 2014
and 2013", restating "certain information for the quarters ended March 31, June 30,
and September 30, 2015" and adjusting the FY2015 Form 8-K information; "In total,
Comscore reversed approximately $50 million in revenue" (¶5). Direction: revenue
overstated — components "over $34.5 million" (NMTs, ¶2) and "approximately $12
million in 2015" (linked monetary contracts, ¶3). Misstated filings enumerated at
¶36 (FY2013/FY2014 10-Ks; Q1-Q3 2014 and Q1-Q3 2015 10-Qs; 2016-02-17
earnings-release 8-K). Restated per-line-item, per-period amounts: not determinable
— the sealed order does not tabulate them, and no restatement filing text is among
the sealed sources read.

---
*Entry status: drafted (sections 7–9 pending owner finalization).*
*채점: Claude 보조 + 인간 최종 확정. 교육·정보 목적, 투자 자문 아님.*
