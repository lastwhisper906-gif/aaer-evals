# atlas/case_61.md — Celadon Group, Inc. (CGI) — wave-2 treatment T24

Authored by Claude Code, pending human audit (D15). Analytical document under D106 ② — not a scored output. 본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).

## 1. CASE HEADER

| field | value |
|---|---|
| Case ID (anonymized frame) | case_61 (scoring ID T24) |
| Cohort | wave-2 |
| Outcome class | TP (main frame, flag at score ≥50) |
| Ground-truth tier | AAER-confirmed (wave-2 treatment cohort; sealed enforcement basis LR-24459, SEC v. Celadon Group, Inc., No. 1:19-cv-1659 (S.D. Ind., filed April 25, 2019)) |
| Frozen score | score 72 (`runs/wave2/scores/case_61.json`, run `original-case_61-r1`, risk_tier "elevated") |
| Grade record | `scoring/grades_wave2/case_61.json` (human_finalized: true, finalized 2026-07-09 via RP-13 workbench; dim1=2, dim2=2, dim3 mapped "mixed"/score null, dim4=3) |

Company: Celadon Group, Inc., CIK 0000865941, cutoff 2017-04-04
(`data/candidates/candidates_wave2.json` T24; `data/evaluatee/cases_wave2.json` case_61).
`analysis/error_analysis_wave2_holdout.md` does not discuss this case individually.

## 2. ACTUAL EVENT

SEC v. Celadon Group, Inc., No. 1:19-cv-1659 (S.D. Ind.); Litigation Release No. 24459 (April
25, 2019), "SEC Charges Truckload Freight Company with Accounting Fraud". Sealed local text:
`~/aaer-data/CGI/comp24459.pdf.txt` (complaint) and `~/aaer-data/CGI/lr-24459.html.txt`
(manifest-pinned, `data/manifests/aaer_data_manifest.json`).

Per the complaint, between June 2016 and April 2017 Celadon "orchestrated a fraudulent scheme
designed to avoid disclosing substantial losses" (¶1, lines 31-32). "The assets in question were
more than a thousand trucks." (¶2, line 35) held above market; to avoid impairment, Celadon
"sold trucks at significantly inflated prices, and in exchange bought trucks from the same party
at similarly inflated prices" (¶3, lines 44-46). June-October 2016: "Quality sold more than 900
trucks to Party A and purchased more than 600 trucks from Party A. The prices in these
transactions were at least $20 million more than the trucks were worth." (¶24, lines 152-154),
fabricating "a tidy $1 million gain" (¶24, line 156) — "almost two-thirds of its 2016 pre-tax
income" per LR-24459 (line 1087). The overpriced trucks went to 19th Capital, an "'off-balance
sheet' entity" (¶33, line 211), "valued ... at or above the inflated prices Celadon had paid"
(¶30, line 201); straddled invoices left the Nov 9, 2016 10-Q "underreporting its outstanding
contractual obligations" (¶28, lines 185-186). Charges: Exchange Act §10(b)/Rule 10b-5, §13(a),
§13(b)(2)(A)-(B) and related rules; "Celadon admitted to those violations" (LR-24459, line 1089).

Registered summary (`data/candidates/candidates_wave2.json`, T24 `scheme_summary`): avoided ~$20M
of used-truck impairment charges via inflated-price truck purchases/sales with a third-party
dealer, overstating asset values, pre-tax income, net income and EPS in the FY2016 10-K and
subsequent filings. `scheme_type`: asset_overstatement; manipulation period 2016-06 to 2017-04.

GAAP topics: no ASC topic is named in the sealed enforcement text. In the complaint's own terms:
avoided "impairment charges" / failure "to mark down the trucks to their fair values" (¶18 line
122, ¶51 lines 327-328); lease-portfolio transfers that should have been recorded "as borrowings
rather than sales" (¶40, line 257); a joint venture "structured ... in order to avoid having to
consolidate" (¶33, lines 212-213); controls insufficient for statements "in accordance with
GAAP", "material weaknesses over the affected periods between 2014 and 2016" (¶52, lines 333,
335-336).

## 3. SIGNALS AVAILABLE PRE-CUTOFF

Cutoff 2017-04-04 — the tail of the alleged conduct window (June 2016-April 2017, ¶1); the
December 2016 auditor inquiries and "campaign of deception" (¶36, lines 227-229) were not
public. Sealed data basis: `~/aaer-data/CGI/xbrl/CIK0000865941.json` (XBRL companyfacts) +
`~/aaer-data/CGI/edgar/CIK0000865941.json` (chronology). Pre-cutoff, at accession level:

