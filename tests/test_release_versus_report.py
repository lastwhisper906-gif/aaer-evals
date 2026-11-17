"""The earnings release beside the report, judged against numbers read by eye.

Three kinds of expected value, each named where it is used:

- **Dell's committed release, read by eye.** `runs/DELL/0001571996-26-000046/input_8k.md`
  prints, in the table of paragraph `0001571996-26-000039:8k_2_02:35`, the rows
  `Net revenue | $ | 46,971`, `Net income | $ | 4,133`, `Change in cash from operating
  activities | $ | 2,225` and `Earnings per share — diluted | $ | 6.34` for the three
  months ended July 31, 2026 and, beside them, 90,813, 7,571, 6,306 and 11.58 for the
  six. Each is set against the same period read out of the committed companyfacts
  record by `tests/companyfacts_source.py`, which imports nothing from `src/`.
  NVIDIA's release row `Revenue | $ | 96,221` (three months ended July 26, 2026) is
  the second company's line.
- **Planted tables.** A release cell that differs from a report fact, the sign
  written by hand: 1,000 million printed against 1,200 million tagged is
  -200 million, the release the smaller; 1,300 against 1,200 is +100 million.
- **The label table itself**: every label is a row of a committed release, and
  none is two lines.

    python3.12 -m pytest tests/test_release_versus_report.py -q
"""

from __future__ import annotations

import datetime as dt
import glob
from pathlib import Path

import pytest

from src import calculator, release_versus_report as rvr
from tests import companyfacts_source as source

REPO_ROOT = Path(__file__).resolve().parent.parent
DELL_RUN = REPO_ROOT / "runs" / "DELL" / "0001571996-26-000046"
DELL_CUTOFF = "2026-09-08"
DELL_QUARTER = "2026-05-02..2026-07-31"
DELL_YEAR_TO_DATE = "2026-01-31..2026-07-31"
DELL_TABLE = "0001571996-26-000039:8k_2_02:35"


@pytest.fixture(scope="module")
def dell():
    out = calculator.calculate(ticker="DELL", cutoff=DELL_CUTOFF, period_end="2026-07-31",
                               form="10-Q", accession="0001571996-26-000046")
    return out["release_versus_report"]


@pytest.fixture(scope="module")
def nvidia():
    out = calculator.calculate(ticker="NVDA", cutoff="2026-08-26", period_end="2026-07-26",
                               form="10-Q", accession="0001045810-26-000075")
    return out["release_versus_report"]


def _cells(entry: dict, months: int) -> list[dict]:
    """Every table's cell for the span: each table of the release votes."""
    found = [c for c in entry["comparisons"] if c["span_months"] == months]
    assert found, entry
    return found


def _by_months(entry: dict, months: int) -> dict:
    """The first table's cell for the span; the tests that use it also hold every other
    table's cell to the same verdict."""
    found = _cells(entry, months)
    assert {c["verdict"] for c in found} == {found[0]["verdict"]}, found
    return found[0]


# --- Dell, read by eye -------------------------------------------------------------------

def test_release_versus_report_dell_rows_are_in_the_committed_release():
    """The rows the expected values below were read from are in the committed file."""
    text = (DELL_RUN / "input_8k.md").read_text(encoding="utf-8")
    assert f"[{DELL_TABLE}]" in text
    for row in ("| Net revenue | $ | 46,971 |", "| Net income | $ | 4,133 |",
                "| Change in cash from operating activities | $ | 2,225 |",
                "| Earnings per share — diluted | $ | 6.34 |"):
        assert row in text


def test_release_versus_report_dell_net_income_agrees_with_the_quarters_net_income(dell):
    """`Net income | $ | 4,133` (millions) is the report's NetIncomeLoss for the quarter."""
    expected = source.one_value("DELL", "NetIncomeLoss", DELL_QUARTER, DELL_CUTOFF)
    assert expected == 4_133 * 1_000_000
    cell = _by_months(dell["lines"]["net_income"], 3)
    assert cell["release"]["cell"] == "4,133"
    assert cell["release"]["paragraph_id"] == DELL_TABLE
    assert cell["release"]["value"] == 4_133_000_000.0
    assert cell["report"]["value"] == expected
    assert cell["report"]["formula"] == "the quarter as stated"
    assert cell["report"]["parts"]["0"]["id"] == \
        "0001571996-26-000046:facts:NetIncomeLoss:2026-05-02..2026-07-31"
    assert cell["difference"] == 0.0 and cell["sign"] == "equal"
    assert cell["verdict"] == "agrees"
    # Dell prints the quarter's net income in four tables (the summary, the statement, the
    # cash-flow statement and the reconciliation), and each one is compared
    assert [c["release"]["paragraph_id"].split(":")[-1] for c in _cells(
        dell["lines"]["net_income"], 3)] == ["35", "63", "74", "103"]


def test_release_versus_report_dell_revenue_and_cash_flow_agree_for_the_quarter_and_the_six_months(dell):
    revenue = dell["lines"]["revenue"]
    assert _by_months(revenue, 3)["release"]["value"] == 46_971 * 1_000_000
    assert _by_months(revenue, 3)["report"]["value"] == \
        source.one_value("DELL", "Revenues", DELL_QUARTER, DELL_CUTOFF)
    assert _by_months(revenue, 6)["release"]["value"] == 90_813 * 1_000_000
    assert _by_months(revenue, 6)["report"]["value"] == \
        source.one_value("DELL", "Revenues", DELL_YEAR_TO_DATE, DELL_CUTOFF)
    cash = dell["lines"]["operating_cash_flow"]
    six = _by_months(cash, 6)
    assert six["release"]["value"] == 6_306 * 1_000_000
    assert six["report"]["value"] == source.one_value(
        "DELL", "NetCashProvidedByUsedInOperatingActivities", DELL_YEAR_TO_DATE, DELL_CUTOFF)
    # the three months' cash flow is not a statement of the 10-Q; the report's
    # quarter is the six months less the three, and the release's 2,225 is that
    assert _by_months(cash, 3)["release"]["value"] == 2_225 * 1_000_000
    assert _by_months(cash, 3)["report"]["value"] == 2_225 * 1_000_000
    for entry in (revenue, cash):
        assert {c["verdict"] for c in entry["comparisons"]} == {"agrees"}


def test_release_versus_report_dell_diluted_earnings_per_share_agrees_at_two_decimals(dell):
    eps = _by_months(dell["lines"]["diluted_earnings_per_share"], 3)
    rows = source.rows("DELL", "EarningsPerShareDiluted", unit="USD/shares")
    stated = [row["val"] for row in rows if source.spelled(row) == DELL_QUARTER
              and row["filed"] <= DELL_CUTOFF]
    assert stated == [6.34]
    assert eps["release"]["cell"] == "6.34" and eps["release"]["printed_decimals"] == 2
    assert eps["report"]["value"] == 6.34 and eps["verdict"] == "agrees"


def test_release_versus_report_dell_prints_capital_expenditure_under_a_label_not_read(dell):
    """Dell's cash-flow statement prints `Capital expenditures and capitalized software
    development costs | (1,239)` (three months, millions) and `(2,202)` (six). That is not a
    stated label, so the line is not compared; it is not `not_in_release` either, because the
    row prints a figure for the period: `printed_under_another_label`, with the row's label,
    paragraph id and figure."""
    entry = dell["lines"]["capital_expenditure"]
    assert entry["verdict"] == "printed_under_another_label"
    assert "comparisons" not in entry
    assert [(r["label"], r["paragraph_id"].split(":")[-1], r["span_months"], r["cell"])
            for r in entry["rows"]] == [
        ("Capital expenditures and capitalized software development costs", "74", 3, "(1,239)"),
        ("Capital expenditures and capitalized software development costs", "74", 6, "(2,202)")]
    text = (DELL_RUN / "input_8k.md").read_text(encoding="utf-8")
    assert "| Capital expenditures and capitalized software development costs | (1,239) |" in text
    # a line no row names at all stays not_in_release
    assert _compare([_row("Net revenue", "1,000")], {"revenue": {"value": 1e9}}
                    )["capital_expenditure"]["verdict"] == "not_in_release"


def test_release_versus_report_second_company_nvidia_revenue(nvidia):
    """NVIDIA's release row `Revenue | $ | 96,221` (millions, three months ended July 26,
    2026) against its Revenues for 2026-04-27..2026-07-26."""
    expected = source.one_value("NVDA", "Revenues", "2026-04-27..2026-07-26", "2026-08-26")
    assert expected == 96_221 * 1_000_000
    cell = _by_months(nvidia["lines"]["revenue"], 3)
    assert cell["release"]["cell"] == "96,221"
    assert cell["report"]["value"] == expected and cell["verdict"] == "agrees"


def test_release_versus_report_is_missing_with_its_reason_when_no_release_is_on_record():
    """TTMI's 10-Q was filed 2026-08-05 and its release (accession 0001193125-26-336163)
    on 2026-08-06, so at the 10-Q's cutoff there is none."""
    out = calculator.release_versus_report(
        calculator.Record({"facts": {"us-gaap": {}}}), {"balance_now": "2026-06-29"},
        ticker="TTMI", cutoff=dt.date(2026, 8, 5), fixtures_root=calculator.cutoff_guard.FIXTURES)
    assert "missing" in out and "no earnings release" in out["missing"]


# --- planted tables ------------------------------------------------------------------------

def _table(rows: list[str], *, header=("Three Months Ended", "June 30, 2026", "(in millions)")):
    span, date, unit = header
    return "\n".join([f"|  | {span} |", f"|  | {date} |  | June 30, 2025 |", f"|  | {unit} |"]
                     + rows)


def _row(label: str, cell: str, prior: str = "1") -> str:
    return f"| {label} | $ | {cell} |  |  | $ | {prior} |"


def _compare(rows: list[str], report: dict, **options):
    table = _table(rows, **options)

    def read(line, months):
        found = report.get(line)
        return found if found is not None else {"missing": "no planted fact"}

    return rvr.compare(["planted:8k_2_02:1"], [table], "2026-06-30", read)


def test_release_versus_report_planted_release_smaller_than_the_report_has_a_negative_sign():
    """1,000 million printed against 1,200 million tagged: the release less the report is
    -200 million, and the release is the smaller."""
    out = _compare([_row("Net revenue", "1,000")], {"revenue": {"value": 1_200_000_000.0}})
    cell = out["revenue"]["comparisons"][0]
    assert cell["difference"] == -200_000_000.0
    assert cell["sign"] == "release_smaller"
    assert cell["verdict"] == out["revenue"]["verdict"] == "differs"


def test_release_versus_report_planted_release_larger_than_the_report_has_a_positive_sign():
    out = _compare([_row("Net revenue", "1,300")], {"revenue": {"value": 1_200_000_000.0}})
    cell = out["revenue"]["comparisons"][0]
    assert cell["difference"] == 100_000_000.0
    assert cell["sign"] == "release_larger" and cell["verdict"] == "differs"


@pytest.mark.parametrize("report,verdict", [
    (4_133_000_000.0, "agrees"),
    (4_133_400_000.0, "agrees"),        # rounds to 4,133 million
    (4_132_500_000.0, "agrees"),        # half rounds up to 4,133
    (4_133_499_999.0, "agrees"),        # still 4,133
    (4_133_500_000.0, "differs"),       # half rounds up to 4,134
    (4_132_499_999.0, "differs"),       # rounds to 4,132
    (4_134_000_000.0, "differs"),
])
def test_release_versus_report_a_release_in_millions_agrees_at_its_own_precision(report, verdict):
    out = _compare([_row("Net income", "4,133")], {"net_income": {"value": report}})
    cell = out["net_income"]["comparisons"][0]
    assert cell["verdict"] == verdict, report
    # the difference is still written exactly, whatever the verdict
    assert cell["difference"] == 4_133_000_000.0 - report


@pytest.mark.parametrize("report,verdict", [
    (6.34, "agrees"), (6.3449, "agrees"), (6.335, "agrees"), (6.345, "differs"),
    (6.33, "differs"), (6.3349, "differs"),
])
def test_release_versus_report_per_share_agrees_at_the_printed_decimals(report, verdict):
    out = _compare([_row("Diluted earnings per share", "6.34")],
                   {"diluted_earnings_per_share": {"value": report}})
    assert out["diluted_earnings_per_share"]["comparisons"][0]["verdict"] == verdict, report


def test_release_versus_report_a_release_in_thousands_steps_by_a_thousand_dollars():
    out = _compare([_row("Net sales", "216,122")], {"revenue": {"value": 216_122_400.0}},
                   header=("Three Months Ended", "June 30, 2026", "(in thousands)"))
    assert out["revenue"]["verdict"] == "agrees"
    out = _compare([_row("Net sales", "216,122")], {"revenue": {"value": 216_123_000.0}},
                   header=("Three Months Ended", "June 30, 2026", "(in thousands)"))
    assert out["revenue"]["verdict"] == "differs"


def test_release_versus_report_a_decimal_in_the_release_sets_a_finer_step():
    """`1,570.7` in millions steps by a tenth of a million."""
    out = _compare([_row("Revenue", "1,570.7")], {"revenue": {"value": 1_570_740_000.0}})
    assert out["revenue"]["verdict"] == "agrees"
    out = _compare([_row("Revenue", "1,570.7")], {"revenue": {"value": 1_570_760_000.0}})
    assert out["revenue"]["verdict"] == "differs"


def test_release_versus_report_capital_expenditure_in_parentheses_is_compared_by_its_size():
    out = _compare([_row("Capital expenditures", "(1,239)")],
                   {"capital_expenditure": {"value": 1_239_000_000.0}})
    assert out["capital_expenditure"]["verdict"] == "agrees"
    out = _compare([_row("Capital expenditures", "(1,239)")],
                   {"capital_expenditure": {"value": 1_300_000_000.0}})
    cell = out["capital_expenditure"]["comparisons"][0]
    assert cell["difference"] == -61_000_000.0 and cell["sign"] == "release_smaller"


def test_release_versus_report_a_loss_in_parentheses_keeps_its_sign():
    out = _compare([_row("Net income", "(12)")], {"net_income": {"value": -12_000_000.0}})
    assert out["net_income"]["verdict"] == "agrees"
    out = _compare([_row("Net income", "(12)")], {"net_income": {"value": 12_000_000.0}})
    assert out["net_income"]["comparisons"][0]["difference"] == -24_000_000.0


def test_release_versus_report_a_line_the_release_does_not_print_is_not_in_release():
    out = _compare([_row("Net revenue", "1,000")], {"revenue": {"value": 1_000_000_000.0}})
    for line in rvr.LINES:
        if line != "revenue":
            assert out[line]["verdict"] == "not_in_release", line
            assert "comparisons" not in out[line]
    assert out["revenue"]["verdict"] == "agrees"


def test_release_versus_report_a_label_that_is_only_part_of_a_row_label_is_not_the_line():
    """Labels are compared whole: `Non-GAAP net income` is not `Net income`, and `Revenue growth`
    is not `Revenue`; the second prints a figure for the period under words that hold the
    stated label, so it is listed, never compared and never called absent."""
    out = _compare([_row("Non-GAAP net income", "9,999"), _row("Revenue growth", "5")],
                   {"net_income": {"value": 1.0}, "revenue": {"value": 1.0}})
    assert out["net_income"]["verdict"] == "not_in_release"
    assert out["revenue"]["verdict"] == "printed_under_another_label"
    assert [r["label"] for r in out["revenue"]["rows"]] == ["Revenue growth"]


def test_release_versus_report_a_line_the_report_lacks_is_named_and_not_filled():
    out = _compare([_row("Net income", "4,133")], {})
    cell = out["net_income"]["comparisons"][0]
    assert cell["verdict"] == "report_fact_missing" and "difference" not in cell
    assert out["net_income"]["verdict"] == "report_fact_missing"


def test_release_versus_report_the_period_is_the_period_end_and_a_span_the_header_states():
    """A prior-year column is not compared, and a table whose header says no dates is
    `period_not_read`, with its reason, never `not_in_release`."""
    table = "\n".join(["|  | Q2 FY27 | Q1 FY27 |", "| (in millions) |  |  |",
                       "| Revenue | $96,221 | $81,615 |"])
    out = rvr.compare(["p:1"], [table], "2026-06-30", lambda line, months: {"value": 1.0})
    assert out["revenue"]["verdict"] == "period_not_read"
    assert out["revenue"]["unread"][0]["paragraph_id"] == "p:1"
    assert out["revenue"]["unread"][0]["reason"]
    out = _compare([_row("Net income", "4,133")], {"net_income": {"value": 4_133_000_000.0}},
                   header=("Three Months Ended", "March 31, 2026", "(in millions)"))
    assert out["net_income"]["verdict"] == "period_not_read"


def test_release_versus_report_header_forms_the_committed_releases_use():
    """Month and day over a row of years (NVIDIA), one span over a month and day with
    its years (Carrier), the whole column in a cell (ESCO), two spans over four dates
    (Dell), each read to the same end date and span."""
    nvidia = ["|  | Three Months Ended |  | Six Months Ended |", "|  | July 26, |  | July 27, |  | July 26, |  | July 27, |",
              "|  | 2026 |  | 2025 |  | 2026 |  | 2025 |", "| ($ in millions) |",
              "| Revenue | $ | 96,221 |  | $ | 46,743 |  | $ | 177,837 |  | $ | 90,805 |"]
    carrier = ["|  | Three Months Ended June 30 |", "| (In millions) | 2026 | 2025 | Change |",
               "| Net sales | $ | 6,351 |  | $ | 6,113 |  | 4 | % |"]
    escoe = ["|  | Three Months Ended June 30, 2026 |  | Three Months Ended June 30, 2025 |",
             "| Net Sales | $ | 339.0 |  | 296.3 |", "| (in millions) |"]
    for rows, expected in ((nvidia, [3, 6]), (carrier, [3]), ([escoe[0], escoe[2], escoe[1]], [3])):
        table = "\n".join(rows)
        seen = []
        out = rvr.compare(["p:1"], [table], "2026-07-26" if rows is nvidia else "2026-06-30",
                          lambda line, months: seen.append(months) or {"value": 1.0})
        entry = out["revenue"]
        assert [c["span_months"] for c in entry["comparisons"]] == expected, (rows[0], entry)


def test_release_versus_report_a_row_that_agrees_does_not_hide_one_that_does_not():
    """The first row agrees and the second row of the same table differs, and the other
    way about: all rows must agree, and each is listed."""
    for first, second in (("1,000", "1,100"), ("1,100", "1,000")):
        table = _table([_row("Net sales", first), _row("Total net sales", second)])
        out = rvr.compare(["p:1"], [table], "2026-06-30",
                          lambda line, months: {"value": 1_000_000_000.0})
        assert out["revenue"]["verdict"] == "differs", (first, second)
        assert sorted(c["verdict"] for c in out["revenue"]["comparisons"]) == ["agrees", "differs"]


