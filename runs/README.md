# runs/

One directory per prediction: `runs/{ticker}/{accession}/`.

It holds everything the predictor saw and everything it said — the inputs, the
manifest, the two predictions and the management explanations. The file list is
in `docs/INPUT_SPEC.md`.

**Append-only.** Existing content is never changed or deleted — and nothing here
is a ledger, so nothing here grows either. A correction is a new file plus one
line in `events/ledger.jsonl`. `src/append_check.py` enforces this in CI, and a
violation stops the cycle rather than opening a ticket.