- **Soft-asset balloon then single-quarter collapse**: OtherAssetsNoncurrent $1.531M (2012-06-30,
  accn 0001008886-13-000085) → $43.342M (2016-06-30, accn 0001008886-16-000363) → $46.607M
  (2016-09-30, accn 0001008886-16-000393) → $9.698M (2016-12-31, accn 0001008886-17-000026); the
  collapse quarter coincides with the trucks' transfer to 19th Capital (¶30-¶35; JV announced by
  8-K 2017-01-06, accn 0001008886-17-000002, sealed EDGAR chronology).
- **Income–cash divergence in the misstated periods**: NetIncomeLoss $24.844M vs
  NetCashProvidedByUsedInOperatingActivitiesContinuingOperations −$5.211M (FY2016, both accn
  0001008886-16-000363 — the September 13, 2016 10-K that ¶25(b) names as misstated);
  NetIncomeLoss $11.367M vs operating cash flow −$22.807M (Q1 FY2016, accn 0001008886-15-000248).
- **Receivables outran revenue FY2013-FY2015**: AccountsReceivableNetCurrent $77.623M
  (2013-06-30, accn 0001008886-13-000085) → $105.968M (2014-06-30, accn 0001008886-14-000114) →
  $130.892M (2015-06-30, accn 0001008886-15-000210), vs Revenues $613.648M → $759.311M →
  $900.756M (same accns); AllowanceForDoubtfulAccountsReceivableCurrent $1.045M (2011-06-30,
  accn 0001008886-12-000071) vs $1.002M (2015-06-30, accn 0001008886-15-000210) against AR of
  $64.723M and $130.892M respectively.
- **Chronology friction**: 10-K/A 2012-05-18 (accn 0001008886-12-000079) plus two 10-Q/A
  2012-05-25 (accns 0001008886-12-000085/-000086); 10-K/A 2015-03-30 (accn 0001008886-15-000055);
  NT 10-Q 2017-02-09 (accn 0001140361-17-005460) followed one day later by the 10-Q 2017-02-10
  (accn 0001008886-17-000026) — the Q2 FY2017 10-Q that ¶25(e) (lines 168-169) names as misstated.

Not visible in this sealed set: the round-trip counterparty ("Party A"), truck-level pricing vs
fair value, the deleted "subject to and dependent upon one another" contract language (¶20, lines
133-134), and the straddled-invoice terms. This section describes the information set — it does
not re-score the case.

## 4. WHAT THE LLM CAUGHT

Frozen output `runs/wave2/scores/case_61.json`: `misstatement_probability`: 72 (legacy v1 key —
an uncalibrated ordinal score; see specs/RISK_SCORE_SEMANTICS.md) = score 72, risk_tier
"elevated" — at/above the flag threshold of 50, hence TP. CL1-CL3/CL5-CL7 flagged; CL4
insufficient_data; CL8 no_flag. All cited evidence values re-verified against the sealed XBRL
facts file at value+accession level; none fabricated (dim4=3).

| model claim (verbatim) | enforcement/restatement reference | match quality |
|---|---|---|
| "Capitalization of costs or gains associated with revenue-equipment transactions and acquisitions into non-current 'other assets'/goodwill rather than expensing ... consistent with deferred recognition of losses or overstated asset values later reversed" (hypothesis 1, top-ranked, "overstated") | ¶18 (lines 122-123): "To avoid having to recognize such charges, Celadon orchestrated a fraudulent scheme."; ¶25 (lines 158-160): "materially overstated the value of its assets and, by extension, materially overstated its income before income taxes, net income and earnings per share"; scheme_summary avoided-impairment / asset_overstatement | right account wrong mechanism |
| "OtherAssetsNoncurrent ballooned from ~1.5M (2012) to ~43-47M (mid-to-late 2016) then collapsed to ~9.7M within a single quarter (Dec 2016), a pattern disproportionate to revenue growth and suggestive of asset/gain manipulation tied to equipment or acquisition-related transactions" (top_signals) | ¶24 (line 156): fabricated "$1 million gain on the transactions with Party A"; ¶30-¶35: trucks contributed to 19th Capital at inflated values, then written down off Celadon's books — the complaint ties none of this to the OtherAssetsNoncurrent caption | right direction only |
| "revenue/receivables were recognized ahead of collectability" (hypothesis 2, AR/Revenues/allowance "overstated") | No receivables or revenue-recognition allegation in the complaint (the ¶39-¶40 lease-portfolio issue is sale-vs-borrowing, not receivables) | unrelated |
| "earnings were increasingly driven by non-cash items (e.g., gains on equipment dispositions, depreciation timing, or other accruals) rather than cash-generating operations" (hypothesis 3, NetIncomeLoss "overstated") | ¶25 (lines 158-160): income overstated — but via unrecognized impairment charges and a fabricated gain (¶24), not a generic accrual divergence; grade: "hypotheses 2 ... and 3 ... do not match the truth mechanism; only H1 does" | right direction only |
| "Filing irregularities near the cutoff date, including an NT 10-Q filed one day before the corresponding 10-Q, plus a history of multiple 10-K/A and 10-Q/A amendments" (top_signals) | The 10-Q filed February 10, 2017 is among the misstated filings ¶25(e) (lines 168-169) lists; the complaint alleges nothing about the NT form or the 2012/2015 amendments | right direction only |

