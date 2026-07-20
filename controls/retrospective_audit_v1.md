# controls/retrospective_audit_v1.md — 회고 대조군 청정성 감사 (공시 전용)

> **Authored by Claude Code, pending human audit (D15).** Authority: D106 §3,
> procedure docs/CONTROL_CRITERIA_v3.md §4 (freeze-committed 1ce4cb8 before
> this run). Disclosure only — no published FPR recomputed, no control
> reclassified, no frozen artifact touched. 본 결과는 Claude 기반 단일
> 파이프라인에 한정된다 (PROJECT.md §5-5).

## 1. Methodology

- **Audit date**: 2026-07-21. All live queries were issued on this date with
  User-Agent `aaer-evals research lastwhisper906@gmail.com`, ≥0.4s between
  requests. Full per-control query URLs and access dates are in
  `controls/retrospective_audit_v1.json` (fields `source`/`search_date`/notes).
- **Population**: 62 controls in 4 sets per v3 §4 (2026-07-21 정정 기록 적용):
  wave-1 C01–C08 (8), wave-1 v2-controls V01–V22 (22), wave-2 W01–W23 (23),
  holdout hc 9 (VIASP, UTL, GRDX, RXO, BCO, XPO, GO, SFM, VLGEA).
  **Dup-CIK note**: 5 CIKs appear in two sets and were audited once with the
  union of the two windows, verdicts recorded on both rows (v3 §4):
  C01=V02 (MOS, 0001285785), C03=V09 (GRMN, 0001121788), C04=V10 (R,
  0000085961), C07=V18 (FORR, 0001023313), C08=V21 (GIS, 0000040704).
- **Window operationalization** (v3 §4, fixed pre-run): W start = matched
  treatment `manipulation_period_start`, else `cutoff` − 36mo (per the offline
  pass); W end = `cutoff` + 24mo. Per-control windows are in the JSON.
- **Sources & query log summary**:
  - **(a)** Sealed AAER respondents index snapshot (fetched_at
    2026-07-06T08:46:46Z, offline pass). Token screen negative for 55/62 rows;
    7 fuzzy token hits (C08/V21 `general`, V22 `campbell`, V01 `products`,
    W01 `nabors`, W19 `technologies`, W15 `universal`) were manually verified
    as false positives — generic-token collisions with unrelated respondents
    (e.g., General Electric–related respondents ≠ General Mills; the
    individual respondent "John Mervyn Nabors" ≠ Nabors Industries Ltd; the
    remaining hits are common-word collisions of the same kind). (a) = PASS
    for all 62.
  - **(b)(c)** Deterministic screens over sealed EDGAR submissions metadata
    (offline pass): in-window 10-K/A·10-Q/A enumerated with accessions;
    Item 4.02 items-field screen — **zero in-window Item 4.02 across all 62**.
  - **(e)** All 15 in-window Item 4.01 8-Ks fetched from
    `https://www.sec.gov/Archives/edgar/data/{cik}/{accession}.txt`
    (access 2026-07-21); Item 304 disagreement/reportable-event language
    extracted and quoted below. 15/15 fetches succeeded.
  - **(d)** EDGAR full-text search
    `https://efts.sec.gov/LATEST/search-index?q=%22material+weakness%22&forms=10-K&ciks={cik}&startdt=…&enddt=…`
    per control window (10-Q re-query when 10-K hit); up to 3 hit documents
    context-checked per control; supplemental phrase query
    `q=%22identified+a+material+weakness%22` (forms 10-K,10-Q, same window)
    run for all 57 unique CIKs as a safety net against the 3-document cap
    (it surfaced FORR's FY2012–13 disclosures, which were then
    document-verified). FTS covers 2001+; all windows start 2008+, so no
    pre-FTS INCOMPLETE was needed. All 57 CIKs had ≥1 raw hit — raw hits are
    dominated by definitional/risk-factor boilerplate; verdicts below rest on
    document context, quoted.
  - **(f)** Stanford SCAC. The pre-registered URL form
    `filings.html?ticker=…` proved to be a login-gated column filter, so the
    public equivalent `https://securities.stanford.edu/fullsearch.html?q=…`
    was used with ticker + company name + former registrant names (CryoLife,
    Spark Energy, Ensco, Entero Therapeutics, First Wave BioPharma, AzurRx,
    DDR/Developers Diversified, Upbound); candidate case labels were
    name-matched and all decision-relevant case pages
    (`filings-case.html?id=…`) were opened (access 2026-07-21). Class-period
    dates, where decision-relevant, were verified from the registrants' own
    EDGAR litigation disclosures (quoted). SCAC banner note: the site is
    under restructuring ("updates and new filings will not be available"
    until Winter 2026) — very recent filings may be missing; this affects
    only hc controls, which are provisional under (g) regardless.
  - **(g)** Date arithmetic: window end (= cutoff + 24mo) vs audit date.

## 2. Verdict table (62 rows)

Codes: P = PASS · P* = PASS with documented note (§3) · M = MINOR ·
F = FAIL · I = INCOMPLETE. Tier per v3 §2: A / B / provisional-INCOMPLETE /
ineligible (FAIL ≥1).

