"""8-K item codes for every filing, and the text of the ones that matter.

Three jobs, from the input spec's table:

1. **Item codes and dates for every 8-K**, read from the stored submissions
   index. The index is the only place a filing's item codes are stated — the
   document itself carries them as prose — and `src/fetch_fixtures.py` stores
   it as `tests/fixtures/{ticker}/submissions.json`.
2. **Item 2.02**, the earnings release: paragraphs and tables from exhibit
   99.1. This is the first-reported value and the only source for guidance
   language.
3. **Verbatim bodies** for items 1.01, 4.01, 4.02 and 5.02 — covenant
   amendment, auditor change, non-reliance, officer departure — taken whole
   from the 8-K body, with no selection. A 4.02 non-reliance body is the event
   the accounting-reliability question exists to anticipate.

Every other item (5.07, 7.01, 8.01, 9.01) contributes its code and date only.

4. **The event filings of the window** (`event_filings`): what the store
   fetched for the triggering report under `src/fetch_fixtures.py`'s "event
   filings" -- the bodies of the 8-Ks reporting items 1.02, 2.04, 2.05, 2.06,
   3.01 or 3.03, an auditor change's 8-K with its EX-16 letter, the notices of
   late filing, and the SEC staff's comment letters with the company's
   responses -- made public after the previous 10-K or 10-Q and before the
   triggering report, each read through the gate and carried verbatim under ids
   of its own accession. A letter is in the window by the day EDGAR made it
   public, never by its filing date or the date printed on it. What the window
   holds and the store does not is named, never left out in silence.

    python3.12 -m src.parse_8k --ticker AAPL --out input_8k.md
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    from src import clean_text, cutoff_guard, fetch_fixtures, html_text, interpreter_pin
except ImportError:  # invoked as a plain script
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import clean_text, cutoff_guard, fetch_fixtures, html_text, interpreter_pin

BAD_INPUT = 2

ITEM_CODE = re.compile(r"^\d+\.\d{2}$")
VERBATIM_ITEMS = ("1.01", "4.01", "4.02", "5.02")
EARNINGS_ITEM = "2.02"

# `8-K/A` is an 8-K. Selecting `form == "8-K"` exactly kept every amendment out
# of the item-code list, and `docs/CHECKLIST.md:186` makes "an amendment that
# changes numbers" a primary year-one target. TTMI filed its earnings release
# (`0001193125-26-336163`, items 2.02/9.01) and an amendment carrying the same
# items (`0001193125-26-337923`) on the same day, one day after the 10-Q this
# bundle is for — so the one company where it happened is inside the window.
INDEX_FORMS = ("8-K", "8-K/A")
AMENDMENT_FORMS = ("8-K/A",)

# A notification of late filing. `docs/CHECKLIST.md:67` names an NT 10-K a
# `filing_irregularity` and `:185` names late filing a primary year-one target.
# LFUS filed one on 2025-02-27 and nothing in the pipeline could see it.
LATE_FORMS = ("NT 10-K", "NT 10-Q", "NT 10-K/A", "NT 10-Q/A")

# An item heading in an 8-K body: "Item 5.02 Departure of Directors…".
_BODY_ITEM = re.compile(r"^item\s*(\d+\.\d{2})\b")
_BODY_END = re.compile(r"^signatures?\b|^exhibit index\b")


def item_codes(items: str) -> list[str]:
    """The submissions index's `items` field, as codes. Nothing else is a code."""
    return [code for code in
            (part.strip() for part in (items or "").split(",")) if code]


def submissions(ticker: str, *, fixtures_root=cutoff_guard.FIXTURES) -> dict:
    """The stored submissions index, read through `cutoff_guard.load_index`.

    An index of filings is not itself a filing, so the date gate does not apply
    to the file — see that function. The cutoff applies to the rows, and
    `eight_k_filings` is where it is applied.
    """
    row = cutoff_guard.one_document(ticker, "submissions", "submissions_index",
                                    fixtures_root=fixtures_root)
    return json.loads(cutoff_guard.load_index(row["full_path"],
                                              fixtures_root=fixtures_root))


