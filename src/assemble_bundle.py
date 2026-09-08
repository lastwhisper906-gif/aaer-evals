"""One run directory: the files the predictor sees, and the manifest.

`docs/INPUT_SPEC.md` §5 names eight. This file writes nine — see `FILES` for
the ninth and the conflict inside the spec that puts it there — and then writes
`input_manifest.json`, which is the index a reader uses to check the others:
every paragraph id that reached a file, every paragraph that was excluded and
why, the cutoff, and the two placeholders that are not real yet.

**The cutoff is the triggering report's filing date**, so the bundle for a 10-K
cannot contain the 10-Q that came after it. That is not a detail of this file —
it decides which documents exist at all, and it is why a 10-K bundle has no note
change history (there is one 10-K on record, and a history needs two) while a
10-Q bundle has one. The absence is written into the file and into the manifest
rather than left for a reader to notice.

**`rules_version` and `served_model` are null.** `rules/v0.1` does not exist and
no prediction has been served, so a value here would be a guess about the two
fields that decide how a prediction is scored. They are null with a comment
saying what has to happen first, and a test asserts they are still null — the
day they become real is a change someone makes on purpose.

**The output root is an argument** and the default is never created as a side
effect. The loop that runs this cannot write `runs/`, and nothing here tries.

    python3.12 -m src.assemble_bundle --ticker AAPL --form 10-K --out /tmp/bundle
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

try:
    from src import (clean_text, cutoff_guard, diff_periods, extract_notes,
                     extract_numbers, html_text, interpreter_pin, note_history,
                     parse_8k, split_sections, trends)
except ImportError:  # invoked as a plain script
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import (clean_text, cutoff_guard, diff_periods, extract_notes,
                     extract_numbers, html_text, interpreter_pin, note_history,
                     parse_8k, split_sections, trends)

BAD_INPUT = 2

DEFAULT_ROOT = Path("runs")
TRIGGERING_FORMS = ("10-K", "10-Q")

# `input_controls.md` is the ninth file and `docs/INPUT_SPEC.md` §5 lists eight.
# §1 requires the auditor's report with its critical audit matters, Item 9A and
# the 10-Q's Item 4 — "HTML section split" — and §5 has no file to put them in,
# so the two sections of the spec disagree. `docs/` is not ours to edit; the
# name follows §5's own convention (`input_{what it holds}.md`) so that
# reconciling it is a one-line change, and the conflict is in the build report.
FILES = ("input_numbers.json", "input_trends.json", "input_notes.md",
         "input_notes_history.md", "input_mdna.md", "input_controls.md",
         "input_8k.md", "input_prior_predictions.md", "input_manifest.json")
# The files a paragraph id can live in. The two JSON files carry fact ids and
# period labels, which are a different kind of thing and are indexed by their
# own contents.
PARAGRAPH_FILES = ("input_notes.md", "input_notes_history.md", "input_mdna.md",
                   "input_controls.md", "input_8k.md",
                   "input_prior_predictions.md")

# 10-K: the auditor's report and Item 9A. 10-Q: Item 4. `docs/INPUT_SPEC.md` §1.
CONTROL_SECTIONS = {"10-K": ("auditors_report", "item_9a"),
                    "10-Q": ("item_4_controls",)}

RULES_VERSION_COMMENT = (
    "null until rules/v0.1 exists; a prediction is scored against its own rules "
    "version and guessing one here would decide that scoring by accident")
SERVED_MODEL_COMMENT = (
    "null until a prediction is served; the pinned-model runner records what it "
    "actually served, and nothing else may claim to know it")

# What a prior prediction file may never carry forward.
PROBABILITY_KEYS = ("probability", "probabilities", "score", "scores",
                    "likelihood", "confidence")


class BundleError(Exception):
    """The bundle cannot be assembled from what is on record."""


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _is_id_line(line: str) -> bool:
    """`[id]` alone on its line, where an id is `accession:file:n`.

    An id holds no whitespace, and that is what tells it from the collapsed
    line `[same as prior period, unchanged from …]` — which since cycle 20
    holds a colon of its own, so a colon no longer distinguishes them.
    """
    stripped = line.strip()
    return (stripped.startswith("[") and stripped.endswith("]")
            and ":" in stripped and not any(c.isspace() for c in stripped))


def paragraph_ids(text: str) -> list[str]:
    """The `[id]` lines of a rendered file, in the order they appear."""
    return [line.strip()[1:-1] for line in text.split("\n") if _is_id_line(line)]


def paragraph_blocks(text: str) -> list[tuple[str, str]]:
    """(id, text) for every paragraph of a rendered file, in order.

    A paragraph is everything between one `[id]` line and the next, which is
    what makes a rendered table one paragraph: its rows are lines inside the
    block, not blocks of their own.
    """
    out: list[tuple[str, str]] = []
    identifier, body = None, []
    for line in text.split("\n"):
        if _is_id_line(line):
            if identifier is not None:
                out.append((identifier, "\n".join(body).strip()))
            identifier, body = line.strip()[1:-1], []
        elif line.startswith("#"):
            continue            # a `#` or `##` heading is the file's own scaffolding
        elif identifier is not None:
            body.append(line)
    if identifier is not None:
        out.append((identifier, "\n".join(body).strip()))
    return out


# --- the pieces --------------------------------------------------------------

def documents_on_record(ticker: str, cutoff, fixtures_root) -> list[dict]:
    """Every fixture document filed at or before the cutoff, as the record has
    it. A document filed later is not in the bundle and not in the manifest."""
    rows = []
    for row in cutoff_guard.documents(ticker, fixtures_root=fixtures_root):
        if row["filing_date"] <= str(cutoff):
            rows.append({"form": row["form"], "role": row["role"],
                         "accession": row["accession"], "path": row["path"],
                         "filing_date": row["filing_date"], "sha256": row["sha256"]})
    rows.sort(key=lambda row: (row["filing_date"], row["accession"], row["role"]))
    return rows


def note_stream(ticker: str, form: str, *, cutoff, fixtures_root):
    """Note paragraphs after the diff layer, and the paragraphs it dropped.

    A 10-Q is diffed against the 10-Q before it. A 10-K has no earlier 10-K on
    record, so every paragraph is carried and the manifest says why.
    """
    if form == "10-Q":
        payload = diff_periods.extract(ticker, cutoff=cutoff, fixtures_root=fixtures_root)
        return payload["notes"], payload["mdna"], payload["prior_accession"]

    notes = diff_periods.diff_stream(
        diff_periods._note_paragraphs(ticker, form, "xbrl_instance",
                                      cutoff=cutoff, fixtures_root=fixtures_root), [])
    row = cutoff_guard.one_document(ticker, form, "primary_html",
                                    fixtures_root=fixtures_root)
    kept = clean_text.clean_stream(
        blocks=split_sections.extract(ticker, form, "mdna", cutoff=cutoff,
                                      fixtures_root=fixtures_root)["blocks"])["paragraphs"]
    mdna = diff_periods.diff_stream(
        [{"id": f"{row['accession']}:mdna:{index}", "text": text, "note": "mdna",
          "verbatim_topic": diff_periods.always_verbatim("mdna", text)}
         for index, text in enumerate(kept, start=1)], [])
    return notes, mdna, None


def control_sections(ticker: str, form: str, *, cutoff, fixtures_root) -> list[dict]:
    """The untagged sections `docs/INPUT_SPEC.md` §1 asks for, one entry each.

    `docs/CHECKLIST.md` makes `control_weakness_disclosed` and
    `new_critical_audit_matter` questions the model answers with a quote and a
    paragraph id. Until this file existed the bundles held no occurrence of
    `critical audit matter`, `disclosure controls and procedures`, `material
    weakness` or `report of independent registered public accounting firm` — so
    the only way to answer was to quote something that is not in the inputs.

    A section that is genuinely not in the document is recorded with the reason,
    the same way a missing 8-K and a missing note history are. It is never
    silently absent.
    """
    out = []
    for section in CONTROL_SECTIONS[form]:
        try:
            found = split_sections.extract(ticker, form, section, cutoff=cutoff,
                                           fixtures_root=fixtures_root)
        except split_sections.SectionNotFound as exc:
            out.append({"section": section, "paragraphs": [], "reason": str(exc)})
            continue
        out.append({"section": section,
                    "accession": found["accession"],
                    "filing_date": found["filing_date"],
                    "heading_candidates": found["heading_candidates"],
                    "paragraphs": list(zip(found["paragraph_ids"], found["carried"])),
                    "reason": None})
    return out


def render_controls(ticker: str, form: str, sections: list[dict]) -> str:
    out = [f"# {ticker} {form} controls and the auditor's report", ""]
    for entry in sections:
        out.extend(["", f"## {entry['section']}", ""])
        if entry["reason"]:
            out.extend([entry["reason"] + ".", ""])
            continue
        for identifier, text in entry["paragraphs"]:
            out.extend([f"[{identifier}]", text, ""])
    return "\n".join(out)


def excluded_paragraphs(ticker: str, form: str, *, cutoff, fixtures_root) -> list[dict]:
    """Every paragraph the cleaner dropped, with the reason it gave.

    The cleaner is run again here rather than threaded through the diff layer,
    because the manifest has to name the drops and the diff layer keeps only
    what survived them.
    """
    out = []
    notes = diff_periods.notes(ticker, form, "xbrl_instance", cutoff=cutoff,
                               fixtures_root=fixtures_root)
    for drop in notes["dropped"]:
        out.append({"id": f"{notes['accession']}:notes_excluded:{len(out) + 1}",
                    "source": f"{form} notes / {drop['source']}",
                    "reason": drop["reason"], "text": drop["text"]})

    mdna = split_sections.extract(ticker, form, "mdna", cutoff=cutoff,
                                  fixtures_root=fixtures_root)
    dropped_mdna = clean_text.clean_stream(blocks=mdna["blocks"])["dropped"]
    row = cutoff_guard.one_document(ticker, form, "primary_html", fixtures_root=fixtures_root)
    for number, drop in enumerate(dropped_mdna, start=1):
        out.append({"id": f"{row['accession']}:mdna_excluded:{number}",
                    "source": f"{form} MD&A", "reason": drop["reason"],
                    "text": drop["text"]})
    return out


def excluded_from_the_release(ticker: str, *, cutoff, fixtures_root) -> list[dict]:
    """The earnings release's own drops, including any table already in XBRL."""
    rows = cutoff_guard.documents(ticker, form="8-K", role="exhibit_99_1",
                                  fixtures_root=fixtures_root)
    rows = [row for row in rows if row["filing_date"] <= str(cutoff)]
    if not rows:
        return []
    row = rows[-1]
    html = cutoff_guard.load_document(row["full_path"], cutoff, fixtures_root=fixtures_root)
    result = clean_text.clean(html)
    out = []
    for number, drop in enumerate(result["dropped"], start=1):
        out.append({"id": f"{row['accession']}:8k_excluded:{number}",
                    "source": "8-K exhibit 99.1", "reason": drop["reason"],
                    "text": drop["text"]})
    for table in result["tables"]:
        if not table["kept"]:
            out.append({"id": f"{row['accession']}:8k_excluded_table:{table['number']}",
                        "source": "8-K exhibit 99.1",
                        "reason": "every number in the table is already an XBRL fact",
                        "text": ""})
    return out


