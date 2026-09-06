# atlas/case_48.md — LivePerson, Inc. (LPSN) — wave-2 control W09 (FALSE POSITIVE)

Authored by Claude Code, pending human audit (D15). Analytical document under D106 ② — not a scored output. 본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).

## 1. CASE HEADER

| field | value |
|---|---|
| Case ID (anonymized frame) | case_48 (scoring ID W09) |
| Cohort | wave-2 (23-control arm) |
| Outcome class | FP (main frame, flag at score ≥50) |
| Ground-truth tier | control (no adverse label) |
| Frozen score | score 55 (`runs/wave2/scores/case_48.json`, run `original-case_48-r1`, risk_tier "elevated") |
| Grade record | `scoring/grades_wave2/case_48.json` (human_finalized: true, finalized 2026-07-09 via RP-13 workbench; dim1=0 "control rubric says p>=50 -> 0", dim2/dim3 null (control), dim4=3, memorization_suspect_condition2=false) |

Company: LivePerson, Inc. (LPSN), CIK 0001102993, SIC 7372 (prepackaged
software), cutoff 2016-03-06 — copied from matched treatment T22 (TNGO) per
the same-snapshot convention (`data/candidates/candidates_wave2.json` W09:
group "control", matched_treatment "T22", scheme fields all null). Identity
frame: the deck carries the registrant's real EDGAR name — case_48 is not
among the fictional-name frames in `data/evaluatee/fict_names_wave2.json`
(its `names` block covers only wave-2 treatments). **This entry documents a
model error on a control company, not a company problem.**

## 2. ACTUAL EVENT

**No adverse event — control** (cleanliness basis per original selection
criteria; see `docs/CONTROL_CRITERIA_v2.md`). Selection record
`runs/wave2/control_group_v2.json` (criteria = CONTROL_CRITERIA_v2.md,
criteria_sha256 f6cc67cb…, per its `_meta`): selected for T22 at rank 1 —
sic_pool "7372", sic_tier 0, rev_pit 209,931,000 (size_dist 0.0121,
size_basis "revenue", size_flags empty), assets_pit 237,236,000, fye 1231
(fye_month_dist 0). Cleanliness under v2 = the E4-v2 machine name-screen
against the AAER respondents index (current name + formerNames) plus the
owner external web screen (§6-v2) — a **non-enforcement** label, not a
purity claim (`analysis/error_analysis_wave2_holdout.md` header: 대조군
라벨="비집행"(무결 아님)). Sealed submissions metadata
(`~/aaer-data/LPSN/edgar/CIK0001102993.json` and `-submissions-001.json`,
jointly spanning filing dates 2000-01-28 → 2026-07-02) contains **zero 8-K
filings with Item 4.02** in the registrant's entire history, and no
enforcement or restatement document is sealed for this registrant.
GP-8-direction caveat: an error in the control label would lower measured
specificity, so the FP finding is conservative on that axis.

## 3. SIGNALS AVAILABLE PRE-CUTOFF

Cutoff 2016-03-06. Sealed basis: the frozen output's quoted deck values,
`~/aaer-data/LPSN/xbrl/CIK0001102993.json` (companyfacts), and
`~/aaer-data/LPSN/edgar/` (submissions metadata; manifest-pinned,
`data/manifests/aaer_data_manifest.json`). Filing narrative text (MD&A,
amendment explanatory notes, comment-letter content) is not among the
sealed sources — filing-text quotes: **insufficient sealed evidence**. The
data points the model reacted to, all filed ≤ cutoff and verified genuine
(§4):

- AllowanceForDoubtfulAccountsReceivableCurrent flat at $708K for seven
  consecutive quarter-ends 2012-03-31 → 2013-09-30 while
  AccountsReceivableNetCurrent grew $17.780M → $32.726M; then $1.165M at
  2013-12-31. The same FY2013 10-K (accn 0001445305-14-001030) carries
  ProvisionForDoubtfulAccounts = $457K (FY2013; FY2012 was $20K), and the
  allowance falls back to $926K (2014-03-31) and $809K (2014-06-30).
