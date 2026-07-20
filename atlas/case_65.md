# atlas/case_65.md — Weatherford International Ltd. (Switzerland) (WFT) — wave-2 treatment T04

Authored by Claude Code, pending human audit (D15). Analytical document under D106 ② — not a scored output. 본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).

## 1. CASE HEADER

| field | value |
|---|---|
| Case ID (anonymized frame) | case_65 (scoring ID T04) |
| Cohort | wave-2 |
| Outcome class | TP (main frame, flag at score ≥50) |
| Ground-truth tier | AAER-confirmed (Securities Act Rel. 33-10221 / Exchange Act Rel. 78944 / AAER-3806, September 27, 2016) |
| Frozen score | score 74 (`runs/wave2/scores/case_65.json`, run `original-case_65-r1`, risk_tier "elevated") |
| Grade record | `scoring/grades_wave2/case_65.json` (human_finalized: true, finalized 2026-07-09 via RP-13 workbench; dim1=2, dim2=0, dim3=null mapped_genre "mixed" — flagged for human auditor, dim4=3) |

Company: Weatherford International Ltd. (Switzerland), CIK 0001453090, cutoff 2011-02-28
(`data/candidates/candidates_wave2.json` T04; `data/evaluatee/cases_wave2.json` case_65).
Deep-dive dossier: `scoring/dossiers/WFT.md` (1차 소스 재검증 2026-07-03, pending human
sign-off). `analysis/error_analysis_wave2_holdout.md` does not discuss this case individually.

## 2. ACTUAL EVENT

In the Matter of Weatherford International plc f/k/a Weatherford International Ltd., James
Hudgins, CPA, and Darryl Kitay, CPA; Admin. Proc. 3-17582; AAER-3806 (Sept. 27, 2016). Sealed
local text: `~/aaer-data/WFT/33-10221.pdf.txt` (manifest-pinned,
`data/manifests/aaer_data_manifest.json`). "Between 2007 and 2012, Weatherford, a large
multinational provider of oil and natural gas equipment and services, issued false financial
statements that inflated its earnings by over $900 million" (¶1, lines 76-78). Core scheme
(¶24, lines 315-323): "Throughout 2007-2010, Hudgins and Kitay made these manual post-closing
adjustments within a line item on the consolidated tax provision labeled intercompany
'dividend exclusion.'" These adjustments "ranged from $286 million to $439 million per year,"
sat "within Weatherford's corporate elimination account, which was known as the 'Eliminations
region,'" were "tax effected at 35%, which falsely lowered Weatherford's year-end provision
for income taxes by $100 million to $154 million each year," and "overstated net income,
understated ETR and tax expense, and ultimately created a $461 million phantom income tax
receivable." Entities: "two different Weatherford Luxembourg entities" (FY2007, ¶30),
"different Luxembourg entities" (FY2008, ¶39), "a Bermuda entity within Weatherford's
Eliminations region" (FY2009-10, ¶43). Motive: to "better align with analysts' expectations
and Weatherford's previously-announced projected results" (¶25). Revelation: "On March 1,
2011, Weatherford filed a Form 8-K" announcing the 2007-2010 restatement and "that a material
weakness existed in its ICFR for the accounting of income taxes"; stock "dropped nearly 11%
to $21.14" (¶55, lines 637-640).

Charges (¶7, lines 142-146): antifraud (Exchange Act §10(b)/Rule 10b-5, Securities Act
§17(a)), reporting (§13(a) and Rules 12b-20, 13a-1, 13a-11, 13a-13), books and records
(§13(b)(2)(A)), internal controls (§13(b)(2)(B)); civil penalty "$140,000,000" (Section IV.K,
line 1118). Registered summary: `data/candidates/candidates_wave2.json` T04 `scheme_summary`
(tax "plug" adjustments, Luxembourg FY2007-08 / Bermuda FY2009-10 within the Eliminations
region — locus per dossier re-verification); `scheme_type`: liability_understatement,
asset_overstatement; manipulation period 2007-2012 (the plug fraud itself spanned FY2007-2010
— ¶2; dossier nuance note). GAAP topics as named by the order: FIN 18, "Accounting for Income
Taxes in Interim Periods" (¶28) and FAS 109, "Accounting for Income Taxes" (¶29); footnote 4
states both "were superseded by ASC Topic 740" upon codification (lines 379-381).

