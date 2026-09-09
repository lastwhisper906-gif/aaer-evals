"""The fourth quarter, which no filing reports, and whether it looks like a dump.

`docs/INPUT_SPEC.md` states the rule this file implements in one line: "Q4 is
derived, never reported: the annual figure minus the nine-month year-to-date
figure. Python does it." A 10-K reports the year and a Q3 10-Q reports the nine
months; nobody files a statement for the three months in between, so the only
way to see the quarter a company closes its books in is to subtract.

`docs/CHECKLIST.md` lists `fourth_quarter_dump` under "articulation and the
filed history": the flag fires when the derived quarter "carries a
disproportionate share of the year's charges, reserves or margin move". **What
size of share is disproportionate is not decided here.** That number needs the
flag distribution over the 30 past cases, it is the owner's, and it is set at
rules v0.1 -- so this module reports its value and raises no flag.
`docs/CHECKLIST.md` §9 says that of four indicators by name and
`fourth_quarter_dump` is not one of them; it is in the same position all the
same, because `rules/thresholds_v0.1.json` does not exist yet and there is no
size for a share to be held against. Writing one here would be a threshold moved
inside the change that adds its inputs, which is the mistake `lessons.md`
already records. `REPORTS_A_VALUE` says all of that in the payload itself,
because an indicator that travels without that sentence eventually gets read as
a flag that never fires.

The source is the companyfacts record, `tests/fixtures/{ticker}/companyfacts.json`,
which is the as-filed point-in-time history: every period from every filing,
each row carrying the accession and the filing date that reported it. The one
XBRL instance a filing carries would give a single year and a single quarter,
which is one subtraction and no history.

**How a period is identified.** A fiscal year is a duration of `YEAR_DAYS`, the
same window `src/trends.py` already calls a year, *under a tag one of the
measures below names* -- an annual-length duration under `LossOnContracts` or a
credit facility's commitment fee is one fact's date, not a year the company
closed, and reading it as one puts a phantom year in the window. Its nine-month
period is the duration that *starts on the same day*, ends before it, and runs
`NINE_MONTH_DAYS`. Sharing the start date is what makes the subtraction mean
anything: two periods that begin together and one ends later, so the difference
is the stretch between the two ends and nothing else.

`NINE_MONTH_DAYS` is measured, not guessed. Over the twelve companies'
companyfacts, taking every distinct duration that shares a start date with an
annual period and is shorter than one, the lengths fall in three clusters --
86-98 days (one quarter), 176-206 (two) and 268-280 (three) -- with two short
stubs at 16 and 38 days below all of them. 260 to 290 takes the third cluster
with 54 days of clearance below it and 60 above.

**Both figures come from one us-gaap tag.** A year taken from `CostOfRevenue`
and a nine months taken from `CostOfGoodsAndServicesSold` differ by whatever
those two tags do not have in common, and the difference would not be a quarter.
`src/trends.py` refuses a period-over-period change across two tags for the same
reason; this refuses a subtraction across them.

**A period reported twice takes the later value, and says what it displaced.**
`docs/INPUT_SPEC.md` settles the choice -- "the latest filing before the cutoff
wins" -- and the choice is not always the flattering one. Carrier's 2023 revenue
is 22,098,000,000 as filed and 18,951,000,000 once the discontinued businesses
are taken out of it; Palo Alto Networks' nine months to 2025-04-30 is
6,685,200,000 as first filed and 6,685,000,000 where the next year's 10-Q
restates it a rounding coarser; Generac's 2025 net income is 159,554,000 in its
own 10-K and 161,400,000 in a filing eight weeks later. The rule takes the later
figure in all three, and `superseded` carries what it displaced, with the filing
that reported it -- `quiet_restatement` is the indicator that judges such a
difference, and it cannot judge what this one throws away.

**And the two figures have to stand on one basis.** "Latest filing wins" is
settled for the year and for the nine months separately, and a recast reaches
them at different times: a 10-Q re-presents one prior year, so the fiscal year
two back pairs a restated annual with a nine months nobody has restated.
Carrier's 2022 is the shape of it -- revenue 20,421,000,000 as filed and
17,288,000,000 once the discontinued businesses come out of it, against a nine
months of 15,316,000,000 last stated in October 2023 on the old basis. The
difference is 1,972,000,000, eleven per cent of the year, where every Carrier
year that does derive closes between twenty-two and twenty-five per cent of
itself in the fourth quarter -- and it is Carrier's fourth quarter on neither
basis. So a pair whose later figure *moved* -- its value displacing one the
record still held when the other figure was last stated -- is refused, with both
filings and the displaced figure named. It is the same refusal the one-tag
paragraph above makes, for the same reason.

That is fail-closed and it costs real cells: 27 across three companies, where
429 derive. Ten are Carrier's case, where the nine months has never been
restated at all. Ten more are recasts that reached both figures but at separate
filings -- Carrier's 2023 and ESCO's 2024, where the two figures look like one
basis and the record does not say they are. The last seven are a rounding: Palo
Alto Networks' nine-month revenue coarsening from 6,685,200,000 to
6,685,000,000 costs its whole 2025 year. Separating the last seventeen from the
first ten takes a size, which is a threshold this file does not have and is not
the place to set. Where a company's second tag for a measure carries a
consistent pair the fall-back finds it: Generac's net income comes back under
`ProfitLoss` from its 10-K and 10-Q rather than under `NetIncomeLoss` from a
proxy statement's pay-versus-performance row.

**A missing figure is never a zero.** Two accessions in this fixture set are in
no companyfacts row at all -- Carrier's and Littelfuse's quarterlies filed in
late July 2026, which is EDGAR's own loading lag -- and a tag can simply not be
reported for a period. Treating either as zero would publish the whole year as
the fourth quarter, in the exact shape a dump has. So a year whose nine-month
figure cannot be found is reported with the reason it could not, and carries no
number at all.

**The cutoff.** The record is read through `src/cutoff_guard.py` like every other
document, so it is refused unless its own recorded date -- the newest filing it
carries a fact from -- is at or before the cutoff. That is fail-closed and it is
also a limit worth stating: this record cannot be read at a cutoff earlier than
its own newest fact, the way `cutoff_guard.load_index` lets the submissions index
be read and filtered by row. A catalogue read at an earlier cutoff is the gate's
to allow, not this module's to arrange around.

    python3.12 -m src.fourth_quarter --ticker AAPL --out fourth_quarter.json

Exit 0, 2 the record could not be read or is not the shape this reads, 3 the
wrong interpreter.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from collections import defaultdict
from pathlib import Path

try:
    from src import cutoff_guard, fetch_companyfacts, interpreter_pin, trends
except ImportError:  # invoked as a plain script: python3.12 src/fourth_quarter.py
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import cutoff_guard, fetch_companyfacts, interpreter_pin, trends

BAD_INPUT = 2

# The annual period and the residual quarter are the ones the trend table
# already reads, imported rather than restated so there is one of each.
YEAR_DAYS = trends.YEAR_DAYS
QUARTER_DAYS = trends.QUARTER_DAYS
YEARS_REQUESTED = trends.YEARS_REQUESTED

# Three quarters, measured over the twelve companies' companyfacts. See the
# module docstring for the three clusters and how they were counted.
NINE_MONTH_DAYS = (260, 290)

REPORTS_A_VALUE = (
    "reports its value and does not flag: what share of the year makes a fourth "
    "quarter a dump needs the flag distribution over the 30 past cases and is "
    "set at rules v0.1 (docs/CHECKLIST.md §9)")

DERIVATION = "fourth_quarter = annual - nine_months"

# Which us-gaap tags may stand for each measure, best first, in the shape
# `src/trends.py` uses for the same reason: a company that switched tags still
# yields a series. The set is the income statement plus the three charge lines,
# because "a disproportionate share of the year's charges" is what
# `fourth_quarter_dump` is about and a charge taken in the fourth quarter is
# what it looks for.
MEASURES: dict[str, tuple[str, ...]] = {
    "revenue": ("RevenueFromContractWithCustomerExcludingAssessedTax",
                "RevenueFromContractWithCustomerIncludingAssessedTax",
                "Revenues", "SalesRevenueNet", "SalesRevenueGoodsNet"),
    "cost_of_revenue": ("CostOfRevenue", "CostOfGoodsAndServicesSold",
                        "CostOfGoodsSold", "CostOfServices", "CostOfSales"),
    "gross_profit": ("GrossProfit",),
    "operating_income": ("OperatingIncomeLoss",),
    "net_income": ("NetIncomeLoss", "ProfitLoss"),
    "research_and_development": ("ResearchAndDevelopmentExpense",),
    "selling_general_and_administrative": (
        "SellingGeneralAndAdministrativeExpense",),
    "income_tax_expense": ("IncomeTaxExpenseBenefit",),
    "restructuring_charges": ("RestructuringCharges",),
    "asset_impairment_charges": ("AssetImpairmentCharges",),
    "goodwill_impairment": ("GoodwillImpairmentLoss",),
}

MEASURED_TAGS = frozenset(tag for tags in MEASURES.values() for tag in tags)

# The margin move the checklist names, computed on the derived quarter and on
# the nine months it was derived against. Python does the division.
MARGINS: dict[str, dict] = {
    "gross_margin": {
        "terms": ("revenue", "cost_of_revenue"),
        "formula": "(revenue - cost_of_revenue) / revenue",
        "value": lambda v: (v["revenue"] - v["cost_of_revenue"]) / v["revenue"],
        "over": "revenue",
    },
    "operating_margin": {
        "terms": ("operating_income", "revenue"),
        "formula": "operating_income / revenue",
        "value": lambda v: v["operating_income"] / v["revenue"],
        "over": "revenue",
    },
}


class FourthQuarterError(Exception):
    """The record is not there, or not the shape this reads. Never a default."""


def _date(value: str) -> dt.date:
    return dt.date.fromisoformat(value)


def _days(start: str, end: str) -> int:
    return (_date(end) - _date(start)).days + 1


def _period(start: str, end: str) -> dict:
    return {"start": start, "end": end, "days": _days(start, end)}


# --- reading the record ------------------------------------------------------

def read_record(ticker: str, cutoff, *, fixtures_root=cutoff_guard.FIXTURES) -> dict:
    """One company's companyfacts document, through the gate, with its row."""
    row = cutoff_guard.one_document(ticker, fetch_companyfacts.FORM,
                                    fetch_companyfacts.ROLE,
                                    fixtures_root=fixtures_root)
    raw = cutoff_guard.load_bytes(row["full_path"], cutoff,
                                  fixtures_root=fixtures_root)
    return {"row": row, "document": json.loads(raw)}


