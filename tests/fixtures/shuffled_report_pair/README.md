# tests/fixtures/shuffled_report_pair/

Two companies' four reports each, written by hand, for the shuffled-report
control in `src/control_shuffled.py`.

**These are not filings and not the pipeline's output.** No reader wrote them,
no filing was read to write them, and every figure in them is invented. They are
here because the control crosses two companies' reports and the pipeline has not
yet produced a single real one — `docs/HOW_WE_WORK.md` §7 puts the four report
shapes and the agent definitions at step six, and `runs/` is empty. A fixture
that had to wait for a real run would leave the control with no judge.

## Why these two companies

`docs/CHECKLIST.md` §8 pairs each company with **the next company in the twelve
by ticker, wrapping around**. Sorted by ticker the twelve begin AAPL, CARR, so
the pair here is the pairing the rule itself produces for AAPL: AAPL keeps the
numbers side, CARR supplies the notes side.

## What each report holds

Each company's four reports are the ones `docs/INPUT_SPEC.md` §6 names —
`report_numbers.md`, `report_numbers_vs_market.md`, `report_notes_text.md`,
`report_notes_vs_market.md`. Each one names its own company on its first line
and carries item ids built on that company's own accession, so a crossed pair is
visible to a reader and not only to a test.

The on-disk shape of a report is unsettled (`src/quote_gate.py` says so, and
`docs/INPUT_SPEC.md` and `docs/CHECKLIST.md` §7 disagree about it). It does not
bear on this control: the control moves whole files and never parses one. The
shape here follows what `src/note_history.py` writes for a quotable input — an
`[id]` on its own line, the text under it — so that the fixture models the real
thing rather than a shape of its own.

The two companies' reports differ file by file, and
`tests/test_control_shuffled.py` asserts that they do before it asserts anything
about the crossing: if the two companies' notes reports held the same text,
"the notes came from the other company" could not be told from the text at all.
