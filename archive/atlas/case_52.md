# atlas/case_52.md — Computer Sciences Corporation (CSC) — wave-2 treatment T02

Authored by Claude Code, pending human audit (D15). Analytical document under D106 ② — not a scored output. 본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).

## 1. CASE HEADER

| field | value |
|---|---|
| Case ID (anonymized frame) | case_52 (scoring ID T02) |
| Cohort | wave-2 |
| Outcome class | FN (main frame, flag at score ≥50) |
| Ground-truth tier | AAER-confirmed (SEC order 33-9804 / AAER-3662, June 5, 2015) |
| Frozen score | score 40 (`runs/wave2/scores/case_52.json`, run `original-case_52-r1`, risk_tier "watch") |
| Grade record | `scoring/grades_wave2/case_52.json` (human_finalized: true, finalized 2026-07-09 via RP-13 workbench; dim1=0, dim2=2, dim4=3) |

Company: Computer Sciences Corporation, CIK 0000023082, cutoff 2010-08-10
(`data/candidates/candidates_wave2.json` T02; `data/evaluatee/cases_wave2.json` case_52).
`analysis/error_analysis_wave2_holdout.md` §2 classifies this FN as "(ii-b) 보정
near-miss, 탐지내용은 맞음" — the detected content was right, the score was not.

## 2. ACTUAL EVENT

In the Matter of Computer Sciences Corporation et al., Admin. Proc. 3-16575; Securities
Act Rel. 9804 / AAER 3662 (June 5, 2015). Sealed local text:
`~/aaer-data/CSC/33-9804.pdf.txt` (manifest-pinned, `data/manifests/aaer_data_manifest.json`).
"From 2009 to 2011, CSC engaged in a wide-ranging accounting and disclosure fraud that
materially overstated its earnings" (¶1, lines 73-74). Three legs:

- **UK NHS contract (POC models)**: a fraudulent "gap closing" exercise contrived
  revenue assumptions to restore the forecast margin (¶3, lines 108-112); models then
  ran on proposed amendments the NHS repeatedly rejected (¶4-5); GAAP violated "by
  failing to impair the value of its contract assets" (¶5, line 134); NHS cash
  advances in operating cash flow "were effectively loans" (¶8, line 158).
- **Australia**: "excess accruals they maintained in 'cookie jar' reserves and by
  failing to record expenses as required," overstating consolidated pretax income by
  over 5% in Q1FY2009 (¶10, lines 192-196; ¶85-89).
- **Nordic region (FY2010)**: "improperly accounting for client disputes, overstating
  assets, and capitalizing expenses" (¶11, lines 198-199), incl. "improperly
  capitalized bench labor costs totaling $8.2 million" (¶97, line 982) and "over $30
  million in prepaid assets that were unsupported" by FY2010 end (fn 32, line 998).

Registered summary: `data/candidates/candidates_wave2.json` T02 `scheme_summary`;
`scheme_type`: revenue_recognition + reserves_smoothing + expense_capitalization +
asset_overstatement; manipulation period 2009-2011.

GAAP topics per the order text (pre-ASC-606 era, stated as such): "For all financial
statement periods ending prior to September 15, 2009, SOP 81-1 was the authoritative
accounting literature. Subsequently, the applicable guidance became ASC 605-35" (fn 7,
lines 357-359); also ASC 450-20-25-2 (fn 24/28), ASC 420-10-25-4 (fn 25), ASC
450-30-25-1 (fn 29), ASC 845-10-30-1 (fn 30), ASC 340-10-5-4 (fn 33), ASC 275 +
Reg S-K 301/303 (fn 7).

## 3. SIGNALS AVAILABLE PRE-CUTOFF

Cutoff 2010-08-10. Sealed data basis: `~/aaer-data/CSC/edgar/CIK0000023082.json` +
`CIK0000023082-submissions-001.json` (chronology), `~/aaer-data/CSC/xbrl/CIK0000023082.json`
(XBRL facts). Pre-cutoff, at accession level:

- **Balance-sheet vs revenue divergence**: OtherAssetsNoncurrent $615M (2009-04-03) →
  $773M (2010-04-02) and ReceivablesNetCurrent $3,786M → $3,849M, while Revenues fell
  $16,740M (FY2009) → $16,128M (FY2010) (all accn 0000023082-10-000036, 10-K FY2010).
- **Accrual/reserve tags present**: AccruedLiabilitiesCurrent had 13 pre-cutoff
  observations, e.g. $1,264M at 2009-04-03 (accn 0000023082-09-000045). The
  AllowanceForDoubtfulAccountsReceivableCurrent series was internally inconsistent:
  $3,786M / $3,849M (accn 0000023082-10-000036, equal to gross receivables) vs $55M
  (2009-07-03, accn 0000023082-09-000045) and $47M (2009-10-02, accn 0000023082-10-000072).
