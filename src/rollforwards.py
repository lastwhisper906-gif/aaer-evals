"""One rollforward identity over every reserve family a filing tables as a rollforward.

The accounting analyst reads a reserve's table -- warranty, allowance, inventory
reserve, restructuring reserve, contract liabilities, supplier finance, goodwill --
and has had to add its rows up and say whether they foot. Python states it instead,
here, from the facts `src/note_tables.py` hands over for each table of the notes
(concept, value, unit, period, axes, fact id), so the analyst cites a field and does
no arithmetic (CLAUDE.md: Python does the arithmetic).

**The identity.** For a family, a table and a period (the span the flow rows are
stated over):

    beginning + charged to expense + other - usage = ending

`beginning` and `ending` are the balance row at the day before the span starts and
at its last day (a fiscal calendar's 52 or 53 weeks put the tagged instant up to
three days either side); a balance row is the same element at both dates. `foots`
is true or false, `difference` is the stated ending less the rows' sum, and the
arithmetic is Decimal on the facts' own values. For supplier finance and goodwill
the `charged_to_expense` line is the additions line (confirmed invoices added,
goodwill acquired), the only line of its kind those tables have.

**Usage is taken away as the filer tagged it.** Every element of the usage role is
tagged positive in every committed instance (warranty payments, write-offs,
restructuring payments, supplier-finance settlements), so the identity subtracts
the tagged value, and a table tagged the other way does not foot and says so. One
element is read as a magnitude: `ContractWithCustomerLiabilityRevenueRecognized`,
tagged positive by 19 of the committed facts and negative by 9, always revenue
leaving the balance.

**One table, one series, never summed.** A rollforward is read inside one table of
the notes and inside one set of axes, so a segment's goodwill, a plan's
restructuring reserve or a receivable type's allowance is a series of its own; a
beginning balance in one table and flows in another make no period. Schedule II
(the valuation and qualifying accounts table) uses the one set of elements
`ValuationAllowancesAndReserves...` for every account, so the family is read off the
member of its type axis (`AllowanceForCreditLossMember`, `InventoryValuationReserveMember`);
the valuation allowance of deferred tax assets is no reserve of this section's. The
gross base (`ending_over_gross_base`, and the fall-while-the-base-rose half of
`release`) is the one thing read from another table: the element named in the
family's base row at the same two dates and on the same axes, a ratio of two facts,
printed with both fact ids, and left out when the filing states two different
values for it.

**What a table may hold that this does not place.** A row the filer tags in its own
namespace, or a us-gaap element this table leaves out, cannot be put in a role; such
a duration row of the same table, axes and span, whose name names the family, is
listed under `rows_not_placed` and `complete` is false. A table that does not foot
and is not complete is a table Python could not read in full, not a finding.

**The elements, and how each was confirmed.** `ELEMENTS` and `SCHEDULE_TWO` below are
the us-gaap elements of each role, and `CONFIRMED_IN` names the ticker whose committed
instances (`tests/fixtures`) use each one, which `tests/test_calculator_rollforwards.py`
greps. An element nobody confirmed is not in the table. Left out for that reason or
because its sign or meaning is not fixed: the extended-warranty elements
(`ExtendedProductWarrantyAccrual...`, deferred revenue, not a reserve), the current
and noncurrent splits of a balance (`...Current`, `...Noncurrent`, `ProductWarrantyAccrualClassifiedCurrent`),
`ProductWarrantyAccrualPeriodIncreaseDecrease` and `RestructuringReservePeriodIncreaseDecrease`
(a net change that a filer states beside or instead of its components),
`FinancingReceivableAllowanceForCreditLossLoanSold`, the cumulative catch-up and
time-frame elements of contract liabilities (signed changes to revenue, no balance
leaving), `GoodwillGross` as a gross base (it excludes impairments, so a goodwill
that fell by impairment would read as a release) and `NotesReceivableGross`. Every
`AccountsReceivableAllowanceForCreditLoss...` element the current taxonomy names was
absent from the committed instances, which tag `AllowanceForDoubtfulAccountsReceivable...`.
`ValuationAllowancesAndReservesPeriodIncreaseDecrease` is read as a component (Generac
states 525 and 0 beside the other rows and its table foots only with it).
"""

from __future__ import annotations

import datetime as dt
import re
from decimal import Decimal

