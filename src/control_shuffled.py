"""The shuffled-report control: one company's numbers, another company's notes.

`docs/CHECKLIST.md` §8 states what this control falsifies:

    the supervisor is fed one company's numbers report together with **another
    company's** notes report, on every pilot filing. If its score matches the
    real run, the supervisor is not reconciling the two reports, it is
    pattern-matching one of them.

and states exactly what is swapped, because "one company's report" leaves the
comparer reports undefined: company A keeps `report_numbers.md` and
`report_numbers_vs_market.md`; `report_notes_text.md` and
`report_notes_vs_market.md` come from company B. The notes side travels with its
own comparer report, so the only thing broken is the correspondence between the
two sides -- which is the thing being tested.

The supervisor is the pipeline's own supervisor, unchanged: same prompt, same
model, same output schema. Nothing here writes a prompt. That is what makes the
control a control -- if the evidence were crossed *and* the prompt changed, a
score that matched the real run would say nothing about reconciliation. So this
module carries no prompt, unlike the single-agent control, whose prompt
`docs/HOW_WE_WORK.md` §6 puts inside its own run script.

What Python owns here, and what it does not
-------------------------------------------

Python crosses the four report files, verifies that they really are two
companies' halves, records which run each half came from, resolves the
supervisor's citations against the crossed set, and writes the two control
files. The one model call per question is the supervisor's, and it is passed in
as `predictor`. There is no command line: the call cannot be made from one, and
an entry point that could not make it would be a script nobody could run.

    reports = crossed(numbers_bundle, notes_bundle)      # what the supervisor sees
    run("AAPL", partner("AAPL"), numbers_bundle=..., notes_bundle=...,
        out=..., predictor=...)                          # both control files

**Which company is B.** `docs/CHECKLIST.md` says "the next company in the twelve
by ticker, wrapping around, so the pairing is fixed rather than drawn". Read as
the twelve in ticker order -- `by ticker` is what distinguishes the pairing from
the order `src/fetch_fixtures.py` and `tests/fixtures/README.md` happen to list
them in, which is a fetch order and not a canonical one. That reading is
`PAIRING_ORDER` below and nothing else depends on it, so a correction is one
line.

A half is what its own reports say it is
----------------------------------------

The two tickers handed to `run` are labels, and a label is the one thing a
crossed pair cannot be checked by: two directories that both hold one company's
reports satisfy every label, and what lands on disk is then the real uncrossed
run wearing the word "shuffled". So each half is read for what it says about
itself -- every report opens with a heading naming its own company, and every
item id it carries begins with the accession of the filing it was written from
-- and the pair is refused unless the two halves name two different companies.
The labels are still checked, against what the reports say rather than against
each other: a half whose label disagrees with its own reports is refused too,
because the label is what the control file would carry.

**The cutoff reaches the crossed set.** `CLAUDE.md`: nothing filed after the
triggering report enters the input. The crossed four reports are not a bundle
and carry no manifest of their own, so nothing else gates them -- and the fixed
pairing does not respect the cutoff: on the twelve as they stand, seven of the
twelve pairings put the partner's annual report *after* the filing being scored,
AAPL's partner CARR by ninety-seven days. So the run being scored is asked what
filing it is scoring -- its `input_manifest.json`, whose `filing_date` is the
triggering report's own -- and any half written from a later filing is refused
rather than crossed. A directory that carries no manifest is a directory of
reports and not a run: it declares no filing being scored, and the control block
records `scored_filing_date: null` so an ungated file says so in its own text.
Whoever owns `docs/CHECKLIST.md` §8 has a pairing rule to settle; until then the
cutoff wins and those seven pairings are refused.

**Citations resolve against the four reports the supervisor saw.** `CLAUDE.md`:
an item carries an upstream id that Python verifies, and a failed item is
dropped and counted. Here the upstream *is* the crossed set, so an item citing
an id that none of the four reports carries is dropped and counted in the
control block. An item citing nothing at all is left standing: requiring a
citation is `src/quote_gate.py`'s rule at the layer that owns the report, and a
control that added it would be measuring two changes at once.

**The control file is never merged into the pipeline's number.** It carries a
`control` block naming the scorecard row it is scored on, the company each half
came from, the run directory and accession each half came from, the filing being
scored, and what was dropped -- so a file that reached the wrong place can be
told from a prediction by reading it, not by trusting its name.
"""