- NI vs CFO: NetIncomeLoss $6.355M / −$3.499M / −$7.348M (FY2012/13/14) vs
  NetCashProvidedByUsedInOperatingActivities $28.009M / $16.958M / $15.673M
  (FY2014 10-K, accn 0001628280-15-001726). Sealed non-cash charges in the
  same facts: FY2014 Depreciation $9.071M + ShareBasedCompensation $12.306M
  + AmortizationOfIntangibleAssets $1.621M = $22.998M vs the $23.021M gap.
- Goodwill $24.090M (2011-12-31) → $32.645M (2012-12-31) → $32.724M
  (2013-12-31) → $35.783M (2014-06-30) → $80.848M (2014-12-31); intangibles
  $14.020M (2014-09-30) → $32.620M (2014-12-31). The same FY2014 10-K
  carries the concurrent acquisition footprint:
  StockIssuedDuringPeriodValueAcquisitions $20.123M,
  BusinessCombinationAcquisitionRelatedCosts $1.400M, and pro-forma FY2014
  revenue $230.894M / pro-forma NI −$6.467M.
- PropertyPlantAndEquipmentGross $34.538M (2011-12-31) → $76.053M
  (2015-09-30).
- Filing chronology (sealed submissions): UPLOAD 2015-11-04, CORRESP
  2015-11-10 / 2015-12-02 / 2015-12-16 / 2016-01-08, UPLOAD 2015-12-10,
  10-K/A filed 2016-01-22 (accn 0001102993-16-000008, reportDate 2014-12-31
  — an amendment of the FY2014 10-K), then a final UPLOAD 2016-01-26 (not
  cited by the model). Historical items: NT 10-Q 2004-08-16, 10-K/A
  2005-05-02, NT 10-K 2007-03-19, 10-Q/A 2007-08-09.

This section describes the information set — it does not re-score the case.

## 4. WHAT THE LLM CAUGHT (what the model asserted, and on what evidence)

Frozen output `runs/wave2/scores/case_48.json`: `misstatement_probability`:
55 (legacy v1 key — an uncalibrated ordinal score; see
specs/RISK_SCORE_SEMANTICS.md) = score 55, risk_tier "elevated". CL2, CL3,
CL6, CL7 flagged (CL3/CL7 confidence "high"); CL1/CL4/CL5/CL8 no_flag. Top
hypothesis: "Under-provisioning of allowance for doubtful accounts while
receivables grew substantially … corrected via a lump-sum adjustment at
year-end 2013". Every cited figure was grep-verified against the sealed
companyfacts/submissions:

| model claim (verbatim) | evidence genuine? (sealed record) | correspondence |
|---|---|---|
| "AllowanceForDoubtfulAccountsReceivableCurrent=708000 (2012-03-31) … (2013-09-30) — flat for 7 consecutive quarter-ends while AccountsReceivableNetCurrent grew from 17780000 … to 32726000 … ~84% increase" then "1165000 (2013-12-31) — a sudden 65% jump" (CL6/hyp 1) | genuine — all eight allowance values and both AR endpoints in sealed companyfacts at the cited dates; 1,165/708 and 32,726/17,780 recompute. Same-source context: the jump equals the FY2013 ProvisionForDoubtfulAccounts of $457K disclosed in the cited 10-K, and allowance/net-AR coverage moved 3.98% (2012-03-31) → 2.16% (2013-09-30) → 3.95% (2013-12-31) — the year-end increase restores the earlier coverage ratio | n/a — control |
| "NetIncomeLoss=-7348000 (FY2014) vs NetCashProvidedByUsedInOperatingActivities=15673000 (FY2014)" (and FY2012/FY2013 pairs, CL3 confidence "high") | genuine — all six values at cited dates/accessions. Sealed same-accession non-cash charges (Depreciation + SBC + intangible amortization = $22.998M FY2014) account for the $23.021M gap; the grade record itself notes "treating positive OCF > negative NI as an overstatement flag is the atypical direction" | n/a — control |
| "Goodwill=35783000 (2014-06-30) jumping to Goodwill=80848000 (2014-12-31) — +126% in second half of 2014 alone; IntangibleAssetsNetExcludingGoodwill=14020000 … to 32620000 … +133%" (CL2) | genuine — all four values in sealed facts. The model's own top_signals[3] concedes the jumps are "from acquisitions", and the cited FY2014 10-K carries the ASC 805 footprint (stock issued for acquisitions $20.123M, acquisition-related costs $1.400M, pro-forma revenue/NI) | n/a — control |
| "UPLOAD filing_date 2015-11-04; CORRESP … 2016-01-08; followed by 10-K/A filing_date 2016-01-22" read as "a common precursor to identification of misstatements" (CL7/hyp 2) | all seven dates genuine in sealed submissions. The inference is not supported by the sealed record: the /A amends the FY2014 10-K (reportDate 2014-12-31); **zero XBRL facts in sealed companyfacts are attributed to the /A accession** (no numeric revision footprint); the sequence ends with UPLOAD 2016-01-26 and the FY2015 10-K follows on regular schedule 2016-03-15 (post-cutoff sealed metadata); zero Item 4.02 8-Ks in history | n/a — control |
| "NT 10-Q filing_date 2004-08-16; NT 10-K filing_date 2007-03-19; 10-K/A filing_date 2005-05-02; 10-Q/A filing_date 2007-08-09" (CL7) | genuine — all four in sealed submissions; all 8-11 years before cutoff and outside the 2012-2015 window of the quantitative flags | n/a — control |

