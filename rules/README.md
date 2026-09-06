# rules/

The frozen, versioned rules: `checklist_v0.1.md`, `targets_v0.1.md`,
`thresholds_v0.1.json`.

Every prediction is scored against the rules version named in its
`input_manifest.json`. An improvement lands as the next version and applies from
then on. Nothing is ever rescored under new rules.

`docs/CHECKLIST.md` is the readable draft these files are cut from. They are
written once the flag distribution over the 30 archived cases exists — until
then this directory is empty on purpose.

**Append-only**, on the same terms as `runs/`.