ELEMENTS = {
    "allowance_for_credit_losses": {
        "balance": (
            "AllowanceForDoubtfulAccountsReceivable",
            "AllowanceForDoubtfulAccountsReceivableCurrent",
            "FinancingReceivableAllowanceForCreditLosses",
        ),
        "charged": (
            "ProvisionForDoubtfulAccounts",
            "ProvisionForLoanLossesExpensed",
        ),
        "usage": (
            "AllowanceForDoubtfulAccountsReceivableWriteOffs",
            "FinancingReceivableAllowanceForCreditLossesWriteOffs",
            "FinancingReceivableAllowanceForCreditLossWriteoffAfterRecovery",
        ),
        "other": (
            "FinancingReceivableAllowanceForCreditLossForeignCurrencyTranslation",
        ),
        "revision": (),
        "base": (
            "AccountsReceivableGross",
            "AccountsReceivableGrossCurrent",
            "FinancingReceivableBeforeAllowanceForCreditLossAndFee",
        ),
    },
    "product_warranty": {
        "balance": (
            "ProductWarrantyAccrual",
            "StandardProductWarrantyAccrual",
        ),
        "charged": (
            "ProductWarrantyAccrualWarrantiesIssued",
            "StandardProductWarrantyAccrualWarrantiesIssued",
        ),
        "usage": (
            "ProductWarrantyAccrualPayments",
            "StandardProductWarrantyAccrualPayments",
        ),
        "other": (
            "ProductWarrantyAccrualAdditionsFromBusinessAcquisition",
            "StandardProductWarrantyAccrualAdditionsFromBusinessAcquisition",
            "StandardProductWarrantyAccrualForeignCurrencyTranslationGainLoss",
            "StandardAndExtendedProductWarrantyAccrualForeignCurrencyTranslationGainLoss",
        ),
        "revision": (
            "ProductWarrantyAccrualPreexistingIncreaseDecrease",
            "StandardProductWarrantyAccrualPreexistingIncreaseDecrease",
        ),
        "base": (),
    },
    "inventory_reserve": {
        "balance": (
            "InventoryValuationReserves",
        ),
        "charged": (
            "InventoryWriteDown",
        ),
        "usage": (),
        "other": (),
        "revision": (),
        "base": (
            "InventoryGross",
        ),
    },
    "restructuring_reserve": {
        "balance": (
            "RestructuringReserve",
        ),
        "charged": (
            "RestructuringCharges",
            "RestructuringSettlementAndImpairmentProvisions",
        ),
        "usage": (
            "PaymentsForRestructuring",
            "RestructuringReserveSettledWithoutCash2",
        ),
        "other": (
            "RestructuringReserveTranslationAndOtherAdjustment",
        ),
        "revision": (
            "RestructuringReserveAccrualAdjustment1",
        ),
        "base": (),
    },
    "contract_liabilities": {
        "balance": (
            "ContractWithCustomerLiability",
        ),
        "charged": (),
        "usage": (
            "ContractWithCustomerLiabilityRevenueRecognized",
        ),
        "other": (
            "ContractWithCustomerLiabilityIncreaseDecreaseForContractAcquiredInBusinessCombination",
        ),
        "revision": (),
        "base": (),
    },
    "supplier_finance_obligations": {
        "balance": (
            "SupplierFinanceProgramObligation",
            "SupplierFinanceProgramObligationCurrent",
        ),
        "charged": (
            "SupplierFinanceProgramObligationIncrease",
        ),
        "usage": (
            "SupplierFinanceProgramObligationDecreaseSettlement",
        ),
        "other": (),
        "revision": (),
        "base": (),
    },
    "goodwill": {
        "balance": (
            "Goodwill",
        ),
        "charged": (
            "GoodwillAcquiredDuringPeriod",
        ),
        "usage": (
            "GoodwillImpairmentLoss",
            "GoodwillWrittenOffRelatedToSaleOfBusinessUnit",
        ),
        "other": (
            "GoodwillForeignCurrencyTranslationGainLoss",
            "GoodwillPurchaseAccountingAdjustments",
            "GoodwillTransfers",
            "GoodwillOtherIncreaseDecrease",
            "GoodwillTranslationAndPurchaseAccountingAdjustments",
        ),
        "revision": (),
        "base": (),
    },
}
SCHEDULE_TWO = {
    "balance": (
        "ValuationAllowancesAndReservesBalance",
    ),
    "charged": (
        "ValuationAllowancesAndReservesChargedToCostAndExpense",
    ),
    "usage": (
        "ValuationAllowancesAndReservesDeductions",
    ),
    "other": (
        "ValuationAllowancesAndReservesChargedToOtherAccounts",
        "ValuationAllowancesAndReservesAdjustments",
        "ValuationAllowancesAndReservesRecoveries",
        "ValuationAllowancesAndReservesReservesOfBusinessesAcquired",
        "ValuationAllowancesAndReservesPeriodIncreaseDecrease",
    ),
    "revision": (),
    "base": (),
}
# the ticker whose committed instances use each element (grep, 2026-11-17)
CONFIRMED_IN = {
    "AccountsReceivableGross": "ADTN",
    "AccountsReceivableGrossCurrent": "LOGI",
    "AllowanceForDoubtfulAccountsReceivable": "CARR",
    "AllowanceForDoubtfulAccountsReceivableCurrent": "ADTN",
    "AllowanceForDoubtfulAccountsReceivableWriteOffs": "CIEN",
    "ContractWithCustomerLiability": "AAPL",
    "ContractWithCustomerLiabilityIncreaseDecreaseForContractAcquiredInBusinessCombination": "AMSC",
    "ContractWithCustomerLiabilityRevenueRecognized": "AAPL",
    "FinancingReceivableAllowanceForCreditLossForeignCurrencyTranslation": "CSCO",
    "FinancingReceivableAllowanceForCreditLossWriteoffAfterRecovery": "CSCO",
    "FinancingReceivableAllowanceForCreditLosses": "CSCO",
    "FinancingReceivableAllowanceForCreditLossesWriteOffs": "DELL",
    "FinancingReceivableBeforeAllowanceForCreditLossAndFee": "CSCO",
    "Goodwill": "ADTN",
    "GoodwillAcquiredDuringPeriod": "AMD",
    "GoodwillForeignCurrencyTranslationGainLoss": "ADTN",
    "GoodwillImpairmentLoss": "ADTN",
    "GoodwillOtherIncreaseDecrease": "CSCO",
    "GoodwillPurchaseAccountingAdjustments": "AMD",
    "GoodwillTransfers": "CARR",
    "GoodwillTranslationAndPurchaseAccountingAdjustments": "JCI",
    "GoodwillWrittenOffRelatedToSaleOfBusinessUnit": "AVGO",
    "InventoryGross": "CIEN",
    "InventoryValuationReserves": "AMSC",
    "InventoryWriteDown": "ADTN",
    "PaymentsForRestructuring": "ADTN",
    "ProductWarrantyAccrual": "AMD",
    "ProductWarrantyAccrualAdditionsFromBusinessAcquisition": "AMSC",
    "ProductWarrantyAccrualPayments": "AMD",
    "ProductWarrantyAccrualPreexistingIncreaseDecrease": "AMSC",
    "ProductWarrantyAccrualWarrantiesIssued": "AMD",
    "ProvisionForDoubtfulAccounts": "CIEN",
    "ProvisionForLoanLossesExpensed": "CSCO",
    "RestructuringCharges": "ADTN",
    "RestructuringReserve": "ADTN",
    "RestructuringReserveAccrualAdjustment1": "CSCO",
    "RestructuringReserveSettledWithoutCash2": "JCI",
    "RestructuringReserveTranslationAndOtherAdjustment": "CARR",
    "RestructuringSettlementAndImpairmentProvisions": "AVGO",
    "StandardAndExtendedProductWarrantyAccrualForeignCurrencyTranslationGainLoss": "JCI",
    "StandardProductWarrantyAccrual": "CLS",
    "StandardProductWarrantyAccrualAdditionsFromBusinessAcquisition": "GNRC",
    "StandardProductWarrantyAccrualForeignCurrencyTranslationGainLoss": "JCI",
    "StandardProductWarrantyAccrualPayments": "CLS",
    "StandardProductWarrantyAccrualPreexistingIncreaseDecrease": "GNRC",
    "StandardProductWarrantyAccrualWarrantiesIssued": "FN",
    "SupplierFinanceProgramObligation": "DELL",
    "SupplierFinanceProgramObligationCurrent": "JCI",
    "SupplierFinanceProgramObligationDecreaseSettlement": "DELL",
    "SupplierFinanceProgramObligationIncrease": "DELL",
    "ValuationAllowancesAndReservesAdjustments": "CARR",
    "ValuationAllowancesAndReservesBalance": "ADTN",
    "ValuationAllowancesAndReservesChargedToCostAndExpense": "ADTN",
    "ValuationAllowancesAndReservesChargedToOtherAccounts": "CLS",
    "ValuationAllowancesAndReservesDeductions": "ADTN",
    "ValuationAllowancesAndReservesPeriodIncreaseDecrease": "GNRC",
    "ValuationAllowancesAndReservesRecoveries": "LII",
    "ValuationAllowancesAndReservesReservesOfBusinessesAcquired": "CSCO",
}

