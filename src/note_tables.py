"""The filing's own facts in each table of its notes that reached the bundle.

The readers see the filing; the accounting and financial analysts see the two
reader reports and `calculator_filings_only.json`, and nothing else (CLAUDE.md).
A table of the notes reached neither analyst whole: the notes reader marks a
table whose change is its amounts "amounts only" and makes no item of it, and
the numbers reader's `input_numbers.json` holds the filing's us-gaap and dei
facts but not the ones the filer tagged in its own namespace. Over the nine
reruns of 2026-10-28, 6 of the analysis-grader's 10 contradictions reported as
unresolved named a row that settled the contradiction and never reached the
analyst: Apple's intangible-assets table, whose non-current line
(`aapl:IntangibleAssetsNetExcludingGoodwillNoncurrent`) is the release's
balance-sheet line, among them.

So this carries, for each table paragraph of the triggering filing's
`input_notes.md`, the facts the filing tagged in that table, each with its
concept, value, unit, period, axes and fact id, under the paragraph's number
(`notes_38` for `<accession>:notes:38`, the id a reader's report names the
table by, which the entry also carries whole). The analyst cites a fact's
path and never adds rows up; Python does the arithmetic.

**How a table is tied to its facts.** The filing's inline XBRL document tags
each number of a note's table with an `ix:nonFraction` element inside the
`<table>`, and the instance carries the same fact under the same id with its
context and unit. A paragraph of `input_notes.md` is tied to a table of the
inline document when that table, rendered by the function that rendered the
paragraph (`clean_text.clean_stream`), reads character for character as the
paragraph. Nothing is matched by value, so a number printed in two tables is
never given to the wrong one. Two tables of the document that render the same
are one table here, and their facts are one list, a fact stated in both
listed once. A table paragraph no table renders to is listed under
`unmatched`, never guessed at.

What is left out, and why: a paragraph of the prior filing (`[same as prior
period ...]` paragraphs carry no table of this filing), a prose paragraph (its
numbers are the readers' to quote), a text fact inside a table, which is not a
number, and a price (`is_a_price`): an amount in a currency per share or per
any unit -- an option's exercise price, a grant-date fair value per share, a
repurchase's average price -- or a concept that names a share's price, a
volatility, an intrinsic value or an input of the model that values an award,
or an equity award's fair value, each the market's price of the company's own
shares or worked out from it. A fact whose own period ends after the cutoff is left
out too, and counted; a typed member's date, a band of a remaining performance
obligation the filing states, is carried as `element = value`
(`docs/needs_judgment.md`). The two analysts never see a price, and each table
counts what it left out under `left_out_as_a_price`. A fair value in dollars
(of debt, of a portfolio, under the fair-value option) and a commodity hedge's
value are carried.
"""

from __future__ import annotations

import copy
import re
import unicodedata
import datetime as dt
from decimal import Decimal
import xml.etree.ElementTree as ET

from src import assemble_bundle, clean_text, cutoff_guard, instance_facts

IX = "http://www.xbrl.org/2013/inlineXBRL"
XHTML = "http://www.w3.org/1999/xhtml"
NOTES = "input_notes.md"
# the roles the triggering filing's own two documents are stored under
INLINE_ROLE, INSTANCE_ROLE = "primary_html", "xbrl_instance"


def _bare(element: ET.Element) -> str:
    """An element as plain HTML: the namespaces dropped, as the instance's text
    block carries the same table, so both render through one function."""
    element = copy.deepcopy(element)
    for node in element.iter():
        if isinstance(node.tag, str) and node.tag.startswith("{"):
            node.tag = node.tag.split("}", 1)[1]
        node.attrib = {key.split("}", 1)[-1]: value for key, value in node.attrib.items()}
    return ET.tostring(element, encoding="unicode")


