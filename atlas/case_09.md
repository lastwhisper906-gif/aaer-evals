# atlas/case_09.md — Iconix Brand Group, Inc. (ICON) — wave-1 treatment T16

Authored by Claude Code, pending human audit (D15). Analytical document under D106 ② — not a scored output. 본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).

## 1. CASE HEADER

| field | value |
|---|---|
| Case ID (anonymized frame) | case_09 (scoring ID T16) |
| Cohort | wave-1 |
| Outcome class | TP (main frame, flag at score ≥50; perturbed frame also ≥50) |
| Ground-truth tier | AAER-confirmed (AAER-4105 / Securities Act Rel. 33-10730, respondent ex-CFO Clamen only — issuer charged separately, SEC v. Iconix Brand Group, 19-CV-11150 / LR-24682; "동일 사건 기준" 귀속 per candidates notes) |
| Frozen score | score 65 (`runs/main/case_09.json`, run `original-case_09-r1`); perturbed frame score 55 (`runs/perturbed/case_09.json`, run `perturbed-case_09-r1`) |
| Grade record | `scoring/grades/main/case_09.json` and `scoring/grades/perturbed/case_09.json` (human_finalized: true, RP-09 Stage 0, commit 986a893, 2026-07-07) |

Company: Iconix Brand Group, Inc., CIK 0000857737, cutoff 2015-08-09
(`data/candidates/candidates.json` T16; `data/evaluatee/cases.json` case_09).
Perturbation delta: score 65 → 55 (−10). Per D8 the delta measures memorization
contribution — not a robustness pass/fail; TP frame-stable at threshold 50.

## 2. ACTUAL EVENT

Three sealed enforcement documents (manifest-pinned,
`data/manifests/aaer_data_manifest.json`):

- **SEC v. Iconix Brand Group, Inc., 19-CV-11150 (S.D.N.Y., filed 2019-12-05)**
  (`~/aaer-data/ICON/comp-pr2019-251-iconix.pdf.txt`): an "intentional fraud
  perpetrated by Iconix Brand Group, Inc. ... to recognize false revenue and
  manipulate" reported earnings in 2014 (¶1) — a scheme to sell "intellectual
  property rights to Company 1 at artificially inflated purchase prices" with a
  promised give-back, which "enabled Iconix to fraudulently recognize $11
  million in false revenue in 2014" (¶2). SEA II: "Iconix recognized a second
  quarter gain of $13.6 million on SEA II" of which "recognition of $5 million
  of the $13.6 million" was improper (¶45); SEA III: Iconix "recorded an $18.7
  million gain" (¶58); "Six million of this gain was improperly recognized
  under GAAP" (¶59).
  Plus negligence-based fraud 2013–Q3 2015: failure to write off two licensees'
  uncollectible receivables via transactions that "misleadingly concealed the
  licensees' distressed financial" condition — Iconix "overstated net income
  derived from Company 2 by over $5 million" and "from Company 3 by over $9
  million" (¶3); and failure to "recognize an impairment loss on intellectual
  property assets associated with three brands" despite clear indicators,
  including "using royalty revenue projections to calculate" unreasonable fair
  values (¶4).
- **Order, In the Matter of Warren Clamen, CPA, Securities Act Rel. 33-10730 /
  AAER-4105 (2019-12-05)** (`~/aaer-data/ICON/33-10730.pdf.txt`): CFO-level
  findings on the receivables/impairment legs — acquisition prices "used to
  funnel past-due and" future royalties back to Iconix (¶1); Brand 1/Brand 2
  values "overstated on Iconix's year-end balance sheet in its 2013 Form 10-K"
  by $132.7–142.7M and "$106.7 million to $116.7 million", totaling
  "approximately $239.4 million to $259.4 million" (¶4).
- **LR-24682 (2019-12-05)** (`~/aaer-data/ICON/lr-24682.html.txt`): Iconix
  charged with "recognizing false revenue and manipulating its reported
  earnings in 2014", "entering into transactions to conceal distressed finances
  at two licensees", and "failing to recognize over $239 million in impairment
  charges for three brands over a multi-year period"; agreed to "pay a $5.5
  million penalty".

GAAP topics: improper revenue/gain recognition on round-trip JV asset sales
lacking economic substance; ASC 310 (receivables impairment, complaint ¶97);
ASC 350 (intangibles impairment testing, complaint ¶¶121-122 area).
Registered summary (`data/candidates/candidates.json` T16 `scheme_summary`):
fabricated licensing revenue in 2014 to beat consensus plus failure to timely
recognize $239M+ brand impairment while propping up distressed licensees;
`scheme_type` revenue_recognition + asset_overstatement + related_party;
manipulation period 2013 to 2015-09-30; first revelation 2015-08-10 (Q2-2015
report disclosing SEC comment-letter review of the JV-gain accounting).