FAMILIES = tuple(ELEMENTS)
# Schedule II's type axis, and the members that say which family a column is.
SCHEDULE_TWO_AXIS = "us-gaap:ValuationAllowancesAndReservesTypeAxis"
SCHEDULE_TWO_MEMBERS = {
    "us-gaap:AllowanceForCreditLossMember": "allowance_for_credit_losses",
    "us-gaap:InventoryValuationReserveMember": "inventory_reserve",
}
# the elements read as a magnitude, whichever sign the filer tagged
MAGNITUDE = ("ContractWithCustomerLiabilityRevenueRecognized",)
# what a row of the family's own table names, to know which row it is that this table
# could not place
STEMS = {
    "allowance_for_credit_losses": ("allowance", "doubtful", "creditloss", "loanloss"),
    "product_warranty": ("warrant",),
    "inventory_reserve": ("inventor",),
    "restructuring_reserve": ("restructuring",),
    "contract_liabilities": ("contractwithcustomerliab",),
    "supplier_finance_obligations": ("supplierfinance",),
    "goodwill": ("goodwill",),
}
SCHEDULE_TWO_STEMS = ("valuationallowancesandreserves",)
FLOW_ROLES = ("charged", "usage", "other", "revision")
# Foreign-currency translation of a reserve (a liability or a contra-asset) is tagged "gain
# (loss)", and filers differ over whether the printed increase of the reserve is the positive
# or the negative value: Cisco's 10-K and Johnson Controls' tag the printed +1 as -1, Lennox's
# and Logitech's 10-K tag it as printed, and Logitech's 10-Qs the other way. Goodwill is an
# asset and its gain adds, in every committed table. So these rows are read as tagged, and
# read with the sign reversed only where that, and nothing else, makes the table foot.
TRANSLATION_EITHER_WAY = (
    "FinancingReceivableAllowanceForCreditLossForeignCurrencyTranslation",
    "StandardProductWarrantyAccrualForeignCurrencyTranslationGainLoss",
    "StandardAndExtendedProductWarrantyAccrualForeignCurrencyTranslationGainLoss",
)
DAYS_TO_THE_BALANCE = 3                 # a balance tagged this near the day it stands for
A_YEAR = (350, 380)                     # days: the span `coverage_years` is read over
USD = "iso4217:USD"

