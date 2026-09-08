# aaer-evals

Reads the filings of twelve companies, compares them with the market, predicts
two questions about each, and leaves a verifiable record.

The twelve: AAPL · STX · CSCO · PANW · CARR · LFUS · GNRC · CIEN · QCOM · ESE ·
TTMI · NVDA.

The two questions, kept separate:

- **accounting reliability** — do these numbers reflect reality?
- **financial pressure** — is this company under pressure?

When one of the twelve files a report, the pipeline pulls the numbers, the notes,
MD&A, the auditor's report, the exhibits and the 8-Ks from EDGAR, and hands them
to three layers that never see each other's inputs: two readers see the filing,
two comparers see the readers' reports next to a market table, and two
supervisors see only reports. It publishes a dated prediction per question.
Nothing published is edited afterwards.

This is forward prediction, so there is nothing to anonymize and nothing to
perturb. It is also an honest-negative test: accounting-reliability events will
barely occur in twelve large filers in year one, and a pipeline that says "clear"
when things are clear is the result being tested.

## Where things are

| Path | What |
|---|---|
| `docs/INPUT_SPEC.md` | what we fetch, and what the predictor is allowed to see |
| `docs/CHECKLIST.md` | what we look at, what we try to get right, how we score it |
| `docs/HOW_WE_WORK.md` | the pipeline, the routines, the loop, which model does what |
| `docs/next_cycle_tasks.md` | the task list — what is built next, and what needs judgment |
| `.claude/` | the agent definitions, the two skills and the hooks that make up the loop |
| `rules/` | the frozen, versioned checklist, targets and thresholds (`docs/rules.md`) |
| `runs/` | one directory per prediction — inputs and outputs, append-only (`docs/runs.md`) |
| `events/ledger.jsonl` | what actually happened, append-only |
| `src/` | parsers, extraction, prediction, scoring |
| `tests/fixtures/` | the filings the parsers are judged against — one 10-K, 10-Q and 8-K 2.02 per company, with the sha256 of every file as EDGAR served it |
| `archive/` | the earlier experiment, frozen at tag `archive-v1` |

## Running the checks

```sh
pip install -r requirements.txt
make check
```

`make check` is `src/append_check.py` followed by pytest. The append check fails
if the branch changes or deletes existing content under `runs/`, `rules/` or
`events/`; appending to the end of a ledger file passes.

Both run on Python 3.12 and refuse to run on anything else — a gate result from
another interpreter is not worth producing.

## The earlier experiment

`archive/` holds a ten-month experiment that asked whether an LLM could separate
past SEC enforcement cases from matched controls using roughly sixty numeric
XBRL tags and the filing index. It reached AUC ≈ 0.83 with 71% false positives,
and the scores moved when company names were hidden. Its notes and MD&A were
never read — zero bytes. Its own results documents are in
`archive/RESULTS.md`, and its gates were green at tag `archive-v1` on Python
3.12. It is kept as written and is not maintained.

## Scope and disclaimer

Educational and informational. No position is held in any company named here.
Nothing in this repository is an allegation of wrongdoing against any current
company; the checklist reports indicators and hypotheses, and it says so
wherever it reports them.
