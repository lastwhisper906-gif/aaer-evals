This file is the scorecard's words. `src/scorecard.py` supplies the numbers and
nothing else, so a sentence that appears on the rendered page is a sentence
somebody wrote here, and a number that appears there was computed from a run.
Blocks are separated by a `=== name ===` line; `$slots` are filled in.

=== page ===
# Scorecard

Every number on this page was computed from the run directories listed at the
foot of it. Nothing here was typed in by hand, and nothing is rounded in the
direction that flatters a result.

One target is scored: the probability that the 60-trading-day abnormal return
from the third trading day after the filing is positive, under each question
separately and never merged. It is scored by Brier and by direction hit rate,
with the count of insufficient answers beside them. Every other target in
`docs/CHECKLIST.md` waits for its horizon to expire, and is absent here rather
than estimated.

A lower Brier is better and a higher hit rate is better. A row with no answer in
the runs says so and carries no number.

## Accounting reliability

| Row | Computed by | Side of the rules-version freeze | Runs | Brier | Direction hit rate | Insufficient |
|---|---|---|---|---|---|---|
$accounting_rows

> Post-2006 drift is close to zero outside small capitalizations (Martineau
> 2022). A coin-flip direction score on these twelve is the expected result, not
> a failure. The drift that survives is what the 8-K day did not price and the
> 10-Q later disclosed, which is exactly the window this pipeline reads.

> Published anomalies lose roughly 58% of their margin after publication (McLean
> and Pontiff 2016). Any margin over a baseline that was measured on past cases
> is reported next to the sentence "expect about half of this forward".

$accounting_verdicts

## Financial pressure

| Row | Computed by | Side of the rules-version freeze | Runs | Brier | Direction hit rate | Insufficient |
|---|---|---|---|---|---|---|
$pressure_rows

> Post-2006 drift is close to zero outside small capitalizations (Martineau
> 2022). A coin-flip direction score on these twelve is the expected result, not
> a failure. The drift that survives is what the 8-K day did not price and the
> 10-Q later disclosed, which is exactly the window this pipeline reads.

> Published anomalies lose roughly 58% of their margin after publication (McLean
> and Pontiff 2016). Any margin over a baseline that was measured on past cases
> is reported next to the sentence "expect about half of this forward".

$pressure_verdicts

## The runs this was computed from

$run_list

=== row ===
| $row | $computed_by | $side | $runs | $brier | $hit_rate | $insufficient |

=== side_pilot ===
pilot · pipeline check

=== side_forward ===
forward cycle · a result

=== insufficient_of ===
$insufficient of $answers

=== no_answer ===
not on record

=== not_scored ===
no answer to score

=== pipeline_beats_the_first_row ===
$side — the pipeline's Brier of $pipeline (scored on $pipeline_runs) beats the Beneish M-score's $other (scored on $other_runs).

=== pipeline_misses_the_first_row ===
$side — the pipeline's Brier of $pipeline (scored on $pipeline_runs) does not beat the Beneish M-score's $other (scored on $other_runs). The structure adds nothing.

=== pipeline_beats_the_single_agent ===
$side — the pipeline's Brier of $pipeline (scored on $pipeline_runs) beats the single-agent control's $other (scored on $other_runs).

=== pipeline_misses_the_single_agent ===
$side — the pipeline's Brier of $pipeline (scored on $pipeline_runs) does not beat the single-agent control's $other (scored on $other_runs). The structure is decoration.

=== no_verdict ===
Nothing to compare yet: no side of the freeze carries both a pipeline number and a baseline number.

=== run_entry ===
- $ticker $accession · filed $filing_date · rules version $rules_version frozen $rules_version_frozen · $side · 60-trading-day abnormal return $abnormal_return

=== no_runs ===
No run has left an outcome on record, so every row above is empty.
