**(a) What did they do?** Built a solo, open-source, reproducible evaluation testing whether an LLM can flag future SEC accounting-enforcement cases from point-in-time filings — and, notably, measured how much of the model's "signal" was memorized company reputation rather than analysis.

**(b) Would I flag it?** Yes, for eval/research-engineering roles specifically. Two things clear the bar in a 60-second skim: the contamination experiment (masking identities and quantifying the 50% → 21.9% drop, with a concrete Hertz/Monsanto example that goes in *both* directions) is exactly the eval-hygiene instinct labs screen for, and "clone it, one command, no accounts, reproduces every number" is a rare, cheaply falsifiable claim — I'd tell the hiring manager to have someone actually run it. The LinkedIn post is stronger than the resume bullets: leading with "the caveat is the finding" and "the fastest way to criticize it is to clone it" reads as genuine calibration, not marketing. Caveats I'd note alongside the flag: solo project, N=12, no external users or review visible.

**(c) Inflated or vague?**

- **"Built and published"** — published where? It's a repo, not a venue. A skimmer may read peer review that isn't there. Say "open-sourced."
- **"the honest-limits framing that makes the result citable"** — self-awarded praise, and "citable" is unverifiable (has anyone cited it?). Cut the clause; the 50% → 21.9% number already makes the point.
- **"the verification layer an external skeptic actually needs"** — editorializing. "Built a verification layer: one command recomputes…" is stronger.
- **Bullet 2 is jargon soup**: "figure-drift sidecars," "machine-locked errata/translation ledger," "structural no-network/no-corpus sandbox" mean nothing to me in 60 seconds and read like invented terminology — which paradoxically makes the (real) engineering sound *less* credible. Keep "7 CI-enforced gates" and "reproduces with zero accounts, zero downloads"; drop or translate the rest.
- **Density**: each bullet carries 3–4 claims plus bracketed row citations. The `[RESULTS rows 1, 3]` cites belong in the repo, not on a resume — on paper they're clutter that signals the author couldn't decide what to cut.
- **The stats will invite scrutiny, not doubt**: p ≈ 0.001 with N=12 and an AUC interval down to 0.62 is honestly stated, but a technical screener will ask about it — that's fine, it's disclosed, but don't lead the resume bullet with the p-value; lead with the design.

Net: substance is above the bar; the prose oversells in exactly the places where the underlying work is strong enough not to need it. Trim the self-praise and the private vocabulary, and it screens very well.