def eight_k_filings(index: dict, cutoff=None) -> list[dict]:
    """Every 8-K and 8-K/A in the index filed at or before the cutoff, newest first.

    The filter is the look-ahead check: the index lists what the company has
    filed to date, and a bundle whose cutoff is earlier than that must not learn
    from it that a later 8-K exists.

    An amendment names what it amends when the index makes that unambiguous:
    the submissions index has no "amends" field, but it does carry each filing's
    `report_date`, and an 8-K/A whose report date belongs to exactly one earlier
    8-K amends that one. Where the report date is blank or matches more than
    one, `amends` is null and the line still says it is an amendment.
    """
    limit = str(cutoff) if cutoff is not None else None
    found = []
    for row in index.get("filings", []):
        if row.get("form") not in INDEX_FORMS:
            continue
        if limit is not None and row["filing_date"] > limit:
            continue
        found.append({"accession": row["accession"],
                      "filing_date": row["filing_date"],
                      "form": row["form"],
                      "report_date": row.get("report_date", ""),
                      "amendment": row["form"] in AMENDMENT_FORMS,
                      "amends": None,
                      "items": item_codes(row.get("items", ""))})
    found.sort(key=lambda row: (row["filing_date"], row["accession"]), reverse=True)

    originals: dict[str, list[str]] = {}
    for row in found:
        if not row["amendment"] and row["report_date"]:
            originals.setdefault(row["report_date"], []).append(row["accession"])
    for row in found:
        candidates = originals.get(row["report_date"], []) if row["amendment"] else []
        if len(candidates) == 1:
            row["amends"] = candidates[0]
    return found


def late_filings(index: dict, cutoff=None) -> list[dict]:
    """Every notification of late filing at or before the cutoff, newest first."""
    limit = str(cutoff) if cutoff is not None else None
    found = []
    for row in index.get("filings", []):
        if row.get("form") not in LATE_FORMS:
            continue
        if limit is not None and row["filing_date"] > limit:
            continue
        found.append({"accession": row["accession"],
                      "filing_date": row["filing_date"],
                      "form": row["form"],
                      "report_date": row.get("report_date", "")})
    found.sort(key=lambda row: (row["filing_date"], row["accession"]), reverse=True)
    return found


def body_items(html: str) -> dict[str, dict]:
    """Each numbered item in an 8-K body, whole, keyed by its code."""
    text = html_text.strip_tags(html)
    line_spans = html_text.lines(text)
    marks = []
    for start, end in line_spans:
        match = _BODY_ITEM.match(html_text.normalized(text[start:end]))
        if match:
            marks.append((start, match.group(1)))
    stop_at = next((start for start, end in line_spans
                    if _BODY_END.match(html_text.normalized(text[start:end]))
                    and (not marks or start > marks[-1][0])), len(text))

    found: dict[str, dict] = {}
    for index, (start, code) in enumerate(marks):
        end = marks[index + 1][0] if index + 1 < len(marks) else stop_at
        body = text[start:end].strip()
        entry = {"code": code, "text": body,
                 "paragraphs": [body[a:b] for a, b in html_text.spans(body)]}
        # A filer may name the same item twice (a heading and a cross
        # reference); the first occurrence carries the body. Unless that one is
        # a line of a table of contents, the item's name and nothing under it:
        # Powell's 8-K of 2011-11-08 lists items 2.02, 2.06, 4.02 and 9.01
        # before the first of them, and its impairment and its non-reliance
        # were read as their own headings. The first occurrence that carries
        # more than one line is the body.
        if code not in found or ("\n" not in found[code]["text"] and "\n" in body):
            found[code] = entry
    return found


# --- the event filings of the window -----------------------------------------

# The items an event 8-K's body is carried for: the six event items, the auditor
# change, and the four the earnings 8-K's body is already carried for.
EVENT_ITEMS = fetch_fixtures.EVENT_ITEMS
AUDITOR_CHANGE_ITEM = fetch_fixtures.AUDITOR_CHANGE_ITEM
CARRIED_FROM_AN_EVENT_BODY = tuple(sorted(set(EVENT_ITEMS) | set(VERBATIM_ITEMS)))
_WRAPPER = re.compile(r"\s*<DOCUMENT>", re.IGNORECASE)
_TEXT_OPEN = re.compile(r"<TEXT>", re.IGNORECASE)
_TEXT_CLOSE = re.compile(r"</TEXT>", re.IGNORECASE)
_BLANK_LINE = re.compile(r"\n[ \t\r\f\v]*\n")
_SLUG = {fetch_fixtures.EVENT_BODY: "8k_event", fetch_fixtures.AUDITOR_LETTER: "auditor_letter",
         fetch_fixtures.LATE_NOTICE: "late_notice", fetch_fixtures.STAFF_LETTER: "staff_letter",
         fetch_fixtures.COMPANY_RESPONSE: "company_response"}