## 3. SIGNALS AVAILABLE PRE-CUTOFF

Cutoff 2015-08-09. Sealed basis: `data/evaluatee/cases.json` case_09 (identity
metadata only — payload reaches the model as XBRL series plus filing
chronology per the frozen output's CL8 note), the frozen outputs' quoted deck
values, `~/aaer-data/ICON/xbrl/CIK0000857737.json`, and
`~/aaer-data/ICON/edgar/` (submissions metadata). Filing narrative text (MD&A,
JV footnotes) is not among the sealed sources — filing-text quotes:
**insufficient sealed evidence**. Data-point signals, all filed ≤ 2015-08-09
(values spot-verified in the sealed company facts at value+date+accession):

- **AR vs revenue divergence**: AccountsReceivableNetCurrent $90.777M
  (2013-12-31, accn 0001193125-15-071602) → $118.774M (2014-12-31, accn
  0001193125-15-071602) vs Revenues $432.626M (FY2013) → $461.243M (FY2014,
  accn 0001193125-15-071602); AR $124.591M at 2015-03-31 while Q1-2015 revenue
  fell to $95.387M from $116.138M (accn 0001193125-15-179670). The order ties
  the growing receivable to licensees "not current on their royalty
  obligations" whose write-off Iconix "failed to write-off" or reserve (¶2).
- **Deferred revenue declining while AR balloons**: DeferredRevenueCurrent
  $29.126M (2013-12-31, accn 0001193125-14-072954) → $22.470M (2015-03-31,
  accn 0001193125-15-179670).
- **The inflated quarters themselves were in the deck**: Revenues $118.943M
  (Q2 2014, accn 0001193125-14-298324) and $113.750M (Q3 2014, accn
  0001193125-14-403492) — the very figures the complaint alleges carried $5M
  (¶46-47: "Record Q2 revenue of $118.9" million) and $6M (¶62-64: quarterly
  revenue "inflated by over 5%") of false revenue. The round-trip nature was
  not observable from the numbers.
- **Q1-2015 margin anomaly**: NetIncomeLoss $62.840M on Revenues $95.387M
  (accn 0001193125-15-179670) — the frozen output computes ~66% net margin on
  an ~18% YoY revenue decline.
- **Filing chronology**: 10-K/A amendments every year 2011–2015 and dense SEC
  CORRESP/UPLOAD correspondence through 2015-07-14 and 2015-07-20 (frozen
  output CL7) — the comment-letter process whose 2015-08-10 disclosure is the
  registered revelation event.
- **Soft-asset weight**: IntangibleAssetsNetExcludingGoodwill $2,024.541M
  (2014-12-31) → $2,182.708M (2015-03-31); OtherAssetsNoncurrent $24.082M
  (2012-12-31) → $63.334M (2014-12-31) (accn 0001193125-15-179670) — carrying
  values including the brands the order found overstated at 2013 year-end.

This section describes the information set — it does not re-score the case.

## 4. WHAT THE LLM CAUGHT

Frozen output `runs/main/case_09.json`: `misstatement_probability`: 65 (legacy
v1 key — an uncalibrated ordinal score; see specs/RISK_SCORE_SEMANTICS.md) =
score 65, risk_tier "elevated"; CL1/CL2/CL3/CL5/CL6/CL7 flagged; three
mechanism hypotheses. Perturbed frame: score 55, "elevated", three hypotheses
on rescaled values. Model quotes are verbatim from the frozen outputs;
enforcement quotes grep-verified in the cited sealed texts.

| model claim (verbatim) | enforcement/restatement reference | match quality |
|---|---|---|
| "Acceleration/front-loading of licensing revenue recognition (e.g., recognizing minimum guaranteed royalties or upfront license fees before cash collection or before the earnings process is complete)" (main, hypotheses[0], top-ranked) | Complaint ¶2: scheme "enabled Iconix to fraudulently recognize $11 million in false revenue in 2014" — fabrication via round-trip JV sales, not premature recognition of real royalties | right account wrong mechanism |
| "Possible use of non-operating gains or deferral of expense recognition to sustain earnings/margins as core licensing revenue decelerated/declined" (main, hypotheses[1]) | Complaint ¶45/¶58-59: improper portions of the $13.6M SEA II and $18.7M SEA III gains recognized to beat consensus — but the model anchors this to Q1-2015 margins, not the 2014 JV gains | right direction only |
| "Capitalization of costs (e.g., deferred transaction/licensing costs, capitalized items) onto the balance sheet at a pace far exceeding revenue growth, potentially deferring expense recognition" (main, hypotheses[2]) | Order 33-10730 ¶4: brand values "overstated on Iconix's year-end balance sheet in its 2013 Form 10-K" by "approximately $239.4 million to $259.4 million" — non-impairment, not cost capitalization | right account wrong mechanism |
| "Potential premature/aggressive revenue recognition or extended customer payment terms causing receivables to build up faster than sales growth ... or bad-debt allowances are insufficient" (perturbed, hypotheses[0], top-ranked) | Complaint ¶2 (false 2014 revenue) and ¶3 / order ¶2 ("failed to write-off the" uncollectible receivables, "create an allowance for bad" debt not done) — account, direction, and the insufficient-allowance clause land; fabrication specifics absent | right account wrong mechanism |
| "if underlying acquired royalty/IP cash flows underperform, impairment charges may be delayed or understated, overstating carrying value of intangibles and net income" (perturbed, hypotheses[1]) | Complaint ¶4: unreasonable failure to "recognize an impairment loss on intellectual property assets associated with three brands"; order ¶4 quantifies $239.4–259.4M | exact mechanism |

Main-frame grades: DIM1=1 (score 65 in the 50–69 band), DIM2=1 ("correct
account area only" — licensing revenue, overstated; "treatment type (premature
recognition of real royalties) does not substantially match fabrication"),
DIM3 active vs mixed key = 1, DIM4=3. Perturbed frame: DIM1=1, DIM2=2 ("treatment
type (improper revenue recognition inflating 2014 results) substantially
match" the enforcement description; no case-specific key fact named), DIM3=2
(key scored active(gains)-우세), DIM4=3. Both grade
rationales note the JV buy-in overpayment gains, the $239M impairment
non-recognition, and the distressed-licensee prop-up transactions as the
uncaptured case-specific facts.

## 5. WHAT THE LLM MISSED

From the §3 sealed information set, by truth leg:

- **JV round-trip gain inflation (the intentional-fraud core)** — not surfaced
  in either frame. Its footprint (inflated purchase prices with promised
  give-backs, complaint ¶42-45, ¶56-59) lived in deal terms and JV footnote
  narrative, not in any numeric series in the deck; the inflated Q2/Q3 2014
  revenue figures were present only as ordinary-looking data points (§3).
- **Uncollectible licensee receivables / allowance failure** — the main frame
  flagged the AR-vs-revenue divergence (CL1) but framed it as revenue
  acceleration, never as collectibility failure; the perturbed frame's
  "bad-debt allowances are insufficient" clause reaches the conduct verbally.
  CL8 in both frames records that no allowance-for-doubtful-accounts series
  was provided.
- **Brand impairment non-recognition** — missed in the main frame (hypotheses[2]
  frames soft-asset growth as cost capitalization); captured in the perturbed
  frame's hypotheses[1], though ranked second and conditional.
- **Related-party/prop-up transactions** (order ¶2: interests purchased from
  licensee owners to "funnel past-due and" future royalties back) — surfaced
  in neither frame; no series in the deck isolates these purchases.
- Earliness: `analysis/error_analysis.md` §4 row "ICON | 2015-05 10-Q | 1q /
  1q | d2=1" — decisive evidence completed one quarter before revelation.

## 6. ERROR TAXONOMY

Outcome is TP at threshold 50 in both frames; the recorded error is on the
mechanism dimension. `scoring/error_taxonomy.md` buckets, atlas vocabulary:

- **Interpretation** (primary): `analysis/error_analysis.md` §2 row: "ICON |
  65 | 1 | 매출 축 일치, 특이 기제(JV buy-in 이익 인식)는 미포착" — revenue
  axis matched, the idiosyncratic JV buy-in gain mechanism uncaptured.
- **Retrieval/data boundary**: under R1, the round-trip's give-back terms and
  the allowance series were absent from the provided data (§3, §5) — the
  mechanism miss has a DATA-side leg whose attribution is an owner call (§7).
  Quoted deck values spot-verified against the sealed company facts (§3); no
  computation errors found.
- **Label-noise**: none as to conduct — settled federal-court action and
  settled administrative order. Attribution nuance per candidates notes:
  AAER-4105 prints on the Clamen-only order; the issuer was a federal-court
  defendant without its own AAER number ("동일 사건 기준" 귀속, GP-4b).
- **Suspected-memorization — the two sealed draws DISAGREE (L-5)**: Draw 1
  (`scoring/probe_results/recognition/case_09.json`): company_guess "Iconix
  Brand Group, Inc.", confidence "low". Draw 2
  (`analysis/name_probe_results.json`, row case_09): guess "Cornerstone
  Therapeutics Inc.", confidence "medium", recognized: false — the frozen
  verdict rule scores case_09 as not recognized. memorization_suspect_condition2:
  false in both grade records; both rationales find reasoning anchored on
  provided data content with no post-cutoff enforcement facts. Frame delta
  −10 (score 65 → 55) is the D8 memorization-contribution measurement.

## 7. CPA JUDGMENT — human_finalized: false

Draft, unaudited work product until owner sign-off (PROJECT.md §7).

- **TP on the right axis, wrong treatment**: both frames led with overstated
  licensing revenue/AR — the correct account area and direction — but read the
  divergence as premature recognition of real royalties rather than fabricated
  round-trip gains plus uncollected royalties left on the books. On a
  numeric-only deck those two mechanisms are near-observationally equivalent;
  proposed reading: creditable account-level detection, mechanism
  identification limited by the information set. **[OWNER REVIEW]**
- **Main hypotheses[1] vs the JV-gains axis**: "use of non-operating gains ...
  to sustain earnings" is generically the gains mechanism; graded not
  top-ranked and anchored to Q1-2015 rather than the 2014 SEA gains. The
  "right direction only" cell above could arguably be upgraded — owner call.
  **[OWNER REVIEW]**
- **Grade asymmetry between frames**: the same account-level story earned
  DIM2=1 (main) and DIM2=2 (perturbed) on rationales that draw the
  premature-vs-fabrication line differently; a boundary-consistency check
  across the two records is warranted. **[OWNER REVIEW]**
- **Deferred-revenue reading**: the model treats the shrinking
  DeferredRevenueCurrent as corroborating pull-forward; the sealed enforcement
  texts do not address deferred revenue — no enforcement counterpart.
  **[OWNER REVIEW]**
- **Perturbed impairment hypothesis**: hypotheses[1] states the ASC 350
  mechanism the order quantifies, from carrying-value-vs-revenue scale alone;
  whether second-rank coverage merits atlas credit as a "catch" is a
  vocabulary call (§4 table says exact mechanism, not top-ranked).
  **[OWNER REVIEW]**

## 8. AUDIT TRANSLATION

Procedures the §3 signals would motivate (procedures, not conclusions):

- Royalty receivable collectibility testing under ASC 310: aging by licensee,
  confirmation of past-due balances, licensee financial-health correlation
  with recorded allowances; write-off policy back-testing.
- Related-party and round-trip procedures: for asset sales and JV buy-ins near
  quarter-end, examine deal files for side agreements or promised give-backs;
  trace consideration to cash and test economic substance of purchase-price
  components; vouch payments flowing back to counterparties.
- Gain-recognition testing on IP contributions to JVs: recompute gains against
  book value and third-party evidence of fair value; scrutinize purchase-price
  increases late in negotiation.
- ASC 350 impairment testing: independent evaluation of triggering events
  (licensee loss/insolvency, receding royalties); challenge royalty revenue
  projections against historical performance and license terms in force.
- Comment-letter and 10-K/A follow-through: read the CORRESP/UPLOAD stream for
  unresolved accounting issues (chronology signals in the deck, CL7).

## 9. FINANCIAL STATEMENT IMPACT

From the enforcement text actually read: revenue and net income overstated.
Complaint: FY2014 false revenue $11M (¶2); Q2 2014 — "Iconix's reported net
income was materially misstated by over 9%" (¶48) and reported revenue
overstated 4.4% (¶47); Q3 2014 — "Iconix's reported revenue for the quarter
was inflated by over 5%" (¶64) and net income "overstated net income for the
third quarter by" over 12% (¶65). Order 33-10730: interim 2013 "net income
after taxes by 16% and" 14% overstated (Q2/Q3 2013), and "Iconix's 2013 Form
10-K materially overstated net income by 7%" (¶3); Brand 1/Brand 2 carrying
values overstated by a total of "approximately $239.4 million to $259.4
million" at 2013 year-end (¶4). LR-24682: "Iconix overstated net income by
hundreds of millions of dollars between 2013 and the third quarter of 2015".
Order n.12: "In March 2016, Iconix restated its historical accounting
treatment for several overseas joint ventures" to consolidate them. Full
restated per-line-item, per-period amounts: not determinable — the sealed
documents do not tabulate a restatement, and no restatement filing text is
among the sealed sources read.

---
*Entry status: drafted (sections 7–9 pending owner finalization).*
*채점: Claude 보조 + 인간 최종 확정. 교육·정보 목적, 투자 자문 아님.*