## 3. SIGNALS AVAILABLE PRE-CUTOFF

Cutoff 2011-02-28 (the day before the March 1, 2011 revelation, ¶55). Sealed basis for this
section: `~/aaer-data/WFT/edgar/` submissions JSONs (chronology only; the deck entry
`data/evaluatee/cases_wave2.json` case_65 carries identifiers and cutoff, no numeric
payload). Pre-cutoff, at accession level:

- **Amendment chronology (Switzerland CIK 1453090)**: 10-Q/A 2009-09-01 (accn
  0000950123-09-040151, "AMENDMENT TO FORM 10-Q"); 10-K FY2009 2010-03-01 (accn
  0000950123-10-019083) amended by 10-K/A 2010-04-30 (accn 0000950123-10-042030); 10-Q/A
  2010-09-01 (accn 0000950123-10-083078). The dossier (xbrl_available field) records the
  2010-09-01 amendment as restating Q2 2010/2009 "due to errors in the Company's accounting
  for income taxes" — quoted there from a post-cutoff 2011 10-Q/A, so the tax-attribution
  text itself is post-cutoff-sourced in the sealed set.
- **SEC comment-letter cycle through the cutoff**: UPLOAD 2010-05-28 (accn
  0000000000-10-030075), CORRESP 2010-06-10 (accn 0000950123-10-057341), CORRESP 2010-06-21,
  UPLOAD 2010-07-23, CORRESP 2010-08-06, UPLOAD 2010-10-08, CORRESP 2010-10-25, UPLOAD
  2011-01-10, CORRESP 2011-01-26 (accn 0000950123-11-005538), UPLOAD 2011-02-23 (accn
  0000000000-11-011608) — the last five days before cutoff.
- **Predecessor amendment history (Bermuda CIK 1170565)**: 10-K/A 2003-06-26 (accn
  0000950129-03-003369), 2004-06-14 (accn 0000950129-04-004037), 2005-06-14 (accn
  0000950129-05-006182).