def document_text(raw: str) -> str:
    """A served document's own text: what sits inside EDGAR's `<DOCUMENT>` …
    `<TEXT>` wrapper when the document is served in one (a comment letter, a
    late-filing notice, an exhibit), the whole of it otherwise. The wrapper's
    type, sequence and file name are EDGAR's, not the filer's."""
    if not _WRAPPER.match(raw):
        return raw
    opened = _TEXT_OPEN.search(raw)
    if opened is None:
        return raw
    closed = _TEXT_CLOSE.search(raw, opened.end())
    return raw[opened.end():closed.start() if closed else len(raw)]


def plain_paragraphs(text: str) -> list[str]:
    """The blocks of a plain-text document between blank lines, edge-trimmed: each
    one the document's own characters, its line breaks and spacing as filed."""
    return [block.strip() for block in _BLANK_LINE.split(text) if block.strip()]


def document_paragraphs(name: str, raw: str) -> list[str]:
    """Every paragraph of one document: a `.txt` (EDGAR's text copy of a staff
    letter, an older response) split on blank lines, anything else as HTML
    through the one tag stripper."""
    text = document_text(raw)
    if name.lower().endswith(".txt"):
        return plain_paragraphs(text)
    return html_text.paragraphs(text)


def triggering_report(ticker: str, cutoff, *, fixtures_root=cutoff_guard.FIXTURES) -> dict | None:
    """The store's 10-K or 10-Q filed on the cutoff, when exactly one is."""
    rows = [row for form in fetch_fixtures.PERIODIC_FORMS
            for row in cutoff_guard.documents(ticker, form=form, role="primary_html",
                                              fixtures_root=fixtures_root)
            if row.get("filing_date") == str(cutoff)]
    return rows[0] if len(rows) == 1 else None


def _summary(row: dict) -> dict:
    return {"form": row["form"], "accession": row["accessionNumber"],
            "filing_date": row["filingDate"], "items": fetch_fixtures.codes_of(row.get("items"))}


def _late_report(notice: dict, known: list[dict]) -> dict | None:
    """The report a late-filing notice gave notice of: the first report of the
    noticed form filed after the notice that stood at the trigger, or None when
    none had been filed by then."""
    form = notice["form"].removeprefix("NT ").removesuffix("/A")
    after = (notice["filingDate"], notice["accessionNumber"])
    later = [row for row in known if row["form"] == form
             and (row["filingDate"], row["accessionNumber"]) > after]
    return min(later, key=lambda row: (row["filingDate"], row["accessionNumber"]),
               default=None)


def _read(row: dict, cutoff: str, fixtures_root) -> tuple[str, str]:
    """(file name, text) of one stored event document, through the gate."""
    name = Path(row["path"]).name
    if row.get("stored") == "gzip":
        name = name.removesuffix(".gz")
    raw = cutoff_guard.load_bytes(row["full_path"], cutoff, fixtures_root=fixtures_root)
    try:
        return name, raw.decode("utf-8")
    except UnicodeDecodeError:
        # an older filing written in a single-byte code page: every byte is a
        # character of Latin-1, so nothing is replaced or dropped
        return name, raw.decode("latin-1")