def inline_tables(html: bytes) -> dict[str, list[str]]:
    """Each table of the inline document, rendered, to the ids of the numeric
    facts tagged inside it, in document order. A table with no rendering is
    left out."""
    root = ET.fromstring(html)
    out: dict[str, list[str]] = {}
    for table in root.iter(f"{{{XHTML}}}table"):
        # an inline fact with no id cannot be looked up in the instance; it is
        # kept as None, so the table that holds it says so
        ids = [fact.get("id") for fact in table.iter(f"{{{IX}}}nonFraction")]
        for rendered in clean_text.clean_stream(_bare(table))["paragraphs"]:
            held = out.setdefault(rendered.strip(), [])
            held.extend(one for one in ids if one is None or one not in held)
    return out


MINUS_SIGNS = ("-", "\u2212", "\u2013")      # hyphen, minus sign, en dash
# a bare footnote mark in the text of a cell: "(a)", "(1)", "(ab)"
FOOTNOTE_MARK = re.compile(r"\(\s*(?:[A-Za-z]{1,2}|\d{1,2})\s*\)")


def _row_tokens(row: ET.Element) -> list[tuple[str, str | None]]:
    """The text of one table row in document order, with each inline numeric fact as a
    marker and the end of each cell as another: ("text", the text), ("fact", its id),
    ("alias", the id of a fact nested inside the one before) and ("cell", None). The text
    of a `<sup>` (a footnote mark) is left out."""
    tokens: list[tuple[str, str | None]] = []

    def walk(node: ET.Element) -> None:
        if node.text:
            tokens.append(("text", node.text))
        for child in node:
            if child.tag == f"{{{IX}}}nonFraction":
                tokens.append(("fact", child.get("id")))
                for inner in child.iter(f"{{{IX}}}nonFraction"):
                    if inner is not child:
                        tokens.append(("alias", inner.get("id")))
            elif child.tag != f"{{{XHTML}}}sup":
                walk(child)
                if child.tag in (f"{{{XHTML}}}td", f"{{{XHTML}}}th"):
                    tokens.append(("cell", None))
            if child.tail:
                tokens.append(("text", child.tail))

    walk(row)
    return tokens


def _squeeze(text: str) -> str:
    """The text with its footnote marks, every space separator (no-break, thin, figure,
    narrow no-break, zero-width and the rest of Unicode's), line breaks and currency signs
    taken out."""
    text = FOOTNOTE_MARK.sub("", text)
    return "".join(one for one in text if one not in "\t\r\n"
                   and unicodedata.category(one) not in ("Zs", "Zl", "Zp", "Cf", "Sc"))


def printed_signs(html: bytes) -> dict[str, str]:
    """For each numeric fact of an inline document's tables, whether the number is
    printed as a negative -- in parentheses, or with a hyphen, a minus sign or an en
    dash written just before it in the same cell -- "negative", or without, "positive":
    the sign the reader of the table sees, which is the contribution of the row to its
    table whatever sign the filer tagged (a printed "1" tagged `sign="-"`, a printed "(1)"
    tagged +1). The parenthesis opens in the text just before the fact and closes in the
    text just after it (a percent sign may come first), across the cell boundary the
    renderer shows as "(1,647 | )"; footnote marks and every kind of space are ignored. A
    dash is a minus only when it is all the text between the start of the fact's own cell and
    the fact, an opening parenthesis and a currency sign aside: so the "-" of an empty cell
    beside it is no sign, and neither is the range "2.00 - 9.00%". A fact nested inside
    another has the sign of the cell it is printed in. A fact outside a table row is not
    listed."""
    root = ET.fromstring(html)
    out: dict[str, str] = {}
    for row in root.iter(f"{{{XHTML}}}tr"):
        tokens = _row_tokens(row)
        for at, (kind, fact_id) in enumerate(tokens):
            if kind != "fact" or fact_id is None:
                continue
            before, after, own_cell, other_fact = "", "", "", False
            for earlier in reversed(tokens[:at]):
                if earlier[0] == "fact":
                    break
                if earlier[0] == "text":
                    before = earlier[1] + before
            for earlier in reversed(tokens[:at]):
                if earlier[0] == "cell":
                    break
                if earlier[0] == "fact":
                    other_fact = True
                if earlier[0] == "text":
                    own_cell = earlier[1] + own_cell
            for later in tokens[at + 1:]:
                if later[0] == "fact":
                    break
                if later[0] == "text":
                    after += later[1]
            parenthesised = (_squeeze(before).endswith("(")
                             and re.match(r"%?\)", _squeeze(after)) is not None)
            minus = not other_fact and _squeeze(own_cell).lstrip("(") in MINUS_SIGNS
            sign = "negative" if parenthesised or minus else "positive"
            out[fact_id] = sign
            for later in tokens[at + 1:]:
                if later[0] != "alias":
                    break
                out[later[1]] = sign
    return out


