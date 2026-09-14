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
reports and not a run, and it declares no filing being scored -- but the numbers
half does: its accession is on record with a filing date, and that is the date
the notes half may not be later than. Leaving the gate off when the manifest was
absent was the one route with no gate at all, and it is the route the fixture
pair took. The control block records the date and where it came from, so a file
says in its own text which of the two answered. Whoever owns `docs/CHECKLIST.md`
§8 has a pairing rule to settle; until then the cutoff wins and those seven
pairings are refused.

**Citations resolve against the four reports the supervisor saw.** `CLAUDE.md`:
an item carries an upstream id that Python verifies, and a failed item is
dropped and counted. Here the upstream *is* the crossed set, so an item citing
an id that none of the four reports carries is dropped and counted in the
control block -- and so is an item citing nothing at all, in the sentence
`src/quote_gate.py` uses for it. Leaving those standing made the two controls
apply different gates to one schema: `src/control_single_agent.py` drops them
through `quote_gate.citation_drop_reason`, so a supervisor citing nothing kept
every item here and lost them there, and the difference between the two controls
would have been the gate rather than the crossing.

**The control file is never merged into the pipeline's number.** It carries a
`control` block naming the scorecard row it is scored on, the company each half
came from, the run directory and accession each half came from, the filing being
scored, and what was dropped -- so a file that reached the wrong place can be
told from a prediction by reading it, not by trusting its name.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

from src import assemble_bundle, cutoff_guard, quote_gate
from src.fetch_fixtures import TICKERS

# The twelve in ticker order. See the module docstring for the reading.
PAIRING_ORDER = tuple(sorted(TICKERS))

# The two halves, by the names `docs/INPUT_SPEC.md` §6 gives them. A is the
# company being scored and keeps the numbers side; B supplies the notes side.
# Where the filing being scored was read from, as the control file records it.
MANIFEST_BASIS = "the run's own input_manifest.json"
HALF_BASIS = "the numbers half's accession, on record in its ticker's manifest"

NUMBERS_SIDE = ("report_numbers.md", "report_numbers_vs_market.md")
NOTES_SIDE = ("report_notes_text.md", "report_notes_vs_market.md")
REPORTS = NUMBERS_SIDE + NOTES_SIDE

# What each report says it is, after the company, on its own first line. The
# heading was read for the company and the rest of it for nothing, so a file
# named `report_notes_text.md` holding the numbers report crossed cleanly and
# the supervisor was handed one company's numbers twice. `tests/` asserts this
# map against all twenty-four committed reports rather than agreeing with it.
REPORT_HEADING = {
    "report_numbers.md": "numbers reader",
    "report_numbers_vs_market.md": "numbers versus market",
    "report_notes_text.md": "notes-text reader",
    "report_notes_vs_market.md": "notes versus market",
}

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
# §7 gives `market_direction` a probability and the ids under it, and nothing
# else. The sibling control refuses any other shape in its schema check, so this
# one does too -- a bare float reaches the gate below as something with no
# citations to resolve and was written standing.
MARKET_FIELDS = ("p_up", "basis")

