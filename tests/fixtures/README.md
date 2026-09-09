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
is one line saying which source produced the number — companyfacts, the
submissions index, the filing read by eye, an independent recount written in a
test file, or a hand computation. `tests/expected_values.py` is the only reader,
and it refuses an entry that names no source, so a value cannot be written
without one and then quietly read. A value nothing outside the parsers could
source was deleted, along with the assertion that read it.

`expected.json` is not an expected-value file. It is the extraction-drift
baseline `src/extraction_checks.py` reads — the ±20% band that answers "has the
pipeline moved since last time?" — and being the pipeline's own output is what
makes it fit for that job and unfit for any other. Its numbers are mirrored from
`expected_values.json`, which carries the provenance, and
`tests/test_expected_values.py` asserts the mirror.

They were one file once, called `expected.json`, and that is what let a number
produced by running a parser pass for an expectation about the filing it read.
