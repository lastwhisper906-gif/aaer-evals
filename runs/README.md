# runs/

One directory per prediction: `runs/{ticker}/{accession}/`.

It holds everything the predictor saw and everything it said — the inputs, the
manifest, the two predictions and the management explanations. The file list is
in `docs/INPUT_SPEC.md`.

**Append-only.** Nothing in here is ever edited or deleted. A correction is a new
file plus one line in `events/ledger.jsonl`. `src/append_check.py` enforces this
in CI, and a violation stops the cycle rather than opening a ticket.
