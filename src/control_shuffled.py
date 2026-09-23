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
`pairing_order()` below and nothing else depends on it, so a correction is one
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

**The answer is checked by the one function both controls call.** Before any
citation is resolved, the supervisor's answer goes through
`src/prediction_schema.py`, which holds `docs/CHECKLIST.md` §7 once and which
the single-agent control calls too, so the two controls cannot apply two
readings of one schema. `evidence` is the argument: this supervisor's upstream
is four reports, so §7's own `upstream_item_id` is the whole of it.

**One run is one manifest, and the files land in the scored run.** Two bundles
were told apart by their paths, which a copy makes two of and a link one of: a
copy of the scored run, carrying the partner's notes reports in place of its
own, crossed and was written as though its notes had come from a second run.
`run_identity` reads the manifest each directory committed instead, and each
half's manifest is held to the half's own reports, the notes side included,
which nobody had read. Where the two files may go is `destination`'s, read off
`docs/INPUT_SPEC.md` §6: in the scored run's directory, never inside any run's
per-agent input tree, which that paragraph makes the isolation boundary, and
never through a link. Nothing said so before, and a control pointed into
another run's supervisor directory wrote both files there.

**The control file is never merged into the pipeline's number.** It carries a
`control` block naming the scorecard row it is scored on, the company each half
came from, the run directory and accession each half came from, the filing being
scored, and what was dropped -- so a file that reached the wrong place can be
told from a prediction by reading it, not by trusting its name.
"""

from __future__ import annotations

import json
from pathlib import Path

from src import (agent_inputs, assemble_bundle, cutoff_guard,
                 prediction_schema, quote_gate, universe)


def pairing_order() -> tuple[str, ...]:
    """The twelve in ticker order. See the module docstring for the reading.

    Read from `universe.json` when it is called rather than fixed when this
    module is imported, so a thirteenth company is a row in a file and not an
    edit here.
    """
    return tuple(sorted(universe.tickers()))


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

# `docs/CHECKLIST.md` §7's `question` and `rules_version` are this module's to
# write -- the supervisor is answering the question it was handed -- so they
# are not asked of the predictor, and `src/prediction_schema.py` refuses them in
# its answer. Every other field of §7 is checked there, once, for both controls.
#
# `evidence` is the one field the two controls are allowed to differ on, and it
# is the argument. The sibling's evidence also carries `quote`, because its
# upstream is the committed filing and an id there names a paragraph; this
# supervisor's upstream is four reports, so §7's own shape is the whole of it.
EVIDENCE_FIELDS = prediction_schema.EVIDENCE_FIELDS


class ControlError(Exception):
    """The control cannot be run as `docs/CHECKLIST.md` §8 describes it."""


def one_of_the_twelve(ticker: str, order: tuple[str, ...] | None = None) -> str:
    """The ticker in upper case, or a refusal naming the twelve.

    The twelve are the whole population of this control: a thirteenth company
    has no reports on record, no pairing and no scorecard row, so a run named
    for one is a run that could not be scored. `order` defaults to
    `pairing_order()` asked at this call, not a tuple bound when the module was
    imported, so a row appended to `universe.json` is in the population without
    a restart.
    """
    order = pairing_order() if order is None else order
    ticker = ticker.upper()
    if ticker not in order:
        raise ControlError(f"{ticker} is not one of the twelve: {', '.join(order)}")
    return ticker


def partner(ticker: str, order: tuple[str, ...] | None = None) -> str:
    """Company B for this company: the next in the twelve, wrapping around.

    `order` defaults to `pairing_order()` asked at this call, like
    `one_of_the_twelve`'s, so a row appended to `universe.json` is in the
    pairing without a restart.
    """
    order = pairing_order() if order is None else order
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

    Everything that is true of a pair rather than of a half: two runs, two
    companies, each half the run its own manifest names, and both halves written
    from filings at or before the one being scored. `run` adds the label check,
    because a label is a caller's claim and not something a pair of directories
    carries.
    """
    numbers = _half(numbers_bundle, NUMBERS_SIDE)
    notes = _half(notes_bundle, NOTES_SIDE)
    one_run = run_identity(numbers_bundle)
    if one_run == run_identity(notes_bundle):
        kind, which = one_run
        if kind == "manifest":
            raise ControlError(
                f"both halves would come out of one run, {which}: "
                f"{numbers['run']} and {notes['run']} each carry its manifest. A "
                "run is the manifest it committed and not the directory it sits "
                "in -- a copy of one run is that run, and so is a link to it")
        raise ControlError(
            f"both halves would come out of {which}. Two companies' reports "
            "are two bundles.")
    if numbers["from"] == notes["from"]:
        raise ControlError(
            f"both halves are {numbers['from']}'s own reports: {numbers['run']} "
            f"and {notes['run']} each hold reports {numbers['from']} wrote about "
            "itself. A supervisor given one company's own numbers and notes is "
            "the real run, not the shuffled control -- the control is the two "
            "halves not corresponding.")
    # A half is the run its manifest names, so the manifest has to be the
    # half's own. The numbers side was held to this for the cutoff's sake -- the
    # date is read off the filing the manifest names -- and the notes side never
    # had its manifest read at all, so the run it named could be any run and
    # the comparison above would be comparing a label.
    for bundle_root, half in ((numbers_bundle, numbers), (notes_bundle, notes)):
        named = committed_run(bundle_root)
        if named is not None and named != half["accession"]:
            raise ControlError(
                f"{Path(bundle_root).resolve() / MANIFEST} says the run is "
                f"{named} and its own reports were written from "
                f"{half['accession']}. A half is the run its manifest names, and "
                "one that names two filings has not said which one it is")

    declared = scored_filing(numbers_bundle)
    if declared is None:
        # A directory of reports declares no filing being scored, and the gate
        # used to come off with it -- the one route through this module with no
        # cutoff at all, and the route a pair of report directories takes. The
        # numbers half declares one all the same: its accession is on record
        # with a filing date, which is what `filed` reads for both halves.
        scored, scored_basis = filed(numbers["from"], numbers["accession"]), HALF_BASIS
    else:
        # The manifest names the numbers half's own filing -- the loop above
        # refused one that did not -- so the date it carries is that filing's.
        scored, scored_basis = declared["filing_date"], MANIFEST_BASIS
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


