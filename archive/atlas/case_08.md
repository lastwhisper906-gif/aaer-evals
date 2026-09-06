# atlas/case_08.md — Hertz Global Holdings, Inc. (HTZ) — wave-1 treatment T13

Authored by Claude Code, pending human audit (D15). Analytical document under D106 ② — not a scored output. 본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).

## 1. CASE HEADER

| field | value |
|---|---|
| Case ID (anonymized frame) | case_08 (scoring ID T13) |
| Cohort | wave-1 |
| Outcome class | TP (main frame, flag at score ≥50; perturbed frame also ≥50) |
| Ground-truth tier | AAER-confirmed (AAER-4012 / Securities Act Rel. 33-10601 / Exchange Act Rel. 84979, File 3-18965) |
| Frozen score | score 78 (`runs/main/case_08.json`, run `original-case_08-r1`); perturbed frame score 55 (`runs/perturbed/case_08.json`, run `perturbed-case_08-r1`) |
| Grade record | `scoring/grades/main/case_08.json` and `scoring/grades/perturbed/case_08.json` (human_finalized: true, RP-09 Stage 0, commit 986a893, 2026-07-07) |

Company: Hertz Global Holdings, Inc., deck CIK 0001657853 (post-2016-reorg
successor; the misstated filings were by predecessor CIK 0001364479 per
candidates notes), cutoff 2014-05-12 (`data/candidates/candidates.json` T13;
`data/evaluatee/cases.json` case_08). Perturbation delta: score 78 → 55 (−23).
Per D8 the delta measures memorization contribution — not a robustness
pass/fail. Both frames cleared the flag band (TP frame-stable at threshold
50); the identity-bearing frame scored 23 points higher.
`analysis/error_analysis.md` §2 directs: "HTZ는 각인된-유죄(Δ −30.2)와 겹쳐
읽어야 한다 (§3.5 그림)" — the single-draw delta here is −23; the −30.2
statistic's basis is not restated in the sections read (§7).

## 2. ACTUAL EVENT

SEC Order, In the Matter of Hertz Global Holdings, Inc. and The Hertz
Corporation, Securities Act Rel. 33-10601 / AAER-4012 (Dec. 31, 2018), settled
cease-and-desist. Sealed local text: `~/aaer-data/HTZ/33-10601.pdf.txt`
(manifest-pinned, `data/manifests/aaer_data_manifest.json`). "From at least
February 2012 through March 2014" Hertz's filings materially misstated pretax
income "because of accounting errors made in a number of business units", as
reflected in the Restatement filed July 16, 2015 (¶2). Legs:

- **Subrogation allowances/reserves (ASC 450)**: "allowance related expenses
  were understated and income was inflated because Hertz relied on
  inappropriate estimation methodologies that resulted in inadequate
  allowances and write-offs" (¶2); subrogation was booked by "recording income
  and a receivable for amounts subject to recovery, partially offset by an
  associated expense and allowance" (¶10; "ASC 450-20-25-2 requires the
  accrual of losses from uncollectible receivables", ¶11). From August 2012,
  "Hertz did not significantly increase its allowance for or write off such
  amounts when sent to attorneys for collection" (¶12) despite ~2% actual
  attorney collection rates (¶13); repeated 2013 methodology changes each had
  "a favorable impact" and each "was not in accordance with U.S. GAAP" (¶14) —
  a May 2013 spreadsheet-error fix booked at <$1M instead of $7M (¶15), a
  fall-2013 "gap-closing" re-reserving at "approximately 4%, which implied a
  96 percent" recovery rate (¶16-17), three ~$1M undocumented post-close
  adjustments (¶18).
- **Fleet depreciation / holding periods (ASC 250-10-50-4)**: 2013 extensions
  of planned U.S. fleet holding periods ("from 20 to 24 or 30 months" for top
  models, ¶19) "spread out over more months the depreciation expense Hertz had
  to incur on its cars, lowering such expense overall for current quarters"
  (¶20) — a change in estimate requiring disclosure (¶21) that the Q2/Q3 2013
  10-Q and FY2013 10-K MD&As did not adequately disclose (¶22-25).
- **November 2013 guidance** reaffirmed despite internal estimates below the
  range (¶27-30); **ICFR** material weaknesses including "inadequate controls
  over accounting estimates, changes to accounting policies, journal entries,
  and the period-end financial reporting process" (¶31).