WHAT_THIS_IS = (
    "for each reserve family the filing tables as a rollforward, the identity beginning + "
    "charged_to_expense + other - usage = ending, worked out by Python from the facts of the "
    "filing's own table (never summed across two tables or two sets of axes). `foots` says "
    "whether the table's rows add to its ending, `difference` is the stated ending less "
    "their sum, `complete` is false when the table holds a row Python could not place (a "
    "row the filer tagged in its own namespace; it is listed under `rows_not_placed`, and "
    "a table that does not foot and is not complete was not read in full). "
    "`provision_over_usage` is the charge over the usage; `coverage_years` is the "
    "beginning balance over the usage of a year; `ending_over_gross_base` is the "
    "ending reserve over the gross base the filing tags; "
    "`prior_period_revision_over_current_expense` is the table's change-in-estimate line "
    "over the charge; `release` is true when the charge is negative or the ending "
    "reserve fell while its gross base rose, with `release_because` saying which. "
    "Each cell prints the fact ids it came from. For supplier finance and goodwill the "
    "charged_to_expense line is the additions line of the table")

ROLE_OF: dict[str, tuple[str, str]] = {}
for _family, _roles in ELEMENTS.items():
    for _role, _names in _roles.items():
        if _role != "base":
            for _name in _names:
                ROLE_OF[_name] = (_family, _role)