def _manifest(directory) -> dict | None:
    """A directory's committed `input_manifest.json`, or None when it carries none.

    One that is there but does not read is a broken record and is refused: an
    absent date is not an early date, and an absent accession is not another
    run.
    """
    if not cutoff_guard.bundle_files(directory, MANIFEST):
        return None
    try:
        manifest = json.loads(cutoff_guard.load_bundle_file(directory, MANIFEST))
    except (cutoff_guard.CutoffGuardError, ValueError) as exc:
        raise ControlError(
            f"{Path(directory) / MANIFEST} does not read as JSON: {exc}") from exc
    if not isinstance(manifest, dict):
        raise ControlError(
            f"{Path(directory) / MANIFEST} is not an object, so it names no filing")
    return manifest


def run_rules_version(numbers_bundle, notes_bundle, asked=None):
    """The rules version both control files carry: the scored run's own.

    It used to be "0.1", written into every control file whatever run it
    scored -- `docs/CHECKLIST.md` §7's example, when no run carried that
    version and a pilot run carries "pilot" (the owner's decision of
    2026-09-23). A prediction is scored against its own rules version, and a
    control is scored beside the run it crosses, so the version is the one that
    run's `input_manifest.json` carries, null included.

    Every manifest the pair carries is read, and so is `asked`, the caller's
    word for a pair of report directories that carry none; they must all say
    one thing. Two halves written under two rules versions are refused -- the
    real run read both sides under one set of rules, and a crossed pair that
    did not measures the rules change along with the crossing. Nothing to read
    at all is refused rather than defaulted, which is what "0.1" was.
    """
    said = []
    for side, bundle in (("numbers", numbers_bundle), ("notes", notes_bundle)):
        manifest = _manifest(bundle)
        if manifest is None:
            continue
        if "rules_version" not in manifest:
            raise ControlError(
                f"{Path(bundle) / MANIFEST} names no rules_version, and the {side} "
                "half's run was read under one; a control file carries it")
        said.append((f"the {side} half's manifest", manifest["rules_version"]))
    if asked is not None:
        said.append(("the caller", asked))
    if not said:
        raise ControlError(
            "neither half carries a manifest and no rules version was named, so "
            "the control files would carry a version nobody said; name the run's")
    if len({json.dumps(version) for _, version in said}) > 1:
        named = ", ".join(f"{who} {version!r}" for who, version in said)
        raise ControlError(
            f"the pair says two rules versions: {named}. The real run read both "
            "sides under one, and a control crossing two measures the rules "
            "change along with the crossing")
    return said[0][1]


