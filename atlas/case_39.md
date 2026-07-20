# atlas/case_39.md — Osiris Therapeutics, Inc. (OSIR) — wave-2 treatment T19

Authored by Claude Code, pending human audit (D15). Analytical document under D106 ② — not a scored output. 본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).

## 1. CASE HEADER

| field | value |
|---|---|
| Case ID (anonymized frame) | case_39 (scoring ID T19) |
| Cohort | wave-2 |
| Outcome class | TP (main frame, flag at score ≥50) |
| Ground-truth tier | AAER-confirmed (AAER-3905 / LR-23978) |
| Frozen score | score 58 (`runs/wave2/scores/case_39.json`, run `original-case_39-r1`) |
| Grade record | `scoring/grades_wave2/case_39.json` (human_finalized: true, finalized 2026-07-09 via RP-13 workbench) |

Company: Osiris Therapeutics, Inc., CIK 0001360886, cutoff 2015-11-05
(`data/candidates/candidates_wave2.json` T19; `data/evaluatee/cases_wave2.json` case_39).

## 2. ACTUAL EVENT

SEC v. Osiris Therapeutics, Inc., et al., Civil Action No. 17-cv-03230 (D. Maryland,
November 2, 2017); Litigation Release No. 23978 / AAER No. 3905 (November 3, 2017).
Sealed local text: `~/aaer-data/OSIR/lr-23978.html.txt` (manifest-pinned,
`data/manifests/aaer_data_manifest.json`).

Per the release body (¶2, line 1083), Osiris "routinely overstated company
performance and issued fraudulent financial statements for a period of nearly two
years": it "improperly recognized revenue using artificially inflated prices,
backdated documents to recognize revenue in earlier periods, and prematurely
recognized revenue upon delivery of products to be held on consignment," and
executives "used pricing data that they knew was false and attempted to book revenue
on a fictitious transaction, among other accounting improprieties." The conduct ran
"during the alleged period of accounting fraud from 2014 to 2015" (¶3, line 1085);
the company "agreed to settle the charges without admitting or denying the
allegations" and "must pay a $1.5 million penalty" (¶4, line 1087).

Registered summary (`data/candidates/candidates_wave2.json`, T19 `scheme_summary`):
revenue inflated via inflated prices, backdated documents, premature consignment
recognition, false pricing data, fictitious transaction. `scheme_type`:
revenue_recognition + document_forgery; manipulation period 2014-01 to 2015-09.

GAAP topics: revenue recognition for 2014-2015 fiscal periods — pre-ASC-606 (ASC 605 /
SAB 104 era). The described mechanisms (revenue before a completed sale on consignment
deliveries; backdated documents shifting revenue into earlier periods; prices known to
be false) implicate ASC 605/SAB Topic 13 recognition criteria and period-end cutoff.
The release cites no ASC sections; no further topic attribution from sealed evidence.

## 3. SIGNALS AVAILABLE PRE-CUTOFF

Cutoff 2015-11-05 (`data/evaluatee/cases_wave2.json`, case_39). The deck's sealed data
basis is `~/aaer-data/OSIR/edgar/CIK0001360886.json` (filing chronology) and
`~/aaer-data/OSIR/xbrl/CIK0001360886.json` (XBRL company facts). Pre-cutoff, at
accession level:

- **Receivables outrunning revenue**: AccountsReceivableNetCurrent $21,446K at
  2014-09-30 (accn 0001104659-14-078750) → $32,022K at 2015-03-31 (accn
  0001104659-15-036502) → $38,598K at 2015-06-30 (accn 0001104659-15-057928), against
  quarterly SalesRevenueGoodsNet of $21,003K (Q1-2015) and $23,688K (Q2-2015, same accns).
- **Allowance decline as receivables grew**: AllowanceForDoubtfulAccountsReceivableCurrent
  $1,300K at 2015-03-31 (accn 0001104659-15-036502) → $261K at 2015-06-30 (accn
  0001104659-15-057928).
- **Inventory build**: InventoryNet $1,929K at 2013-12-31 (accn 0001047469-14-003199)
  → $10,924K at 2014-12-31 (accn 0001047469-15-002532) → $13,348K at 2015-06-30 (accn
  0001104659-15-057928), versus SalesRevenueGoodsNet $24,308K (FY2013) → $59,867K
  (FY2014, accn 0001047469-15-002532).