SCHEDULE_ROLE = {name: role for role, names in SCHEDULE_TWO.items() for name in names}


def _dec(value) -> Decimal:
    return Decimal(str(value))


def _local(concept: str) -> str | None:
    return concept.split(":", 1)[1] if concept.startswith("us-gaap:") else None


def _axes_key(axes: dict | None) -> tuple:
    return tuple(sorted((axes or {}).items()))


def _date(text: str) -> dt.date:
    return dt.date.fromisoformat(text[:10])


def _row(one: dict) -> dict:
    return {"concept": one["concept"], "value": one["value"], "fact": one["fact"]}


def _usable(one: dict) -> bool:
    return (not one.get("nil") and one.get("unit") == USD
            and isinstance(one.get("value"), (int, float)) and not isinstance(one["value"], bool))


def classify(one: dict):
    """(family, role, kind, axes of the series) for a fact a role holds, or None."""
    local = _local(one["concept"])
    if local is None:
        return None
    axes = dict(one.get("axes") or {})
    if local in SCHEDULE_ROLE:
        family = SCHEDULE_TWO_MEMBERS.get(axes.pop(SCHEDULE_TWO_AXIS, None))
        return (family, SCHEDULE_ROLE[local], "schedule_two", _axes_key(axes)) if family else None
    if local in ROLE_OF and SCHEDULE_TWO_AXIS not in axes:
        family, role = ROLE_OF[local]
        return family, role, "note_table", _axes_key(axes)
    return None


def _natural(key: str) -> int:
    match = re.search(r"(\d+)$", key)
    return int(match.group(1)) if match else 0


def _series_in(key: str, table: dict) -> list[dict]:
    """Every series of one table: the facts a role holds, by family, kind and axes."""
    groups: dict[tuple, dict] = {}
    for one in table["facts"]:
        if not _usable(one):
            continue
        placed = classify(one)
        if placed is None:
            continue
        family, role, kind, axes = placed
        group = groups.setdefault((family, kind, axes), {"roles": {}, "table": key,
                                                         "paragraph": table.get("paragraph")})
        group["roles"].setdefault(role, []).append(one)
    out = []
    for (family, kind, axes), group in groups.items():
        group.update(family=family, kind=kind, axes=dict(axes))
        group["unplaced"] = _unplaced(table, family, kind, axes)
        out.append(group)
    return sorted(out, key=lambda group: (group["kind"], _axes_key(group["axes"])))


def _unplaced(table: dict, family: str, kind: str, axes: tuple) -> list[dict]:
    """Duration rows of this table, on this series' axes, that no role holds and whose name
    names the family."""
    stems = SCHEDULE_TWO_STEMS if kind == "schedule_two" else STEMS[family]
    found = []
    for one in table["facts"]:
        if not _usable(one) or "instant" in one or classify(one) is not None:
            continue
        concept = one["concept"].lower()
        if not any(stem in concept for stem in stems):
            continue
        own = dict(one.get("axes") or {})
        if kind == "schedule_two":
            if SCHEDULE_TWO_MEMBERS.get(own.pop(SCHEDULE_TWO_AXIS, None)) != family:
                continue
        if _axes_key(own) == axes:
            found.append(one)
    return found


def _nearest(balances: list[dict], day: dt.date) -> dict | None:
    close = [one for one in balances
             if abs((_date(one["instant"]) - day).days) <= DAYS_TO_THE_BALANCE]
    if not close:
        return None
    return min(close, key=lambda one: (abs((_date(one["instant"]) - day).days), one["fact"]))


def _balance_names(family: str, kind: str) -> tuple[str, ...]:
    return SCHEDULE_TWO["balance"] if kind == "schedule_two" else ELEMENTS[family]["balance"]


def _cell(rows: list[dict], total: Decimal) -> dict:
    return {"value": float(total), "facts": [one["fact"] for one in rows],
            "rows": [_row(one) for one in rows]}


def _flow_total(rows: list[dict]) -> Decimal:
    total = Decimal(0)
    for one in rows:
        total += abs(_dec(one["value"])) if _local(one["concept"]) in MAGNITUDE else \
            _dec(one["value"])
    return total