# The rest of §7, field by field. Every value below is read out of
# `docs/CHECKLIST.md` §7 and §1, which is also where `src/control_single_agent.py`
# reads them: the two controls answer one schema, and a field one of them checks
# and the other does not is a difference between the controls that is not the
# crossing. They agree here by reading one document rather than by sharing code,
# which is a duplication to remove once both are on main -- it is a row in
# `docs/next_cycle_tasks.md`, not something to do inside this item.
#
# `evidence` carries `upstream_item_id` alone. The sibling's evidence also
# carries `quote`, because its upstream is the committed filing and an id there
# names a paragraph; this supervisor's upstream is four reports, so §7's own
# shape is the whole of it.
CHECKLIST_FIELDS = ("key", "finding", "confidence", "evidence")
CONTINUOUS_FIELDS = ("key", "point", "direction", "low", "high")
EVENT_FIELDS = ("key", "p_within_horizon")
EXPLANATION_FIELDS = ("id", "support", "realization_p")
EVIDENCE_FIELDS = ("upstream_item_id",)
FINDINGS = ("flag", "no_flag", "insufficient")
SUPPORT = ("sufficient", "insufficient", "unknown")
TIERS = ("elevated", "watch", "clear")
TOP_SIGNALS_MAX = 5



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
    """The company a report names on its own first line, and what it says it is.

    Every report opens `# TICKER — what it is`, so the heading is what a half
    can be identified by without parsing a line of the body. A report that opens
    with no heading names no company and cannot be placed on either side.

    The rest of the heading is read too. It was not, so only the *name* of a
    file said which of the four reports it held -- and a file named
    `report_notes_text.md` holding the numbers report crossed with everything
    checking out: one company, one filing, both sides inside the cutoff, and a
    supervisor handed one company's numbers twice under two names. "Verify the
    reports it crossed" is company, filing and kind.
    """
    first = text.split("\n", 1)[0].strip()
    heading = first[2:].split() if first.startswith("# ") else []
    if not heading:
        raise ControlError(
            f"{name} does not open with a heading naming the company it is "
            "about, so nothing in it says whose half it is")
    company = one_of_the_twelve(heading[0])
    wanted = REPORT_HEADING.get(name)
    said = first.split("—", 1)[1].strip() if "—" in first else ""
    if wanted is not None and said != wanted:
        raise ControlError(
            f"{name} opens {said!r} and a file of that name is the {wanted!r} "
            "report. The name is the caller's word for what is inside; the "
            "heading is the report's own, and a report of the wrong kind under "
            "the right name hands the supervisor one half twice")
    return company


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
    if "" in found:
        raise ControlError(
            f"{name} carries an item id that begins with no accession. An empty "
            "accession names no filing, and `filed` would look it up against the "
            "rows that carry none -- the submissions index and the companyfacts "
            "record, which are catalogues and not filings, and whose recorded "
            "date is the newest filing in them")
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


def _crossed_pair(numbers_bundle, notes_bundle):
    """The two halves and the filing date they are scored against, or a refusal.

    Everything that is true of a pair rather than of a half: two directories,
    two companies, and both halves written from filings at or before the one
    being scored. `run` adds the label check, because a label is a caller's
    claim and not something a pair of directories carries.
    """
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

    declared = scored_filing(numbers_bundle)
    if declared is None:
        # A directory of reports declares no filing being scored, and the gate
        # used to come off with it -- the one route through this module with no
        # cutoff at all, and the route a pair of report directories takes. The
        # numbers half declares one all the same: its accession is on record
        # with a filing date, which is what `filed` reads for both halves.
        scored, scored_basis = filed(numbers["from"], numbers["accession"]), HALF_BASIS
    else:
        scored, scored_basis = declared["filing_date"], MANIFEST_BASIS
        if declared["accession"] != numbers["accession"]:
            raise ControlError(
                f"{Path(numbers_bundle).resolve() / MANIFEST} says the run is "
                f"{declared['accession']} and its own reports were written from "
                f"{numbers['accession']}. The date the cutoff is read off "
                "belongs to the filing the manifest names, so a run that names "
                "two filings has not said which one it is")
        # One filing, one date, held in two places. Comparing the half against
        # the manifest in one direction refused a manifest dated *earlier* than
        # the record and accepted one dated later, which is the direction that
        # loosens the boundary: a manifest saying 2026-08-01 for a filing the
        # record files 2026-02-05 let a notes half from 2026-07-31 through.
        # `src/assemble_bundle.py` writes `filing_date` out of the very row
        # `filed` reads, so any difference at all is a record contradicting
        # itself.
        on_record = filed(numbers["from"], numbers["accession"])
        if scored != on_record:
            raise ControlError(
                f"{Path(numbers_bundle).resolve() / MANIFEST} says "
                f"{numbers['accession']} was filed {scored} and "
                f"{numbers['from']}'s own record says {on_record}. The filing "
                "being scored has one date, and a run whose manifest disagrees "
                "with the record set its own boundary")
    # Only the notes half is gated, and that is the whole of the rule rather
    # than half of it: `scored` *is* the numbers half's own filing date, by one
    # of the two routes above -- either read straight off it, or read off a
    # manifest that has just been proved to name the same accession and the
    # same date. `_within_cutoff("numbers", ...)` compared that date with
    # itself. It was a line no test could ever fail and no input could ever
    # trip, which reads as a check and is a comment.
    _within_cutoff("notes", notes, scored)
    return numbers, notes, scored, scored_basis


