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


def _by_months(entry: dict, months: int) -> dict:
    found = [c for c in entry["comparisons"] if c["span_months"] == months]
    assert len(found) == 1, entry
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
    assert cell["verdict"] == "agrees" and dell["lines"]["net_income"]["verdict"] == "agrees"


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
        assert entry["verdict"] == "agrees"


def test_release_versus_report_dell_diluted_earnings_per_share_agrees_at_two_decimals(dell):
    eps = _by_months(dell["lines"]["diluted_earnings_per_share"], 3)
    rows = source.rows("DELL", "EarningsPerShareDiluted", unit="USD/shares")
    stated = [row["val"] for row in rows if source.spelled(row) == DELL_QUARTER
              and row["filed"] <= DELL_CUTOFF]
    assert stated == [6.34]
    assert eps["release"]["cell"] == "6.34" and eps["release"]["printed_decimals"] == 2
    assert eps["report"]["value"] == 6.34 and eps["verdict"] == "agrees"


def test_release_versus_report_dell_prints_no_row_under_a_stated_capital_expenditure_label(dell):
    """Dell's cash-flow statement prints `Capital expenditures and capitalized software
    development costs`, which is not a label of the table, so the line is not_in_release
    rather than guessed."""
    entry = dell["lines"]["capital_expenditure"]
    assert entry["verdict"] == "not_in_release"
    assert entry["labels"] == list(rvr.ROW_LABELS["capital_expenditure"])


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
    """Labels are compared whole: `Non-GAAP net income` is not `Net income`, and
    `Revenue growth` is not `Revenue`."""
    out = _compare([_row("Non-GAAP net income", "9,999"), _row("Revenue growth", "5")],
                   {"net_income": {"value": 1.0}, "revenue": {"value": 1.0}})
    assert out["net_income"]["verdict"] == out["revenue"]["verdict"] == "not_in_release"


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
    assert out["revenue"]["paragraph_id"] == "p:1" and out["revenue"]["reason"]
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


def test_release_versus_report_the_first_readable_table_decides_and_a_later_one_is_listed():
    first = _table([_row("Net sales", "1,000")])
    segment = _table([_row("Net sales", "400")])
    out = rvr.compare(["p:1", "p:2"], [first, segment], "2026-06-30",
                      lambda line, months: {"value": 1_000_000_000.0})
    cell = out["revenue"]["comparisons"][0]
    assert cell["release"]["paragraph_id"] == "p:1" and cell["verdict"] == "agrees"
    assert [c["cell"] for c in cell["later_cells_that_differ"]] == ["400"]


def test_release_versus_report_the_first_block_of_a_span_is_the_one_read():
    """Side by side GAAP and non-GAAP columns of one span: the first is read."""
    rows = ["|  | Quarter Ended |  | Quarter Ended |", "|  | June 30, |  | June 30, |",
            "|  | 2026 |  | 2026 |", "| (in millions) |", "| Net income | $ | 100 |  | $ | 130 |"]
    out = rvr.compare(["p:1"], ["\n".join(rows)], "2026-06-30",
                      lambda line, months: {"value": 100_000_000.0})
    entries = out["net_income"]["comparisons"]
    assert [c["release"]["cell"] for c in entries] == ["100"]
    assert "other_rows_of_the_same_table" not in entries[0]
    # the second block's 130 is not what the report is held to
    out = rvr.compare(["p:1"], ["\n".join(rows)], "2026-06-30",
                      lambda line, months: {"value": 130_000_000.0})
    assert out["net_income"]["verdict"] == "differs"
    assert out["net_income"]["comparisons"][0]["difference"] == -30_000_000.0


# --- the label table ------------------------------------------------------------------------

def _labels_in_the_committed_releases() -> dict[str, set[str]]:
    found: dict[str, set[str]] = {}
    for path in glob.glob(str(REPO_ROOT / "runs" / "*" / "*" / "input_8k.md")):
        ticker = Path(path).parts[-3]
        for line in Path(path).read_text(encoding="utf-8").splitlines():
            if not (line.startswith("| ") and line.endswith(" |")):
                continue
            cells = rvr.cells_of(line)
            placed = rvr._label_of(cells)
            if placed and any(rvr.read_number(cell) is not None for cell in cells[placed[0] + 1:]):
                found.setdefault(rvr.normal_label(placed[1]), set()).add(ticker)
    return found


def test_release_versus_report_every_label_is_a_row_of_a_committed_release():
    found = _labels_in_the_committed_releases()
    unconfirmed = [(line, label) for line, labels in rvr.ROW_LABELS.items() for label in labels
                   if rvr.normal_label(label) not in found]
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
                           "Income tax provision", "Income tax (benefit) expense"),
    "net_income": ("Net income", "Net earnings", "Net income (loss)", "Net earnings (loss)",
                   "GAAP net income", "Net income (GAAP)",
                   "Net income attributable to Generac Holdings Inc.",
                   "Net income attributable to Johnson Controls",
                   "Net earnings (loss) attributable to common shareowners"),
    "diluted_earnings_per_share": ("Diluted earnings per share", "Earnings per share - diluted",
                                   "Diluted EPS", "GAAP diluted EPS",
                                   "GAAP diluted net income per share",
                                   "Diluted earnings per share (EPS)",
                                   "GAAP net income per share, diluted"),
    "operating_cash_flow": ("Net cash provided by operating activities",
                            "Change in cash from operating activities",
                            "Net cash flows provided by operating activities",
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


def test_release_versus_report_the_spec_example_labels_are_revenues():
    for label in ("Net revenue", "Total net revenue", "Net sales", "Revenue", "Total revenue"):
        assert label in EXPECTED_LABELS["revenue"]


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
    value = "(7)" if line == "capital_expenditure" else ("2.50" if line == "diluted_earnings_per_share"
                                                          else "7")
    report = 2.5 if line == "diluted_earnings_per_share" else 7_000_000.0
    out = _compare([_row(label, value)], {line: {"value": report}})
    assert out[line]["verdict"] == "agrees", (line, label)
    assert [other for other in rvr.LINES
            if other != line and out[other]["verdict"] != "not_in_release"] == []


@pytest.mark.parametrize("label", ["Sales", "Diluted", "Basic", "Income tax (expense) benefit",
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
