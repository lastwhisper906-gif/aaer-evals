# atlas/case_03.md — Logitech International S.A. (LOGI) — wave-1 treatment T12

Authored by Claude Code, pending human audit (D15). Analytical document under D106 ② — not a scored output. 본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).

## 1. CASE HEADER

| field | value |
|---|---|
| Case ID (anonymized frame) | case_03 (scoring ID T12) |
| Cohort | wave-1 |
| Outcome class | FN (main frame, flag at score ≥50) |
| Ground-truth tier | AAER-confirmed (AAER-3765 / Rel. 34-77644, File 3-17212) |
| Frozen score | score 42 (`runs/main/case_03.json`, run `original-case_03-r1`); perturbed frame score 45 (`runs/perturbed/case_03.json`, run `perturbed-case_03-r1`) |
| Grade record | `scoring/grades/main/case_03.json` and `scoring/grades/perturbed/case_03.json` (human_finalized: true, RP-09 Stage 0, commit 986a893, 2026-07-07) |

Company: Logitech International S.A., CIK 0001032975, cutoff 2013-08-06
(`data/candidates/candidates.json` T12; `data/evaluatee/cases.json` case_03).
Perturbation delta: score 42 → 45 (+3). Per D8 the delta measures memorization
contribution — not a robustness pass/fail. As a recorded fact, both frames fall
below the ≥50 flag band (DIM1=0 in both grade records) — the miss is frame-stable.

## 2. ACTUAL EVENT

SEC Order Instituting Cease-and-Desist Proceedings, In the Matter of Logitech
International, S.A., Michael Doktorczyk, and Sherralyn Bolles, CPA, Exchange Act
Rel. 34-77644 / AAER-3765 (April 19, 2016), settled without admitting or denying.
Sealed local text: `~/aaer-data/LOGI/34-77644.pdf.txt` (manifest-pinned,
`data/manifests/aaer_data_manifest.json`). Fiscal year is April 1 to March 31 (fn.2).