def test_release_versus_report_each_table_is_compared_at_its_own_printed_precision():
    """Ciena's case: the summary in millions prints 1,570.7 and the statement in thousands
    1,570,778 for a report fact of 1,570,739,000. The summary cannot see a 39,000 dollar
    difference and the statement can."""
    summary = _table([_row("Revenue", "1,570.7")])
    statement = _table([_row("Total revenue", "1,570,778")],
                       header=("Three Months Ended", "June 30, 2026", "(in thousands)"))
    out = rvr.compare(["p:1", "p:2"], [summary, statement], "2026-06-30",
                      lambda line, months: {"value": 1_570_739_000.0})
    verdicts = {c["release"]["paragraph_id"]: c for c in out["revenue"]["comparisons"]}
    assert verdicts["p:1"]["verdict"] == "agrees"
    assert verdicts["p:2"]["verdict"] == "differs"
    assert verdicts["p:2"]["difference"] == 39_000.0 and verdicts["p:2"]["sign"] == "release_larger"
    assert out["revenue"]["verdict"] == "differs"


def _blocks(rows):
    return "\n".join(["|  | Three Months Ended |", "|  | June 30, 2026 |  | June 30, 2025 |",
                      "| (in millions) |"] + rows)


def test_release_versus_report_per_share_rows_stay_in_the_per_share_line():
    rows = ["| Earnings per share: |", _row("Diluted earnings per share", "6.34")]
    out = rvr.compare(["p:1"], [_blocks(rows)], "2026-06-30",
                      lambda line, months: {"value": 6.34})
    assert out["diluted_earnings_per_share"]["verdict"] == "agrees"


def test_release_versus_report_an_empty_verdict_list_is_not_in_release():
    assert rvr.line_verdict([]) == "not_in_release"


def test_release_versus_report_the_precedence_holds_through_compare_both_ways():
    """A differing cell in one table and an unreadable table: `differs`. An agreeing cell
    and an unreadable table: `period_not_read`, not `agrees`."""
    unread = "\n".join(["|  | Q2 FY27 |", "| (in millions) |", "| Net revenue | 5 |"])
    for ids, tables in ((["p:1", "p:2"], [_table([_row("Net revenue", "1,100")]), unread]),
                        (["p:2", "p:1"], [unread, _table([_row("Net revenue", "1,100")])])):
        out = rvr.compare(ids, tables, "2026-06-30",
                          lambda line, months: {"value": 1_000_000_000.0})
        assert out["revenue"]["verdict"] == "differs"
    tables = [unread, _table([_row("Net revenue", "1,000")])]
    out = rvr.compare(["p:1", "p:2"], tables, "2026-06-30",
                      lambda line, months: {"value": 1_000_000_000.0})
    assert out["revenue"]["verdict"] == "period_not_read"
    assert [c["verdict"] for c in out["revenue"]["comparisons"]] == ["agrees"]
    out = rvr.compare(["p:1"], [_table([_row("Net revenue", "1,000")])], "2026-06-30",
                      lambda line, months: {"missing": "none"})
    assert out["revenue"]["verdict"] == "report_fact_missing"


# --- the label table ------------------------------------------------------------------------

def _labels_in_the_committed_releases() -> dict[str, set[str]]:
    """Every row label of every pipe row of every committed `input_8k.md` that has a
    figure after it, found with a reader of its own: split on the pipe, take the first
    cell that has text, keep the row if a later cell looks like a number. It uses nothing
    from `src/release_versus_report.py`."""
    import re
    found: dict[str, set[str]] = {}
    for path in glob.glob(str(REPO_ROOT / "runs" / "*" / "*" / "input_8k.md")):
        ticker = Path(path).parts[-3]
        for line in Path(path).read_text(encoding="utf-8").splitlines():
            if not (line.startswith("| ") and line.endswith(" |")):
                continue
            cells = [cell.strip() for cell in line[2:-2].split(" | ")]
            text = [i for i, cell in enumerate(cells) if cell]
            if not text:
                continue
            label, later = cells[text[0]], cells[text[0] + 1:]
            if not any(re.fullmatch(r"\(?\$?\(?[\d,]*\d(\.\d+)?\)?%?", cell) for cell in later):
                continue
            label = label.lower().replace("\u2014", "-").replace("\u2013", "-")
            label = re.sub(r"\s+", " ", label).strip().rstrip(":").strip()
            label = re.sub(r"(\s*\((\d{1,2}|[a-z])\)|\s*\*+)+$", "", label)
            found.setdefault(label, set()).add(ticker)
    return found


def test_release_versus_report_every_label_is_a_row_of_a_committed_release():
    found = _labels_in_the_committed_releases()
    unconfirmed = [(line, label) for line, labels in EXPECTED_LABELS.items() for label in labels
                   if label.lower() not in found]
    assert unconfirmed == []


# The table as the specification states it, written out here and not read from
# the module: a label dropped from `ROW_LABELS`, or moved to another line, or added,
# is a difference from this list. Each label is confirmed above in a committed release.
EXPECTED_LABELS = {
    "revenue": ("Net revenue", "Total net revenue", "Net sales", "Total net sales", "Revenue",
                "Total revenue", "Revenues", "Total revenues"),
    "cost_of_revenue": ("Cost of revenue", "Total cost of revenue", "Cost of revenues",
                        "Cost of sales", "Total cost of sales", "Total cost of goods sold",
                        "Costs of goods sold"),
    "operating_income": ("Operating income", "Income from operations", "Operating income (loss)",
                         "Operating profit", "GAAP operating income",
                         "GAAP income from operations"),
    "pretax_income": ("Income before income taxes", "Income before provision for income taxes",
                      "Earnings before income taxes", "Income before income tax",
                      "Income from continuing operations before income taxes",
                      "Earnings before taxes (EBT)"),
    "income_tax_expense": ("Income tax expense", "Provision for income taxes",
                           "Income tax provision", "Income tax (benefit) expense",
                           "Income tax (expense) benefit", "Income taxes"),
    "net_income": ("Net income", "Net earnings", "Net income (loss)", "Net earnings (loss)",
                   "GAAP net income", "Net income (GAAP)",
                   "Net income attributable to Generac Holdings Inc.",
                   "Net income attributable to Johnson Controls",
                   "Net earnings (loss) attributable to common shareowners"),
    "diluted_earnings_per_share": ("Diluted earnings per share", "Earnings per share - diluted",
                                   "Diluted EPS", "GAAP diluted EPS",
                                   "GAAP diluted net income per share",
                                   "Diluted earnings per share (EPS)",
                                   "Diluted net income per potential common share",
                                   "GAAP net income per share, diluted"),
    "operating_cash_flow": ("Net cash provided by operating activities",
                            "Change in cash from operating activities",
                            "Net cash flows provided by operating activities",
                            "Net cash flows provided by (used in) operating activities",
                            "Cash generated by operating activities",
                            "GAAP net cash provided by operating activities"),
    "capital_expenditure": ("Capital expenditures", "Purchases of property and equipment",
                            "Purchases of property, plant, and equipment",
                            "Expenditures for property and equipment",
                            "Payments for acquisition of property, plant and equipment"),
}


def test_release_versus_report_the_label_table_is_the_stated_one():
    assert {line: set(labels) for line, labels in rvr.ROW_LABELS.items()} == \
        {line: set(labels) for line, labels in EXPECTED_LABELS.items()}


def test_release_versus_report_the_nine_lines_are_the_nine_the_row_names():
    assert rvr.LINES == ("revenue", "cost_of_revenue", "operating_income", "pretax_income",
                         "income_tax_expense", "net_income", "diluted_earnings_per_share",
                         "operating_cash_flow", "capital_expenditure")
    assert set(rvr.ROW_LABELS) == set(rvr.LINES)


def test_release_versus_report_the_stated_table_gives_no_label_to_two_lines():
    owners = rvr.label_owners(rvr.ROW_LABELS)
    assert all(len(lines) == 1 for lines in owners.values())
    assert rvr.refuse_shared_labels(rvr.ROW_LABELS) == rvr.LINE_OF_LABEL


def test_release_versus_report_a_label_matched_to_two_lines_is_refused():
    planted = {"revenue": ("Net sales", "Total revenue"),
               "cost_of_revenue": ("Cost of sales", "total  Revenue")}
    with pytest.raises(rvr.ReleaseLabelError, match="total revenue"):
        rvr.refuse_shared_labels(planted)


@pytest.mark.parametrize("line,label", [(line, label) for line, labels in EXPECTED_LABELS.items()
                                        for label in labels])
def test_release_versus_report_each_label_reads_its_own_line_and_no_other(line, label):
    value = "(7)" if line == "capital_expenditure" or label == "Income tax (expense) benefit" else ("2.50" if line == "diluted_earnings_per_share"
                                                          else "7")
    report = 2.5 if line == "diluted_earnings_per_share" else 7_000_000.0
    out = _compare([_row(label, value)], {line: {"value": report}})
    assert out[line]["verdict"] == "agrees", (line, label)
    assert [other for other in rvr.LINES
            if other != line and out[other]["verdict"] != "not_in_release"] == []


@pytest.mark.parametrize("label", ["Sales", "Diluted", "Basic",
                                   "Capital expenditures and capitalized software development costs",
                                   "Non-GAAP net income", "Adjusted free cash flow"])
def test_release_versus_report_labels_left_out_on_purpose_stay_out(label):
    """`Sales` is a segment's row in three committed releases, `Diluted` is a heading's
    sub-row (earnings per share in one table, shares in the next), `Income tax (expense)
    benefit` prints an expense as a negative, and the last three are other measures."""
    assert rvr.normal_label(label) not in rvr.LINE_OF_LABEL


def test_release_versus_report_labels_ignore_case_spacing_dashes_and_a_footnote_mark():
    assert rvr.normal_label("  TOTAL   net sales (1)") == "total net sales"
    assert rvr.normal_label("Earnings per share — diluted") == "earnings per share - diluted"
    assert rvr.normal_label("Net income*") == "net income"
    assert rvr.normal_label("Net income:") == "net income"
    # a parenthetical that is part of the label stays
    assert rvr.normal_label("Operating income (loss)") == "operating income (loss)"


# --- reading cells ----------------------------------------------------------------------------

@pytest.mark.parametrize("text,expected", [
    ("4,133", (4133, 0)), ("(13)%", (-13, 0)), ("1,570.7", (15707, 1)), ("$96,221", (96221, 0)),
    ("(168,202", (-168202, 0)), ("—", (0, 0)), ("58%", (58, 0)), ("6.34", (634, 2)),
])
def test_release_versus_report_cells_read_as_the_figures_they_print(text, expected):
    value, decimals = rvr.read_number(text)
    assert value * (10 ** expected[1]) == expected[0] and decimals == expected[1]


@pytest.mark.parametrize("text", ["", "$", "%", ")", "Net income", "July 31, 2026", "(unaudited)"])
def test_release_versus_report_a_cell_that_is_not_a_figure_is_not_read(text):
    assert rvr.read_number(text) is None


def test_release_versus_report_pipe_rows_round_trip_to_their_cells():
    assert rvr.cells_of("|  | Three Months Ended |  |  |") == ["", "Three Months Ended", "", ""]
    assert rvr.cells_of("| Net income | $ | 4,133 |") == ["Net income", "$", "4,133"]


def test_release_versus_report_reads_the_structure_input_8k_is_written_from():
    """The paragraphs the comparison reads are the ones `input_8k.md` carries, under the
    same ids: the committed file's Dell table is the same text."""
    from src import parse_8k
    release = parse_8k.earnings_release("DELL", cutoff=DELL_CUTOFF)
    item = release["item_2_02"]
    text = (DELL_RUN / "input_8k.md").read_text(encoding="utf-8")
    for identifier, paragraph in zip(item["paragraph_ids"], item["paragraphs"]):
        assert f"[{identifier}]\n{paragraph}\n" in text


# --- headers, units, figure counts --------------------------------------------------------

@pytest.mark.parametrize("phrase,months", [
    ("Three Months Ended", 3), ("Six Months Ended", 6), ("Nine Months Ended", 9),
    ("Twelve Months Ended", 12), ("Year Ended", 12), ("Quarter Ended", 3)])
def test_release_versus_report_each_span_a_header_names_is_that_many_months(phrase, months):
    table = "\n".join([f"|  | {phrase} |", "|  | June 30, 2026 |  | June 30, 2025 |",
                       "| (in millions) |", _row("Net income", "100")])
    header = rvr.read_header([rvr.cells_of(line) for line in table.split("\n")])
    assert [c["months"] for c in header["columns"]] == [months, months]
    out = rvr.compare(["p:1"], [table], "2026-06-30", lambda line, m: {"value": 1e8})
    assert [c["span_months"] for c in out["net_income"]["comparisons"]] == [months]


def test_release_versus_report_a_header_with_the_words_run_together_is_read():
    """Carrier's `Six Months EndedJune 30,` has no space before the month. Here the three
    months end earlier (March 31), so only the six-month columns are the period, and they
    are found only if the run-together month is read as a date of its own."""
    table = "\n".join(["|  | Three Months Ended March 31, |  | Six Months EndedJune 30, |",
                       "| (In millions) | 2026 | 2025 | 2026 | 2025 |",
                       "| Net sales | $ | 6,351 |  | $ | 6,113 |  | $ | 11,692 |  | $ | 11,331 |"])
    header = rvr.read_header([rvr.cells_of(line) for line in table.split("\n")])
    assert [(c["months"], c["end"].isoformat()) for c in header["columns"]] == [
        (3, "2026-03-31"), (3, "2025-03-31"), (6, "2026-06-30"), (6, "2025-06-30")]
    out = rvr.compare(["p:1"], [table], "2026-06-30",
                      lambda line, months: {"value": {6: 11.692e9}[months]})
    assert [(c["span_months"], c["verdict"]) for c in out["revenue"]["comparisons"]] == [
        (6, "agrees")]
    assert out["revenue"]["comparisons"][0]["release"]["cell"] == "11,692"


def test_release_versus_report_a_misdated_header_is_never_a_false_difference():
    """A release whose header dates its columns a quarter early, or only a year early,
    has no column for the period: `period_not_read`, with the cells never compared."""
    for date in ("March 31, 2026", "June 30, 2025"):
        table = "\n".join(["|  | Three Months Ended |", f"|  | {date} |", "| (in millions) |",
                           _row("Net income", "9,999")])
        out = rvr.compare(["p:1"], [table], "2026-06-30", lambda line, m: {"value": 1e8})
        assert out["net_income"]["verdict"] == "period_not_read", date
        assert out["net_income"]["comparisons"] == []
    # years in the other order: the 2026 column is still the second figure
    table = "\n".join(["|  | Three Months Ended June 30, |", "| (in millions) | 2025 | 2026 |",
                       "| Net income | $ | 90 |  | $ | 100 |"])
    out = rvr.compare(["p:1"], [table], "2026-06-30", lambda line, m: {"value": 1e8})
    assert out["net_income"]["verdict"] == "agrees"
    assert out["net_income"]["comparisons"][0]["release"]["cell"] == "100"


def test_release_versus_report_a_row_with_the_wrong_count_of_figures_is_not_read():
    """Three figures under a header of two columns are not read at the first two."""
    table = _table(["| Net income | $ | 100 |  | $ | 90 |  | $ | 80 |"])
    out = rvr.compare(["p:1"], [table], "2026-06-30", lambda line, m: {"value": 1e8})
    assert out["net_income"]["verdict"] == "period_not_read"
    assert out["net_income"]["comparisons"] == []
    assert "3 figures" in out["net_income"]["unread"][0]["reason"]
    table = _table(["| Net income | $ | 100 |"])
    out = rvr.compare(["p:1"], [table], "2026-06-30", lambda line, m: {"value": 1e8})
    assert out["net_income"]["verdict"] == "period_not_read"


def test_release_versus_report_no_unit_statement_is_never_assumed_to_be_millions():
    table = _table([_row("Net income", "100")], header=("Three Months Ended", "June 30, 2026",
                                                         "unaudited"))
    out = rvr.compare(["p:1"], [table], "2026-06-30", lambda line, m: {"value": 1e8})
    assert out["net_income"]["verdict"] == "period_not_read"
    assert "no unit statement" in out["net_income"]["unread"][0]["reason"]
    assert out["net_income"]["comparisons"] == []


def test_release_versus_report_a_unit_in_a_sentence_is_not_a_tables_unit():
    """Prose that says millions is not the table's statement. A title line that is only
    the statement `(In millions, except per share amounts)` is, and carries to the next
    table that prints none."""
    bare = _table([_row("Net income", "100")], header=("Three Months Ended", "June 30, 2026",
                                                        "unaudited"))
    for sentence in ("Net income was reported in millions of dollars for the quarter.",
                     "Revenue grew to 5 in millions as the company said in thousands of calls."):
        out = rvr.compare(["p:0", "p:1"], [sentence, bare], "2026-06-30",
                          lambda line, m: {"value": 1e8})
        assert out["net_income"]["verdict"] == "period_not_read", sentence
    out = rvr.compare(["p:0", "p:1"], ["(In millions, except per share amounts)", bare],
                      "2026-06-30", lambda line, m: {"value": 1e8})
    assert out["net_income"]["verdict"] == "agrees"
    # the first unit statement of a title that names two is the dollars'
    out = rvr.compare(["p:0", "p:1"], ["(In millions, except shares, which are in thousands)",
                                      bare], "2026-06-30", lambda line, m: {"value": 1e8})
    assert out["net_income"]["comparisons"][0]["release"]["scale"] == "millions"


# --- the refuter's plants, in the committed releases ---------------------------------------

def _run_inputs(ticker: str, accession: str):
    import json
    run = next(iter(sorted((REPO_ROOT / "runs" / ticker).glob(f"{accession}*"))))
    published = json.loads((run / "calculator.json").read_text(encoding="utf-8"))
    cutoff = dt.date.fromisoformat(published["cutoff"])
    from src import trends
    document, _ = calculator.supplemented(trends.read_record(ticker, cutoff), run, cutoff)
    record = calculator.Record(document)
    periods = calculator.trigger_periods(record.usd, published["period_end"], published["form"])
    return run, cutoff, record, periods


def _planted_full(ticker: str, accession: str, plants: dict[str, tuple[str, str]]) -> dict:
    """The committed release with figures changed in named paragraphs (the paragraph
    number after `8k_2_02:`), each change the first occurrence of an exact string, read
    through the calculator against the real record and the filing's own segments. Returns
    the whole `release_versus_report` section."""
    from src import parse_8k
    run, cutoff, record, periods = _run_inputs(ticker, accession)
    release = parse_8k.earnings_release(ticker, cutoff=cutoff)
    item = release["item_2_02"]
    paragraphs = list(item["paragraphs"])
    for number, (old, new) in plants.items():
        index = next(i for i, pid in enumerate(item["paragraph_ids"])
                     if pid.endswith(f":8k_2_02:{number}"))
        assert old in paragraphs[index], (number, old)
        paragraphs[index] = paragraphs[index].replace(old, new, 1)     # the first one
    planted = dict(release, item_2_02=dict(item, paragraphs=paragraphs))
    return calculator.release_versus_report(
        record, periods, ticker=ticker, cutoff=cutoff,
        fixtures_root=calculator.cutoff_guard.FIXTURES, release=planted,
        facts=calculator.instance_facts(run, cutoff))