def tagged_signs(html: bytes) -> dict[str, str]:
    """The sign the filer tagged, apart from the printed one: an inline numeric fact is
    "negative" when its own element says `sign="-"` and "positive" otherwise."""
    root = ET.fromstring(html)
    return {one.get("id"): "negative" if one.get("sign") == "-" else "positive"
            for one in root.iter(f"{{{IX}}}nonFraction") if one.get("id")}


# The printed sign of every non-zero flow (a fact with a span) is carried with the table: a
# row whose element does not fix its own direction -- recoveries, adjustments, translation,
# acquisitions, transfers, "other" -- is tagged with whichever sign the filer chose, and the
# table's reader sees the printed one (`src/rollforwards.py`).
# What a concept's name says when the number is a price of the company's own
# shares or is worked out from one. Words, not the bare "price": a commodity
# hedge (`PriceRiskDerivativeAssetsAtFairValue`) or a contract's transaction
# price is no share's price and stands.
PRICE_WORDS = ("shareprice", "stockprice", "pricepershare", "pershareprice", "pershare",
               "pricepaid",
               "exerciseprice", "strikeprice", "capprice", "floorprice", "conversionprice",
               "volatility",
               # the share price less the strike, times the shares
               "intrinsicvalue",
               # every input of the model that values an award: a dividend
               # yield is the dividend over the share price, and the rest go
               # with it, so the model's inputs are one class
               "fairvalueassumptions")
# An equity award's fair value is the share price at grant, or a model fed by
# it. The words name share-based pay only: the fair-value option of ASC 825
# (`FairValueOption...`) is a dollar fair value of debt or assets, and stands.
AWARD_WORDS = ("sharebased", "restrictedstock", "stockoption", "stockappreciationright",
               "performanceshare")


def is_a_price(fact: dict) -> bool:
    """A fact the accounting and financial analysts are not handed: an amount in
    a currency per anything (per share, or per a unit the filer defines, as
    Western Digital's `usdPerUnit` for its capped call's cap price), a concept
    that names a share's price (an exercise, strike, cap or conversion price), a
    volatility, an intrinsic value or an input of the model that values an
    award, or an equity award's fair value. Each is, or is worked out from, the
    market's price of the company's own shares at some date the filing names,
    and those analysts never see a price (CLAUDE.md). Earnings and dividends per
    share go with the per-share amounts; the calculator carries both from
    companyfacts."""
    unit = fact.get("unit") or ""
    numerator = unit.split("/", 1)[0]
    per_something = "/" in unit and numerator.startswith("iso4217:")
    local = fact["name"].rsplit(":", 1)[-1].lower()
    award_value = "fairvalue" in local and any(word in local for word in AWARD_WORDS)
    return per_something or award_value or any(word in local for word in PRICE_WORDS)


def cell(fact: dict) -> dict:
    """One fact as the analyst reads it: a cell whose `value` is the number."""
    context = fact["context"]
    out = {"concept": fact["name"], "value": fact["value"], "unit": fact["unit"]}
    if "instant" in context:
        out["instant"] = context["instant"]
    else:
        out["start"], out["end"] = context.get("start"), context.get("end")
    axes = instance_facts.members(fact)
    # a typed member carries a value of its own (a date, a name), written as
    # "element = value": the date of a remaining-performance-obligation band is
    # one the filing states, and as a whole string it would read as a period
    for typed in context.get("typed_segment", []):
        axes[typed["dimension"]] = f"{typed['element']} = {typed['value']}"
    if axes:
        out["axes"] = axes
    if fact["nil"]:
        out["nil"] = True
    out["fact"] = fact["id"]
    return out


def _end(cell_: dict) -> str:
    return cell_.get("instant") or cell_.get("end") or ""