def duration_rows(document: dict) -> dict[tuple, list[dict]]:
    """Every us-gaap duration fact, gathered by (tag, unit, start, end).

    Instants are left out: a fourth quarter is a stretch of time, and a balance
    at a date is not a thing to subtract a nine-month balance from.
    """
    gathered: dict[tuple, list[dict]] = defaultdict(list)
    facts = document.get("facts")
    if not isinstance(facts, dict):
        raise FourthQuarterError("the companyfacts record has no 'facts' object")
    for tag, concept in facts.get("us-gaap", {}).items():
        for unit, rows in concept.get("units", {}).items():
            for row in rows:
                start, end = row.get("start"), row.get("end")
                if start and end:
                    gathered[(tag, unit, start, end)].append(row)
    return dict(gathered)


def filed_after(gathered: dict[tuple, list[dict]], cutoff: dt.date) -> list[str]:
    """Rows the cutoff should have kept out. On a consistent record, none.

    The gate checks the document's *recorded* date, which `fetch_companyfacts`
    writes as the newest filing the record carries a fact from. This checks the
    rows themselves, so a record whose manifest date understates what is inside
    it is refused here rather than quietly read.
    """
    late = cutoff.isoformat()
    return sorted({f"us-gaap:{tag} [{unit}] {row['accn']} filed {row['filed']}"
                   for (tag, unit, _, _), rows in gathered.items()
                   for row in rows if row.get("filed", "") > late})


