# atlas/case_60.md — MiMedx Group, Inc. (MDXG) — wave-2 treatment T26

Authored by Claude Code, pending human audit (D15). Analytical document under D106 ② — not a scored output. 본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).

## 1. CASE HEADER

| field | value |
|---|---|
| Case ID (anonymized frame) | case_60 (scoring ID T26) |
| Cohort | wave-2 |
| Outcome class | TP (main frame, flag at score ≥50) |
| Ground-truth tier | AAER-confirmed (wave-2 treatment cohort; sealed enforcement basis LR-24678, SEC v. MiMedx Group, Inc., Parker H. Petit, William C. Taylor, and Michael J. Senken, 1:19-cv-10927 (S.D.N.Y., filed Nov. 26, 2019)) |
| Frozen score | score 65 (`runs/wave2/scores/case_60.json`, run `original-case_60-r1`, risk_tier "elevated") |
| Grade record | `scoring/grades_wave2/case_60.json` (human_finalized: true, finalized 2026-07-09 via RP-13 workbench; dim1=1, dim2=2, dim3=2 "active", dim4=3) |

Company: MiMedx Group, Inc., CIK 0001376339, cutoff 2016-12-14
(`data/candidates/candidates_wave2.json` T26; `data/evaluatee/cases_wave2.json` case_60).
`analysis/error_analysis_wave2_holdout.md` does not discuss this case individually.

## 2. ACTUAL EVENT

SEC v. MiMedx Group, Inc. et al., 1:19-cv-10927 (S.D.N.Y.); Litigation Release No. 24678
(Nov. 26, 2019). Sealed local text: `~/aaer-data/MDXG/comp24678.pdf.txt` (complaint) and
`~/aaer-data/MDXG/lr-24678.html.txt` (manifest-pinned, `data/manifests/aaer_data_manifest.json`).

Per the complaint, from 2013 through Q3 2017 MiMedx "engaged in a wide-ranging fraud designed
to artificially inflate the company's reported revenue" (¶1, line 50) involving "five of its
largest distributors". From Q1 2013 MiMedx "improperly recognized revenue at the time it
shipped products to Distributor E, its largest distributor" (¶2, line 61) under a secret side
arrangement "allowing Distributor E to pay MiMedx only when it resold the products, and
crediting Distributor E for lost, damaged, or returned products" (¶2, line 65). As Distributor E
sales declined, in the last three quarters of 2015 Petit and Taylor added concealed side
arrangements with Distributors A-D, causing improper revenue "representing at least 6% to 14%
of its reported revenue each quarter" (¶3, line 73). To cover up, the executives "repeatedly
lied to and withheld critical information from" the Audit Committee, outside auditors, and
outside counsel (¶8, line 118). Charges: Securities Act §17(a), Exchange Act §10(b)/Rule 10b-5,
§13(a), §13(b)(2) and related rules; the company settled for a "$1.5 million penalty" with
litigation continuing against the three executives (LR-24678, lines 1089-1091 — individual
allegations contested as of that release).

Registered summary (`data/candidates/candidates_wave2.json`, T26 `scheme_summary`): premature
revenue recognition and exaggerated growth via channel-stuffing to distributors and undisclosed
side arrangements with five distributors, concealed from accountants, auditors and the audit
committee. `scheme_type`: revenue_recognition; manipulation period 2013-01 to 2017-09.

GAAP topics: revenue recognition, pre-ASC-606 era. The complaint states the four revenue
criteria beginning "(i) persuasive evidence of an arrangement exists; (ii) delivery" (¶21, line
236), names "ASC 605, Revenue Recognition" (quoted management representation, line 1458), and
holds the Distributor E arrangement "was, in substance, a consignment arrangement" under GAAP
substance-over-form (¶172, line 1013). No other codification topics are cited.

## 3. SIGNALS AVAILABLE PRE-CUTOFF

Cutoff 2016-12-14 — mid-scheme (conduct ran to Q3 2017; per ¶236 a November 2016 demand letter
alleging "channel stuffing" (line 1463) and the December 2016 Audit Committee Investigation were
not public). Sealed data basis: `~/aaer-data/MDXG/xbrl/CIK0001376339.json` (XBRL companyfacts) +
`~/aaer-data/MDXG/edgar/CIK0001376339.json` / `CIK0001376339-submissions-001.json` (chronology).
Pre-cutoff, at accession level:

- **Receivables outran revenue in FY2015**: AccountsReceivableNetCurrent $26.672M (2014-12-31,
  accn 0001376339-15-000040) → $53.755M (2015-12-31, accn 0001376339-16-000138), +101.5%, vs
  SalesRevenueGoodsNet $118.223M (FY2014) → $187.296M (FY2015) (same accns), +58.6%; Q4 revenue
  $39.573M (Q4-2014) vs $51.835M (Q4-2015, same accns). Pay-on-resale terms and return
  crediting of the ¶2 kind would surface exactly here, though the deck cannot show terms.
- **Income–cash divergence**: NetIncomeLoss $29.446M vs NetCashProvidedByUsedInOperatingActivities
  $18.807M (FY2015, both accn 0001376339-16-000138); NetIncomeLoss $1.197M vs operating cash flow
  −$0.977M (Q1-2016, both accn 0001376339-16-000160).
- **2016 balance-sheet build**: InventoryNet $7.460M (2015-12-31, accn 0001376339-16-000138) →
  $18.313M (2016-09-30, accn 0001376339-16-000213); Goodwill $4.040M (2015-12-31, accn
  0001376339-16-000138) → $30.730M (2016-03-31, accn 0001376339-16-000160);
  IntangibleAssetsNetExcludingGoodwill $10.763M → $33.710M (same dates/accns), against 9M2016
  SalesRevenueGoodsNet $175.139M (accn 0001376339-16-000213) vs 9M2015 $135.461M (accn
  0001376339-15-000100).
- **Chronology friction**: NT 10-Q 2009-02-18 (accn 0001362310-09-002351) preceding a 10-Q
  2009-02-23; 10-K/A amendments incl. 2008-07-29, 2012-04-27, 2014-04-30 (accns
  0001362310-08-003918, 0001193125-12-191763, 0001376339-14-000011); CORRESP 2016-11-30 (accn
  0001376339-16-000216) and UPLOAD 2016-12-06 (accn 0000000000-16-103743) shortly before cutoff.

Not visible in this sealed set: distributor-level terms and side letters, customer concentration
(Distributor E "56% of MiMedx's total reported revenue in 2013; 34%" in 2014, 24% in 2015 —
¶135, lines 823-826), and collections quality (of >$150M Distributor E revenue 2012-2017,
"approximately 8% of which was never collected." — ¶136, line 828). This section describes the
information set — it does not re-score the case.

## 4. WHAT THE LLM CAUGHT

Frozen output `runs/wave2/scores/case_60.json`: `misstatement_probability`: 65 (legacy v1 key —
an uncalibrated ordinal score; see specs/RISK_SCORE_SEMANTICS.md) = score 65, risk_tier
"elevated" — at/above the flag threshold of 50, hence TP. CL1-CL4/CL7 flagged; CL5/CL6 no_flag;
CL8 insufficient_data. Cited evidence values re-verified against the sealed XBRL facts file at
value+date level; one $1K discrepancy noted in §6, none fabricated.

| model claim (verbatim) | enforcement/restatement reference | match quality |
|---|---|---|
| "Potential premature or aggressive revenue recognition (e.g., recording sales to distributors/consignees as final revenue) leading to receivables growing much faster than revenue and a rising implied days-sales-outstanding" (hypothesis 1, top-ranked, "overstated") | ¶2 (lines 61-65): revenue at shipment to Distributor E improper under a side arrangement "allowing Distributor E to pay MiMedx only when it resold the products"; ¶172 (line 1013): arrangement "was, in substance, a consignment arrangement"; scheme_summary premature recognition / channel-stuffing | exact mechanism |
| "Accounts receivable growing far faster than revenue in FY2015 with implied DSO rising from ~61 to ~94 days, suggesting possible aggressive revenue recognition or channel stuffing" (top_signals) | ¶3 (lines 71-73): side arrangements with four additional distributors in "the last three quarters of 2015"; ¶136 (line 828): ~8% of Distributor E revenue "was never collected." | exact mechanism |
| "reported net income substantially outpaces cash generated from operations, potentially reflecting non-cash revenue recognition, working-capital-driven earnings, or aggressive accrual accounting" (hypothesis 2, "overstated") | ¶30 (lines 282-284) / ¶173 (line 1023): "misstated its revenue and operating income in each quarter, year, and interim period from 2013 to 2017." — the complaint does not frame an NI-vs-OCF divergence, but resale-contingent payment terms yield revenue without cash | right direction only |
| "Inventory build materially outpacing revenue growth in 2016 could reflect channel-stuffing preparation, capitalization of costs that should be expensed, or risk of future write-downs" (hypothesis 3, InventoryNet/COGS "overstated") | No inventory or COGS finding in the complaint; the channel-stuffed inventory sat with distributors, not in MiMedx's InventoryNet | right direction only |
| "History of multiple 10-K/A and 8-K/A amendments plus an NT 10-Q late filing, and SEC CORRESP/UPLOAD correspondence shortly before the cutoff date" (top_signals) | No counterpart — the complaint alleges nothing about the 2008-2014 amendments or the late-2016 comment-letter correspondence (the ¶236 demand letter is not a filing-chronology item) | unrelated |