Per the order (Summary), "recurring instances of improper accounting in three
separate areas" over "a five-year period": (a) "fraudulently accounting for the
write-down of a failed product" — the Revue set-top box — in FY11: the year-end LCM
analysis "recorded a $2.2M adjustment" only (¶14) against internally flagged
"total potential excess inventory of $19.4M for Revue units and components" (¶12);
"LOGI overstated its operating income by $30.7M, i.e., over 27%" (¶27); (b) FY12-13
warranty accruals under a non-GAAP model (the FY13 10-K "misstated the amount of
its product warranty liability by over $17.2M", ¶48), plus the uncorrected failure
to amortize acquired intangibles, "estimated at approximately $1.87M" (¶46-47);
(c) FY09 AMR revenue recognition on "sell-in" to its largest Distributor amid a
"hockey stick" quarter-end pattern (¶60): "LOGI materially overstated its
operating income by approximately $16.2M in FY09" (¶73).

Registered summary (`data/candidates/candidates.json`, T12 `scheme_summary`):
delayed ~$30.7M LCM write-down of Revue inventory inflating FY2011 operating income
~27%; understated FY12-13 warranty liabilities; failure to amortize acquired
intangibles; FY09 Americas revenue-recognition/controls violations. `scheme_type`:
inventory, reserves_smoothing, revenue_recognition; manipulation period 2008-04 to
2013-03; first revelation 2013-08-07 (FY13 10-K/A).

GAAP topics, as cited by the order: ASC 330-10-35 Inventory — Subsequent
Measurement (fn.3); SFAS 5 codified as ASC 460-10-25, Product Warranties (fn.4);
SFAS 48, codified "as ASC 605-15-25 for FY10 and later" (fn.6). No other ASC topics
attributed from sealed evidence.

## 3. SIGNALS AVAILABLE PRE-CUTOFF

Cutoff 2013-08-06 (`data/evaluatee/cases.json`, case_03). Sealed deck basis:
`~/aaer-data/LOGI/xbrl/CIK0001032975.json` (XBRL company facts) and
`~/aaer-data/LOGI/edgar/CIK0001032975*.json` (filing chronology). Pre-cutoff, at
accession level:

- **FY2011 inventory build — the scheme year**: InventoryNet $219,593K at
  2010-03-31 (accn 0001032975-10-000019) → $300,630K at 2010-12-31, the Revue
  launch/production-halt quarter-end (accn 0001193125-11-025852) → $280,814K at
  2011-03-31 (accn 0001193125-11-153485), +27.9% YoY against SalesRevenueNet
  +20.1% ($1,966,748K FY2010 → $2,362,886K FY2011); then $297,072K at 2012-03-31
  on falling revenue ($2,316,203K FY2012, accn 0001047469-12-006385).
- **Margin fade**: GrossProfit/SalesRevenueNet 35.4% FY2011 ($836,506K/$2,362,886K)
  → 33.5% FY2012 ($776,589K/$2,316,203K) (accns 0001193125-11-153485,
  0001047469-12-006385).
- **Warranty accrual flat-to-declining at ~$2.1-2.4B revenue scale**:
  ProductWarrantyAccrualClassifiedCurrent $4,970K at 2011-03-31 (accn
  0001104659-11-061563) → $5,184K at 2012-03-31 (accn 0001047469-12-006385 —
  the balance the order describes as "reserved $5.2M", ¶53) → $4,243K at
  2012-09-30 → $3,397K at 2012-12-31 (accns 0001104659-12-074325,
  0001104659-13-007557) → $5,156K at 2013-03-31 (accn 0001047469-13-006614).
- **Filing-chronology friction**: NT 10-Q 2009-08-06; 10-Q/A 2010-08-25 (accn
  0001032975-10-000019) and 10-Q/A 2011-09-06 (accn 0001193125-11-241116) amending
  consecutive Q1 filings; CORRESP 2013-01-22 shortly before the 8-K of 2013-01-24
  (`~/aaer-data/LOGI/edgar/CIK0001032975*.json`; as itemized in the frozen CL7).
- The revelation FY13 10-K/A of 2013-08-07 post-dates the cutoff — not in the
  information set.

This section describes the information set — it does not re-score the case.

## 4. WHAT THE LLM CAUGHT (sub-threshold — FN)

Frozen output `runs/main/case_03.json`: `misstatement_probability`: 42 (legacy v1
key — an uncalibrated ordinal score; see specs/RISK_SCORE_SEMANTICS.md) = score 42,
risk_tier "watch"; CL4 (inventory/margin, confidence "low"), CL6 (allowance
decline), CL7 (chronology) flagged. All assertions below sat under the ≥50 flag
band. Original frame primary; quotes grep-verified in the frozen output, values
verified against the sealed XBRL file.

| model claim (verbatim) | enforcement/restatement reference | match quality |
|---|---|---|
| "Possible delayed/insufficiently conservative goodwill impairment testing in FY2010-FY2012 … before a sudden, very large non-cash impairment was recognized in Q3 FY2013" (hypothesis 1, top-ranked, direction "overstated") | No goodwill-impairment allegation in 34-77644.pdf.txt; nearest truth leg is the uncorrected "failed to amortize certain intangibles" error, ~$1.87M (¶46-47) — different account (goodwill vs amortizable acquired intangibles), different treatment (impairment testing vs amortization) | right direction only |
| "Reduction of bad debt allowance … could reflect reserve releases that modestly understate the allowance for doubtful accounts" (hypothesis 2, direction "understated") | No AR-allowance allegation; nearest truth leg is the warranty under-accrual — "reserved $5.2M … should have reserved $25.5M -- an under-accrual of over $21M" (¶53) — a reserve understated, but a different liability account | right direction only |
| "Inventory build-up in FY2012 … despite a revenue decline … could indicate delayed recognition of inventory obsolescence/excess reserves, deferring cost of goods sold recognition" (hypothesis 3, direction "timing_shift") | Core scheme: "errors in the timing of the Revue-related inventory write-downs" (¶27); FY11 LCM analysis that "recorded a $2.2M adjustment" against $19.4M flagged exposure (¶14, ¶12) | exact mechanism |

Row 3 is the striking record: the mechanism the order establishes — delayed
inventory write-down for excess/obsolete product — appears in the frozen output,
but ranked third, centered one fiscal year late (FY2012 build vs the FY2011 Revue
close), and under a score of 42. Row 1 carries the grade: DIM2=1 both frames,
main-frame rationale "adjacent-correct account area" with the 0-vs-1 call left to
the human auditor; the same rationale notes the third-ranked hypothesis "would be
~2 in account+direction+treatment" had it been top-ranked
(`scoring/grades/main/case_03.json`). Genre omission-estimate = key: DIM3=2; DIM4=3,
both frames. Perturbed frame (`runs/perturbed/case_03.json`): score 45, "watch";
same goodwill-first ranking on scaled values; CL1 flips to flag, CL8 to
insufficient_data.

## 5. WHAT THE LLM MISSED

From the sealed §3 information set, by truth leg:

- **Revue LCM timing (the fraud leg)** — surfaced but mis-ranked and mis-dated.
  The sealed series place the sharper anomaly in FY2011 itself: inventory +27.9%
  vs revenue +20.1%, peaking at $300,630K at 2010-12-31 — the quarter-end at
  which the order records production halted with no write-down taken (¶4-5). The
  frozen output anchored on the milder FY2012 comparison ($280,814K → $297,072K
  vs −2.0% revenue) and never cited the FY2010→FY2011 build. The signal
  corresponding to the actual mechanism was in the information set and was
  under-weighted, not absent.
- **Warranty under-accrual** — not surfaced anywhere. The sealed public XBRL
  carries a pre-cutoff warranty-accrual series flat-to-declining ($5,184K at
  2012-03-31 → $3,397K at 2012-12-31) against $2.1-2.3B revenue — squarely CL6's
  question, yet CL6 was answered solely with the AR bad-debt allowance. Whether
  the warranty series was in the deck payload is not determinable from the sealed
  evidence read (CL8's enumeration of provided series lists no warranty tag) —
  attribution deferred to §6/§7.
- **Intangibles amortization (~$1.87M)** — insufficient sealed evidence: no
  distinct footprint at that magnitude in the deck-level
  IntangibleAssetsNetExcludingGoodwill series (declining throughout).
- **FY09 AMR revenue recognition** — insufficient sealed evidence: FY09 (ended
  2009-03-31) largely pre-dates the sealed XBRL series coverage; no distinct
  pre-cutoff footprint identifiable for the sell-in/hockey-stick leg.

## 6. ERROR TAXONOMY

Outcome is FN; `scoring/error_taxonomy.md` buckets, atlas vocabulary:

- **Interpretation** (primary): `analysis/error_analysis.md` §1 classifies T12 as
  "분류 (ii): 증거 존재, 순위 판단 실패" — evidence present, ranking failure: the
  third-ranked hypothesis in-substance captured the answer mechanism, but the
  goodwill narrative was ranked first and the score held at 42. §5 adds a
  period-anchoring component (FY2012 vs FY2011). The warranty leg is an R1
  question: if the series was absent from the deck payload, that portion is
  DATA, not MODEL — undetermined here.
- **Computation / Retrieval**: none found — checklist and hypothesis values
  spot-verified at value+date+accession level against
  `~/aaer-data/LOGI/xbrl/CIK0001032975.json` (§3).
- **Label-noise**: none — AAER-confirmed tier; settled order with a $7,500,000
  company civil money penalty (34-77644.pdf.txt §IV.D).
- **Suspected-memorization — recognized in BOTH sealed draws, yet FN**: Draw 1
  (`scoring/probe_results/recognition/case_03.json`): company_guess "Logitech
  International S.A.", confidence "high". Draw 2
  (`analysis/name_probe_results.json`, row case_03): guess "Logitech International
  S.A.", confidence "medium", recognized: true (L-5: verdicts vary across draws —
  here both recognize; confidence differs). Both grade records set
  memorization_suspect_condition2: false — reasoning "anchored throughout in
  concrete provided data content", "no mention of the SEC enforcement action, the
  AAER, the Revue-specific revelation, or any fact public only after the cutoff".
  The FN-despite-recognition combination is internally consistent with the frozen
  record: recognizing the issuer did not import outcome knowledge, and the
  identity-masked frame scored higher, not lower (42 → 45, D8 delta +3) — the
  opposite sign from a recognition-boosted hit. Recognition without conversion
  points to an analysis-ranking failure, not a contamination artifact.

## 7. CPA JUDGMENT — human_finalized: false

Draft, unaudited work product until owner sign-off (PROJECT.md §7).

- The output's accounting instinct — an estimate omitted or delayed until a
  catch-up charge — was correct in genre (DIM3=2, exact) but attached to the
  loudest balance (the visible Q3 FY2013 goodwill impairment) instead of the
  quieter one the order establishes (Revue inventory carried above market at the
  FY2011 close). The big-bath narrative explained the symptom the deck displayed
  most dramatically; the fraud lived in a smaller, earlier reserve.
  **[OWNER REVIEW]**
- The main-frame grader's DIM2 0-vs-1 borderline (goodwill as "adjacent" to
  amortizable acquired intangibles) is expressly deferred to the human auditor in
  the grade rationale; this entry records it without taking a position.
  **[OWNER REVIEW]**
