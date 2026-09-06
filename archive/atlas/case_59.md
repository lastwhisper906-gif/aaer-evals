# atlas/case_59.md — The Hain Celestial Group, Inc. (HAIN) — wave-2 treatment T23

Authored by Claude Code, pending human audit (D15). Analytical document under D106 ② — not a scored output. 본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).

## 1. CASE HEADER

| field | value |
|---|---|
| Case ID (anonymized frame) | case_59 (scoring ID T23) |
| Cohort | wave-2 |
| Outcome class | TP (main frame, flag at score ≥50) |
| Ground-truth tier | AAER-confirmed (SEC order Exchange Act Rel. 84781 / AAER-3997, December 11, 2018) |
| Frozen score | score 58 (`runs/wave2/scores/case_59.json`, run `original-case_59-r1`, risk_tier "elevated") |
| Grade record | `scoring/grades_wave2/case_59.json` (human_finalized: true, finalized 2026-07-09 via RP-13 workbench; dim1=1, dim2=1, dim3=0 "omission-estimate", dim4=3) |

Company: The Hain Celestial Group, Inc., CIK 0000910406, cutoff 2016-08-14
(`data/candidates/candidates_wave2.json` T23; `data/evaluatee/cases_wave2.json` case_59).
`analysis/error_analysis_wave2_holdout.md` does not discuss this case individually.

## 2. ACTUAL EVENT

In the Matter of The Hain Celestial Group, Inc., Admin. Proc. 3-18921; Exchange Act
Rel. 84781 / AAER 3997 (Dec. 11, 2018). Sealed local text:
`~/aaer-data/HAIN/34-84781.pdf.txt` (manifest-pinned, `data/manifests/aaer_data_manifest.json`).
From at least 2014 until May 2016, Hain U.S. sales personnel gave sales incentives to
"certain distributors to promote sales at the end of quarters." (Summary, line 60).
"EOQ" (end-of-quarter) sales "included asking Distributors 1 and 2 to purchase specific dollar
values of inventory by quarter-end, in exchange for additional incentives." (¶5, lines 116-117):
"cash incentives (up to $500,000)", "extended payment terms (up to 90 days)",
"discounts off list price (up to 20% off)", and spoils coverage (¶5, lines 118-120) — none
"improper; however, they could have financial reporting implications." (¶5, lines 121-122).
"Distributor 1 purchased 52-64% of its" inventory "in or around the last month of the quarter"
(¶10, lines 176-177); arrangements were memorialized only in emails or orally (¶9, ¶15).
"In August 2016, Hain self-reported the incentives practice to the SEC and" delayed its FY2016
reporting (Summary, line 61); the review covered "whether the revenue associated with those
incentives was accounted for in the correct" period (¶19, lines 251-252). In its FY2016 10-K
(June 22, 2017) Hain determined "no financial restatements were required, but corrected
immaterial errors to prior period" financial statements, and disclosed material weaknesses
including "an ineffective control environment and ineffective controls related to U.S."
revenue recognition (¶20, lines 258-261).