def as_filed(rows: list[dict]) -> dict:
    """One period's value under one tag: the latest filing before the cutoff wins.

    `docs/INPUT_SPEC.md`: "When a period is reported more than once, the latest
    filing before the cutoff wins." If that filing states two different values
    for the same period there is nothing to choose between, and choosing anyway
    is how a wrong number gets published with a source note attached.

    Every earlier filing that reported a *different* value comes back in
    `superseded`, because taking the later value quietly is how a re-presented
    period stops being visible. `quiet_restatement` is the indicator that judges
    the difference; this one records it so that indicator has something to read.
    """
    latest = max(row["filed"] for row in rows)
    newest = [row for row in rows if row["filed"] == latest]
    values = sorted({row["val"] for row in newest})
    accessions = sorted({row["accn"] for row in newest})
    if len(values) != 1:
        return {"missing": f"the filing of {latest} reports {values} for this "
                           f"period ({', '.join(accessions)})"}
    superseded = sorted({(row["filed"], row["accn"], row["val"]) for row in rows
                         if row["filed"] < latest and row["val"] != values[0]})
    return {"value": values[0], "filed": latest, "accessions": accessions,
            "superseded": [{"filed": filed, "accession": accession, "value": value}
                           for filed, accession, value in superseded]}


# --- finding the two periods -------------------------------------------------