- **Net income vs operating cash flow divergence**: FY2013 net income to common
  $41,638K vs operating cash flow -$13,269K, with a $49,806K Q4-2013 net income figure
  against FY2013 OperatingIncomeLoss of -$2,833K (all accn 0001047469-14-003199);
  FY2011 $14,892K vs -$20,436K (accn 0001047469-12-002580).
- **Filing-chronology friction**: NT 10-K filed 2014-03-17 (accn 0001104659-14-020263)
  and 2015-03-17 (accn 0001104659-15-020443); 8-K/A filed 2014-03-11 (accn
  0001104659-14-018183) (`~/aaer-data/OSIR/edgar/CIK0001360886.json`, filings.recent).

This section describes the information set — it does not re-score the case.

## 4. WHAT THE LLM CAUGHT

Frozen output `runs/wave2/scores/case_39.json`: `misstatement_probability`: 58 (legacy
v1 key — an uncalibrated ordinal score; see specs/RISK_SCORE_SEMANTICS.md) = score 58,
risk_tier "elevated"; CL1 (AR vs revenue), CL3 (NI vs OCF), CL4 (inventory vs revenue),
CL6 (allowance decline), CL7 (NT 10-K chronology) flagged. All checklist evidence values
re-verified against the sealed XBRL facts file at value+date+accession level; no
fabricated data point found.

| model claim (verbatim) | enforcement/restatement reference | match quality |
|---|---|---|
| "Potential premature or aggressive revenue recognition (e.g., extended payment terms, bill-and-hold, or channel stuffing to distributors) causing receivables to grow far faster than sales" (hypothesis 1, direction "overstated") | lr-23978.html.txt ¶2 (line 1083): "prematurely recognized revenue upon delivery of products to be held on consignment"; "improperly recognized revenue using artificially inflated prices" | exact mechanism |
| "understating the allowance for doubtful accounts relative to a rapidly growing and increasingly aged receivables base, thereby overstating net receivables and net income" (hypothesis 1) | lr-23978.html.txt ¶2: no allowance/estimate allegation; overstatement of performance is alleged ("routinely overstated company performance") | right account wrong mechanism |
| "capitalization of costs that should be expensed, failure to write down slow-moving/obsolete tissue-graft inventory, or overproduction potentially tied to the same channel-stuffing dynamic" (hypothesis 2, InventoryNet "overstated") | No inventory mechanism in lr-23978.html.txt; restatement 10-K/A (accn 0001104659-17-019408) reports FY2014 InventoryNet $9,824K vs $10,924K as originally reported (accn 0001047469-15-002532) | right direction only |
| "Large non-operating/non-cash gains (likely fair-value remeasurement of warrant or derivative liabilities...) drove reported net income sharply positive" (hypothesis 3, "timing_shift") | No counterpart in lr-23978.html.txt or T19 scheme_summary | unrelated |

Notes: row 1 matches the mechanism family (premature revenue recognition, revenue/AR/NI
overstated) but names bill-and-hold/channel-stuffing rather than consignment, and no
hypothesis names backdating, false pricing data, or the fictitious transaction —
consistent with grade DIM2=2, not 3 (`scoring/grades_wave2/case_39.json`).

## 5. WHAT THE LLM MISSED

From the sealed §3 information set: none identified — the frozen checklist surfaced the
receivables, allowance, inventory, NI/OCF, and NT-10-K signals the sealed deck supports.
The document_forgery leg of the ground truth (backdating, false pricing data, fictitious
transaction; `candidates_wave2.json` T19) has no distinct pre-cutoff footprint in the
sealed XBRL/chronology data — insufficient sealed evidence to name a missed signal for
that leg.

## 6. ERROR TAXONOMY

Outcome is TP; taxonomy applies to residual grading gaps (`scoring/error_taxonomy.md`
buckets, atlas vocabulary):

- **Computation / Retrieval**: none found — every cited value and accession
  attribution re-verified against `~/aaer-data/OSIR/xbrl/CIK0001360886.json` (§4).