The grade record concurs on evidence quality: "Evidence is specific and
verifiable against provided data … the analysis coherently combines
multi-year, multi-point series -> 3" (dim4=3), naming the flaw quoted above.

## 5. WHAT THE LLM MISSED

n/a — control: there is no adverse mechanism to miss. Notably the model
supplied its own benign readings on four axes — CL1 (AR tracking or lagging
revenue), CL4 (margins stable), CL5 (quarterly earnings volatile with sign
changes, i.e., not smoothed), CL8 (coverage adequate) — and top_signals[3]
concedes the goodwill jump is acquisition-driven, yet it still promoted the
CL6/CL3/CL7 composite to score 55 / "elevated".

## 6. ERROR TAXONOMY

- **Interpretation (primary)** — registered classification
  `analysis/error_analysis_wave2_holdout.md` §1, LPSN row: "(ii-a)" —
  "'allowance flat at $708,000 for seven quarter-ends ... AR +84%, then 65%
  catch-up' + SEC comment letters. 실재하나 양성(코멘트레터≠부정,
  allowance catch-up 흔함). (ii-a)". First-pass disposition
  `review_packets/RP-13_grading_workbench.md` case_48: "오탐이나 채점 d1=0
  정확 — trust boundary 데이터" (finalize proposed). MECE R1 corroboration
  that the signal exists in the data (so the failure is interpretive, not
  retrieval): the deterministic chronology baseline `analysis/results_b3.json`
  W09 W4 also registers b_ka=1 (score 1) for the in-window 10-K/A.
- **Computation** — none found: all quoted values verified at
  value+date+accession level (§4); "65%", "~84%", and the 18.1% revenue
  growth recompute from sealed facts.
- **Label-noise** — none within the design: control label per §2 (v2
  machine name-screen + owner web screen); zero Item 4.02 in the sealed
  filing history; non-enforcement ≠ pristine, direction conservative.
- **Suspected-memorization** — name recognition without event knowledge,
  mixed across draws. `scoring/probe_results_wave2/recognition/case_48.json`:
  guess "LivePerson, Inc. (ticker: LPSN)", confidence "medium" — the frozen
  frame is name-identifiable on that draw;
  `scoring/probe_results_v2ds_wave2/recognition/case_48.json`: "unknown"/
  "low"; `scoring/probe_results_wave2/verbatim/case_48.json`: known: false,
  all recall fields null; `analysis/outcome_recognition_results.json` W09:
  name_id_recognized_frozen true, **knows_event false**, confidence "low" —
  one sealed draw each; verdicts vary across draws (L-5). As a control
  there is no adverse outcome to recall; grade record:
  memorization_suspect_condition2=false ("no post-cutoff facts"; the 10-K/A
  2016-01-22 is in the provided chronology, pre-cutoff). Draw stability
  (`analysis/draw_k3_results.json` case_48): draws 55, 48, 62 (median3 55,
  band 48-62), flag_draw1 and flag_median3 both true — unlike the wave-1
  Ryder FP, not a max-of-draws artifact.

