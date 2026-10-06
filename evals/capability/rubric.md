# The analysis-grader's rubric

The analysis-grader reads one run's published outputs and this rubric, and writes
`grade.json` into the run directory. It never sees the analysts' transcripts, and it
is never the analysts' model: it runs on Opus, and the analysts run on Fable. It
grades the output, not how the output was made.

## What it reads

The run's own files:
- `analysis_accounting.json`, `analysis_financial.json` and `analysis_valuation.json`
- `assumptions.json`
- `report_numbers.md` and `report_notes_text.md`
- `calculator.json` and `calculator_filings_only.json`
- the `input_*.md` files
- `memo_ko.md`

## Dealbreakers: an anomaly or answer with any of these scores zero

1. **A number not from the calculator.** A figure in the analyst's own words that no
   calculator path supplies. A number inside a verbatim quote is the filer's and is
   allowed.
2. **An unresolved quote.** A quote that is not, character for character, in the
   file it names (whitespace aside).
3. **A post-cutoff fact.** Anything dated after the run's cutoff in
   `input_manifest.json`.
4. **A contradiction reported as unresolved.** Two inputs disagree, the analyst
   saw both, and left it as unresolved when the inputs settle it.

## Severity-weighted checks, for everything else

For each anomaly in the two frames (accounting; finance), give a verdict:
- **supported**: the cited evidence shows what the anomaly says
- **unsupported**: the evidence does not show it, or shows the opposite
- **unclear**: the evidence is relevant but does not settle it

Weight each verdict by severity:
- **high**: it would change how a reader trusts the numbers or values the company
- **medium**: it changes a ratio's reading
- **low**: presentation

Then three questions for the whole run, each answered yes or no with one line of
evidence:
- **Coverage.** Did the accounting analysis answer each of its seven areas and the
  industry lens, and the financial analysis each of its sections? A gate drop counts
  as unanswered here.
- **Calibration.** Do the verdicts in the areas match the anomalies listed under
  them?
- **Valuation reading.** Does the valuation reading say where the price sits, what
  growth it implies, and the two assumptions value is most sensitive to, all from the
  calculator?

## The score

- An anomaly scores 1 when supported, 0.5 when unclear, and 0 when unsupported or a
  dealbreaker.
- The run's score is the severity-weighted mean, with high weighing 3, medium 2 and
  low 1.
- The three whole-run questions are reported beside the score, not folded into it.
- The score grades the analysis, never the company. It is reported and never gated
  until the grader agrees with the owner on the golden filings at the floor set in
  `evals/thresholds.json`.

## grade.json

```json
{
  "run": "<ticker>/<run directory>",
  "rubric": "evals/capability/rubric.md",
  "dealbreakers": [{"kind": "number_not_from_calculator", "where": "anomalies[3].what", "why": "..."}],
  "items": [{"id": "<anomaly id>", "frame": "accounting", "verdict": "supported",
             "severity": "high", "why": "one line, citing the paragraph id or calculator path"}],
  "coverage": {"answer": "yes", "why": "..."},
  "calibration": {"answer": "yes", "why": "..."},
  "valuation_reading": {"answer": "no", "why": "..."},
  "score": 0.0
}
```