def _days(cell_: dict) -> int | None:
    """A flow's length in days, or None for a cell with no dated span: a
    `forever` context, or a context the instance does not carry, gives the
    cell no start and no end, and such a cell is set beside nothing."""
    start, end = cell_.get("start"), cell_.get("end")
    if not (isinstance(start, str) and isinstance(end, str)):
        return None
    try:
        return (dt.date.fromisoformat(end[:10]) - dt.date.fromisoformat(start[:10])).days
    except ValueError:
        return None


# Two flows are like for like when their lengths differ by at most a tenth of
# the longer: a 13-week quarter beside a 14-week one (91 and 98 days), never a
# quarter beside six months to date, nor a 45-day stub beside a 30-day month.
LIKE_SPANS = 0.10


def _like(one: int, other: int) -> bool:
    return abs(one - other) <= LIKE_SPANS * max(one, other)


def _period(cell_: dict) -> dict:
    return {"instant": cell_["instant"]} if "instant" in cell_ else \
        {"start": cell_["start"], "end": cell_["end"]}


def changes(cells: list[dict]) -> list[dict]:
    """For each fact a table states at more than one date -- the same concept,
    axes and unit; a balance at two dates, or a flow over two spans whose
    lengths differ by at most a tenth (`LIKE_SPANS`) -- the change from each
    earlier date to the latest, worked out here, so a swing the table shows is
    a number the analyst cites and never one it subtracts. Each change is a
    cell (`value`, `unit`) with the two periods and the two fact ids it is the
    difference of, later minus earlier. A cell with no date, and a nil cell,
    is set beside nothing."""
    groups: dict[tuple, list[dict]] = {}
    for one in cells:
        if one.get("nil") or not isinstance(one.get("value"), (int, float)):
            continue
        if "instant" in one:
            if not isinstance(one["instant"], str):
                continue
            kind = "instant"
        elif _days(one) is None:
            continue
        else:
            kind = "flow"
        same = (one["concept"], tuple(sorted((one.get("axes") or {}).items())), one["unit"],
                kind)
        groups.setdefault(same, []).append(one)
    out = []
    for (_, _, _, kind), group in groups.items():
        last = max(_end(c) for c in group)
        for latest in sorted((c for c in group if _end(c) == last), key=lambda c: c["fact"]):
            for earlier in sorted(group, key=lambda c: (_end(c), c["fact"])):
                if _end(earlier) >= last:
                    continue
                if kind == "flow" and not _like(_days(earlier), _days(latest)):
                    continue
                entry = {"concept": latest["concept"],
                         "value": float(Decimal(str(latest["value"]))
                                        - Decimal(str(earlier["value"]))),
                         "unit": latest["unit"], "from": _period(earlier),
                         "to": _period(latest)}
                if latest.get("axes"):
                    entry["axes"] = latest["axes"]
                entry["facts"] = [earlier["fact"], latest["fact"]]
                out.append(entry)
    return out


def key(paragraph: str) -> str:
    """A paragraph's key here: `notes_38` for `<accession>:notes:38`. The
    accession is the triggering filing's, the one every table here is from, and
    a path an analyst writes in braces is lower-case letters, digits, `_`, `.`
    and `-` (`src/analysis_check.py`, `PLACEHOLDER`), so a colon cannot be in it."""
    return "notes_" + paragraph.rsplit(":", 1)[1]


def ends_after(fact: dict, cutoff: str | None) -> bool:
    """Whether a fact's own period ends after the cutoff: a context the filing
    dates later than the day it was filed, which the owner's grader refuses in
    any calculator file. A typed member's date is not the fact's period."""
    context = fact["context"]
    end = context.get("instant") or context.get("end") or ""
    return bool(cutoff) and end[:10] > str(cutoff)[:10]