Notes: grade dim2=2 — top hypothesis "names the correct account area (SalesRevenueGoodsNet/AR),
correct direction (overstated), and correct treatment type"; "Not a 3: no case-specific
pinpointed fact from the key (five distributors, undisclosed side arrangements allowing returns,
payment conditioned on resale to end users, concealment from auditors/audit committee) is
explicitly named; 'distributors/consignees' is generic" (`scoring/grades_wave2/case_60.json`).
dim3=2: active vs active — exact genre match.

## 5. WHAT THE LLM MISSED

From the sealed §3 information set: **none identified from sealed evidence** as an unsurfaced
signal class — the receivables/DSO, income-vs-cash, inventory/soft-asset, and chronology axes
were all surfaced (§4). The scheme's most direct footprints — concealed side terms (¶2-¶7),
the related-family loan behind Distributor C's payments (¶6), Distributor E concentration
(¶135), and the ~8% never-collected receivables (¶136) — are absent from the sealed XBRL
aggregates and chronology; insufficient sealed evidence to name any as a missable signal.

## 6. ERROR TAXONOMY

Per `scoring/error_taxonomy.md` (R1→R2→R3), atlas vocabulary. The case is a TP with an exact
genre match (dim3=2); the taxonomy applies to the residual dimension gap (dim2=2, not 3):

- **Primary — no MODEL error identified**: the dim2 2-vs-3 gap turns on case-specific pinpoint
  facts (five distributors, concealed side arrangements, resale-contingent payment) that were
  not in the provided deck; their absence is a world-fact — the complaint alleges active
  concealment (¶8) — not a collection/extraction defect, so the R1 DATA branch does not apply
  and no reasoning failure is chargeable under R3. Recorded as an information-ceiling on the
  grade, not a bucketed error.
- **Computation**: one trivial discrepancy — the model quotes 9M2016 revenue as "175,138,000";
  the sealed XBRL reports 175,139,000 (accn 0001376339-16-000213), consistent with the model
  summing the three quarters (53,367+57,342+64,429 = 175,138) rather than citing the reported
  YTD figure; immaterial to every ratio claimed. All other cited values re-verified (dim4=3).
- **Label-noise**: none — enforcement-confirmed tier; nuance for the record: the company
  settled "[w]ithout admitting or denying the allegations" while "[t]he litigation continues
  against the three executives" (LR-24678, line 1091).
- **Suspected-memorization**: recognition probe — the single stored draw
  `scoring/probe_results_wave2/recognition/case_60.json` — guessed "OPKO Health, Inc." with
  confidence "medium" (incorrect company); verbatim probe
  `scoring/probe_results_wave2/verbatim/case_60.json`: known: false, recall fields null. Grade
  memorization_suspect_condition2: false — reasoning "cites concrete provided data content ...
  rather than merely listing documents, and mentions no post-cutoff facts (no reference to the
  revelation, SEC complaint LR-24678, or enforcement outcome)".

## 7. CPA JUDGMENT — human_finalized: false

Draft, unaudited work product until owner sign-off (PROJECT.md §7).