- Score 42 with three flagged checklist items: under the frozen consistency rule
  the "watch" tier is coherent with the band, so the FN is a within-rubric
  confidence-setting outcome — the model held its inventory hypothesis at CL4
  confidence "low" and ranked it third. **[OWNER REVIEW]**
- Warranty-leg attribution (DATA vs MODEL) turns on whether the deck payload
  carried any warranty series; the sealed public XBRL did (§3), and CL8's list of
  provided series names none. R1 requires a deck-payload inspection before
  charging this leg to the model. **[OWNER REVIEW]**

## 8. AUDIT TRANSLATION

Procedures the near-miss signals would motivate (procedures, not conclusions):

- LCM recomputation for slow-moving product lines: test market-value assumptions
  against planned price reductions and actual sell-through; corroborate
  component build-out assumptions with operations personnel; test
  purchase-commitment liabilities for stopped products; months-of-supply
  analytics at the launch-quarter inventory spike.
- Warranty reserve recomputation on an independent waterfall model using
  sell-through data and contractual terms; sensitivity-test the recorded model to
  warranty-term-length changes; inquire into management "exposure lists" or other
  schedules of uncorrected items.
- Recompute amortization of acquired intangibles from the FY10 purchase price
  allocation forward.
- Distributor confirmations of return rights, discounts, and quarter-end
  incentive terms; sell-in vs sell-through analysis against the "hockey stick"
  intra-quarter shipment pattern.

