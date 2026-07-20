# atlas/case_10.md — Ryder System, Inc. (R) — wave-1 control C04 (FALSE POSITIVE)

Authored by Claude Code, pending human audit (D15). Analytical document under D106 ② — not a scored output. 본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).

## 1. CASE HEADER

| field | value |
|---|---|
| Case ID (anonymized frame) | case_10 (scoring ID C04) |
| Cohort | wave-1 (8-control arm) |
| Outcome class | FP (main frame, flag at score ≥50); also flagged in the E2 trajectory layer (`analysis/decision_table.json` L4, threshold-50 cell, `flagged_control` includes case_10) |
| Ground-truth tier | control (no adverse label) |
| Frozen score | score 58 (`runs/main/case_10.json`, run `original-case_10-r1`); no perturbed frame — `runs/perturbed/` contains only the 8 wave-1 treatment cases (frozen asymmetric design, RP-05 J14: 교란 T vs 원본 C) |
| Grade record | `scoring/grades/main/case_10.json` (human_finalized: true, RP-09 Stage 0, commit 986a893, 2026-07-07) — dim1=0 ("output p=58, which is >=50 on a control -> 0 per rubric"), dim2/dim3 null (control), dim4=2, memorization_suspect_condition2=false |

Company: Ryder System, Inc. (R), CIK 0000085961, cutoff 2014-05-12 — copied
from matched treatment T13 HTZ per GP-9 same-snapshot convention
(`data/candidates/candidates.json` C04; `data/evaluatee/cases.json` case_10,
identity metadata only — the payload reaches the model as XBRL series plus
filing chronology, per the frozen output's CL8 coverage note). **This entry
documents a model error on a control company, not a company problem.**

## 2. ACTUAL EVENT

**No adverse event — control** (cleanliness basis per original selection
criteria; formalized criteria at `docs/CONTROL_CRITERIA_v1.md`). Selection
record `data/candidates/candidates.json` C04: "Control for T13 HTZ: 4-axis
match — industry SIC 7510 (Services-Auto Rental & Leasing (No Drivers)), size
rev=6419285000 assets=9367483000 (point-in-time at matched cutoff), period FYE
1231 … Selected per D17"; notes: "Non-enforcement verified 2026-07-06: AAER
index (3,339 entries, AAER 987-4595) name-search negative for the registrant;
secondary web search (2026-07-06) negative for SEC accounting enforcement."
(`review_packets/RP-01_control_group.md` C04 row: "색인·웹 음성".) The company
has **no enforcement action and no restatement in the case window** per those
criteria; additionally, the sealed submissions metadata
(`~/aaer-data/R/edgar/CIK0000085961.json` and `-submissions-001.json`, jointly
spanning filing dates 1994-03-29 → 2026-07-02) contains **zero 8-K filings
with Item 4.02** in their entire history. GP-8 caveat as recorded
(`review_packets/RP-05_results.md` §10): non-enforcement is not proof of
cleanliness — an error in that direction would lower measured specificity,
so the FP finding is conservative on that axis.

## 3. SIGNALS AVAILABLE PRE-CUTOFF

Cutoff 2014-05-12. Sealed basis: the frozen output's quoted deck values,
`~/aaer-data/R/xbrl/CIK0000085961.json` (companyfacts), and
`~/aaer-data/R/edgar/` (submissions metadata). Filing narrative text (MD&A,
amendment explanatory notes) is not among the sealed sources — filing-text
quotes: **insufficient sealed evidence**. The data points the model reacted
to, all filed ≤ cutoff and all verified genuine (§4):

- One 10-K/A, accn 0001193125-12-121535, filed 2012-03-19 — one month after
  the original FY2011 10-K (accn 0001193125-12-065540, filed 2012-02-16). It
  is the only 10-K/A in the sealed submissions history.
- CORRESP/UPLOAD cluster 2011-2013 (sealed submissions: UPLOAD 2011-06-06,
  CORRESP 2011-06-08 … UPLOAD 2013-07-09 — 15 filings).
- Goodwill $216.444M (2009-12-31) → $355.842M (2010-12-31), with the
  2010-12-31 value **first reported in the original FY2010 10-K** (accn
  0000950123-11-013941, filed 2011-02-15); intangibles $39.120M → $72.269M.
  Concurrent sealed acquisition footprint:
  PaymentsToAcquireBusinessesNetOfCashAcquired = $211.897M (FY2010) and
  $361.921M (FY2011) in the same companyfacts.
- Receivables/revenue and allowance-ratio drifts of small magnitude (§4
  table), and a large structural NI-vs-OCF gap (Depreciation $881.216M
  FY2009) that the model itself treated as benign (CL3 no_flag).

This section describes the information set — it does not re-score the case.

## 4. WHAT THE LLM CAUGHT (what the model asserted, and on what evidence)

Frozen output `runs/main/case_10.json`: `misstatement_probability`: 58 (legacy
v1 key — an uncalibrated ordinal score; see specs/RISK_SCORE_SEMANTICS.md) =
score 58, risk_tier "elevated"; CL1 (low), CL2 (medium), CL6 (low), CL7 (high)
flagged; CL3/CL4/CL5 no_flag with benign readings. Top hypothesis: the 10-K/A
"used as the reporting source for a broad swath of FY2008-FY2011 balance sheet
and income statement figures … consistent with a restatement/correction of
previously issued financial statements (ASC 250) or a measurement-period
adjustment to a business combination (ASC 805)"; top_signals[0] calls it a
"strong indicator of a financial restatement". Every cited figure was
grep-verified against the sealed companyfacts/submissions:

| model claim (verbatim) | evidence genuine? (sealed record) | correspondence |
|---|---|---|
| "Revenues=6,050,534,000 (FY2011) vs Revenues=5,136,435,000 (FY2010) = +17.8%" … "ReceivablesNetCurrent=754,644,000 (2011-12-31) vs … 615,003,000 (2010-12-31) = +22.7%" (CL1) | genuine — all four values in `~/aaer-data/R/xbrl/CIK0000085961.json` at the cited dates | n/a — control |
| "Goodwill=355,842,000 (2010-12-31) vs Goodwill=216,444,000 (2009-12-31) = +64.4%" vs revenue "+5.1%" (CL2) | genuine values; but the 2010-12-31 value appears in the **original** FY2010 10-K (0000950123-11-013941), so the companion claim of "a large goodwill step-up recognized only in the year-end/restated figures" (hypotheses[0]) is contradicted by the sealed record | n/a — control |
| "implied allowance/receivables ratio fell from ~2.31% to ~2.18%" (CL6) | genuine — 13,808/598,661 and 16,955/777,370 recompute to the stated ratios (allowance over **net** receivables, as the output's "implied" concedes) | n/a — control |
| "10-K/A filing_date=2012-03-19 … filed roughly one month after the original 10-K (filing_date=2012-02-16), and used as the source accession for numerous FY2008-FY2011 line items" (CL7) | dates and accessions genuine (sealed submissions). The inference drawn from it is not supported: every spot-checked figure the output sources to the 10-K/A (Revenues/NetIncomeLoss/Depreciation/CFO FY2009, StockholdersEquity 2008-12-31, quarterly 2010 NetIncomeLoss) carries a value **identical** to an earlier original filing — no revision footprint in the sealed facts | n/a — control |
| "Multiple CORRESP and UPLOAD filings clustered in 2011-2013" (CL7) | genuine — all listed dates match sealed submissions (which also contain UPLOAD 2013-04-11, unlisted) | n/a — control |
| "NetIncomeLoss quarterly data for 2010 … all sourced from the 10-K/A filed 2012-03-19 rather than contemporaneous 10-Qs" (hypotheses[1]) | source-attribution is genuine as deck metadata, but the same quarterly values sit in the contemporaneous 10-Qs in sealed facts (e.g., Q2 29,841,000 in 0000950123-10-067673; Q3 38,835,000 in 0000950123-10-094963) — the accession label reflects the pipeline's point-in-time reconstruction, not a company revision | n/a — control |

The grade record concurs: "Data points are genuine and specific (meets 2) but
the multi-point combination over-concludes on a clean control, so not 3"
(dim4=2; A2 cross-grade claude-opus-4-8 would have given d4=3 —
`review_packets/RP-06_grading_workbench.md` case_10).

## 5. WHAT THE LLM MISSED

n/a — control: there is no adverse mechanism to miss. Notably, the model
itself supplied benign readings for three checklist axes (CL3 depreciation-
driven NI/CFO gap "structural"; CL4 margins "modest, gradual"; CL5 seasonal
swings "not artificially smoothed") — the error is confined to the promotion
of the CL7/CL2/CL6 pattern into a restatement narrative.

## 6. ERROR TAXONOMY

- **Interpretation (primary)** — evidence-exists / reasoning-failure
  over-reading (error_analysis 분류 (ii) family). First-pass attribution,
  `review_packets/RP-05_results.md` §6 (MECE R1→R3): "R(라이더) d1 | 오탐
  p=58 (대조군) | **MODEL** | R1: 10-K/A 연대기는 실제 데이터. R3: 원본 10-K
  1개월 후 /A(통상 Part III 편입 관행)를 왜곡표시 증거로 과대 해석" — 전건
  인간 확정 대기. `analysis/error_analysis.md` (wave-1 v2-controls FPs) does
  not cover case_10 directly but cites it as the reference axis at line 93:
  LQDT's over-reading is "RP-05의 Ryder 오탐과 같은 축의 추론 실패".
- **Retrieval/data boundary (counter-argument on record)** —
  `review_packets/RP-06_grading_workbench.md` case_10 SKEPTICAL-REVIEW flag:
  the 10-K/A source chronology the model over-read "is metadata injected by
  the pipeline's point-in-time reconstruction" (모델이 과대 해석한 10-K/A 출처
  연대기는 파이프라인의 point-in-time 재구성이 주입한 메타데이터다) — a
  DATA(설계) reattribution argument; flip would move MODEL 5→4, DATA 1→2
  (trust boundary direction unchanged). Owner call.
- **Computation** — none found: all quoted values verified at
  value+date+accession level (§4); ratio arithmetic recomputes.
- **Label-noise** — none within the design: control label verified per §2
  criteria; GP-8 residual (non-enforcement ≠ clean) noted, direction
  conservative.
- **Suspected-memorization** — not indicated on the sealed draws.
  `scoring/probe_results/recognition/case_10.json`: **not present** (that
  probe set covers only the 8 wave-1 treatment cases).
  `analysis/name_probe_results.json` probes this registrant's payload in the
  v2-controls frame as row case_27 (truth_ticker "R"): guess "Waste
  Management, Inc.", confidence "low", recognized: false — one sealed draw;
  probe verdicts vary across draws (L-5). Grade record:
  memorization_suspect_condition2=false ("mentions no post-cutoff facts").
  Interpretive footnote on record (`review_packets/RP-06_hardening.md` §3-2):
  k=5 re-draws of this case scored 58,40,28,25,22 (mean 34.6, σ 13.2, range
  22-58) — the frozen draw-1 score 58 was the maximum of five, 4/5 draws
  below 50; scoring and attribution stay fixed to draw 1.

## 7. CPA JUDGMENT — human_finalized: false

Draft, unaudited work product until owner sign-off (PROJECT.md §7). Why each
flagged pattern is explainable in benign terms — the recurring accounting
shape of FPs:

- **10-K/A ≠ restatement.** An amendment one month after a 10-K, with every
  sealed spot-checked figure identical between the /A and earlier original
  filings, has no restatement footprint; RP-05 records the ordinary
  explanation (Part III incorporation practice — 통상 Part III 편입 관행).
  The model's own hypothesis text concedes the ASC 805 measurement-period
  alternative, then leads with the ASC 250 reading anyway. The decisive test
  it skipped: do any values actually change across filings? Sealed answer: no
  change found. **[OWNER REVIEW]**
- **Goodwill/intangible step-up = the accounting shape of acquisitions.**
  FY2010 goodwill +$139.4M and intangibles +$33.1M against sealed
  acquisition cash outflows of $211.897M (FY2010) and $361.921M (FY2011) is
  the ordinary ASC 805 footprint of purchased businesses; the step-up was
  reported in the original FY2010 10-K, not "only in the year-end/restated
  figures". **[OWNER REVIEW]**
- **Comment-letter correspondence is routine.** CORRESP/UPLOAD filings mark
  an SEC staff review cycle, common for large registrants; the sealed
  metadata carries no content, so treating the cluster as corroboration of a
  restatement narrative (CL7 confidence "high") exceeds the evidence.
  **[OWNER REVIEW]**
- **The allowance drift is immaterial in magnitude.** 2.31% → 2.18% over four
  years (~13bp, on a net-receivables denominator) in a full-service-lease
  receivables book is within ordinary estimation variation; the model itself
  set CL6 confidence "low", then let the item survive into hypotheses[2].
  **[OWNER REVIEW]**
- **Net shape of the error**: genuine, individually weak benign-side signals
  (chronology artifact + M&A step-up + small ratio drift) were compounded
  into an adverse composite — the same over-reading axis error_analysis.md
  assigns to LQDT. The strongest-weighted signal (CL7, confidence "high") was
  the one most dependent on pipeline metadata rather than filing content.
  **[OWNER REVIEW]**

## 8. AUDIT TRANSLATION

Procedures that would have cleared the flag (procedures, not conclusions):

- Read the 10-K/A itself and diff against the original 10-K: identify amended
  items (cover/Part III/exhibits vs financial statements); confirm absence of
  any ASC 250 restatement or Item 4.02 disclosure.
- Search the 8-K record for Item 4.02 and auditor-change items (sealed
  metadata already answers: zero 4.02 in history).
- Obtain the SEC comment letters (UPLOAD) and responses (CORRESP); confirm
  the review closed without restatement.
- Vouch FY2010-FY2011 goodwill/intangible additions to business-combination
  disclosures (ASC 805 purchase-price allocations) and the acquisition cash
  outflows in the cash flow statement.
- Recompute allowance coverage on gross receivables with aging and
  charge-off history to size the 13bp drift.
- Confirm continuity of auditor opinions and ICFR conclusions across the
  amendment period.

## 9. FINANCIAL STATEMENT IMPACT

n/a — no restatement (control). No restated line items exist; the sealed
record contains no Item 4.02 8-K and no enforcement or restatement document
for this registrant (§2).

---
*Entry status: drafted (sections 7–9 pending owner finalization).*
*채점: Claude 보조 + 인간 최종 확정. 교육·정보 목적, 투자 자문 아님.*