from __future__ import annotations

import json
from pathlib import Path

from src import assemble_bundle, cutoff_guard, quote_gate
from src.fetch_fixtures import TICKERS

# The twelve in ticker order. See the module docstring for the reading.
PAIRING_ORDER = tuple(sorted(TICKERS))

# The two halves, by the names `docs/INPUT_SPEC.md` §6 gives them. A is the
# company being scored and keeps the numbers side; B supplies the notes side.
NUMBERS_SIDE = ("report_numbers.md", "report_numbers_vs_market.md")
NOTES_SIDE = ("report_notes_text.md", "report_notes_vs_market.md")
REPORTS = NUMBERS_SIDE + NOTES_SIDE

# What a run directory calls the record of the filing it was built from.
MANIFEST = "input_manifest.json"

# One control file and one scorecard row per question.
CONTROL_FILES = {
    "accounting_reliability": "control_shuffled_accounting.json",
    "financial_pressure": "control_shuffled_pressure.json",
}
SCORECARD_ROWS = {
    "accounting_reliability": "shuffled_accounting",
    "financial_pressure": "shuffled_pressure",
}
QUESTIONS = tuple(CONTROL_FILES)

CONTROL_NAME = "shuffled_report"
RULES_VERSION = "0.1"

# The prediction schema, `docs/CHECKLIST.md` §7. `question` and `rules_version`
# are this module's to write -- the supervisor is answering the question it was
# handed -- so they are not asked of the predictor. `continuous` is financial
# pressure only, which the schema says in those words, so it is required on one
# question and refused on the other rather than merely tolerated on both.
PREDICTED_KEYS = ("checklist", "events", "explanations", "market_direction",
                  "tier", "top_signals")
CONTINUOUS = "continuous"
CONTINUOUS_QUESTION = "financial_pressure"

# The abstention `docs/CHECKLIST.md` §7 allows, which is where a market call
# whose basis resolves to nothing lands: the field cannot leave, so it degrades.
INSUFFICIENT = "insufficient"


class ControlError(Exception):
    """The control cannot be run as `docs/CHECKLIST.md` §8 describes it."""


def one_of_the_twelve(ticker: str, order: tuple[str, ...] = PAIRING_ORDER) -> str:
    """The ticker in upper case, or a refusal naming the twelve.

    The twelve are the whole population of this control: a thirteenth company
    has no reports on record, no pairing and no scorecard row, so a run named
    for one is a run that could not be scored.
    """
    ticker = ticker.upper()
    if ticker not in order:
        raise ControlError(f"{ticker} is not one of the twelve: {', '.join(order)}")
    return ticker


def partner(ticker: str, order: tuple[str, ...] = PAIRING_ORDER) -> str:
    """Company B for this company: the next in the twelve, wrapping around."""
    ticker = one_of_the_twelve(ticker, order)
    return order[(order.index(ticker) + 1) % len(order)]


def named_company(name: str, text: str) -> str:
    """The company a report names on its own first line.

    Every report opens `# TICKER — what it is`, so the heading is what a half
    can be identified by without parsing a line of the body. A report that opens
    with no heading names no company and cannot be placed on either side.
    """
    first = text.split("\n", 1)[0].strip()
    heading = first[2:].split() if first.startswith("# ") else []
    if not heading:
        raise ControlError(
            f"{name} does not open with a heading naming the company it is "
            "about, so nothing in it says whose half it is")
    return one_of_the_twelve(heading[0])


def named_accession(name: str, text: str) -> str:
    """The accession every item id in a report begins with.

    `docs/INPUT_SPEC.md` §2.2 builds an item id on the accession of the filing
    the item came from, so a report carrying two of them was written from two
    filings and is not one run's half.
    """
    found = {identifier.split(":", 1)[0]
             for identifier in assemble_bundle.paragraph_ids(text)}
    if not found:
        raise ControlError(
            f"{name} carries no item id, so nothing in it says which filing it "
            "was written from")
    if len(found) > 1:
        raise ControlError(
            f"{name} carries items from {', '.join(sorted(found))}. One report "
            "is one run's, and a half assembled from two filings is not one")
    return found.pop()