def fiscal_years(gathered: dict[tuple, list[dict]]) -> list[dict]:
    """Every annual period an income-statement tag reports, newest first.

    An annual-length duration under a tag no measure names is not evidence of a
    fiscal year. TTM Technologies' 2025 year runs 2024-12-31..2025-12-29 under
    132 tags; one `us-gaap:LossOnContracts` fact in a 2026 10-Q starts it a day
    early, and reading every annual duration as a year turns that one fact into
    a second fiscal year ending the same day -- which takes a slot in the window
    from a real year and then answers all eleven measures with "none of them
    reports the year". Nine such spans sit in the twelve records, each under one
    to three tags, none of them an income-statement line, one of them a credit
    facility's commitment-fee period. `MEASURES` is already this file's account
    of what it can read a year off, so it is what a year is counted from.
    """
    spans = {(start, end) for tag, _, start, end in gathered
             if tag in MEASURED_TAGS
             and YEAR_DAYS[0] <= _days(start, end) <= YEAR_DAYS[1]}
    return [_period(start, end) for start, end
            in sorted(spans, key=lambda span: (span[1], span[0]), reverse=True)]


def _ends_by_tag(gathered: dict[tuple, list[dict]]) -> dict[tuple, dict[str, set]]:
    """(tag, start) → unit → the ends reported under it. The index the search needs."""
    ends: dict[tuple, dict[str, set]] = defaultdict(lambda: defaultdict(set))
    for tag, unit, start, end in gathered:
        ends[(tag, start)][unit].add(end)
    return ends


def nine_month_ends(ends: set, year: dict) -> list[str]:
    """The nine-month year-to-date ends inside one fiscal year, in date order."""
    return sorted(end for end in ends
                  if end < year["end"]
                  and NINE_MONTH_DAYS[0] <= _days(year["start"], end)
                  <= NINE_MONTH_DAYS[1])


def candidates(ends_by_tag, term: str, year: dict) -> tuple[list, list]:
    """(tag, unit, nine-month end) triples that can carry this measure, and why not.

    A candidate has the year and exactly one nine-month year-to-date under one
    tag and one unit. Everything that got close and did not qualify comes back
    as a line, because "no fourth quarter for this measure" and "the fourth
    quarter is zero" have to be told apart by whoever reads the output.
    """
    found, reasons = [], []
    for tag in MEASURES[term]:
        for unit, ends in sorted(ends_by_tag.get((tag, year["start"]), {}).items()):
            if year["end"] not in ends:
                continue
            nine = nine_month_ends(ends, year)
            if not nine:
                reasons.append(
                    f"us-gaap:{tag} [{unit}] reports {year['start']}..{year['end']} "
                    f"and no nine-month year-to-date starting {year['start']}")
                continue
            if len(nine) > 1:
                reasons.append(
                    f"us-gaap:{tag} [{unit}] reports {len(nine)} nine-month "
                    f"year-to-date periods starting {year['start']} "
                    f"({', '.join(nine)}), and the fourth quarter is not a guess")
                continue
            found.append((tag, unit, nine[0]))
    return found, reasons