## 9. FINANCIAL STATEMENT IMPACT

From the enforcement text actually read (34-77644.pdf.txt): FY11 operating income
overstated — "LOGI reported operating income of $142.7M" (¶26); properly
accounted, "it would have reported operating income of approximately $112M" —
"LOGI overstated its operating income by $30.7M, i.e., over 27%" (¶27); "On
November 14, 2014, LOGI restated its financial results for FY11 and FY12" for
Revue write-down timing (¶27). Warranty: FY12 "reserved $5.2M … should have
reserved $25.5M -- an under-accrual of over $21M" against reported net income of
$71.5M; "in FY13, LOGI’s accrual was over $17M lower than the GAAP-compliant model
required" (¶53); the FY13 10-K "misstated the amount of its product warranty
liability by over $17.2M" (¶48). Intangibles amortization error "estimated at
approximately $1.87M" (¶46). FY09: "gross sales would have been $52M lower in
FY09"; operating income overstated "by approximately $16.2M" (¶73). "On August 7,
2013, LOGI filed an amended Form 10-K for FY13, disclosing and correcting the
warranty accrual and amortization expense errors, revising its financial
statements for FY09 through FY13" (¶54). Full restated per-line-item, per-period
amounts: not determinable — the sealed order does not tabulate them, and no
restatement filing text is among the sealed sources read.

---
*Entry status: drafted (sections 7–9 pending owner finalization).*
*채점: Claude 보조 + 인간 최종 확정. 교육·정보 목적, 투자 자문 아님.*