def _half(bundle_root, names: tuple[str, ...]) -> dict:
    """One side of the crossing, read for what its own reports say it is.

    Whole files, byte for byte as the bundle holds them: what is being broken is
    the correspondence between the two sides, and a control that edited a report
    would be breaking something else as well and could not say which one the
    score answered. Only the heading and the item ids are read, and only to say
    whose half this is and which filing it was written from.
    """
    text = {}
    for name in names:
        try:
            text[name] = cutoff_guard.load_bundle_file(bundle_root, name)
        except cutoff_guard.CutoffGuardError as exc:
            raise ControlError(
                f"the shuffled control needs {name}: {exc}") from exc

    companies = {name: named_company(name, body) for name, body in text.items()}
    if len(set(companies.values())) > 1:
        named = ", ".join(f"{name} is {who}'s" for name, who in sorted(companies.items()))
        raise ControlError(
            f"{Path(bundle_root).resolve()} holds more than one company's "
            f"reports on one side: {named}. One half is one company's")
    accessions = {name: named_accession(name, body) for name, body in text.items()}
    if len(set(accessions.values())) > 1:
        named = ", ".join(f"{name} is {which}" for name, which in sorted(accessions.items()))
        raise ControlError(
            f"{Path(bundle_root).resolve()} holds reports from more than one "
            f"filing on one side: {named}. One half is one run's")
    return {"from": next(iter(companies.values())),
            "run": str(Path(bundle_root).resolve()),
            "accession": next(iter(accessions.values())),
            "reports": text}


def crossed(numbers_bundle, notes_bundle) -> dict[str, str]:
    """The four reports a shuffled supervisor sees: two out of each bundle.

    Each side is read for what it says about itself on the way through, and the
    text handed on is the text on disk. Whether the two sides are two companies
    is `run`'s to refuse, because that is the pair and not a half.
    """
    numbers = _half(numbers_bundle, NUMBERS_SIDE)
    notes = _half(notes_bundle, NOTES_SIDE)
    return {**numbers["reports"], **notes["reports"]}


def scored_filing(run_directory):
    """The filing date the run being scored declares, or None when it declares none.

    A run directory records what it was built from in `input_manifest.json`, and
    `src/assemble_bundle.py` puts the triggering report's own filing date under
    `filing_date` -- which is the cutoff, in those words. A directory holding
    four reports and no manifest is not a run and declares no filing; a manifest
    that is there but says nothing readable is a broken record and is refused,
    because an absent date is not an early date.
    """
    if not cutoff_guard.bundle_files(run_directory, MANIFEST):
        return None
    try:
        manifest = json.loads(cutoff_guard.load_bundle_file(run_directory, MANIFEST))
    except (cutoff_guard.CutoffGuardError, ValueError) as exc:
        raise ControlError(
            f"{Path(run_directory) / MANIFEST} does not read as JSON: {exc}") from exc
    if not isinstance(manifest, dict):
        raise ControlError(
            f"{Path(run_directory) / MANIFEST} is not an object, so it names no "
            "filing being scored")
    try:
        return cutoff_guard.parse_date(manifest.get("filing_date"),
                                       f"{MANIFEST} filing_date")
    except cutoff_guard.CutoffGuardError as exc:
        raise ControlError(
            f"{Path(run_directory) / MANIFEST} names no filing date this control "
            f"could check the crossed reports against: {exc}") from exc


def filed(ticker: str, accession: str):
    """When the filing behind one half's reports was filed, off the manifests."""
    try:
        rows = cutoff_guard.documents(ticker)
    except cutoff_guard.CutoffGuardError as exc:
        raise ControlError(f"{ticker} has no record to date {accession}: {exc}") from exc
    dates = {row.get("filing_date") for row in rows
             if row.get("accession") == accession}
    if not dates:
        raise ControlError(
            f"no manifest records {accession} for {ticker} — refused, because a "
            "report written from a filing nobody recorded has no filing date to "
            "check against the one being scored")
    if len(dates) > 1:
        raise ControlError(
            f"{ticker} records {accession} filed on "
            f"{', '.join(sorted(str(one) for one in dates))} — one accession is "
            "one filing on one day")
    try:
        return cutoff_guard.parse_date(dates.pop(), f"{ticker} {accession} filing_date")
    except cutoff_guard.CutoffGuardError as exc:
        raise ControlError(str(exc)) from exc