def group_empty(exclusions: list[dict], accession: str) -> list[dict]:
    """Collapse the empty-paragraph drops into one line per source.

    A filing separates its blocks with paragraphs holding one zero-width space,
    and Esterline's 10-Q has nearly five thousand of them. Listing each one
    would put three quarters of a megabyte of nothing in the manifest and bury
    the drops a reader has to check. There is no text to lose, so they are
    counted per source instead — still an exclusion, still with a reason.
    """
    kept, counted = [], {}
    for entry in exclusions:
        if entry["reason"] == "empty":
            counted[entry["source"]] = counted.get(entry["source"], 0) + 1
        else:
            kept.append(entry)
    for number, (source, count) in enumerate(sorted(counted.items()), start=1):
        kept.append({
            "id": f"{accession}:empty_excluded:{number}",
            "source": source,
            "reason": f"empty paragraph — whitespace or a zero-width space and "
                      f"nothing else; {count} of them, with no text to record",
            "text": "",
        })
    return kept


def run_filing_date(run: Path) -> str | None:
    """The filing date a past run recorded for itself, out of its own manifest."""
    try:
        manifest = json.loads(cutoff_guard.load_bundle_file(run, "input_manifest.json"))
    except (cutoff_guard.CutoffGuardError, OSError, ValueError):
        return None
    date = manifest.get("filing_date") or manifest.get("cutoff")
    return str(date) if date else None


