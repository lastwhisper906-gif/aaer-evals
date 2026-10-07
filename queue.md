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

[ ] NVDA's 10-Q filed 2026-08-26 on Fable · `.venv/bin/python -m evals --runs runs/NVDA` · item one

[ ] QCOM's 10-Q filed 2026-07-29 on Fable · `.venv/bin/python -m evals --runs runs/QCOM` · item one

[ ] ESE's 10-Q filed 2026-08-10 on Fable · `.venv/bin/python -m evals --runs runs/ESE` · item one

[ ] TTMI's 10-Q filed 2026-08-05 on Fable · `.venv/bin/python -m evals --runs runs/TTMI` · item one

[ ] `data/notes-and-calendar`: merge the code (`src/event_calendar.py`, `src/fsn.py` and their tests), download nothing; the bulk-data location is a row in `docs/needs_judgment.md` · `.venv/bin/python -m pytest tests/test_event_calendar.py tests/test_fsn.py -q` · none

[ ] golden consistency runs: three runs of each approved golden case · `.venv/bin/python -m evals.capability.consistency` · the owner approving at least one case in `evals/golden/cases/`

[ ] new runs for the eight filings published on 2026-09-29 (AAPL, CARR, CIEN, CSCO, GNRC, LFUS, PANW, STX), each as a rerun directory · `.venv/bin/python -m evals --runs runs` · items one to three

[ ] the SessionStart hook runs `sh tools/session_start_lessons.sh` in place of `cat lessons.md`: a pull request of that one line in `.claude/settings.json`, a guarded path, merged with the owner's label `owner-approved-eval` · eval: `.venv/bin/python -m pytest tests/test_session_start_lessons.py tests/test_guards.py -q` passes and the guard job is green on the labeled run · depends on: the owner's label

[ ] the first CRSP fetch through WRDS: `.venv/bin/python -m src.probe_price_sources` prints a served crsp line with rows for Lehman Brothers Holdings (LEH, delisted 2008-09-17) carrying dlret · eval: `.venv/bin/python -m src.probe_price_sources` -- that command's crsp line reads served and the row count is printed · depends on: the owner's two environment steps (`docs/needs_judgment.md`, "CRSP through WRDS from the cloud session")

[ ] DELL's 10-Q filed 2026-09-08 on Fable · `.venv/bin/python -m evals --runs runs/DELL` · item one

[ ] WDC's 10-Q filed 2026-05-01 on Fable · `.venv/bin/python -m evals --runs runs/WDC` · item one

[ ] ANET's 10-Q filed 2026-08-05 on Fable · `.venv/bin/python -m evals --runs runs/ANET` · item one

[ ] FTNT's 10-Q filed 2026-07-30 on Fable · `.venv/bin/python -m evals --runs runs/FTNT` · item one

[ ] JCI's 10-Q filed 2026-07-29 on Fable · `.venv/bin/python -m evals --runs runs/JCI` · item one

[ ] POWL's 10-Q filed 2026-08-04 on Fable · `.venv/bin/python -m evals --runs runs/POWL` · item one

[ ] FELE's 10-Q filed 2026-07-29 on Fable · `.venv/bin/python -m evals --runs runs/FELE` · item one

[ ] FN's 10-Q filed 2026-05-05 on Fable · `.venv/bin/python -m evals --runs runs/FN` · item one

[ ] MSI's 10-Q filed 2026-08-05 on Fable · `.venv/bin/python -m evals --runs runs/MSI` · none

[ ] LITE's 10-Q filed 2026-05-06 on Fable · `.venv/bin/python -m evals --runs runs/LITE` · none

[ ] FLEX's 10-Q filed 2026-07-31 on Fable · `.venv/bin/python -m evals --runs runs/FLEX` · none

[ ] AVGO's 10-Q filed 2026-09-10 on Fable · `.venv/bin/python -m evals --runs runs/AVGO` · none

[ ] SMCI's 10-Q filed 2026-05-11 on Fable · `.venv/bin/python -m evals --runs runs/SMCI` · none

[ ] SNDK's 10-Q filed 2026-05-01 on Fable · `.venv/bin/python -m evals --runs runs/SNDK` · none

## Done