def committed_run(directory) -> str | None:
    """Which run a directory is: the accession its committed manifest names.

    `src/assemble_bundle.py` writes the triggering report's accession into
    `input_manifest.json` and files the run under it, so that is the run's name
    wherever the directory sits. None when the directory carries no manifest --
    a directory of reports, which is not a run.
    """
    manifest = _manifest(directory)
    if manifest is None:
        return None
    accession = manifest.get("accession")
    if not isinstance(accession, str) or not accession:
        raise ControlError(
            f"{Path(directory) / MANIFEST} names no accession, so it does not say "
            "which run the directory is")
    return accession


def run_identity(directory) -> tuple[str, str]:
    """What makes two directories one run: the manifest, and failing that the place.

    The place used to be the whole of it, and a path is what a copy changes and
    a link does not: a copy of the scored run read as a second run, and a link
    to it as the same one. A run is the manifest it committed. A directory that
    committed none has nothing but its place to be told apart by, so its
    resolved path is what it is compared on -- one directory of reports handed
    in as both halves is still one directory.
    """
    accession = committed_run(directory)
    if accession is not None:
        return ("manifest", accession)
    return ("directory", str(Path(directory).resolve()))


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
    manifest = _manifest(run_directory)
    if manifest is None:
        return None
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
    if (market.get("p_up") != prediction_schema.INSUFFICIENT
            or quote_gate.citations(market)):
        reason = _drop_reason(market, declared)
        if reason:
            drop(f"{question}:market_direction", reason)
            kept["market_direction"] = {"p_up": prediction_schema.INSUFFICIENT,
                                         "basis": []}
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


def _predicted(question: str, answer) -> dict:
    """The supervisor's answer against `docs/CHECKLIST.md` §7, field by field.

    The gate below reads citations, so a field with no citations in it used to
    pass through untouched whatever it held: `p_up: "up"`, `p_up: 1.7`,
    `tier: "banana"`, `events: "lots"` were all written standing and uncounted.
    The check is `src/prediction_schema.py`'s, the one the sibling control
    calls; what is this control's own is the sentence for a supervisor that
    answered with something other than an object, because the supervisor is
    who answered.
    """
    if not isinstance(answer, dict):
        raise ControlError(
            f"the supervisor answered {question} with {type(answer).__name__}, "
            "and a control file holds a prediction")
    try:
        prediction_schema.check(answer, question, evidence=EVIDENCE_FIELDS)
    except prediction_schema.SchemaError as exc:
        raise ControlError(str(exc)) from exc
    return dict(answer)


