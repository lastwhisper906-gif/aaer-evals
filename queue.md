# Queue

The live work list. One line per item:

`[ ] what · eval command that must pass · depends on`

The nightly worker takes the first unchecked item whose dependencies are done, runs
`/goal <its eval command> exits 0 and the output is printed; no test or grader changed`,
and opens a pull request. Done items move to the bottom with their pull request
number. Claude may add items at the end; only the owner deletes or reorders them.
An item with no eval command is not an item: it goes to `docs/needs_judgment.md`.

`make eval` is the owner's grader over every run; `make eval-quick` grades the runs a
branch changed. A run item is done when its run directory is published and
`.venv/bin/python -m evals --runs <that directory>` exits 0.

## Open

[ ] new Fable runs for AAPL, GNRC and LFUS, each in `runs/<ticker>/<accession>-rerun-<date>/` · `.venv/bin/python -m evals --runs runs/AAPL runs/GNRC runs/LFUS` · items one to three

[ ] golden consistency runs: three runs of each approved golden case · `.venv/bin/python -m evals.capability.consistency` · the owner approving at least one case in `evals/golden/cases/`

[ ] new runs for the eight filings published on 2026-09-29 (AAPL, CARR, CIEN, CSCO, GNRC, LFUS, PANW, STX), each as a rerun directory · `.venv/bin/python -m evals --runs runs` · items one to three

[ ] the SessionStart hook runs `sh tools/session_start_lessons.sh` in place of `cat lessons.md`: a pull request of that one line in `.claude/settings.json`, a guarded path, merged with the owner's label `owner-approved-eval` · eval: `.venv/bin/python -m pytest tests/test_session_start_lessons.py tests/test_guards.py -q` passes and the guard job is green on the labeled run · depends on: the owner's label

[ ] the first CRSP fetch through WRDS: `.venv/bin/python -m src.probe_price_sources` prints a served crsp line with rows for Lehman Brothers Holdings (LEH, delisted 2008-09-17) carrying dlret · eval: `.venv/bin/python -m src.probe_price_sources` -- that command's crsp line reads served and the row count is printed · depends on: the owner's two environment steps (`docs/needs_judgment.md`, "CRSP through WRDS from the cloud session")

[ ] DELL's 10-Q filed 2026-09-08 on Fable · `.venv/bin/python -m evals --runs runs/DELL` · item one
    pending, 2026-10-14: the first run finished, readers on Opus and the three analysts on Fable with no fallback, regression 18 pass, 0 fail; not published, because the notes-text reader wrote the filer's fiscal years as a capital and two digits in one sentence, which the plain-name check names in four copies of its report and which a committed report is never renamed to pass (`docs/structure_changes.md`, 2026-09-23); that run is kept outside the tree, and the filing is extracted and run again into the same directory after the batch, as the four of 2026-10-08 were.
    2026-10-14, evening: a third attempt, on Opus, was stopped at the analysts once its notes-text reader had written the filer's fiscal years as a capital and two digits again; three of three attempts refused for the same reason, so the filing is not run again until the reader-prompt row in `docs/needs_judgment.md` is decided.

[ ] WDC's 10-Q filed 2026-05-01 on Fable · `.venv/bin/python -m evals --runs runs/WDC` · item one

[ ] POWL's 10-Q filed 2026-08-04 on Fable · `.venv/bin/python -m evals --runs runs/POWL` · item one

[ ] FELE's 10-Q filed 2026-07-29 on Fable · `.venv/bin/python -m evals --runs runs/FELE` · item one

[ ] FN's 10-Q filed 2026-05-05 on Fable · `.venv/bin/python -m evals --runs runs/FN` · item one

[ ] MSI's 10-Q filed 2026-08-05 on Fable · `.venv/bin/python -m evals --runs runs/MSI` · none

[ ] LITE's 10-Q filed 2026-05-06 on Fable · `.venv/bin/python -m evals --runs runs/LITE` · none

[ ] FLEX's 10-Q filed 2026-07-31 on Fable · `.venv/bin/python -m evals --runs runs/FLEX` · none

[ ] AVGO's 10-Q filed 2026-09-10 on Fable · `.venv/bin/python -m evals --runs runs/AVGO` · none

[ ] SMCI's 10-Q filed 2026-05-11 on Fable · `.venv/bin/python -m evals --runs runs/SMCI` · none