def _planted(ticker: str, accession: str, plants: dict[str, tuple[str, str]]) -> dict:
    return _planted_full(ticker, accession, plants)["lines"]


def _in_table(entry: dict, number: str) -> list[dict]:
    return [c for c in entry["comparisons"]
            if c["release"]["paragraph_id"].endswith(f":8k_2_02:{number}")]


def test_release_versus_report_planted_dell_net_income_and_revenue_in_the_statement_differ():
    lines = _planted("DELL", "0001571996-26-000046", {
        "63": ("| Net income | $ | 4,133 |", "| Net income | $ | 4,233 |")})
    entry = lines["net_income"]
    assert entry["verdict"] == "differs"
    bad = _in_table(entry, "63")
    assert [(c["span_months"], c["verdict"], c["difference"], c["sign"]) for c in bad
            if c["span_months"] == 3] == [(3, "differs", 100_000_000.0, "release_larger")]
    assert [c["verdict"] for c in _in_table(entry, "35")] == ["agrees", "agrees"]
    lines = _planted("DELL", "0001571996-26-000046", {
        "63": ("| Total net revenue | 46,971 |", "| Total net revenue | 47,971 |")})
    revenue = [c for c in _in_table(lines["revenue"], "63") if c["span_months"] == 3]
    assert lines["revenue"]["verdict"] == "differs"
    assert [(c["verdict"], c["difference"]) for c in revenue] == [("differs", 1_000_000_000.0)]


def test_release_versus_report_planted_carrier_net_sales_operating_profit_and_net_earnings_differ():
    lines = _planted("CARR", "0001783180-26-000032", {
        "84": ("| Total Net sales |  | 6,351 |", "| Total Net sales |  | 6,451 |")})
    assert lines["revenue"]["verdict"] == "differs"
    assert [(c["verdict"], c["difference"]) for c in _in_table(lines["revenue"], "84")
            if c["span_months"] == 3] == [("differs", 100_000_000.0)]
    lines = _planted("CARR", "0001783180-26-000032", {
        "84": ("| Operating profit |  | 825 |", "| Operating profit |  | 925 |")})
    assert lines["operating_income"]["verdict"] == "differs"
    # the first `Net earnings (loss) attributable` row is the one changed, and the
    # second, further down the same table, still agrees: no row hides another
    lines = _planted("CARR", "0001783180-26-000032", {
        "84": ("| Net earnings (loss) attributable to common shareowners |  | $ | 501 |",
               "| Net earnings (loss) attributable to common shareowners |  | $ | 601 |")})
    quarter = [c for c in _in_table(lines["net_income"], "84") if c["span_months"] == 3]
    assert lines["net_income"]["verdict"] == "differs"
    assert sorted(c["verdict"] for c in quarter if c["release"]["cell"] in ("601", "501")) \
        == ["agrees", "differs"]


def test_release_versus_report_planted_ciena_statement_in_thousands_catches_what_the_summary_cannot():
    lines = _planted("CIEN", "0001628280-26-040767", {
        "55": ("| Total revenue | 1,570,739 |", "| Total revenue | 1,570,778 |")})
    entry = lines["revenue"]
    assert entry["verdict"] == "differs"
    statement = [c for c in _in_table(entry, "55") if c["span_months"] == 3]
    assert [(c["verdict"], c["difference"]) for c in statement] == [("differs", 39_000.0)]
    # the summary table (paragraph 19) states its unit only in a sentence above it, which
    # is not a unit, so it is not read: its 1,570.7 million could not have caught the 39,000
    assert [r["paragraph_id"].split(":")[-1] for r in entry["unread"]] == ["19"]


def test_release_versus_report_planted_apple_statement_row_against_the_footnote_totals():
    lines = _planted("AAPL", "0000320193-26-000020", {
        "29": ("| Total net sales (1) | 109,417 |", "| Total net sales (1) | 109,517 |")})
    entry = lines["revenue"]
    assert entry["verdict"] == "differs"
    quarter = [c for c in entry["comparisons"] if c["span_months"] == 3]
    assert sorted((c["release"]["label"], c["verdict"]) for c in quarter) == [
        ("Total net sales", "agrees"), ("Total net sales", "agrees"),
        ("Total net sales (1)", "differs")]
    assert [c["difference"] for c in quarter if c["verdict"] == "differs"] == [100_000_000.0]


# --- expected values read through the companyfacts record, by hand ---------------------

def test_release_versus_report_dell_quarters_operating_cash_flow_is_the_six_months_less_the_three():
    """The 10-Q states Dell's operating cash flow for six months (6,306 million) and for
    the first quarter (4,081 million); the second quarter's is the difference, 2,225
    million, worked here from the record. The release's `Change in cash from operating
    activities | 2,225` is the three-month cell, and the calculator's report side is the
    same difference."""
    tag = "NetCashProvidedByUsedInOperatingActivities"
    six = source.one_value("DELL", tag, "2026-01-31..2026-07-31", DELL_CUTOFF)
    first = source.one_value("DELL", tag, "2026-01-31..2026-05-01", DELL_CUTOFF)
    assert (six, first) == (6_306_000_000.0, 4_081_000_000.0)
    assert six - first == 2_225_000_000.0
    out = calculator.calculate(ticker="DELL", cutoff=DELL_CUTOFF, period_end="2026-07-31",
                               form="10-Q", accession="0001571996-26-000046")
    cell = _by_months(out["release_versus_report"]["lines"]["operating_cash_flow"], 3)
    assert cell["report"]["value"] == six - first
    assert cell["release"]["value"] == 2_225 * 1_000_000




# --- a heading may label a cell and never hide it ----------------------------------------------

def _fact(**values):
    """A planted report: line -> value, anything else missing."""
    return lambda line, months: ({"value": values[line]} if line in values
                                 else {"missing": "no planted fact"})


def _run(rows, report, **options):
    return rvr.compare(["p:1"], [_blocks(rows)], "2026-06-30", report, **options)


def test_release_versus_report_the_precedence_is_a_total_order_and_each_pair_holds_both_ways():
    order = rvr.PRECEDENCE
    assert order == ("differs", "differs_outside_gaap", "block_not_identified",
                     "report_fact_missing", "period_not_read", "agrees")
    for i, higher in enumerate(order):
        for lower in order[i + 1:]:
            assert rvr.line_verdict([higher, lower]) == higher, (higher, lower)
            assert rvr.line_verdict([lower, higher]) == higher, (higher, lower)
            assert rvr.line_verdict([lower, higher, lower, "agrees"]) == higher


def test_release_versus_report_the_flags_among_themselves_rank_as_stated():
    """The refuter found the order of these three untested."""
    for first, second in (("block_not_identified", "report_fact_missing"),
                          ("block_not_identified", "period_not_read"),
                          ("report_fact_missing", "period_not_read")):
        assert rvr.line_verdict([first, second]) == first
        assert rvr.line_verdict([second, first]) == first


def test_release_versus_report_an_empty_verdict_list_is_not_in_release():
    assert rvr.line_verdict([]) == "not_in_release"


def test_release_versus_report_the_precedence_holds_through_compare_each_way():
    """Through the whole comparison: a GAAP cell that differs outranks a differing cell
    outside GAAP, an unread table, and an agreeing cell; each flag outranks agrees."""
    unread = "\n".join(["|  | Q2 FY27 |", "| (in millions) |", "| Net revenue | 5 |"])
    good, bad = _table([_row("Net revenue", "1,000")]), _table([_row("Net revenue", "1,100")])
    fact = lambda line, months: {"value": 1_000_000_000.0}      # noqa: E731
    for ids, tables in ((["p:1", "p:2"], [bad, unread]), (["p:2", "p:1"], [unread, bad]),
                        (["p:1", "p:2"], [good, bad]), (["p:1", "p:2"], [bad, good])):
        assert rvr.compare(ids, tables, "2026-06-30", fact)["revenue"]["verdict"] == "differs"
    out = rvr.compare(["p:2", "p:1"], [unread, good], "2026-06-30", fact)
    assert out["revenue"]["verdict"] == "period_not_read"
    assert [c["verdict"] for c in out["revenue"]["comparisons"]] == ["agrees"]
    out = rvr.compare(["p:1"], [good], "2026-06-30", lambda line, months: {"missing": "none"})
    assert out["revenue"]["verdict"] == "report_fact_missing"
    # a GAAP difference outranks a difference outside GAAP, in either order
    rows_gaap_first = ["| GAAP |", _row("Net income", "110"), "| Non-GAAP |",
                       _row("Net income", "130")]
    rows_outside_first = ["| Non-GAAP |", _row("Net income", "130"), "| GAAP |",
                          _row("Net income", "110")]
    for rows in (rows_gaap_first, rows_outside_first):
        assert _run(rows, _fact(net_income=1e8))["net_income"]["verdict"] == "differs"


def test_release_versus_report_a_non_gaap_heading_labels_the_rows_and_never_hides_them():
    """GAAP above non-GAAP, the same label in both: the GAAP cell is held to the report; the
    cell under the non-GAAP heading is compared too, labelled `unidentified` (a heading
    is prose), and if only it differs the line is `differs_outside_gaap`, with the hint, the
    paragraph id and both values listed."""
    rows = ["| GAAP |", _row("Net income", "100"), "| Non-GAAP |", _row("Net income", "130")]
    out = _run(rows, _fact(net_income=1e8))
    assert out["net_income"]["verdict"] == "differs_outside_gaap"
    assert [(c["release"]["cell"], c["block"], c["verdict"])
            for c in out["net_income"]["comparisons"]] == [
        ("100", "gaap", "agrees"), ("130", "unidentified", "differs")]
    listed, = out["net_income"]["differs_outside_gaap"]
    assert listed["hint"] == "unidentified" and listed["paragraph_id"] == "p:1"
    assert listed["release"]["value"] == 130_000_000.0 and listed["report"]["value"] == 1e8
    assert listed["difference"] == 30_000_000.0
    # the GAAP cell wrong: `differs`
    rows[1] = _row("Net income", "110")
    assert _run(rows, _fact(net_income=1e8))["net_income"]["verdict"] == "differs"


def test_release_versus_report_the_non_gaap_block_first_hides_nothing_either():
    rows = ["| Non-GAAP |", _row("Net income", "130"), "| GAAP |", _row("Net income", "110")]
    out = _run(rows, _fact(net_income=1e8))
    assert out["net_income"]["verdict"] == "differs"
    assert [(c["release"]["cell"], c["block"]) for c in out["net_income"]["comparisons"]] == [
        ("130", "unidentified"), ("110", "gaap")]
    only_non_gaap = _run(rows[:2], _fact(net_income=1e8))
    assert only_non_gaap["net_income"]["verdict"] == "differs_outside_gaap"


def test_release_versus_report_a_non_gaap_total_closes_the_block_its_heading_opened():
    rows = [_row("Operating income", "5,385"), "| Non-GAAP adjustments: |",
            _row("Amortization of intangibles", "96"), _row("Non-GAAP operating income", "5,929"),
            _row("Net income", "4,133")]
    out = _run(rows, _fact(operating_income=5.385e9, net_income=4.133e9))
    assert [c["block"] for c in out["net_income"]["comparisons"]] == ["gaap"]
    assert [c["block"] for c in out["operating_income"]["comparisons"]] == ["gaap"]
    rows[0] = _row("Operating income", "5,485")
    assert _run(rows, _fact(operating_income=5.385e9, net_income=4.133e9)
                )["operating_income"]["verdict"] == "differs"


def test_release_versus_report_a_columns_own_header_says_not_gaap_and_is_still_compared():
    named = "\n".join(["|  | GAAP Results |  | Non-GAAP Results |",
                       "|  | Quarter Ended |  | Quarter Ended |", "|  | June 30, |  | June 30, |",
                       "|  | 2026 |  | 2026 |", "| (in millions) |",
                       "| Net income | $ | 100 |  | $ | 130 |"])
    out = rvr.compare(["p:1"], [named], "2026-06-30", _fact(net_income=1e8))
    assert [(c["release"]["cell"], c["block"]) for c in out["net_income"]["comparisons"]] == [
        ("100", "gaap"), ("130", "not_gaap")]
    assert out["net_income"]["verdict"] == "differs_outside_gaap"
    assert out["net_income"]["differs_outside_gaap"][0]["hint"] == "not_gaap"
    # the column that says Adjusted, the whole word, is not GAAP either
    adjusted = named.replace("Non-GAAP Results", "Adjusted")
    out = rvr.compare(["p:1"], [adjusted], "2026-06-30", _fact(net_income=1e8))
    assert [c["block"] for c in out["net_income"]["comparisons"]] == ["gaap", "not_gaap"]


@pytest.mark.parametrize("text,hint", [
    ("Non-GAAP", "not_gaap"), ("Non- GAAP Results", "not_gaap"), ("Adjusted", "not_gaap"),
    ("Adjusted Results", "not_gaap"), ("GAAP", "gaap"), ("GAAP Results (unaudited)", "gaap"),
    ("GAAP and non-GAAP", "unidentified"), ("(As Adjusted)", None),
    ("June 30, 2026 (As Adjusted)", None), ("As Adjusted Basis", None),
    ("excluding special items", None), ("Pro forma", None), ("Quarter Ended", None)])
def test_release_versus_report_a_header_hint_comes_from_the_header_and_not_from_prose(text, hint):
    assert rvr.header_hint(text) == hint


def test_release_versus_report_a_column_headed_as_adjusted_in_brackets_is_compared_as_gaap():
    """Apple's `(As Adjusted)` plant: the column is the statement's, and a changed figure
    in it reads `differs`."""
    table = "\n".join(["|  | Three Months Ended |", "|  | June 30, 2026 (As Adjusted) |  | June 30, 2025 |",
                       "| (in millions) |", _row("Net income", "110")])
    out = rvr.compare(["p:1"], [table], "2026-06-30", _fact(net_income=1e8))
    assert out["net_income"]["comparisons"][0]["block"] == "gaap"
    assert out["net_income"]["verdict"] == "differs"


@pytest.mark.parametrize("heading", ["Net sales by segment", "Net sales by reportable segment:",
                                     "Operating expenses (including share-based compensation)",
                                     "Summary of Stock-Based Compensation Expense:"])
def test_release_versus_report_a_total_row_under_a_component_heading_is_compared(heading):
    """The refuter's Apple plants: `Total net sales` under a segment or component heading
    is the line's own total, labelled `gaap`, compared, and a changed one reads `differs`."""
    rows = [f"| {heading} |", _row("Total net sales", "109,517")]
    out = _run(rows, _fact(revenue=109_417e6))
    assert out["revenue"]["comparisons"][0]["block"] == "gaap"
    assert out["revenue"]["verdict"] == "differs"
    assert out["revenue"]["comparisons"][0]["difference"] == 100_000_000.0


def test_release_versus_report_a_part_row_under_a_component_heading_is_labelled_and_compared():
    """Arista's `Cost of revenue | 7.4` under `Summary of Stock-Based Compensation
    Expense:` is a component: compared, labelled `component`, and a difference there is
    `differs_outside_gaap`."""
    rows = ["| Summary of Stock-Based Compensation Expense: |", _row("Cost of revenue", "7.4")]
    out = _run(rows, _fact(cost_of_revenue=1_125.4e6))
    assert out["cost_of_revenue"]["comparisons"][0]["block"] == "component"
    assert out["cost_of_revenue"]["verdict"] == "differs_outside_gaap"


@pytest.mark.parametrize("heading", ["Weighted average shares:", "Percentage of Total Net Revenue:"])
def test_release_versus_report_shares_and_percent_headings_do_not_take_a_dollar_row_out(heading):
    rows = [f"| {heading} |", _row("Net income", "110")]
    out = _run(rows, _fact(net_income=1e8))
    assert out["net_income"]["verdict"] == "differs"
    assert "excluded_rows" not in out["net_income"]


@pytest.mark.parametrize("heading", ["Basic:", "Diluted:", "Earnings per share:",
                                     "Net income per share"])
def test_release_versus_report_only_per_share_rows_and_percent_cells_are_not_dollars(heading):
    rows = [_row("Net income", "100"), f"| {heading} |", _row("Net income", "0.61"),
            "| Operating expenses: |", _row("Net earnings", "100")]
    out = _run(rows, _fact(net_income=1e8))
    assert [c["release"]["cell"] for c in out["net_income"]["comparisons"]] == ["100", "100"]
    assert out["net_income"]["verdict"] == "agrees"
    assert [e["cell"] for e in out["net_income"]["excluded_rows"]] == ["0.61"]
    pct = _blocks(["| Net income | $ | 8.8% |  | $ | 3.9% |", "| Net income | 8.8 | % |  | 3.9 | % |",
                   _row("Net income", "100")])
    out = rvr.compare(["p:1"], [pct], "2026-06-30", _fact(net_income=1e8))
    assert [c["release"]["cell"] for c in out["net_income"]["comparisons"]] == ["100"]
    assert [e["cell"] for e in out["net_income"]["excluded_rows"]] == ["8.8%", "8.8"]
    # a percent row with more figures than the header has columns is a percent row, not an
    # unread table
    wide = _blocks(["| Net income | 8.8 | % |  | 3.9 | % |  | 1.2 | % |", _row("Net income", "100")])
    out = rvr.compare(["p:1"], [wide], "2026-06-30", _fact(net_income=1e8))
    assert out["net_income"]["verdict"] == "agrees" and "unread" not in out["net_income"]
    assert [e["cell"] for e in out["net_income"]["excluded_rows"]] == ["8.8"]


def test_release_versus_report_a_segment_is_only_what_the_instance_names_as_a_segment():
    labels = [rvr.segment_label("carr:ClimateSolutionsAmericasSegmentMember"),
              rvr.segment_label("carr:ClimateSolutionsCSAMESegmentMember"),
              rvr.segment_label("carr:ClimateSolutionsAsiaPacificMiddleEastAndAfricaMember")]
    assert labels == ["climate solutions americas", "climate solutions csame",
                      "climate solutions asia pacific middle east and africa"]
    assert rvr.names_a_segment("Climate Solutions Americas (CSA)", labels)
    assert rvr.names_a_segment("Climate Solutions Asia Pacific, Middle East & Africa (CSAME)",
                               labels)
    for company in ("Apple Inc", "NVIDIA CORPORATION", "Total Company", None, "",
                    "Total Climate Solutions Americas results", "Climate Solutions"):
        assert not rvr.names_a_segment(company, labels), company
    assert not rvr.names_a_segment("Climate Solutions Americas (CSA)", [])

    first = _table([_row("Net sales", "1,000")])
    seg = _table([_row("Net sales", "400")])
    fact = lambda line, months: {"value": 1_000_000_000.0}      # noqa: E731
    out = rvr.compare(["p:1", "p:0", "p:2"], [first, "Climate Solutions Americas (CSA)", seg],
                      "2026-06-30", fact, segment_labels=labels)
    assert [(c["release"]["cell"], c["block"]) for c in out["revenue"]["comparisons"]] == [
        ("1,000", "gaap"), ("400", "segment")]
    assert out["revenue"]["verdict"] == "differs_outside_gaap"
    assert out["revenue"]["differs_outside_gaap"][0]["hint"] == "segment"
    # a company's name above the table, or a segment the instance does not carry, is no segment
    for heading in ("Apple Inc", "NVIDIA CORPORATION", "Climate Solutions Americas (CSA)"):
        out = rvr.compare(["p:1", "p:0", "p:2"], [first, heading, seg], "2026-06-30", fact,
                          segment_labels=["something else"])
        assert out["revenue"]["verdict"] == "differs", heading
    # a column header that names a segment labels the table's cells as that segment's
    header = _table([_row("Net sales", "400")], header=("Three Months Ended", "June 30, 2026",
                                                         "(in millions)"))
    header = header.replace("|  | Three Months Ended |", "|  | Climate Solutions Americas |\n|  | Three Months Ended |", 1)
    out = rvr.compare(["p:1"], [header], "2026-06-30", fact, segment_labels=labels)
    assert out["revenue"]["comparisons"][0]["block"] == "segment"


