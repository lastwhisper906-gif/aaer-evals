"""The articulation check: the cash-flow statement against the balance sheet.

A filing states the change in receivables, inventory and payables twice. The
cash-flow statement states it as a line under "changes in operating assets and
liabilities"; the balance sheet states the two ends of it. The two should be the
same number, and where they are not the difference has a small number of honest
causes -- an acquisition brought the balance in without an operating cash flow,
or a foreign subsidiary's balance was translated at a different rate -- and one
dishonest one. `docs/INPUT_SPEC.md` §2.2 asks for the difference as a number
from the first run: the size of gap that raises a flag needs the distribution
over the past cases and is set at rules v0.1, so nothing here flags and nothing
here carries a threshold.

**The sign, which is where a reader goes wrong.** Apple's cash-flow statement
for the year ended 27 September 2025 prints `Accounts receivable, net (6,682)`
and `Inventories 1,400`: the printed figure is the effect on cash, so for an
asset it is the change in the account with the sign turned over. The us-gaap
element is the change itself -- `IncreaseDecreaseInAccountsReceivable` is
+6,682,000,000 and `IncreaseDecreaseInInventories` is −1,400,000,000 -- and that
is what this module reads, so it compares like with like against a balance-sheet
change of closing minus opening. For a liability the printed figure and the
element agree: `Accounts payable 902` is +902,000,000 either way.

**One filing at a time.** Every number in a row comes from the same accession,
because that is what "read off the statements" means: the cash-flow duration and
the two balance-sheet instants are the three figures a reader sees on two facing
pages of one document. companyfacts carries several filings' versions of the
same period, and joining across them would be comparing a filing with a later
filing's restatement of it -- a different check, and `docs/next_cycle_tasks.md`
gives it to `src/restatement_trace.py`.

**Pairing a period.** A balance-sheet instant belongs to a cash-flow duration
when it is the day before the duration starts, or the day it ends. Nothing else
pairs: over the twelve companies' thirty-six filings no period needed a looser
rule, and a looser rule is how a quarter gets differenced against a year. A
10-K's earlier cash-flow columns therefore carry no row, because their opening
balance sheet is not in that filing -- it is in the previous one. They are
counted in `coverage` rather than dropped in silence.

**What it refuses to compare.** A cash-flow line that covers more than the
account is not this account's line, and three of these companies state one.
ESCO's quarterlies collapse the whole of working capital into
`IncreaseDecreaseInOperatingCapital`, and Carrier's and Ciena's cash-flow
statements state payables and accrued liabilities together as
`IncreaseDecreaseInAccountsPayableAndAccruedLiabilities`, which does not
articulate with a balance sheet that carries `AccountsPayableCurrent` alone.
Differencing them anyway would produce a number that is a gap in the wrong
account. `coverage` names the wider concept instead.

**Through the gate, like every other extractor.** The companyfacts record is
read with `src/cutoff_guard.py`'s `load_bytes`, and the filings it is read
against come from that module's `documents`. Borrowing
`fetch_fixtures.read_stored` would have read the same bytes and left the bypass
scan in `tests/test_cutoff_guard.py` unable to see the read, which is what
`tests/test_fetch_companyfacts.py::test_only_the_companyfacts_fetcher_borrows_the_fetcher_file_helpers`
exists to stop; it caught this module doing it.

The gate is coarse on this document and that is worth naming. companyfacts is a
catalogue of facts drawn from many filings rather than a filing, so its manifest
row records the newest filing it carries and `date_basis` says so. `load_index`
is the gate's treatment for a catalogue -- check the path, skip the date, make
the caller filter the rows -- and it is restricted to the submissions index, so
this record goes through the date gate whole. At the fixture set's own as-of
date, which is the default cutoff here, all twelve pass. An earlier cutoff
refuses the record rather than filtering its rows, which is fail-closed and is
the direction the gate takes everywhere else. Widening `load_index` to a second
catalogue role is a change to `src/cutoff_guard.py` and is not this item's file.

**Two filings companyfacts has not loaded.** Carrier's and Littelfuse's
quarterlies filed in late July 2026 are in no companyfacts row at all -- EDGAR's
own loading lag, recorded by
`tests/test_fetch_companyfacts.py::NOT_YET_IN_COMPANYFACTS`. A period that
resolves to one of them has nothing to look up, so it is reported absent by
accession, with the filing date and the newest date companyfacts holds beside
it. It never arrives as a zero.

**Net of disclosed acquisitions and foreign exchange, and what that comes to
here.** Each row nets out every adjustment its own filing states and lists by
name every adjustment it could not, so the gap is never quietly a raw
difference. Across these twelve companies it nets nothing, and the reason is
worth stating plainly rather than leaving to be discovered: a purchase-price
allocation is reported against `us-gaap:BusinessAcquisitionAxis` and
companyfacts holds the entity-wide fact alone, and no us-gaap concept states the
foreign-exchange effect on receivables, inventory or payables at all -- the
taxonomy carries `EffectOfExchangeRateOn...` for cash. Littelfuse is the
measured case: its 10-K for the year ended 27 December 2025 discloses 16,798,000
of receivables and 23,363,000 of inventory acquired with Basler Electric, both
in the instance and neither in companyfacts, against a reported receivables gap
of 32,443,000 and inventory gap of 40,380,000. Over half of each gap is an
acquisition the filing discloses and this module cannot reach from the source it
reads. `tests/test_articulation.py` records that as a strict expected failure,
so the day the amounts are read out of the instance the suite says so.

`docs/INPUT_SPEC.md` §5 puts these rows inside `input_trends.json`. Assembling
that file is the trend table's job; this module produces the rows and their ids,
in the spelling §2.2 gives them -- `{accession}:articulation:{account}:{period}`
for a row and `{accession}:facts:{tag}:{period}` for each fact under it -- and
each row carries a `reads` line, which is the sentence a numbers reader quotes.

    python3.12 -m src.articulation --ticker AAPL --out input_articulation.json

Exit 0, 2 when a company has no companyfacts fixture to read, 3 on the wrong
interpreter.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

try:
    from src import cutoff_guard, fetch_companyfacts, interpreter_pin
except ImportError:  # invoked as a plain script: python3.12 src/articulation.py
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import cutoff_guard, fetch_companyfacts, interpreter_pin

BAD_INPUT = 2

NAMESPACE = "us-gaap"
UNIT = "USD"
INSTANCE_ROLES = ("xbrl_instance", "prior_period_xbrl_instance")

# The three accounts, in the order `docs/CHECKLIST.md` names them. `cash_flow`
# and `balance_sheet` are the concepts that may stand for the account, best
# first; the first one a filing reports is the one used, and the row says which.
# `wider` is the concepts that state a change covering more than this account:
# finding one is the reason the comparison is refused, not a fallback.
ACCOUNTS: dict[str, dict[str, tuple[str, ...]]] = {
    "receivables": {
        "cash_flow": ("IncreaseDecreaseInAccountsReceivable",
                      "IncreaseDecreaseInReceivables"),
        "balance_sheet": ("AccountsReceivableNetCurrent", "ReceivablesNetCurrent",
                          "AccountsAndOtherReceivablesNetCurrent",
                          "AccountsReceivableNet"),
        "wider": ("IncreaseDecreaseInOperatingCapital",
                  "IncreaseDecreaseInOtherOperatingCapitalNet"),
    },
    "inventory": {
        "cash_flow": ("IncreaseDecreaseInInventories",),
        "balance_sheet": ("InventoryNet",),
        "wider": ("IncreaseDecreaseInOperatingCapital",
                  "IncreaseDecreaseInOtherOperatingCapitalNet"),
    },
    "payables": {
        "cash_flow": ("IncreaseDecreaseInAccountsPayable",
                      "IncreaseDecreaseInAccountsPayableTrade"),
        "balance_sheet": ("AccountsPayableCurrent", "AccountsPayableTradeCurrent"),
        "wider": ("IncreaseDecreaseInAccountsPayableAndAccruedLiabilities",
                  "IncreaseDecreaseInOperatingCapital",
                  "IncreaseDecreaseInOtherOperatingCapitalNet"),
    },
}

# What a gap is netted against, and what the row says when the filing states
# none of it. Both kinds run through one path: an amount found is subtracted
# from the balance-sheet change, an amount not found is named in `not_netted`
# so the gap is never read as a fully adjusted one. The empty tuple under
# foreign exchange is the taxonomy's answer and not an omission here.
NETTING: dict[str, dict] = {
    "acquisitions": {
        "concepts": {
            "receivables": ("BusinessCombinationRecognizedIdentifiableAssetsAcquired"
                            "AndLiabilitiesAssumedCurrentAssetsReceivables",
                            "BusinessCombinationRecognizedIdentifiableAssetsAcquired"
                            "AndLiabilitiesAssumedReceivables"),
            "inventory": ("BusinessCombinationRecognizedIdentifiableAssetsAcquired"
                          "AndLiabilitiesAssumedInventory",),
            "payables": ("BusinessCombinationRecognizedIdentifiableAssetsAcquired"
                         "AndLiabilitiesAssumedCurrentLiabilitiesAccountsPayable",),
        },
        "absent": ("no us-gaap concept in this filing states the {account} acquired "
                   "in a business combination; a purchase-price allocation is "
                   "reported against us-gaap:BusinessAcquisitionAxis and companyfacts "
                   "holds the entity-wide fact alone, so where a filing discloses one "
                   "the amount is in the instance and not in this record"),
    },
    "foreign_exchange": {
        "concepts": {"receivables": (), "inventory": (), "payables": ()},
        "absent": ("no us-gaap concept states the foreign-exchange effect on "
                   "{account}; the taxonomy carries EffectOfExchangeRateOn... for "
                   "cash and nothing for a working-capital account, so this gap is "
                   "before translation"),
    },
}


def _number(value):
    """companyfacts writes these as whole numbers; keep one whole."""
    return int(value) if isinstance(value, float) and value.is_integer() else value


def _period(start: str, end: str) -> str:
    """The printed spelling of a duration, and half of every id under it."""
    return f"{start}..{end}"


def _opening(start: str) -> str:
    """The balance-sheet date a duration opens against: the day before it starts."""
    return (dt.date.fromisoformat(start) - dt.timedelta(days=1)).isoformat()


def _fact(accession: str, tag: str, period: str, value) -> dict:
    return {"tag": tag, "unit": UNIT, "period": period, "value": value,
            "id": f"{accession}:facts:{tag}:{period}"}


def document(ticker: str, fixtures_root: Path, cutoff: dt.date) -> tuple[dict, dict]:
    """One company's companyfacts record and the manifest row it was read from.

    `cutoff_guard.load_bytes` and nothing else: the record is a committed
    fixture, gzipped, and reading it any other way is a read the bypass scan
    cannot see.
    """
    entry = cutoff_guard.one_document(ticker, fetch_companyfacts.FORM,
                                      fetch_companyfacts.ROLE,
                                      fixtures_root=fixtures_root)
    raw = cutoff_guard.load_bytes(entry["full_path"], cutoff,
                                  fixtures_root=fixtures_root)
    return json.loads(raw), entry


def filings(ticker: str, fixtures_root: Path, cutoff: dt.date) -> list[dict]:
    """The filings this fixture set holds an XBRL instance for, oldest first.

    A filing made after the cutoff is not an input, so it is left out here
    rather than counted and then explained away downstream.
    """
    seen, out = set(), []
    for entry in cutoff_guard.documents(ticker, fixtures_root=fixtures_root):
        if entry.get("role") not in INSTANCE_ROLES or entry["accession"] in seen:
            continue
        if cutoff_guard.parse_date(entry["filing_date"],
                                   f"{ticker} {entry['path']} filing_date") > cutoff:
            continue
        seen.add(entry["accession"])
        out.append({"accession": entry["accession"], "form": entry["form"],
                    "filing_date": entry["filing_date"],
                    "report_date": entry["report_date"]})
    return sorted(out, key=lambda filing: (filing["filing_date"], filing["accession"]))


def facts_by_accession(record: dict) -> dict[str, dict[str, dict]]:
    """`accession` → `tag` → the durations and instants that filing reported.

    us-gaap and USD only. A dimensioned fact is not here to be filtered out:
    companyfacts holds the entity-wide value alone.
    """
    index: dict[str, dict[str, dict]] = {}
    for tag, concept in record.get("facts", {}).get(NAMESPACE, {}).items():
        for row in concept.get("units", {}).get(UNIT, []):
            held = index.setdefault(row["accn"], {}).setdefault(
                tag, {"durations": {}, "instants": {}})
            if row.get("start"):
                held["durations"][(row["start"], row["end"])] = _number(row["val"])
            else:
                held["instants"][row["end"]] = _number(row["val"])
    return index


def _stated(held: dict, tags: tuple[str, ...]) -> str | None:
    """The first of `tags` this filing states a change over any period under."""
    return next((tag for tag in tags if held.get(tag, {}).get("durations")), None)


def _balance_sheet_pair(held: dict, tags: tuple[str, ...],
                        opening: str, closing: str) -> tuple[str, object, object] | None:
    """The first concept that carries both ends of this period, and both values."""
    for tag in tags:
        instants = held.get(tag, {}).get("instants", {})
        if opening in instants and closing in instants:
            return tag, instants[opening], instants[closing]
    return None


def _balance_dates(held: dict, tags: tuple[str, ...]) -> list[str]:
    """Every date this filing carries a balance for the account at."""
    return sorted({instant for tag in tags
                   for instant in held.get(tag, {}).get("instants", {})})


def netting(held: dict, accession: str, account: str,
            start: str, end: str) -> tuple[list[dict], list[dict]]:
    """What this filing states about the gap's honest causes, and what it does not.

    An acquisition's balances arrive on the balance sheet without an operating
    cash flow, so an amount found inside the period is subtracted from the
    balance-sheet change. A kind with nothing found is named rather than treated
    as zero, because those are different claims.
    """
    netted, not_netted = [], []
    for kind, rule in NETTING.items():
        found = [_fact(accession, tag, instant, value)
                 for tag in rule["concepts"][account]
                 for instant, value in sorted(held.get(tag, {}).get("instants", {}).items())
                 if start <= instant <= end]
        if found:
            netted.extend(dict(fact, kind=kind) for fact in found)
        else:
            not_netted.append({"kind": kind,
                               "reason": rule["absent"].format(account=account),
                               "concepts_looked_for": list(rule["concepts"][account])})
    return netted, not_netted


def account_rows(held: dict, filing: dict, account: str) -> tuple[list[dict], dict]:
    """Every period of one account in one filing, and what became of the rest."""
    accession, concepts = filing["accession"], ACCOUNTS[account]
    entry = {"accession": accession, "form": filing["form"], "account": account}

    cash_flow_tag = _stated(held, concepts["cash_flow"])
    if cash_flow_tag is None:
        wider = _stated(held, concepts["wider"])
        if wider is not None:
            return [], dict(entry, status="stated_wider", reason=(
                f"this filing states no change in {account} on its own; it states "
                f"us-gaap:{wider}, which covers more than {account} and does not "
                f"articulate with a balance sheet that carries the account alone"))
        return [], dict(entry, status="no_cash_flow_line", reason=(
            f"this filing reports none of {', '.join(concepts['cash_flow'])} as a "
            f"change in {account} over any period"))

    rows, not_paired = [], []
    for (start, end), cash_flow_change in sorted(held[cash_flow_tag]["durations"].items()):
        opening, period = _opening(start), _period(start, end)
        pair = _balance_sheet_pair(held, concepts["balance_sheet"], opening, end)
        if pair is None:
            carried = _balance_dates(held, concepts["balance_sheet"])
            not_paired.append({"period": period, "reason": (
                f"this filing carries no {account} balance at both {opening} and "
                f"{end}; it carries one at "
                f"{', '.join(carried) if carried else 'no date at all'}")})
            continue
        balance_sheet_tag, opening_value, closing_value = pair
        balance_sheet_change = closing_value - opening_value
        netted, not_netted = netting(held, accession, account, start, end)
        adjusted = balance_sheet_change - sum(fact["value"] for fact in netted)
        gap = adjusted - cash_flow_change
        rows.append({
            "id": f"{accession}:articulation:{account}:{period}",
            "accession": accession, "form": filing["form"], "account": account,
            "period": period, "start": start, "end": end,
            "balance_sheet_change": balance_sheet_change,
            "cash_flow_change": cash_flow_change,
            "gap": gap,
            "netted": netted,
            "not_netted": not_netted,
            "inputs": {
                "cash_flow": _fact(accession, cash_flow_tag, period, cash_flow_change),
                "balance_sheet_opening":
                    _fact(accession, balance_sheet_tag, opening, opening_value),
                "balance_sheet_closing":
                    _fact(accession, balance_sheet_tag, end, closing_value),
            },
            "reads": reads_line(account, period, balance_sheet_change,
                                cash_flow_change, netted, not_netted, gap),
        })
    if not rows:
        return [], dict(entry, status="no_paired_period", not_paired=not_paired, reason=(
            f"this filing states a change in {account} as us-gaap:{cash_flow_tag} and "
            f"carries no {account} balance at both ends of any of those periods"))
    return rows, dict(entry, status="filled",
                      periods=[found["period"] for found in rows],
                      not_paired=not_paired)


def reads_line(account: str, period: str, balance_sheet_change, cash_flow_change,
               netted: list[dict], not_netted: list[dict], gap) -> str:
    """The row as one sentence, which is what a numbers reader quotes.

    The qualifier travels with the number: a gap that could not be netted
    against an acquisition or against translation says so in the same line, so
    the figure cannot be quoted without it.
    """
    applied = "".join(f", less {fact['value']:,} of {fact['kind'].replace('_', ' ')} "
                      f"stated as us-gaap:{fact['tag']}" for fact in netted)
    outstanding = "".join(f", before {entry['kind'].replace('_', ' ')}"
                          for entry in not_netted)
    return (f"{account} {period}: the balance sheet moved {balance_sheet_change:,}"
            f"{applied}, the cash-flow statement stated {cash_flow_change:,}, "
            f"and the gap is {gap:,}{outstanding}")


def articulation(ticker: str, fixtures: Path | None = None,
                 cutoff=None) -> dict:
    """Every articulation row this company's committed filings support."""
    root = Path(fixtures) if fixtures else cutoff_guard.FIXTURES
    cutoff = (cutoff_guard.parse_date(cutoff, "cutoff") if cutoff
              else cutoff_guard.default_cutoff(ticker, fixtures_root=root))
    record, held_on_record = document(ticker, root, cutoff)
    index = facts_by_accession(record)
    latest = fetch_companyfacts.latest_filed(record.get("facts", {}))
    on_file = filings(ticker, root, cutoff)

    rows, coverage = [], []
    for filing in on_file:
        held = index.get(filing["accession"])
        if held is None:
            coverage.append({
                "accession": filing["accession"], "form": filing["form"],
                "account": None, "status": "absent_from_companyfacts",
                "reason": (f"companyfacts holds no row filed under "
                           f"{filing['accession']}: this filing was filed "
                           f"{filing['filing_date']} and the newest row in this "
                           f"record was filed {latest}, so EDGAR had not loaded it "
                           f"when the fixture was fetched. The three accounts are in "
                           f"the instance and nothing here stands in for them")})
            continue
        for account in ACCOUNTS:
            more, entry = account_rows(held, filing, account)
            rows.extend(more)
            coverage.append(entry)

    return {
        "ticker": ticker,
        "cutoff": cutoff.isoformat(),
        "record_as_of": record.get("as_of"),
        "source": {"companyfacts": held_on_record["path"],
                   "sha256": held_on_record["sha256"],
                   "latest_filed": latest,
                   "filings": [filing["accession"] for filing in on_file]},
        "rows": rows,
        "coverage": coverage,
    }