def crossed(numbers_bundle, notes_bundle) -> dict[str, str]:
    """The four reports a shuffled supervisor sees: two out of each bundle.

    Every refusal the pair carries runs first. This used to read the two halves
    and hand them straight back while `run` held the checks, so the one function
    the docstring calls "what the supervisor sees" was the one route with no
    cutoff on it and no refusal of a company crossed with itself. Nothing
    outside this module calls it, which is the only reason that was never a
    live leak.
    """
    numbers, notes, _, _ = _crossed_pair(numbers_bundle, notes_bundle)
    return {**numbers["reports"], **notes["reports"]}


def scored_filing(run_directory):
    """The filing date the run being scored declares, or None when it declares none.

    A run directory records what it was built from in `input_manifest.json`, and
    `src/assemble_bundle.py` puts the triggering report's own filing date under
    `filing_date` -- which is the cutoff, in those words. A directory holding
    four reports and no manifest is not a run and declares no filing; a manifest
    that is there but says nothing readable is a broken record and is refused,
    because an absent date is not an early date.

    The accession comes back with the date. The date is only the date of the
    filing the manifest *names*, and a run whose manifest and whose reports name
    two different filings has not said which one it is.
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
        when = cutoff_guard.parse_date(manifest.get("filing_date"),
                                       f"{MANIFEST} filing_date")
    except cutoff_guard.CutoffGuardError as exc:
        raise ControlError(
            f"{Path(run_directory) / MANIFEST} names no filing date this control "
            f"could check the crossed reports against: {exc}") from exc
    accession = manifest.get("accession")
    if not isinstance(accession, str) or not accession:
        raise ControlError(
            f"{Path(run_directory) / MANIFEST} names no accession, so nothing "
            "says the filing date it carries belongs to the filing these "
            "reports were written from")
    return {"filing_date": when, "accession": accession}


def filed(ticker: str, accession: str, *, fixtures_root=cutoff_guard.FIXTURES):
    """When the filing behind one half's reports was filed, off the manifests.

    `fixtures_root` is here for the rule below: no committed manifest records one
    accession twice, and inventing one under `tests/fixtures/` to judge the rule
    would be writing the record this control reads. The test writes its own two
    rows in a directory of its own instead.
    """
    try:
        rows = cutoff_guard.documents(ticker, fixtures_root=fixtures_root)
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


# `src/quote_gate.py`'s own sentence for an item that cites nothing, quoted so
# the two gates say one thing about one failure. It is not imported because it is
# written inline there, inside `citation_drop_reason`.
CITES_NOTHING = "the item cites no upstream item"


def _drop_reason(item, declared: set[str]) -> str | None:
    """Why this item is dropped, or None when it stands.

    The same two failures `quote_gate.citation_drop_reason` names, in the same
    order: an item that cites nothing, then a citation none of the four crossed
    reports carries. That function is not called directly because it also
    requires an item id, and a checklist entry here is named by its key.
    """
    cited = quote_gate.citations(item)
    if not cited:
        return CITES_NOTHING
    for one in cited:
        if not isinstance(one, str) or one not in declared:
            return (f"the citation {one!r} is in none of the four crossed reports")
    return None


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

    def drop(identifier: str, reason: str) -> None:
        dropped.append({"item_id": identifier, "reason": reason})

    standing = []
    for entry in _a_list(question, "checklist", answer["checklist"]):
        if not isinstance(entry, dict) or not isinstance(entry.get("key"), str):
            raise ControlError(
                f"a {question} checklist entry carries no key, and an item with "
                "no name can neither be cited nor dropped by name")
        reason = _drop_reason(entry, declared)
        if reason:
            drop(f"{question}:checklist:{entry['key']}", reason)
        else:
            standing.append(entry)
    kept["checklist"] = standing

    standing_explanations = []
    for entry in _a_list(question, "explanations", answer["explanations"]):
        if not isinstance(entry, dict) or not isinstance(entry.get("id"), str):
            raise ControlError(
                f"a {question} explanation carries no id, and an item with no "
                "name can neither be resolved nor dropped by name")
        # §7 spells this field `id` rather than `upstream_item_id`, and says
        # explanations are assembled from what the supervisors say about those
        # items -- so the id names an upstream item and resolves like one. That
        # reading is inferred from one sentence rather than stated, which is why
        # it is a row in `docs/needs_judgment.md`; until it is decided, an
        # explanation naming an item the crossing removed is dropped and counted
        # like any other citation that resolves against nothing.
        reason = _drop_reason({"upstream_item_id": entry["id"]}, declared)
        if reason:
            drop(f"{question}:explanations:{entry['id']}", reason)
        else:
            standing_explanations.append(entry)
    kept["explanations"] = standing_explanations

    # A signal whose entry was dropped leaves with it, and no second drop row is
    # written: the drop is already on record under the entry's own key, and
    # counting it twice would say two items failed where one did. A signal
    # naming no entry at all never reaches here -- `_predicted` refuses the
    # answer, the way the sibling control does.
    names = {entry["key"] for entry in standing}
    kept["top_signals"] = [one for one in
                           _a_list(question, "top_signals", answer["top_signals"])
                           if one in names]

    # `market_direction` abstains by naming no basis, which `docs/CHECKLIST.md`
    # §7 allows -- but the abstention §7 allows is `p_up: "insufficient"`, not a
    # number resting on an empty basis. A probability standing on nothing is
    # exactly what the abstention is for, and `src/control_single_agent.py`
    # drops it in this same sentence; skipping the field whenever the basis was
    # empty left the two controls applying two gates to one schema. The field
    # cannot be dropped, so it degrades to that same abstention.
    market = answer["market_direction"]
    if market.get("p_up") != INSUFFICIENT or quote_gate.citations(market):
        reason = _drop_reason(market, declared)
        if reason:
            drop(f"{question}:market_direction", reason)
            kept["market_direction"] = {"p_up": INSUFFICIENT, "basis": []}
    return kept, dropped


def provenance(numbers: dict, notes: dict, question: str, *, scored_filing_date,
               scored_filing_date_from: str, dropped: list[dict]) -> dict:
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
        # Which of the two said so: the run's own manifest, or the numbers
        # half's accession on record. A date with no basis is a date nobody can
        # check, and the two are not the same claim.
        "scored_filing_date_from": scored_filing_date_from,
        "reports": {name: (numbers["from"] if name in NUMBERS_SIDE else notes["from"])
                    for name in REPORTS},
        "dropped_items": [dict(row) for row in dropped],
        "counts": {"dropped_items": len(dropped)},
    }


def _fields(entry, expected: tuple[str, ...], where: str) -> None:
    if not isinstance(entry, dict):
        raise ControlError(f"{where} is {type(entry).__name__}, not an object")
    found = tuple(sorted(entry))
    if found != tuple(sorted(expected)):
        raise ControlError(
            f"{where} carries {', '.join(found) or 'no fields'} and "
            f"docs/CHECKLIST.md §7 gives it {', '.join(sorted(expected))}")


def _text(entry, field: str, where: str) -> str:
    value = entry.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ControlError(
            f"{where}.{field} is {value!r}, and the schema gives it a name")
    return value


def _one_of(entry, field: str, allowed: tuple[str, ...], where: str) -> str:
    value = entry.get(field)
    if value not in allowed:
        raise ControlError(
            f"{where}.{field} is {value!r}; the schema allows {', '.join(allowed)}")
    return value


def _number(entry, field: str, where: str, *, low=None, high=None) -> float:
    value = entry.get(field)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ControlError(
            f"{where}.{field} is {value!r}, and the schema gives it a number")
    # An infinity is an instance of `float`, and the range below runs only on a
    # field §7 gives a range to. `point`, `low` and `high` have none, so an
    # infinity there reached `_rendered` untouched and `json.dumps` wrote it as
    # `Infinity` -- a bare token RFC 8259 does not have. A number outside its
    # range costs one item; a number outside JSON costs the file. And nothing
    # downstream would have said so: `json.loads` reads `Infinity` back without
    # complaint unless it is handed a `parse_constant`.
    if not math.isfinite(value):
        raise ControlError(
            f"{where}.{field} is {value!r} — json.dumps spells these Infinity "
            "and NaN, which are not JSON, and a control file the scorer cannot "
            "read back is the prediction lost")
    if low is not None and not low <= value <= high:
        raise ControlError(
            f"{where}.{field} is {value}, outside {low} to {high} — a probability "
            "outside its own range is not a probability")
    return float(value)


def _unique(keys: list[str], where: str) -> None:
    """One indicator, one key — `docs/CHECKLIST.md` §2 says it in those words."""
    repeated = sorted({key for key in keys if keys.count(key) > 1})
    if repeated:
        raise ControlError(
            f"{where} names {', '.join(repeated)} more than once; one indicator, "
            "one key, and a repeated key names a set")


def _predicted(question: str, answer) -> dict:
    """The supervisor's answer against `docs/CHECKLIST.md` §7, field by field.

    The gate below reads citations, so a field with no citations in it used to
    pass through untouched whatever it held: `p_up: "up"`, `p_up: 1.7`,
    `tier: "banana"`, `events: "lots"` were all written standing and uncounted.
    A control file is scored -- §8 scores market direction by Brier and hit rate
    and events by Brier -- so an unscorable value on record is a row of the
    scorecard that cannot be computed, found later and with nothing to recover.
    """
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
    # `continuous` before the closed-prediction check below, because the closed
    # check refuses every field §7 does not give this question -- `continuous` on
    # accounting reliability among them -- and it refuses them all in one
    # sentence. So the sentence naming this field, "the schema gives it to
    # financial pressure alone", was written for a branch nothing could reach:
    # the stray check answered first, and answered less precisely. Asked in this
    # order both rules are reachable and each says its own thing.
    if wants_continuous and CONTINUOUS not in answer:
        raise ControlError(f"the {question} answer has no {CONTINUOUS}, which the "
                           "schema requires of this question")
    if not wants_continuous and CONTINUOUS in answer:
        raise ControlError(f"the {question} answer carries {CONTINUOUS}, which the "
                           "schema gives to financial pressure alone")
    # Every nested object below is closed and the prediction itself was not, so
    # a `scored_filing_date`, a `price_on_reaction_day_60` and a note to the
    # scorer were written into the control file whole, beside the audited
    # `scored_filing_date` this module writes in `control`. The sibling closes
    # the prediction in one line; so does this.
    allowed = PREDICTED_KEYS + ((CONTINUOUS,) if wants_continuous else ())
    stray = sorted(set(answer) - set(allowed))
    if stray:
        raise ControlError(
            f"the {question} answer carries {', '.join(stray)}, which "
            "docs/CHECKLIST.md §7 does not give it. `question`, `rules_version` "
            "and `control` are this module's to write, and a field the schema "
            "has no column for is a row of the scorecard nobody can score")

    checklist = _a_list(question, "checklist", answer["checklist"])
    for position, entry in enumerate(checklist, start=1):
        where = f"checklist[{position}]"
        _fields(entry, CHECKLIST_FIELDS, where)
        _text(entry, "key", where)
        _one_of(entry, "finding", FINDINGS, where)
        _number(entry, "confidence", where, low=0, high=1)
        evidence = _a_list(question, f"{where}.evidence", entry["evidence"])
        for index, cited in enumerate(evidence, start=1):
            cited_where = f"{where}.evidence[{index}]"
            _fields(cited, EVIDENCE_FIELDS, cited_where)
            _text(cited, "upstream_item_id", cited_where)
    _unique([entry["key"] for entry in checklist], "checklist")

    if wants_continuous:
        continuous = _a_list(question, CONTINUOUS, answer[CONTINUOUS])
        if not continuous:
            raise ControlError(
                "continuous is empty; financial pressure predicts next quarter's "
                "revenue growth, operating margin and operating cash flow")
        for position, entry in enumerate(continuous, start=1):
            where = f"{CONTINUOUS}[{position}]"
            _fields(entry, CONTINUOUS_FIELDS, where)
            _text(entry, "key", where)
            # §7 gives `direction` a string and does not enumerate its values.
            _text(entry, "direction", where)
            point = _number(entry, "point", where)
            low = _number(entry, "low", where)
            high = _number(entry, "high", where)
            if not low <= point <= high:
                raise ControlError(
                    f"{where} puts its point {point} outside its own range "
                    f"{low} to {high}")
        _unique([entry["key"] for entry in continuous], CONTINUOUS)

    events = _a_list(question, "events", answer["events"])
    for position, entry in enumerate(events, start=1):
        where = f"events[{position}]"
        _fields(entry, EVENT_FIELDS, where)
        _text(entry, "key", where)
        _number(entry, "p_within_horizon", where, low=0, high=1)
    _unique([entry["key"] for entry in events], "events")

    explanations = _a_list(question, "explanations", answer["explanations"])
    for position, entry in enumerate(explanations, start=1):
        where = f"explanations[{position}]"
        _fields(entry, EXPLANATION_FIELDS, where)
        _text(entry, "id", where)
        _one_of(entry, "support", SUPPORT, where)
        _number(entry, "realization_p", where, low=0, high=1)
    _unique([entry["id"] for entry in explanations], "explanations")

    market = answer["market_direction"]
    _fields(market, MARKET_FIELDS, "market_direction")
    if market["p_up"] != INSUFFICIENT:
        _number(market, "p_up", "market_direction", low=0, high=1)
    basis = market["basis"]
    if not isinstance(basis, list) or not all(
            isinstance(one, str) and one.strip() for one in basis):
        raise ControlError(
            f"market_direction.basis is {basis!r}; §7 gives it a list of upstream "
            "item ids, and an id that is not a name resolves for nobody")

    _one_of(answer, "tier", TIERS, "the prediction")
    signals = _a_list(question, "top_signals", answer["top_signals"])
    for position, one in enumerate(signals, start=1):
        if not isinstance(one, str) or not one.strip():
            raise ControlError(
                f"top_signals[{position}] is {one!r}, and a signal is the key of "
                "a checklist entry")
    _unique(list(signals), "top_signals")
    if len(signals) > TOP_SIGNALS_MAX:
        raise ControlError(
            f"top_signals names {len(signals)} signals and §7 allows "
            f"{TOP_SIGNALS_MAX}")
    # A signal naming no checklist entry at all is the answer contradicting
    # itself before any citation is resolved, so it is refused here rather than
    # dropped later. `src/control_single_agent.py` refuses it in these words,
    # and one schema gets one gate: the difference between the two controls is
    # the crossing and nothing else. A signal whose entry is dropped *later*,
    # for citing nothing in the crossed set, still leaves quietly with it --
    # that drop is on record under the entry's own key.
    unknown = [one for one in signals
               if one not in {entry["key"] for entry in checklist}]
    if unknown:
        raise ControlError(
            f"top_signals names {', '.join(unknown)}, which no checklist entry "
            "carries — a top signal that names no entry names nothing")
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
    numbers, notes, scored, scored_basis = _crossed_pair(numbers_bundle, notes_bundle)
    for side, half, label in (("numbers", numbers, numbers_from),
                              ("notes", notes, notes_from)):
        if half["from"] != label:
            raise ControlError(
                f"the {side} half is labelled {label} and its reports are "
                f"{half['from']}'s, out of {half['run']}. The label is what the "
                "control file would carry, so it is the reports that settle it.")

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
                                         scored_filing_date_from=scored_basis,
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
