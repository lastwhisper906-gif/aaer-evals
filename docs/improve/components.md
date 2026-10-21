# Harness components — the assumption each one encodes

One line per component the improvement loop may edit (`docs/improve_loop.md`):
what weakness it exists for, on which model that weakness was seen, and the
measurement that justified it. A component is an assumption about what the
model cannot yet do alone; when the model changes, the first pass turns each
off in turn and measures, and one that moves nothing is removed by its own
pull request. Newest last.

| component | weakness it covers | seen on | measurement |
|---|---|---|---|
| `src/analysis_hook.py` (the gate read to each analyst at write time) | the analysts quoted a filing's figure inline and the gate dropped the sentence: 400 of 414 drops over the fifteen runs of 2026-10-14 | claude-opus-5-5, effort xhigh | 2026-10-15, FN and FFIV, one call each side: drops 14→0, 1→0, 39→0, 0→0; output tokens about 2.3× (`docs/structure_changes.md` 2026-10-15) |
| the digit rule's wording in the three analyst prompts ("only inside the `quote` field") | the same | the same | the same measurement; the prompt line and the hook were changed together, so their effects are not separated |