def event_filings(ticker: str, *, cutoff, fixtures_root=cutoff_guard.FIXTURES,
                  trigger: dict | None = None) -> dict:
    """The event filings of the triggering report's window, as the store holds them.

    The window is `fetch_fixtures.event_window` over the stored index's rows at
    the cutoff: the event 8-Ks and late-filing notices that stood when the
    trigger was accepted and not when the previous 10-K or 10-Q was, and the
    comment letters EDGAR made public from that report's day to the day before
    the trigger's (`fetch_fixtures.public_in_window`). Each document is read
    through `cutoff_guard`, whose gate refuses a letter not public before the
    cutoff. What comes back:

    * `state`: `fetched` when the store's `event_filings` record is for this
      trigger, `another_filing` when it is for another, `not_fetched` when the
      store holds none, `no_trigger` when no report was named or found;
    * `carried`: one entry per document carried, with its paragraphs and ids;
    * `listed`: the window's 8-Ks and notices the index names and the store
      does not hold, which the file names so nothing is absent in silence;
    * `not_carried`: letters of the window EDGAR holds as a PDF only.

    A comment letter the store does not hold is never named from the index: its
    filing date says nothing about whether anyone could read it at the cutoff.
    """
    cutoff = str(cutoff)
    if trigger is None:
        trigger = triggering_report(ticker, cutoff, fixtures_root=fixtures_root)
    payload = {"cutoff": cutoff, "state": "no_trigger", "previous": None,
               "letter_lookback_years": fetch_fixtures.LETTER_LOOKBACK_YEARS,
               "carried": [], "listed": [], "not_carried": []}
    if trigger is None:
        return payload
    me = fetch_fixtures.as_index_row(trigger)
    index = submissions(ticker, fixtures_root=fixtures_root)
    rows = [fetch_fixtures.as_index_row(row) for row in index.get("filings", [])
            if row.get("filing_date", "") <= cutoff]
    window = fetch_fixtures.event_window(rows, me)
    previous = window["previous"]
    if previous is not None:
        payload["previous"] = _summary(previous)
    record = cutoff_guard.fetched_event_filings(ticker, fixtures_root=fixtures_root)
    if record is None:
        payload["state"] = "not_fetched"
    elif record.get("for") != me["accessionNumber"]:
        payload["state"] = "another_filing"
    else:
        after = previous["accessionNumber"] if previous is not None else None
        if record.get("after") != after:
            raise cutoff_guard.CutoffGuardError(
                f"{ticker}: the store's event filings were fetched for the window after "
                f"{record.get('after')}, and the index at {cutoff} opens it after {after}")
        payload["state"] = "fetched"
        if isinstance(record.get("letter_lookback_years"), int):
            payload["letter_lookback_years"] = record["letter_lookback_years"]

    held: dict[str, list[dict]] = {}
    if payload["state"] == "fetched":
        for row in cutoff_guard.documents(ticker, fixtures_root=fixtures_root):
            if row.get("role") in fetch_fixtures.EVENT_ROLES:
                held.setdefault(row["accession"], []).append(row)
    known = fetch_fixtures.known_at(rows, me)
    carried = []
    for row in window["eight_ks"] + window["notices"]:
        documents = held.get(row["accessionNumber"], [])
        if not documents:
            payload["listed"].append(_summary(row))
            continue
        if row["form"] in fetch_fixtures.LATE_NOTICE_FORMS:
            carried.extend(_notice(row, documents, known, cutoff, fixtures_root))
        else:
            carried.extend(_eight_k(row, documents, cutoff, fixtures_root))
    releases = (record or {}).get(fetch_fixtures.RELEASES) or {} \
        if payload["state"] == "fetched" else {}
    for row in window["letters"]:
        release = releases.get(row["accessionNumber"])
        released = release.get("released") if isinstance(release, dict) else None
        if not released or not fetch_fixtures.public_in_window(str(released), previous, me):
            continue
        carried.extend(_letter(row, str(released), held.get(row["accessionNumber"], []),
                               cutoff, fixtures_root, payload["not_carried"]))
    carried.sort(key=lambda entry: (entry["public"], entry["accession"], entry["order"]))
    payload["carried"] = carried
    return payload


def _ids(accession: str, role: str, count: int, first: int = 1) -> list[str]:
    return [f"{accession}:{_SLUG[role]}:{number}" for number in range(first, first + count)]