- **Interpretation**: two gaps. (a) DIM3=1: the top hypothesis blends active
  manipulation with an estimate-omission element (allowance understatement), mapping
  to "mixed" against an active answer-key scheme (`scoring/grades_wave2/case_39.json`
  rationale). (b) Score 58 sits in the lowest flagged band (DIM1=1) despite evidence
  graded DIM4=3. Both are MODEL-bucket under the R1→R2→R3 rules (signals present in
  the provided data; anchors forced a unique grade).
- **Label-noise**: none — AAER-confirmed tier, settled action with civil penalty (§2).
- **Suspected-memorization**: no. Recognition probe — the single stored draw
  `scoring/probe_results_wave2/recognition/case_39.json` — guessed "PhotoMedex, Inc."
  with confidence "low" (wrong company); verbatim probe
  `scoring/probe_results_wave2/verbatim/case_39.json` returned known: false; grade
  record memorization_suspect_condition2: false.

`analysis/error_analysis_wave2_holdout.md` does not mention this case — no FP/FN
context to import.

## 7. CPA JUDGMENT — human_finalized: false

Draft, unaudited work product until owner sign-off (PROJECT.md §7).

- The model reached the right flag for substantially the right accounting reason: the
  receivables/revenue divergence and allowance release it quoted are the classic
  balance-sheet residue of premature, price-inflated revenue recognition, and the
  10-K/A later restated FY2014 revenue and receivables downward (§9). **[OWNER REVIEW]**
- Consignment was not named, but consignment, bill-and-hold, and channel stuffing
  share the same footprint (goods shipped without a completed sale → AR and revenue
  inflate ahead of cash). Grading §4 row 1 "exact mechanism" at family level while
  DIM2=2 (not pinpointed) is a judgment call. **[OWNER REVIEW]**
- The allowance-understatement clause reads as over-reach: the enforcement text
  alleges active revenue-side manipulation, not reserve manipulation; the allowance
  drop is more plausibly a symptom than a scheme leg, and it dragged the genre
  mapping to "mixed" (DIM3=1). **[OWNER REVIEW]**
- Score 58 against DIM4=3 evidence looks conservative; document-forgery schemes are
  quantitatively quiet, so hesitance to score higher on XBRL-only data is defensible.
  Under-confidence vs appropriate calibration is an owner call. **[OWNER REVIEW]**

## 8. AUDIT TRANSLATION

Procedures the flag would motivate (framed as procedures, not conclusions):

- AR confirmations with distributors, including terms (right of return,
  consignment/hold arrangements, extended payment terms).
- Revenue cutoff testing at quarter-ends: agree recognition dates to shipping
  documents and contract execution dates; document date-integrity checks.
- Price testing: agree invoiced prices to signed distributor agreements and price
  lists; investigate price changes near period-end.
- Recompute the allowance for doubtful accounts against an AR aging; corroborate the
  Q2-2015 allowance reduction with cash-collection evidence.
- Inventory existence and NRV/obsolescence testing on the FY2014 build; reconcile
  units shipped vs units sold-through.
- Review NT 10-K/NT 10-Q filings, the 8-K/A, and auditor communications for
  close-process issues.

## 9. FINANCIAL STATEMENT IMPACT

Determinable from sealed restatement data — the FY2014 10-K/A (accn
0001104659-17-019408, filed 2017-03-27, post-cutoff; XBRL values in
`~/aaer-data/OSIR/xbrl/CIK0001360886.json`) versus the original FY2014 10-K (accn
0001047469-15-002532), FY2014 (period ended 2014-12-31): **[OWNER REVIEW — figures are
XBRL-tag comparisons from the sealed facts file, not narrative restatement text]**

| line item | as originally reported | as restated (10-K/A) | direction |
|---|---|---|---|
| SalesRevenueGoodsNet (FY2014) | $59,867K | $50,835K | revenue overstated |
| AccountsReceivableNetCurrent (2014-12-31) | $24,307K | $13,373K | receivables overstated |
| InventoryNet (2014-12-31) | $10,924K | $9,824K | inventory overstated |
| NetIncomeLossAvailableToCommonStockholdersBasic (FY2014) | -$1,789K | -$9,970K | loss understated |

FY2015 and interim restated amounts: not determinable from the sealed sources read.
The enforcement release quantifies no line items beyond the $1.5 million penalty.

---
*Entry status: drafted (sections 7–9 pending owner finalization).*
*채점: Claude 보조 + 인간 최종 확정. 교육·정보 목적, 투자 자문 아님.*