def test_release_versus_report_a_heading_naming_both_is_unidentified_and_never_agrees():
    rows = ["| Reconciliation of GAAP and non-GAAP net income |", _row("Net income", "100")]
    out = _run(rows, _fact(net_income=1e8))
    assert out["net_income"]["comparisons"][0]["block"] == "unidentified"
    assert out["net_income"]["verdict"] == "block_not_identified"
    out = _run(["| Reconciliation of GAAP and non-GAAP net income |", _row("Net income", "101")],
               _fact(net_income=1e8))
    assert out["net_income"]["verdict"] == "differs_outside_gaap"
    # a label that says GAAP is GAAP wherever it sits
    out = _run(["| Non-GAAP |", _row("GAAP net income", "100")], _fact(net_income=1e8))
    assert out["net_income"]["comparisons"][0]["block"] == "gaap"
    assert out["net_income"]["verdict"] == "agrees"


def test_release_versus_report_repeated_columns_nothing_names_are_unidentified_not_dropped():
    unnamed = "\n".join(["|  | Quarter Ended |  | Quarter Ended |", "|  | June 30, |  | June 30, |",
                         "|  | 2026 |  | 2026 |", "| (in millions) |",
                         "| Net income | $ | 100 |  | $ | 130 |"])
    out = rvr.compare(["p:1"], [unnamed], "2026-06-30", _fact(net_income=1e8))
    assert [(c["release"]["cell"], c["block"]) for c in out["net_income"]["comparisons"]] == [
        ("100", "unidentified"), ("130", "unidentified")]
    assert out["net_income"]["verdict"] == "differs_outside_gaap"


# --- the face statement, beside the line verdict and never borrowed by it -------------------

def _statement_table(values: dict[str, str]) -> str:
    return _table([_row(label, cell) for label, cell in values.items()])


FOUR = {"Net revenue": "1,000", "Cost of revenue": "600", "Operating income": "300",
        "Net income": "200"}


def test_release_versus_report_the_statement_is_the_table_with_four_lines_chosen_without_values():
    fact = _fact(revenue=1e9, cost_of_revenue=6e8, operating_income=3e8, net_income=2e8)
    three = _table([_row("Net revenue", "1,000"), _row("Net income", "200"),
                    _row("Operating income", "300")])
    four = _statement_table(FOUR)
    out = rvr.compare_release(["p:1", "p:2"], [three, four], "2026-06-30", fact)
    assert out["statement"] == "p:2"
    assert {line: out["lines"][line]["statement"] for line in FOUR_LINES} == {
        line: {"paragraph_id": "p:2", "verdict": "agrees"} for line in FOUR_LINES}
    # the same labels with other figures choose the same table: values play no part
    other = _statement_table({k: "7" for k in FOUR})
    assert rvr.compare_release(["p:1", "p:2"], [three, other], "2026-06-30", fact)["statement"] == "p:2"
    # the table printing the most lines wins, and a tie goes to the first
    five = _statement_table(dict(FOUR, **{"Income tax expense": "50"}))
    assert rvr.compare_release(["p:1", "p:2"], [four, five], "2026-06-30", fact)["statement"] == "p:2"
    assert rvr.compare_release(["p:1", "p:2"], [four, four], "2026-06-30", fact)["statement"] == "p:1"


FOUR_LINES = ("revenue", "cost_of_revenue", "operating_income", "net_income")


def test_release_versus_report_the_statement_verdict_is_its_own_and_the_line_never_borrows_it():
    fact = _fact(revenue=1e9, cost_of_revenue=6e8, operating_income=3e8, net_income=2e8)
    bad = _statement_table(dict(FOUR, **{"Net income": "250"}))
    good_elsewhere = _table([_row("Net income", "200")])
    out = rvr.compare_release(["p:1", "p:2"], [bad, good_elsewhere], "2026-06-30", fact)["lines"]
    assert out["net_income"]["statement"] == {"paragraph_id": "p:1", "verdict": "differs"}
    assert out["revenue"]["statement"]["verdict"] == "agrees"
    assert out["net_income"]["verdict"] == "differs"
    # a line the statement does not print is not_compared there, and says so
    out = rvr.compare_release(["p:1", "p:2"], [_statement_table(FOUR), _table([
        _row("Income tax expense", "50")])], "2026-06-30",
        _fact(income_tax_expense=5e7, revenue=1e9, cost_of_revenue=6e8, operating_income=3e8,
              net_income=2e8))["lines"]
    assert out["income_tax_expense"]["statement"] == {"paragraph_id": "p:1",
                                                      "verdict": "not_compared"}
    assert out["income_tax_expense"]["verdict"] in ("agrees", "differs")
    # no table with four lines: nothing is the statement
    out = rvr.compare_release(["p:1"], [_table([_row("Net revenue", "1,000")])], "2026-06-30",
                              fact)
    assert out["statement"] is None
    assert out["lines"]["revenue"]["statement"] == {"paragraph_id": None,
                                                    "verdict": "not_compared"}


def test_release_versus_report_unread_tables_are_grouped_by_kind_and_unread_columns_dated():
    guidance = "\n".join(["|  | FY27 Previous |  | FY27 Updated |", "| Revenue | $ | 167.0 |  | $ | 192.0 |"])
    undated = "\n".join(["|  | Q2 FY27 |  | Q1 FY27 |", "| (in millions) |", "| Revenue | 5 | 6 |"])
    non_gaap = "\n".join(["|  | Non-GAAP |", "|  | Q2 FY27 |  | Q1 FY27 |", "| (in millions) |",
                          "| Revenue | 5 | 6 |"])
    segment = "\n".join(["|  | Residential |  | Commercial |", "| (in thousands) |",
                         "| Net sales | 617 | 556 | 1,173 |"])
    out = rvr.compare_release(["p:1", "p:2", "p:3", "p:4"], [guidance, undated, non_gaap, segment],
                              "2026-06-30", _fact(revenue=1.0), segment_labels=["residential", "commercial"])
    kinds = {kind: [item["paragraph_id"] for item in items]
             for kind, items in out["unread_tables"].items()}
    assert kinds == {"guidance": ["p:1"], "undated": ["p:2"], "non_gaap": ["p:3"],
                     "segment_column": ["p:4"]}
    assert out["lines"]["revenue"]["verdict"] == "period_not_read"
    # a column neither the period nor the year before it is listed with its date
    table = "\n".join(["|  | Three Months Ended |", "|  | May 1, 2026 |  | June 30, 2026 |  | June 30, 2025 |",
                       "| (in millions) |", "| Net income | $ | 90 |  | $ | 100 |  | $ | 80 |"])
    out = rvr.compare_release(["p:1"], [table], "2026-06-30", _fact(net_income=1e8))
    assert out["unread_columns"] == [{"paragraph_id": "p:1", "date": "2026-05-01",
                                      "span_months": 3,
                                      "reason": "a column that is neither the period nor the "
                                                "year before it"}]
    assert out["lines"]["net_income"]["verdict"] == "agrees"
    assert [c["release"]["cell"] for c in out["lines"]["net_income"]["comparisons"]] == ["100"]


# --- net income: the table's own attributable row decides what an unlabelled one is ------------

def test_release_versus_report_net_income_unlabelled_beside_an_attributable_row_is_profit_or_loss():
    report = lambda line, months: {"value": {"net_income": 501e6,   # noqa: E731
                                             "net_income_with_noncontrolling": 541e6}[line]}
    rows = [_row("Net earnings (loss)", "541"),
            _row("Net earnings (loss) attributable to common shareowners", "501")]
    out = _run(rows, report)
    cells = out["net_income"]["comparisons"]
    assert [c["verdict"] for c in cells] == ["agrees", "agrees"]
    assert cells[0]["report"]["value"] == 541e6 and cells[1]["report"]["value"] == 501e6
    # the refuter's plant: the unlabelled row changed to the parent's figure reads `differs`
    rows[0] = _row("Net earnings (loss)", "501")
    out = _run(rows, report)
    assert out["net_income"]["verdict"] == "differs"
    assert out["net_income"]["comparisons"][0]["difference"] == -40_000_000.0


def test_release_versus_report_net_income_with_no_attributable_row_is_held_to_net_income_loss():
    report = lambda line, months: {"value": {"net_income": 501e6,   # noqa: E731
                                             "net_income_with_noncontrolling": 541e6}[line]}
    out = _run([_row("Net earnings (loss)", "541")], report)
    cell = out["net_income"]["comparisons"][0]
    assert cell["verdict"] == "differs" and cell["difference"] == 40_000_000.0
    assert cell["also_against"]["agrees"] is True
    assert cell["also_against"]["net_income_with_noncontrolling"]["value"] == 541e6
    out = _run([_row("Net earnings (loss)", "501")], report)
    assert out["net_income"]["verdict"] == "agrees"
    assert "also_against" in out["net_income"]["comparisons"][0]     # the two differ
    same = lambda line, months: {"value": 501e6}      # noqa: E731
    assert "also_against" not in _run([_row("Net earnings (loss)", "501")], same)["net_income"]["comparisons"][0]


def test_release_versus_report_planted_net_income_rows_beside_an_attributable_row_differ():
    lines = _planted("CARR", "0001783180-26-000032", {
        "84": ("| Net earnings (loss) |  | 541 |", "| Net earnings (loss) |  | 501 |")})
    assert lines["net_income"]["verdict"] == "differs"
    lines = _planted("JCI", "0000833444-26-000087", {
        "72": ("| Net income | 752 |", "| Net income | 749 |")})
    assert lines["net_income"]["verdict"] == "differs"
    lines = _planted("GNRC", "0001437749-26-025669", {
        "103": ("| Net income | ​ | ​ | 143,010 |", "| Net income | ​ | ​ | 143,244 |")})
    assert lines["net_income"]["verdict"] == "differs"


def test_release_versus_report_unplanted_net_income_rows_beside_an_attributable_row_agree():
    for ticker, accession, paragraph in (("CARR", "0001783180-26-000032", "84"),
                                         ("JCI", "0000833444-26-000087", "72"),
                                         ("GNRC", "0001437749-26-025669", "103")):
        lines = _planted(ticker, accession, {})
        cells = [c for c in _in_table(lines["net_income"], paragraph) if c["span_months"] == 3]
        assert cells and {c["verdict"] for c in cells} == {"agrees"}, ticker


# --- the bulk check: raise every number under a line label, one at a time --------------------

def _raised(text: str) -> str:
    """The printed figure one step higher at its own precision, keeping its commas, its
    parentheses and its dollar sign: 4,133 is 4,134 and (1,239) is (1,240) and 6.34 is 6.35."""
    from decimal import Decimal
    figure = rvr.read_number(text)
    value, decimals = figure
    bumped = value + (Decimal(1).scaleb(-decimals) if value >= 0 else -Decimal(1).scaleb(-decimals))
    body = f"{abs(bumped):,.{decimals}f}"
    shown = f"({body})" if text.lstrip("$ ").startswith("(") else body
    shown = f"-{body}" if bumped < 0 and not text.lstrip("$ ").startswith("(") else shown
    return ("$" if text.startswith("$") else "") + shown


def bulk_check(ticker: str, accession: str) -> dict:
    """Every figure in every row of the committed release whose label is one of the lines'
    is raised by one step, one at a time, and the release read again against the real
    record. Returns `flipped` (compared cells that read `differs` once raised), `not_compared`
    (figures that are not a compared cell, with why) and `stayed` (compared cells that did
    not flip: there should be none)."""
    from src import parse_8k
    run, cutoff, record, periods = _run_inputs(ticker, accession)
    release = parse_8k.earnings_release(ticker, cutoff=cutoff)
    item = release["item_2_02"]
    reader = calculator.release_report_reader(record, periods)
    labels = rvr.segment_label
    members = calculator.segment_members(calculator.instance_facts(run, cutoff))
    del labels

    def read(paragraphs):
        return rvr.compare_release(item["paragraph_ids"], paragraphs, periods["balance_now"],
                                   reader, members)

    base = read(item["paragraphs"])
    compared = {(c["release"]["paragraph_id"], c["release"]["label"], c["release"]["cell"])
                for entry in base["lines"].values() for c in entry.get("comparisons", [])}
    result = {"flipped": [], "not_compared": [], "stayed": []}
    for index, (pid, paragraph) in enumerate(zip(item["paragraph_ids"], item["paragraphs"])):
        rows = paragraph.split("\n")
        if not all(row.startswith("| ") and row.endswith(" |") for row in rows):
            continue
        for r, row in enumerate(rows):
            cells = rvr.cells_of(row)
            placed = rvr._label_of(cells)
            if not placed or rvr.normal_label(placed[1]) not in rvr.LINE_OF_LABEL:
                continue
            for j in range(placed[0] + 1, len(cells)):
                if rvr.read_number(cells[j]) is None or rvr._is_year(cells[j]):
                    continue
                text = cells[j].strip()
                key = {"paragraph_id": pid, "label": placed[1], "cell": text, "row": r, "col": j}
                if (pid, placed[1], text) not in compared:
                    result["not_compared"].append(key)
                    continue
                changed = list(cells)
                changed[j] = _raised(text)
                rows2 = list(rows)
                rows2[r] = "| " + " | ".join(changed) + " |"
                paragraphs = list(item["paragraphs"])
                paragraphs[index] = "\n".join(rows2)
                after = read(paragraphs)
                line = rvr.LINE_OF_LABEL[rvr.normal_label(placed[1])]
                hit = [c for c in after["lines"][line].get("comparisons", [])
                       if c["release"]["paragraph_id"] == pid and c["release"]["label"] == placed[1]
                       and c["release"]["cell"] == changed[j].strip()]
                if hit and all(c["verdict"] == "differs" for c in hit) and \
                        after["lines"][line]["verdict"] in ("differs", "differs_outside_gaap"):
                    result["flipped"].append(key)
                else:
                    result["stayed"].append(dict(key, verdicts=[c["verdict"] for c in hit]))
    return result


def test_release_versus_report_raised_figures_are_written_one_step_higher():
    assert _raised("4,133") == "4,134" and _raised("(1,239)") == "(1,240)"
    assert _raised("6.34") == "6.35" and _raised("$1,570.7") == "$1,570.8"
    assert _raised("(12)") == "(13)" and _raised("999") == "1,000"


def test_release_versus_report_every_compared_figure_of_dells_release_flips_when_raised():
    """Dell's tables print the quarter and the six months of their lines; each compared figure,
    raised one at a time, reads `differs`, and none stays `agrees`. The count is written by
    hand, table by table, from the committed release (each line twice, the quarter and the six
    months): `:35` the summary, five lines, 10; `:63` the statement, revenue, cost of revenue,
    operating income, pretax income, tax and net income, 12; `:74` cash flows, net income and
    operating cash flow, 4; `:98` net revenue, 2; `:103` the reconciliation, operating income and
    net income, 4; `:110` diluted earnings per share, 2. That is 34."""
    by_hand = {"35": 10, "63": 12, "74": 4, "98": 2, "103": 4, "110": 2}
    assert sum(by_hand.values()) == 34
    outcome = bulk_check("DELL", "0001571996-26-000046")
    assert outcome["stayed"] == []
    counted: dict[str, int] = {}
    for cell in outcome["flipped"]:
        number = cell["paragraph_id"].split(":")[-1]
        counted[number] = counted.get(number, 0) + 1
    assert counted == by_hand


# --- dates that are not dates, signs, the span guard, the labels the specification names ----------

def test_release_versus_report_a_header_date_that_is_not_a_date_makes_the_table_unread():
    """February 29 in a year without one is the table's `period_not_read`, with its reason,
    never an exception, in a header that names its columns by month and year and in one
    that carries the whole column in a cell."""
    split = "\n".join(["|  | Three Months Ended |", "|  | February 29, 2026 |  | February 28, 2025 |",
                       "| (in millions) |", _row("Net income", "100")])
    whole = "\n".join(["|  | Three Months Ended February 29, 2026 |  | Three Months Ended February 28, 2025 |",
                       "| (in millions) |", "| Net income | $ | 100 |  | 90 |"])
    paired = "\n".join(["|  | Three Months Ended February 29, |", "| (in millions) | 2026 | 2025 |",
                        "| Net income | $ | 100 |  | $ | 90 |"])
    for table in (split, whole, paired):
        out = rvr.compare(["p:1"], [table], "2026-02-28", _fact(net_income=1e8))
        assert out["net_income"]["verdict"] == "period_not_read", table
        assert "not a date" in out["net_income"]["unread"][0]["reason"]
    with pytest.raises(rvr.Unread, match="not a date"):
        rvr.read_header([rvr.cells_of(line) for line in split.split("\n")])
    ok = split.replace("29, 2026", "28, 2026")
    assert rvr.compare(["p:1"], [ok], "2026-02-28", _fact(net_income=1e8)
                       )["net_income"]["verdict"] == "agrees"


def test_release_versus_report_a_cost_in_parentheses_is_compared_by_its_size():
    for printed, report, verdict in (("(4,081)", 4_081e6, "agrees"), ("4,081", 4_081e6, "agrees"),
                                     ("(4,081)", 4_090e6, "differs")):
        out = _run([_row("Cost of sales", printed)], _fact(cost_of_revenue=report))
        assert out["cost_of_revenue"]["comparisons"][0]["verdict"] == verdict, printed
    out = _run([_row("Cost of sales", "(4,081)")], _fact(cost_of_revenue=4_090e6))
    assert out["cost_of_revenue"]["comparisons"][0]["difference"] == -9_000_000.0


def test_release_versus_report_income_tax_is_by_size_unless_its_label_says_benefit():
    for label, printed, report, verdict in (
            ("Provision for income taxes", "(180)", 180e6, "agrees"),      # Carrier's style
            ("Provision for income taxes", "180", 180e6, "agrees"),
            ("Income tax provision", "(180)", 181e6, "differs"),
            ("Income tax (benefit) expense", "(12)", -12e6, "agrees"),      # a benefit, signed
            ("Income tax (benefit) expense", "(12)", 12e6, "differs"),       # not by size
            ("Income tax (benefit) expense", "12", 12e6, "agrees")):
        out = _run([_row(label, printed)], _fact(income_tax_expense=report))
        assert out["income_tax_expense"]["comparisons"][0]["verdict"] == verdict, (label, printed)
    out = _run([_row("Income tax (benefit) expense", "(12)")], _fact(income_tax_expense=12e6))
    assert out["income_tax_expense"]["comparisons"][0]["difference"] == -24_000_000.0