- **Cash flow**: NetCashProvidedByUsedInOperatingActivities $1,986M (FY2009) → $1,643M
  (FY2010) vs NetIncomeLoss $1,115M → $817M (accn 0000023082-10-000036).
- **Chronology friction (prior era)**: NT 10-Q 2006-11-09 (accn 0000023082-06-000150)
  through NT 10-Q 2007-11-08; 10-K/A 2008-01-11 (accn 0000023082-08-000011)
  (`CIK0000023082-submissions-001.json`).

The Australia-inflated Q1FY2009 quarter sits inside the deck's quarterly series
(NetIncomeLoss $121M, cited by the model at CL5). This section describes the
information set — it does not re-score the case.

## 4. WHAT THE LLM CAUGHT

Frozen output `runs/wave2/scores/case_52.json`: `misstatement_probability`: 40 (legacy
v1 key — an uncalibrated ordinal score; see specs/RISK_SCORE_SEMANTICS.md) = score 40,
risk_tier "watch" — below the flag threshold of 50, hence FN. CL1/CL2/CL7/CL8 flagged;
CL3/CL4/CL5 no_flag; CL6 insufficient_data. Cited evidence values re-verified against
the sealed XBRL facts file at value+date+accession level; none fabricated.

| model claim (verbatim) | enforcement/restatement reference | match quality |
|---|---|---|
| "Possible under-impairment or continued capitalization of costs (e.g., deferred contract costs, capitalized software, or transition/setup costs on outsourcing contracts) into Other Assets, Noncurrent" (hypothesis 1, "overstated") | 33-9804.pdf.txt ¶5 (line 134): "failing to impair the value of its contract assets"; ¶97-98: bench-labor capitalization and unsupported "prepaid" assets | exact mechanism |
| "Potential revenue recognition timing acceleration (e.g., percentage-of-completion estimates on long-term outsourcing/systems-integration contracts)" (hypothesis 2, "overstated") | ¶3 (lines 108-112): fraudulent "gap closing" POC model; ¶31-33: NHS contract on POC (SOP 81-1 / ASC 605-35) | exact mechanism |
| "the true allowance for doubtful accounts may be understated relative to receivables outstanding" (hypothesis 3, "understated") | Order alleges excess accruals built and released ("cookie jar", ¶86-88), not AR-allowance understatement; income direction shared, account/mechanism differ | right direction only |
| "History of multiple NT 10-Q/NT 10-K late-filing notices (2006-2007) and periodic-report amendments" (top_signals) | 2006-2008 chronology precedes the 2009-2011 manipulation period (¶1); no counterpart in the order | unrelated |

Notes: grade dim2=2 — "substantially matches the answer key's expense_capitalization
... and asset_overstatement ... in account area, direction (overstated), and treatment
type", but "No case-specific fact from the order ... is named, so not 3"
(`scoring/grades_wave2/case_52.json`). The FN is a score/threshold outcome, not an
absence of the mechanism.

## 5. WHAT THE LLM MISSED

From the sealed §3 information set:

- **Weight, not content — score 40 vs threshold 50**: both answer-key mechanism
  families were surfaced (§4), yet the composite landed 10 points under the flag line.
  `analysis/error_analysis_wave2_holdout.md` §2: "미탐의 실체는 탐지 실패가 아니라 확신
  부족 ... 10점 상향이면 플래그" — under-weighting of surfaced signals, not a missed
  signal class.
- **Reserve axis uncovered despite a usable sealed series**: CL6 examined only the
  inconsistent allowance tags (insufficient_data). AccruedLiabilitiesCurrent — the
  account family of the Australian cookie-jar excess accruals (¶86-88; ASC 450-20-25-2,
  fn 24) — had 13 pre-cutoff observations in the sealed XBRL and was not examined.
  Grade rationale: "reserves_smoothing is uncovered (CL6 = insufficient_data)".
- **OCF strength read as affirmatively mitigating**: CL3 called OCF > NI "the opposite
  of an earnings-quality red flag"; top_signals lists it as "a mitigating (not
  aggravating) factor". Per the order, NHS advances inside operating cash flow "were
  effectively loans" (¶8, line 158; ¶9: "the old fashioned hard way", line 177).
  Advance composition is invisible in the sealed XBRL aggregates — an over-weighted
  mitigant within the information set, not an omitted data point.
- **Australia Q1FY2009 leg**: a >5% consolidated pretax overstatement in one quarter
  (¶85) leaves no distinct ratio footprint in consolidated XBRL — insufficient sealed
  evidence to name a missed signal for that leg.

## 6. ERROR TAXONOMY

Per `scoring/error_taxonomy.md` (R1→R2→R3), atlas vocabulary:

