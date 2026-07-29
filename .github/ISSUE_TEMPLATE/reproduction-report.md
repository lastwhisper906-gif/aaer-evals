---
name: Reproduction report
about: You ran the two-command reproduction path (REPRODUCING.md) — tell us what
  happened, whether it matched or not.
title: "[repro] "
labels: reproduction
---

<!--
Thank you for attempting the reproduction path. Both PASS and FAIL reports
are valuable — a matching run is evidence, a mismatch is a finding.
-->

**Environment**
- OS / Python version (canonical: Python 3.12):
- Clone type: full clone / `git fetch --unshallow` repaired
  (shallow clones fail-closed by design — see REPRODUCING.md)

**Commands run** (from REPRODUCING.md)

```
<paste the exact commands>
```

**Result**
- [ ] All gates green (`make verify-public` RC=0)
- [ ] Mismatch / failure (paste the failing output below)

```
<paste output here>
```

**Which claim were you checking?** (optional — e.g. a RESULTS.md row, an
AUDIT_INDEX.md identifier)