def tables(paragraphs: list[tuple[str, str]], html: bytes, instance: bytes, *,
           accession: str, cutoff: str | None = None) -> dict:
    """The facts of each table paragraph of this filing, keyed by paragraph id."""
    rendered = inline_tables(html)
    by_id = {fact["id"].split(":", 1)[1]: fact
             for fact in instance_facts.facts(instance, accession=accession)
             if fact["kind"] == "numeric"}
    found, unmatched, untagged, prices, later = {}, [], [], {}, {}
    signs, printed = {}, None
    for paragraph, text in paragraphs:
        if not paragraph.startswith(f"{accession}:notes:") or not text.startswith("|"):
            continue
        ids = rendered.get(text.strip())
        if ids is None:
            unmatched.append(paragraph)
            continue
        cells, seen = [], set()
        for one in ids:
            fact = by_id.get(one) if one is not None else None
            if fact is None:
                untagged.append(f"{paragraph}: {one or 'an inline fact with no id'}")
                continue
            if is_a_price(fact):
                prices[key(paragraph)] = prices.get(key(paragraph), 0) + 1
                continue
            if ends_after(fact, cutoff):
                later[key(paragraph)] = later.get(key(paragraph), 0) + 1
                continue
            # one fact the document states twice, in two tables that render
            # the same, is one cell
            same = (fact["name"], fact["context_ref"], fact["unit"], fact["value"])
            if same not in seen:
                seen.add(same)
                cells.append(cell(fact))
                if fact["value"] and "instant" not in fact["context"]:
                    if printed is None:
                        printed = printed_signs(html)
                    if one in printed:
                        signs[fact["id"]] = printed[one]
        if cells:
            found[key(paragraph)] = {"paragraph": paragraph, "facts": cells}
            moved = changes(cells)
            if moved:
                found[key(paragraph)]["changes"] = moved
    return {"tables": found, "unmatched": unmatched, "not_in_the_instance": untagged,
            "left_out_as_a_price": prices, "left_out_ending_after_the_cutoff": later,
            "printed_signs": signs}


WHAT_THIS_IS = ("for each table of the triggering filing's notes that reached the readers "
                "(input_notes.md), the numbers the filing itself tagged in that table, read "
                "from its XBRL instance: concept, value, unit, period, axes and fact id, under "
                "the paragraph's number (notes_38 for <accession>:notes:38, the id a reader's "
                "report names the table by, which `paragraph` carries whole). A table is "
                "tied to its facts when the inline document's table renders character for "
                "character as the paragraph, never by value. Each fact is a cell whose `value` "
                "is the number; cite its path, and never add rows up. `changes` holds, for a "
                "fact the table states at more than one date (a balance at two dates, or a "
                "flow over two spans whose lengths differ by at most a tenth), the change from each earlier date to "
                "the latest, later minus earlier, worked out by Python: cite a change's path "
                "and never subtract")


def from_run(ticker: str, accession: str | None, cutoff, *, fixtures_root,
             bundle) -> dict:
    """The note tables of one run, or `missing` with the reason."""
    if bundle is None or not accession:
        return {"missing": "no run bundle or accession was given, so no note table was read"}
    try:
        notes = cutoff_guard.load_bundle_file(bundle, NOTES)
        rows = {row["role"]: row for row in cutoff_guard.documents(
                    ticker, fixtures_root=fixtures_root)
                if row.get("accession") == accession
                and row.get("role") in (INLINE_ROLE, INSTANCE_ROLE)}
        if set(rows) != {INLINE_ROLE, INSTANCE_ROLE}:
            return {"missing": f"the store holds no inline document and instance of "
                               f"{accession} under the roles {INLINE_ROLE} and "
                               f"{INSTANCE_ROLE}; it holds {sorted(rows)}"}
        html = cutoff_guard.load_bytes(rows[INLINE_ROLE]["full_path"], cutoff,
                                       fixtures_root=fixtures_root)
        instance = cutoff_guard.load_bytes(rows[INSTANCE_ROLE]["full_path"], cutoff,
                                           fixtures_root=fixtures_root)
    except cutoff_guard.CutoffGuardError as exc:
        return {"missing": str(exc)}
    try:
        found = tables(assemble_bundle.paragraph_blocks(notes), html, instance,
                       accession=accession, cutoff=str(cutoff))
    except ET.ParseError as exc:
        return {"missing": f"the inline document of {accession} is not well-formed XML: {exc}"}
    return {"what_this_is": WHAT_THIS_IS, **found}
