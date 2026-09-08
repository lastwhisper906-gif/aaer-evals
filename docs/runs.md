# runs/

One directory per prediction: `runs/{ticker}/{accession}/`.

It holds everything every layer saw and everything each one said — the inputs,
each agent's own input directory, the manifest, the four reports, the two
predictions, the management explanations, the baselines and the controls. The
file list is in `docs/INPUT_SPEC.md`.

**Append-only.** Existing content is never changed or deleted — and nothing here
is a ledger, so nothing here grows either. A correction is a new file plus one
line in `events/ledger.jsonl`. `src/append_check.py` enforces this in CI, and a
violation stops the cycle rather than opening a ticket.

The directory itself is empty until the first prediction lands. This page lives
in `docs/` rather than inside it, because a file inside an append-only directory
can never be corrected — which is how that was found out.
