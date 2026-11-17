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


def test_release_versus_report_every_table_votes_and_a_segment_table_is_not_the_line():
    """Two statements print the line: the second's cell differs, and the line differs, with
    both cells listed under their paragraph ids. A table under a segment's heading is not
    the company's line and is listed apart."""
    first = _table([_row("Net sales", "1,000")])
    second = _table([_row("Net sales", "1,100")])
    out = rvr.compare(["p:1", "p:2"], [first, second], "2026-06-30",
                      lambda line, months: {"value": 1_000_000_000.0})
    assert out["revenue"]["verdict"] == "differs"
    assert [(c["release"]["paragraph_id"], c["verdict"]) for c in out["revenue"]["comparisons"]] \
        == [("p:1", "agrees"), ("p:2", "differs")]
    assert out["revenue"]["comparisons"][1]["difference"] == 100_000_000.0
    segment = _table([_row("Net sales", "400")])
    out = rvr.compare(["p:1", "p:0", "p:2"], [first, "Climate Solutions Americas (CSA)", segment],
                      "2026-06-30", lambda line, months: {"value": 1_000_000_000.0})
    assert out["revenue"]["verdict"] == "agrees"
    assert [c["cell"] for c in out["revenue"]["segment_cells_not_compared"]] == ["400"]


def test_release_versus_report_a_statement_title_above_a_table_is_not_a_segment_heading():
    for title in ("Condensed Consolidated Statements of Operations", "Reconciliation of net income",
                  "Total revenue by quarter", "Results of operations (unaudited)"):
        assert not rvr.is_segment_heading(title), title
    for title in ("Climate Solutions Americas (CSA)", "Climate Solutions Transportation (CST)"):
        assert rvr.is_segment_heading(title), title
    assert not rvr.is_segment_heading(None)
    assert not rvr.is_segment_heading("Net sales rose 4% to $6.4 billion.")


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


def test_release_versus_report_a_non_gaap_block_below_the_gaap_one_is_listed_not_compared():
    """GAAP above non-GAAP, the same label in both: the GAAP cell is held to the report,
    the non-GAAP cell is `not_gaap` and is not."""
    rows = ["| GAAP |", _row("Net income", "100"), "| Non-GAAP |", _row("Net income", "130")]
    out = rvr.compare(["p:1"], [_blocks(rows)], "2026-06-30",
                      lambda line, months: {"value": 100_000_000.0})
    assert out["net_income"]["verdict"] == "agrees"
    assert [c["release"]["cell"] for c in out["net_income"]["comparisons"]] == ["100"]
    assert [c["release"]["cell"] for c in out["net_income"]["not_gaap"]] == ["130"]
    assert out["net_income"]["not_gaap"][0]["verdict"] == "not_gaap"
    out = rvr.compare(["p:1"], [_blocks(["| GAAP |", _row("Net income", "110")] + rows[2:])],
                      "2026-06-30", lambda line, months: {"value": 100_000_000.0})
    assert out["net_income"]["verdict"] == "differs"


def test_release_versus_report_a_non_gaap_block_above_the_gaap_one():
    rows = ["| Non-GAAP |", _row("Net income", "130"), "| GAAP |", _row("Net income", "100")]
    out = rvr.compare(["p:1"], [_blocks(rows)], "2026-06-30",
                      lambda line, months: {"value": 100_000_000.0})
    assert [c["release"]["cell"] for c in out["net_income"]["comparisons"]] == ["100"]
    assert [c["release"]["cell"] for c in out["net_income"]["not_gaap"]] == ["130"]
    assert out["net_income"]["verdict"] == "agrees"
    # with only the non-GAAP block in the release the line is `not_gaap`, never `agrees`
    out = rvr.compare(["p:1"], [_blocks(rows[:2])], "2026-06-30",
                      lambda line, months: {"value": 100_000_000.0})
    assert out["net_income"]["verdict"] == "not_gaap"


def test_release_versus_report_side_by_side_blocks_are_told_apart_by_the_header_or_not_at_all():
    named = "\n".join(["|  | GAAP Results |  | Non-GAAP Results |",
                       "|  | Quarter Ended |  | Quarter Ended |", "|  | June 30, |  | June 30, |",
                       "|  | 2026 |  | 2026 |", "| (in millions) |",
                       "| Net income | $ | 100 |  | $ | 130 |"])
    out = rvr.compare(["p:1"], [named], "2026-06-30", lambda line, months: {"value": 1e8})
    assert out["net_income"]["verdict"] == "agrees"
    assert [c["release"]["cell"] for c in out["net_income"]["not_gaap"]] == ["130"]
    unnamed = named.replace("GAAP Results", "Results").replace("Non-Results", "Results") \
                   .replace("Non-GAAP Results", "More results")
    out = rvr.compare(["p:1"], [unnamed], "2026-06-30", lambda line, months: {"value": 1e8})
    assert out["net_income"]["verdict"] == "block_not_identified"
    assert {c["verdict"] for c in out["net_income"]["comparisons"]} == {"block_not_identified"}


