# atlas/case_66.md — Under Armour, Inc. (UAA) — wave-2 treatment T29

Authored by Claude Code, pending human audit (D15). Analytical document under D106 ② — not a scored output. 본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).

## 1. CASE HEADER

| field | value |
|---|---|
| Case ID (anonymized frame) | case_66 (scoring ID T29) |
| Cohort | wave-2 |
| Outcome class | TP (main frame, flag at score ≥50) |
| Ground-truth tier | AAER-confirmed (Securities Act Rel. 33-10940 / Exchange Act Rel. 91741 / AAER-4220, May 3, 2021) |
| Frozen score | score 55 (`runs/wave2/scores/case_66.json`, run `original-case_66-r1`, risk_tier "elevated") |
| Grade record | `scoring/grades_wave2/case_66.json` (human_finalized: true, finalized 2026-07-09 via RP-13 workbench; dim1=1, dim2=2, dim3=1 mapped_genre "active", dim4=3) |

Company: Under Armour, Inc., CIK 0001336917, cutoff 2019-11-02 (`data/candidates/candidates_wave2.json` T29; `data/evaluatee/cases_wave2.json` case_66). `analysis/error_analysis_wave2_holdout.md` does not discuss this case individually.

## 2. ACTUAL EVENT

In the Matter of Under Armour, Inc.; Admin. Proc. File No. 3-20278; AAER-4220 (May 3, 2021),
settled cease-and-desist order; sealed local text `~/aaer-data/UAA/33-10940.pdf.txt`
(manifest-pinned, `data/manifests/aaer_data_manifest.json`). "This matter concerns Under
Armour's failure to disclose material information about its revenue management practices that
rendered statements it made misleading" (¶1, lines 55-56). Mechanism (¶2, lines 65-70): Under
Armour "sought to accelerate, or 'pull forward,' existing orders that customers had requested
be shipped in future quarters"; "For six consecutive quarters from the third quarter of 2015
through the fourth quarter of 2016 (the 'Relevant Period') … Under Armour pulled forward
approximately $408 million in orders" (¶3, lines 71-74), aided by "extended payment terms and
discounts" (¶10, lines 131-133). Critically, footnote 2 (lines 90-91): "This Offer does not
make any findings that revenue from these sales was not recorded in accordance with generally
accepted accounting principles ('GAAP')" — a disclosure case, not an alleged GAAP
misstatement of the sales themselves.