def _eight_k(row: dict, documents: list[dict], cutoff: str, fixtures_root) -> list[dict]:
    """An event 8-K's body, the event and verbatim items whole, and its EX-16 letters."""
    out = []
    codes = fetch_fixtures.codes_of(row.get("items"))
    listed = [code for code in codes if code in EVENT_ITEMS or code == AUDITOR_CHANGE_ITEM]
    base = {"form": row["form"], "accession": row["accessionNumber"],
            "filing_date": row["filingDate"], "public": row["filingDate"], "released": None,
            "items": codes}
    body = next((one for one in documents if one.get("role") == fetch_fixtures.EVENT_BODY),
                None)
    if body is not None:
        name, raw = _read(body, cutoff, fixtures_root)
        text = document_text(raw)
        items = body_items(text)
        missing = [code for code in listed if code not in items]
        if missing:
            paragraphs = html_text.paragraphs(text)
            what = (f"its body heads no item {', '.join(missing)}, so the whole body is "
                    "carried, verbatim")
        else:
            shown = [code for code in items if code in CARRIED_FROM_AN_EVENT_BODY]
            paragraphs = [one for code in shown for one in items[code]["paragraphs"]]
            what = (f"the bod{'ies' if len(shown) > 1 else 'y'} of item"
                    f"{'s' if len(shown) > 1 else ''} {', '.join(shown)}, verbatim")
        out.append(dict(base, role=fetch_fixtures.EVENT_BODY, order=0, document=name,
                        heading=(f"{row['form']} {row['accessionNumber']} filed "
                                 f"{row['filingDate']}, item{'s' if len(codes) > 1 else ''} "
                                 f"{', '.join(codes)}: {what}"),
                        paragraphs=paragraphs,
                        paragraph_ids=_ids(row["accessionNumber"], fetch_fixtures.EVENT_BODY,
                                           len(paragraphs))))
    letters = sorted((one for one in documents
                      if one.get("role") == fetch_fixtures.AUDITOR_LETTER),
                     key=lambda one: one["path"])
    number = 1
    for letter in letters:
        name, raw = _read(letter, cutoff, fixtures_root)
        paragraphs = document_paragraphs(name, raw)
        out.append(dict(base, role=fetch_fixtures.AUDITOR_LETTER, order=1, document=name,
                        heading=(f"{row['form']} {row['accessionNumber']} filed "
                                 f"{row['filingDate']}: exhibit 16, the former auditor's "
                                 f"letter ({name}), verbatim"),
                        paragraphs=paragraphs,
                        paragraph_ids=_ids(row["accessionNumber"],
                                           fetch_fixtures.AUDITOR_LETTER, len(paragraphs),
                                           number)))
        number += len(paragraphs)
    if AUDITOR_CHANGE_ITEM in codes and not letters and body is not None:
        out[0]["heading"] += "; the filing carries no exhibit 16"
    return out


def _notice(row: dict, documents: list[dict], known: list[dict], cutoff: str,
            fixtures_root) -> list[dict]:
    notice = next((one for one in documents if one.get("role") == fetch_fixtures.LATE_NOTICE),
                  None)
    if notice is None:
        return []
    name, raw = _read(notice, cutoff, fixtures_root)
    paragraphs = document_paragraphs(name, raw)
    late = _late_report(row, known)
    noticed = row["form"].removeprefix("NT ").removesuffix("/A")
    period = f", report date {row['reportDate']} in the index" if row.get("reportDate") else ""
    filed = (f"the {late['form']} {late['accessionNumber']} filed {late['filingDate']}"
             if late is not None else f"no {noticed} filed after it on or before {cutoff}")
    return [{"form": row["form"], "accession": row["accessionNumber"],
             "filing_date": row["filingDate"], "public": row["filingDate"], "released": None,
             "items": [], "role": fetch_fixtures.LATE_NOTICE, "order": 0, "document": name,
             "late_report": _summary(late) if late is not None else None,
             "heading": (f"{row['form']} {row['accessionNumber']} filed {row['filingDate']}"
                         f"{period}, a notification of late filing; the report it gives "
                         f"notice of: {filed}; verbatim"),
             "paragraphs": paragraphs,
             "paragraph_ids": _ids(row["accessionNumber"], fetch_fixtures.LATE_NOTICE,
                                   len(paragraphs))}]


