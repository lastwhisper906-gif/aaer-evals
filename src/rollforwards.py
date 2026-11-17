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

**The sign of a row whose element does not fix its own direction is the one the filing
prints.** Recoveries, adjustments, acquisitions, translation, transfers and "other" rows
(the `other` role) are tagged with whichever sign the filer chose, and filers differ:
NSSC prints a deduction (7) and tags it +7 as `Recoveries`; Cisco prints 3 and
tags -3, Johnson Controls prints (1) and tags +1, Logitech's 10-Q prints 94 and tags
-94, Lennox prints (0.8) and tags -0.8. Such a row contributes the sign the inline table
prints (parentheses round the number, read by `note_tables.printed_signs` and carried
as `printed_signs`), `sign_source` "printed" and `sign_disagrees` where the tag differs;
where no printed sign was read it contributes its tagged value, `sign_source` "tagged".
Whether the table foots never decides a sign.

**What a table may hold that no role places.** Every duration row of the table, over the
period's span, on the series' axes or on more (an acquisition member beside the
segment), that no role of the series holds and that no other series with balances of its
own holds, is listed under `rows_not_placed` and makes `complete` false: a row the
filer tagged in its own namespace, a us-gaap element this table leaves out (a net change),
a row on an extra axis (never summed into a role), a row with no dated span. A zero row
counts. A table that does not foot and is not complete is a table Python could not read
in full, not a finding. One figure the filing tags twice, for the same dates and value, is
one row.