Violations: Securities Act §§17(a)(2)-(3); Exchange Act §§13(a),
13(b)(2)(A)-(B), 15(d) and rules (¶38); $16,000,000 civil penalty (§IV.C).
Registered summary (`data/candidates/candidates.json` T13 `scheme_summary`):
overstated pre-tax income via allowances/reserves and expense timing plus
fleet holding-period extensions lowering depreciation; `scheme_type`
reserves_smoothing + expense_capitalization + disclosure_only; manipulation
period 2012-02 to 2014-03; first revelation 2014-05-13 (order ¶33: Hertz
announced it was "unable to file its Form 10-Q for the first quarter of 2014"
with a possible FY2011 restatement).

## 3. SIGNALS AVAILABLE PRE-CUTOFF

Cutoff 2014-05-12. Sealed basis: `data/evaluatee/cases.json` case_08 (identity
metadata only — the payload reaches the model as XBRL series plus filing
chronology, per the frozen output's own CL8 coverage note), the frozen
outputs' quoted deck values, `~/aaer-data/HTZ/xbrl/CIK0001364479.json`, and
`~/aaer-data/HTZ/edgar/` (submissions metadata). Filing narrative text (MD&A)
is not among the sealed sources — filing-text quotes: **insufficient sealed
evidence**. Data-point signals, all filed ≤ 2014-05-12:

- **Restatement-adjacent chronology**: NT 10-K 2014-03-03; FY2013 10-K
  2014-03-19; 10-K/A 2014-03-20 (accn 0001364479-14-000008) — a one-day
  amendment; earlier NT 10-Ks 2009-03-03 and 2013-03-04 (frozen output CL7).
- **AR vs revenue divergence, then reversal**: AccountsReceivableNet $1,616.4M
  (2011-12-31) → $1,879.7M (2012-12-31) → $1,512.6M (2013-12-31) vs Revenues
  $8,299.3M → $9,024.9M → $10,771.9M (accns 0001445305-13-000446,
  0001364479-14-000008; 2011-12-31 value spot-verified at 1,616,382,000 in the
  sealed company facts).
- **Q4 2012 goodwill/intangibles step-up** (benign origin — Dollar Thrifty
  acquisition, closed Nov 2012, named in the frozen output itself): Goodwill
  $454.7M (2012-09-30, accn 0001445305-12-003378) → $1,329.3M (2012-12-31,
  accn 0001364479-14-000008; spot-verified at 1,329,300,000).
- **Persistent NI vs OCF gap** FY2008-FY2013 (accns 0001047469-11-001397,
  0001364479-14-000008) — structural in a fleet-depreciation business.
- **Absent from the deck** (CL6/CL8): allowance/reserve breakouts, COGS/gross
  margin, and any depreciation-of-revenue-earning-equipment expense series —
  the account-level footprints of both truth mechanisms. The Q2/Q3 2013 10-Qs
  whose MD&As the order faults (¶22-24) are in documents_used (accns
  0001364479-13-000006, 0001364479-13-000011) as numeric series, not text.
- The 2014-05-13 announcement (¶33) and July 2015 Restatement post-date the
  cutoff — not in the information set.

This section describes the information set — it does not re-score the case.

## 4. WHAT THE LLM CAUGHT

Frozen output `runs/main/case_08.json`: `misstatement_probability`: 78 (legacy
v1 key — an uncalibrated ordinal score; see specs/RISK_SCORE_SEMANTICS.md) =
score 78, risk_tier "elevated"; CL1/CL2/CL3/CL7/CL8 flagged; three mechanism
hypotheses. Perturbed frame: score 55, "elevated", three hypotheses on
rescaled values. Model quotes verified verbatim in the frozen outputs; order
quotes grep-verified in `33-10601.pdf.txt`.

| model claim (verbatim) | enforcement/restatement reference | match quality |
|---|---|---|
| "Purchase price allocation / capitalization adjustments related to the Dollar Thrifty acquisition (closed Nov 2012) appear to have been substantially revised … with Goodwill and Intangibles roughly tripling and doubling respectively" (main, hypotheses[0], top-ranked) | No acquisition/PPA finding anywhere in 33-10601.pdf.txt; the order's mechanisms are subrogation allowances (¶9-18), fleet depreciation (¶19-26), guidance (¶27-30) | unrelated |
| "potential overstatement/aggressive revenue-related receivable recognition or delayed write-offs … consistent with a subsequent correction/write-down of previously overstated receivable balances" (main, hypotheses[1]) | ¶12: "Hertz did not significantly increase its allowance for or write off such amounts when sent to attorneys for collection"; ¶10 receivable-and-allowance structure | right account wrong mechanism |
| "a pattern of internal control weaknesses or last-minute accounting corrections that increases the risk of misstatement across multiple periods" (main, hypotheses[2]) | ¶31: "inadequate controls over accounting estimates, changes to accounting policies, journal entries, and the period-end financial reporting process" | right direction only |
| "premature/aggressive revenue recognition or delayed write-off of receivables in 2011-2012" (perturbed, hypotheses[0], top-ranked) | Same ¶10/¶12 subrogation receivable-allowance conduct; the premature-revenue framing has no counterpart in the order | right account wrong mechanism |
| "capitalization of costs that would otherwise be expensed, understating operating expenses relative to cash generation" (perturbed, hypotheses[2]) | ¶20: extensions "spread out over more months the depreciation expense Hertz had to incur on its cars, lowering such expense overall for current quarters" | right direction only |

Main-frame grades: DIM1=2 (score 78 ≥ 70), DIM2=0 (top hypothesis "unrelated
accounts to all three truth mechanisms"; goodwill jump "explained by the Nov
2012 acquisition the output itself names"), DIM3 omission-estimate = 2
(matches key genre), DIM4=2 ("the flagship goodwill/intangible signal is
self-refuted by the acknowledged acquisition"). Perturbed frame: DIM1=1 (score
55), DIM2=1 (account-area credit for "delayed write-off of receivables"), DIM3
mixed = 1, DIM4=3; its coverage note: hypothesis 3 "loosely touches the
expense_capitalization/depreciation leg", but only the top hypothesis is
scored.

## 5. WHAT THE LLM MISSED

From the §3 sealed information set, by truth leg:

- **Subrogation allowance understatement (account level)** — signal NOT in the
  set as a dedicated series (CL6 "insufficient_data"; CL8 flags the absence).
  The main frame's "delayed write-offs" clause reaches the right conduct
  verbally but is subordinated to a receivable/revenue-overstatement framing
  and ranked second; neither frame states allowance-expense understatement.
- **Fleet depreciation / holding-period extension** — not surfaced in either
  frame. No depreciation-of-revenue-earning-equipment series was in the deck,
  and the faulted MD&A narrative (¶22-25) was not part of the numeric payload;
  perturbed hypothesis 3 brushes the direction without the fleet or
  estimate-change content.
- **November 2013 guidance misstatement (¶27-30)** — no press-release/8-K
  narrative in the deck; not surfaced; not chargeable on this information set.
- **What was caught instead**: "10-K/A filed only one day after the original
  FY2013 10-K (2014-03-19 -> 2014-03-20), an extremely unusual amendment
  turnaround suggesting a rapid correction of a known error" (main
  top_signals[0]) — temporally adjacent to the order's "revisions made in
  early 2014" (¶5), though the order does not describe that filing (§7).
  `analysis/error_analysis.md` §4 dates the decisive evidence "2014-03
  10-K(/A)", earliness "0q / 0q" — "폭로 직전 신호".

## 6. ERROR TAXONOMY

Outcome is TP at threshold 50 in both frames; the recorded error is on the
mechanism dimension. `scoring/error_taxonomy.md` buckets, atlas vocabulary:

- **Interpretation** (primary): `analysis/error_analysis.md` §2 row: "HTZ | 78
  | 0 | **점수는 맞고 기제는 틀림** — PPA/goodwill 서사; 정답은 추정
  계정(충당금·감가) 조작". The goodwill top-narrative is a MODEL-side reading
  error on its own terms (the output names the acquisition that explains the
  jump, then leads with the jump as its misstatement narrative — self-refuted
  per the main grade).
- **Retrieval/data boundary**: under R1, the answer key's account-level
  signals (allowance/reserve series, fleet depreciation expense) were absent
  from the provided data (§3, §5) — the mechanism miss has a DATA-side leg
  whose attribution is an owner call (§7). No computation errors found: quoted
  values spot-verified at value+date+accession level against
  `~/aaer-data/HTZ/xbrl/CIK0001364479.json` (§3).
- **Label-noise**: none — AAER-confirmed; settled order, $16,000,000 penalty
  (§IV.C).
- **Suspected-memorization — the two sealed draws DISAGREE (L-5)**: Draw 1
  (`scoring/probe_results/recognition/case_08.json`): company_guess "Hertz
  Global Holdings, Inc. (Hertz Corporation)", confidence "medium". Draw 2
  (`analysis/name_probe_results.json`, row case_08): guess "unknown",
  confidence "low", recognized: false. memorization_suspect_condition2: false
  in both grade records — neither frame cites post-cutoff enforcement facts;
  the perturbed rationale notes the referenced 10-K/A is itself in
  documents_used. The frame delta (78 → 55, −23) carries the sign
  `analysis/error_analysis.md` §2 labels 각인된-유죄 (imprinted-guilty) for
  HTZ — familiarity as an inculpating prior, opposite to the MON FN
  (atlas/case_06.md §6).

## 7. CPA JUDGMENT — human_finalized: false

Draft, unaudited work product until owner sign-off (PROJECT.md §7).

- **TP for partially wrong reasons**: the score cleared the band on chronology
  and trend heuristics (one-day 10-K/A, NT 10-K pattern, AR divergence) while
  the lead mechanism narrative is unrelated to the enforcement findings and
  internally self-refuted. Proposed reading: creditable as risk triage, not as
  mechanism identification — consistent with DIM1=2 / DIM2=0. **[OWNER REVIEW]**
- **The near-miss is buried**: "delayed write-offs" of receivables is the
  verbal shadow of ¶12; inverting the framing (understated allowance expense
  rather than overstated receivables/revenue) would have landed on the
  subrogation mechanism. Whether that inversion was inferable from a deck with
  no allowance series is the key DATA-vs-MODEL attribution question.
  **[OWNER REVIEW]**
- **Fleet-depreciation leg detectability**: its numeric footprint ($15M / $18M
  depreciation-expense declines, ¶23-24) lived in a series the deck did not
  carry; proposed as not chargeable to the model on this information set — a
  materiality-and-coverage judgment. **[OWNER REVIEW]**
- **10-K/A ↔ "revisions made in early 2014" (¶5)**: temporally adjacent, but
  the order never describes the 2014-03-20 10-K/A; equating them would exceed
  the sealed text. **[OWNER REVIEW]**
- **Delta bookkeeping**: single-draw delta −23 vs "Δ −30.2" in
  `analysis/error_analysis.md` §2 (presumed multi-draw statistic, its §3.5
  figure) — confirm the basis before citing the overlay quantitatively.
  **[OWNER REVIEW]**

## 8. AUDIT TRANSLATION

Procedures the §3 signals would motivate (procedures, not conclusions):

- Subrogation allowance recomputation under ASC 450: roll-rate methodology vs
  actual collections by aging bucket and handling channel (attorney-referred
  vs in-house); retest the >360-day 100%-allowance policy and any relief from
  it; back-test allowance changes against subsequent net recovery rates.
- Estimate-change control testing: inventory of 2012-2013 allowance/write-off
  methodology changes with documented rationale, approval, and directional
  impact (a run of uniformly favorable changes is an audit flag, ¶14 pattern).
- Post-close journal-entry testing over estimate accounts (documentation and
  authorization, ¶18 pattern); period-end reconciliation testing (¶31-32).
- Depreciation estimate testing for revenue-earning equipment: planned holding
  periods by model vs depreciation rates in use; ASC 250-10-50-4 disclosure
  evaluation; fleet age/mileage and maintenance-cost analytics against
  depreciation-per-unit trends.
- MD&A consistency procedures: depreciation-driver disclosures and reaffirmed
  guidance vs contemporaneous internal forecasts.

## 9. FINANCIAL STATEMENT IMPACT

From the enforcement text actually read (`33-10601.pdf.txt`): the Restatement,
filed July 16, 2015, covered "2012, 2013, and prior periods, including
selected data for 2011 (unaudited)"; "Including revisions made in early 2014,
the company reduced its previously reported GAAP pretax income by a total of
$235 million" (¶5) — direction: pretax income previously overstated. "The
Restatement identified 17 areas with material accounting errors" and "eleven
separate material weaknesses" (¶5); on July 16, 2015 "Hertz restated its 2011,
2012 and 2013 financial statements and disclosed 11 material weaknesses"
(¶35). Subrogation: "a cumulative pre-tax misstatement of $48 million" (¶9);
the May 2013 correction booked at "less than $1 million" instead of $7 million
(¶15); three post-close adjustments each "improved reported results by
approximately $1 million" (¶18). Depreciation: reported declines of $15
million (H1 2013, ¶23) and $18 million (Q3 2013, ¶24); the restated FY2014
10-K "disclosed that there had been extensions in planned holding periods and
the reduction in the company’s 2013 depreciation expense that resulted from
the longer holding periods", and 2014 "[f]leet related expenses" "increased
$182 million" (¶26). Full restated per-line-item, per-period amounts: not
determinable — the sealed order does not tabulate them, and no restatement
filing text is among the sealed sources read.

---
*Entry status: drafted (sections 7–9 pending owner finalization).*
*채점: Claude 보조 + 인간 최종 확정. 교육·정보 목적, 투자 자문 아님.*