Charges (¶46-48, lines 385-419): Securities Act §17(a)(2)-(3) (non-scienter), Exchange Act
§13(a) and Rules 13a-1, 13a-11, 13a-13, 12b-20; the MD&A failure is grounded in Reg S-K Item
303 ("any known trends or uncertainties," ¶48, lines 403-406). Sanctions: cease-and-desist
plus "a civil penalty of $9,000,000.00" (Section IV.B, lines 430-432); no restatement ordered
or described. GAAP topics: none named by the order (fn.2). Registered summary:
`data/candidates/candidates_wave2.json` T29 `scheme_summary` ("SEC did not allege the sales
themselves violated GAAP"); `scheme_type`: disclosure_only, revenue_recognition; manipulation
period 2015-07-01 to 2016-12-31.

## 3. SIGNALS AVAILABLE PRE-CUTOFF

Cutoff 2019-11-02. Sealed basis: the deck entry `data/evaluatee/cases_wave2.json` case_66
carries identifiers and cutoff only (no numeric payload); numeric and chronology series sit
in `~/aaer-data/UAA/xbrl/CIK0001336917.json` and `~/aaer-data/UAA/edgar/` submissions JSONs
(manifest-pinned). At accession level:

- **Receivables vs revenue**: AccountsReceivableNetCurrent 433,638,000 (2015-12-31) and
  NetIncomeLoss 232,573,000 (FY2015) — XBRL facts of accn 0001336917-16-000064 (10-K FY2015,
  filed 2016-02-22).
- **Income-cash divergence and inventory build**: NetCashProvidedByUsedInOperatingActivities
  14,541,000 (FY2015) and InventoryNet 1,158,548,000 (2017-12-31) — XBRL facts of accn
  0001336917-18-000009 (10-K FY2017, filed 2018-02-28).
- **Amendment chronology** (`~/aaer-data/UAA/edgar/` submissions JSONs): 10-K/A 2013-02-26
  (accn 0001336917-13-000013, one day after the 10-K); 8-K/A 2015-05-01 (accn
  0001336917-15-000018), 2015-12-23 (accn 0001336917-15-000056), 2017-02-16 (accn
  0001336917-17-000010), 2017-10-31 (accn 0001336917-17-000047) — all pre-cutoff, matching
  the frozen output's CL7 claims.

Not visible in this sealed §3 set: earnings-release/earnings-call text, analyst consensus
estimates, MD&A narrative, order-book or requested-ship-date data — the axes on which the
order's findings actually run (¶15, ¶19, ¶28, ¶37); per-quarter pull-forward dollar amounts
(¶14-¶38) are not derivable from the sealed XBRL levels — insufficient sealed evidence to
treat them as part of the pre-cutoff information set. This section describes the information
set — it does not re-score the case.

## 4. WHAT THE LLM CAUGHT

Frozen output `runs/wave2/scores/case_66.json`: `misstatement_probability`: 55 (legacy v1 key
— an uncalibrated ordinal score; see specs/RISK_SCORE_SEMANTICS.md) = score 55, risk_tier
"elevated" — above the flag threshold of 50, hence TP. CL1/CL3/CL4 flagged "high", CL7
flagged "low"; CL2/CL5 no_flag; CL6 insufficient_data; CL8 sufficient.

| model claim (verbatim) | enforcement/restatement reference | match quality |
|---|---|---|
| "Possible premature/aggressive revenue recognition or 'sell-in' shipment to distributors/off-price channel ahead of end-customer demand … which would inflate current-period revenue/receivables at the expense of future periods." (hypothesis 1, top-ranked, "overstated") | ¶2 (lines 65-70): "accelerate, or 'pull forward,' existing orders that customers had requested be shipped in future quarters"; ¶39 (lines 336-338): Under Armour "could record the sale as occurring in the earlier quarter but, all things being equal, would lose that particular sale in the later quarter" — the shift-forward-at-expense-of-future-quarters core matches; but fn.2 (lines 90-91) makes no GAAP findings on the sales, and the order's charged conduct is the disclosure omission, which no hypothesis covers | exact mechanism |
| "earnings not converting to cash … a classic marker of low earnings quality potentially tied to extended payment terms or sell-in recognition to move product" (hypothesis 2 / top_signals, FY2015 NI $232.6M vs OCF $14.5M) | ¶10 (lines 131-133): "periodic use of sales incentives, such as extended payment terms and discounts, to convince customers to agree to take Under Armour product the quarter before the customer had requested shipment"; ¶26 (lines 248-249): "a 25% price discount and an extra 30 days to pay to secure an additional $6.7 million of pull forwards" — incentive terms confirmed, but the order does not allege earnings overstatement | right direction only |
| "Accounts receivable growing 40-55% YoY versus 20-32% revenue growth in FY2015 and FY2016, indicating potential channel stuffing or extension of credit terms to accelerate sales recognition" (top_signals) | ¶26 (lines 241-243): "increasing reliance on pull forwards often resulted in it making multiple requests each quarter to its largest wholesale customers, and periodically offering sales incentives such as price discounts and extended payment terms" — acceleration-of-sales pressure on customers confirmed; the order quantifies pull-forward dollars, not receivables impact | right direction only |
| "Insufficient inventory obsolescence/lower-of-cost-or-market write-downs during the 2016-2017 inventory build" (hypothesis 3, "understated" COGS) | No counterpart — the order contains no inventory, obsolescence, or COGS finding | unrelated |

Grade notes (`scoring/grades_wave2/case_66.json`, dim2=2): the top-ranked hypothesis
"substantially matches the key's pull-forward of existing customer orders (correct account +
direction + acceleration-of-sales treatment type), but names no case-specific pinpointed fact
from the key … so not 3. Coverage: the disclosure_only/omission component of the multi-part
truth is uncovered by any hypothesis."