def test_release_versus_report_the_span_length_guard_never_compares_a_twelve_month_column_to_a_nine_month_year_to_date():
    """JCI's release prints a trailing-twelve-month column against a 10-Q whose year to
    date is nine months (273 days): the report side is missing, with the reason, and the
    cell reads `report_fact_missing`, never a comparison."""
    class Stub:
        usd = {}

        def term(self, term, span):
            return {"value": 7.0, "id": f"stub:{term}:{span}", "tag": "Stub", "period": str(span)}

    periods = {"balance_now": "2026-06-30", "annual_trigger": False,
               "current_to_date": ("2025-10-01", "2026-06-30"), "quarter": None}
    read = calculator.release_report_reader(Stub(), periods)
    found = read("pretax_income", 12)
    assert "missing" in found and "12 months" in found["missing"] and "273 days" in found["missing"]
    assert read("pretax_income", 9)["value"] == 7.0
    assert "missing" in read("pretax_income", 6) and "missing" in read("pretax_income", 3)
    annual = dict(periods, annual_trigger=True, current_to_date=("2025-07-01", "2026-06-30"))
    assert calculator.release_report_reader(Stub(), annual)("pretax_income", 12)["value"] == 7.0
    assert "missing" in calculator.release_report_reader(Stub(), annual)("pretax_income", 9)
    # through the comparison: a twelve-month column against the nine-month report
    table = "\n".join(["|  | Last Twelve Months Ended |", "|  | June 30, 2026 |  | June 30, 2025 |",
                       "| (in millions) |", _row("Net income", "2,718")])
    table = table.replace("Last Twelve Months Ended", "Twelve Months Ended")
    out = rvr.compare(["p:1"], [table], "2026-06-30", read)
    assert [c["verdict"] for c in out["net_income"]["comparisons"]] == ["report_fact_missing"]


def test_release_versus_report_the_specification_names_these_labels_for_revenue():
    """The five the specification gives as examples are in the module's own table."""
    for label in ("Net revenue", "Total net revenue", "Net sales", "Revenue", "Total revenue"):
        assert rvr.LINE_OF_LABEL[rvr.normal_label(label)] == "revenue", label
    assert rvr.LINE_OF_LABEL[rvr.normal_label("Total net sales (1)")] == "revenue"
    assert "Net revenue" in rvr.ROW_LABELS["revenue"]


def test_release_versus_report_a_column_dated_a_quarter_early_in_dells_release_is_noted():
    """Dell's statement with its three-month column dated `May 1, 2026` instead of July 31:
    the column is listed with its date, the six-month cell of the same table still votes,
    and the other tables' three-month cells still vote."""
    full = _planted_full("DELL", "0001571996-26-000046", {
        "63": ("|  | July 31, 2026 |", "|  | May 1, 2026 |")})
    notes = [n for n in full["unread_columns"] if n["paragraph_id"].endswith(":8k_2_02:63")]
    assert [(n["date"], n["span_months"]) for n in notes] == [("2026-05-01", 3)]
    income = full["lines"]["net_income"]
    six = [c for c in _in_table(income, "63") if c["span_months"] == 6]
    assert [c["verdict"] for c in six] == ["agrees"]
    assert [c["span_months"] for c in _in_table(income, "63")] == [6]
    assert [c["verdict"] for c in _in_table(income, "35") if c["span_months"] == 3] == ["agrees"]


# --- the 13 releases' face statements, read by eye ----------------------------------------------

# ticker -> (accession, the statement's paragraph, the lines it does not print under a label)
# Each paragraph was opened and read: the income statement of the quarter, with its dated
# columns for the period. Johnson Controls' prints its net sales on a row with no label and
# labels only three of the nine lines, so it has no statement and nothing is compared.
STATEMENTS = {
    "AAPL": ("0000320193-26-000020", "29", {"capital_expenditure", "operating_cash_flow"}),
    "ANET": ("0001596532-26-000175", "34", {"capital_expenditure", "operating_cash_flow"}),
    "CARR": ("0001783180-26-000032", "84", {"capital_expenditure", "cost_of_revenue", "diluted_earnings_per_share", "operating_cash_flow"}),
    "CIEN": ("0001628280-26-040767", "55", {"capital_expenditure", "operating_cash_flow"}),
    "DELL": ("0001571996-26-000046", "63", {"capital_expenditure", "operating_cash_flow"}),
    "ESE": ("0001104659-26-093266", "53", {"capital_expenditure", "diluted_earnings_per_share", "operating_cash_flow", "operating_income"}),
    "FTNT": ("0001262039-26-000021", "68", {"capital_expenditure", "operating_cash_flow", "pretax_income"}),
    "GNRC": ("0001437749-26-025669", "103", {"capital_expenditure", "diluted_earnings_per_share", "operating_cash_flow"}),
    "JCI": ("0000833444-26-000087", None, set(rvr.LINES)),
    "LFUS": ("0001628280-26-050481", "53", {"capital_expenditure", "operating_cash_flow"}),
    "NVDA": ("0001045810-26-000075", "69", {"capital_expenditure", "operating_cash_flow"}),
    "QCOM": ("0000804328-26-000086", "54", {"capital_expenditure", "operating_cash_flow"}),
    "STX": ("0001137789-26-000159", "59", {"capital_expenditure", "operating_cash_flow"}),
}


@pytest.mark.parametrize("ticker", sorted(STATEMENTS))
def test_release_versus_report_each_releases_face_statement_is_the_paragraph_read_by_eye(ticker):
    accession, number, not_compared = STATEMENTS[ticker]
    full = _planted_full(ticker, accession, {})
    if number is None:
        assert full["statement_table"] is None
    else:
        assert full["statement_table"].endswith(f":8k_2_02:{number}")
    verdicts = {line: entry["statement"]["verdict"] for line, entry in full["lines"].items()}
    assert {line for line, verdict in verdicts.items() if verdict == "not_compared"} == not_compared
    assert {verdict for verdict in verdicts.values()} <= {"agrees", "not_compared"}


def test_release_versus_report_johnson_controls_revenue_is_not_compared_on_its_statement():
    full = _planted_full("JCI", "0000833444-26-000087", {})
    assert full["lines"]["revenue"]["statement"] == {"paragraph_id": None, "verdict": "not_compared"}


def test_release_versus_report_a_planted_figure_in_the_statement_reads_differs_there_and_in_the_line():
    for ticker, (accession, number, _) in STATEMENTS.items():
        if number is None:
            continue
        run, cutoff, record, periods = _run_inputs(ticker, accession)
        full = _planted_full(ticker, accession, {})
        mine = [c for c in full["lines"]["net_income"]["comparisons"]
                if c["release"]["paragraph_id"].endswith(f":8k_2_02:{number}")
                and c["span_months"] == 3 and c["verdict"] == "agrees"]
        if not mine:
            continue
        old = mine[0]["release"]["cell"]
        label = mine[0]["release"]["label"]
        row = next(r for r in _paragraph(ticker, cutoff, number).split("\n")
                   if rvr.cells_of(r) and any(c.strip() == label for c in rvr.cells_of(r))
                   and old in [c.strip() for c in rvr.cells_of(r)])
        cells = rvr.cells_of(row)
        position = next(i for i, c in enumerate(cells) if c.strip() == old)
        changed = list(cells)
        changed[position] = _raised(old)
        planted = _planted_full(ticker, accession, {number: (row, "| " + " | ".join(changed) + " |")})
        assert planted["lines"]["net_income"]["statement"]["verdict"] == "differs", ticker
        assert planted["lines"]["net_income"]["verdict"] in ("differs", "differs_outside_gaap"), ticker


def _paragraph(ticker: str, cutoff, number: str) -> str:
    from src import parse_8k
    item = parse_8k.earnings_release(ticker, cutoff=cutoff)["item_2_02"]
    return item["paragraphs"][next(i for i, pid in enumerate(item["paragraph_ids"])
                                   if pid.endswith(f":8k_2_02:{number}"))]


def test_release_versus_report_a_gaap_label_in_a_column_headed_non_gaap_is_not_identified():
    """`GAAP net income` printed under the column its own header calls non-GAAP is a
    contradiction: the cell is labelled `unidentified`, still compared, and the cell in the
    GAAP column keeps `gaap`."""
    table = "\n".join(["|  | GAAP Results |  | Non-GAAP Results |",
                       "|  | Quarter Ended |  | Quarter Ended |", "|  | June 30, |  | June 30, |",
                       "|  | 2026 |  | 2026 |", "| (in millions) |",
                       "| GAAP net income | $ | 100 |  | $ | 130 |"])
    out = rvr.compare(["p:1"], [table], "2026-06-30", _fact(net_income=1e8))
    assert [(c["release"]["cell"], c["block"]) for c in out["net_income"]["comparisons"]] == [
        ("100", "gaap"), ("130", "unidentified")]
    assert out["net_income"]["verdict"] == "differs_outside_gaap"


# --- a statement of cash flows starts from net income before the noncontrolling interest -------

def test_release_versus_report_a_cash_flow_statements_net_income_is_held_to_profit_or_loss():
    """A table that prints an operating cash flow line is a statement of cash flows, whose net
    income is consolidated by construction: held to `ProfitLoss`, with `NetIncomeLoss`
    beside it where the two differ. A table with no such line keeps the earlier rule."""
    report = lambda line, months: {"value": {"net_income": 501e6,   # noqa: E731
                                             "net_income_with_noncontrolling": 541e6,
                                             "operating_cash_flow": 700e6}[line]}
    cash_flow = [_row("Net earnings (loss)", "541"),
                 _row("Net cash provided by operating activities", "700"),
                 _row("Net cash used in investing activities", "(200)"),
                 _row("Net cash used in financing activities", "(300)"),
                 _row("Cash and cash equivalents, end of period", "1,200")]
    cell = _run(cash_flow, report)["net_income"]["comparisons"][0]
    assert cell["verdict"] == "agrees" and cell["report"]["value"] == 541e6
    assert cell["also_against"]["net_income"]["value"] == 501e6
    assert cell["also_against"]["agrees"] is False
    # a cash-flow net income that is not the consolidated figure differs
    cash_flow[0] = _row("Net earnings (loss)", "501")
    cell = _run(cash_flow, report)["net_income"]["comparisons"][0]
    assert cell["verdict"] == "differs" and cell["difference"] == -40_000_000.0
    assert cell["also_against"]["agrees"] is True
    # the same row in a table with no operating cash flow line is held to NetIncomeLoss
    cell = _run([_row("Net earnings (loss)", "541")], report)["net_income"]["comparisons"][0]
    assert cell["verdict"] == "differs" and cell["report"]["value"] == 501e6
    # with no ProfitLoss on record there is no interest to tell apart: NetIncomeLoss
    only = lambda line, months: ({"value": {"net_income": 501e6, "operating_cash_flow": 7e8}[line]}   # noqa: E731
                                 if line in ("net_income", "operating_cash_flow")
                                 else {"missing": "no ProfitLoss"})
    assert only("net_income_with_noncontrolling", 3) == {"missing": "no ProfitLoss"}
    cash_flow[0] = _row("Net income", "501")
    cell = _run(cash_flow, only)["net_income"]["comparisons"][0]
    assert cell["verdict"] == "agrees" and cell["report"]["value"] == 501e6


def test_release_versus_report_carriers_and_generacs_cash_flow_net_income_agree():
    """Carrier's `Net earnings (loss) | 541` (`:93`) and Generac's `Net income | 216,122`
    (`:106`, six months) start the statement of cash flows, before the noncontrolling
    interest: they agree with `ProfitLoss`, and the cells say `NetIncomeLoss` differs."""
    for ticker, accession, number, cell_text in (
            ("CARR", "0001783180-26-000032", "93", "541"),
            ("GNRC", "0001437749-26-025669", "106", "216,122")):
        lines = _planted(ticker, accession, {})
        cells = _in_table(lines["net_income"], number)
        assert cells and {c["verdict"] for c in cells} == {"agrees"}, ticker
        shown = [c for c in cells if c["release"]["cell"] == cell_text]
        report = shown[0]["report"]
        tag = report.get("tag") or report["parts"]["0"]["tag"]
        assert shown and tag == "ProfitLoss", ticker
        if ticker == "CARR":       # no attributable row in the cash-flow statement: both facts shown
            assert shown[0]["also_against"]["agrees"] is False
        assert lines["net_income"]["verdict"] == "agrees", (ticker, lines["net_income"]["verdict"])


def test_release_versus_report_a_planted_cash_flow_net_income_differs_from_profit_or_loss():
    lines = _planted("CARR", "0001783180-26-000032", {
        "93": ("| Net earnings (loss) |  | $ | 541 |", "| Net earnings (loss) |  | $ | 551 |")})
    assert lines["net_income"]["verdict"] == "differs"
    bad = [c for c in _in_table(lines["net_income"], "93") if c["verdict"] == "differs"]
    assert [(c["release"]["cell"], c["difference"]) for c in bad] == [("551", 10_000_000.0)]
    lines = _planted("GNRC", "0001437749-26-025669", {
        "106": ("| Net income | ​ | $ | 216,122 |", "| Net income | ​ | $ | 216,222 |")})
    assert lines["net_income"]["verdict"] == "differs"


# --- what a statement of cash flows is, by what it prints ------------------------------------------

def _table_rows(rows):
    return [rvr.cells_of(line) for line in _blocks(rows).split("\n")]


END = _row("Cash and cash equivalents, end of period", "1,200")


@pytest.mark.parametrize("rows,expected", [
    ([_row("Net cash provided by operating activities", "700"),
      _row("Net cash used in investing activities", "(200)"),
      _row("Net cash used in financing activities", "(300)"), END], True),
    ([_row("Net cash provided by operating activities", "700"),
      _row("Net cash used in investing activities", "(200)"), END], True),
    ([_row("Change in cash from operating activities", "2,225"),
      _row("Change in cash from investing activities", "(1,337)"),
      _row("Cash, cash equivalents, and restricted cash at beginning of the period", "11,753")], True),
    # the change in cash is not the cash at an end of the period
    ([_row("Net cash provided by operating activities", "700"),
      _row("Net cash used in investing activities", "(200)"),
      _row("Change in cash, cash equivalents, and restricted cash", "(16)")], False),
    ([_row("Net cash provided by operating activities", "700"),
      _row("Net cash used in investing activities", "(200)"),
      _row("Net cash used in financing activities", "(300)")], False),
    ([_row("Net income", "100"), _row("Net cash provided by operating activities", "700"), END], False),
    ([_row("Net cash provided by operating activities", "700"),
      _row("Purchases of property and equipment", "(88)"), END], False),
    (["| Cash flows from operating activities: |", "| Cash flows from investing activities: |",
      "| Cash flows from financing activities: |", _row("Net income", "100"), END], False),
])
def test_release_versus_report_a_statement_of_cash_flows_is_known_by_what_it_prints(rows, expected):
    assert rvr.is_a_statement_of_cash_flows(_table_rows(rows)) is expected


def test_release_versus_report_a_highlights_table_with_operating_cash_flow_is_not_a_cash_flow_statement():
    """A summary that prints net income beside operating cash flow keeps the default: its
    unlabelled net income is held to the parent's `NetIncomeLoss`, with `ProfitLoss` beside
    it. Where the two differ, the parent's figure agrees and the consolidated one does not."""
    report = lambda line, months: {"value": {"net_income": 501e6,   # noqa: E731
                                             "net_income_with_noncontrolling": 541e6,
                                             "operating_cash_flow": 700e6}[line]}
    highlights = [_row("Net income", "501"), _row("Net cash provided by operating activities", "700")]
    cell = _run(highlights, report)["net_income"]["comparisons"][0]
    assert cell["verdict"] == "agrees" and cell["report"]["value"] == 501e6
    assert cell["also_against"]["net_income_with_noncontrolling"]["value"] == 541e6
    assert cell["also_against"]["agrees"] is False
    highlights[0] = _row("Net income", "541")
    cell = _run(highlights, report)["net_income"]["comparisons"][0]
    assert cell["verdict"] == "differs" and cell["difference"] == 40_000_000.0
    # the same rows with investing and financing lines are a statement of cash flows
    statement = highlights + [_row("Net cash used in investing activities", "(200)"),
                              _row("Net cash used in financing activities", "(300)"),
                              _row("Cash and cash equivalents, end of period", "1,200")]
    cell = _run(statement, report)["net_income"]["comparisons"][0]
    assert cell["verdict"] == "agrees" and cell["report"]["value"] == 541e6


def test_release_versus_report_dells_summary_table_is_not_a_cash_flow_statement_and_its_statement_is():
    from src import parse_8k
    item = parse_8k.earnings_release("DELL", cutoff=DELL_CUTOFF)["item_2_02"]
    by_number = {pid.split(":")[-1]: [rvr.cells_of(line) for line in paragraph.split("\n")]
                 for pid, paragraph in zip(item["paragraph_ids"], item["paragraphs"])
                 if paragraph.startswith("|")}
    assert rvr.is_a_statement_of_cash_flows(by_number["74"]) is True
    assert rvr.is_a_statement_of_cash_flows(by_number["35"]) is False
    assert rvr.is_a_statement_of_cash_flows(by_number["63"]) is False


# --- the expected `agrees`, read independently of the calculator -------------------------------

def _filing_fact(ticker: str, accession: str, tag: str, start: str, end: str) -> float:
    """A fact of the triggering filing with no dimension, read from the run's committed
    `input_numbers.json` with `json` alone: the report side for the two companies whose
    companyfacts record has not yet caught up with the filing."""
    import json
    run = next(iter(sorted((REPO_ROOT / "runs" / ticker).glob(f"{accession}*"))))
    facts = json.loads((run / "input_numbers.json").read_text(encoding="utf-8"))["facts"]
    values = {fact["number"] for fact in facts
              if fact["tag"] == tag and fact["unit"] == "iso4217:USD"
              and fact["source_accession"] == accession
              and not fact["context"].get("segment") and not fact["context"].get("typed_segment")
              and fact["context"].get("start") == start and fact["context"].get("end") == end}
    assert len(values) == 1, (ticker, tag, start, end, values)
    return float(values.pop())


def _report_value(cell: dict) -> float:
    return cell["report"]["value"]