Notes: grade dim2=2 — "account area overlaps ..., direction matches (assets and income
overstated), and treatment type substantially matches (deferred recognition of losses /
overstated asset values ≈ avoided impairment charges)"; "It does NOT reach 3: no case-specific
facts from the key (third-party dealer, >1,000 trucks, 2-3x fair value pricing, ~$20M /
two-thirds of pre-tax income, FY2016 10-K specificity) are named"
(`scoring/grades_wave2/case_61.json`). dim3: mapped "mixed", score null — the answer key's
genre_tag_row is null, flagged for the human auditor in the grade record.

## 5. WHAT THE LLM MISSED

From the sealed §3 information set: the soft-asset balloon/collapse, income-vs-cash, receivables,
and chronology axes were all surfaced (§4). One candidate gap, stated with its limit: the frozen
output does not mention the 8-K of 2017-01-06 announcing the joint venture — ¶31 (lines 202-204)
alleges the JV investment was materially misstated in that very 8-K — but whether it was in the
deck's "Filing chronology list" cannot be established from sealed evidence. The scheme's direct
footprints (Party A round-trip pricing, straddled invoices, contributed-truck valuations) are
absent from the sealed XBRL aggregates; beyond these, none identified from sealed evidence.

## 6. ERROR TAXONOMY

Per `scoring/error_taxonomy.md` (R1→R2→R3), atlas vocabulary. The case is a TP; the taxonomy
applies to the residual dimension gaps:

- **Primary — no MODEL error identified**: the dim2 2-vs-3 gap turns on case-specific facts
  (third-party dealer, >1,000 trucks, 2-3x fair-value pricing, ~$20M magnitude) concealed by
  design (¶20 deleted contract language; ¶36 deception of the auditor) and absent from the deck
  — a world-fact absence, not a collection/extraction defect, so the R1 DATA branch does not
  apply and no reasoning failure is chargeable under R3. An information-ceiling on the grade,
  not a bucketed error.
- **Criteria-adjacent note (dim3)**: score null because "The answer key's genre_tag_row is null,
  so no key genre exists to score against" (grade rationale) — an answer-key coverage gap
  flagged for the human auditor, not a model error.
- **Computation**: the H1 narrative's "43x growth from 2012 to mid-2016" does not reproduce from
  the cited endpoints ($1.531M → $43.342M ≈ 28x; → $46.607M ≈ 30x); the "~80% single-quarter
  collapse" reproduces ($46.607M → $9.698M = −79.2%), as do the allowance-ratio claims (~1.6% →
  ~0.77%). All value+accession pairs cited in the checklist re-verified against the sealed XBRL
  file, including the CL5 tag variant (NetCashProvidedByUsedInOperatingActivities −22,807,000,
  accn 0001008886-15-000248).
- **Label-noise**: none — "Celadon admitted to those violations" (LR-24459, line 1089).
- **Suspected-memorization**: recognition probe — the single stored draw
  `scoring/probe_results_wave2/recognition/case_61.json` — company_guess "unknown", confidence
  "low"; verbatim probe `scoring/probe_results_wave2/verbatim/case_61.json`: known: false,
  recall fields null. Grade memorization_suspect_condition2: false — "the reasoning points
  extensively at concrete provided data content (specific XBRL values with periods and
  accessions), not bare document lists" and "no mention of post-cutoff facts".