def _ratio(top: Decimal, bottom: Decimal, facts: list[str], *, why: str) -> dict:
    if bottom == 0:
        return {"missing": why, "facts": facts}
    return {"value": float(top / bottom), "facts": facts}


def _gross_base(family: str, axes: tuple, instant: str, tables: dict) -> dict:
    """The family's gross base at one date, on the series' axes, from any table of the filing:
    one value, or `missing` with the reason. Two different values at one date is ambiguous."""
    names = ELEMENTS[family]["base"]
    if not names:
        return {"missing": f"the filing's reserve of {family.replace('_', ' ')} has no gross base "
                           f"element in this section"}
    found = []
    for key in sorted(tables, key=_natural):
        for one in tables[key]["facts"]:
            if (_usable(one) and one.get("instant") == instant and _local(one["concept"]) in names
                    and _axes_key(one.get("axes")) == axes):
                found.append((key, one))
    if not found:
        return {"missing": f"the filing tags no {' or '.join(names)} at {instant} on these axes"}
    if len({_dec(one["value"]) for _, one in found}) > 1:
        return {"missing": f"the filing states more than one gross base at {instant}"}
    key, one = found[0]
    return {"value": one["value"], "concept": one["concept"], "instant": instant,
            "table": key, "facts": [one["fact"]]}


def _period(group: dict, start: str, end: str, tables: dict) -> dict:
    span = {"start": start, "end": end, "days": (_date(end) - _date(start)).days}
    roles = {role: [one for one in group["roles"].get(role, [])
                    if one.get("start") == start and one.get("end") == end]
             for role in FLOW_ROLES}
    flows = [one for role in FLOW_ROLES for one in roles[role]]
    out: dict = {"period": span}
    seen: dict[tuple, Decimal] = {}
    for one in flows:
        if seen.setdefault((one["concept"], _axes_key(one.get("axes"))),
                           _dec(one["value"])) != _dec(one["value"]):
            return {**out, "missing": f"the table states {one['concept']} twice over this span "
                                      f"with different values",
                    "facts": [one["fact"] for one in flows]}
    balances = [one for one in group["roles"].get("balance", []) if "instant" in one]
    chosen = None
    for name in _balance_names(group["family"], group["kind"]):
        same = [one for one in balances if _local(one["concept"]) == name]
        opening = _nearest(same, _date(start) - dt.timedelta(days=1))
        closing = _nearest(same, _date(end))
        if opening and closing and opening["fact"] != closing["fact"]:
            chosen = (opening, closing)
            break
    if chosen is None:
        # name the half that is missing
        have = [one["instant"] for one in balances]
        which = "beginning" if not any(
            abs((_date(day) - (_date(start) - dt.timedelta(days=1))).days)
            <= DAYS_TO_THE_BALANCE for day in have) else "ending"
        return {**out, "missing": f"the table states no {which} balance row for this span "
                                  f"(balance rows at {sorted(set(have)) or 'no date'})",
                "facts": [one["fact"] for one in flows]}
    opening, closing = chosen
    charged, usage = roles["charged"], roles["usage"]
    other = roles["other"] + roles["revision"]
    begin, end_value = _dec(opening["value"]), _dec(closing["value"])
    charge, spent, rest = _flow_total(charged), _flow_total(usage), _flow_total(other)
    expected = begin + charge + rest - spent
    difference = end_value - expected
    translation = sum((_dec(one["value"]) for one in other
                       if _local(one["concept"]) in TRANSLATION_EITHER_WAY), Decimal(0))
    sign = "as_tagged"
    if difference != 0 and translation != 0 and difference + 2 * translation == 0:
        sign = "reversed"
        rest -= 2 * translation
        expected = begin + charge + rest - spent
        difference = end_value - expected
    ordered = [opening] + charged + other + usage
    out["beginning"] = {"value": float(begin), "concept": opening["concept"],
                        "instant": opening["instant"], "facts": [opening["fact"]]}
    out["charged_to_expense"] = _cell(charged, charge) if charged else {
        "missing": "the table states no charge or additions row among the elements of "
                   "this section"}
    out["other"] = _cell(other, rest) if other else {
        "missing": "the table states no other row among the elements of this section"}
    out["usage"] = _cell(usage, spent) if usage else {
        "missing": "the table states no usage row among the elements of this section"}
    out["ending"] = {"value": float(end_value), "concept": closing["concept"],
                     "instant": closing["instant"], "facts": [closing["fact"]]}
    out["identity"] = "beginning + charged_to_expense + other - usage = ending"
    out["translation_sign"] = sign
    out["expected_ending"] = {"value": float(expected), "facts": [one["fact"] for one in ordered]}
    out["foots"] = difference == 0
    out["difference"] = {"value": float(difference),
                         "facts": [one["fact"] for one in ordered] + [closing["fact"]]}
    unplaced = [one for one in group["unplaced"]
                if one.get("start") == start and one.get("end") == end]
    out["complete"] = not unplaced
    out["rows_not_placed"] = [_row(one) for one in unplaced]
    # the measures
    out["provision_over_usage"] = (
        _ratio(charge, spent, [one["fact"] for one in charged + usage],
               why="the usage of the span is zero") if charged and usage else
        {"missing": "the table states no charge row or no usage row"})
    if spent and A_YEAR[0] <= span["days"] <= A_YEAR[1]:
        out["coverage_years"] = _ratio(begin, spent, [opening["fact"]] + [
            one["fact"] for one in usage], why="the usage of the span is zero")
    else:
        out["coverage_years"] = {
            "missing": ("the usage of the span is zero or the table states none" if not spent
                        else f"the span is {span['days']} days, and coverage is read over a year")}
    revision = roles["revision"]
    out["prior_period_revision_over_current_expense"] = (
        _ratio(_flow_total(revision), charge,
               [one["fact"] for one in revision + charged],
               why="the charge of the span is zero") if revision and charged else
        {"missing": "the table has no change-in-estimate row or no charge row"})
    base_end = _gross_base(group["family"], _axes_key(group["axes"]), closing["instant"], tables)
    base_begin = _gross_base(group["family"], _axes_key(group["axes"]), opening["instant"],
                             tables)
    out["gross_base"] = {"beginning": base_begin, "ending": base_end}
    if "value" in base_end:
        ratio = _ratio(end_value, _dec(base_end["value"]),
                       [closing["fact"]] + base_end["facts"], why="the gross base is zero")
        out["ending_over_gross_base"] = ratio
    else:
        out["ending_over_gross_base"] = {"missing": base_end["missing"]}
    because = []
    if charged and charge < 0:
        because.append("charged_to_expense_negative")
    if (end_value < begin and "value" in base_end and "value" in base_begin
            and _dec(base_end["value"]) > _dec(base_begin["value"])):
        because.append("reserve_fell_while_gross_base_rose")
    out["release"] = bool(because)
    out["release_because"] = because
    return out