def different_bases(annual: dict, nine: dict) -> str:
    """Why the two figures do not stand on one reporting basis, or "" when they do.

    `as_filed` settles the year and the nine months separately, and a recast
    reaches them at different times: a 10-Q re-presents one prior year, so the
    fiscal year two back pairs a restated annual with a nine months nobody has
    restated. The figure filed later having *moved* -- its value displacing one
    the record still held when the other figure was last stated -- is what says
    so, and it is a fact about the record rather than a size, which is the only
    kind of test this file is allowed to make.
    """
    for side, later, earlier in (("annual", annual, nine),
                                 ("nine-month", nine, annual)):
        if later["filed"] > earlier["filed"] and later["superseded"]:
            displaced = later["superseded"][-1]
            return (f"the {side} figure was reported {later['filed']} "
                    f"({', '.join(later['accessions'])}) over "
                    f"{displaced['value']} filed {displaced['filed']} "
                    f"({displaced['accession']}), and the other figure has not "
                    f"been reported since {earlier['filed']} "
                    f"({', '.join(earlier['accessions'])}), so the two stand on "
                    f"different reporting bases")
    return ""


def why_missing(term: str, reasons: list[str]) -> str:
    """The reason line, which never says or implies zero."""
    named = ", ".join(f"us-gaap:{tag}" for tag in MEASURES[term])
    if reasons:
        return f"no fourth quarter for {term}: " + "; ".join(reasons)
    return (f"no fourth quarter for {term}: none of {named} reports the year "
            f"consolidated in this record")


def measure(gathered, ends_by_tag, term: str, year: dict) -> dict:
    """One measure's fourth quarter for one fiscal year, or the reason there is none."""
    found, reasons = candidates(ends_by_tag, term, year)
    for tag, unit, nine_end in found:
        annual = as_filed(gathered[(tag, unit, year["start"], year["end"])])
        nine = as_filed(gathered[(tag, unit, year["start"], nine_end)])
        if "missing" in annual:
            reasons.append(f"us-gaap:{tag} [{unit}] {year['start']}..{year['end']}: "
                           f"{annual['missing']}")
            continue
        if "missing" in nine:
            reasons.append(f"us-gaap:{tag} [{unit}] {year['start']}..{nine_end}: "
                           f"{nine['missing']}")
            continue
        apart = different_bases(annual, nine)
        if apart:
            reasons.append(f"us-gaap:{tag} [{unit}] {year['start']}..{year['end']} "
                           f"less {year['start']}..{nine_end}: {apart}, and their "
                           f"difference is not a fourth quarter")
            continue
        quarter = _period((_date(nine_end) + dt.timedelta(days=1)).isoformat(),
                          year["end"])
        if not QUARTER_DAYS[0] <= quarter["days"] <= QUARTER_DAYS[1]:
            reasons.append(
                f"us-gaap:{tag} [{unit}]: {year['start']}..{year['end']} less "
                f"{year['start']}..{nine_end} leaves {quarter['days']} days, "
                f"which is not a quarter")
            continue
        return {
            "tag": tag,
            "unit": unit,
            "formula": DERIVATION,
            "annual": annual["value"],
            "nine_months": nine["value"],
            "fourth_quarter": annual["value"] - nine["value"],
            "nine_month_period": _period(year["start"], nine_end),
            "fourth_quarter_period": quarter,
            "annual_as_filed": {"filed": annual["filed"],
                                "accessions": annual["accessions"],
                                "superseded": annual["superseded"]},
            "nine_months_as_filed": {"filed": nine["filed"],
                                     "accessions": nine["accessions"],
                                     "superseded": nine["superseded"]},
        }
    return {"missing": why_missing(term, reasons)}


# --- the indicator -----------------------------------------------------------

def share_of_the_year(cell: dict) -> dict:
    """The fourth quarter over the year, signed.

    Signed arithmetic and not a share of a magnitude: where the annual figure is
    negative the ratio's sign is not the quarter's sign, so the quarter and the
    year are reported beside it and the ratio never stands alone.
    """
    if "missing" in cell:
        return {"missing": cell["missing"]}
    if cell["annual"] == 0:
        return {"missing": f"the annual {cell['tag']} figure is zero, so the "
                           f"fourth quarter has no share of it"}
    return {"value": cell["fourth_quarter"] / cell["annual"],
            "formula": "fourth_quarter / annual",
            "fourth_quarter": cell["fourth_quarter"],
            "annual": cell["annual"]}