## 5. WHAT THE LLM MISSED

The quantitative axes the sealed §3 set offered — receivables, inventory, income-cash
divergence, amendment chronology — were all surfaced (§4). Residual gaps:

- **The disclosure-omission limb** (the only conduct actually charged): no hypothesis frames
  the risk as an MD&A/known-trends omission (grade note, §4). But the deck contained no MD&A
  or earnings-release text and no analyst-estimate data (§3) — insufficient sealed evidence
  that this limb was detectable from the provided information set.
- **Timing concentration**: the order's signature is per-quarter acceleration ($45M → $99M →
  $17.5M → $10M → $65M → ~$172M; ¶14-¶35) ending in the January 31, 2017 miss with a ~23%
  stock drop (¶36, lines 315-319). The frozen output works at annual-level ratios and does
  not surface the 2016→2017 quarterly break as an event; whether payload quarterly revenue
  made the streak-break independently visible is not verifiable from the sealed deck entry
  (metadata only) — insufficient sealed evidence.

## 6. ERROR TAXONOMY

Per `scoring/error_taxonomy.md` (R1→R2→R3), atlas vocabulary. The case is a TP; the
taxonomy applies to the dimension losses (dim2=2 not 3; dim3=1):

- **dim2 shortfall — data-limit, not model error**: the pinpointed key facts anchor 3
  requires (~$408M, six named quarters, analyst-estimate motive, MD&A non-disclosure) were
  absent from the provided data (XBRL + chronology, no narrative text) as a fact of the
  deck's design, not a build defect (R1); anchor unambiguous (R2) — an information-set
  ceiling, not an error bucket.
- **dim3 loss — interpretation (MODEL), with a data-limit nuance**: mapped_genre "active" vs
  the key's mixed active + disclosure_only → score 1 (one-sided-vs-mixed rule); the model
  chose an exclusively active-misstatement framing (R3); nuance — no narrative disclosure
  text existed in the deck to anchor an omission hypothesis.
- **Computation / retrieval**: none identified — dim4=3; grade rationale: evidence "cites
  specific provided data points that genuinely support claims." Spot re-verification here:
  433,638,000 / 14,541,000 / 232,573,000 / 1,158,548,000 all present in sealed
  `~/aaer-data/UAA/xbrl/CIK0001336917.json`; CL7 amendment chronology matches the sealed
  submissions JSONs (§3). Hygiene nuance: one CL7 evidence row carries source_accession_no
  "n/a".
- **Label-noise**: none — AAER-confirmed tier (settled Commission order). Definitional
  nuance: fn.2 disclaims GAAP findings on the sales, so this case's "misstatement" label
  rests on materially misleading disclosure (§17(a)(2)-(3), Item 303), not a restated figure.
- **Suspected-memorization**: recognition probe (single stored draw,
  `scoring/probe_results_wave2/recognition/case_66.json`): company_guess "Under Armour,
  Inc.", confidence "medium" — correct identification. Verbatim probe (single stored draw,
  `scoring/probe_results_wave2/verbatim/case_66.json`): known: true; recalled revenue
  5,193,185,000 equals the FY2018 figure the frozen output cites, while recalled net_income
  46,258,000 does not match the output's NetIncomeLoss -46,302,000. Grade
  memorization_suspect_condition2: false — reasoning "points at concrete provided data
  content (specific XBRL values tied to accessions) … and mentions no post-cutoff facts."

## 7. CPA JUDGMENT — human_finalized: false