- **Primary — interpretation (MODEL)**: the corresponding signals existed in the
  provided data and were quoted by the model (R1 pass); the dim1 band rule (score <50
  → 0) and pre-fixed threshold force a unique grade (R2 pass); the under-threshold
  composite is a model weighting/calibration error — type (ii-b) per
  `analysis/error_analysis_wave2_holdout.md` §2/§5.
- **Secondary — retrieval/data (DATA, CL6 leg)**: the sealed allowance series is
  internally inconsistent (gross-receivable-sized values vs $55M/$47M), identified by
  the model itself as a likely tagging error; under R1 this input defect owns the
  uncovered reserve axis.
- **Label-noise**: none — AAER-confirmed tier, settled Commission order (§2).
- **Suspected-memorization**: recognition probe — the single stored draw
  `scoring/probe_results_wave2/recognition/case_52.json` — guessed "Computer Sciences
  Corporation (CSC)" with confidence "low" (correct company); verbatim probe
  `scoring/probe_results_wave2/verbatim/case_52.json`: known: false, recall fields
  null. Grade memorization_suspect_condition2: false — reasoning "mentions no
  post-cutoff facts (no reference to the SEC order 33-9804/AAER-3662, the revelation,
  or enforcement outcome)". The correct low-confidence recognition draw is noted for
  the owner-facing record.

## 7. CPA JUDGMENT — human_finalized: false

Draft, unaudited work product until owner sign-off (PROJECT.md §7).

- The FN is a threshold artifact over substantially correct accounting content: the
  two lead hypotheses map to the order's capitalization/under-impairment and
  POC-timing legs. Whether score 40 on an XBRL-only deck is under-confidence or
  defensible conservatism — the dominant NHS scheme lived in contract-level model
  assumptions invisible to consolidated XBRL — is the core owner call. **[OWNER REVIEW]**
- Treating OCF > NI as an affirmative mitigant subtracted weight exactly where the
  order shows cash flow was propped by advances (¶8-9); a neutral reading of OCF
  strength, on a deck that cannot see cash-flow composition, seems the correct
  posture. **[OWNER REVIEW]**
- CL6's anchoring to the corrupted allowance tag rather than the available
  AccruedLiabilitiesCurrent series left the reserve axis untested; checklist-design
  limitation vs model retrieval choice affects DATA-vs-MODEL ownership. **[OWNER REVIEW]**
- Materiality: Nordic overstatements ran 3-7% of consolidated operating income per
  FY2010 quarter (¶90), Australia >5% of pretax in Q1FY2009 (¶85) — near the edge of
  consolidated-ratio visibility, bearing on how much score the surfaced divergences
  could carry. **[OWNER REVIEW]**

## 8. AUDIT TRANSLATION

Procedures the (sub-threshold) signals would motivate — procedures, not conclusions:

- POC model testing on long-term contracts: agree assumptions to the enforceable
  contract and executed (not proposed) amendments; recompute inception-to-date margin
  adjustments (SOP 81-1 / ASC 605-35 era); WIP / contract-asset recoverability and
  impairment testing where milestones lag plan.
- Reserve roll-forwards for accrual accounts (bonus, restructuring, labor): vouch
  build-ups to obligating events; test period-end releases against support.
- Prepaid/other-asset support testing (ASC 340-10-5-4); journal-entry testing for
  reversals of previously expensed costs at foreign subsidiaries; legal-letter
  procedures for side agreements linked to client settlements.
- Cash-flow composition analysis: customer advances within operating cash flow, terms
  (interest, refundability), disclosure adequacy.

## 9. FINANCIAL STATEMENT IMPACT

From the sealed order text — the order quantifies impacts, but restated line-item
amounts are **not determinable** from the sealed sources read (post-cutoff 10-Q/A
filings of 2011-2012 appear in the sealed chronology; contents not read):

- "CSC was required to restate its financial statements" for FY2010-FY2012 (¶99,
  lines 1016-1018).
- Consolidated pretax income overstated "by over 5%" in Q1FY2009 (Australia, ¶85).
- Consolidated operating income overstated 5% / 3% / 4% / 7% in Q1-Q4FY2010 (Nordic,
  ¶90, lines 913-914); items: $9M (¶92), $900K (¶93), over $4M (¶95), $8.2M bench
  labor (¶97), over $30M unsupported prepaid assets (fn 32) — income and assets
  overstated, expenses understated.
- NHS leg (post-period remediation): CSC "wrote down approximately $1.5 billion in NHS
  contract assets from its balance sheet" in Q3FY2012 (¶68, lines 707-708) — contract
  assets previously overstated.

---
*Entry status: drafted (sections 7–9 pending owner finalization).*
*채점: Claude 보조 + 인간 최종 확정. 교육·정보 목적, 투자 자문 아님.*