[ ] SNDK's 10-Q filed 2026-05-01 on Fable · `.venv/bin/python -m evals --runs runs/SNDK` · none

[ ] FFIV's 10-Q filed 2026-08-06 on Fable · `.venv/bin/python -m evals --runs runs/FFIV` · none

[ ] WDC's 10-K filed 2026-08-14 on Fable, the default in force for the five whose fixture 8-K postdates their fixture 10-Q (`docs/needs_judgment.md`) · `.venv/bin/python -m evals --runs runs/WDC` · none

[ ] FN's 10-K filed 2026-08-18 on Fable, the same default · `.venv/bin/python -m evals --runs runs/FN` · none

[ ] LITE's 10-K filed 2026-08-17 on Fable, the same default · `.venv/bin/python -m evals --runs runs/LITE` · none

[ ] SMCI's 10-K filed 2026-08-31 on Fable, the same default · `.venv/bin/python -m evals --runs runs/SMCI` · none

[ ] SNDK's 10-K filed 2026-08-17 on Fable, the same default · `.venv/bin/python -m evals --runs runs/SNDK` · none

[ ] UI, Ubiquiti, joins `universe.json` with the fixture set and expected values fetched and written on 2026-10-14 (kept outside the tree, `docs/structure_changes.md`), once the same-day 8-K row in `docs/needs_judgment.md` is decided · `.venv/bin/python -m pytest tests -q -k "UI"` passes with every defect a strict expected failure · the owner's decision on that row

[ ] NSSC, Napco Security Technologies, joins `universe.json` the same way, once the three-gap row in `docs/needs_judgment.md` is decided · `.venv/bin/python -m pytest tests -q -k "NSSC"` passes with every defect a strict expected failure · the owner's decision on that row

[ ] CLS, Celestica, joins `universe.json` the same way, once the Exhibit 21 and IFRS row in `docs/needs_judgment.md` is decided · `.venv/bin/python -m pytest tests -q -k "CLS"` passes with every defect a strict expected failure · the owner's decision on that row

[ ] MU, Micron Technology, the reading's pick under 3674 (`docs/structure_changes.md`, 2026-10-14): fixtures as of the day it is fetched, the two 10-K headers and Exhibit 21 documents by hand, expected values with the 43 keys, and its row · `.venv/bin/python -m pytest tests -q -k "MU"` passes with every defect a strict expected failure · none

## Done

[x] JCI's 10-Q filed 2026-07-29 on Fable · `.venv/bin/python -m evals --runs runs/JCI` · item one · 2026-10-14: run on Opus by the owner's decision of the evening (`--model opus`, recorded as `model_override` in the manifest; every agent served claude-opus-5-5, no fallback); regression 18 pass, 0 fail; analysis-grader 0.848 with 2 dealbreakers, the grader's stated score differing from the rubric's formula as the open row records; earlier attempts on Fable stopped at the session limit and at the plain-name check and were set aside, and the filing was extracted again for this run · PR: this one

[x] LOGI's 10-Q filed 2026-07-29 on Fable · `.venv/bin/python -m evals --runs runs/LOGI` · none · 2026-10-14: run on Opus by the owner's decision of the evening (`--model opus`, recorded as `model_override` in the manifest; every agent served claude-opus-5-5, no fallback); regression 18 pass, 0 fail; analysis-grader 0.933 with 0 dealbreakers, the grader's stated score differing from the rubric's formula as the open row records; two earlier attempts were set aside, one stopped at the readers by the limit and one refused by the plain-name check, and the filing was extracted again for this run · PR: this one

[x] FTNT's 10-Q filed 2026-07-30 on Fable · `.venv/bin/python -m evals --runs runs/FTNT` · item one · 2026-10-14: regression 18 pass, 0 fail; the analysts served by claude-fable-5-1, no fallback, the readers on Opus, as their definitions say (it ran before the owner's decision of the evening that every run is on Opus); analysis-grader 0.779 with 5 dealbreakers, the grader's stated score differing from the rubric's formula as the open row records; a first attempt stopped at the valuation analyst when the Fable session limit was reached and was set aside, and the filing was extracted again for this run · PR: this one

