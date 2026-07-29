# REPRODUCING.md — Third-party reproduction guide

> Authored by Claude Code, pending human audit (GA-001 (b)).
> Rewritten 2026-07-22 (Phase B2, D108): the reproduction interface is fixed
> at two tiers, `make verify-public` / `make verify-full`. Tier-assignment
> criterion = **actual code behavior** (audit:
> `analysis/REVIEW_CLAIMS_AUDIT.md`). The former hand-maintained table of
> commands and point-in-time values is preserved in git history.
> Purpose (G2 public good): let a reader recompute and re-verify the
> published numbers **from committed artifacts alone**.
> Korean original: [REPRODUCING.ko.md](REPRODUCING.ko.md).

## 0. Two commands are everything

| Command | External data | What it does |
|---|---|---|
| `make verify-public` | **strictly 0** | Recomputes every published number + publication-conformance lint + doc-number lint + full pytest + manifest schema conformance + grading-precedence history & canary proof |
| `make verify-full` | requires `~/aaer-data` | All of the above + deterministic baseline recomputation (baselines·stats·synthesis·calibration) + exhaustive sha256 comparison of the raw corpus |

The "zero external data" claim of `verify-public` is proven **by an actual
run in a sandbox with HOME pointed at an empty temporary directory** —
transcript: `audit/verify_public_sandbox_transcript_20260722.txt`.
Corpus-dependent pytest cases are marked skip when the corpus is absent
(the synthetic tier runs in full).

The list of numbers and commands is a generated block derived from the
repository (refresh with `make docs-refresh`; CI compares it via
`tools/lint_doc_counts.py`):

<!-- BEGIN-GENERATED: repro-facts (refresh: make docs-refresh; CI: tools/lint_doc_counts.py) -->
- data manifest: **538 files** (`data/manifests/aaer_data_manifest.json` · `file_count`)
- pytest: **279 tests collected** (`pipeline tools scoring analysis`)
- `make verify-public` (zero external data):
  - `.venv/bin/python tools/reproduce_analysis.py`
  - `.venv/bin/python tools/lint_publication.py`
  - `.venv/bin/python tools/lint_doc_counts.py`
  - `.venv/bin/python -m pytest pipeline tools scoring analysis -q`
  - `.venv/bin/python tools/verify_manifest.py --schema-only`
  - `.venv/bin/python tools/verify_blindness.py`
- `make verify-full` (requires `~/aaer-data` corpus; see REPRODUCING.md §2):
  - `.venv/bin/python analysis/baselines.py`
  - `.venv/bin/python analysis/stats.py`
  - `.venv/bin/python analysis/synthesis.py`
  - `.venv/bin/python analysis/calibration_wave2.py`
  - `.venv/bin/python tools/verify_manifest.py`
  - `$(MAKE) verify-public`
<!-- END-GENERATED: repro-facts -->

## 1. Tier 1 — fully portable (`make verify-public`, anyone)

```bash
git clone <repo> && cd aaer-evals
python3.12 -m venv .venv                                    # 3.12 = canonical version of the reproduction claim
.venv/bin/pip install --require-hashes -r requirements.lock  # hash-pinned install (C4, D109)
make verify-public
```

**The canonical Python of the reproduction claim is 3.12** — CI runs a
3.11/3.12/3.13 matrix, but the reproduction claim is stated against 3.12;
a failure on a non-canonical version is only recorded as a finding and
does not break the reproduction claim (C5).

`requirements.lock` is the output of `pip-compile --generate-hashes`
(pip-tools, Python 3.12), sha256-pinning down to transitive dependencies —
`requirements.txt` remains the human-readable intent declaration of the 5
top-level pins (both are committed; regenerate the lock with
`pip-compile --allow-unsafe --generate-hashes --strip-extras -o
requirements.lock requirements.txt`).

Re-verification of the published headline numbers ends here — possible
**without the raw corpus** (the first line of defense for verifiability,
PROJECT.md §6-5). CI runs the same gates on every push.

## 2. Tier 2 — full corpus-dependent path (`make verify-full`)

Prerequisites (`corpus-check` prints the guidance below and fails when the
corpus is absent):

- **Layout**: `~/aaer-data/<TICKER>/xbrl/` (data.sec.gov companyfacts) +
  `<TICKER>/edgar/` (submissions) — detailed conventions in
  `data/README.md`. Absolute path outside git.
- **Size**: about 2.3 GB on disk (what the manifest pins is the file count
  in the generated block / about 586 MB).
- **Acquisition**: the two fetch tools in §3 below (SEC fair-access
  User-Agent required). In environments where SEC egress is blocked, the
  tools print a **fetch manifest (the list of required URLs)** so you can
  acquire the files separately and place them — or it is available on
  request.

`analysis/synthesis.py` belongs to this tier — it calls
`scoring/baselines/screens.run_case` to **recompute** the Beneish M /
Dechow F baselines from raw XBRL (`DATA_DIR = ~/aaer-data` in
`screens.py`). The logic is exactly the frozen code that produced the
numbers re-verified in tier 1.

```bash
make verify-full   # corpus-check → baselines·stats·synthesis·calibration → full manifest → verify-public
```

## 3. Rebuilding the raw XBRL cache (for external reproducers)

```bash
# per-CIK companyfacts (scoring-side collection; SEC fair-access UA required)
.venv/bin/python tools/fetch_xbrl_facts.py       # case & control-group CIK companyfacts
.venv/bin/python tools/fetch_primary_sources.py  # submissions / filing history
```

Provenance follows the `runs/*/control_pool_raw/provenance.jsonl`
convention.

## 4. Re-running the pipeline (evaluatee grading — subscription required, optional for reproduction)

**Not needed** to re-verify the published numbers (§1 suffices).
Re-running the grading itself requires subscription OAuth (the `claude`
CLI); `ANTHROPIC_API_KEY` must be absent — asserted (the zero-metered
mandate, D102).

**Installing the Claude CLI (harness — previously missing from the docs,
C4)**:

```bash
npm install -g @anthropic-ai/claude-code@2.1.201   # = pipeline/cli_client.HARNESS_PIN
claude --version                                    # confirm the output contains the pin string
```

Before the first call, `cli_client.enforce_harness_pin()` compares a live
`claude --version` reading against the pin and halts fail-closed on
mismatch or command failure (the honest record of when enforcement began
is the 2026-07-22 entry in `CHANGELOG.md`). Example: reproducing the E3
redraw — `python pipeline/runner.py --cases
data/evaluatee/cases_wave2.json --perturbed --out
runs/wave2/perturbed_redraw/draw_2 --only <9 fraud ids>`
(idempotent, pin-verified, rate-limit resume).

## 5. Monthly holdout rescan (`tools/holdout_rescan.py`)

Accumulates post-cutoff new disclosures (8-K Item 4.02) with a single
command — the procedure that fills `docs/FUTURE_HOLDOUT_CANDIDATES.md`
Tier-2. Same SEC fair-access UA as §3; prints a fetch manifest when
egress is blocked.

## 6. Disclaimer

Scoped to a single Claude-based pipeline. Re-verification of the
published numbers is possible from committed artifacts alone
(verifiability = the best defense, §6-5). Grading re-runs are
harness-mediated and may differ from the raw API (L-2).
