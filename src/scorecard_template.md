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

The table scores each row over every run that row answered. The sentences under
it are comparisons, and a comparison is made only on the runs both of its rows
answered, so a Brier quoted in a sentence can differ from the same row's Brier in
the table above it. That is not a contradiction and it is not a rounding:
scoring a row that declined a run against a row that answered it would credit
the declining row for the run it left out. Each sentence says how many runs it
was made on and how many of that side's runs it set aside, and the two add up to
everything that side had to score.

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
$side — on the $runs runs both rows answered, with the side's other $set_aside set aside because one row or both put no probability on them, the pipeline's Brier of $pipeline beats the Beneish M-score's $other.

=== pipeline_misses_the_first_row ===
$side — on the $runs runs both rows answered, with the side's other $set_aside set aside because one row or both put no probability on them, the pipeline's Brier of $pipeline does not beat the Beneish M-score's $other. The structure adds nothing.

=== pipeline_beats_the_single_agent ===
$side — on the $runs runs both rows answered, with the side's other $set_aside set aside because one row or both put no probability on them, the pipeline's Brier of $pipeline beats the single-agent control's $other.

=== pipeline_misses_the_single_agent ===
$side — on the $runs runs both rows answered, with the side's other $set_aside set aside because one row or both put no probability on them, the pipeline's Brier of $pipeline does not beat the single-agent control's $other. The structure is decoration.

=== no_verdict ===
Nothing to compare yet: no side of the freeze carries a run that both a pipeline row and a baseline row answered.

=== run_entry ===
- $ticker $accession · filed $filing_date · rules version $rules_version $frozen · $side · 60-trading-day abnormal return $abnormal_return

=== frozen_on ===
frozen $rules_version_frozen

=== never_frozen ===
never frozen

=== no_runs ===
No run has left an outcome on record, so every row above is empty.