Charges: Exchange Act Sections 13(b)(2)(A) — books and records, "which requires Hain to make
and keep books, records and accounts which, in reasonable" detail (¶23, line 286) — and
13(b)(2)(B) — "system of internal accounting controls" (¶24, line 290). No fraud charge, no
penalty (Section IV.B), no restatement. Registered summary:
`data/candidates/candidates_wave2.json` T23 `scheme_summary` (undocumented end-of-quarter
incentives to the two largest distributors "to pull inventory forward and meet internal
quarterly sales targets"); `scheme_type`: revenue_recognition; manipulation period 2014-01
to 2016-06. GAAP topics: the order cites no codification section — it references "potential
revenue recognition implications." (¶11, line 184; also ¶16) and GAAP conformity generically
(¶24); it names neither ASC 605 nor ASC 606, so no pre/post-ASC-606 framing is asserted here
beyond the conduct period (FY2014–FY2016) stated in the order.

## 3. SIGNALS AVAILABLE PRE-CUTOFF

Cutoff 2016-08-14 (the day before the ¶19 self-report of August 15, 2016). Sealed data
basis: `~/aaer-data/HAIN/xbrl/CIK0000910406.json` (XBRL companyfacts) +
`~/aaer-data/HAIN/edgar/` submissions JSONs (chronology). Pre-cutoff, at accession level:

- **Receivables outgrew revenue into the manipulation period**: AccountsReceivableNetCurrent
  $166.677M (2012-06-30, accn 0000910406-13-000023) → $287.915M (2014-06-30, accn
  0000910406-14-000035) → $320.197M (2015-06-30, accn 0000910406-15-000028) → $360.964M
  (2016-03-31, accn 0000910406-16-000117); Revenues $1,378.247M (FY2012) → $2,153.611M
  (FY2014) (both accn 0000910406-14-000035) → $2,688.515M (FY2015, accn 0000910406-15-000028).
  Extended payment terms of the kind described at ¶5 would surface here, though the deck
  cannot show terms.
- **Allowance compression**: AllowanceForDoubtfulAccountsReceivableCurrent $2.661M
  (2012-06-30, accn 0000910406-13-000023) → $1.586M (2014-06-30, accn 0000910406-14-000035)
  → $0.896M (2015-06-30, accn 0000910406-15-000028) → $1.049M (2016-03-31, accn
  0000910406-16-000117), against the near-doubling receivables above.
- **Inventory and margin**: InventoryNet $186.440M (2012-06-30, accn 0000910406-13-000023)
  → $250.175M (2013-06-30, accn 0000910406-14-000035) → $394.958M (2016-03-31, accn
  0000910406-16-000117); GrossProfit $382.470M on Revenues $1,378.247M (FY2012, accn
  0000910406-14-000035) vs $618.617M on $2,688.515M (FY2015, accn 0000910406-15-000028).
- **Chronology friction**: NT 10-K 2007-08-29 (accn 0001144204-07-046999), NT 10-Q
  2007-11-09, 10-K/A 2008-03-26 and 2008-10-28; SEC UPLOAD 2016-03-15 (accn
  0000000000-16-068350), CORRESP 2016-03-24 (accn 0000910406-16-000109), UPLOAD 2016-04-08
  shortly before cutoff (`CIK0000910406.json` / `CIK0000910406-submissions-001.json`).

Not visible in this sealed set: intra-quarter sales concentration (¶10), distributor-level
terms, and U.S.-segment growth deceleration (¶2, "from a high of 17% sales growth (FY 2014),
to 6.6% sales growth (FY" 2015 to negative in 1H FY2016, lines 89-91) — segment sales are
not among the sealed us-gaap facts. This section describes the information set — it does
not re-score the case.

## 4. WHAT THE LLM CAUGHT

Frozen output `runs/wave2/scores/case_59.json`: `misstatement_probability`: 58 (legacy v1
key — an uncalibrated ordinal score; see specs/RISK_SCORE_SEMANTICS.md) = score 58,
risk_tier "elevated" — at/above the flag threshold of 50, hence TP. CL1/CL2/CL4/CL6/CL7
flagged; CL3/CL5 no_flag; CL8 sufficient. Cited evidence values re-verified against the
sealed XBRL facts file at value+date+accession level; none fabricated.

| model claim (verbatim) | enforcement/restatement reference | match quality |
|---|---|---|
| "This pattern is consistent with under-reserving for doubtful accounts, which would understate bad debt expense and overstate net receivables and net income." (hypothesis 1, top-ranked, "overstated") | Order describes receivables-side conduct — "extended payment terms (up to 90 days)" (¶5, line 119; ¶12, ¶17) on EOQ sales — but alleges no allowance under-reserving; account area shared, mechanism not | right account wrong mechanism |
| "consistent with either channel-stuffing of distributors/retailers (recognizing revenue on inventory pushed into the channel) or delayed write-downs of slow-moving/obsolete inventory" (hypothesis 2, "overstated") | ¶5 (lines 116-117): asking distributors "to purchase specific dollar values of inventory by quarter-end, in exchange for additional incentives."; ¶6-¶7 renegotiated purchasing targets; scheme_summary "pull inventory forward" — the channel-stuffing limb is the enforcement mechanism (the write-down limb has no counterpart) | exact mechanism |
| "aggressive purchase price allocation to intangibles/goodwill in serial M&A" (hypothesis 3, "overstated") | No counterpart in the order (no intangibles/goodwill/PPA finding) | unrelated |
| "Recurring SEC CORRESP/UPLOAD correspondence in early-to-mid 2016 shortly before the analysis cutoff, alongside a history of prior 10-K/A amendments and NT filings" (top_signals) | Order mentions no comment-letter correspondence; 2007-2008 NT/10-K/A history precedes the FY2014-2016 relevant period | unrelated |

Notes: grade dim2=1 — top hypothesis "is in the receivables/revenue-adjacent account area,
so 'correct account area' (1) applies"; the grader's coverage note records that
"hypothesis #2 explicitly posits 'channel-stuffing of distributors,' a much closer match to
the enforcement description, but rubric restricts grading to the top-ranked hypothesis"
(`scoring/grades_wave2/case_59.json`). dim3=0: top-hypothesis genre omission-estimate vs
the answer key's active scheme.

## 5. WHAT THE LLM MISSED

From the sealed §3 information set: **none identified from sealed evidence** as an
unsurfaced signal class — the receivables/allowance, inventory/margin, and
chronology-friction axes were all surfaced (§4). The residual errors are ordering and
framing, not omission: the enforcement-matching mechanism (channel-stuffing) was surfaced
but ranked second, behind the allowance-estimate story, and framed on inventory/COGS line
items rather than revenue timing (costing dim2 and dim3). The scheme's most direct
footprints — intra-quarter sales concentration (¶10) and U.S.-segment growth deceleration
(¶2) — are absent from the sealed XBRL aggregates (§3); insufficient sealed evidence to
name either as a missable signal.

## 6. ERROR TAXONOMY

Per `scoring/error_taxonomy.md` (R1→R2→R3), atlas vocabulary. The case is a TP; the
taxonomy applies to the dimension losses (dim2=1, dim3=0), not the outcome:

- **Primary — interpretation (MODEL)**: the data supporting the closer hypothesis existed
  and was quoted by the model itself (R1 pass); the pre-fixed rubric's top-ranked-hypothesis
  restriction forces a unique grade (R2 pass); ranking the reserve-estimate narrative above
  the channel-stuffing narrative is a model interpretation/ordering error (R3).
- **Computation / retrieval**: none identified — all cited values re-verified against the
  sealed XBRL at value+date+accession level (§4); dim4=3.
- **Label-noise**: none — AAER-confirmed tier (settled Commission order); nuance for the
  record: a books-and-records / internal-controls order with no restatement (¶20, ¶23-24),
  registered as `scheme_type` revenue_recognition.
- **Suspected-memorization**: recognition probe — the single stored draw
  `scoring/probe_results_wave2/recognition/case_59.json` — guessed "The Hain Celestial
  Group, Inc." with confidence "medium" (correct company; noted for the owner-facing
  record); verbatim probe `scoring/probe_results_wave2/verbatim/case_59.json`: known:
  false, recall fields null. Grade memorization_suspect_condition2: false — reasoning
  "cites only pre-cutoff filings (latest 2016-05-10); no mention of the August 2016
  revelation, the 2018 SEC enforcement (AAER-3997 / PR 2018-277), or outcomes".

## 7. CPA JUDGMENT — human_finalized: false

Draft, unaudited work product until owner sign-off (PROJECT.md §7).

- The TP is a right-answer / second-best-reason outcome: score 58 crossed the threshold on
  an allowance-compression story the order does not allege, while the actual mechanism
  (quarter-end pull-forward via undocumented incentives) sat in hypothesis 2. Whether flag
  credit should be discounted for the ordering, or the receivables-axis anchoring counted
  as substantively on-target (extended terms and spoils rights sit in that account area),
  is the core owner call — the rubric's top-ranked-hypothesis restriction (§4 notes) is the
  pre-registered design choice that made this cost dim2/dim3. **[OWNER REVIEW]**
- The enforcement outcome was books-and-records/ICFR with no restatement, no fraud charge,
  and errors characterized as immaterial (¶20, ¶23-24). Whether a score-58 "elevated" flag
  is the right calibration for a no-restatement outcome — or the label tier (AAER-confirmed,
  revenue_recognition) fully justifies TP treatment — merits a trust-boundary note. **[OWNER REVIEW]**
- The allowance-to-receivables compression the model led with ($2.661M→$0.896M against
  $166.677M→$320.197M) is a genuine sealed-data pattern; on a deck without terms or segment
  data, reading it as reserve risk rather than terms-driven AR aging is a defensible analyst
  posture even though it is not what the order found. **[OWNER REVIEW]**
- Hypothesis 2's line-item framing (Hain's own inventory/COGS "overstated") misplaces the
  channel-stuffing footprint — the inventory build the order describes is distributor-held
  (¶22: "Distributor 1 went from holding approximately $74 million in Hain" inventory in
  June 2016, to $47M in June 2017), not Hain's InventoryNet. **[OWNER REVIEW]**

## 8. AUDIT TRANSLATION

Procedures the flag would motivate — procedures, not conclusions:

- Distributor confirmations that explicitly cover side terms — return/spoils rights beyond
  the 1% contractual off-invoice discount, cash incentives, discounts, payment terms (the
  ¶5 incentive set) — with inquiry beyond the signed annual contract, given terms
  memorialized only in email or orally (¶9, ¶15).
- Revenue cutoff testing weighted to the final month of each quarter (¶10 concentration);
  month-within-quarter sales disaggregation for top distributors.
- Sales-incentive completeness: reconcile trade-spend/incentive accruals to correspondence
  and payments (EOQ spoils grew "from $0.5 million in FY 2013, to $0.8 million" in FY2014
  to $1.6M in FY2016, ¶8; Distributor 2 quarterly discounts "from around $200,000 to
  nearly $1.5" million by Q4 FY2016, ¶14).
- AR aging and subsequent-cash-receipt testing keyed to extended (60-90 day) terms;
  allowance recomputation under that terms profile; ICFR walkthroughs of sales-to-finance
  communication of contract modifications (¶12, ¶17) and concession-approval thresholds.

## 9. FINANCIAL STATEMENT IMPACT

From the sealed order text: **no restated line items exist** — "no financial restatements
were required, but corrected immaterial errors to prior period" financial statements (¶20,
line 258). The order does not identify or quantify those immaterial corrections by line
item, so their amounts and direction are **not determinable** from the sealed sources read.
Determinable from the order: ICFR material weaknesses disclosed in the FY2016 10-K (¶20,
lines 259-261); no civil penalty (Section IV.B); incentive magnitudes as quoted in §8
(¶8, ¶14) — findings about conduct and controls, not restated financial-statement amounts.

---
*Entry status: drafted (sections 7–9 pending owner finalization).*
*채점: Claude 보조 + 인간 최종 확정. 교육·정보 목적, 투자 자문 아님.*