def test_release_versus_report_carriers_net_earnings_agree_with_profit_or_loss_read_independently():
    """Carrier's income statement `:84` and cash-flow statement `:93`, read by eye: `Net
    earnings (loss)` 541 (three months) and 806 (six), `... attributable to common
    shareowners` 501 and 739. The report side is the filing's own `ProfitLoss` and
    `NetIncomeLoss`, read from its committed facts with `json`."""
    accession = "0001783180-26-000032"
    profit = {3: _filing_fact("CARR", accession, "ProfitLoss", "2026-04-01", "2026-06-30"),
              6: _filing_fact("CARR", accession, "ProfitLoss", "2026-01-01", "2026-06-30")}
    parent = {3: _filing_fact("CARR", accession, "NetIncomeLoss", "2026-04-01", "2026-06-30"),
              6: _filing_fact("CARR", accession, "NetIncomeLoss", "2026-01-01", "2026-06-30")}
    assert profit == {3: 541e6, 6: 806e6} and parent == {3: 501e6, 6: 739e6}
    lines = _planted("CARR", accession, {})
    for number in ("84", "93"):
        generic = {c["span_months"]: c for c in _in_table(lines["net_income"], number)
                   if c["release"]["label"] == "Net earnings (loss)"}
        assert {m: c["release"]["cell"] for m, c in generic.items()} == {3: "541", 6: "806"}
        for months, cell in generic.items():
            assert _report_value(cell) == profit[months] == cell["release"]["value"], (number, months)
            assert cell["verdict"] == "agrees"
    attributable = {c["span_months"]: c for c in _in_table(lines["net_income"], "84")
                    if c["release"]["label"].startswith("Net earnings (loss) attributable")}
    assert {m: c["release"]["cell"] for m, c in attributable.items()} == {3: "501", 6: "739"}
    for months, cell in attributable.items():
        assert _report_value(cell) == parent[months] == cell["release"]["value"]
        assert cell["verdict"] == "agrees"


def test_release_versus_report_johnson_controls_net_income_rows_agree_read_independently():
    """JCI's statement `:72`, by eye: `Net income | 752` and `Net income attributable to
    Johnson Controls | 749` for the three months, 1,893 and 1,886 for the nine."""
    accession = "0000833444-26-000087"
    profit = {3: _filing_fact("JCI", accession, "ProfitLoss", "2026-04-01", "2026-06-30"),
              9: _filing_fact("JCI", accession, "ProfitLoss", "2025-10-01", "2026-06-30")}
    parent = {3: _filing_fact("JCI", accession, "NetIncomeLoss", "2026-04-01", "2026-06-30"),
              9: _filing_fact("JCI", accession, "NetIncomeLoss", "2025-10-01", "2026-06-30")}
    assert profit == {3: 752e6, 9: 1_893e6} and parent == {3: 749e6, 9: 1_886e6}
    lines = _planted("JCI", accession, {})
    cells = _in_table(lines["net_income"], "72")
    generic = {c["span_months"]: c for c in cells if c["release"]["label"] == "Net income"}
    attributable = {c["span_months"]: c for c in cells
                    if c["release"]["label"] == "Net income attributable to Johnson Controls"}
    assert {m: c["release"]["cell"] for m, c in generic.items()} == {3: "752", 9: "1,893"}
    assert {m: c["release"]["cell"] for m, c in attributable.items()} == {3: "749", 9: "1,886"}
    for months in (3, 9):
        assert _report_value(generic[months]) == profit[months]
        assert _report_value(attributable[months]) == parent[months]
        assert generic[months]["verdict"] == attributable[months]["verdict"] == "agrees"


def test_release_versus_report_generacs_net_income_rows_agree_read_through_companyfacts():
    """Generac's statement `:103` and cash-flow statement `:106`, by eye: `Net income`
    143,010 and 216,122, `Net income attributable to Generac Holdings Inc.` 143,244 and
    216,497 (thousands). The record is read through `tests/companyfacts_source.py`."""
    cutoff = "2026-08-04"
    profit = {3: source.one_value("GNRC", "ProfitLoss", "2026-04-01..2026-06-30", cutoff),
              6: source.one_value("GNRC", "ProfitLoss", "2026-01-01..2026-06-30", cutoff)}
    parent = {3: source.one_value("GNRC", "NetIncomeLoss", "2026-04-01..2026-06-30", cutoff),
              6: source.one_value("GNRC", "NetIncomeLoss", "2026-01-01..2026-06-30", cutoff)}
    assert profit == {3: 143_010e3, 6: 216_122e3} and parent == {3: 143_244e3, 6: 216_497e3}
    lines = _planted("GNRC", "0001437749-26-025669", {})
    statement = _in_table(lines["net_income"], "103")
    generic = {c["span_months"]: c for c in statement if c["release"]["label"] == "Net income"}
    attributable = {c["span_months"]: c for c in statement if "attributable" in c["release"]["label"]}
    assert {m: c["release"]["cell"] for m, c in generic.items()} == {3: "143,010", 6: "216,122"}
    assert {m: c["release"]["cell"] for m, c in attributable.items()} == {3: "143,244", 6: "216,497"}
    for months in (3, 6):
        assert _report_value(generic[months]) == profit[months] == generic[months]["release"]["value"]
        assert _report_value(attributable[months]) == parent[months]
    cash_flow, = _in_table(lines["net_income"], "106")
    assert cash_flow["release"]["cell"] == "216,122" and cash_flow["span_months"] == 6
    assert _report_value(cash_flow) == profit[6] and cash_flow["verdict"] == "agrees"


# ticker -> (cutoff, statement paragraph, [(line, label as printed, the cell by eye in
# millions, the record's tag, the record's period for the three months)])
STATEMENT_CELLS = {
    "DELL": ("2026-09-08", "63", "2026-05-02..2026-07-31", [
        ("revenue", "Total net revenue", "46,971", "Revenues"),
        ("cost_of_revenue", "Total cost of revenue", "37,141", "CostOfRevenue"),
        ("operating_income", "Operating income", "5,385", "OperatingIncomeLoss"),
        ("income_tax_expense", "Income tax expense", "998", "IncomeTaxExpenseBenefit"),
        ("net_income", "Net income", "4,133", "NetIncomeLoss")]),
    "NVDA": ("2026-08-26", "69", "2026-04-27..2026-07-26", [
        ("revenue", "Revenue", "96,221", "Revenues"),
        ("cost_of_revenue", "Cost of revenue", "24,079", "CostOfRevenue"),
        ("operating_income", "Operating income", "63,734", "OperatingIncomeLoss"),
        ("income_tax_expense", "Income tax expense", "11,819", "IncomeTaxExpenseBenefit"),
        ("net_income", "Net income", "59,688", "NetIncomeLoss")]),
    "AAPL": ("2026-07-31", "29", "2026-03-29..2026-06-27", [
        ("revenue", "Total net sales", "109,417", "RevenueFromContractWithCustomerExcludingAssessedTax"),
        ("cost_of_revenue", "Total cost of sales", "54,647", "CostOfGoodsAndServicesSold"),
        ("operating_income", "Operating income", "35,695", "OperatingIncomeLoss"),
        ("income_tax_expense", "Provision for income taxes", "6,478", "IncomeTaxExpenseBenefit"),
        ("net_income", "Net income", "29,789", "NetIncomeLoss")]),
}


@pytest.mark.parametrize("ticker", sorted(STATEMENT_CELLS))
def test_release_versus_report_the_face_statements_cells_equal_the_records_figures(ticker):
    """The statement table's three-month cells, read by eye in millions, against the
    record's own tagged figures through `tests/companyfacts_source.py`; the calculator's
    report side must be that same figure."""
    cutoff, number, period, rows = STATEMENT_CELLS[ticker]
    lines = _planted(ticker, STATEMENTS[ticker][0], {})
    for line, label, printed, tag in rows:
        expected = source.one_value(ticker, tag, period, cutoff)
        assert expected == float(printed.replace(",", "")) * 1_000_000, (ticker, line)
        cells = [c for c in _in_table(lines[line], number)
                 if c["span_months"] == 3 and c["release"]["label"] == label]
        assert cells and {c["release"]["cell"] for c in cells} == {printed}, (ticker, line)
        assert {_report_value(c) for c in cells} == {expected}, (ticker, line)
        assert {c["verdict"] for c in cells} == {"agrees"}
        assert lines[line]["statement"]["verdict"] == "agrees"


# --- final round: unit rows, prefixes, candidates, cash, attributable, mixed rows ---------------------

UNIT_ROW = "| (In millions, except per share amounts) |"


def test_release_versus_report_a_unit_statement_is_never_a_heading():
    """The refuter's synthetic: a unit row above the figures says `per share` and excluded
    everything under it. It opens no block and excludes nothing."""
    table = "\n".join([UNIT_ROW, "|  | Three Months Ended |",
                       "|  | June 30, 2026 |  | June 30, 2025 |",
                       _row("Net revenue", "1,500"), _row("Net income", "999")])
    out = rvr.compare(["p:1"], [table], "2026-06-30", _fact(revenue=1e9, net_income=1e8))
    assert out["net_income"]["verdict"] == "differs" and out["revenue"]["verdict"] == "differs"
    assert "excluded_rows" not in out["net_income"]
    # a unit row in the middle of the body does not switch anything either
    middle = _blocks([_row("Net income", "100"), UNIT_ROW, _row("Net revenue", "1,500")])
    out = rvr.compare(["p:1"], [middle], "2026-06-30", _fact(revenue=1e9, net_income=1e8))
    assert out["revenue"]["verdict"] == "differs"


@pytest.mark.parametrize("heading,per_share", [
    ("Basic:", True), ("Diluted earnings per share:", True), ("Earnings per share", True),
    ("Net income per share", True), ("Per share data", True), ("Diluted", True),
    ("(In millions, except per share amounts)", False), ("Operating costs per share of revenue", False),
    ("Net income attributable to common shareholders per common share - basic:", False),
    ("Total per share", False)])
def test_release_versus_report_a_per_share_heading_starts_with_the_per_share_words(heading, per_share):
    assert bool(rvr.PER_SHARE_HEADING.search(rvr.normal_label(heading))) is per_share


def test_release_versus_report_planted_carrier_adjustment_table_reads_a_difference():
    """Carrier `:111` prints Reported, Adjustments and Adjusted for each of two periods in one
    row: six figures under two dated columns. The Reported cell is the statement's (`gaap`),
    Adjusted is not GAAP, Adjustments are not dollars of the line. Operating profit 825 to 925
    and earnings before income taxes 721 to 821 each read `differs`."""
    unplanted = _planted("CARR", "0001783180-26-000032", {})
    reported = [c for c in _in_table(unplanted["operating_income"], "111") if c["span_months"] == 3]
    assert [(c["release"]["cell"], c["block"], c["verdict"]) for c in reported] == [
        ("825", "gaap", "agrees"), ("1,095", "not_gaap", "differs")]
    lines = _planted("CARR", "0001783180-26-000032", {
        "111": ("| Operating profit | $ | 825 |", "| Operating profit | $ | 925 |")})
    assert lines["operating_income"]["verdict"] == "differs"
    lines = _planted("CARR", "0001783180-26-000032", {
        "111": ("| Earnings before income taxes | $ | 721 |",
                "| Earnings before income taxes | $ | 821 |")})
    assert lines["pretax_income"]["verdict"] == "differs"
    bad = [c for c in _in_table(lines["pretax_income"], "111") if c["verdict"] == "differs"
           and c["block"] == "gaap"]
    assert [(c["release"]["cell"], c["difference"]) for c in bad] == [("821", 100_000_000.0)]


def test_release_versus_report_sub_columns_are_read_only_when_the_header_prints_them_each_time():
    table = "\n".join(["|  | Three Months Ended June 30, 2026 |  | Six Months Ended June 30, 2026 |",
                       "| (In millions) | Reported | Adjustments | Adjusted | Reported | Adjustments | Adjusted |",
                       "| Operating profit | $ | 825 |  | 270 |  | $ | 1,095 |  | $ | 1,083 |  | 606 |  | $ | 1,689 |"])
    out = rvr.compare(["p:1"], [table], "2026-06-30", _fact(operating_income=825e6))
    assert [(c["span_months"], c["release"]["cell"], c["block"]) for c in
            out["operating_income"]["comparisons"]] == [
        (3, "825", "gaap"), (3, "1,095", "not_gaap"), (6, "1,083", "gaap"), (6, "1,689", "not_gaap")]
    ragged = table.replace("| Reported | Adjustments | Adjusted | Reported | Adjustments | Adjusted |",
                           "| Reported | Adjustments | Adjusted | Reported |")
    out = rvr.compare(["p:1"], [ragged], "2026-06-30", _fact(operating_income=825e6))
    assert out["operating_income"]["verdict"] == "period_not_read"


@pytest.mark.parametrize("label", ["Less: Capital expenditures", "less:  Capital expenditures",
                                   "Add: Capital expenditures", "Plus: Capital expenditures",
                                   "Minus: Capital expenditures", "Deduct: Capital expenditures"])
def test_release_versus_report_a_prefixed_label_is_the_line(label):
    out = _run([_row(label, "(117)")], _fact(capital_expenditure=117e6))
    assert out["capital_expenditure"]["verdict"] == "agrees"
    out = _run([_row(label, "(118)")], _fact(capital_expenditure=117e6))
    assert out["capital_expenditure"]["verdict"] == "differs"
    assert rvr.normal_label(label) == "capital expenditures"


def test_release_versus_report_planted_free_cash_flow_reconciliation_capital_expenditure_differs():
    """Fortinet's `Less: Purchases of property and equipment | (78.0)` (`:79`), planted to
    (88.0), against the record's payments for property and equipment; and Carrier's
    `Less: Capital expenditures | (117)`."""
    unplanted = _planted("FTNT", "0001262039-26-000021", {})
    cells = [c for c in _in_table(unplanted["capital_expenditure"], "79") if c["span_months"] == 3]
    assert [(c["release"]["cell"], c["verdict"]) for c in cells] == [("(78.0)", "agrees")]
    lines = _planted("FTNT", "0001262039-26-000021", {
        "79": ("| Less: Purchases of property and equipment | (78.0) |",
               "| Less: Purchases of property and equipment | (88.0) |")})
    assert lines["capital_expenditure"]["verdict"] == "differs"
    bad = [c for c in _in_table(lines["capital_expenditure"], "79") if c["verdict"] == "differs"]
    assert [(c["release"]["cell"], c["difference"]) for c in bad] == [("(88.0)", 10_000_000.0)]
    carrier = _planted("CARR", "0001783180-26-000032", {})
    assert carrier["capital_expenditure"]["verdict"] == "agrees"
    assert any(c["release"]["label"] == "Less: Capital expenditures" and c["verdict"] == "agrees"
               for c in carrier["capital_expenditure"]["comparisons"])


def test_release_versus_report_the_free_cash_flow_reconciliation_is_not_a_cash_flow_statement():
    from src import parse_8k
    item = parse_8k.earnings_release("FTNT", cutoff="2026-08-06")["item_2_02"]
    paragraph = item["paragraphs"][next(i for i, pid in enumerate(item["paragraph_ids"])
                                        if pid.endswith(":8k_2_02:79"))]
    assert rvr.is_a_statement_of_cash_flows([rvr.cells_of(r) for r in paragraph.split("\n")]) is False


def test_release_versus_report_a_row_printed_under_another_label_must_be_a_dollar_candidate():
    """Only a row that could be the line is listed: not a non-GAAP or adjusted measure, not a
    deferred, current or weighted part, not a share count."""
    for label in ("Non-GAAP net income", "Adjusted net income", "Deferred income taxes",
                  "Current income taxes", "Weighted-average shares used in computing diluted net income per share",
                  "Diluted shares outstanding"):
        out = _run([_row("Net revenue", "1,000"), _row(label, "812")], _fact(revenue=1e9))
        assert out["net_income"]["verdict"] == "not_in_release", label
    out = _run([_row("Net revenue", "1,000"), _row("Net income before special items", "5")],
               _fact(revenue=1e9))
    assert out["net_income"]["verdict"] == "printed_under_another_label"
    assert out["net_income"]["rows"] == [{"label": "Net income before special items",
                                          "paragraph_id": "p:1", "cell": "5", "span_months": 3}]
    # a percent is not a dollar figure either
    out = _run([_row("Net revenue", "1,000"), "| Net income margin | 8.8 | % |  | 3.9 | % |"],
               _fact(revenue=1e9))
    assert out["net_income"]["verdict"] == "not_in_release"


@pytest.mark.parametrize("printed,report,verdict", [
    ("(180)", 180e6, "agrees"),        # Carrier: the expense is printed negative
    ("(181)", 180e6, "differs"),
    ("4,136", -4_136e6, "agrees"),     # a benefit, printed positive, is a negative expense
    ("4,136", 4_136e6, "differs"),
    ("180", 180e6, "differs")])        # an expense printed positive under this label is not
def test_release_versus_report_income_tax_expense_benefit_prints_the_expense_negative(printed, report, verdict):
    out = _run([_row("Income tax (expense) benefit", printed)], _fact(income_tax_expense=report))
    assert out["income_tax_expense"]["comparisons"][0]["verdict"] == verdict


def test_release_versus_report_carriers_tax_line_is_compared_and_agrees():
    carrier = _planted("CARR", "0001783180-26-000032", {})
    tax = [c for c in _in_table(carrier["income_tax_expense"], "84") if c["span_months"] == 3]
    assert [(c["release"]["label"], c["release"]["cell"], c["verdict"]) for c in tax] == [
        ("Income tax (expense) benefit", "(180)", "agrees")]
    assert carrier["income_tax_expense"]["statement"]["verdict"] == "agrees"
    lines = _planted("CARR", "0001783180-26-000032", {
        "84": ("| Income tax (expense) benefit |  | (180) |", "| Income tax (expense) benefit |  | (190) |")})
    assert lines["income_tax_expense"]["verdict"] == "differs"


def test_release_versus_report_a_highlights_table_with_three_cash_lines_and_no_cash_balance_is_not_a_statement():
    """The refuter's: revenue, parent net income 501 and the operating, investing and financing
    lines, with no cash at the beginning or the end of the period: not a statement of cash
    flows, so net income is held to the parent's `NetIncomeLoss`, and 501 agrees."""
    report = lambda line, months: ({"value": {"net_income": 501e6, "revenue": 6e9,     # noqa: E731
                                              "net_income_with_noncontrolling": 541e6,
                                              "operating_cash_flow": 700e6}[line]})
    rows = [_row("Revenue", "6,000"), _row("Net income", "501"),
            _row("Net cash provided by operating activities", "700"),
            _row("Net cash used in investing activities", "(200)"),
            _row("Net cash used in financing activities", "(300)")]
    out = _run(rows, report)
    assert out["net_income"]["verdict"] == "agrees"
    assert out["net_income"]["comparisons"][0]["report"]["value"] == 501e6


def test_release_versus_report_any_row_attributable_to_someone_makes_the_unlabelled_row_consolidated():
    """The refuter's Acme statement: net income 541, less the noncontrolling interest's 40, and
    `Net income attributable to Acme Corp.` 501. The attributable row is not one of the stated
    labels, but it is a row that says attributable to, so 541 is the total before the
    noncontrolling interest and is held to `ProfitLoss`."""
    report = _fact(net_income=501e6, net_income_with_noncontrolling=541e6, revenue=6e9)
    table = _blocks([_row("Revenue", "6,000"), _row("Net income", "541"),
                     "| Less: Net income attributable to noncontrolling interests | 40 |  | 10 |",
                     _row("Net income attributable to Acme Corp.", "501")])
    out = rvr.compare(["p:1"], [table], "2026-06-30", report)
    cell = out["net_income"]["comparisons"][0]
    assert cell["verdict"] == "agrees" and cell["report"]["value"] == 541e6
    table = table.replace("| Net income | $ | 541 |", "| Net income | $ | 501 |")
    assert rvr.compare(["p:1"], [table], "2026-06-30", report)["net_income"]["verdict"] == "differs"
    # a table with no attributable row keeps the default
    plain = _blocks([_row("Revenue", "6,000"), _row("Net income", "541")])
    assert rvr.compare(["p:1"], [plain], "2026-06-30", report)["net_income"]["verdict"] == "differs"