def prior_predictions(ticker: str, root: Path, cutoff=None) -> tuple[str, list[dict]]:
    """Past flag lists and outcomes, with every probability left behind.

    Nothing is invented when there are none: the file says there are none, and
    that is a true statement about the record rather than an empty file.

    **A run of a later quarter is not a prior run.** `cutoff_guard` does not
    date-gate a bundle file on purpose, so nothing stopped a run dated after the
    cutoff — its flags, its outcomes — from entering this file, and the default
    root is `runs/`, so it fires by itself the day a later quarter is published
    and an earlier one reassembled. The date is the one the past run recorded
    for itself in its own `input_manifest.json`. A run that recorded none is not
    carried, because an undated run cannot be shown to be earlier.
    """
    limit = str(cutoff) if cutoff is not None else None
    kept = []
    for run in cutoff_guard.prior_runs(root, ticker):
        date = run_filing_date(run)
        if limit is None or (date is not None and date <= limit):
            kept.append(run)
    found = [(run, name) for run in kept
             for name in cutoff_guard.bundle_files(run, "prediction_*.json")]
    if not found:
        return ("# {ticker} prior predictions\n\n"
                "None on record. This company has no earlier run under the given "
                "run root, so there are no flags, no management explanations and "
                "no outcomes to carry forward.\n".format(ticker=ticker), [])

    lines, entries = [f"# {ticker} prior predictions", ""], []
    for run, name in found:
        try:
            payload = json.loads(cutoff_guard.load_bundle_file(run, name))
        except ValueError as exc:
            raise BundleError(f"{run}/{name} is not readable JSON: {exc}") from exc
        accession = run.name
        lines.extend([f"## {accession} — {name}", ""])
        for number, flag in enumerate(payload.get("flags", []), start=1):
            identifier = f"{accession}:prior:{name.removesuffix('.json')}:{number}"
            text = flag if isinstance(flag, str) else json.dumps(
                {key: value for key, value in flag.items()
                 if key.lower() not in PROBABILITY_KEYS}, sort_keys=True)
            lines.extend([f"[{identifier}]", text, ""])
            entries.append({"id": identifier, "file": "input_prior_predictions.md",
                            "kind": "prior_flag"})
    return "\n".join(lines) + "\n", entries


