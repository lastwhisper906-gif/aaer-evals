# Next cycle tasks

This replaces the work ledger. Git and pull requests carry the state; this file
carries the list.

One line per item:

`[ ] title · builds · judge · expected value from · PR`

- **judge** is the command that decides pass or fail.
- **expected value from** is where the judge's numbers came from. It must name
  a source outside the code being built: the filing, the companyfacts JSON, a
  hand computation written into the test, or a value planted on purpose. If the
  honest answer is "a run of the thing this judges", the item is not ready.
- An item with no judge is **needs judgment**. It is never launched. The owner
  reads all of them in one sitting at the next rules version.

Build each item with the `build-item` skill, and brief every agent with the
`dispatch` skill. One worktree, one branch, one pull request per item, auto-merge
on the moment it opens.

The parsers on the branch `harness/cycle-020` — the numeric extractor, the note
extractor, the MD&A and controls splitters, the 8-K parser, the paragraph diff,
the note history, the trend table, the bundle assembler, the cutoff guard and
the extraction checks — land through their own pull request. Several items below
build on them and assume that has merged.

---

## Ready to build

[ ] write the plain-name check · `src/plain_name_check.py` and the post-write hook that calls it · `python3.12 -m pytest tests/test_plain_name_check.py -q` · a letter-number code planted in a fixture file by the test itself, and a filter output that is greped rather than a filter that is inspected — a no-op regular expression fails quietly · PR:

[ ] companyfacts fetcher · `src/fetch_companyfacts.py` and one `companyfacts.json` fixture per company, with its sha256 in the manifest · `python3.12 -m pytest tests/test_fetch_companyfacts.py -q` · every `us-gaap` numeric fact in the committed XBRL instance, looked up in companyfacts and matched by value, with every difference listed rather than tolerated · PR:

[ ] trend table on companyfacts · `src/trends.py` reading companyfacts instead of a single instance · `python3.12 -m pytest tests/test_trends.py -q` · each ratio computed by hand from the raw companyfacts JSON and written out in the test, 12 of 12 companies, 8 quarters and 5 years · PR:

[ ] fourth-quarter derivation and the dump indicator · `src/fourth_quarter.py` · `python3.12 -m pytest tests/test_fourth_quarter.py -q` · annual and nine-month figures read off the filings for three companies and subtracted by hand in the test · PR:

[ ] quiet-restatement trace · `src/restatement_trace.py` and the ledger line it writes · `python3.12 -m pytest tests/test_restatement_trace.py -q` · a duplicate-period value planted in a copy of the companyfacts fixture, whose planted difference is the expected output · PR:

[ ] articulation checks · `src/articulation.py` · `python3.12 -m pytest tests/test_articulation.py -q` · the cash-flow and balance-sheet lines for receivables, inventory and payables read off the statements of two companies and differenced by hand in the test · PR:

[ ] tag-continuity map · `src/tag_continuity.py` and the map as versioned data · `python3.12 -m pytest tests/test_tag_continuity.py -q` · the two tag names read off the two filings of a company whose revenue tag changed; the expected output is an unbroken series across the change · PR:

[ ] research-and-development-capitalized column · `src/trends.py` · `python3.12 -m pytest tests/test_trends_rnd.py -q` · research and development expense and capitalized development cost read off the filings of two companies and capitalized by hand in the test · PR:

[ ] formula baselines · `src/baselines.py` writing `baselines.json` — Beneish M-score, accruals over assets, net operating assets, Piotroski F-score, Ohlson O-score, Altman Z-score, note cosine similarity, Loughran and McDonald negative share · `python3.12 -m pytest tests/test_baselines.py -q` · each published formula applied by hand to the frozen fixture and written out term by term in the test; the word-list file's sha256 recorded in the manifest · PR:

[ ] Exhibit 21 fetch and diff · `src/exhibits.py` and `input_exhibits.md` · `python3.12 -m pytest tests/test_exhibits.py -q` · the exhibit type read from the submission's SGML header for 12 of 12 companies, never from the filename, plus one subsidiary planted in a copy of a fixture that the diff must report · PR:

[ ] Exhibit 10 fetch on trigger · `src/exhibits.py` · `python3.12 -m pytest tests/test_exhibits_on_trigger.py -q` · a fixture 8-K carrying item 1.01, whose submission index names the exhibit that must be pulled · PR:

[ ] Item 1A splitter and diff · `src/split_sections.py` and `input_risk_factors.md` · `python3.12 -m pytest tests/test_split_risk_factors.py -q` · the section boundaries located by hand in 12 of 12 filings, plus a fixture whose risk factors are reordered without edits, which must yield zero changes · PR:

[ ] diff alignment with a multiset and a boilerplate score · `src/diff_periods.py` · `python3.12 -m pytest tests/test_diff_alignment.py -q` · constructed fixtures — one reordered, one retitled, one with a table of a hundred identical cells — whose expected change count is zero by construction · PR:

[ ] market module · `src/market.py` writing `input_market.json` · `python3.12 -m pytest tests/test_market.py -q` · abnormal returns computed by hand from a frozen price fixture and written out in the test; an after-close acceptance time that must shift the window one day; a FINRA row that must attach by publication date and must not attach by settlement date · PR:

[ ] price-source delisting probe · a probe script and one line in `docs/structure_changes.md` · the probe run, exit status checked directly · a ticker known to have been delisted, whose history must come back; the source's own response is the expected value · PR:

[ ] per-agent input directory builder · `src/agent_inputs.py` · `python3.12 -m pytest tests/test_agent_inputs.py -q` · the layer table in `docs/INPUT_SPEC.md`, asserted file by file: a reader directory with no price file, a comparer directory with no filing, a supervisor directory with neither a filing nor the market table · PR:

[ ] quote and citation gate at every layer · `src/quote_gate.py` · `python3.12 -m pytest tests/test_quote_gate.py -q` · items planted on purpose — a quote with a changed dash, a quote with trimmed whitespace, a citation naming an id that does not exist — each of which must be dropped, and the drop count written into `input_manifest.json` · PR:

[ ] single-agent baseline runner · `src/control_single_agent.py` and the two control files · `python3.12 -m pytest tests/test_control_single_agent.py -q` · the output schema in `docs/CHECKLIST.md`, plus the quote gate, which must pass on the control's own output · PR:

[ ] shuffled-report control runner · `src/control_shuffled.py` and the two control files · `python3.12 -m pytest tests/test_control_shuffled.py -q` · a fixture pair of two companies' reports, where the expected output is that both files are written and that the numbers report and notes report in them came from different companies · PR:

[ ] scorecard template · `src/scorecard.py` and the template it renders · `python3.12 -m pytest tests/test_scorecard.py -q` · a fixture `runs/` directory; the expected output is a rendered scorecard with the Beneish M-score as the first accounting row and both caveat sentences present, with no hand edits anywhere in the path · PR:

[ ] monthly canary scheduled task · the task definition and its ledger line · one dry run, exit status checked directly · a defect planted on a branch on purpose; the expected result is that `refute-check` names it, and either a hit or a miss is appended to `events/ledger.jsonl` · PR:

---

## Needs judgment

Not launched. No judge exists for these, and inventing one would be inventing the
answer.

[ ] thresholds for the four new numeric indicators — `articulation_gap`, `asset_growth_high`, `rnd_capitalization_shift`, `net_stock_issuance` · a threshold is the owner's, and each of these needs the flag distribution over the 30 past cases before a number means anything · needs judgment

[ ] the two-by-two flag thresholds · the accounting flag count grew from 26 to 33 and the pressure count from 16 to 17 while "4 or more" and "3 or more" stayed put, which loosens both tiers · needs judgment

[ ] the map from SIC code to sector ETF · which ETF stands for which range of SIC codes is a modelling choice with no test that can settle it, and the abnormal return depends on it · needs judgment

[ ] the price source, if no free source retains delisted tickers · the probe item above answers whether one does; if none does, the choice is between a paid source, a narrower universe, and dropping the abnormal-return target · needs judgment

[ ] whether the review-response branch's published results merge into this history · two published-results histories diverge, and merging them is a claim about the record · needs judgment