Not visible in this sealed §3 set: the numeric XBRL facts the frozen output cites, the
ETR-vs-statutory-rate build-up, the intercompany "dividend exclusion" line, and the growing
current-income-tax debit balance the order says "should have raised red flags" (¶45) —
insufficient sealed evidence here to reconstruct those as an independent pre-cutoff
information set (the grade record attests the cited values were "arithmetically verifiable
provided data points"). This section describes the information set — it does not re-score
the case.

## 4. WHAT THE LLM CAUGHT

Frozen output `runs/wave2/scores/case_65.json`: `misstatement_probability`: 74 (legacy v1 key
— an uncalibrated ordinal score; see specs/RISK_SCORE_SEMANTICS.md) = score 74, risk_tier
"elevated" — above the flag threshold of 50, hence TP. CL1-CL4 and CL7 flagged (CL7 the sole
"high" confidence); CL5/CL6 no_flag; CL8 sufficient. Cross-check: the output's cited
NetIncomeLoss values equal the order's pre-restatement figures — 1,070,606K (2007), 253,766K
(2009) vs "1,070.6", "253.8", and its Q1-Q3 2010 quarterly figures sum to 78,273K vs "78.3"
(¶56 table, lines 660-663).

| model claim (verbatim) | enforcement/restatement reference | match quality |
|---|---|---|
| "Potential premature/aggressive revenue recognition or delayed write-down of receivables during a period of declining top-line" (hypothesis 1, top-ranked, "overstated") | No counterpart — the order alleges income-tax provision manipulation (¶24), no revenue-recognition or receivables conduct | unrelated |
| "acquisition-related goodwill/intangibles were not adequately tested for impairment, potentially overstating non-current assets" (hypothesis 2, "overstated") | No counterpart — no goodwill/impairment finding in the order | unrelated |
| "underlying control weaknesses, historically most often related to complex multinational tax/consolidation accounting, potentially understating tax liabilities and overstating reported net income" (hypothesis 3, "overstated") | ¶24 (lines 320-323): "falsely lowered Weatherford's year-end provision for income taxes by $100 million to $154 million each year … overstated net income, understated ETR and tax expense"; ¶2 (lines 87-88): "a material weakness existed in its internal control over financial reporting ('ICFR') for the accounting of income taxes" — account family and direction match; the deliberate ETR-guidance "plug" mechanism (¶23-25) is not identified | right account wrong mechanism |
| "Chronic pattern of financial statement amendments (10-K/A, multiple 10-Q/A) plus heavy, recurring SEC comment-letter correspondence (CORRESP/UPLOAD) through 2010-2011, indicating persistent control/reporting weaknesses" (top_signals) | Chronology confirmed in sealed `~/aaer-data/WFT/edgar/` JSONs (§3); the dossier records the 2010-09-01 10-Q/A as an income-tax restatement — a genuine symptom of the scheme, with no mechanism asserted | right direction only |

Grade notes (`scoring/grades_wave2/case_65.json`): dim2=0 — top-ranked hypothesis "unrelated
to the answer key's mechanism of manual post-closing income-tax provision plugs"; coverage
note: hypothesis #3 "substantially matches account+direction and would likely score 2 if
top-ranked, but rubric grades top-ranked only." dim3: mapped_genre "mixed" but answer-key
genre_tag_row null → score null, flagged for human auditor.

## 5. WHAT THE LLM MISSED

Within the sealed §3 set: **none identified from sealed evidence** as an unsurfaced signal
class — the amendment history (both CIK eras), the CORRESP/UPLOAD cycle, and the quantitative
axes the model cited were all surfaced (§4). The residual error is ordering, not omission:
the income-tax hypothesis ranked third, behind two stories with no enforcement counterpart.
The scheme's most direct footprints — the ETR-vs-FAS-109 gap (¶30, ¶39), the "dividend
exclusion" line (¶24), the "multi-year large debit balance" in current income taxes (¶45) —
are absent from the sealed §3 sources and, per the model's own hypothesis 3, income tax
accounts were "not directly itemized in provided data"; insufficient sealed evidence to name
any of them as a missable signal.

## 6. ERROR TAXONOMY

Per `scoring/error_taxonomy.md` (R1→R2→R3), atlas vocabulary. The case is a TP; the taxonomy
applies to the dimension losses (dim2=0, dim3=null), not the outcome:

- **Primary — interpretation (MODEL), for dim2**: the chronology signals feeding the tax
  hypothesis were in the provided data and quoted by the model (R1 pass); the pre-fixed
  top-ranked-hypothesis rubric forces a unique grade (R2 pass); ranking the revenue and
  goodwill narratives above the income-tax narrative is an interpretation/ordering error (R3).
- **Criteria-side gap, for dim3**: score null because the answer key's genre_tag_row is null
  — a key-coverage gap, not a model error; flagged for human auditor.
- **Computation / retrieval**: none identified — dim4=3; grade rationale calls the cited
  values "specific, arithmetically verifiable provided data points". Chronology claims
  re-verified here against the sealed edgar JSONs (both CIKs). The grader's borderline item —
  CL7's CORRESP 2011-01-26 / UPLOAD 2011-02-23 entries postdating the last used document —
  both exist in the sealed chronology and both predate the 2011-02-28 cutoff; whether they
  were in the delivered payload is not verifiable from the sealed deck entry (metadata only).
  Retrieval hygiene nuance: two CL7 evidence rows carry source_accession_no "N/A".
- **Label-noise**: none — AAER-confirmed tier (settled Commission order); nuance: the
  dossier's 1차 소스 재검증 corrected the plug-entity locus to Luxembourg FY2007-08 /
  Bermuda FY2009-10, all within the Eliminations region (¶30, ¶39, ¶43-44).
- **Suspected-memorization**: recognition probe — the single stored draw
  `scoring/probe_results_wave2/recognition/case_65.json` — company_guess "unknown",
  confidence "low"; verbatim probe `scoring/probe_results_wave2/verbatim/case_65.json`:
  known: false, all recall fields null. Grade memorization_suspect_condition2: false —
  reasoning "never mentions the restatement, enforcement order, or outcome."

## 7. CPA JUDGMENT — human_finalized: false

Draft, unaudited work product until owner sign-off (PROJECT.md §7).

- The TP is a right-flag / third-best-reason outcome: score 74 crossed the threshold led by
  revenue/receivables and goodwill stories the order does not allege, while the income-tax
  hypothesis — matching account family and direction — sat third. Whether the pre-registered
  top-ranked-only rubric fairly prices this, or hypothesis 3 deserves recognized standing in
  the trust-boundary narrative, is the core owner call. **[OWNER REVIEW]**
- The scheme was structured to defeat aggregate-level screening: the plug existed precisely
  to make reported ETR match previously "touted" guidance (¶3, ¶25), and its balance-sheet
  residue sat in intercompany elimination entities and the current-income-tax balance — not
  itemized in the deck. The strongest genuinely scheme-linked pre-cutoff signal was the
  amendment chronology (the 2010 10-Q/A being an income-tax restatement per the dossier),
  which the model made its only high-confidence flag (CL7) and first top_signal — arguably
  the correct read of the available set. **[OWNER REVIEW]**
- The quantitative flags (receivables +2.5% vs revenue -8.1%; inventory +7.3%; gross margin
  ~20.6%→~8.0%) coincide with a 2009 downturn at "a large multinational provider of oil and
  natural gas equipment and services" (¶1) — a false-mechanism/true-flag pattern that can
  inflate apparent hit quality if not discounted. **[OWNER REVIEW]**
- Direction bookkeeping: hypothesis 3's "understating tax liabilities and overstating
  reported net income" matches both registered scheme_type limbs at account-family level —
  the order describes a "$461 million debit balance to Weatherford's current income tax
  payable, which Respondents reclassified as an income tax receivable" (¶45): an understated
  liability presented as an overstated asset. **[OWNER REVIEW]**

## 8. AUDIT TRANSLATION

Procedures the flag would motivate — procedures, not conclusions:

- Manual and top-side journal-entry testing over the consolidated tax provision, targeting
  post-closing adjustments booked to intercompany elimination entities, with substantiation
  required for each "dividend exclusion" line component (¶24, ¶30).
- Recompute the year-end provision under FAS 109/ASC 740 and reconcile it to the FIN 18
  interim ETR path; investigate year-end gaps closed by late adjustments against previously
  communicated ETR guidance (¶28-29, ¶31).
- Reconcile current income taxes payable/receivable to jurisdictional returns and refund
  claims — the expanded procedure that uncovered the phantom receivable ("a reconciliation of
  Weatherford's current taxes payable (and receivable) accounts", ¶54); treat persistent
  multi-year debit balances in current tax payable as a standing red-flag analytic (¶45).
- Chronology-driven scoping: repeated amendments plus a sustained SEC comment-letter cycle
  (§3) motivate ICFR walkthroughs of the tax close and evaluation of prior-amendment root
  causes before reliance on year-end tax estimates.

## 9. FINANCIAL STATEMENT IMPACT

Determinable from the sealed order text (`~/aaer-data/WFT/33-10221.pdf.txt`):

- **First Restatement** (announced 2011-03-01, filed 2011-03-08): "reduced previously
  reported net income by approximately $500 million," of which "$461 million … resulted from
  a four-year income tax accounting fraud" (¶2, lines 88-91). Net income by period (¶56
  table, lines 660-663): 2007 $1,070.6M → $940.6M (13.8%); 2008 $1,393.2M → $1,246.5M
  (11.3%); 2009 $253.8M → $170.1M (42.6%); Q1-Q3 2010 $78.3M → $(21.6)M (462.0%).
- **Tax expense understated by year**: $153.9M (2007, ¶31), $106.3M (2008, ¶39), $101.6M
  (2009) and $100.3M (2010) (¶43).
- **Balance sheet**: $461M phantom income tax receivable (¶24, ¶45); "The year-end 2010
  current income tax balance of $441,553,629 included the $461 million phantom receivable
  and a $20 million credit balance to 'U.S. Income Tax Payable.'" (footnote 5, lines 573-575).
- **Second Restatement** (filed 2012-03-15): "a $256 million drop in net income from
  2007-2011 as a result of additional errors in its income tax accounting" (¶4); **Third
  Restatement** (issued 2012-12-17): net income reduced "by an additional $186 million" (¶5).
  Cumulative: earnings inflated "by over $900 million" 2007-2012 (¶1). Direction: net income,
  EPS, and income tax receivable overstated; income tax expense, ETR, and current income
  taxes payable understated (¶1, ¶24, ¶45).

---
*Entry status: drafted (sections 7–9 pending owner finalization).*
*채점: Claude 보조 + 인간 최종 확정. 교육·정보 목적, 투자 자문 아님.*