[x] ANET's 10-Q filed 2026-08-05 on Fable · `.venv/bin/python -m evals --runs runs/ANET` · item one · 2026-10-14: regression 18 pass, 0 fail; the analysts served by claude-fable-5-1, no fallback; the readers on Opus, as their definitions say; analysis-grader 0.917 with 0 dealbreakers, the grader's stated score differing from the rubric's formula as the open row in `docs/needs_judgment.md` records; extracted by hand the same day, the store fetched up to the filing · PR: this one

[x] the store fetch reads a submission header EDGAR does not publish out of the complete submission text file: `src/fetch_fixtures.document_types` and the header documents the store records fall back, on a 404 of `{accession}-index-headers.html`, to `{accession}.txt`, whose SGML header carries the same `<TYPE>` and `<FILENAME>` blocks, so the 10-Ks and 10-Qs of 2009 to 2013 collect · `.venv/bin/python -m pytest tests/test_fetch_fixtures.py -q -k header_fallback` passes on a planted header whose (type, filename) pairs are read by eye off the filing index page of QCOM's 10-Q 0001234452-13-000292 (six documents, `qcom6301310-q.htm` first) and never off the parser · none · 2026-10-14: done on this branch, with the second gap the same filings showed once the header was read, the instance named `{stem}.xml` beside its `.xsd` before inline XBRL; `tests/test_fetch_fixtures.py` 35 passed, the judge's `-k` reading six of them; the first batch after built FN's and WDC's 10-Qs of May 2014 · PR: this one

[x] NVDA's 10-Q filed 2026-08-26 on Fable · `.venv/bin/python -m evals --runs runs/NVDA` · item one · 2026-10-08: regression 18 pass, 0 fail; the analysts served by claude-fable-5-1, no fallback; the readers on Opus, as their definitions say; analysis-grader 0.69 with 20 dealbreakers; the run the graders refused on 2026-10-07 is not published, and this one ran after the gates were held to the graders (#125) · PR: this one

[x] QCOM's 10-Q filed 2026-07-29 on Fable · `.venv/bin/python -m evals --runs runs/QCOM` · item one · 2026-10-08: regression 18 pass, 0 fail; the analysts served by claude-fable-5-1, no fallback; the readers on Opus, as their definitions say; analysis-grader 0.893 with 6 dealbreakers; the run the graders refused on 2026-10-07 is not published, and this one ran after the gates were held to the graders (#125) · PR: this one

[x] ESE's 10-Q filed 2026-08-10 on Fable · `.venv/bin/python -m evals --runs runs/ESE` · item one · 2026-10-08: regression 18 pass, 0 fail; the analysts served by claude-fable-5-1, no fallback; the readers on Opus, as their definitions say; analysis-grader 0.93125 with 4 dealbreakers; the run the graders refused on 2026-10-07 is not published, and this one ran after the gates were held to the graders (#125) · PR: this one

[x] TTMI's 10-Q filed 2026-08-05 on Fable · `.venv/bin/python -m evals --runs runs/TTMI` · item one · 2026-10-08: regression 18 pass, 0 fail; the analysts served by claude-fable-5-1, no fallback; the readers on Opus, as their definitions say; analysis-grader 0.851 with 7 dealbreakers; the run the graders refused on 2026-10-07 is not published, and this one ran after the gates were held to the graders (#125) · PR: this one

[x] `data/notes-and-calendar`: merge the code (`src/event_calendar.py`, `src/fsn.py` and their tests), download nothing; the bulk-data location is a row in `docs/needs_judgment.md` · `.venv/bin/python -m pytest tests/test_event_calendar.py tests/test_fsn.py -q` · none · 2026-10-07: 67 passed, also with every proxy variable at a closed port and every socket connection refused; nothing was downloaded and no `make fetch` ran; the five needs-judgment rows are in the Open list; one test had started failing by the calendar date (a daily index not read stood for the week before it was written) and `read_through` now skips such a line; `src/fsn_index/`, which the rows and `make fetch` name, was never committed on the branch, so `make fetch` has nothing to fetch until the index is built again · 2026-10-08, after main's #123 was merged in and the three lenses read the merge: 79 passed, also with every proxy variable at a closed port and every socket connection refused (no connection attempted); with no index line `make fetch` now stops at once and says so (run once, with a scratch home and the proxy at a closed port: the first step exited 1 and nothing was written or downloaded), and the storage row says the index was never committed and what comes before `make fetch`; `load` and the calendar's bulk read write nothing before their floor checks; a zip whose size is not stated is not downloaded; the counts key is `the_universe`; each of these changes and the read-through fix has a test the branch's code fails, and the download path, which had none, has tests; the loader's tests fail rather than skip without duckdb · PR: this one