# --- the bundle ---------------------------------------------------------------

def build(ticker: str, form: str, *, cutoff=None, fixtures_root=cutoff_guard.FIXTURES,
          prior_runs: Path = DEFAULT_ROOT) -> dict:
    """Every file's text, plus what the manifest needs to describe them."""
    if form not in TRIGGERING_FORMS:
        raise BundleError(f"{form} is not a triggering report; "
                          f"one of {', '.join(TRIGGERING_FORMS)}")
    trigger = cutoff_guard.one_document(ticker, form, "primary_html",
                                        fixtures_root=fixtures_root)
    # The cutoff is the triggering report's own filing date unless a run names
    # another one. Nothing filed after it is read, so the rule is enforced by
    # what is loaded rather than by remembering to check.
    cutoff = str(cutoff) if cutoff else trigger["filing_date"]
    if cutoff < trigger["filing_date"]:
        raise BundleError(f"cutoff {cutoff} is before {form} {trigger['accession']} "
                          f"was filed on {trigger['filing_date']}")
    # And bounded above. `CLAUDE.md`: the cutoff **is** the triggering report's
    # filing date. A later one was accepted silently, and `--form 10-K --cutoff
    # 2026-08-01` on a 10-K triggered 2025-10-31 pulled six later documents in
    # and built a note history out of them, exit 0.
    if cutoff > trigger["filing_date"]:
        raise BundleError(f"cutoff {cutoff} is after {form} {trigger['accession']} "
                          f"was filed on {trigger['filing_date']}. The cutoff is "
                          f"the triggering report's own filing date")

    on_record = {(row["form"], row["role"]): row
                 for row in documents_on_record(ticker, cutoff, fixtures_root)}
    forms = tuple(name for name in ("10-K", "10-Q")
                  if (name, "xbrl_instance") in on_record)
    numbers = extract_numbers.extract(ticker, forms, cutoff=cutoff,
                                      fixtures_root=fixtures_root)
    table = trends.trends(json.loads(json.dumps(numbers, default=str)))

    notes, mdna, prior_accession = note_stream(ticker, form, cutoff=cutoff,
                                               fixtures_root=fixtures_root)

    if ("8-K", "exhibit_99_1") in on_record and ("8-K", "primary_html") in on_record:
        eight_k_text = parse_8k.render(
            parse_8k.extract(ticker, cutoff=cutoff, fixtures_root=fixtures_root))
        eight_k_note = None
    else:
        # The sentence says what is missing and nothing about what comes later.
        # It used to name the held 8-K's own filing date, a date after the
        # cutoff, in 15 of the 24 bundles. PANW's 10-K stated that an 8-K was
        # filed 2026-09-01 under a cutoff of 2025-08-29 — twelve months of
        # look-ahead, plus the fact that the company filed one in the window.
        eight_k_note = (f"no 8-K filed at or before {cutoff} is on record, so this "
                        f"bundle has no earnings release and no verbatim item body")
        # No exhibit on record does not mean no filing index. The item codes and
        # the late-filing notices come from `submissions.json`, which is stored
        # for every company, and a bundle that says nothing about them cannot
        # answer `filing_irregularity` either way.
        eight_k_text = (f"# {ticker} 8-K\n\n{eight_k_note}.\n\n"
                        + parse_8k.render_index(ticker, cutoff=cutoff,
                                                fixtures_root=fixtures_root))

    # The history is two consecutive 10-Qs, whatever form triggered the run.
    if all(key in on_record for key in (("10-Q", "xbrl_instance"),
                                        ("10-Q", "prior_period_xbrl_instance"))):
        history = note_history.history(ticker, cutoff=cutoff, fixtures_root=fixtures_root)
        history_text = note_history.render(history)
        history_note = None
    else:
        history = None
        history_note = (f"no note change history: a history needs two 10-Qs and the "
                        f"record holds fewer at or before {cutoff}")
        history_text = f"# {ticker} note change history\n\n{history_note}.\n"

    prior_text, prior_entries = prior_predictions(ticker, Path(prior_runs), cutoff)

    controls = control_sections(ticker, form, cutoff=cutoff,
                                fixtures_root=fixtures_root)

    texts = {
        "input_numbers.json": json.dumps(numbers, indent=2, sort_keys=False,
                                         default=str) + "\n",
        "input_trends.json": trends.render(table),
        "input_notes.md": diff_periods.render(
            notes, f"{ticker} notes — {trigger['accession']}"),
        "input_notes_history.md": history_text,
        "input_mdna.md": diff_periods.render(
            mdna, f"{ticker} MD&A — {trigger['accession']}"),
        "input_controls.md": render_controls(ticker, form, controls),
        "input_8k.md": eight_k_text,
        "input_prior_predictions.md": prior_text,
    }

    paragraphs = []
    for entry in notes:
        paragraphs.append({"id": entry["id"], "file": "input_notes.md",
                           "kind": entry["kind"]})
    for entry in mdna:
        paragraphs.append({"id": entry["id"], "file": "input_mdna.md",
                           "kind": entry["kind"]})
    if history is not None:
        for entry in history["entries"]:
            paragraphs.append({"id": entry["id"], "file": "input_notes_history.md",
                               "kind": entry["kind"]})
            # A `changed` entry prints two paragraphs from two filings. Both are
            # in the file, so both are in the manifest, each under the accession
            # its text came from.
            if entry["kind"] == "changed":
                paragraphs.append({"id": entry["previous_id"],
                                   "file": "input_notes_history.md",
                                   "kind": "previous"})
    for entry in controls:
        for identifier, _ in entry["paragraphs"]:
            paragraphs.append({"id": identifier, "file": "input_controls.md",
                               "kind": "verbatim"})
    for identifier in paragraph_ids(texts["input_8k.md"]):
        paragraphs.append({"id": identifier, "file": "input_8k.md",
                           "kind": "table" if ":8k_2_02_table:" in identifier
                                   else "verbatim"})
    paragraphs.extend(prior_entries)

    exclusions = excluded_paragraphs(ticker, form, cutoff=cutoff,
                                     fixtures_root=fixtures_root)
    exclusions += excluded_from_the_release(ticker, cutoff=cutoff,
                                            fixtures_root=fixtures_root)
    exclusions = group_empty(exclusions, trigger["accession"])
    for name, reason in (("input_notes_history.md", history_note),
                         ("input_8k.md", eight_k_note)):
        if reason:
            exclusions.append({"id": f"{trigger['accession']}:file:{name}",
                               "source": name, "reason": reason, "text": ""})
    for entry in controls:
        if entry["reason"]:
            exclusions.append({"id": f"{trigger['accession']}:section:{entry['section']}",
                               "source": "input_controls.md",
                               "reason": entry["reason"], "text": ""})

    manifest = {
        "ticker": ticker,
        "form": form,
        "accession": trigger["accession"],
        "filing_date": trigger["filing_date"],
        "cutoff": str(cutoff),
        "prior_accession": prior_accession,
        "rules_version": None,
        "rules_version_comment": RULES_VERSION_COMMENT,
        "served_model": None,
        "served_model_comment": SERVED_MODEL_COMMENT,
        "documents": documents_on_record(ticker, cutoff, fixtures_root),
        "paragraphs": paragraphs,
        "exclusions": exclusions,
        "counts": {
            "paragraphs": len(paragraphs),
            "exclusions": len(exclusions),
            "facts": len(numbers["facts"]),
            "notes": sum(1 for entry in paragraphs if entry["file"] == "input_notes.md"),
            "mdna": sum(1 for entry in paragraphs if entry["file"] == "input_mdna.md"),
            "note_history": sum(1 for entry in paragraphs
                                if entry["file"] == "input_notes_history.md"),
            "controls": sum(1 for entry in paragraphs
                            if entry["file"] == "input_controls.md"),
            "eight_k": sum(1 for entry in paragraphs if entry["file"] == "input_8k.md"),
        },
        "files": {name: {"sha256": _sha256(text.encode("utf-8")),
                         "bytes": len(text.encode("utf-8"))}
                  for name, text in sorted(texts.items())},
    }
    texts["input_manifest.json"] = json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    return {"texts": texts, "manifest": manifest}