**The elements, and how each was confirmed.** `ELEMENTS` and `SCHEDULE_TWO` below are
the us-gaap elements of each role, and `CONFIRMED_IN` names the ticker whose committed
instances (`tests/fixtures`) use each one, which `tests/test_calculator_rollforwards.py`
greps. An element nobody confirmed is not in the table. Left out for that reason or
because its sign or meaning is not fixed: the extended-warranty elements
(`ExtendedProductWarrantyAccrual...`, deferred revenue, not a reserve), the current
and noncurrent splits of a balance (`...Current`, `...Noncurrent`, `ProductWarrantyAccrualClassifiedCurrent`),
`ProductWarrantyAccrualPeriodIncreaseDecrease`, `RestructuringReservePeriodIncreaseDecrease`
and `ValuationAllowancesAndReservesPeriodIncreaseDecrease` (a net change that a filer states
beside or instead of its components),
`FinancingReceivableAllowanceForCreditLossLoanSold`, the cumulative catch-up and
time-frame elements of contract liabilities (signed changes to revenue, no balance
leaving), `GoodwillGross` as a gross base (it excludes impairments, so a goodwill
that fell by impairment would read as a release) and `NotesReceivableGross`. Every
`AccountsReceivableAllowanceForCreditLoss...` element the current taxonomy names was
absent from the committed instances, which tag `AllowanceForDoubtfulAccountsReceivable...`.
Schedule II's other accounts (a filer's own members, such as Omnicell's
`omcl:AccountsReceivableAndUnbilledReceivablesMember`) are the series of the family
`schedule_two_other`, each with its `member`; only the deferred tax asset valuation allowance
is left out. `RestructuringCosts` and `RestructuringCostsAndAssetImpairmentCharges` are the
restructuring provision. Left out because they are no row of the family's own rollforward: the
measurement-period adjustments `BusinessCombinationProvisionalInformationInitialAccounting
IncompleteAdjustment...` (rows of a purchase price allocation, found beside goodwill), and
every flow on an extra axis, which is its own series with no balance (an acquisition member of
a segment, the period axis of Flex's restructuring), listed in `rows_not_placed`.
`ValuationAllowancesAndReservesPeriodIncreaseDecrease`, a net change like its two
siblings above, is a row no role holds. Goodwill has no
`release` (it is not a reserve, its impairment is its usage, a negative purchase
accounting adjustment is not a release): the cell is null and says why.
"""

from __future__ import annotations

import datetime as dt
import re
from decimal import Decimal

ELEMENTS = {
    "schedule_two_other": {
        "balance": (), "charged": (), "usage": (), "other": (), "revision": (), "base": (),
    },
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
            "RestructuringCosts",
            "RestructuringCostsAndAssetImpairmentCharges",
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
    "RestructuringCosts": "ADTN",
    "RestructuringCostsAndAssetImpairmentCharges": "AVGO",
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
    "ValuationAllowancesAndReservesRecoveries": "LII",
    "ValuationAllowancesAndReservesReservesOfBusinessesAcquired": "CSCO",
}

FAMILIES = tuple(ELEMENTS)
# Schedule II's type axis, and the members that say which family a column is.
SCHEDULE_TWO_AXIS = "us-gaap:ValuationAllowancesAndReservesTypeAxis"
# Any other account of Schedule II, the filer's own members among them (Omnicell's
# `omcl:AccountsReceivableAndUnbilledReceivablesMember`), is a series of the family below,
# keyed by its member. The deferred tax asset valuation allowance is no reserve of this
# section's and is left out.
SCHEDULE_TWO_OTHER = "schedule_two_other"
SCHEDULE_TWO_LEFT_OUT = ("us-gaap:ValuationAllowanceOfDeferredTaxAssetsMember",)
SCHEDULE_TWO_MEMBERS = {
    "us-gaap:AllowanceForCreditLossMember": "allowance_for_credit_losses",
    "us-gaap:InventoryValuationReserveMember": "inventory_reserve",
}
# the elements read as a magnitude, whichever sign the filer tagged
MAGNITUDE = ("ContractWithCustomerLiabilityRevenueRecognized",)
FLOW_ROLES = ("charged", "usage", "other", "revision")
# A row whose element does not fix its own direction (recoveries, adjustments, translation,
# acquisitions, transfers, "other") is tagged with whichever sign the filer chose: Cisco
# prints 3 and tags -3, Johnson Controls prints (1) and tags +1, Logitech's 10-Q prints 94 and
# tags -94, Lennox prints (0.8) and tags -0.8, and NSSC prints a deduction (7) and tags it
# +7 as `Recoveries`. Such a row (the `other` role, the change-in-estimate rows with it)
# contributes the sign the filing prints (parentheses round the number, as
# `note_tables.printed_signs` reads them), and where no printed sign was read, the tagged
# value, with `sign_source` saying which. Whether the table foots never decides a sign. A
# charge and a usage row keep their role's direction.
DAYS_TO_THE_BALANCE = 3                 # a balance tagged this near the day it stands for
A_YEAR = (350, 380)                     # days: the span `coverage_years` is read over
USD = "iso4217:USD"

WHAT_THIS_IS = (
    "for each reserve family the filing tables as a rollforward, the identity beginning + "
    "charged_to_expense + other - usage = ending, worked out by Python from the facts of the "
    "filing's own table (never summed across two tables or two sets of axes). `foots` says "
    "whether the table's rows add to its ending, `difference` is the stated ending less "
    "their sum, and `complete` is false when the table holds any other row of the same span "
    "that no role holds (a row the filer tagged in its own namespace, a row on an extra axis "
    "such as an acquisition, a row with no dated span, a net change); each is listed under "
    "`rows_not_placed`, and a `foots` false beside a `complete` false is a table not read in "
    "full. `difference` is the stated ending less the rows. Every row of `other` takes the sign "
    "the filing prints, for every row whose element does not fix its own direction "
    "(recoveries, adjustments, acquisitions, translation, transfers, other): parentheses round "
    "the number is negative, `sign_source` printed, and the tagged value where no printed sign "
    "was read, `sign_source` tagged; a row whose printed and tagged signs differ says "
    "`sign_disagrees`. A charge and a usage row keep their role's direction. "
    "`provision_over_usage` is the charge over the usage; "
    "`coverage_years` is the beginning balance over the usage of a year; "
    "`ending_over_gross_base` is the ending reserve over the gross base the filing tags; "
    "`prior_period_revision_over_current_expense` is the table's change-in-estimate line "
    "over the charge; `release` is true when the charge is negative or the ending "
    "reserve fell while its gross base rose, with `release_because` saying which (goodwill "
    "has no release: it is null). "
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


def _dated(one: dict) -> bool:
    """A duration with a start and an end the filing dates; a `forever` context, or one the
    instance does not carry, has none."""
    return isinstance(one.get("start"), str) and isinstance(one.get("end"), str)


def _contribution(one: dict, signs: dict, signed: bool = False) -> tuple[Decimal, str | None,
                                                                         bool]:
    """What a row adds to (or, in the usage role, takes from) the identity, where its sign
    came from ("printed", "tagged", or None for a row whose sign is no question), and whether
    the printed sign differs from the tagged one."""
    value = _dec(one["value"])
    if _local(one["concept"]) in MAGNITUDE:
        return abs(value), None, False
    if signed and value != 0:
        printed = signs.get(one["fact"])
        if printed:
            read = -abs(value) if printed == "negative" else abs(value)
            return read, "printed", (read < 0) != (value < 0)
        return value, "tagged", False
    return value, None, False


def _row(one: dict, signs: dict | None = None, signed: bool = False) -> dict:
    out = {"concept": one["concept"], "value": one["value"], "fact": one["fact"]}
    if signs is not None and signed:
        if one["value"] == 0:
            # a zero has no sign to read: it adds nothing, whichever way it is printed
            out["contribution"], out["sign_source"] = 0.0, "tagged"
            return out
        contribution, source, disagrees = _contribution(one, signs, True)
        out["contribution"] = float(contribution)
        out["sign_source"] = source
        if source == "printed":
            out["sign_disagrees"] = disagrees
    return out


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
        member = axes.get(SCHEDULE_TWO_AXIS)
        if member in SCHEDULE_TWO_MEMBERS:
            del axes[SCHEDULE_TWO_AXIS]
            return (SCHEDULE_TWO_MEMBERS[member], SCHEDULE_ROLE[local], "schedule_two",
                    _axes_key(axes))
        if member and member not in SCHEDULE_TWO_LEFT_OUT:
            return SCHEDULE_TWO_OTHER, SCHEDULE_ROLE[local], "schedule_two", _axes_key(axes)
        return None
    if local in ROLE_OF and SCHEDULE_TWO_AXIS not in axes:
        family, role = ROLE_OF[local]
        return family, role, "note_table", _axes_key(axes)
    return None


def _natural(key: str) -> int:
    match = re.search(r"(\d+)$", key)
    return int(match.group(1)) if match else 0


def _series_in(key: str, table: dict) -> list[dict]:
    """Every series of one table: the facts a role holds, by family, kind and axes. One figure
    the filing tags twice, in two contexts of the same dates and value, is one row."""
    groups: dict[tuple, dict] = {}
    seen: set = set()
    for one in table["facts"]:
        if not _usable(one):
            continue
        placed = classify(one)
        if placed is None:
            continue
        family, role, kind, axes = placed
        group = groups.setdefault((family, kind, axes), {"roles": {}, "table": key,
                                                         "paragraph": table.get("paragraph")})
        if role != "balance" and "instant" not in one and not _dated(one):
            group.setdefault("undated", []).append(one)
            continue
        same = (family, kind, axes, one["concept"], one.get("instant"), one.get("start"),
                one.get("end"), _dec(one["value"]))
        group.setdefault("ids", set()).add(one["fact"])
        if same in seen:
            continue
        seen.add(same)
        group["roles"].setdefault(role, []).append(one)
    out = []
    for (family, kind, axes), group in groups.items():
        group.update(family=family, kind=kind, axes=dict(axes))
        out.append(group)
    return sorted(out, key=lambda group: (group["kind"], _axes_key(group["axes"])))


def _unplaced_pool(table: dict, group: dict, accounted: set) -> list[dict]:
    """Every duration row of this table that no role of this series holds, on this series' axes
    or on a superset of them (an acquisition member of a segment), that another series with
    balances of its own has not taken: a row the filer tagged in its own namespace, a row on
    an extra axis, a net change, a row with no dated span."""
    found, seen = [], set()
    for one in table["facts"]:
        if not _usable(one) or "instant" in one or one["fact"] in accounted:
            continue
        own = dict(one.get("axes") or {})
        member = own.get(SCHEDULE_TWO_AXIS)
        if group["kind"] == "schedule_two":
            # a filer's own account keeps its member among the axes, so another account's
            # rows are no superset of them; a standard account is told by its member
            if group["family"] != SCHEDULE_TWO_OTHER:
                if SCHEDULE_TWO_MEMBERS.get(member) != group["family"]:
                    continue
                del own[SCHEDULE_TWO_AXIS]
        elif member is not None:
            continue
        if not set(group["axes"].items()) <= set(own.items()):
            continue
        same = (one["concept"], _axes_key(own), one.get("start"), one.get("end"),
                _dec(one["value"]))
        if same not in seen:
            seen.add(same)
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


def _cell(rows: list[dict], total: Decimal, signs: dict, signed: bool = False) -> dict:
    out = {"value": float(total), "facts": [one["fact"] for one in rows],
           "rows": [_row(one, signs, signed) for one in rows]}
    sources = [row["sign_source"] for row in out["rows"]
               if "sign_source" in row and row["value"] != 0]
    if signed and not sources and rows:
        out["sign_source"], out["sign_disagrees"] = "tagged", False
    elif sources:
        out["sign_source"] = "tagged" if "tagged" in sources else "printed"
        out["sign_disagrees"] = any(row.get("sign_disagrees") for row in out["rows"])
    return out


def _flow_total(rows: list[dict], signs: dict, signed: bool = False) -> Decimal:
    total = Decimal(0)
    for one in rows:
        total += _contribution(one, signs, signed)[0]
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


def _period(group: dict, start: str, end: str, tables: dict, signs: dict) -> dict:
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
    charge = _flow_total(charged, signs)
    spent = _flow_total(usage, signs)
    rest = _flow_total(other, signs, True)
    expected = begin + charge + rest - spent
    difference = end_value - expected
    ordered = [opening] + charged + other + usage
    out["beginning"] = {"value": float(begin), "concept": opening["concept"],
                        "instant": opening["instant"], "facts": [opening["fact"]]}
    out["charged_to_expense"] = _cell(charged, charge, signs) if charged else {
        "missing": "the table states no charge or additions row among the elements of "
                   "this section"}
    out["other"] = _cell(other, rest, signs, True) if other else {
        "missing": "the table states no other row among the elements of this section"}
    out["usage"] = _cell(usage, spent, signs) if usage else {
        "missing": "the table states no usage row among the elements of this section"}
    out["ending"] = {"value": float(end_value), "concept": closing["concept"],
                     "instant": closing["instant"], "facts": [closing["fact"]]}
    out["identity"] = "beginning + charged_to_expense + other - usage = ending"
    out["expected_ending"] = {"value": float(expected), "facts": [one["fact"] for one in ordered]}
    out["foots"] = difference == 0
    out["difference"] = {"value": float(difference),
                         "facts": [one["fact"] for one in ordered] + [closing["fact"]]}
    unplaced = [one for one in group["unplaced_pool"]
                if not _dated(one) or (one.get("start") == start and one.get("end") == end)]
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
        _ratio(_flow_total(revision, signs, True), charge,
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
    if group["family"] == "goodwill":
        out["release"] = None
        out["release_because"] = []
        out["release_note"] = ("goodwill has no release: it is not a reserve, its impairment is "
                               "its usage, and a negative acquisition adjustment is a revision "
                               "of the purchase price allocation")
        return out
    because = []
    if charged and charge < 0:
        because.append("charged_to_expense_negative")
    if (end_value < begin and "value" in base_end and "value" in base_begin
            and _dec(base_end["value"]) > _dec(base_begin["value"])):
        because.append("reserve_fell_while_gross_base_rose")
    out["release"] = bool(because)
    out["release_because"] = because
    return out


def _family(name: str, tables: dict, signs: dict) -> dict:
    series = []
    for key in sorted(tables, key=_natural):
        groups = _series_in(key, tables[key])
        balanced = [group for group in groups if group["roles"].get("balance")]
        accounted = {fact_id for group in balanced for fact_id in group.get("ids", ())}
        for group in balanced:
            if group["family"] != name:
                continue
            spans = sorted({(one["start"], one["end"]) for role in FLOW_ROLES
                            for one in group["roles"].get(role, [])},
                           key=lambda span: (span[1], span[0]), reverse=True)
            spans = [span for span in spans if _date(span[1]) > _date(span[0])]
            if not spans:
                continue
            pool = _unplaced_pool(tables[key], group, accounted)
            group["unplaced_pool"] = pool
            series.append({"table": key, "paragraph": group["paragraph"], "kind": group["kind"],
                           "axes": group["axes"],
                           **({"member": group["axes"][SCHEDULE_TWO_AXIS]}
                              if name == SCHEDULE_TWO_OTHER else {}),
                           "periods": [_period(group, start, end, tables, signs)
                                       for start, end in spans]})
    if not series:
        names = ", ".join(ELEMENTS[name]["balance"]
                          + (SCHEDULE_TWO["balance"] if name in (*SCHEDULE_TWO_MEMBERS.values(), SCHEDULE_TWO_OTHER)
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
    signs = note_table_facts.get("printed_signs", {})
    return {"what_this_is": WHAT_THIS_IS,
            **{name: _family(name, tables, signs) for name in FAMILIES}}