[x] the manifest records the triggering filing's EDGAR acceptance stamp, Eastern, no Z: the fetch projects `acceptanceDateTime` onto the submissions rows and the manifest document rows (the two field tuples in `src/fetch_fixtures.py` and `submissions_record`), `src/assemble_bundle.py` writes it beside `filing_date`, and the hand-written `acceptance_datetime` on NVDA's 10-Q row in `tests/fixtures/NVDA/submissions.json` is then the fetcher's · eval: `python -m evals --runs <run>` passes nothing_after_cutoff on a run with a market table · depends on: nothing · 2026-10-07: the index's Z is universal time, not decoration (NVDA's committed 10-K headers against the index's rows for the same accessions, `docs/needs_judgment.md`), so the fetch converts the stamp rather than dropping the letter; NVDA's hand-written value is the constant `NVDA_ACCEPTED` in `tests/test_run_analysis.py`, not a field of the hash-held fixture, and stays as written; the eval is shown on a planted run, since no published run has a market table · PR: this one

[x] DCF sanity: a free-cash-flow-yield cross-check, a WACC components table, and reverse-DCF growth beside three- and five-year revenue history, in `calculator.json` and the memo, each with a hand-worked test · `.venv/bin/python -m pytest tests/test_calculator.py tests/test_analysis_check.py -q -k "free_cash_flow_yield or wacc_components or growth_beside_history"` · none · PR: this one

[x] the memo names a cost-of-debt fallback where calculator.json labels one (`pre_tax_cost_of_debt.fallback`), in the finance frame's valuation section (created and done in this change) · `.venv/bin/python -m pytest tests/test_analysis_check.py -q -k cost_of_debt_fallback` · items one and three · PR: this one

[x] the comparers become Python: `src/market_labels.py` labels each item priced_in, not_priced or opposite_direction from the sign of the abnormal return in each reaction window against the item's expected direction, plus short interest above its two-year median; `notes-vs-market` and `numbers-vs-market` move to `archive/agents/` · `.venv/bin/python -m pytest tests/test_market_labels.py tests/test_agent_inputs.py -q` · none · PR: #107 (the row was left open when it merged; its eval command passes on main, 112 passed)

[x] valuation failures: AAPL's pre-tax cost of debt falls back to interest paid (`InterestPaidNet`) over average debt, then to the risk-free rate plus one point, labelled `fallback`; GNRC's and LFUS's scenarios stop being dropped for a bare year in a driver's reason (their `assumptions.json` `dropped_items`: "a number written in the analyst's own words" on "the second half of 2026", "through 2027"), which is the analysis gate's year rule, not a field mismatch · `.venv/bin/python -m pytest tests/test_calculator.py tests/test_analysis_check.py -q --runxfail -k "interest_paid or risk_free_fallback or bare_year or published_scenarios"` · none · 2026-10-07: the cost-of-debt ladder is in; the year rule reads a year after "margin of", "margins of", "growth of", "surge of" and the elided "and of" that continues one ("the margin of 2023", "the growth of 2021 and 2022", "the margin of the year before last and of 2022"), a range opening with a fiscal year ("fiscal 2022 to 2025"), "was" after a subject that is a year ("the only fiscal year in the record that grew faster was 2021 at"), a hyphenated adjective followed by a word that cannot be its noun ("the second half of 2025 loss-making recur"), "peak" after a year and "once" and "earned" after one, while "inventory of 2048", "fiscal 2022 to 2048 units", "the headcount was 2048" and "sold in 2048 high-margin units" stay counts; LFUS's, GNRC's and AAPL's scenarios pass the gate whole. Of the 91 items in `tests/test_analysis_check.py`, 57 pass whole, 6 carry a figure and are dropped rightly, 28 are years the rule still cannot tell from a count and stay `xfail(strict=True)` with the reason each · PR: this one

[x] the nightly crew: collects newest first; writes its ledger line to main through an auto-merging pull request instead of a `nightly/*` branch; reads the `TIINGO_TOKEN` secret; and `lessons.md` records why the 2006–2011 filings answered 404 · `.venv/bin/python -m pytest tests/test_nightly.py tests/test_collect_history.py -q` · none · PR: this one