def _rendered(payload: dict) -> str:
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def destination(out, scored: dict) -> Path:
    """Where the two control files may land, or a refusal before anyone is asked.

    `docs/INPUT_SPEC.md` §6 lists both files in one run's committed bundle,
    under `runs/{ticker}/{accession}/`, and in the same paragraph makes "each
    agent's input directory" the isolation boundary, "committed as what it
    saw"; `docs/HOW_WE_WORK.md` §1.6 says it again. So, in order:

    - never inside a run's per-agent input tree, whoever's run it is, and not
      through a link into one -- a file written there is part of what that tree
      records an agent as having seen;
    - when the directory is a run, the run being scored: `scored` is the numbers
      half, which is company A's, and in the partner's run the two files would
      sit under the names §6 gives the partner's own shuffled control. Which run
      a directory is, is its manifest -- a copy of the scored run is the scored
      run. A directory carrying no manifest is not a run and says nothing
      either way, which is the route a pair of report directories takes;
    - no link at either file's name. `write_text` follows one, and a link whose
      target does not exist yet is not a file, so `_writable` would read it as
      absent and the write would create the target wherever it points.

    Asked before the supervisor is, because an answer with nowhere it may go is
    a call paid for nothing.
    """
    folder = Path(out)
    if not folder.is_dir():
        raise ControlError(f"{folder} is not a directory to write a control into")
    held = agent_inputs.input_tree_holding(folder)
    if held is not None:
        raise ControlError(
            f"{folder} is inside {held}, a run's per-agent input tree. That tree "
            "is committed as what each agent saw, so a control file written there "
            "rewrites another agent's record of its input; a control's files "
            "land in the run directory, beside the bundle")
    which = committed_run(folder)
    if which is not None and which != scored["accession"]:
        raise ControlError(
            f"{folder} is the run of {which}, and this control scores "
            f"{scored['from']}'s {scored['accession']}. The two control files are "
            "the scored run's, and in another run they would sit under the names "
            "that run's own shuffled control is written to")
    linked = [folder / name for name in CONTROL_FILES.values()
              if (folder / name).is_symlink()]
    if linked:
        named = ", ".join(f"{path} to {path.readlink()}" for path in linked)
        raise ControlError(
            f"{named}. A control's file is written where it was handed, never "
            "through a link out of it")
    return folder


def _writable(folder: Path, name: str, text: str) -> Path:
    """Where one control file will land, refusing one already on record.

    A run directory is append-only: a new file may be added to it, and an
    existing one is never rewritten. A correction is a new run. Rewriting the
    identical bytes changes nothing on record and so is not a change. `folder`
    is one `destination` has already allowed.
    """
    if cutoff_guard.bundle_files(folder, name) and \
            cutoff_guard.load_bundle_file(folder, name) != text:
        raise ControlError(
            f"{folder / name} is already on record with different content. A "
            "control file is written once; a correction is a new run.")
    return folder / name


def run(numbers_from: str, notes_from: str, *, numbers_bundle, notes_bundle,
        out, predictor, rules_version: str | None = None) -> dict:
    """Both control files for one crossed pair, and what was crossed to get them.

    `predictor(question, reports) -> dict` is the one model call per question:
    the pipeline's own supervisor, handed the crossed four reports and nothing
    else. It is called once for each question, on the same crossed evidence.

    `rules_version` is only for a pair that carries no manifest; the version
    the files carry is `run_rules_version`'s, and a caller who names one the
    manifests disagree with is refused there.
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
    folder = destination(out, numbers)
    version = run_rules_version(numbers_bundle, notes_bundle, rules_version)

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
        answer.update(question=question, rules_version=version,
                      control=provenance(numbers, notes, question,
                                         scored_filing_date=scored,
                                         scored_filing_date_from=scored_basis,
                                         dropped=drops[question]))
        rendered[question] = _rendered(answer)
    written = {question: _writable(folder, CONTROL_FILES[question], text)
               for question, text in rendered.items()}

    for question, path in written.items():
        path.write_text(rendered[question], encoding="utf-8")
    return {"numbers_from": numbers["from"], "notes_from": notes["from"],
            "numbers_run": numbers["run"], "notes_run": notes["run"],
            "numbers_accession": numbers["accession"],
            "notes_accession": notes["accession"],
            "scored_filing_date": scored,
            "reports": reports, "dropped": drops, "files": written}