def _margin(name: str, measures: dict, which: str) -> dict:
    """One margin over one of the two periods, or the reason it is not there."""
    spec = MARGINS[name]
    values = {}
    for term in spec["terms"]:
        cell = measures[term]
        if "missing" in cell:
            return {"missing": cell["missing"]}
        values[term] = cell[which]
    if values[spec["over"]] == 0:
        return {"missing": f"{spec['over']} is zero over the {which.replace('_', ' ')}"}
    return {"value": spec["value"](values)}


def margin_move(name: str, measures: dict) -> dict:
    """The fourth quarter's margin against the nine months it was derived against."""
    nine = _margin(name, measures, "nine_months")
    quarter = _margin(name, measures, "fourth_quarter")
    if "missing" in nine:
        return {"missing": nine["missing"]}
    if "missing" in quarter:
        return {"missing": quarter["missing"]}
    return {"nine_months": nine["value"], "fourth_quarter": quarter["value"],
            "move": quarter["value"] - nine["value"],
            "formula": f"{MARGINS[name]['formula']}, fourth quarter minus nine months"}


def dump_indicator(measures: dict) -> dict:
    """`fourth_quarter_dump`, as a value. No flag, no threshold, on purpose."""
    return {
        "key": "fourth_quarter_dump",
        "reports": REPORTS_A_VALUE,
        "share_of_the_year": {term: share_of_the_year(measures[term])
                              for term in MEASURES},
        "margin_move": {name: margin_move(name, measures) for name in MARGINS},
    }


# --- the whole company -------------------------------------------------------

def fourth_quarters(ticker: str, cutoff=None, *,
                    fixtures_root=cutoff_guard.FIXTURES,
                    years=YEARS_REQUESTED) -> dict:
    """Every fiscal year in the window, each derived or explained."""
    if cutoff is None:
        cutoff = cutoff_guard.default_cutoff(ticker, fixtures_root=fixtures_root)
    cutoff = cutoff_guard.parse_date(cutoff, "cutoff_date")

    held = read_record(ticker, cutoff, fixtures_root=fixtures_root)
    document, row = held["document"], held["row"]
    gathered = duration_rows(document)
    late = filed_after(gathered, cutoff)
    if late:
        raise FourthQuarterError(
            f"{ticker}: {len(late)} companyfacts rows were filed after the cutoff "
            f"{cutoff.isoformat()}, so the record disagrees with the date recorded "
            f"for it: " + "; ".join(late[:5]))

    ends_by_tag = _ends_by_tag(gathered)
    available = fiscal_years(gathered)
    derived = []
    for year in available[:years]:
        measures = {term: measure(gathered, ends_by_tag, term, year)
                    for term in MEASURES}
        derived.append({
            "fiscal_year": year,
            "measures": measures,
            "dump_indicator": dump_indicator(measures),
        })
    return {
        "ticker": ticker,
        "cutoff": cutoff.isoformat(),
        "source": {"path": row["path"], "url": row["url"],
                   "filing_date": row["filing_date"],
                   "date_basis": row.get("date_basis", ""),
                   "duration_facts": sum(len(rows) for rows in gathered.values())},
        "requested_years": years,
        "fiscal_years_on_record": len(available),
        "fiscal_years": derived,
    }


def render(payload: dict) -> str:
    """Deterministic by construction: sorted keys, no clock, no set iteration."""
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="the derived fourth quarter and the dump indicator")
    parser.add_argument("--ticker", required=True)
    parser.add_argument("--cutoff", default=None,
                        help="default: the fixture set's own as-of date")
    parser.add_argument("--out", required=True)
    args = parser.parse_args(argv)

    try:
        payload = fourth_quarters(args.ticker, args.cutoff)
    except (OSError, ValueError, FourthQuarterError,
            cutoff_guard.CutoffGuardError) as exc:
        print(f"fourth_quarter: {exc}", file=sys.stderr)
        return BAD_INPUT
    Path(args.out).write_text(render(payload), encoding="utf-8")
    filled = sum(1 for year in payload["fiscal_years"]
                 for cell in year["measures"].values() if "missing" not in cell)
    print(f"fourth_quarter: {payload['ticker']} "
          f"{len(payload['fiscal_years'])} of {payload['fiscal_years_on_record']} "
          f"fiscal years on record, {filled} measures derived → {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(interpreter_pin.enforce() or main())