def render(payload: dict) -> str:
    """Deterministic by construction: sorted keys, no clock, no set iteration."""
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def main(argv: list[str] | None = None) -> int:
    wrong_interpreter = interpreter_pin.enforce()
    if wrong_interpreter:
        return wrong_interpreter

    parser = argparse.ArgumentParser(
        description="the cash-flow statement against the balance sheet, per account")
    parser.add_argument("--ticker", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--fixtures", default=None, help="fixture root")
    parser.add_argument("--cutoff", default=None,
                        help="no filing after this date is read; default is the "
                             "fixture set's own as-of date")
    args = parser.parse_args(argv)

    try:
        payload = articulation(args.ticker.upper(),
                               Path(args.fixtures) if args.fixtures else None,
                               args.cutoff)
    except (cutoff_guard.CutoffGuardError, OSError, ValueError) as problem:
        print(f"articulation: {problem}", file=sys.stderr)
        return BAD_INPUT

    Path(args.out).write_text(render(payload), encoding="utf-8")
    absent = [entry for entry in payload["coverage"]
              if entry["status"] == "absent_from_companyfacts"]
    print(f"articulation: {args.ticker.upper()} {len(payload['rows'])} rows over "
          f"{len(payload['source']['filings'])} filings, "
          f"{len(absent)} of them absent from companyfacts → {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