def _within_cutoff(side: str, half: dict, scored) -> None:
    """Refuse a half written from a filing later than the one being scored."""
    when = filed(half["from"], half["accession"])
    if when > scored:
        raise ControlError(
            f"the {side} half is {half['from']}'s {half['accession']}, filed "
            f"{when}, and the filing being scored was filed {scored}. Nothing "
            "filed after the triggering report enters the input (CLAUDE.md), "
            "so the pair is refused rather than crossed")


def declared_ids(reports: dict[str, str]) -> set[str]:
    """Every item id the four crossed reports carry.

    One id names one item, and across a crossed pair that holds without
    counting: the two halves are two companies' reports and an item id begins
    with the accession of the filing it came from, so a repeat would mean one
    filing on both sides -- which is the pair this module refuses outright.
    """
    return {identifier for text in reports.values()
            for identifier in assemble_bundle.paragraph_ids(text)}


def _unresolved(item, declared: set[str]) -> list:
    """The citations this item makes that none of the four reports carries."""
    return [one for one in quote_gate.citations(item)
            if not isinstance(one, str) or one not in declared]


def _a_list(question: str, key: str, value):
    """One list the schema promised, or a refusal rather than an iteration over it."""
    if not isinstance(value, list):
        raise ControlError(
            f"the {question} answer gives {key} as {type(value).__name__}, and "
            "docs/CHECKLIST.md §7 gives it as a list")
    return value


def resolved(question: str, answer: dict, declared: set[str]) -> tuple[dict, list[dict]]:
    """The answer with every item citing nothing in the crossed set taken out.

    A checklist entry goes whole, because that is what the gate does with an
    item, and a `top_signals` entry naming a key that left goes with it.
    `market_direction` cannot go -- `docs/CHECKLIST.md` §7 requires the field --
    so it degrades to the abstention §7 already allows and the drop is counted
    like any other.
    """
    kept, dropped = dict(answer), []

    def drop(identifier: str, missing: list) -> None:
        dropped.append({"item_id": identifier,
                        "reason": f"the citation {missing[0]!r} is in none of "
                                  "the four crossed reports"})

    standing = []
    for entry in _a_list(question, "checklist", answer["checklist"]):
        if not isinstance(entry, dict) or not isinstance(entry.get("key"), str):
            raise ControlError(
                f"a {question} checklist entry carries no key, and an item with "
                "no name can neither be cited nor dropped by name")
        missing = _unresolved(entry, declared)
        if missing:
            drop(f"{question}:checklist:{entry['key']}", missing)
        else:
            standing.append(entry)
    kept["checklist"] = standing

    names = {entry["key"] for entry in standing}
    kept["top_signals"] = [one for one in
                           _a_list(question, "top_signals", answer["top_signals"])
                           if one in names]

    market = answer["market_direction"]
    missing = _unresolved(market, declared) if isinstance(market, dict) else []
    if missing:
        drop(f"{question}:market_direction", missing)
        kept["market_direction"] = {"p_up": INSUFFICIENT, "basis": []}
    return kept, dropped


def provenance(numbers: dict, notes: dict, question: str, *, scored_filing_date,
               dropped: list[dict]) -> dict:
    """Which run each half came from, as the control file records it.

    `numbers` and `notes` are the two half records: the company each one's own
    reports name, the run directory it was read out of, and the accession its
    item ids carry. The directory and the accession are the part a label cannot
    forge, which is why they are here beside the tickers.
    """
    return {
        "name": CONTROL_NAME,
        "scorecard_row": SCORECARD_ROWS[question],
        "numbers_from": numbers["from"],
        "numbers_run": numbers["run"],
        "numbers_accession": numbers["accession"],
        "notes_from": notes["from"],
        "notes_run": notes["run"],
        "notes_accession": notes["accession"],
        "scored_filing_date": str(scored_filing_date) if scored_filing_date else None,
        "reports": {name: (numbers["from"] if name in NUMBERS_SIDE else notes["from"])
                    for name in REPORTS},
        "dropped_items": [dict(row) for row in dropped],
        "counts": {"dropped_items": len(dropped)},
    }


