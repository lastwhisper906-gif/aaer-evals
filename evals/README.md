# evals/ — the owner's graders

This directory is the owner's. Claude reads it and never writes it. A pull request
that touches it cannot merge without the label `owner-approved-eval`, which only the
owner adds. Appending lines to `scoreboard.jsonl` is the one exception: `make eval`
does that.

The graders read **run directories** (`runs/<ticker>/<run>/`): what a run published,
never how an agent got there. `tests/` keeps grading the code; `evals/` grades the
outputs.

    make eval          every run: regression and capability; appends one line to scoreboard.jsonl
    make eval-quick    regression on the runs this branch changed; under two minutes
    .venv/bin/python -m evals --runs runs/NVDA     the runs under a path

`make eval` exits non-zero on any regression failure, or on a capability score below
a floor in `thresholds.json`. CI runs it with **main's copy of evals/**, so a branch
is always graded by the owner's current graders.

## Regression: must stay at 100%; any failure blocks a merge

`regression/mechanical.py`, per run:

| check | what it asks |
|---|---|
| files_present | the run published its manifest, the calculator files, the three analyses, both reader reports and the memo |
| agents_written | every agent the manifest lists wrote its file, and no analysis failure is recorded |
| quotes_resolve | every quote a report or an analysis kept is, character for character after the whitespace fold, in the files that agent was handed |
| cited_numbers_exist | every `{path}` an analysis writes, and every `fields` entry, names a field of the calculator file that analyst saw |
| nothing_after_cutoff | no input document, calculator fact or market date is after the run's cutoff |
| calculator_finite | every numeric value in calculator.json is finite |
| dcf_recomputes | each scenario's enterprise value and value a share, and the simple free cash flow, recompute from the run's own drivers with this file's own arithmetic |

Also, once per `make eval`, two hand-worked cases, Gordon and fade (`hand_worked_*`). Both the grader's own arithmetic and `src/calculator.py` must reproduce them:
- **Gordon:** 92.7 / (0.09 − 0.03) = 1,545, or 140 a share.
- **Fade:** 12% fading to 3% gives 2,240.8020, or 209.5802 a share.

`regression/coverage.py`, per run:

| check | what it asks |
|---|---|
| accounting_areas | each of the seven areas and the industry lens has a finding ("nothing found, because" counts), or the gate's note on why it was dropped |
| financial_sections | profitability, efficiency, liquidity, solvency, growth and DuPont, the same way |
| valuation_answer | a value range, or the calculator's stated reason there is none; the market-implied growth, or its reason; the revenue history beside it |
| memo_frames | the memo has a 회계 section and a 재무 section |
| forbidden_words | **Everywhere:** no fraud or manipulation (or 분식, 회계부정, 조작). **In the valuation, its assumptions and the memo:** no buy, sell or alpha, and no 매수 or 매도 followed by 추천, 의견 or 권. In the accounting and financial analyses, "buy" and "sell" describe what a company does, as the analysis gate has allowed since #101. |
| no_combined_score | no field named score, composite, rank or overall in any analysis |

A dropped area passes regression, because the record says what was dropped and why;
an area that is simply absent fails it. How many areas were *answered* is capability.

## Capability: tracked; gated only where thresholds.json sets a floor

| grader | what it measures |
|---|---|
| coverage rates | the share of accounting areas and financial sections answered rather than dropped; value range computed; implied growth beside three- and five-year history |
| golden.py | **Against approved golden cases: found, missed and extra.** An item counts as found when an anomaly in the case's frame reaches one of its filing paragraphs, or uses every word of one of its keywords. The score per run is (found − extra) ÷ must_find. |
| rubric.md + analysis-grader | Opus reads one run and the rubric and writes `grade.json`. Dealbreakers score zero; other items are weighted by severity. The score is reported and never gated until grader agreement passes the owner's floor. |
| grader_agreement.py | on golden filings, how often the analysis-grader's verdict on an anomaly matches the owner's case |
| consistency.py | golden filings run three times: overlap of the anomaly sets and spread of the value range (pass^k) |
| outcomes.py | runs at least 60 trading days old: anomalies by frame, events after the cutoff, and the abnormal return when a price series is committed; younger runs are "pending" |
| memorization.py | forward runs (filed after every serving model's training cutoff) are clean; the others need an anonymized re-run probe, reported beside the score; a model with no cutoff on record is "unknown" |

## Golden cases

- `golden/TEMPLATE.yaml` is the shape of a case: filing, frame, `must_find` (area, what, the filing paragraph ids or keywords that count), `must_not_claim`, and `approved_by_owner: false`.
- `golden/drafts/` is where Claude may propose cases. Drafts are never counted.
- `golden/cases/` holds the owner's approved cases, the only ones counted.

To approve a draft, the owner:
1. checks every claim and paragraph id against the filing (each draft lists what to check);
2. corrects it;
3. sets `approved_by_owner: true`;
4. moves it into `cases/`, in a pull request labelled `owner-approved-eval`.

The three seed drafts were written from the runs published on 2026-09-29, so they match those runs by construction. Until the owner checks them against the filings, they say nothing about the analysts.

**Size target.** 20 to 50 approved cases over time. Each real miss or false alarm the
owner notices becomes a new draft. The weekly gardener lists candidates from the
week's runs.

## Files

- `thresholds.json`: the owner's floors, as `{"capability": {"golden": 0.6, ...}}` keyed by the score names `make eval` prints. Empty means report-only.
- `scoreboard.jsonl`: one line per `make eval`, holding the date, the commit, the runs and every score. Append-only.