def _letter(row: dict, released: str, documents: list[dict], cutoff: str, fixtures_root,
            not_carried: list[dict]) -> list[dict]:
    role = fetch_fixtures.LETTER_ROLE[row["form"]]
    who = ("a letter from the SEC staff" if row["form"] == "UPLOAD"
           else "the company's letter to the SEC staff")
    text = next((one for one in documents if one.get("role") == role), None)
    if text is None:
        not_carried.append(dict(_summary(row), released=released))
        return []
    name, raw = _read(text, cutoff, fixtures_root)
    paragraphs = document_paragraphs(name, raw)
    return [{"form": row["form"], "accession": row["accessionNumber"],
             "filing_date": row["filingDate"], "public": released, "released": released,
             "items": [], "role": role, "order": 0, "document": name,
             "heading": (f"{row['form']} {row['accessionNumber']}, {who}, filed "
                         f"{row['filingDate']} and made public {released}, verbatim"),
             "paragraphs": paragraphs,
             "paragraph_ids": _ids(row["accessionNumber"], role, len(paragraphs))}]


def _years(lookback_years: int) -> str:
    return f"{lookback_years} year{'s' if lookback_years != 1 else ''}"


def nothing_in_the_window(lookback_years: int) -> str:
    """What a whole window with nothing in it comes to, in the bundle manifest's
    record of the window (`window_record`). It says what was looked at: a
    comment letter is found only through its header, and only the letters filed
    within the lookback of the window's opening had theirs read."""
    return ("none: no 8-K of items " + ", ".join(EVENT_ITEMS) + " or " + AUDITOR_CHANGE_ITEM
            + ", no notification of late filing, and no comment letter filed in the "
            f"{_years(lookback_years)} before the window opened was made public in this "
            "window")


NOT_FETCHED = ("this store was fetched without event filings, so input_8k.md carries no "
               "8-K body of these items, no auditor's letter, no notification of late "
               "filing and no comment letter; the window's 8-Ks and notices the index "
               "lists are under `listed`")


def window_record(events: dict) -> dict:
    """The bundle manifest's record of the window: what was drawn, what was
    carried, what the index lists and the store does not hold, and, for a
    window with nothing in it, the sentence saying so with the lookback. It is
    where an empty window and a store fetched without event filings are told
    apart, since `input_8k.md` prints nothing for either."""
    state = events["state"]
    record = {
        "state": state,
        "opens_after": events["previous"],
        "through": events["cutoff"],
        "letter_lookback_years": events["letter_lookback_years"],
        "carried": [{"form": entry["form"], "accession": entry["accession"],
                     "role": entry["role"], "filing_date": entry["filing_date"],
                     "released": entry["released"], "paragraphs": len(entry["paragraphs"])}
                    for entry in events["carried"]],
        "listed": events["listed"],
        "not_carried": events["not_carried"],
    }
    if state == "not_fetched":
        record["note"] = NOT_FETCHED
    elif state == "fetched" and not (events["carried"] or events["listed"]
                                     or events["not_carried"]):
        record["note"] = nothing_in_the_window(events["letter_lookback_years"])
    return record


def render_event_filings(events: dict) -> list[str]:
    """The window's section of `input_8k.md`. Every line that is not a paragraph
    is a heading, because a line under an `[id]` is that paragraph's text.

    Nothing at all for a store that holds no window record (`not_fetched`) or
    no triggering report (`no_trigger`), and nothing for a window that holds
    nothing: the committed stores were fetched before event filings were, and a
    published run rebuilds byte for byte from its store only if the file ends
    where it ended -- NVIDIA's 10-Q of 2026-08-26 has an empty window, and its
    file is the same whether its store was fetched with event filings or
    without. Which of the two it was is the manifest's to say (`window_record`).
    """
    state = events["state"]
    empty = not (events["carried"] or events["listed"] or events["not_carried"])
    if state in ("no_trigger", "not_fetched") or (state == "fetched" and empty):
        return []
    cutoff, previous = events["cutoff"], events["previous"]
    if previous is not None:
        title = (f"## event filings made public after the {previous['form']} "
                 f"{previous['accession']} filed {previous['filing_date']}, through {cutoff}")
    else:
        title = f"## event filings made public on or before {cutoff}"
    out = ["", title, ""]
    if state == "fetched":
        out.extend(["### comment letters: those filed in the "
                    f"{_years(events['letter_lookback_years'])} before the window opened "
                    "were looked for, and are carried when made public inside it", ""])
    if state == "another_filing":
        out.extend(["### this store's event filings were fetched for another filing than "
                    "this one, so none is carried; any 8-K or notice of the window the index "
                    "lists is named below", ""])
    for entry in events["carried"]:
        out.extend([f"### {entry['heading']}", ""])
        for paragraph_id, paragraph in zip(entry["paragraph_ids"], entry["paragraphs"]):
            out.extend([f"[{paragraph_id}]", paragraph, ""])
    for row in events["listed"]:
        items = (f", item{'s' if len(row['items']) > 1 else ''} {', '.join(row['items'])}"
                 if row["items"] else "")
        out.extend([f"### listed by the index, its text not in the store: {row['form']} "
                    f"{row['accession']} filed {row['filing_date']}{items}", ""])
    for row in events["not_carried"]:
        out.extend([f"### not carried: {row['form']} {row['accession']} filed "
                    f"{row['filing_date']} and made public {row['released']}: EDGAR holds "
                    "the letter as a PDF with no text copy", ""])
    return out


