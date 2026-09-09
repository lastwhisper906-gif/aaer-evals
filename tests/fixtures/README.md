# tests/fixtures/

One directory per company: `tests/fixtures/{ticker}/`.

Each holds three saved filings — a 10-K, a 10-Q and an 8-K 2.02 — with an
expected-value file beside each one. Twelve companies by three filings is 36
fixtures, and the parsers are done when 36 of 36 pass.

Companies: AAPL · STX · CSCO · PANW · CARR · LFUS · GNRC · CIEN · QCOM · ESE ·
TTMI · NVDA.

## The two files that are not filings

`expected_values.json` holds the expected values, and every one of them names
where it came from. It is a flat object: one entry per expectation, keyed by a
dotted path, and each entry is exactly `{"value": …, "from": "…"}` where `from`
is one line saying which source produced the number — the submissions index, the
filing read by eye, the XBRL instance, an independent recount written in a test
file, or a hand computation. `tests/expected_values.py` is the only reader, and
a note that names none of the source kinds this project has, or cites a file that
is not there, is refused as firmly as a missing one: a value cannot be written
without a source and then quietly read. Cite `path` or `path::name`, never
`path:12` — the line moves and the note becomes a lie. A value nothing outside
the parsers could source was deleted, along with the assertion that read it.

`expected.json` is not an expected-value file. It is the extraction-drift
baseline `src/extraction_checks.py` reads — the ±20% band that answers "has the
pipeline moved since last time?" — and being the pipeline's own output is what
makes it fit for that job and unfit for any other. It carries no provenance
because it is not claiming any, and no test may read it as an answer key. Where a
recorded parser defect makes the pipeline's count differ from what the filing was
read to hold, the two files disagree, and the test carrying the expectation says
which defect and by how much.

They were one file once, called `expected.json`, and that is what let a number
produced by running a parser pass for an expectation about the filing it read.