def test_release_versus_report_a_row_of_dollars_and_percents_compares_its_dollars():
    """Two dollar figures and one percent under a header of two periods: the dollars are
    compared and only the percent cell is left out."""
    table = _blocks(["| Net income | $ | 100 |  | $ | 90 |  | 11 | % |"])
    out = rvr.compare(["p:1"], [table], "2026-06-30", _fact(net_income=1e8))
    assert [c["release"]["cell"] for c in out["net_income"]["comparisons"]] == ["100"]
    assert out["net_income"]["verdict"] == "agrees"
    assert [e["cell"] for e in out["net_income"]["excluded_rows"]] == ["11"]
    wrong = _blocks(["| Net income | $ | 110 |  | $ | 90 |  | 11 | % |"])
    assert rvr.compare(["p:1"], [wrong], "2026-06-30", _fact(net_income=1e8)
                       )["net_income"]["verdict"] == "differs"


def test_release_versus_report_a_mixed_row_that_does_not_fit_the_header_is_listed_unread():
    table = _blocks(["| Net income | $ | 100 |  | $ | 90 |  | $ | 80 |  | 11 | % |"])
    out = rvr.compare(["p:1"], [table], "2026-06-30", _fact(net_income=1e8))
    assert out["net_income"]["verdict"] == "period_not_read"
    assert out["net_income"]["comparisons"] == []
    assert "figures and the header names" in out["net_income"]["unread"][0]["reason"]
    # a row printed wholly as percents is left out and named
    table = _blocks(["| Net income | 8.8 | % |  | 3.9 | % |  | 1.2 | % |", _row("Net income", "100")])
    out = rvr.compare(["p:1"], [table], "2026-06-30", _fact(net_income=1e8))
    assert out["net_income"]["verdict"] == "agrees"
    assert [e["cell"] for e in out["net_income"]["excluded_rows"]] == ["8.8"]


# --- every verdict is named in what the section says it is, and in the analyst's sentence ----------

VERDICTS = ("differs", "differs_outside_gaap", "agrees", "block_not_identified",
            "report_fact_missing", "period_not_read", "not_in_release",
            "printed_under_another_label")


def test_release_versus_report_the_section_names_every_verdict_it_can_write():
    for verdict in VERDICTS:
        assert f"`{verdict}`" in calculator.RELEASE_WHAT_THIS_IS, verdict
    for verdict in ("agrees", "differs", "not_compared"):
        assert f"`{verdict}`" in calculator.RELEASE_WHAT_THIS_IS
    written = set()
    for rows in ([_row("Net revenue", "1,000")], [_row("Net revenue", "1,100")]):
        written |= {e["verdict"] for e in _run(rows, _fact(revenue=1e9)).values()}
    assert {"agrees" , "differs", "not_in_release"} <= written


def test_release_versus_report_the_analysts_sentence_names_every_verdict():
    prompt = (REPO_ROOT / ".claude" / "agents" / "accounting-analyst.md").read_text(encoding="utf-8")
    area = prompt.split("**Cross-document reconciliation**", 1)[1].split(
        "**Revenue and working capital.**", 1)[0]
    sentence = area.split("`release_versus_report`", 1)[1].split("\n\n", 1)[0]
    flat = " ".join(sentence.split())
    for verdict in VERDICTS:
        assert f"`{verdict}`" in flat, verdict
    assert "`statement`" in flat
    assert prompt.count("`release_versus_report`") == 1


def test_release_versus_report_a_unit_row_between_a_heading_and_its_rows_ends_nothing():
    rows = ["| Summary of Stock-Based Compensation Expense: |", UNIT_ROW,
            _row("Cost of revenue", "7.4")]
    out = _run(rows, _fact(cost_of_revenue=1_125.4e6))
    assert out["cost_of_revenue"]["comparisons"][0]["block"] == "component"
    rows = ["| Basic: |", UNIT_ROW, _row("Net income", "0.61")]
    out = _run(rows, _fact(net_income=1e8))
    assert [e["cell"] for e in out["net_income"]["excluded_rows"]] == ["0.61"]


# --- round five: independent expected values -----------------------------------------------------------

def _instance_value(ticker: str, accession: str, tag: str, start: str, end: str) -> float:
    """A fact read from the filing's committed XBRL instance with `xml.etree` alone, nothing
    from `src/`: the entity-wide value (no dimension) of one concept over one period."""
    import gzip
    import json
    import xml.etree.ElementTree as ET
    manifest = json.loads((REPO_ROOT / "tests" / "fixtures" / ticker / "manifest.json")
                          .read_text(encoding="utf-8"))
    row, = [d for d in manifest["documents"]
            if d.get("role") == "xbrl_instance" and d.get("accession") == accession]
    path = REPO_ROOT / "tests" / "fixtures" / ticker / row["path"]
    raw = path.read_bytes()
    root = ET.fromstring(gzip.decompress(raw) if path.suffix == ".gz" else raw)
    xbrli = "{http://www.xbrl.org/2003/instance}"
    wanted = set()
    for context in root.iter(f"{xbrli}context"):
        period = context.find(f"{xbrli}period")
        if (context.find(f"{xbrli}entity/{xbrli}segment") is None and period is not None
                and period.findtext(f"{xbrli}startDate") == start
                and period.findtext(f"{xbrli}endDate") == end):
            wanted.add(context.get("id"))
    values = {float(element.text) for element in root.iter()
              if element.tag.endswith("}" + tag) and element.get("contextRef") in wanted
              and element.text}
    assert len(values) == 1, (ticker, tag, start, end, values)
    return values.pop()


def _eps(ticker: str, period: str, cutoff: str) -> float:
    rows = [row["val"] for row in source.rows(ticker, "EarningsPerShareDiluted", unit="USD/shares")
            if source.spelled(row) == period and row["filed"] <= cutoff]
    assert len(set(rows)) == 1, (ticker, period, rows)
    return float(rows[0])


def _printed_value(text: str, scale: str) -> tuple[float, float]:
    """The dollars a printed cell says and half its step, worked here: `1,570.7` in millions
    is 1,570,700,000 with a half step of 50,000."""
    factor = {"millions": 1e6, "thousands": 1e3, "dollars": 1.0}[scale]
    body = text.strip("()$ ").replace(",", "")
    decimals = len(body.split(".")[1]) if "." in body else 0
    return float(body) * factor, factor / (10 ** decimals) / 2


# ticker -> (cutoff, statement paragraph, scale, how the record is read, [(line, label, printed
# cell, concept, period)]). The cells are the three-month column of each face statement, read
# by eye in the committed `input_8k.md`.
STATEMENT_ROWS = {
    "ANET": ("2026-08-05", "34", "millions", "facts", [
        ("revenue", "Total revenue", "3,035.7", "RevenueFromContractWithCustomerExcludingAssessedTax", "2026-04-01..2026-06-30"),
        ("cost_of_revenue", "Total cost of revenue", "1,125.4", "CostOfGoodsAndServicesSold", "2026-04-01..2026-06-30"),
        ("operating_income", "Income from operations", "1,378.0", "OperatingIncomeLoss", "2026-04-01..2026-06-30"),
        ("pretax_income", "Income before income taxes", "1,504.3", "IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest", "2026-04-01..2026-06-30"),
        ("income_tax_expense", "Provision for income taxes", "291.4", "IncomeTaxExpenseBenefit", "2026-04-01..2026-06-30"),
        ("net_income", "Net income", "1,212.9", "NetIncomeLoss", "2026-04-01..2026-06-30")]),
    "CIEN": ("2026-06-04", "55", "thousands", "facts", [
        ("revenue", "Total revenue", "1,570,739", "Revenues", "2026-02-01..2026-05-02"),
        ("cost_of_revenue", "Total cost of goods sold", "879,185", "CostOfGoodsAndServicesSold", "2026-02-01..2026-05-02"),
        ("operating_income", "Income from operations", "237,871", "OperatingIncomeLoss", "2026-02-01..2026-05-02"),
        ("pretax_income", "Income before income taxes", "231,060", "IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest", "2026-02-01..2026-05-02"),
        ("income_tax_expense", "Provision for income taxes", "12,840", "IncomeTaxExpenseBenefit", "2026-02-01..2026-05-02"),
        ("net_income", "Net income", "218,220", "NetIncomeLoss", "2026-02-01..2026-05-02")]),
    "ESE": ("2026-08-10", "53", "thousands", "facts", [
        ("revenue", "Net Sales", "339,027", "RevenueFromContractWithCustomerExcludingAssessedTax", "2026-04-01..2026-06-30"),
        ("cost_of_revenue", "Cost of sales", "197,508", "CostOfRevenue", "2026-04-01..2026-06-30"),
        ("pretax_income", "Earnings before income taxes", "40,954", "IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest", "2026-04-01..2026-06-30"),
        ("income_tax_expense", "Income tax expense", "8,219", "IncomeTaxExpenseBenefit", "2026-04-01..2026-06-30"),
        ("net_income", "Net earnings", "32,735", "NetIncomeLoss", "2026-04-01..2026-06-30")]),
    "FTNT": ("2026-07-30", "68", "millions", "facts", [
        ("revenue", "Total revenue", "2,047.9", "RevenueFromContractWithCustomerExcludingAssessedTax", "2026-04-01..2026-06-30"),
        ("cost_of_revenue", "Total cost of revenue", "404.7", "CostOfGoodsAndServicesSold", "2026-04-01..2026-06-30"),
        ("operating_income", "OPERATING INCOME", "689.3", "OperatingIncomeLoss", "2026-04-01..2026-06-30"),
        ("income_tax_expense", "PROVISION FOR INCOME TAXES", "115.0", "IncomeTaxExpenseBenefit", "2026-04-01..2026-06-30"),
        ("net_income", "NET INCOME", "606.3", "NetIncomeLoss", "2026-04-01..2026-06-30")]),
    "LFUS": ("2026-07-29", "53", "thousands", "instance", [
        ("revenue", "Net sales", "738,781", "RevenueFromContractWithCustomerIncludingAssessedTax", "2026-03-29..2026-06-27"),
        ("cost_of_revenue", "Cost of sales", "432,717", "CostOfGoodsAndServicesSold", "2026-03-29..2026-06-27"),
        ("operating_income", "Operating income", "119,724", "OperatingIncomeLoss", "2026-03-29..2026-06-27"),
        ("pretax_income", "Income before income taxes", "117,064", "IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest", "2026-03-29..2026-06-27"),
        ("income_tax_expense", "Income taxes", "27,659", "IncomeTaxExpenseBenefit", "2026-03-29..2026-06-27"),
        ("net_income", "Net income", "89,405", "NetIncomeLoss", "2026-03-29..2026-06-27")]),
    "QCOM": ("2026-07-29", "54", "millions", "facts", [
        ("revenue", "Total revenues", "9,947", "Revenues", "2026-03-30..2026-06-28"),
        ("cost_of_revenue", "Cost of revenues", "4,670", "CostOfRevenue", "2026-03-30..2026-06-28"),
        ("operating_income", "Operating income", "1,626", "OperatingIncomeLoss", "2026-03-30..2026-06-28"),
        ("pretax_income", "Income before income taxes", "2,462", "IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest", "2026-03-30..2026-06-28"),
        ("income_tax_expense", "Income tax (expense) benefit", "(460)", "IncomeTaxExpenseBenefit", "2026-03-30..2026-06-28"),
        ("net_income", "Net income", "2,002", "NetIncomeLoss", "2026-03-30..2026-06-28")]),
}

# diluted earnings per share, the three-month column of each statement that prints it under
# a per-share heading or a stated label
EPS_ROWS = {
    "AAPL": ("2026-07-31", "29", "Diluted", "2.02", "2026-03-29..2026-06-27"),
    "ANET": ("2026-08-05", "34", "Diluted", "0.95", "2026-04-01..2026-06-30"),
    "CIEN": ("2026-06-04", "55", "Diluted net income per potential common share", "1.49", "2026-02-01..2026-05-02"),
    "DELL": ("2026-09-08", "63", "Diluted", "6.34", "2026-05-02..2026-07-31"),
    "FTNT": ("2026-07-30", "68", "Diluted", "0.82", "2026-04-01..2026-06-30"),
    "NVDA": ("2026-08-26", "69", "Diluted", "2.46", "2026-04-27..2026-07-26"),
    "QCOM": ("2026-07-29", "54", "Diluted earnings per share", "1.87", "2026-03-30..2026-06-28"),
}


@pytest.mark.parametrize("ticker", sorted(STATEMENT_ROWS))
def test_release_versus_report_each_face_statement_line_equals_the_records_own_figure(ticker):
    """For seven releases the statement's compared lines were only ever checked against the
    code's own run. Here every line's report value is read from the record itself (companyfacts
    through `tests/companyfacts_source.py`, or the committed instance with `xml.etree` for
    Littelfuse, whose record has not caught up), and the release's printed cell must equal it
    at the cell's own printed precision."""
    cutoff, number, scale, how, rows = STATEMENT_ROWS[ticker]
    accession = STATEMENTS[ticker][0]
    lines = _planted(ticker, accession, {})
    for line, label, printed, tag, period in rows:
        start, end = period.split("..")
        expected = (source.one_value(ticker, tag, period, cutoff) if how == "facts"
                    else _instance_value(ticker, accession, tag, start, end))
        value, half_step = _printed_value(printed, scale)
        assert abs(value - expected) <= half_step, (ticker, line, printed, expected)
        cells = [c for c in _in_table(lines[line], number)
                 if c["span_months"] == 3 and c["release"]["label"] == label]
        assert cells and {c["release"]["cell"] for c in cells} == {printed}, (ticker, line)
        assert {c["report"]["value"] for c in cells} == {expected}, (ticker, line)
        assert {c["verdict"] for c in cells} == {"agrees"}, (ticker, line)


def test_release_versus_report_seagates_fourth_quarter_is_the_year_less_the_nine_months():
    """Seagate's statement prints the quarter and the fiscal year; the 10-K tags only the year,
    so the quarter is the year less the nine months, worked here from the record."""
    cutoff, accession = "2026-08-04", STATEMENTS["STX"][0]
    lines = _planted("STX", accession, {})
    for line, label, printed, tag in (
            ("revenue", "Revenue", "3,629", "RevenueFromContractWithCustomerExcludingAssessedTax"),
            ("cost_of_revenue", "Cost of revenue", "1,731", "CostOfGoodsAndServicesSold"),
            ("operating_income", "Income from operations", "1,559", "OperatingIncomeLoss"),
            ("pretax_income", "Income before income taxes", "1,505",
             "IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest"),
            ("income_tax_expense", "Provision for income taxes", "211", "IncomeTaxExpenseBenefit"),
            ("net_income", "Net income", "1,294", "NetIncomeLoss")):
        year = source.one_value("STX", tag, "2025-06-28..2026-07-03", cutoff)
        nine = source.one_value("STX", tag, "2025-06-28..2026-04-03", cutoff)
        quarter = year - nine
        value, half_step = _printed_value(printed, "millions")
        assert abs(value - quarter) <= half_step, (line, printed, quarter)
        cell, = [c for c in _in_table(lines[line], "59")
                 if c["span_months"] == 3 and c["release"]["label"] == label]
        assert cell["report"]["value"] == quarter and cell["verdict"] == "agrees", line


@pytest.mark.parametrize("ticker", sorted(EPS_ROWS))
def test_release_versus_report_diluted_earnings_per_share_equals_the_records_figure(ticker):
    cutoff, number, label, printed, period = EPS_ROWS[ticker]
    expected = _eps(ticker, period, cutoff)
    assert abs(float(printed) - expected) <= 0.005, (ticker, expected)
    lines = _planted(ticker, STATEMENTS[ticker][0], {})
    cells = [c for c in _in_table(lines["diluted_earnings_per_share"], number)
             if c["span_months"] == 3 and c["release"]["label"] == label]
    assert [c["release"]["cell"] for c in cells] == [printed], ticker
    assert [c["report"]["value"] for c in cells] == [expected] and cells[0]["verdict"] == "agrees"


def test_release_versus_report_littelfuses_diluted_earnings_per_share_is_read_from_the_filing():
    """Littelfuse's companyfacts record lacks the quarter, so its diluted earnings per share is
    read from the committed instance: `Diluted | $ | 3.49`."""
    expected = _instance_value("LFUS", STATEMENTS["LFUS"][0], "EarningsPerShareDiluted",
                               "2026-03-29", "2026-06-27")
    assert expected == 3.49
    lines = _planted("LFUS", STATEMENTS["LFUS"][0], {})
    cell, = [c for c in _in_table(lines["diluted_earnings_per_share"], "53") if c["span_months"] == 3]
    assert cell["release"]["cell"] == "3.49" and cell["report"]["value"] == expected
    assert cell["verdict"] == "agrees"


# --- capital expenditure, read independently (L2) and the plain synonyms (R3) ----------------------

def test_release_versus_report_capital_expenditure_agrees_exactly_for_fortinet_and_carrier():
    """Fortinet's `Less: Purchases of property and equipment (78.0)` is the six months' payments
    for property and equipment (148.6 million) less the first quarter's (70.6 million), read
    through companyfacts. Carrier's record tags `PaymentsToAcquireProductiveAssets`, not the
    property-and-equipment concept; its first quarter is in companyfacts (94 million) and its six
    months (211 million) in the committed instance, so the quarter is 117 million."""
    fortinet = (source.one_value("FTNT", "PaymentsToAcquirePropertyPlantAndEquipment",
                                 "2026-01-01..2026-06-30", "2026-07-30")
                - source.one_value("FTNT", "PaymentsToAcquirePropertyPlantAndEquipment",
                                   "2026-01-01..2026-03-31", "2026-07-30"))
    assert fortinet == 78.0e6
    lines = _planted("FTNT", STATEMENTS["FTNT"][0], {})
    assert lines["capital_expenditure"]["verdict"] == "agrees"
    cell, = [c for c in _in_table(lines["capital_expenditure"], "79") if c["span_months"] == 3]
    assert cell["release"]["cell"] == "(78.0)" and cell["report"]["value"] == fortinet

    six = _instance_value("CARR", STATEMENTS["CARR"][0], "PaymentsToAcquireProductiveAssets",
                          "2026-01-01", "2026-06-30")
    first = source.one_value("CARR", "PaymentsToAcquireProductiveAssets", "2026-01-01..2026-03-31",
                             "2026-07-28")
    assert (six, first) == (211e6, 94e6) and six - first == 117e6
    carrier = _planted("CARR", STATEMENTS["CARR"][0], {})
    assert carrier["capital_expenditure"]["verdict"] == "agrees"
    quarter = [c for c in carrier["capital_expenditure"]["comparisons"] if c["span_months"] == 3]
    assert {c["release"]["cell"] for c in quarter} == {"(117)"}
    assert {c["report"]["value"] for c in quarter} == {six - first}
    assert {c["block"] for c in carrier["capital_expenditure"]["comparisons"]} == {"gaap"}