Draft, unaudited work product until owner sign-off (PROJECT.md §7).

- The TP is substantively earned: the top-ranked hypothesis names the pull-forward core —
  acceleration of sales into the current quarter at the expense of future quarters (¶2, ¶39)
  — down to the extended-payment-terms detail (¶10/¶26). But the model frames it as a
  possible GAAP violation, which the Commission expressly did not find (fn.2). Whether
  "exact mechanism, wrong legal theory" counts as a full catch of a disclosure_only scheme
  is the core owner call. **[OWNER REVIEW]**
- Score 55 sits one band above threshold (dim1=1). A no-GAAP-violation disclosure case
  leaves a fainter quantitative footprint than a booked misstatement, so a mid-band score
  arguably reflects calibration rather than a weak catch. **[OWNER REVIEW]**
- The FY2015 income-cash divergence flag (NI $232.6M vs OCF $14.5M) overlaps the Relevant
  Period, and extended payment terms (¶10) would plausibly slow collections — a coherent
  chain, but the order never quantifies any receivables or cash-flow effect; the linkage is
  hypothesis, not enforcement fact. **[OWNER REVIEW]**
- Hypothesis 3 (understated inventory write-downs, FY2016-17 build) has no counterpart in
  the order, yet its timing coincides with the demand hole the order describes — sales "no
  longer available in the future quarter" (¶4, line 94), the "double impact on the growth
  rate" (¶40, lines 347-348); a benign-adjacent explanation fits the same data. **[OWNER REVIEW]**

## 8. AUDIT TRANSLATION

Procedures the flag would motivate — procedures, not conclusions:

- Revenue cutoff testing concentrated on quarter-end: compare actual ship dates to
  customer-requested delivery dates; investigate shipments moved earlier than requested (the
  order's mechanism, ¶2, ¶9).
- Examine quarter-end sales incentives — price discounts, extended payment terms — granted
  to large wholesale customers, and their approval trail (¶10, ¶26); confirm terms and side
  agreements, including requests to accept early shipment (¶26 records customer pushback in
  writing).
- DSO and receivables-aging analytics by quarter against revenue growth; correlate spikes
  with quarter-end shipment concentration (§3 receivables series).
- MD&A review under Reg S-K Item 303: compare internal forecasts and known demand trends
  (e.g., the $120 million wholesale-apparel projection decline, ¶8) with disclosed
  known-trends language and earnings-release growth attributions (¶15, ¶19, ¶28, ¶37);
  inquire of FP&A about forecast-vs-consensus gap tracking (¶9-¶10).

## 9. FINANCIAL STATEMENT IMPACT

Determinable from the sealed order text (`~/aaer-data/UAA/33-10940.pdf.txt`): the order
imposes no restatement and identifies no restated line items — consistent with fn.2 (lines
90-91). The impact the order does state is compositional and prospective, not a correction
of reported figures:

- Pull-forward revenue within reported totals: ~$45M Q3 2015 ("nearly 4% of its total
  revenue," ¶16), ~$99M Q4 2015 ("nearly 8.5%" of revenue, "approximately 35%" of growth,
  ¶20), $17.5M Q1 2016 (¶22), $10M Q2 2016 (¶24), ~$65M Q3 2016 ("nearly 4.5%" of revenue,
  "approximately 25%" of growth, ¶29), ~$172M Q4 2016 ("approximately 13% of its quarterly
  revenue," ¶35); ~$408M total (¶3).
- Reported results "did not reflect its natural revenue and revenue growth, and were not
  indicative of its future financial results" (¶41, lines 356-357).
- Restated line items and directions: **not determinable** — none exist in the sealed order;
  the sanction is a cease-and-desist and a $9,000,000.00 civil penalty (Section IV.A-B).

---
*Entry status: drafted (sections 7–9 pending owner finalization).*
*채점: Claude 보조 + 인간 최종 확정. 교육·정보 목적, 투자 자문 아님.*