def test_release_versus_report_a_heading_naming_both_is_not_identified_and_never_agrees():
    rows = ["| Reconciliation of GAAP and non-GAAP net income |", _row("Net income", "100")]
    out = rvr.compare(["p:1"], [_blocks(rows)], "2026-06-30", lambda line, months: {"value": 1e8})
    assert out["net_income"]["verdict"] == "block_not_identified"
    assert out["net_income"]["comparisons"][0]["verdict"] == "block_not_identified"
    assert "difference" not in out["net_income"]["comparisons"][0]
    # a label that says GAAP is GAAP wherever it sits
    rows = ["| Non-GAAP |", _row("GAAP net income", "100")]
    out = rvr.compare(["p:1"], [_blocks(rows)], "2026-06-30", lambda line, months: {"value": 1e8})
    assert out["net_income"]["verdict"] == "agrees"


@pytest.mark.parametrize("heading", ["Basic:", "Diluted:", "Earnings per share:",
                                     "Net income per share", "Weighted average shares:",
                                     "Percentage of Total Net Revenue:",
                                     "Summary of Stock-Based Compensation Expense:"])
def test_release_versus_report_rows_under_a_per_share_share_or_percent_heading_are_left_out(heading):
    """Carrier and ESCO print per-share rows under the net earnings label, and Dell
    prints percent of revenue rows under `Net income`; none is the dollar line, and the
    next ordinary heading puts the line back."""
    rows = [_row("Net income", "100"), f"| {heading} |", _row("Net income", "0.61"),
            "| Operating expenses: |", _row("Net earnings", "100")]
    out = rvr.compare(["p:1"], [_blocks(rows)], "2026-06-30", lambda line, months: {"value": 1e8})
    assert [c["release"]["cell"] for c in out["net_income"]["comparisons"]] == ["100", "100"]
    assert out["net_income"]["verdict"] == "agrees"
    assert [e["cell"] for e in out["net_income"]["excluded_rows"]] == ["0.61"]


def test_release_versus_report_a_percent_row_is_not_the_dollar_line():
    table = _blocks(["| Net income | 8.8 | % |  | 3.9 | % |", _row("Net income", "100")])
    out = rvr.compare(["p:1"], [table], "2026-06-30", lambda line, months: {"value": 1e8})
    assert [c["release"]["cell"] for c in out["net_income"]["comparisons"]] == ["100"]
    cell_percent = _blocks(["| Net income | $ | 8.8% |  | $ | 3.9% |"])
    out = rvr.compare(["p:1"], [cell_percent], "2026-06-30", lambda line, months: {"value": 1e8})
    assert out["net_income"]["comparisons"] == []
    assert out["net_income"]["excluded_rows"][0]["cell"] == "8.8%"


def test_release_versus_report_per_share_rows_stay_in_the_per_share_line():
    rows = ["| Earnings per share: |", _row("Diluted earnings per share", "6.34")]
    out = rvr.compare(["p:1"], [_blocks(rows)], "2026-06-30",
                      lambda line, months: {"value": 6.34})
    assert out["diluted_earnings_per_share"]["verdict"] == "agrees"


@pytest.mark.parametrize("other", ["block_not_identified", "report_fact_missing", "period_not_read"])
def test_release_versus_report_a_difference_outranks_the_other_flags_in_either_order(other):
    assert rvr.line_verdict(["differs", other]) == "differs"
    assert rvr.line_verdict([other, "differs"]) == "differs"
    assert rvr.line_verdict(["agrees", "differs", other]) == "differs"


@pytest.mark.parametrize("other", ["block_not_identified", "report_fact_missing", "period_not_read"])
def test_release_versus_report_each_flag_outranks_agrees_in_either_order(other):
    assert rvr.line_verdict(["agrees", other]) == other
    assert rvr.line_verdict([other, "agrees", "agrees"]) == other
    assert rvr.line_verdict([other]) == other


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


def test_release_versus_report_the_span_length_guard_never_compares_a_twelve_month_column_to_a_nine_month_year_to_date():
    """JCI's release prints a trailing-twelve-month column against a 10-Q whose year to
    date is nine months (273 days): the report side is missing, with the reason."""
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
    assert "missing" in read("pretax_income", 6)
    assert "missing" in read("pretax_income", 3)       # no quarter span on record
    annual = dict(periods, annual_trigger=True, current_to_date=("2025-07-01", "2026-06-30"))
    assert read.__closure__ is not None
    assert calculator.release_report_reader(Stub(), annual)("pretax_income", 12)["value"] == 7.0


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