def _family(name: str, tables: dict) -> dict:
    series = []
    for key in sorted(tables, key=_natural):
        for group in _series_in(key, tables[key]):
            if group["family"] != name:
                continue
            spans = sorted({(one["start"], one["end"]) for role in FLOW_ROLES
                            for one in group["roles"].get(role, []) if "start" in one},
                           key=lambda span: (span[1], span[0]), reverse=True)
            spans = [span for span in spans if _date(span[1]) > _date(span[0])]
            if not spans:
                continue
            series.append({"table": key, "paragraph": group["paragraph"], "kind": group["kind"],
                           "axes": group["axes"],
                           "periods": [_period(group, start, end, tables)
                                       for start, end in spans]})
    if not series:
        names = ", ".join(ELEMENTS[name]["balance"]
                          + (SCHEDULE_TWO["balance"] if name in SCHEDULE_TWO_MEMBERS.values()
                             else ()))
        return {"missing": f"no table of the filing's notes carries a rollforward of "
                           f"{name.replace('_', ' ')}: no balance row ({names}) with a flow row "
                           f"of the same table, on the same axes, over a span"}
    return {"series": series}


def build(note_table_facts: dict) -> dict:
    """`rollforwards` for the calculator: each family's series from the filing's note tables
    (`note_tables.from_run`'s output), or `missing` with the reason."""
    if "tables" not in note_table_facts:
        reason = note_table_facts.get("missing", "no note table was read")
        return {"what_this_is": WHAT_THIS_IS, **{name: {"missing": reason} for name in FAMILIES}}
    tables = note_table_facts["tables"]
    return {"what_this_is": WHAT_THIS_IS, **{name: _family(name, tables) for name in FAMILIES}}
