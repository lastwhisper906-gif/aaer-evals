# atlas/case_13.md — Marvell Technology Group, Ltd. (MRVL) — wave-1 treatment T17

Authored by Claude Code, pending human audit (D15). Analytical document under D106 ② — not a scored output. 본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).

## 1. CASE HEADER

| field | value |
|---|---|
| Case ID (anonymized frame) | case_13 (scoring ID T17) |
| Cohort | wave-1 |
| Outcome class | TP (main frame, flag at score ≥50) |
| Ground-truth tier | AAER-confirmed (AAER-4076 / Securities Act Rel. 33-10684 / Exchange Act Rel. 34-86971, File 3-19454) |
| Frozen score | score 55 (`runs/main/case_13.json`, run `original-case_13-r1`); perturbed frame score 42 (`runs/perturbed/case_13.json`, run `perturbed-case_13-r1`) |
| Grade record | `scoring/grades/main/case_13.json` and `scoring/grades/perturbed/case_13.json` (human_finalized: true, RP-09 Stage 0, commit 986a893, 2026-07-07; the perturbed record is covered by D21's "MRVL DATA(design) PROPOSAL" adoption, `scoring/decisions_log.md` D21) |

Company: Marvell Technology Group, Ltd., CIK 0001058057, cutoff 2015-09-10
(`data/candidates/candidates.json` T17; `data/evaluatee/cases.json` case_13).
Perturbation delta: score 55 → 42 (main − perturbed = +13). Per D8 the delta
measures memorization contribution — not a robustness pass/fail; here the
identity-masked frame fell below the threshold, so only the main frame is a
TP at 50. `review_packets/RP-06_hardening.md` records five perturbed-frame
draws 42/25/33/50/58 (mean 41.6, sd 11.7); Δ +13 classed within draw noise.

Governance note (manipulation window): D2 (`scoring/decisions_log.md`,
2026-07-06; owner reconfirmation, `scoring/overrides.md` "GA-001 부속") fixed
the manipulation window to the order's self-defined Relevant Period — "From
approximately January 2015 through July 2015" (33-10684.pdf.txt ¶2) — under
the signed GP-3 rule ("창 = 명령문 정의, 재량 0"). The registered
`candidates.json` fields (2014-11 ~ 2015-05, calendar span of the two charged
quarters) predate D2 and are annotated in the T17 `notes`.

## 2. ACTUAL EVENT

SEC Order Instituting Cease-and-Desist Proceedings, In the Matter of Marvell
Technology Group, Ltd., Securities Act Rel. 10684 / Exchange Act Rel. 86971 /
AAER-4076 (Sept. 16, 2019), settled. Sealed local text:
`~/aaer-data/MRVL/33-10684.pdf.txt` (manifest-pinned,
`data/manifests/aaer_data_manifest.json`).

Per ¶1: "an undisclosed revenue management scheme" — facing "a substantial
decline in customer demand", Marvell "orchestrated a plan to accelerate, or
pull-in, sales that had originally been scheduled for future quarters to the
current quarter in order to close the gap between actual and forecasted
revenue, meet publicly-issued guidance, and mask declining sales." An internal
policy (¶7 fn.2) defined a pull-in as "a transaction where Marvell initiates
and obtains agreement from customer to modify an existing sales order
scheduled shipment date from a subsequent quarter into the current quarter."
Pull-ins were used in three quarters (¶10): $24 million in Q4 FY2015 ended
2015-01-31 (¶12), $64 million in Q1 FY2016 ended 2015-05-02 (¶18), and "a
record amount of $77 million" in Q2 FY2016 ended 2015-08-01 (¶21). Customers
were incentivized with "price rebates, discounted prices, free products, and
extended payment terms" (¶9). Senior management "failed to inform the company’s Board of
Directors or its independent auditor of its pull-in scheme" (¶2; concealment
detail ¶37).
Violations charged (¶3, ¶40–41): Securities Act
Sections 17(a)(2)/(3) and Exchange Act Section 13(a) and Rules 13a-1, 13a-13,
12b-20 — misleading statements/omissions in the FY2015 Form 10-K and Q1
FY2016 Form 10-Q, including the Regulation S-K Item 303 MD&A trend omission.
Civil penalty $5,500,000 (§IV.B). A disclosure-side revenue-management case,
not a GAAP-restatement case (§9). Prior history recorded in the order itself
(¶4): a May 2008 SEC settlement for "improperly backdating stock options".