| set | ID | ticker | CIK | a | b | c | d | e | f | g | tier |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C | C01 | MOS | 0001285785 | P | P* | P | P | P | P | P | A |
| C | C02 | NUVA | 0001142596 | P | P | P | P | P | F | P | ineligible |
| C | C03 | GRMN | 0001121788 | P | P* | P | P | M | P | P | B |
| C | C04 | R | 0000085961 | P | P* | P | P | P | F | P | ineligible |
| C | C05 | PERY | 0000900349 | P | P | P | P | M | P* | P | B |
| C | C06 | XLNX | 0000743988 | P | P | P | P | P | P* | P | A |
| C | C07 | FORR | 0001023313 | P | P | P* | M | P | P | P | B |
| C | C08 | GIS | 0000040704 | P* | P | P* | P | P | P | P | A |
| V | V01 | APD | 0000002969 | P* | P | P | P | P | P* | P | A |
| V | V02 | MOS | 0001285785 | P | P* | P | P | P | P | P | A |
| V | V03 | CE | 0001306830 | P | P* | P | P | P | P | P | A |
| V | V04 | MASI | 0000937556 | P | P* | P | P | P | P* | P | A |
| V | V05 | ARAY | 0001138723 | P | P* | P* | M | P | P* | P | B |
| V | V06 | MMSI | 0000856982 | P | P | P | P | P | P* | P | A |
| V | V07 | TDY | 0001094285 | P | P | P | P | M | P | P | B |
| V | V08 | CIEN | 0000936395 | P | P | P | P | P | P* | P | A |
| V | V09 | GRMN | 0001121788 | P | P* | P | P | M | P | P | B |
| V | V10 | R | 0000085961 | P | P* | P | P | P | F | P | ineligible |
| V | V11 | UPBD | 0000933036 | P | P* | P | P | M | F | P | ineligible |
| V | V12 | IDCC | 0001405495 | P | P | P | P | P | P | P | A |
| V | V13 | RCKY | 0000895456 | P | P* | P | P | P | P | P | A |
| V | V14 | DLB | 0001308547 | P | P | P | P | P | P | P | A |
| V | V15 | FSLR | 0001274494 | P | P* | P | P | P | P* | P | A |
| V | V16 | AMKR | 0001047127 | P | P | P* | P | P | P* | P | A |
| V | V17 | BHE | 0000863436 | P | P* | P | P | P | P* | P | A |
| V | V18 | FORR | 0001023313 | P | P | P* | M | P | P | P | B |
| V | V19 | EXPO | 0000851520 | P | P | P | P | P | P | P | A |
| V | V20 | LQDT | 0001235468 | P | P | P | P | P | F | P | ineligible |
| V | V21 | GIS | 0000040704 | P* | P | P* | P | P | P | P | A |
| V | V22 | CPB | 0000016732 | P* | P | P | P | P | M | P | B |
| W | W01 | NBR | 0001163739 | P* | P* | P | P | P | P | P | A |
| W | W02 | VAL | 0000314808 | P | P | P | P | P | P* | P | A |
| W | W03 | RGEN | 0000730272 | P | P | P* | P | P | P | P | A |
| W | W04 | IOVA | 0001425205 | P | P* | P | M | M | P* | P | B |
| W | W05 | HALO | 0001159036 | P | P* | P | P | P | P | P | A |
| W | W06 | SITC | 0000894315 | P | P* | P | P | P | P | P | A |
| W | W07 | BXMT | 0001061630 | P | P | P | P | M | P | P | B |
| W | W08 | ADAM | 0001273685 | P | P | P* | P | P | P | P | A |
| W | W09 | LPSN | 0001102993 | P | P* | P | P | P | P* | P | A |
| W | W10 | HSTM | 0001095565 | P | P | P | P | P | P | P | A |
| W | W11 | MCHX | 0001224133 | P | P* | P | P | M | M | P | B |
| W | W12 | DAR | 0000916540 | P | P | P | P | P | P | P | A |
| W | W13 | FLO | 0001128928 | P | P | P | P | P | F | P | ineligible |
| W | W14 | BF-A | 0000014693 | P | P | P | P | P | P | P | A |
| W | W15 | ULH | 0001308208 | P* | P | P* | P | P | P | P | A |
| W | W16 | SAIA | 0001177702 | P | P | P | P | P | P | P | A |
| W | W17 | MRTN | 0000799167 | P | P | P | P | P | P | P | A |
| W | W18 | AORT | 0000784199 | P | P* | P | P | P | P* | P | A |
| W | W19 | UFPT | 0000914156 | P* | P* | P | P | P | P | P | A |
| W | W20 | ATRC | 0001323885 | P | P | P | P | P | P* | P | A |
| W | W21 | LEVI | 0000094845 | P | P | P | P | P | P* | P | A |
| W | W22 | RL | 0001037038 | P | P | P* | P | P | P | P | A |
| W | W23 | CTAS | 0000723254 | P | P | P | P | P | M | P | B |
| hc | VIASP | VIASP | 0001606268 | P | P* | P | M | P | P* | I | provisional-INCOMPLETE |
| hc | UTL | UTL | 0000755001 | P | P | P | P | P | P | I | provisional-INCOMPLETE |
| hc | GRDX | GRDX | 0001604191 | P | P* | P | I | F | P* | I | ineligible |
| hc | RXO | RXO | 0001929561 | P | P | P | P | M | P | I | provisional-INCOMPLETE |
| hc | BCO | BCO | 0000078890 | P | P | P | M | P | P | I | provisional-INCOMPLETE |
| hc | XPO | XPO | 0001166003 | P | P | P | P | P | P* | I | provisional-INCOMPLETE |
| hc | GO | GO | 0001771515 | P | P | P | F | P | I | I | ineligible |
| hc | SFM | SFM | 0001575515 | P | P | P | P | P | P* | I | provisional-INCOMPLETE |
| hc | VLGEA | VLGEA | 0000103595 | P | P* | P | P | P | P | I | provisional-INCOMPLETE |