def _predicted(question: str, answer) -> dict:
    """The supervisor's answer, checked against the schema before it is written."""
    if not isinstance(answer, dict):
        raise ControlError(
            f"the supervisor answered {question} with {type(answer).__name__}, "
            "and a control file holds a prediction")
    missing = [key for key in PREDICTED_KEYS if key not in answer]
    if missing:
        raise ControlError(
            f"the {question} answer has no {', '.join(missing)}; a control is "
            "scored on the same targets as the pipeline and cannot be short of "
            "them (docs/CHECKLIST.md §7)")
    wants_continuous = question == CONTINUOUS_QUESTION
    if wants_continuous and CONTINUOUS not in answer:
        raise ControlError(f"the {question} answer has no {CONTINUOUS}, which the "
                           "schema requires of this question")
    if not wants_continuous and CONTINUOUS in answer:
        raise ControlError(f"the {question} answer carries {CONTINUOUS}, which the "
                           "schema gives to financial pressure alone")
    return dict(answer)


def _rendered(payload: dict) -> str:
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def _writable(out, name: str, text: str) -> Path:
    """Where one control file will land, refusing one already on record.

    A run directory is append-only: a new file may be added to it, and an
    existing one is never rewritten. A correction is a new run. Rewriting the
    identical bytes changes nothing on record and so is not a change.
    """
    folder = Path(out)
    if not folder.is_dir():
        raise ControlError(f"{folder} is not a directory to write a control into")
    if cutoff_guard.bundle_files(folder, name) and \
            cutoff_guard.load_bundle_file(folder, name) != text:
        raise ControlError(
            f"{folder / name} is already on record with different content. A "
            "control file is written once; a correction is a new run.")
    return folder / name


def run(numbers_from: str, notes_from: str, *, numbers_bundle, notes_bundle,
        out, predictor, rules_version: str = RULES_VERSION) -> dict:
    """Both control files for one crossed pair, and what was crossed to get them.

    `predictor(question, reports) -> dict` is the one model call per question:
    the pipeline's own supervisor, handed the crossed four reports and nothing
    else. It is called once for each question, on the same crossed evidence.
    """
    numbers_from, notes_from = one_of_the_twelve(numbers_from), one_of_the_twelve(notes_from)
    if Path(numbers_bundle).resolve() == Path(notes_bundle).resolve():
        raise ControlError(
            f"both halves would come out of {Path(numbers_bundle).resolve()}. "
            "Two companies' reports are two bundles.")

    numbers = _half(numbers_bundle, NUMBERS_SIDE)
    notes = _half(notes_bundle, NOTES_SIDE)
    if numbers["from"] == notes["from"]:
        raise ControlError(
            f"both halves are {numbers['from']}'s own reports: {numbers['run']} "
            f"and {notes['run']} each hold reports {numbers['from']} wrote about "
            "itself. A supervisor given one company's own numbers and notes is "
            "the real run, not the shuffled control -- the control is the two "
            "halves not corresponding.")
    for side, half, label in (("numbers", numbers, numbers_from),
                              ("notes", notes, notes_from)):
        if half["from"] != label:
            raise ControlError(
                f"the {side} half is labelled {label} and its reports are "
                f"{half['from']}'s, out of {half['run']}. The label is what the "
                "control file would carry, so it is the reports that settle it.")

    scored = scored_filing(numbers_bundle)
    if scored is not None:
        _within_cutoff("numbers", numbers, scored)
        _within_cutoff("notes", notes, scored)

    reports = {**numbers["reports"], **notes["reports"]}
    declared = declared_ids(reports)

    # Both answers, and both destinations, before either file is opened. A
    # control is two rows of one scorecard, and a run that wrote one of them and
    # then refused the other would leave a half-crossed pair on record in a
    # directory where nothing may be rewritten to finish it.
    rendered, drops = {}, {}
    for question in QUESTIONS:
        answer = _predicted(question, predictor(question, dict(reports)))
        answer, drops[question] = resolved(question, answer, declared)
        answer.update(question=question, rules_version=rules_version,
                      control=provenance(numbers, notes, question,
                                         scored_filing_date=scored,
                                         dropped=drops[question]))
        rendered[question] = _rendered(answer)
    written = {question: _writable(out, CONTROL_FILES[question], text)
               for question, text in rendered.items()}

    for question, path in written.items():
        path.write_text(rendered[question], encoding="utf-8")
    return {"numbers_from": numbers["from"], "notes_from": notes["from"],
            "numbers_run": numbers["run"], "notes_run": notes["run"],
            "numbers_accession": numbers["accession"],
            "notes_accession": notes["accession"],
            "scored_filing_date": scored,
            "reports": reports, "dropped": drops, "files": written}