Registered summary (`data/candidates/candidates.json` T17 `scheme_summary`):
undisclosed "pull-in" revenue-management scheme accelerating future-quarter
sales into the current quarter to close the gap to guidance and mask
declining demand, concealed from board and auditor; `scheme_type`
revenue_recognition + disclosure_only; first revelation 2015-09-11
(8-K/press release: audit-committee investigation, Q2 FY2016 10-Q delay;
order ¶22), cutoff 2015-09-10.

## 3. SIGNALS AVAILABLE PRE-CUTOFF

Cutoff 2015-09-10. Sealed basis: `~/aaer-data/MRVL/xbrl/CIK0001058057.json`
and `~/aaer-data/MRVL/edgar/CIK0001058057-submissions-001.json`. Pre-cutoff,
as-reported, at accession level:

- **The two charged filings were in the information set**: FY2015 10-K accn
  0001193125-15-107187 (filed 2015-03-26) and Q1 FY2016 10-Q accn
  0001193125-15-213442 (filed 2015-06-04) — both in `documents_used` of both
  frozen runs.
- **Relevant-Period quarter numerics**: Revenues $857,452k for Q4 FY2015
  (2014-11-02→2015-01-31, accn 0001193125-15-107187) and $724,288k for Q1
  FY2016 (2015-02-01→2015-05-02, accn 0001193125-15-213442) — the $857M/$724M
  the order narrates (¶13, ¶19). NetIncomeLoss fell to $14,090k in Q1 FY2016
  (accn 0001193125-15-213442). Net AR *declined* across the charged quarter
  ends: $445,050k (2014-11-01, accn 0001193125-14-433564) → $420,955k
  (2015-01-31, accn 0001193125-15-107187) → $393,814k (2015-05-02, accn
  0001193125-15-213442) — no quarter-end AR ramp footprint.
- **FY2013 working-capital divergence** (pre-window): AR $330,238k
  (2013-02-02) → $453,496k (2014-02-01) and InventoryNet $250,420k →
  $347,861k (both accn 0001193125-14-118715) against Revenues $3,168,630k
  (FY2012) → $3,404,400k (FY2013) (accn 0001193125-15-107187).
- **Allowance decline**: AllowanceForDoubtfulAccountsReceivableCurrent
  $7,366k (2011-01-29) → $2,663k (2012-01-28, accn 0001193125-12-134488); no
  allowance fact after 2012-01-28.
- **Chronology**: NT 10-Q 2006-09-07 / NT 10-Q/A 2006-09-28 / NT 10-Q
  2006-12-06 / NT 10-K 2007-03-29 / NT 10-Q 2007-06-08 / 10-Q/A 2007-07-02 /
  10-K/A 2007-07-13 (submissions JSON) — the options-review-era cluster. G&A
  spike $102,728k, 2009-02-01→2009-05-02 (accn 0001193125-10-134950).

The scheme's defining falsity — undisclosed acceleration of real sales plus
the MD&A trend omission — has no XBRL tag; beyond the revenue/NI step-down
above, no numeric trace of the pull-ins exists in the sealed facts. This
section describes the information set — it does not re-score the case.

## 4. WHAT THE LLM CAUGHT

Frozen output `runs/main/case_13.json`: `misstatement_probability`: 55
(legacy v1 key — an uncalibrated ordinal score; see
specs/RISK_SCORE_SEMANTICS.md) = score 55, risk_tier "watch"; CL1/CL4/
CL6/CL7 flagged; three mechanism hypotheses. Quotes grep-verified in the
frozen outputs; values verified against sealed XBRL and submissions JSON.

| model claim (verbatim) | enforcement/restatement reference | match quality |
|---|---|---|
| "Improper stock option grant-date/exercise-price accounting (backdating-type issue) requiring restatement" (top hypothesis, direction "understated") | Charged scheme is the pull-in plan (¶1–2); backdating appears only as ¶4 prior history ("improperly backdating stock options", 2008 settlement) | unrelated |
| "Possible premature revenue recognition, extended payment terms, or channel stuffing near FY2013 (fiscal year ended 2014-02-01), where receivables and inventory grew far faster than revenue, consistent with pulling forward sales" (hypothesis 2, accounts Revenues/AR/Inventory) | ¶1: "accelerate, or pull-in, sales that had originally been scheduled for future quarters to the current quarter"; ¶9 incentives include "extended payment terms" — but the Relevant Period is 2015-01~07 (¶2, D2), not FY2013 | exact mechanism |
| "Under-reserving for doubtful accounts as receivable allowance fell 63.9%" (hypothesis 3) | No allowance/reserve allegation appears in 33-10684.pdf.txt | unrelated |
| "Anomalous one-quarter G&A spike to $102.7M ... suggesting one-time charges tied to the historical governance issue" (top_signals[1]) | No counterpart in the order | unrelated |