def extract(ticker: str, *, cutoff=None, fixtures_root=cutoff_guard.FIXTURES,
            trigger: dict | None = None) -> dict:
    """The index lists, the release, the held 8-K's verbatim items and the event
    filings of the window (`event_filings`). `trigger` is the triggering report's
    manifest row; without one, the store's 10-K or 10-Q filed on the cutoff."""
    cutoff = cutoff_guard.resolve_cutoff(cutoff, ticker, fixtures_root=fixtures_root)
    index = submissions(ticker, fixtures_root=fixtures_root)
    filings = eight_k_filings(index, cutoff)
    late = late_filings(index, cutoff)

    held = cutoff_guard.one_document(ticker, "8-K", "primary_html",
                                     fixtures_root=fixtures_root)
    exhibit = cutoff_guard.one_document(ticker, "8-K", "exhibit_99_1",
                                        fixtures_root=fixtures_root)
    accession = held["accession"]

    exhibit_html = cutoff_guard.load_document(exhibit["full_path"], cutoff,
                                              fixtures_root=fixtures_root)
    body_html = cutoff_guard.load_document(held["full_path"], cutoff,
                                           fixtures_root=fixtures_root)

    # The release goes through the cleaner, once, and both what survives and
    # what was dropped come out of that one call. It used to be rendered from
    # the *uncleaned* paragraphs while `assemble_bundle.excluded_from_the_release`
    # cleaned the same document again to build the manifest's exclusion list —
    # so the same paragraph was published as `verbatim` and recorded as excluded
    # at the same time, 43 times across the fixture set. Two cleanings of one
    # document cannot be kept in agreement; there is now one.
    #
    # No `facts` are passed on purpose. `table_is_in_xbrl` drops a table whose
    # numbers are already XBRL facts, and the release's numbers are the
    # first-reported ones — `CLAUDE.md`'s ground truth. Dropping the earnings
    # table because the later 10-Q tagged the same figures would delete the very
    # values a restatement is measured against.
    release = clean_text.clean_stream(exhibit_html)
    items = body_items(body_html)

    verbatim, body_paragraphs = {}, []
    for code in VERBATIM_ITEMS:
        if code in items:
            first = len(body_paragraphs) + 1
            body_paragraphs.extend(items[code]["paragraphs"])
            verbatim[code] = {
                "code": code,
                "paragraphs": items[code]["paragraphs"],
                "paragraph_ids": [f"{accession}:8k_body:{index}" for index in
                                  range(first, len(body_paragraphs) + 1)],
            }

    return {
        "ticker": ticker,
        "cutoff": str(cutoff),
        "accession": accession,
        "filing_date": held["filing_date"],
        "held_items": item_codes(held.get("items", "")),
        "filings": filings,
        "late_filings": late,
        "item_2_02": {
            "paragraphs": release["paragraphs"],
            "paragraph_ids": [f"{accession}:8k_2_02:{index}"
                              for index in range(1, len(release["paragraphs"]) + 1)],
            "dropped": release["dropped"],
        },
        "verbatim_items": verbatim,
        "body_item_codes": sorted(items),
        "event_filings": event_filings(ticker, cutoff=cutoff, fixtures_root=fixtures_root,
                                       trigger=trigger),
    }