def write(bundle: dict, out: Path) -> Path:
    out.mkdir(parents=True, exist_ok=True)
    for name in FILES:
        (out / name).write_text(bundle["texts"][name], encoding="utf-8")
    return out


def assemble(ticker: str, form: str, out: Path, *, cutoff=None,
             fixtures_root=cutoff_guard.FIXTURES,
             prior_runs: Path = DEFAULT_ROOT) -> dict:
    bundle = build(ticker, form, cutoff=cutoff, fixtures_root=fixtures_root,
                   prior_runs=prior_runs)
    write(bundle, Path(out))
    return bundle["manifest"]


def default_out(ticker: str, accession: str, root: Path = DEFAULT_ROOT) -> Path:
    """Where a run lands when nobody says otherwise. Naming it does not make it."""
    return Path(root) / ticker / accession


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="one run directory of predictor inputs")
    parser.add_argument("--ticker", required=True)
    parser.add_argument("--form", default="10-K", choices=list(TRIGGERING_FORMS))
    parser.add_argument("--cutoff", default=None,
                        help="ISO date; default is the triggering report's filing date")
    parser.add_argument("--fixtures", default=str(cutoff_guard.FIXTURES))
    parser.add_argument("--prior-runs", default=str(DEFAULT_ROOT),
                        help="where earlier runs live; missing is fine and is recorded")
    parser.add_argument("--out", default=None,
                        help=f"the bundle directory; default {DEFAULT_ROOT}/TICKER/ACCESSION")
    args = parser.parse_args(argv)

    ticker = args.ticker.upper()
    try:
        bundle = build(ticker, args.form, cutoff=args.cutoff,
                       fixtures_root=Path(args.fixtures),
                       prior_runs=Path(args.prior_runs))
        out = Path(args.out) if args.out else default_out(
            ticker, bundle["manifest"]["accession"])
        write(bundle, out)
    except (cutoff_guard.CutoffGuardError, BundleError, OSError) as exc:
        print(f"assemble_bundle: {exc}", file=sys.stderr)
        return BAD_INPUT
    print(f"assemble_bundle: {ticker} {args.form} "
          f"{bundle['manifest']['counts']['paragraphs']} paragraphs, "
          f"{bundle['manifest']['counts']['exclusions']} exclusions → {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(interpreter_pin.enforce() or main())