@pytest.mark.parametrize("label,kind", [
    ("Purchases of property and equipment", "line"),
    ("Acquisition of property, equipment and leasehold improvements", "line"),
    ("Payments for equipment, furniture, and fixtures", "line"),
    ("Expenditures for property, plant and equipment", "line"),
    ("Purchases related to property and equipment and intangible assets", "other"),
    ("Purchases of property and equipment, net", "other"),
    ("Purchase of equipment in accounts payable", "other"),
    ("Capital expenditures and capitalized software development costs", None),
    ("Proceeds from sale of property and equipment", None),
    ("Purchases of investments", None)])
def test_release_versus_report_a_plain_synonym_of_capital_expenditure_is_the_line(label, kind):
    assert rvr.capex_synonym(label) == kind
    expected = "capital_expenditure" if kind == "line" else None
    assert rvr.line_of_label(label) == (LINE_OF_STATED.get(label) or expected)


LINE_OF_STATED = {"Purchases of property and equipment": "capital_expenditure"}


def test_release_versus_report_committed_capital_expenditure_synonyms_agree_with_the_record():
    """Seagate `Acquisition of property, equipment and leasehold improvements | (569)` (the
    fiscal year; the record's 569,000,000, and (187) the quarter, 569 less the nine months'
    382); Ciena `Payments for equipment, furniture, and fixtures | (114,933)` (six months,
    114,933,000)."""
    year = source.one_value("STX", "PaymentsToAcquirePropertyPlantAndEquipment",
                            "2025-06-28..2026-07-03", "2026-08-04")
    nine = source.one_value("STX", "PaymentsToAcquirePropertyPlantAndEquipment",
                            "2025-06-28..2026-04-03", "2026-08-04")
    assert (year, nine, year - nine) == (569e6, 382e6, 187e6)
    stx = _planted("STX", STATEMENTS["STX"][0], {})["capital_expenditure"]
    assert stx["verdict"] == "agrees"
    cells = {(c["release"]["cell"], c["span_months"]): c for c in stx["comparisons"]}
    assert cells[("(569)", 12)]["report"]["value"] == year
    assert cells[("(187)", 3)]["report"]["value"] == year - nine
    ciena = source.one_value("CIEN", "PaymentsToAcquirePropertyPlantAndEquipment",
                             "2025-11-02..2026-05-02", "2026-06-04")
    assert ciena == 114_933e3
    cell, = _planted("CIEN", STATEMENTS["CIEN"][0], {})["capital_expenditure"]["comparisons"]
    assert (cell["release"]["label"], cell["release"]["cell"], cell["span_months"]) == (
        "Payments for equipment, furniture, and fixtures", "(114,933)", 6)
    assert cell["report"]["value"] == ciena and cell["verdict"] == "agrees"


def test_release_versus_report_nvidias_purchases_that_also_cover_intangibles_are_not_the_line():
    """`Purchases related to property and equipment and intangible assets | (2,677)` covers more
    than property and equipment: printed under another label, listed, never absent and never
    compared."""
    entry = _planted("NVDA", STATEMENTS["NVDA"][0], {})["capital_expenditure"]
    assert entry["verdict"] == "printed_under_another_label" and "comparisons" not in entry
    assert [(r["label"], r["cell"], r["span_months"]) for r in entry["rows"]] == [
        ("Purchases related to property and equipment and intangible assets", "(2,677)", 3),
        ("Purchases related to property and equipment and intangible assets", "(4,434)", 6)]


def test_release_versus_report_a_table_with_no_stated_row_still_gets_the_other_label_scan():
    table = _blocks([_row("Purchases of property and equipment, net", "(100)"),
                     _row("Free cash flow", "500")])
    out = rvr.compare(["p:1"], [table], "2026-06-30", _fact(capital_expenditure=100e6))
    assert out["capital_expenditure"]["verdict"] == "printed_under_another_label"
    assert [(r["label"], r["cell"]) for r in out["capital_expenditure"]["rows"]] == [
        ("Purchases of property and equipment, net", "(100)")]
    # beside a stated row it is the same
    table = _blocks([_row("Net revenue", "1,000"), _row("Purchases of property and equipment, net", "(100)")])
    out = rvr.compare(["p:1"], [table], "2026-06-30", _fact(capital_expenditure=100e6, revenue=1e9))
    assert out["capital_expenditure"]["verdict"] == "printed_under_another_label"


def test_release_versus_report_income_taxes_is_the_tax_line_and_littelfuses_agrees():
    expected = _instance_value("LFUS", STATEMENTS["LFUS"][0], "IncomeTaxExpenseBenefit",
                               "2026-03-29", "2026-06-27")
    assert expected == 27_659e3
    cell, = [c for c in _in_table(_planted("LFUS", STATEMENTS["LFUS"][0], {})["income_tax_expense"], "53")
             if c["span_months"] == 3]
    assert (cell["release"]["label"], cell["release"]["cell"]) == ("Income taxes", "27,659")
    assert cell["report"]["value"] == expected and cell["verdict"] == "agrees"
    out = _run([_row("Income taxes", "28")], _fact(income_tax_expense=27e6))
    assert out["income_tax_expense"]["verdict"] == "differs"


def test_release_versus_report_diluted_is_earnings_per_share_only_under_a_per_share_heading():
    """Apple's `Diluted | $ | 2.02` under `Earnings per share:`, and its share count `Diluted |
    14,714,676` under `Shares used in computing earnings per share:`: the first is the line, the
    second is not."""
    aapl = _planted("AAPL", STATEMENTS["AAPL"][0], {})["diluted_earnings_per_share"]
    assert {c["release"]["cell"] for c in aapl["comparisons"] if c["span_months"] == 3} == {"2.02"}
    assert aapl["verdict"] == "agrees"
    rows = ["| Earnings per share: |", _row("Basic", "2.03"), _row("Diluted", "2.02"),
            "| Shares used in computing earnings per share: |", _row("Basic", "14,656,110"),
            _row("Diluted", "14,714,676")]
    out = _run(rows, _fact(diluted_earnings_per_share=2.02))
    assert [c["release"]["cell"] for c in out["diluted_earnings_per_share"]["comparisons"]] == ["2.02"]
    assert out["diluted_earnings_per_share"]["verdict"] == "agrees"
    assert _run([_row("Diluted", "2.02")], _fact(diluted_earnings_per_share=2.02)
                )["diluted_earnings_per_share"]["verdict"] == "not_in_release"
    assert rvr.row_lines([rvr.cells_of(r) for r in _blocks(rows).split("\n")])[-1] is None


# --- the heading that carries a unit (R1) ---------------------------------------------------------

@pytest.mark.parametrize("label,words", [
    ("Other financial data (in millions):", "Other financial data"),
    ("Consolidated results (in thousands)", "Consolidated results"),
    ("GAAP results ($ in millions):", "GAAP results"),
    ("(In millions, except per share amounts)", ""),
    ("(U.S. Dollars in Thousands, Except Share and Per Share Data)", ""),
    ("(in thousands, except per share data) (unaudited)", ""),
    ("Basic:", "Basic")])
def test_release_versus_report_a_heading_keeps_its_own_words_and_loses_its_unit(label, words):
    assert rvr.heading_text(label) == words


def test_release_versus_report_a_heading_with_a_unit_ends_a_per_share_block():
    rows = ["| Diluted earnings per share: |", _row("Net income", "0.61"),
            "| Other financial data (in millions): |", _row("Net income", "999")]
    out = _run(rows, _fact(net_income=100e6))
    assert out["net_income"]["verdict"] == "differs"
    assert [c["release"]["cell"] for c in out["net_income"]["comparisons"]] == ["999"]
    assert [e["cell"] for e in out["net_income"]["excluded_rows"]] == ["0.61"]


def test_release_versus_report_a_heading_with_a_unit_ends_a_component_block():
    rows = ["| Summary of stock-based compensation: |", _row("Cost of revenue", "7"),
            "| Consolidated results (in millions): |", _row("Net income", "150")]
    out = _run(rows, _fact(net_income=100e6, cost_of_revenue=400e6))
    assert out["net_income"]["verdict"] == "differs"
    assert out["net_income"]["comparisons"][0]["block"] == "gaap"
    assert out["cost_of_revenue"]["comparisons"][0]["block"] == "component"


def test_release_versus_report_a_gaap_heading_with_a_unit_labels_its_rows_gaap():
    table = "\n".join(["|  | Non-GAAP |", "|  | Three Months Ended |",
                       "|  | June 30, 2026 |  | June 30, 2025 |", "|  | (in millions) |",
                       "| Net revenue | $ | 1,000 |  |  | $ | 1 |",
                       "| GAAP results (in millions): |", _row("Net income", "150")])
    out = rvr.compare(["p:1"], [table], "2026-06-30", _fact(net_income=100e6, revenue=1e9))
    cell = out["net_income"]["comparisons"][0]
    assert cell["block"] == "gaap" and cell["verdict"] == "differs"
    assert out["net_income"]["verdict"] == "differs"


# --- net income: the parent's row is a dollar row, and a missing ProfitLoss falls back (R2) ----------

def test_release_versus_report_without_profit_or_loss_a_planted_net_income_still_differs():
    """A table with a parent's row, a record with no ProfitLoss: the planted 150 against
    NetIncomeLoss 100 reads `differs`, and the cell says which fact it was held to."""
    rows = [_row("Revenue", "1,000"), _row("Net income", "150"),
            _row("Net income attributable to Acme Corp.", "100")]
    only = _fact(net_income=100e6, revenue=1e9)
    out = _run(rows, only)
    cell = out["net_income"]["comparisons"][0]
    assert out["net_income"]["verdict"] == "differs" and cell["verdict"] == "differs"
    assert cell["report"]["value"] == 100e6 and "ProfitLoss is not on record" in cell["held_to"]
    assert cell["difference"] == 50_000_000.0
    # with ProfitLoss on record the same row is the total and agrees at 150
    both = _fact(net_income=100e6, net_income_with_noncontrolling=150e6, revenue=1e9)
    out = _run(rows, both)
    assert out["net_income"]["comparisons"][0]["verdict"] == "agrees"
    assert "held_to" not in out["net_income"]["comparisons"][0]
    # a cash-flow statement with no ProfitLoss falls back the same way
    cash = [_row("Net income", "150"), _row("Net cash provided by operating activities", "700"),
            _row("Net cash used in investing activities", "(200)"),
            _row("Cash and cash equivalents, end of period", "1,200")]
    out = _run(cash, _fact(net_income=100e6, operating_cash_flow=700e6))
    assert out["net_income"]["verdict"] == "differs"


@pytest.mark.parametrize("label,heading", [
    ("Net income per share attributable to common stockholders - diluted", None),
    ("Net income attributable to Acme Corp. per common share", None),
    ("Earnings per share attributable to Acme Corp.", None),
    ("Net income attributable to Acme Corp.", "Basic:")])
def test_release_versus_report_a_per_share_row_never_switches_the_concept(label, heading):
    """An EPS row that says attributable to is not the parent's dollar row: the unlabelled net
    income keeps `NetIncomeLoss`, and 501 agrees where `ProfitLoss` is 541."""
    report = _fact(net_income=501e6, net_income_with_noncontrolling=541e6)
    rows = [_row("Net income", "501")] + ([f"| {heading} |"] if heading else []) + [_row(label, "1.50")]
    out = _run(rows, report)
    cell = out["net_income"]["comparisons"][0]
    assert cell["verdict"] == "agrees" and cell["report"]["value"] == 501e6, label


def test_release_versus_report_a_dollar_row_that_names_net_income_and_attributable_to_switches_it():
    report = _fact(net_income=501e6, net_income_with_noncontrolling=541e6)
    for label in ("Net income attributable to Acme Corp.", "Earnings attributable to Acme Corp.",
                  "Net earnings attributable to common shareowners"):
        out = _run([_row("Net income", "541"), _row(label, "501")], report)
        assert out["net_income"]["comparisons"][0]["verdict"] == "agrees", label
        assert out["net_income"]["comparisons"][0]["report"]["value"] == 541e6, label
    # a row that says attributable to but is not net income or earnings does not
    out = _run([_row("Net income", "501"), _row("Revenue attributable to Acme Corp.", "900")],
               _fact(net_income=501e6, net_income_with_noncontrolling=541e6, revenue=9e8))
    assert out["net_income"]["comparisons"][0]["report"]["value"] == 501e6
    assert rvr._names_attributable_net_income("Less: Net income attributable to noncontrolling interests")


# --- sub-columns are named, and only the statement's are GAAP (R4) ----------------------------------

def _sub_table(names):
    header = " | ".join(names * 2)
    return "\n".join(["|  | Three Months Ended June 30, 2026 |  | Six Months Ended June 30, 2026 |",
                      f"| (In millions) | {header} |",
                      "| Operating profit | $ | 825 |  | 270 |  | $ | 1,095 |  | $ | 1,083 |  | 606 |  | $ | 1,689 |"])


@pytest.mark.parametrize("names", [["As Reported", "Special Items", "Adjusted"],
                                   ["Reported", "Impact", "Non-GAAP"], ["GAAP", "Adj.", "Adjusted"]])
def test_release_versus_report_only_reported_and_gaap_sub_columns_are_the_statements(names):
    full = rvr.compare_release(["p:1"], [_sub_table(names)], "2026-06-30",
                               _fact(operating_income=825e6))
    comparisons = full["lines"]["operating_income"]["comparisons"]
    assert [(c["span_months"], c["release"]["cell"], c["block"]) for c in comparisons] == [
        (3, "825", "gaap"), (3, "1,095", "not_gaap"), (6, "1,083", "gaap"), (6, "1,689", "not_gaap")]
    # the middle sub-column is not a dollar of the line: left out, and listed with its name
    assert {c["release"]["cell"] for c in comparisons}.isdisjoint({"270", "606"})
    listed = [(n["sub_column"], n["span_months"]) for n in full["unread_columns"] if "sub_column" in n]
    assert listed == [(names[1], 3), (names[1], 6)]
    assert all(names[1] in n["reason"] for n in full["unread_columns"] if "sub_column" in n)


def test_release_versus_report_a_middle_sub_column_called_special_items_is_never_gaap():
    """The refuter's `As Reported | Special Items | Adjusted`: the Special Items cell, 270, is not
    compared, so a planted change there cannot be read as a difference, and the Reported
    cell is held to the statement."""
    out = rvr.compare(["p:1"], [_sub_table(["As Reported", "Special Items", "Adjusted"])
                                .replace("825", "925", 1)], "2026-06-30", _fact(operating_income=825e6))
    assert out["operating_income"]["verdict"] == "differs"
    assert [c["block"] for c in out["operating_income"]["comparisons"] if c["verdict"] == "differs"
            ][0] == "gaap"


# --- _NOT_THE_LINE, one word at a time, and the figure count (needs judgment) -------------------------

@pytest.mark.parametrize("word,label", [
    ("weighted", "Weighted net income"), ("shares", "Net income shares"),
    ("deferred", "Deferred net income"), ("current", "Current net income"),
    ("adjusted", "Adjusted net income"), ("non-GAAP", "Non-GAAP net income")])
def test_release_versus_report_each_excluding_word_alone_keeps_a_row_out_of_the_candidates(word, label):
    """Each label holds the stated `Net income` and only the one excluding word, so each is
    kept out of `printed_under_another_label` by that word alone; without it the row would be
    listed."""
    out = _run([_row("Net revenue", "1,000"), _row(label, "812")], _fact(revenue=1e9))
    assert out["net_income"]["verdict"] == "not_in_release", word
    # and the same label without the word is a candidate
    import re
    bare = re.sub(re.escape(word), "", label, flags=re.IGNORECASE).strip()
    out = _run([_row("Net revenue", "1,000"), _row(f"{bare} before special items", "812")],
               _fact(revenue=1e9))
    assert out["net_income"]["verdict"] == "printed_under_another_label", word


def test_release_versus_report_a_candidate_row_with_the_wrong_count_of_figures_is_not_listed():
    """`Net income before special items` with three figures under a header of two columns cannot
    be read at the period: not listed, and the line is not called printed."""
    out = _run([_row("Net revenue", "1,000"),
                "| Net income before special items | $ | 812 |  | $ | 700 |  | $ | 600 |"],
               _fact(revenue=1e9))
    assert out["net_income"]["verdict"] == "not_in_release"
    out = _run([_row("Net revenue", "1,000"), "| Net income before special items | $ | 812 |"],
               _fact(revenue=1e9))
    assert out["net_income"]["verdict"] == "not_in_release"
    out = _run([_row("Net revenue", "1,000"), _row("Net income before special items", "812")],
               _fact(revenue=1e9))
    assert out["net_income"]["verdict"] == "printed_under_another_label"


# --- every cited paragraph, label and cell resolves in the committed input_8k.md (L3) ---------------

def _committed_paragraphs(ticker: str, accession: str) -> dict[str, list[list[str]]]:
    run = next(iter(sorted((REPO_ROOT / "runs" / ticker).glob(f"{accession}*"))))
    text = (run / "input_8k.md").read_text(encoding="utf-8")
    paragraphs: dict[str, list[list[str]]] = {}
    for block in text.split("\n\n["):
        head, _, body = block.partition("]\n")
        head = head.lstrip("[")
        if ":8k_2_02:" in head:
            paragraphs[head] = [[c.strip() for c in line[2:-2].split(" | ")]
                                for line in body.split("\n") if line.startswith("| ")]
    return paragraphs


def _cited(section) -> list[dict]:
    found = []
    if isinstance(section, dict):
        if "paragraph_id" in section and ("cell" in section or "label" in section):
            found.append(section)
        for value in section.values():
            found.extend(_cited(value))
    elif isinstance(section, list):
        for value in section:
            found.extend(_cited(value))
    return found


@pytest.mark.parametrize("ticker", sorted(STATEMENTS))
def test_release_versus_report_every_cited_paragraph_label_and_cell_is_in_the_committed_release(ticker):
    """Every paragraph id, row label and cell text the section cites resolves, in the run's own
    committed `input_8k.md`, to a row of that paragraph holding both."""
    accession = STATEMENTS[ticker][0]
    full = _planted_full(ticker, accession, {})
    committed = _committed_paragraphs(ticker, accession)
    cited = [c for c in _cited(full) if c.get("label") and c.get("cell")]
    assert cited, ticker
    for item in cited:
        rows = committed.get(item["paragraph_id"])
        assert rows is not None, (ticker, item["paragraph_id"])
        assert any(item["label"] in row and item["cell"] in row for row in rows), (
            ticker, item["paragraph_id"], item["label"], item["cell"])
    for item in _cited(full):
        if "paragraph_id" in item and item["paragraph_id"]:
            assert item["paragraph_id"] in committed, (ticker, item["paragraph_id"])