## 7. CPA JUDGMENT — human_finalized: false

Draft, unaudited work product until owner sign-off (PROJECT.md §7).

- The model's strongest observable — OtherAssetsNoncurrent $1.5M → $46.6M → $9.7M, collapsing
  in the December 2016 quarter — aligns temporally with the ¶24 trade window and the ¶30-¶35
  transfer to 19th Capital, but mapping that XBRL caption to the trucks/JV investment is
  inference; the complaint never names the caption. **[OWNER REVIEW]**
- H1's capitalization framing is the wrong mechanism (actual: round-trip trades at inflated
  prices to avoid impairment, ¶3/¶18), yet its effect clause — "deferred recognition of losses
  or overstated asset values later reversed" — describes the outcome ¶25 alleges and the
  reversal ¶35 records at 19th Capital; whether that deserves more than dim2=2 under the
  pre-fixed anchors is an owner call. **[OWNER REVIEW]**
- The FY2016 income-vs-cash divergence comes from the very 10-K ¶25(b) names as misstated;
  unrecognized impairments are a non-cash income overstatement, so the divergence is mechanically
  connected even though the model's framing was generic. **[OWNER REVIEW]**
- Hypothesis 2 (receivables/collectability) has no enforcement counterpart and rests on a
  FY2013-FY2015 trend predating the 2016-06 manipulation start; treating it as support for the
  score-72 flag would over-credit the flag. **[OWNER REVIEW]**
- Cutoff 2017-04-04 sits at the end of the alleged conduct window; the auditor's December 2016
  inquiries and report withdrawal (¶36-¶38) were not in the sealed pre-cutoff set, so the model
  flagged on statement-level footprints alone. **[OWNER REVIEW]**

## 8. AUDIT TRANSLATION

Procedures the flag would motivate — procedures, not conclusions:

- Used-equipment valuation testing: net book values of revenue equipment vs open-market/
  wholesale used-truck pricing; impairment triggering-event assessment (¶17-¶18, ¶21, ¶51).
- Round-trip counterparty analytics: match equipment sales to and purchases from the same
  counterparty within a window; examine contract terms for linkage (the deleted "subject to and
  dependent upon one another" language, ¶20) and gain recognition on such trades (¶24).
- Quarter-end cutoff/settlement testing of receivables and payables with equipment
  counterparties, targeting straddled invoices (¶26-¶28); completeness of disclosed obligations.
- Joint-venture formation audit: valuation support for contributed equipment, day-one JV
  investment carrying amount vs the venture's own markdown of the same assets (¶30-¶35), and
  consolidation/off-balance-sheet structure analysis (¶33).
- Risk-of-ownership analysis on lease-portfolio transfers — sale vs secured borrowing (¶39-¶40);
  corroboration of management representations against signed counterparty documentation (¶36).

## 9. FINANCIAL STATEMENT IMPACT

From the sealed complaint text: the auditor "withdrew its previously issued reports on Celadon's
financial statements for the fiscal year ending June 30, 2016, and for the first two fiscal
quarters of 2017" and "Celadon subsequently announced its intention to restate those financial
statements.  To date, it has not done so." (¶38, lines 239-246) — restated line-item amounts are
therefore **not determinable** from the sealed sources read. Determinable direction and alleged
magnitudes: asset values, income before income taxes, net income and EPS materially overstated
(¶25, lines 158-160) in the FY2016 10-K, the 10-Qs of Nov 9, 2016 and Feb 10, 2017, and three
earnings 8-Ks (¶25(a)-(e), lines 161-169); avoided impairments/losses "at least $20 million ...
almost two-thirds of its 2016 pre-tax income" (LR-24459, line 1087); fabricated "$1 million
gain" (¶24, line 156); "purported $100 million investment in 19th Capital" materially misstated
(¶31, lines 202-203); ~$27.9M of deferred payment obligations underreported in the Nov 9, 2016
10-Q (¶26-¶28); separately, the ¶40 lease-portfolio sale-vs-borrowing error was expected (April
2, 2018 press release) to "reduce Celadon's net income before income taxes between $200-$250
million cumulatively over the three-year period ended June 30, 2016", with no restatement to the
complaint date (lines 257-262). Disgorgement: $7 million, deemed satisfied by DOJ restitution
(LR-24459, line 1089).

---
*Entry status: drafted (sections 7–9 pending owner finalization).*
*채점: Claude 보조 + 인간 최종 확정. 교육·정보 목적, 투자 자문 아님.*
