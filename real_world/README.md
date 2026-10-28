# The real-world test

The published runs test the pipeline, not the signal: none of the companies of
the universe had an accounting enforcement case (CLAUDE.md). This folder holds the
test that asks the other question: run the same pipeline on filings the SEC later
found misstated, filed before anyone said so, and on filings of companies in the
same industry that no restatement followed, and count how often the accounting
analysis flagged the accounts the SEC named.

The rule is `src/real_world_test.py`'s docstring, fixed before any run here
existed. Its tests are `tests/test_real_world_test.py`.

| file | what it is | who writes it |
|---|---|---|
| `cases.json` | the SEC's accounting and auditing enforcement releases used: company, CIK, misstated periods, the accounts the SEC's document names (each a quote copied from it), the day the problem became public, and the filings inside the window filed before that day | collected from the SEC's documents and EDGAR; `check` fetches every source again and refuses a case whose quote is not on its page |
| `controls.json` | one company per case, by the rule | `controls` |
| `plan.json` | every run: a case's latest candidate filing and its control's | `plan` |
| `runs/<label>/<accession>/` | the runs, through `src/on_demand.py` exactly as any run | `run` |
| `memory_probe.jsonl` | what the model says it remembers of each company, asked with no filing and no tool, verbatim | `probe` |
| `results.json` | the counts, by the rule, every run listed | `score` |

Nothing under `runs/`, `memory_probe.jsonl` or `results.json` is ever changed or
deleted once written; a correction is a new file and a line saying so, as under
the repository's `runs/`. An adverse count is printed as it comes.