The "exact mechanism" enum call on row 2 carries a period offset (FY2013 vs
the D2 window) and a rank caveat — see §7. Main-frame grades: DIM1=1,
DIM2=0 (top-ranked-only rubric; coverage note: hypothesis 2 "substantially
matches the enforcement description and would have scored ~2 had it been
ranked first; it targets FY2013 rather than the FY2015 window"), DIM3
"active" = 2 (genre match vs key active(revenue)), DIM4=3.

Perturbed frame (`runs/perturbed/case_13.json`): score 42, "watch"; top
hypothesis "Disproportionate release/reduction of the allowance for doubtful
accounts" (unrelated accounts, ~3 years pre-window); the third-ranked
"aggressive revenue recognition" hypothesis is, per the grade rationale,
"materially closer to the true mechanism, but rubric grades top-ranked
only." Perturbed grades: DIM1=0 (42<50), DIM2=0, DIM3 "omission-estimate" =
0, DIM4=3.

## 5. WHAT THE LLM MISSED

From the sealed §3 information set, against the truth mechanism (pull-in
acceleration + disclosure omission, window 2015-01~07):

- **Relevant-Period step-down quoted but discounted**: the main frame quoted
  the Q1 FY2016 NI collapse ("NetIncomeLoss=14090000 (2015-02-01 to
  2015-05-02) ... sharp drop from prior quarter 81693000", CL5 evidence) yet
  set CL5 no_flag and anchored no hypothesis on the 2015 quarters; its
  revenue-acceleration hypothesis targeted FY2013 instead.
- **No numeric pull-in footprint to miss**: net AR declined across both
  charged quarter ends (§3) and the falsity lived in MD&A/guidance framing
  (¶33–34, ¶41), invisible at XBRL granularity — charging the model with a
  miss of the window itself would overstate detectability (§7; D21
  DATA(design) attribution). No other truth-mechanism footprint identified
  from sealed evidence.

`analysis/error_analysis.md` §4 excludes MRVL from earliness measurement:
"d2=0 — 무관 신호라 조기성 무의미, 제외" (top-evidence 2010-06, backdating
narrative).

## 6. ERROR TAXONOMY

Outcome is TP at threshold in the main frame only; recorded errors are
dimension-level (DIM2=0 both frames; perturbed DIM1=0, DIM3=0). Buckets per
`scoring/error_taxonomy.md`, atlas vocabulary:

- **Interpretation (main frame, mechanism content)**: the score's top
  narrative rebuilt the 2006-07 options era from the NT/amendment cluster —
  a real prior event (order ¶4) but not the charged mechanism.
  `analysis/error_analysis.md` §2: "동상 — 옵션 백데이팅(2006-07) 서사;
  정답은 pull-in (창 2015)"; §5 notes the same "10-Q/A 군집 + 2006-07 →
  백데이팅" template also fired on control FORR (2/2 unhelpful in this
  sample).
- **DATA(design) (perturbed frame, finalized)**: D21
  (`scoring/decisions_log.md`, RP-09 Stage 0, commit 986a893) adopted
  "MRVL(perturbed case_13) UNCLASSIFIED×2 → DATA(design) PROPOSAL" — the
  perturbed misses are attributed to information-set design limits for a
  disclosure-side scheme, not finalized as model error.
- **Computation / Retrieval**: none found — cited values spot-verified at
  value+date+accession level against `~/aaer-data/MRVL/xbrl/CIK0001058057.json`
  (AR $330,238k/$453,496k; InventoryNet $250,420k/$347,861k; allowance
  $7,366k→$2,663k; G&A $102,728k; §3) and the NT/amendment dates against the
  submissions JSON.
- **Label-noise**: none — AAER-confirmed settled order; $5,500,000 penalty
  (§IV.B).
- **Suspected-memorization — both sealed draws agree: recognized**: Draw 1
  (`scoring/probe_results/recognition/case_13.json`): company_guess "Marvell
  Technology Group Ltd.", confidence "medium". Draw 2
  (`analysis/name_probe_results.json`, row case_13): same guess, "medium",
  recognized: true — no cross-draw disagreement (L-5: verdicts can vary;
  here they concur). memorization_suspect_condition2: false in both grade
  records — neither frame cites post-cutoff facts (no AAER-4076, no
  "pull-in" terminology, no revelation/outcome). D8 delta +13, within
  perturbed draw noise per `review_packets/RP-06_hardening.md` (sd 11.7).