def _planted(ticker: str, accession: str, plants: dict[str, tuple[str, str]]) -> dict:
    """The committed release with figures changed in named paragraphs (the paragraph
    number after `8k_2_02:`), each change the first occurrence of an exact string, read through
    the calculator against the real record."""
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
    return calculator.release_versus_report(record, periods, ticker=ticker, cutoff=cutoff,
                                            fixtures_root=calculator.cutoff_guard.FIXTURES,
                                            release=planted)["lines"]


def _in_table(entry: dict, number: str) -> list[dict]:
    return [c for c in entry["comparisons"]
            if c["release"]["paragraph_id"].endswith(f":8k_2_02:{number}")]


def test_release_versus_report_unplanted_committed_releases_have_no_difference():
    for ticker, accession in (("DELL", "0001571996-26-000046"), ("CARR", "0001783180-26-000032"),
                              ("CIEN", "0001628280-26-040767"), ("AAPL", "0000320193-26-000020")):
        lines = _planted(ticker, accession, {})
        for line, entry in lines.items():
            assert entry["verdict"] != "differs", (ticker, line)
            assert all(c["verdict"] != "differs" for c in entry.get("comparisons", [])), (ticker, line)


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


def test_release_versus_report_carriers_segment_tables_are_not_the_company_line():
    lines = _planted("CARR", "0001783180-26-000032", {})
    cells = {c["cell"] for c in lines["revenue"]["segment_cells_not_compared"]}
    assert {"3,372", "1,324", "917", "738"} <= cells
    assert lines["revenue"]["verdict"] != "differs"


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


def test_release_versus_report_net_earnings_before_the_noncontrolling_interest_is_held_to_profit_or_loss():
    """Carrier's statement prints `Net earnings (loss) | 541` (before the noncontrolling
    interest's 40) and `... attributable to common shareowners | 501`. The record's
    `NetIncomeLoss` is 501 and its `ProfitLoss` is 541, so the first agrees with the second
    fact and says so; the attributable row is held to `NetIncomeLoss` alone, and a plant of
    541 into the attributable row differs."""
    lines = _planted("CARR", "0001783180-26-000032", {})
    quarter = {c["release"]["label"]: c for c in _in_table(lines["net_income"], "84")
               if c["span_months"] == 3}
    assert quarter["Net earnings (loss)"]["verdict"] == "agrees"
    assert "noncontrolling" in quarter["Net earnings (loss)"]["agrees_with"]
    assert quarter["Net earnings (loss)"]["report"]["parts"]["0"]["tag"] == "ProfitLoss"
    assert quarter["Net earnings (loss) attributable to common shareowners"]["verdict"] == "agrees"
    assert "agrees_with" not in quarter["Net earnings (loss) attributable to common shareowners"]
    lines = _planted("CARR", "0001783180-26-000032", {
        "84": ("| Net earnings (loss) attributable to common shareowners |  | $ | 501 |",
               "| Net earnings (loss) attributable to common shareowners |  | $ | 541 |")})
    assert lines["net_income"]["verdict"] == "differs"


def test_release_versus_report_a_non_gaap_total_closes_the_block_its_heading_opened():
    """Dell's reconciliation prints GAAP `Operating income`, then `Non-GAAP adjustments:`
    and its rows, then `Non-GAAP operating income`, and then the next GAAP line `Net
    income`: the heading's block ends with the non-GAAP total, so the GAAP rows on either
    side are GAAP and the adjustments are not."""
    rows = [_row("Operating income", "5,385"), "| Non-GAAP adjustments: |",
            _row("Amortization of intangibles", "96"), _row("Non-GAAP operating income", "5,929"),
            _row("Net income", "4,133")]
    out = rvr.compare(["p:1"], [_blocks(rows)], "2026-06-30",
                      lambda line, months: {"value": {"operating_income": 5.385e9,
                                                      "net_income": 4.133e9}.get(line)}
                      if line != "net_income_with_noncontrolling" else {"missing": "none"})
    assert out["operating_income"]["verdict"] == "agrees"
    assert out["net_income"]["verdict"] == "agrees"
    assert "not_gaap" not in out["net_income"] and "not_gaap" not in out["operating_income"]
    # a GAAP row planted wrong after the total is still caught
    rows[-1] = _row("Net income", "4,233")
    out = rvr.compare(["p:1"], [_blocks(rows)], "2026-06-30",
                      lambda line, months: {"value": {"operating_income": 5.385e9,
                                                      "net_income": 4.133e9}.get(line)}
                      if line != "net_income_with_noncontrolling" else {"missing": "none"})
    assert out["net_income"]["verdict"] == "differs"