- The footprint the model led with is the one this scheme mechanically produces: paying only
  on resale and crediting returns (¶2) converts shipments into uncollected AR, and the sharpest
  AR-vs-revenue divergence appears in FY2015 — the exact period four additional distributor
  side arrangements were layered on (¶3). This supports reading the score-65 flag as
  substantive rather than coincidental. **[OWNER REVIEW]**
- The model's "distributors/consignees as final revenue" phrasing lands close to ¶172's
  consignment-in-substance holding — notable because MiMedx's disclosed policy (¶22) was
  facially GAAP-conformant and the terms were concealed; a filings-only analyst could suspect
  but not confirm this. Whether that closeness deserves more than dim2=2 under the pre-fixed
  anchors is an owner call. **[OWNER REVIEW]**
- The CL2 goodwill/intangibles jump at 2016-03-31 ($4.040M→$30.730M; $10.763M→$33.710M) has no
  counterpart in the complaint; treating it as supporting evidence risks over-crediting the
  flag. **[OWNER REVIEW]**
- Hypothesis 3's line-item framing (MiMedx's own InventoryNet/COGS "overstated") misplaces the
  channel-stuffing footprint — the complaint locates the stuffed product with distributors and
  alleges revenue/operating-income misstatement (¶30), not inventory misstatement.
  **[OWNER REVIEW]**
- Cutoff 2016-12-14 sits inside the concealment window (¶236-¶240: November 2016 demand
  letter, December 2016 misleading disclosures to Law Firm A and the Audit Committee), none of
  it public; the model was scoring mid-scheme, three quarters before the conduct ended.
  **[OWNER REVIEW]**

## 8. AUDIT TRANSLATION

Procedures the flag would motivate — procedures, not conclusions:

- Distributor confirmations explicitly covering side terms — return/swap rights, payment
  contingent on resale or third-party authorization, credits for lost/damaged/returned product
  (the ¶2-¶7 arrangement set) — with inquiry beyond the written distribution agreement.
- Substance-over-form evaluation of the largest-distributor relationship against consignment
  indicators (¶19: no payment obligation until use, seller retains risk of loss,
  returnability), including payment-history analytics for resale-linked cash patterns.
- AR aging, subsequent-cash-receipt testing, and collectibility assessment on distributor
  balances (motivated by the never-collected share at ¶136); source-of-funds inquiry where a
  startup distributor's payments evidence collectibility (¶6 related-family loan).
- Revenue cutoff testing weighted to quarter-ends and newly onboarded distributors in
  growth-gap quarters (¶3-¶7 cluster in Q2-Q4 2015); credit-memo and post-period return/swap
  activity review.
- Management-representation and Audit Committee corroboration keyed to revenue-criteria
  assertions (¶21 four criteria; the lines 1456-1458 representation that new-distributor sales
  "have met the" ASC 605 criteria).

## 9. FINANCIAL STATEMENT IMPACT

From the sealed complaint text: MiMedx announced in "a June 7, 2018 Form 8-K" that it "would be
restating its financial statements for fiscal years 2012-2016 and its condensed financial
statements for the first three quarters of 2017" (¶27, lines 272-274), but as of the complaint
date "MiMedx has not yet filed restated financial statements." (¶29, line 281) — restated
line-item amounts are therefore **not determinable** from the sealed sources read. Determinable
direction and alleged magnitudes from the complaint: revenue and operating income misstated
(overstated via improper/premature recognition) "in each quarter, year, and interim period from
2013 to 2017" (¶173, line 1023; ¶30); improper revenue of "at least 6% to 14% of its reported
revenue each quarter" in the last three quarters of 2015 (¶3, line 73); named amounts: "$1.9
million order" and "$2.54 million order" (Distributor A, ¶4, lines 75/82), "$1.4 million of
revenue" ≈3% of quarterly revenue (Distributor B, ¶5/¶58, lines 86/413), "$4.6 million of
revenue" plus "$1 million" (Distributor C, ¶6, lines 92/96), "$2.2 million in revenue" plus
"$450,000" (Distributor D, ¶7, lines 106/110); more than "$150 million in Distributor E
revenue" 2012-2017, ~8% never collected (¶136, lines 827-828). Company civil penalty: $1.5
million (LR-24678, line 1091).

---
*Entry status: drafted (sections 7–9 pending owner finalization).*
*채점: Claude 보조 + 인간 최종 확정. 교육·정보 목적, 투자 자문 아님.*