## 7. CPA JUDGMENT — human_finalized: false

Draft, unaudited work product until owner sign-off (PROJECT.md §7).

- This TP is a right-score/wrong-reason hit whose *second* hypothesis was
  substantively right: "pulling forward sales" on Revenues/AR with "extended
  payment terms" is the pull-in mechanism, misdated to FY2013 and ranked
  behind a backdating narrative — DIM2=0 under the top-ranked-only rubric;
  ~2 under a rank-weighted one (grade rationale). **[OWNER REVIEW]**
- The §4 enum call "exact mechanism" for hypothesis 2 despite the FY2013 vs
  2015-01~07 period offset is a judgment; "right account wrong mechanism" is
  arguable if the window is treated as part of the mechanism. **[OWNER REVIEW]**
- Detectability: pull-ins were $24M of $857M (3%) and $64M of $724M (9% of
  total revenues, ¶14, ¶19) of *real* accelerated sales, with net AR falling
  at both charged quarter ends (§3) and the operative falsity in undisclosed
  MD&A trend information (¶41). Proposed reading: the numeric set could
  support suspicion (score 55) but arguably could not identify this
  mechanism — consistent with D21's DATA(design) call. **[OWNER REVIEW]**
- Identity effect: recognized at medium confidence in both draws, Δ +13,
  but the five perturbed draws straddle the threshold (25–58). Proposed
  reading: the TP-vs-miss split across frames is within sampling noise, so
  the headline TP should carry the RP-06 dispersion. **[OWNER REVIEW]**
- The backdating top narrative echoes a genuine prior enforcement event the
  order itself records (¶4) — not a hallucination, but as a ranking it
  displaced the correct story; template-reuse risk documented in
  `analysis/error_analysis.md` §5. **[OWNER REVIEW]**

## 8. AUDIT TRANSLATION

Procedures the flag and the §3 signals would motivate (procedures, not
conclusions):

- Quarter-end cutoff testing of shipments against original
  customer-requested delivery dates; test sales-order modification logs for
  scheduled-shipment-date changes from a subsequent quarter into the current
  quarter (the order's own pull-in definition, ¶7 fn.2).
- Side-agreement and incentive review for period-end sales — rebates,
  discounts, free product, extended payment terms (¶9) — reconciled to the
  stated revenue recognition policy; customer confirmations of requested
  delivery dates, early-acceptance requests, and customer inventory levels
  (¶28 excess-inventory dynamic).
- MD&A / Item 303 review: compare internal FP&A tracking of "natural" vs
  pull-in-assisted revenue and backlog percentage (¶8) against disclosed
  trend language; test disclosure-committee consideration (¶35) and
  board-package completeness (¶37 records deletions of pull-in references).
- For the model's own signals: receivables confirmations and allowance
  recomputation for the FY2013 AR/inventory divergence.

## 9. FINANCIAL STATEMENT IMPACT

The sealed order text contains no restatement: the string "restat" does not
appear anywhere in `~/aaer-data/MRVL/33-10684.pdf.txt`, and the violations
found are disclosure/reporting provisions only — Securities Act 17(a)(2) and
17(a)(3) and Exchange Act 13(a)/Rules 13a-1, 13a-13, 12b-20 (¶3, ¶40–41),
with the Section 13(a) violation framed as failure to disclose a known trend
in MD&A of the FY2015 Form 10-K and Q1 FY2016 Form 10-Q (¶41). No GAAP
misstatement of a line item is alleged. Quantified scheme magnitudes stated
in the order: pull-ins of $24 million (Q4 FY2015, ¶12), $64 million (Q1
FY2016, ¶18), $77 million (Q2 FY2016, ¶21); without pull-ins Marvell "would
have missed the low-end of its revenue guidance by the far greater margin of
approximately $50 million" in Q4 FY2015 (¶14) and "approximately $30
million" in Q1 FY2016 (¶19). Registered record concurs (`candidates.json`
T17 notes: "Marvell did NOT restate"). Restated line items and amounts: none
stated in the sealed sources; per-line impact not determinable beyond the
figures quoted above.

---
*Entry status: drafted (sections 7–9 pending owner finalization).*
*채점: Claude 보조 + 인간 최종 확정. 교육·정보 목적, 투자 자문 아님.*