Tallies: **Tier A 35 · Tier B 12 · provisional-INCOMPLETE
7 · ineligible (≥1 FAIL) 8**.

## 3. Notes and citations

### 3.1 (a) fuzzy-token disambiguation

The 7 token hits and their resolutions are recorded in the JSON per row; all
are generic-token collisions (company-name common words or homonymous
individual respondents), verified manually against the sealed index snapshot
(fetched_at 2026-07-06). No SEC enforcement action naming any of the 62
registrants with conduct intersecting its window was found.

### 3.2 FAIL verdicts (full citations)

- **C02 (NUVA) — (f) FAIL**: NuVasive, Inc. Securities Litigation (SCAC id=105097, filed 2013-08-28, status SETTLED, final judgment 2018-12-06). Class period 2008-10-22 -> 2013-07-30 (per registrant's FY2013 10-K accn 0001142596-14-000004, filed 2014-03-03: "a putative class period stemming from October 22, 2008 to July 30, 2013") intersects C02 window [2011-01-01, 2015-07-28]. Docket (SCAC page): two motions to dismiss granted with leave to amend (2014-08-19, 2014-12-09); subsequent amended complaints proceeded, defendants' motion for summary judgment denied 2018-02-01, case settled — the operative complaint survived dismissal and the case proceeded past the pleading stage. v3 SS1(f) FAIL branch (survival in whole or part).
- **C04 (R) — (f) FAIL**: Ryder System, Inc. Securities Litigation (SCAC id=107418, filed 2020-05-20, status SETTLED, final judgment 2024-11-12). Class period 2015-07-23 -> 2020-02-13 (per registrant's 10-Q filed 2020-07-31: "on behalf of purchasers of our securities who purchased or otherwise acquired their securities between July 23, 2015 and February 13, 2020") intersects C04 window [2012-02-01, 2016-05-12]. SCAC page: "On May 12, 2022, the Court issued an Order denying Defendants' Motion to Dismiss." — MTD denied (survived) -> FAIL.
- **V10 (R) — (f) FAIL**: Same case and facts as C04 (same CIK); class period 2015-07-23 -> 2020-02-13 intersects V10 window [2011-05-13, 2016-05-12]; MTD denied 2022-05-12.
- **V11 (UPBD) — (f) FAIL**: Rent-A-Center, Inc. Securities Litigation (Hall/DePalma; SCAC id=106002, filed 2016-12-23, status SETTLED, final judgment 2019-05-03). Class period 2015-07-27 -> 2016-10-10 (per registrant's FY2016 10-K, filed 2017-03-01: "on behalf of all purchasers of our common stock from July 27, 2015, through October 10, 2016") intersects V11 window [2011-05-13, 2016-05-12]. SCAC page: "On December 14, [2017,] the Court issued an Order denying Defendants' Motion to Dismiss." — MTD denied (survived) -> FAIL. (Separate 2018 case, SCAC id=106690: merger-related, voluntarily dismissed 2018-10-19, conduct post-window — note only.)
- **V20 (LQDT) — (f) FAIL**: Liquidity Services, Inc. Securities Litigation (SCAC id=105322, filed 2014-07-14, status SETTLED, final judgment 2018-10-05). Class period 2012-02-01 -> 2014-05-07 (per registrant's FY2014 10-K, filed 2014-11-21: "on behalf of shareholders who purchased the Company's common stock between February 1, 2012 and May 7, 2014") intersects V20 window [2013-02-28, 2018-02-28]. SCAC page: "On March 31, 2016, the Court issued an Order granting in part and denying in part Defendants' Motion to Dismiss"; class certified 2017-09-06; settled — partial survival -> FAIL.
- **W13 (FLO) — (f) FAIL**: Flowers Foods, Inc. Securities Litigation (SCAC id=105872, filed 2016-08-12, status SETTLED, final judgment 2019-12-11). Class period 2013-02-07 -> 2016-08-10 (per registrant's 10-Q filed 2016-11-09: "securities holders that acquired company securities between February 7, 2013 and August 10, 2016") intersects W13 window [2013-08-15, 2018-08-14]. SCAC page: "On March 23, 2018, the Court issued an Order granting in part and denying in part Defendants' Motion to Dismiss." — partial survival -> FAIL.
- **GRDX (GRDX) — (e) FAIL**: Three in-window Item 4.01 8-Ks. Two are routine (accn 0001104659-24-068733, 2024-06-05, Forvis Mazars engagement, no disagreements; accn 0001104659-24-094936, 2024-08-29, MGO engagement, no disagreements). One reports an auditor resignation accompanied by a stated Disagreement: accn 0001104659-24-089923 (2024-08-15, registrant then named Entero Therapeutics, Inc., same CIK 0001604191): "Forvis Mazars resigned due to a belief that the Company can no longer generate reliable information to prepare its financials as a result of the cost reduction measures and other corporate developments ... The Company disagrees with Forvis Mazars' belief (the 'Disagreement')." and "During the Interim Period, Forvis Mazars did not advise the Company of any matters specified in Item 304(a)(1)(v) of Regulation S-K other than the subject matter of the Disagreement discussed above." A resignation accompanied by an Item 304 disagreement/reportable-event subject matter meets the v3 SS1(e) FAIL branch.
- **GO (GO) — (d) FAIL**: MW as of 2023-12-30 (IT general controls during ERP component replacement; FY2023 10-K accn 0001771515-24-000016, 2024-02-28: "we concluded that the deficiencies represent a material weakness ... internal control over financial reporting was not effective as of December 30, 2023", Deloitte adverse ICFR opinion). NOT remediated at the next annual assessment: FY2024 10-K accn 0001771515-25-000017 (2025-02-26): "certain controls have not consistently operated effectively for a sufficient period of time to conclude the material weakness was remediated ... internal control over financial reporting was not effective as of December 28, 2024", second consecutive adverse ICFR opinion. Remediated only at FY2025 assessment (10-K accn 0001771515-26-000015, 2026-03-04: "the material weakness was remediated" as of 2026-01-03). Persistence past the next annual assessment meets the v3 SS1(d) FAIL branch. No restatement link evidenced (FY2024 10-K: "We did not identify any material misstatements to the consolidated financial statements"; zero Item 4.02).

### 3.3 MINOR verdicts

- **C03 (GRMN) — (e) MINOR**: Two in-window Item 4.01 8-Ks, both auditor changes for the registrant's employee benefit plan financial statements, both routine: accn 0001144204-14-044890 (2014-07-25): "there were no disagreements between the Plan and Mayer Hoffman McCann P.C. ... [and] no 'reportable events' as that term is defined in Item 304(a)(1)(v) of Regulation S-K"; accn 0001144204-14-063970 (2014-10-30, RubinBrown engagement): no disagreement/reportable-event consultation.
- **C05 (PERY) — (e) MINOR**: One in-window Item 4.01 8-K, routine: accn 0001193125-13-370542 (2013-09-18, Deloitte -> new auditor): "there were no disagreements between the Company and Deloitte on any matters of accounting principles or practices, financial statement disclosure, or auditing scope and procedures".
- **C07 (FORR) — (d) MINOR**: MW as of 2012-12-31 (controls over advisory services/consulting revenue; FY2012 10-K accn 0001193125-13-112678, 2013-03-18, ICFR not effective, auditor adverse ICFR opinion) plus second MW as of 2013-09-30 (event-ticket revenue, 10-Qs 2013); FY2013 10-K accn 0001193125-14-097919 (2014-03-13): "as of December 31, 2013, we concluded that we have remediated these material weaknesses" — remediated by next annual assessment; no Item 4.02 ever in window. Note: both MW assessment dates precede C07's own window start (2014-02-01); disclosure/remediation reporting falls in window. Verdict kept uniform with V18 (same CIK, audited once).
- **V05 (ARAY) — (d) MINOR**: MW as of 2011-06-30 (accounting for significant non-routine transactions), disclosed in FY2011 10-K accn 0001047469-11-008120 (2011-09-19); FY2012 10-K accn 0001047469-12-008730 (2012-09-10): "management determined that the material weakness described above was successfully remediated and no longer existed as of June 30, 2012" — remediated by next annual assessment; no Item 4.02 in window (no restatement link evidenced).
- **V07 (TDY) — (e) MINOR**: Two in-window Item 4.01 8-Ks (E&Y dismissal / D&T engagement), routine: accn 0001094285-15-000043 (2015-04-15) and 0001094285-15-000080 (2015-05-04): "there was no disagreement (as described in Item 304(a)(1)(iv) ...) with E&Y ... which ... would have caused E&Y to make reference to the matter in their report".
- **V09 (GRMN) — (e) MINOR**: Same two filings as C03 (same CIK).
- **V11 (UPBD) — (e) MINOR**: Two in-window Item 4.01 8-Ks (Grant Thornton -> KPMG), routine: accn 0000933036-12-000006 (2012-12-19) and 0000933036-13-000009 (2013-02-26): "there were no (i) disagreements ... or (ii) reportable events as defined in Item 304(a)(1)(v) of Regulation S-K".
- **V18 (FORR) — (d) MINOR**: Same facts as C07 (same CIK; MW as of 2012-12-31 disclosed 2013-03-18 in-window for V18, second MW as of 2013-09-30, both remediated as of 2013-12-31 per FY2013 10-K accn 0001193125-14-097919); no restatement link evidenced.
- **V22 (CPB) — (f) MINOR**: Campbell Soup Company Securities Litigation (SCAC id=106750, filed 2018-09-28, in-window, status DISMISSED). SCAC page: MTD granted 2020-11-30 (leave to amend) and again 2022-10-12 — "The case was dismissed with prejudice." Dismissed at the motion-to-dismiss stage -> MINOR. (Second listed case, id=101334, filed 2000-01-07 — pre-window, note only.)
- **W04 (IOVA) — (d) MINOR**: MW as of 2014-12-31 (then-named Lion Biotechnologies: insufficient monitoring/review controls over close process, segregation of duties; FY2014 10-K accn 0001144204-15-016315, 2015-03-16, ICFR not effective, adverse auditor ICFR report); FY2015 10-K accn 0001144204-16-087506 (2016-03-11): "As of December 31, 2015, we believe we have remedied any material weaknesses" — remediated by next annual assessment; no Item 4.02 in window.
- **W04 (IOVA) — (e) MINOR**: One in-window Item 4.01 8-K, routine: accn 0001144204-16-093221 (2016-04-07, Weinberg -> Marcum): "there were no disagreements between our company and Weinberg ... [no] reportable event (as defined in Item 304(a)(1)(v) of Regulation S-K)".
- **W07 (BXMT) — (e) MINOR**: Two in-window Item 4.01 8-Ks (2013 Ernst & Young transitions), routine: accn 0001193125-13-107775 (2013-03-14) and 0001193125-13-126816 (2013-03-26): "there were (i) no disagreements ... and (ii) no 'reportable events' (as that term is defined in Item 304(a)(1)(v) of Regulation S-K)".
- **W11 (MCHX) — (e) MINOR**: One in-window Item 4.01 8-K, routine: accn 0001564590-17-013072 (2017-06-28, KPMG dismissal / Moss Adams engagement): "we had no disagreements (as defined in Item 304 of Regulation S-K) with KPMG ... there were no reportable events of the type described in Item 304(a)(1)(v)".
- **W11 (MCHX) — (f) MINOR**: Marchex, Inc. Securities Litigation (SCAC id=105697, filed 2015-11-17, in-window, status DISMISSED): "This case was voluntarily dismissed on April 22, 2016." Voluntary dismissal -> MINOR.
- **W23 (CTAS) — (f) MINOR**: Cintas Corporation Securities Litigation (SCAC id=107260, filed 2019-12-12, in-window, status DISMISSED): notice of voluntary dismissal 2020-04-22. Voluntary dismissal -> MINOR.
- **VIASP (VIASP) — (d) MINOR**: MW as of 2022-12-31 (controls over deferred tax assets/liabilities and income tax expense; disclosed in FY2022 10-K accn 0001606268-23-000009, 2023-03-29, in-window); FY2023 10-K accn 0001606268-24-000008 (2024-02-29): "management concluded that the material weakness described above had been fully remediated as of December 31, 2023" — remediated by next annual assessment. FY2024/FY2025 10-Ks each contain a single carried-over cross-reference sentence in Item 9A; both conclude "internal control over financial reporting was effective" (as of 2024-12-31 and 2025-12-31 — verified in accn 0001606268-25-000006 and 0001606268-26-000013). No Item 4.02 in window.
- **RXO (RXO) — (e) MINOR**: One in-window Item 4.01 8-K, routine: accn 0001929561-24-000055 (2024-04-02, KPMG): "there were no (1) disagreements (within the meaning of Item 304(a)(1)(iv) of Regulation S-K) with KPMG ... or (2) reportable events (within the meaning of Item 304(a)(1)(v) of Regulation S-K)".
- **BCO (BCO) — (d) MINOR**: MW as of 2022-12-31 (risk assessment/process-level controls incl. NoteMachine acquisition scope; FY2022 10-K accn 0000078890-23-000090, 2023-03-01, in-window disclosure, KPMG adverse ICFR opinion); FY2023 10-K accn 0000078890-24-000054 (2024-02-29): remediation of the 2022 material weakness completed — "identified during 2022, which was fully remediated by December 31, 2023" — remediated by next annual assessment; no Item 4.02 in window.

### 3.4 INCOMPLETE verdicts — (d)/(f)

- **GRDX (GRDX) — (d) INCOMPLETE**: MW disclosed in FY2025 10-K accn 0001104659-26-054106 (2026-05-01; registrant's first MW disclosure in window): "insufficient accounting resources and processes to ensure the timely and accurate preparation, review, and consolidation of financial information in accordance with U.S. GAAP. Management is in the process of implementing remediation measures ... these remediation efforts were not fully implemented or tested as of December 31, 2025." The next annual assessment (FY2026) does not yet exist, so the MINOR-vs-FAIL branch (remediated by next annual assessment or not) cannot be determined yet — INCOMPLETE, time-resolved; FAIL-candidate if unremediated at the FY2026 assessment.
- **GO (GO) — (f) INCOMPLETE**: Grocery Outlet Holding Corp. Securities Litigation (SCAC id=108530, filed 2025-01-30, status ONGOING, last review 2025-07-15). Class period 2023-11-07 -> 2024-05-07 (per registrant's FY2024 10-K, filed 2025-02-26: "on behalf of purchasers of our common stock between November 7, 2023 and May 7, 2024") intersects the window [2023-02-20, 2028-02-19]. No motion-to-dismiss ruling on the SCAC page (only consolidation/lead-plaintiff order 2025-06-03) — MTD status undeterminable -> INCOMPLETE.

All 9 hc rows additionally carry **(g) INCOMPLETE** (window end = cutoff
2026-02/03 + 24mo not yet reached at audit date 2026-07-21) — provisional per
v3 §1(g); (a)–(f) are to be re-searched when each window elapses.

### 3.5 (b) amendment documentation notes (PASS-with-note rows)

Zero in-window Item 4.02 across all 62 rows means no non-reliance (Big-R)
restatement is evidenced for any in-window amendment; the amendments below are
documented facts of record (little-r / administrative / unknown character):

- **C01 (MOS)**: In-window amendment(s), documented: 10-K/A 2012-07-31 accn 0001193125-12-323518; 10-Q/A 2010-10-29 accn 0001193125-10-240904. Zero Item 4.02 8-K in window — no non-reliance (Big-R) restatement is evidenced; amendment character little-r/administrative/unknown.
- **C03 (GRMN)**: In-window amendment(s), documented: 10-Q/A 2011-08-30 accn 0001144204-11-050441; 10-Q/A 2009-09-01 accn 0001144204-09-046684. Zero Item 4.02 8-K in window — no non-reliance (Big-R) restatement is evidenced; amendment character little-r/administrative/unknown.
- **C04 (R)**: In-window amendment(s), documented: 10-K/A 2012-03-19 accn 0001193125-12-121535. Zero Item 4.02 8-K in window — no non-reliance (Big-R) restatement is evidenced; amendment character little-r/administrative/unknown. Resolved benignly in atlas/case_10.md: the 10-K/A 0001193125-12-121535 carries no numeric revision footprint in sealed XBRL facts (every spot-checked figure identical to earlier originals).
- **V02 (MOS)**: In-window amendment(s), documented: 10-K/A 2012-07-31 accn 0001193125-12-323518; 10-Q/A 2010-10-29 accn 0001193125-10-240904. Zero Item 4.02 8-K in window — no non-reliance (Big-R) restatement is evidenced; amendment character little-r/administrative/unknown.
- **V03 (CE)**: In-window amendment(s), documented: 10-K/A 2012-04-24 accn 0001306830-12-000053. Zero Item 4.02 8-K in window — no non-reliance (Big-R) restatement is evidenced; amendment character little-r/administrative/unknown.
- **V04 (MASI)**: In-window amendment(s), documented: 10-K/A 2013-04-29 accn 0001193125-13-182006. Zero Item 4.02 8-K in window — no non-reliance (Big-R) restatement is evidenced; amendment character little-r/administrative/unknown.
- **V05 (ARAY)**: In-window amendment(s), documented: 10-K/A 2013-03-25 accn 0001104659-13-023771. Zero Item 4.02 8-K in window — no non-reliance (Big-R) restatement is evidenced; amendment character little-r/administrative/unknown.
- **V09 (GRMN)**: In-window amendment(s), documented: 10-Q/A 2011-08-30 accn 0001144204-11-050441. Zero Item 4.02 8-K in window — no non-reliance (Big-R) restatement is evidenced; amendment character little-r/administrative/unknown.
- **V10 (R)**: In-window amendment(s), documented: 10-K/A 2012-03-19 accn 0001193125-12-121535. Zero Item 4.02 8-K in window — no non-reliance (Big-R) restatement is evidenced; amendment character little-r/administrative/unknown. Resolved benignly in atlas/case_10.md: the 10-K/A 0001193125-12-121535 carries no numeric revision footprint in sealed XBRL facts (every spot-checked figure identical to earlier originals).
- **V11 (UPBD)**: In-window amendment(s), documented: 10-K/A 2012-04-20 accn 0001193125-12-173208; 10-K/A 2015-09-18 accn 0000933036-15-000031. Zero Item 4.02 8-K in window — no non-reliance (Big-R) restatement is evidenced; amendment character little-r/administrative/unknown.
- **V13 (RCKY)**: In-window amendment(s), documented: 10-K/A 2013-03-05 accn 0001144204-13-012851; 10-Q/A 2012-10-31 accn 0001144204-12-058600. Zero Item 4.02 8-K in window — no non-reliance (Big-R) restatement is evidenced; amendment character little-r/administrative/unknown.
- **V15 (FSLR)**: In-window amendment(s), documented: 10-Q/A 2015-11-20 accn 0001274494-15-000053; 10-Q/A 2015-11-20 accn 0001274494-15-000051. Zero Item 4.02 8-K in window — no non-reliance (Big-R) restatement is evidenced; amendment character little-r/administrative/unknown.
- **V17 (BHE)**: In-window amendment(s), documented: 10-Q/A 2017-08-08 accn 0000863436-17-000032. Zero Item 4.02 8-K in window — no non-reliance (Big-R) restatement is evidenced; amendment character little-r/administrative/unknown.
- **W01 (NBR)**: In-window amendment(s), documented: 10-K/A 2009-03-31 accn 0000950129-09-001082; 10-K/A 2011-03-31 accn 0000950123-11-031283. Zero Item 4.02 8-K in window — no non-reliance (Big-R) restatement is evidenced; amendment character little-r/administrative/unknown.
- **W04 (IOVA)**: In-window amendment(s), documented: 10-K/A 2015-04-20 accn 0001144204-15-023756. Zero Item 4.02 8-K in window — no non-reliance (Big-R) restatement is evidenced; amendment character little-r/administrative/unknown.
- **W05 (HALO)**: In-window amendment(s), documented: 10-Q/A 2015-08-11 accn 0001159036-15-000082. Zero Item 4.02 8-K in window — no non-reliance (Big-R) restatement is evidenced; amendment character little-r/administrative/unknown.
- **W06 (SITC)**: In-window amendment(s), documented: 10-K/A 2013-03-19 accn 0001193125-13-115090; 10-K/A 2015-03-12 accn 0001193125-15-088978; 10-K/A 2014-03-20 accn 0001193125-14-106856. Zero Item 4.02 8-K in window — no non-reliance (Big-R) restatement is evidenced; amendment character little-r/administrative/unknown.
- **W09 (LPSN)**: In-window amendment(s), documented: 10-K/A 2016-01-22 accn 0001102993-16-000008. Zero Item 4.02 8-K in window — no non-reliance (Big-R) restatement is evidenced; amendment character little-r/administrative/unknown. Resolved benignly in atlas/case_48.md: zero XBRL facts attributed to the 10-K/A accession (no numeric revision footprint); zero Item 4.02 in the registrant's entire sealed history.
- **W11 (MCHX)**: In-window amendment(s), documented: 10-K/A 2017-04-27 accn 0001564590-17-007567. Zero Item 4.02 8-K in window — no non-reliance (Big-R) restatement is evidenced; amendment character little-r/administrative/unknown.
- **W18 (AORT)**: In-window amendment(s), documented: 10-K/A 2016-03-25 accn 0001193125-16-518038; 10-Q/A 2018-11-19 accn 0001193125-18-329708. Zero Item 4.02 8-K in window — no non-reliance (Big-R) restatement is evidenced; amendment character little-r/administrative/unknown.
- **W19 (UFPT)**: In-window amendment(s), documented: 10-K/A 2016-08-18 accn 0001558370-16-008050. Zero Item 4.02 8-K in window — no non-reliance (Big-R) restatement is evidenced; amendment character little-r/administrative/unknown.
- **VIASP (VIASP)**: In-window amendment(s), documented: 10-K/A 2026-04-27 accn 0001606268-26-000020; 10-K/A 2025-04-28 accn 0001606268-25-000011; 10-K/A 2024-03-27 accn 0001606268-24-000011. Zero Item 4.02 8-K in window — no non-reliance (Big-R) restatement is evidenced; amendment character little-r/administrative/unknown.
- **GRDX (GRDX)**: In-window amendment(s), documented: 10-K/A 2025-04-09 accn 0001410578-25-000673. Zero Item 4.02 8-K in window — no non-reliance (Big-R) restatement is evidenced; amendment character little-r/administrative/unknown.
- **VLGEA (VLGEA)**: In-window amendment(s), documented: 10-K/A 2025-11-07 accn 0000103595-25-000017. Zero Item 4.02 8-K in window — no non-reliance (Big-R) restatement is evidenced; amendment character little-r/administrative/unknown.

### 3.6 (c) outside-window Item 4.02 documentation (PASS-with-note rows)

- **C07 (FORR)**: Zero Item 4.02 8-K in window (deterministic items-field screen over sealed submissions). Outside-window Item 4.02 filings exist in the registrant's history (documented, not a criterion event): 2007-03-05 accn 0000950135-07-001388; 2006-02-02 accn 0000950135-06-000437; 2006-01-31 accn 0000950135-06-000400.
- **C08 (GIS)**: Zero Item 4.02 8-K in window (deterministic items-field screen over sealed submissions). Outside-window Item 4.02 filings exist in the registrant's history (documented, not a criterion event): 2007-01-05 accn 0000897101-07-000052.
- **V05 (ARAY)**: Zero Item 4.02 8-K in window (deterministic items-field screen over sealed submissions). Outside-window Item 4.02 filings exist in the registrant's history (documented, not a criterion event): 2026-02-09 accn 0001437749-26-003515.
- **V16 (AMKR)**: Zero Item 4.02 8-K in window (deterministic items-field screen over sealed submissions). Outside-window Item 4.02 filings exist in the registrant's history (documented, not a criterion event): 2006-08-16 accn 0000950153-06-002213; 2005-06-06 accn 0000950153-05-001356; 2005-05-13 accn 0000950153-05-001130.
- **V18 (FORR)**: Zero Item 4.02 8-K in window (deterministic items-field screen over sealed submissions). Outside-window Item 4.02 filings exist in the registrant's history (documented, not a criterion event): 2007-03-05 accn 0000950135-07-001388; 2006-02-02 accn 0000950135-06-000437; 2006-01-31 accn 0000950135-06-000400.
- **V21 (GIS)**: Zero Item 4.02 8-K in window (deterministic items-field screen over sealed submissions). Outside-window Item 4.02 filings exist in the registrant's history (documented, not a criterion event): 2007-01-05 accn 0000897101-07-000052.
- **W03 (RGEN)**: Zero Item 4.02 8-K in window (deterministic items-field screen over sealed submissions). Outside-window Item 4.02 filings exist in the registrant's history (documented, not a criterion event): 2024-09-18 accn 0001193125-24-221406.
- **W08 (ADAM)**: Zero Item 4.02 8-K in window (deterministic items-field screen over sealed submissions). Outside-window Item 4.02 filings exist in the registrant's history (documented, not a criterion event): 2005-03-17 accn 0001273685-05-000012.
- **W15 (ULH)**: Zero Item 4.02 8-K in window (deterministic items-field screen over sealed submissions). Outside-window Item 4.02 filings exist in the registrant's history (documented, not a criterion event): 2026-03-09 accn 0001193125-26-098600.
- **W22 (RL)**: Zero Item 4.02 8-K in window (deterministic items-field screen over sealed submissions). Outside-window Item 4.02 filings exist in the registrant's history (documented, not a criterion event): 2005-06-10 accn 0000950142-05-001741.

### 3.7 (f) PASS-with-note rows (cases exist; no window intersection)

- **C05 (PERY)**: One SCAC case (id=106740, filed 2018-09-24): merger/proxy action over the June 2018 going-private transaction, voluntarily dismissed 2018-10-19; conduct entirely after window end 2017-08-09 — no intersection.
- **C06 (XLNX)**: One SCAC case (id=107614, filed 2021-01-15): AMD merger-consideration action, voluntarily dismissed 2021-03-10; conduct (October 2020 merger agreement) after window end 2017-09-10 — no intersection.
- **V01 (APD)**: Only SCAC entry is a 1997 stock-option plan case (id=101057, filed 1997-05-14) — class period ends before window start 2008-06-28; no intersection.
- **V04 (MASI)**: One SCAC case (id=108208, filed 2023-08-22, ONGOING): allegations concern FY2022-2023 forecasting; class period after window end 2015-07-28 — no intersection.
- **V05 (ARAY)**: One SCAC case (id=104339, filed 2009-07-22): class period necessarily ends by the filing date, before window start 2010-07-29 — no intersection.
- **V06 (MMSI)**: One SCAC case (id=107246, filed 2019-12-03, SETTLED): allegations concern 2019 integration disclosures; class period after window end 2015-07-28 — no intersection.
- **V08 (CIEN)**: One SCAC case (id=100276, filed 1998-08-26, DISMISSED 2000) — decades before window start 2010-08-07; no intersection.
- **V15 (FSLR)**: Two SCAC cases: id=104873 (filed 2012-03-15, SETTLED) — class period ends by filing date, before window start 2012-09-10; id=107868 (filed 2022-01-07, DISMISSED with prejudice at MTD 2023-06-23) — class period 2019-02-22 -> 2020-02-20 per registrant's FY2021 10-K (filed 2022-03-01), after window end 2017-09-10. No intersection either way.
- **V16 (AMKR)**: One SCAC case (id=103564, filed 2006-01-23) — class period ends before window start 2012-09-10; no intersection.
- **V17 (BHE)**: One SCAC case (id=101492, filed 1999-11-18) — before window start 2012-09-10; no intersection.
- **W02 (VAL)**: One SCAC case under successor name Valaris plc (id=107124, filed 2019-08-20, voluntarily dismissed 2021-08-13): allegations concern 2019 offshore-drilling disclosures; class period after window end 2013-02-28. Supplemental former-name search 'Ensco' returned no Ensco-registrant case page. No intersection.
- **W04 (IOVA)**: One SCAC case (id=108602, filed 2025-05-15, ONGOING): allegations concern FY2025 Amtagvi revenue guidance; class period after window end 2017-11-05 — no intersection.
- **W09 (LPSN)**: One SCAC case (id=108139, filed 2023-04-24, DISMISSED, final judgment 2025-03-19): allegations concern 2022 statements; class period after window end 2018-03-06 — no intersection.
- **W18 (AORT)**: Supplemental former-name search 'CryoLife' returns one case (id=102490, filed 2002-07-03) — class period ends before window start 2013-12-15; no intersection.
- **W20 (ATRC)**: Two SCAC cases (id=103697 filed 2006-12-11; id=104181 filed 2008-12-12) — class periods end before window start 2013-12-15; no intersection.
- **W21 (LEVI)**: Only SCAC entry is a 2003 bonds case (id=103005, filed 2003-12-12) — before window start 2016-11-02; no intersection.
- **VIASP (VIASP)**: SCAC fullsearch 'VIASP' and 'Via Renewables' returned zero case summary pages; former-name search 'Spark Energy' returned documents but zero case summary pages.
- **GRDX (GRDX)**: SCAC fullsearch for 'GRDX', 'GridAI Technologies', and former names 'Entero Therapeutics', 'First Wave BioPharma', 'AzurRx' returned zero case summary pages.
- **XPO (XPO)**: One SCAC case (id=106845, filed 2018-12-14) — class period ends by filing date, before window start 2023-02-05; no intersection.
- **SFM (SFM)**: Two SCAC cases (id=105777 filed 2016-03-24; id=106525 filed 2018-03-02) — class periods end before window start 2023-02-20; no intersection.

## 4. Disclosure

1. **FAIL findings exist.** 8 of 62 control rows (7 unique registrants) FAIL
   at least one v3 §1 criterion under this retrospective checklist:
   - **(f)** C02 (NUVA), C04+V10 (R), V11 (UPBD/Rent-A-Center), V20 (LQDT),
     W13 (FLO) — securities class actions with class periods intersecting the
     audit window that survived (in whole or in part) a motion to dismiss.
   - **(e)** GRDX (hc) — auditor resignation 8-K accompanied by a stated
     Item 304 disagreement.
   - **(d)** GO (hc) — material weakness not remediated by the next annual
     assessment (two consecutive adverse ICFR opinions).
   These are documented facts from public filings and court-docket records;
   none of these registrants carries an adverse enforcement label, and (a)
   passes for all 62. Per D106 common OUT this audit changes nothing: the
   verdicts are disclosure only.
2. **Published FPRs are conditional on the original selection criteria**
   (v1/v1.1/v2), which predate this checklist. The v3 §1 criteria were not
   part of any selection or scoring that produced published numbers; the
   FAIL/MINOR verdicts above do not recompute, requalify, or reweight any
   published FPR, and the original selection documents remain the historical
   record of how these controls were chosen.
3. **Holdout (hc) controls are provisional** until their (g) windows elapse
   (2028-02/03); their (a)–(f) verdicts here are interim and will be
   re-searched at window elapse per v3 §1(g). GO's (f) is additionally
   INCOMPLETE on its own terms (pending motion-to-dismiss ruling) and GRDX's
   (d) pending the FY2026 annual assessment.

A dated L-entry recording finding (1)–(2) has been appended to
`docs/methodology_limitations.md` (L-8) per v3 §4.

*채점: Claude 보조 + 인간 최종 확정. 본 문서는 특정 기업에 대한 부정적
라벨을 부여하지 않는다 — 기재된 것은 공시·법원 기록상의 사실이다. 포지션
없음 · 교육·정보 목적.*