[x] the manifest records the triggering filing's EDGAR acceptance stamp, Eastern, no Z: the fetch projects `acceptanceDateTime` onto the submissions rows and the manifest document rows (the two field tuples in `src/fetch_fixtures.py` and `submissions_record`), `src/assemble_bundle.py` writes it beside `filing_date`, and the hand-written `acceptance_datetime` on NVDA's 10-Q row in `tests/fixtures/NVDA/submissions.json` is then the fetcher's · eval: `python -m evals --runs <run>` passes nothing_after_cutoff on a run with a market table · depends on: nothing · 2026-10-07: the index's Z is universal time, not decoration (NVDA's committed 10-K headers against the index's rows for the same accessions, `docs/needs_judgment.md`), so the fetch converts the stamp rather than dropping the letter; NVDA's hand-written value is the constant `NVDA_ACCEPTED` in `tests/test_run_analysis.py`, not a field of the hash-held fixture, and stays as written; the eval is shown on a planted run, since no published run has a market table · PR: this one

[x] DCF sanity: a free-cash-flow-yield cross-check, a WACC components table, and reverse-DCF growth beside three- and five-year revenue history, in `calculator.json` and the memo, each with a hand-worked test · `.venv/bin/python -m pytest tests/test_calculator.py tests/test_analysis_check.py -q -k "free_cash_flow_yield or wacc_components or growth_beside_history"` · none · PR: this one

[x] the memo names a cost-of-debt fallback where calculator.json labels one (`pre_tax_cost_of_debt.fallback`), in the finance frame's valuation section (created and done in this change) · `.venv/bin/python -m pytest tests/test_analysis_check.py -q -k cost_of_debt_fallback` · items one and three · PR: this one

[x] the comparers become Python: `src/market_labels.py` labels each item priced_in, not_priced or opposite_direction from the sign of the abnormal return in each reaction window against the item's expected direction, plus short interest above its two-year median; `notes-vs-market` and `numbers-vs-market` move to `archive/agents/` · `.venv/bin/python -m pytest tests/test_market_labels.py tests/test_agent_inputs.py -q` · none · PR: #107 (the row was left open when it merged; its eval command passes on main, 112 passed)

[x] valuation failures: AAPL's pre-tax cost of debt falls back to interest paid (`InterestPaidNet`) over average debt, then to the risk-free rate plus one point, labelled `fallback`; GNRC's and LFUS's scenarios stop being dropped for a bare year in a driver's reason (their `assumptions.json` `dropped_items`: "a number written in the analyst's own words" on "the second half of 2026", "through 2027"), which is the analysis gate's year rule, not a field mismatch · `.venv/bin/python -m pytest tests/test_calculator.py tests/test_analysis_check.py -q --runxfail -k "interest_paid or risk_free_fallback or bare_year or published_scenarios"` · none · 2026-10-07: the cost-of-debt ladder is in; the year rule reads a year after "margin of", "margins of", "growth of", "surge of" and the elided "and of" that continues one ("the margin of 2023", "the growth of 2021 and 2022", "the margin of the year before last and of 2022"), a range opening with a fiscal year ("fiscal 2022 to 2025"), "was" after a subject that is a year ("the only fiscal year in the record that grew faster was 2021 at"), a hyphenated adjective followed by a word that cannot be its noun ("the second half of 2025 loss-making recur"), "peak" after a year and "once" and "earned" after one, while "inventory of 2048", "fiscal 2022 to 2048 units", "the headcount was 2048" and "sold in 2048 high-margin units" stay counts; LFUS's, GNRC's and AAPL's scenarios pass the gate whole. Of the 91 items in `tests/test_analysis_check.py`, 57 pass whole, 6 carry a figure and are dropped rightly, 28 are years the rule still cannot tell from a count and stay `xfail(strict=True)` with the reason each · PR: this one

[x] the nightly crew: collects newest first; writes its ledger line to main through an auto-merging pull request instead of a `nightly/*` branch; reads the `TIINGO_TOKEN` secret; and `lessons.md` records why the 2006–2011 filings answered 404 · `.venv/bin/python -m pytest tests/test_nightly.py tests/test_collect_history.py -q` · none · PR: this one
