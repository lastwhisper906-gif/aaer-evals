# Lens answers, as they came back

One file per real lens answer that the verdict reader had to be taught to read.
They are copied byte for byte out of a run's `.lens/` directory and never
hand-written, because the thing being judged is what a lens actually does with
the prompt -- not what this project imagines it does.

- `fable_prose_before_the_verdict.json` — the `claude -p --output-format json`
  envelope from the fallback lens's reading of the lens design itself,
  2026-09-22. Its `result` opens with one sentence ("Finishing up: I've read the
  full diff...") and then carries a schema-valid `fail` with three findings. The
  reader threw the whole answer away and the run recorded `no_lens_ran`, which
  turned a `fail` into silence.