## 7. CPA JUDGMENT — human_finalized: false

Draft, unaudited work product until owner sign-off (PROJECT.md §7). Why
each flagged pattern is explainable in benign terms:

- **The allowance pattern is small-dollar estimation, not a
  misstatement-scale lever.** The entire "65% catch-up" is a $457K FY2013
  provision (~0.26% of FY2013 revenue of $177.805M, ~13% of the FY2013 net
  loss), disclosed in the ordinary rollforward of the same 10-K the model
  cited; coverage on net AR ended FY2013 at 3.95%, essentially back at the
  2012-03-31 level (3.98%), and the allowance then declined again in 2014
  ($926K, $809K) — routine re-estimation dynamics. A balance this small
  cannot move NI materially in either direction. **[OWNER REVIEW]**
- **The NI-CFO gap is the ordinary shape of a SaaS company expensing
  non-cash items.** Depreciation + share-based compensation + intangible
  amortization tie to the FY2014 gap within $23K in the sealed facts. The
  direction the model flagged (positive CFO above negative NI) is the
  opposite of the classic overstatement signature — the grade record itself
  calls this "the atypical direction". **[OWNER REVIEW]**
- **The goodwill/intangibles jump is the ASC 805 footprint of Q4-2014
  acquisitions**, evidenced in the very accession the model cited (stock
  consideration $20.123M, acquisition-related costs $1.400M, pro-forma
  disclosures). The model's own top_signals text concedes "from
  acquisitions … raising purchase-accounting allocation risk", then weights
  the concession as an adverse signal anyway. **[OWNER REVIEW]**
- **Comment-letter correspondence plus a 10-K/A is not, on this sealed
  record, a restatement footprint.** The CORRESP/UPLOAD content is not
  sealed (metadata only), the /A left no numeric revision trace in sealed
  companyfacts, no Item 4.02 exists in history, and the FY2015 10-K
  followed on schedule. Reading the cycle as "a common precursor to
  identification of misstatements" (hyp 2) exceeds the metadata — the same
  CL7 over-reading axis as the wave-1 Ryder FP (`atlas/case_10.md` §7).
  **[OWNER REVIEW]**
- **Net shape of the error**: genuine, individually benign-explainable
  signals (immaterial allowance drift + structural non-cash NI/CFO gap +
  M&A step-up + review-cycle metadata) compounded into "elevated" at score
  55, five points over the flag threshold — consistent with the wave-2
  finding that FPs are grounded over-reading, not fabrication
  (error_analysis §1). **[OWNER REVIEW]**

## 8. AUDIT TRANSLATION

Procedures that would have cleared the flag (procedures, not conclusions):

- Obtain the allowance rollforward and AR aging; recompute coverage on
  gross receivables; vouch the FY2013 $457K provision and 2014 write-off
  activity; size the balance against the statements as a whole.
- Reconcile the NI-CFO gap to the non-cash add-backs (depreciation, SBC, amortization, deferred taxes).
- Vouch the H2-2014 goodwill and intangible additions to the
  business-combination disclosures (ASC 805 purchase-price allocations),
  including the $20.123M stock consideration and pro-forma disclosures.
- Read the 10-K/A (2016-01-22) and diff against the original FY2014 10-K
  (2015-03-12); identify amended items; confirm absence of any ASC 250
  restatement or Item 4.02 disclosure.
- Obtain the SEC comment letters (UPLOAD) and responses (CORRESP); confirm
  the review closed without restatement.
- Search the 8-K record for Item 4.02 and auditor-change items (sealed
  metadata already answers: zero 4.02 in history).

## 9. FINANCIAL STATEMENT IMPACT

n/a — no restatement (control). No restated line items exist; the sealed
record contains no Item 4.02 8-K, no enforcement or restatement document
for this registrant, and no XBRL fact attributed to the 2016-01-22 10-K/A
accession — i.e., no numeric revision footprint in the sealed companyfacts
(§2, §4).

---
*Entry status: drafted (sections 7–9 pending owner finalization).*
*채점: Claude 보조 + 인간 최종 확정. 교육·정보 목적, 투자 자문 아님.*