def index_lines(filings: list[dict], late: list[dict], cutoff) -> list[str]:
    """The two lists that come from `submissions.json` and nothing else."""
    out = [f"## item codes, every 8-K on or before {cutoff}", ""]
    for row in filings:
        line = (f"- {row['filing_date']} {row['accession']} — "
                f"{', '.join(row['items']) or '(none recorded)'}")
        if row["amendment"]:
            line += (f" — amendment of {row['amends']}" if row["amends"] else
                     " — amendment, the index does not say of what")
        out.append(line)
    out.extend(["", f"## late-filing notifications on or before {cutoff}", ""])
    if late:
        for row in late:
            out.append(f"- {row['filing_date']} {row['accession']} — {row['form']}"
                       + (f", for the period ended {row['report_date']}"
                          if row["report_date"] else ""))
    else:
        out.append(f"- none on or before {cutoff}")
    out.append("")
    return out


def render_index(ticker: str, *, cutoff, fixtures_root=cutoff_guard.FIXTURES,
                 trigger: dict | None = None, events: dict | None = None) -> str:
    """The filing index alone, for a bundle with no earnings exhibit on record,
    and the event filings of the window, which do not depend on one.

    `submissions.json` is stored for every company, so the item codes and the
    late-filing notices exist whether or not an 8-K body does. A bundle that
    printed neither could not answer `filing_irregularity` either way.
    """
    index = submissions(ticker, fixtures_root=fixtures_root)
    if events is None:
        events = event_filings(ticker, cutoff=cutoff, fixtures_root=fixtures_root,
                               trigger=trigger)
    return "\n".join(index_lines(eight_k_filings(index, cutoff),
                                 late_filings(index, cutoff), cutoff)
                     + render_event_filings(events))


def render(payload: dict) -> str:
    out = [f"# {payload['ticker']} 8-K — {payload['accession']} "
           f"filed {payload['filing_date']}", ""]
    out.extend(index_lines(payload["filings"], payload["late_filings"],
                           payload["cutoff"]))

    out.append("## item 2.02 — earnings release, exhibit 99.1")
    out.append("")
    # One stream, in the filing's order, a table being one entry holding all of
    # its rows — the same shape the notes and the MD&A arrive in. The tables no
    # longer trail the prose under an id of their own.
    for paragraph_id, paragraph in zip(payload["item_2_02"]["paragraph_ids"],
                                       payload["item_2_02"]["paragraphs"]):
        out.append(f"[{paragraph_id}]")
        out.append(paragraph)
        out.append("")

    for code in VERBATIM_ITEMS:
        item = payload["verbatim_items"].get(code)
        if item is None:
            continue
        out.append(f"## item {code} — body, verbatim")
        out.append("")
        for paragraph_id, paragraph in zip(item["paragraph_ids"], item["paragraphs"]):
            out.append(f"[{paragraph_id}]")
            out.append(paragraph)
            out.append("")
    if payload.get("event_filings") is not None:
        out.extend(render_event_filings(payload["event_filings"]))
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="8-K item codes, earnings release, bodies")
    parser.add_argument("--ticker", required=True)
    parser.add_argument("--cutoff", default=None)
    parser.add_argument("--fixtures", default=str(cutoff_guard.FIXTURES))
    parser.add_argument("--out", required=True)
    args = parser.parse_args(argv)

    try:
        payload = extract(args.ticker.upper(), cutoff=args.cutoff,
                          fixtures_root=Path(args.fixtures))
    except cutoff_guard.CutoffGuardError as exc:
        print(f"parse_8k: {exc}", file=sys.stderr)
        return BAD_INPUT
    Path(args.out).write_text(render(payload), encoding="utf-8")
    print(f"parse_8k: {args.ticker.upper()} {len(payload['filings'])} 8-K filings, "
          f"{len(payload['item_2_02']['paragraphs'])} release paragraphs, "
          f"verbatim {sorted(payload['verbatim_items']) or 'none'}, "
          f"{len(payload['event_filings']['carried'])} event documents → {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(interpreter_pin.enforce() or main())
