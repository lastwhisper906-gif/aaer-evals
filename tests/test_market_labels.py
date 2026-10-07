"""The market labels, judged against market tables written down by hand.

Every table below is built here from closing prices written in the test, and
every abnormal return in it was worked by hand from those prices, in the
docstring beside it, with the form `docs/INPUT_SPEC.md` §4 states:

    abnormal return = raw return - beta x market return - sector return

and the reaction window as the sum of the abnormal returns of reaction days
zero, one and two. Beta is written down rather than estimated, because the 250
trading days it is estimated over are not in a market table: `src/market.py`
records the beta and not the days behind it. The label each test asserts is the
one the owner's decision of 2026-10-06 gives the sign by hand -- in the item's
direction `priced_in`, inside the band `not_priced`, against it
`opposite_direction` -- and none was read off the code's output.

The dates are a real calendar: 2026-04-24 and 2026-05-08 are Fridays, so each
window runs Friday, Monday, Tuesday.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from src import market_labels
from src.market_labels import MarketLabelError

FILING_DAYS = ["2026-05-08", "2026-05-11", "2026-05-12"]
EARNINGS_DAYS = ["2026-04-24", "2026-04-27", "2026-04-28"]

# Short interest, worked by hand. Shares outstanding 1,000,000,000. Three FINRA
# reports published inside the trailing two years: 30,000,000, 40,000,000 and
# 50,000,000 shares short, so the ratios are 0.03, 0.04 and 0.05 and their median
# is 0.04. The ratio on the day is the newest report published by then.
SHARES_OUTSTANDING = 1_000_000_000
NO_SHORT_INTEREST = {"short_interest_ratio": None,
                     "short_interest_two_year_median": None,
                     "short_interest_above_median": None}


def short_interest(shares_short: int, flag) -> dict:
    """The three columns, with the ratio and the median written as worked above."""
    ratio = {30_000_000: 0.03, 40_000_000: 0.04, 50_000_000: 0.05}[shares_short]
    return {"short_interest_ratio": ratio, "short_interest_two_year_median": 0.04,
            "short_interest_above_median": flag}


def rows(days: list[str], abnormal: list[float], kind: str, window_sum: float,
         short=NO_SHORT_INTEREST) -> list[dict]:
    return [{"ticker": "ZZZZ", "date": day, "abnormal_return": value, "window": kind,
             "reaction_window": window_sum, **short}
            for day, value in zip(days, abnormal)]


def table(*windows_and_rows, accepted: str | None = None, filing_date: str | None = None) -> dict:
    """A market table in the shape `src/market.py` writes, from hand-worked windows.

    Each window is accepted at nine in the morning of its day zero unless `accepted`
    says otherwise, so day zero is the acceptance day and the filing date is it."""
    windows, all_rows = [], []
    for kind, days, abnormal, window_sum, short in windows_and_rows:
        windows.append({"kind": kind, "day_zero": days[0], "days": days,
                        "accepted": accepted or f"{days[0]}T09:00:00-04:00",
                        "filing_date": filing_date or days[0],
                        "reaction_window": window_sum})
        all_rows += rows(days, abnormal, kind, window_sum, short)
    cutoff = max((row["date"] for row in all_rows), default=None)
    return {"ticker": "ZZZZ", "cutoff": cutoff, "windows": windows, "rows": all_rows}


def rose() -> dict:
    """The filing window moves up.

    Closes, 2026-05-07 then the three window days:
      ZZZZ   100.00  103.00  103.00  104.03   raw  +0.03, 0.00, +0.01
      market 400.00  404.00  404.00  404.00   raw  +0.01, 0.00,  0.00
      sector  50.00   50.00   50.00   50.00   raw   0.00, 0.00,  0.00
    beta 1.0, so the abnormal returns are
      0.03 - 1.0 x 0.01 - 0 = +0.02,  0 - 0 - 0 = 0.00,  0.01 - 0 - 0 = +0.01
    and the window is +0.02 + 0.00 + 0.01 = +0.03, three points above zero and
    outside a one-point band.
    """
    return table(("filing", FILING_DAYS, [0.02, 0.0, 0.01], 0.03, NO_SHORT_INTEREST))


def fell() -> dict:
    """The filing window moves down.

    Closes, 2026-05-07 then the three window days:
      ZZZZ   100.00   97.00   97.00   97.00   raw  -0.03, 0.00, 0.00
      market 400.00  400.00  400.00  400.00   raw   0.00, 0.00, 0.00
      sector  50.00   50.00   50.00   50.00   raw   0.00, 0.00, 0.00
    beta 1.0: abnormal returns -0.03, 0.00, 0.00; the window is -0.03.
    """
    return table(("filing", FILING_DAYS, [-0.03, 0.0, 0.0], -0.03, NO_SHORT_INTEREST))


def barely() -> dict:
    """The filing window barely moves.

    Closes, 2026-05-07 then the three window days:
      ZZZZ   100.00  100.50  100.50  100.50   raw  +0.005, 0.00, 0.00
      market 400.00  400.00  400.00  400.00   raw   0.00,  0.00, 0.00
      sector  50.00   50.00   50.00   50.00   raw   0.00,  0.00, 0.00
    beta 1.2, and the market did not move, so the abnormal returns are the raw
    returns: +0.005, 0.00, 0.00; the window is +0.005, half a point, inside a
    one-point band.
    """
    return table(("filing", FILING_DAYS, [0.005, 0.0, 0.0], 0.005, NO_SHORT_INTEREST))


def item(identifier: str, direction) -> dict:
    found = {"id": identifier, "what_changed": "x", "account": "a", "horizon": "h",
             "quote": "q", "paragraph_id": "p"}
    if direction is not None:
        found["expected_direction"] = direction
    return found


UP = "liquidity_and_capital_receivables_rising"
DOWN = "liquidity_and_capital_cash_falling"


def labelled(document: dict, identifier: str) -> list[str]:
    entry = next(one for one in document["items"] if one["upstream_item_id"] == identifier)
    return [one["label"] for one in entry["labels"]]


def labelled_numbers(found_table: dict, *items: dict) -> dict:
    return market_labels.labels({"report_numbers.md": list(items)}, found_table)


# --- each label ----------------------------------------------------------------

def test_a_move_in_the_items_direction_is_priced_in():
    """Window +0.03 (worked in `rose`), item points up: same sign, outside the band."""
    document = labelled_numbers(rose(), item(UP, "up"))
    assert labelled(document, UP) == ["priced_in"]


def test_a_move_against_the_items_direction_is_opposite_direction():
    """Window +0.03 against an item pointing down, and window -0.03 (worked in
    `fell`) against an item pointing up: the other sign, outside the band."""
    assert labelled(labelled_numbers(rose(), item(DOWN, "down")), DOWN) == ["opposite_direction"]
    assert labelled(labelled_numbers(fell(), item(UP, "up")), UP) == ["opposite_direction"]


def test_a_fall_is_priced_in_for_an_item_pointing_down():
    """Window -0.03, item points down: same sign."""
    assert labelled(labelled_numbers(fell(), item(DOWN, "down")), DOWN) == ["priced_in"]


def test_a_move_inside_the_band_is_not_priced_whichever_way_the_item_points():
    """Window +0.005 (worked in `barely`): half a point is inside a one-point band,
    so neither direction is read off it."""
    document = labelled_numbers(barely(), item(UP, "up"), item(DOWN, "down"))
    assert labelled(document, UP) == ["not_priced"]
    assert labelled(document, DOWN) == ["not_priced"]
    reason = document["items"][0]["labels"][0]["reason"]
    assert "band" in reason


def test_the_band_is_named_and_written_beside_the_labels():
    """The band is the module's named constant, and every document says which
    band it used and where that came from. A band of four points takes in the
    +0.03 of `rose`, so the same window is then inside it."""
    document = labelled_numbers(rose(), item(UP, "up"))
    assert document["near_zero_band"] == market_labels.NEAR_ZERO_BAND
    assert "default" in document["near_zero_band_source"]
    wider = market_labels.labels({"report_numbers.md": [item(UP, "up")]}, rose(), band=0.04)
    assert labelled(wider, UP) == ["not_priced"]


def test_each_window_is_labelled_on_its_own():
    """Two windows, never added together.

    Earnings release, closes 2026-04-23 then 04-24, 04-27, 04-28:
      ZZZZ   100.00   98.00   98.00   98.00   raw  -0.02, 0.00, 0.00
      market 400.00  400.00  400.00  400.00   raw   0.00, 0.00, 0.00
      sector  50.00   50.00   50.00   50.00   raw   0.00, 0.00, 0.00
    beta 1.0: abnormal returns -0.02, 0, 0; window -0.02. The filing window is
    `rose`'s +0.03. An item pointing up is opposite in the first and priced in
    the second, in the table's own order.
    """
    found = table(("earnings_release", EARNINGS_DAYS, [-0.02, 0.0, 0.0], -0.02,
                   NO_SHORT_INTEREST),
                  ("filing", FILING_DAYS, [0.02, 0.0, 0.01], 0.03, NO_SHORT_INTEREST))
    document = labelled_numbers(found, item(UP, "up"))
    entry = document["items"][0]
    assert [one["window"] for one in entry["labels"]] == ["earnings_release", "filing"]
    assert labelled(document, UP) == ["opposite_direction", "priced_in"]


# --- no window, no direction ---------------------------------------------------

def test_a_table_with_no_window_is_refused_and_an_item_with_none_is_not_priced():
    """A table with no filing window ties nothing to the run's filing and is
    refused. An item handed no window at all -- the case `item_labels` keeps for
    itself -- is not priced, with the reason."""
    found = {"ticker": "ZZZZ", "cutoff": None, "windows": [], "rows": []}
    with pytest.raises(MarketLabelError, match="no filing window"):
        labelled_numbers(found, item(UP, "up"))
    entry = market_labels.item_labels(item(UP, "up"), "report_numbers.md", [])
    assert entry["labels"] == [{"window": None, "filing_date": None, "abnormal_return": None,
                                "label": "not_priced",
                                "reason": "the market table records no reaction window"}]


def test_a_window_with_no_abnormal_return_is_not_priced():
    found = rose()
    found["windows"][0]["reaction_window"] = None
    document = labelled_numbers(found, item(UP, "up"))
    assert labelled(document, UP) == ["not_priced"]
    assert "no abnormal return" in document["items"][0]["labels"][0]["reason"]


@pytest.mark.parametrize("direction", ["none", None, "sideways"])
def test_an_item_with_no_direction_is_not_priced_with_the_reason(direction):
    """Window +0.03 is a move, but an item that points nowhere cannot be in its
    direction or against it."""
    document = labelled_numbers(rose(), item(UP, direction))
    assert labelled(document, UP) == ["not_priced"]
    assert "expected_direction" in document["items"][0]["labels"][0]["reason"]


# --- short interest, a separate field ------------------------------------------

def test_short_interest_above_its_median_is_true_and_the_label_does_not_move():
    """Newest report 50,000,000 shares short: ratio 0.05 against the median 0.04
    worked above, so above. The window is `fell`'s -0.03 against an item
    pointing up, and stays opposite: the field never changes a label."""
    found = table(("filing", FILING_DAYS, [-0.03, 0.0, 0.0], -0.03,
                   short_interest(50_000_000, True)))
    document = labelled_numbers(found, item(UP, "up"))
    assert document["windows"][0]["short_interest"] == {
        "date": "2026-05-08", "above_two_year_median": True,
        "ratio": 0.05, "two_year_median": 0.04}
    assert labelled(document, UP) == ["opposite_direction"]


def test_short_interest_below_its_median_is_false():
    """Newest report 30,000,000 shares short: ratio 0.03 against 0.04, not above."""
    found = table(("filing", FILING_DAYS, [0.02, 0.0, 0.01], 0.03,
                   short_interest(30_000_000, False)))
    short = labelled_numbers(found, item(UP, "up"))["windows"][0]["short_interest"]
    assert short["above_two_year_median"] is False


def test_short_interest_at_its_median_is_not_above_it():
    """Newest report 40,000,000: ratio 0.04, the median itself. "Above" is strict."""
    found = table(("filing", FILING_DAYS, [0.02, 0.0, 0.01], 0.03,
                   short_interest(40_000_000, False)))
    short = labelled_numbers(found, item(UP, "up"))["windows"][0]["short_interest"]
    assert short["above_two_year_median"] is False


def test_no_short_interest_series_is_written_missing_with_the_reason():
    document = labelled_numbers(rose(), item(UP, "up"))
    short = document["windows"][0]["short_interest"]
    assert "above_two_year_median" not in short
    assert "no short-interest series" in short["missing"]
    assert labelled(document, UP) == ["priced_in"]


def test_a_flag_that_contradicts_its_own_ratio_is_refused():
    """Ratio 0.03 under the median 0.04, with the flag written true."""
    found = table(("filing", FILING_DAYS, [0.02, 0.0, 0.01], 0.03,
                   short_interest(30_000_000, True)))
    with pytest.raises(MarketLabelError, match="above median"):
        labelled_numbers(found, item(UP, "up"))


# --- what the table must be ----------------------------------------------------

def test_a_window_that_is_not_the_sum_of_its_rows_is_refused():
    """`rose`'s rows sum to +0.03; a window written +0.05 over them is two answers."""
    found = rose()
    found["windows"][0]["reaction_window"] = 0.05
    with pytest.raises(MarketLabelError, match="not the sum"):
        labelled_numbers(found, item(UP, "up"))


def test_a_row_past_the_cutoff_is_refused():
    found = rose()
    found["rows"].append(dict(found["rows"][-1], date="2026-05-13"))
    with pytest.raises(MarketLabelError, match="past its cutoff"):
        labelled_numbers(found, item(UP, "up"))


def test_an_item_with_no_id_is_counted_and_not_labelled():
    document = labelled_numbers(rose(), {"expected_direction": "up"}, item(UP, "up"))
    assert [one["upstream_item_id"] for one in document["items"]] == [UP]
    assert document["not_labelled"] == [{"report": "report_numbers.md",
                                         "reason": "the item carries no id to cite"}]


def test_both_reader_reports_are_labelled_and_each_item_is_named_versus_market():
    document = market_labels.labels(
        {"report_numbers.md": [item(UP, "up")],
         "report_notes_text.md": [item(DOWN, "down")]}, rose())
    assert [(one["report"], one["id"]) for one in document["items"]] == [
        ("report_numbers.md", f"{UP}_versus_market"),
        ("report_notes_text.md", f"{DOWN}_versus_market")]
    assert labelled(document, DOWN) == ["opposite_direction"]


# --- the run directory ----------------------------------------------------------

def fenced(*items: dict) -> str:
    return "".join(f"```json\n{json.dumps(one)}\n```\n" for one in items)


GATE_RAN_NOTHING_DROPPED = {"cutoff": "2026-05-08", "dropped_items": []}


def plant(tmp_path: Path, *, market: dict | None,
          manifest: dict | None = GATE_RAN_NOTHING_DROPPED) -> Path:
    """A run directory: the two reader reports, the market table when given, and
    the manifest the quote gate leaves -- `dropped_items` -- unless `manifest` is
    None, which plants a run with no manifest at all."""
    run = tmp_path / "ZZZZ" / "0000000000-26-000001"
    run.mkdir(parents=True)
    (run / "report_numbers.md").write_text(fenced(item(UP, "up")), encoding="utf-8")
    (run / "report_notes_text.md").write_text(fenced(item(DOWN, "down")), encoding="utf-8")
    if market is not None:
        (run / "input_market.json").write_text(json.dumps(market), encoding="utf-8")
    if manifest is not None:
        (run / "input_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    return run


def test_with_no_market_table_nothing_is_written(tmp_path, capsys):
    run = plant(tmp_path, market=None)
    result = market_labels.write(run)
    assert result["written"] is False
    assert "no input_market.json" in result["reason"]
    assert not (run / "market_labels.json").exists()
    assert market_labels.main(["--run", str(run)]) == 0
    assert "no market table" in capsys.readouterr().out
    assert not (run / "market_labels.json").exists()


def test_with_a_market_table_the_labels_are_written_once(tmp_path):
    """The reports' items, against `rose`'s +0.03: up priced in, down opposite."""
    run = plant(tmp_path, market=rose())
    result = market_labels.write(run)
    assert result == {"written": True, "path": str(run / "market_labels.json"), "items": 2}
    written = json.loads((run / "market_labels.json").read_text(encoding="utf-8"))
    assert labelled(written, UP) == ["priced_in"]
    assert labelled(written, DOWN) == ["opposite_direction"]
    assert market_labels.write(run) == result          # the same bytes again
    (run / "market_labels.json").write_text("{}\n", encoding="utf-8")
    with pytest.raises(MarketLabelError, match="append-only"):
        market_labels.write(run)


def test_the_command_reports_a_run_it_cannot_label(tmp_path, capsys):
    run = plant(tmp_path, market=rose())
    (run / "report_notes_text.md").unlink()
    assert market_labels.main(["--run", str(run)]) == market_labels.BAD_INPUT
    assert "report_notes_text.md" in capsys.readouterr().err
    assert market_labels.main(["--run", str(tmp_path / "nowhere")]) == market_labels.BAD_INPUT


# --- the gate's drop list, and the run's own cutoff ------------------------------------

def test_an_item_the_quote_gate_dropped_is_set_aside_not_labelled():
    """A drop is matched by (report, id), as the gate records it: `gone` dropped from
    the numbers report is set aside; the same id dropped from the notes report is
    a different item, and `gone` in the numbers report then stands."""
    reports = {"report_numbers.md": [item(UP, "up"), item("gone", "up")]}
    document = market_labels.labels(reports, rose(), dropped={("report_numbers.md", "gone")})
    assert [one["upstream_item_id"] for one in document["items"]] == [UP]
    assert document["not_labelled"] == [{"report": "report_numbers.md", "id": "gone",
                                         "reason": "dropped by the quote gate; nothing cites it"}]
    assert document["gate_dropped"] == 1
    other = market_labels.labels(reports, rose(), dropped={("report_notes_text.md", "gone")})
    assert [one["upstream_item_id"] for one in other["items"]] == [UP, "gone"]


def test_a_table_with_no_cutoff_is_refused():
    found = rose()
    found["cutoff"] = None
    with pytest.raises(MarketLabelError, match="names no cutoff"):
        labelled_numbers(found, item(UP, "up"))


def test_a_window_is_held_to_its_own_acceptance_stamp():
    """Rows 2026-05-08, 05-11 and 05-12. Accepted Friday the 8th at 09:00: day zero
    is the 8th and the window is the 8th, 11th and 12th. Accepted the 8th at 16:30,
    after the close: day zero is the next trading day, Monday the 11th, so a window
    that starts on the 8th is not that acceptance's window."""
    good = rose()
    market_labels.labels({"report_numbers.md": [item(UP, "up")]}, good)
    wrong = table(("filing", FILING_DAYS, [0.02, 0.01, 0.0], 0.03, NO_SHORT_INTEREST),
                  accepted="2026-05-08T16:30:00-04:00")
    # day zero moves to the 11th, and day two is then the 13th, which has no row
    with pytest.raises(MarketLabelError, match="no row for 2026-05-13"):
        market_labels.labels({"report_numbers.md": []}, wrong)
    shifted = table(("filing", ["2026-05-11", "2026-05-12", "2026-05-13"], [0.02, 0.01, 0.0],
                     0.03, NO_SHORT_INTEREST), accepted="2026-05-08T16:30:00-04:00")
    shifted["rows"].insert(0, dict(shifted["rows"][0], date="2026-05-08", abnormal_return=0.5))
    shifted["windows"][0]["days"] = ["2026-05-08", "2026-05-11", "2026-05-12"]
    shifted["windows"][0]["day_zero"] = "2026-05-08"
    with pytest.raises(MarketLabelError, match="not reaction days zero to two"):
        market_labels.labels({"report_numbers.md": []}, shifted)


def test_a_window_with_no_acceptance_stamp_is_refused():
    found = rose()
    del found["windows"][0]["accepted"]
    with pytest.raises(MarketLabelError, match="no acceptance stamp"):
        market_labels.labels({"report_numbers.md": []}, found)


def test_the_filing_window_is_held_to_the_runs_cutoff():
    """Filed on the 8th, accepted the 8th at 09:00: the run's cutoff is the 8th.
    A run whose cutoff is the 7th is some other filing."""
    found = rose()
    market_labels.labels({"report_numbers.md": [item(UP, "up")]}, found, run_cutoff="2026-05-08")
    with pytest.raises(MarketLabelError, match="some other filing"):
        market_labels.labels({"report_numbers.md": []}, found, run_cutoff="2026-05-07")


def test_an_after_close_acceptance_may_carry_the_next_days_filing_date():
    """Accepted Thursday the 7th at 18:00, past EDGAR's half past five: EDGAR may
    date the filing the 7th or the 8th, and day zero is the next trading row, the
    8th, either way."""
    for filed in ("2026-05-07", "2026-05-08"):
        found = table(("filing", FILING_DAYS, [0.02, 0.01, 0.0], 0.03, NO_SHORT_INTEREST),
                      accepted="2026-05-07T18:00:00-04:00", filing_date=filed)
        market_labels.labels({"report_numbers.md": []}, found, run_cutoff=filed)
    found = table(("filing", FILING_DAYS, [0.02, 0.01, 0.0], 0.03, NO_SHORT_INTEREST),
                  accepted="2026-05-07T18:00:00-04:00", filing_date="2026-05-06")
    with pytest.raises(MarketLabelError, match="not one EDGAR puts"):
        market_labels.labels({"report_numbers.md": []}, found)


def test_a_table_whose_rows_end_before_reaction_day_two_is_refused():
    """Cut the table off at day one, the 11th: day two, the 12th, has no row."""
    found = rose()
    found["cutoff"] = "2026-05-11"
    found["rows"] = [row for row in found["rows"] if row["date"] <= "2026-05-11"]
    with pytest.raises(MarketLabelError, match="no row for 2026-05-12"):
        market_labels.labels({"report_numbers.md": []}, found)


def test_the_tables_cutoff_is_day_two_of_its_latest_window():
    """`rose`'s rows end on day two, the 12th, and its cutoff is the 12th: it stands.
    The same rows under a cutoff of the 13th hold no row past the cutoff and reach
    day two, so only the cutoff itself is wrong -- it is not the latest window's
    day two -- and that is what is refused."""
    market_labels.labels({"report_numbers.md": []}, rose())
    found = rose()
    found["cutoff"] = "2026-05-13"
    with pytest.raises(MarketLabelError, match="not reaction day two of its latest window"):
        market_labels.labels({"report_numbers.md": []}, found)


# --- the rows are not the calendar: each window is held to the exchange calendar ------

def test_a_table_missing_the_row_for_its_own_day_zero_is_refused():
    """Accepted Friday the 8th at 09:00, before the close: the 8th is day zero and
    has to be a row. A table with rows for the 11th, 12th and 13th only would read
    its own day zero as the 11th and pass one trading day late; it is refused.
    `rose`, whose rows start on the 8th, stands."""
    market_labels.labels({"report_numbers.md": []}, rose())
    late = table(("filing", ["2026-05-11", "2026-05-12", "2026-05-13"], [0.02, 0.0, 0.01],
                  0.03, NO_SHORT_INTEREST),
                 accepted="2026-05-08T09:00:00-04:00", filing_date="2026-05-08")
    with pytest.raises(MarketLabelError, match="no row for 2026-05-08"):
        market_labels.labels({"report_numbers.md": []}, late)


def test_a_skipped_trading_day_after_the_close_is_refused():
    """Accepted Thursday the 7th at 16:35, after the close: day zero is Friday the
    8th, a trading day. A table with rows for Monday the 11th on would read its
    own day zero as the 11th and pass one trading day late; the exchange calendar
    says the 8th was open, and the table has no row for it."""
    friday_missing = table(("filing", ["2026-05-11", "2026-05-12", "2026-05-13"],
                            [0.02, 0.0, 0.01], 0.03, NO_SHORT_INTEREST),
                           accepted="2026-05-07T16:35:00-04:00", filing_date="2026-05-07")
    with pytest.raises(MarketLabelError, match="no row for 2026-05-08"):
        market_labels.labels({"report_numbers.md": []}, friday_missing)


def test_a_window_over_an_exchange_holiday_stands():
    """Accepted Friday 2026-05-22 at 16:35: Monday the 25th is Memorial Day, so day
    zero is Tuesday the 26th and the window runs the 26th, 27th and 28th. Accepted
    Thursday 2026-04-02 at 16:35: Friday the 3rd is Good Friday (Easter the 5th),
    so day zero is Monday the 6th. Both windows are `rose`'s +0.03 by the same
    arithmetic on other days, and an item pointing up is priced in. EDGAR's own
    close is half past five, so each filing date is the acceptance day."""
    memorial = table(("filing", ["2026-05-26", "2026-05-27", "2026-05-28"], [0.02, 0.0, 0.01],
                      0.03, NO_SHORT_INTEREST),
                     accepted="2026-05-22T16:35:00-04:00", filing_date="2026-05-22")
    document = market_labels.labels({"report_numbers.md": [item(UP, "up")]}, memorial,
                                    run_cutoff="2026-05-22")
    assert document["windows"][0]["day_zero"] == "2026-05-26"
    assert labelled(document, UP) == ["priced_in"]
    good_friday = table(("filing", ["2026-04-06", "2026-04-07", "2026-04-08"], [0.02, 0.0, 0.01],
                         0.03, NO_SHORT_INTEREST),
                        accepted="2026-04-02T16:35:00-04:00", filing_date="2026-04-02")
    document = market_labels.labels({"report_numbers.md": [item(UP, "up")]}, good_friday,
                                    run_cutoff="2026-04-02")
    assert document["windows"][0]["day_zero"] == "2026-04-06"
    assert labelled(document, UP) == ["priced_in"]


def test_a_row_on_a_day_the_exchange_was_closed_is_refused():
    """A row dated Saturday the 9th, inside the cutoff, is not a trading day."""
    found = rose()
    found["rows"].append(dict(found["rows"][0], date="2026-05-09"))
    with pytest.raises(MarketLabelError, match="2026-05-09 is not a trading day"):
        market_labels.labels({"report_numbers.md": []}, found)


# --- every window but the filing's is an earlier filing's -------------------------------

def test_a_window_for_a_filing_after_the_runs_cutoff_is_refused():
    """The earnings release of the 24th of April, a fortnight before the filing of
    the 8th of May, stands under the run's cutoff of the 8th. A release dated the
    15th of May is after the cutoff: not an input, and it would otherwise carry the
    table's cutoff and the late-row limit out to the 19th."""
    earlier = table(("earnings_release", EARNINGS_DAYS, [-0.02, 0.0, 0.0], -0.02,
                     NO_SHORT_INTEREST),
                    ("filing", FILING_DAYS, [0.02, 0.0, 0.01], 0.03, NO_SHORT_INTEREST))
    document = market_labels.labels({"report_numbers.md": [item(UP, "up")]}, earlier,
                                    run_cutoff="2026-05-08")
    assert [one["window"] for one in document["windows"]] == ["earnings_release", "filing"]
    later = table(("filing", FILING_DAYS, [0.02, 0.0, 0.01], 0.03, NO_SHORT_INTEREST),
                  ("earnings_release", ["2026-05-15", "2026-05-18", "2026-05-19"],
                   [-0.02, 0.0, 0.0], -0.02, NO_SHORT_INTEREST))
    assert later["cutoff"] == "2026-05-19"
    with pytest.raises(MarketLabelError, match="after the run's cutoff 2026-05-08"):
        market_labels.labels({"report_numbers.md": []}, later, run_cutoff="2026-05-08")


# --- the gate's record is required ------------------------------------------------------

def test_a_manifest_with_an_empty_drop_list_labels_and_one_without_the_key_refuses(tmp_path):
    with_record = plant(tmp_path / "ran", market=rose(),
                        manifest={"cutoff": "2026-05-08", "dropped_items": []})
    assert market_labels.write(with_record)["written"] is True
    no_key = plant(tmp_path / "no_key", market=rose(), manifest={"cutoff": "2026-05-08"})
    with pytest.raises(MarketLabelError, match="no dropped_items list"):
        market_labels.write(no_key)
    assert not (no_key / "market_labels.json").exists()


def test_a_manifest_with_no_cutoff_is_refused_and_the_command_says_so(tmp_path, capsys):
    """Without the run's cutoff nothing ties the filing window to this run's filing
    or holds its other windows before it, so the labeller refuses, as it refuses a
    missing drop list. The same manifest with its cutoff labels."""
    run = plant(tmp_path / "none", market=rose(), manifest={"dropped_items": []})
    with pytest.raises(MarketLabelError, match="names no cutoff"):
        market_labels.write(run)
    assert market_labels.main(["--run", str(run)]) == market_labels.BAD_INPUT
    assert "names no cutoff" in capsys.readouterr().err
    assert not (run / "market_labels.json").exists()
    with_cutoff = plant(tmp_path / "dated", market=rose(),
                        manifest={"cutoff": "2026-05-08", "dropped_items": []})
    assert market_labels.write(with_cutoff)["written"] is True


def test_a_run_with_no_manifest_is_refused_and_the_command_says_so(tmp_path, capsys):
    run = plant(tmp_path, market=rose(), manifest=None)
    with pytest.raises(MarketLabelError, match="no input_manifest.json"):
        market_labels.write(run)
    assert market_labels.main(["--run", str(run)]) == market_labels.BAD_INPUT
    assert "no record that the quote gate ran" in capsys.readouterr().err
    assert not (run / "market_labels.json").exists()


def test_a_dropped_item_in_the_manifest_is_set_aside_by_write(tmp_path):
    run = plant(tmp_path, market=rose(),
                manifest={"cutoff": "2026-05-08",
                          "dropped_items": [{"report": "report_notes_text.md", "item_id": DOWN,
                                             "reason": "quote not found"}]})
    assert market_labels.write(run)["items"] == 1
    written = json.loads((run / "market_labels.json").read_text(encoding="utf-8"))
    assert [one["upstream_item_id"] for one in written["items"]] == [UP]
    assert written["not_labelled"][0]["id"] == DOWN
    assert written["gate_dropped"] == 1
    assert market_labels.check(run) == {"checked": True, "items": 1}


def test_a_drop_row_that_names_no_report_is_refused(tmp_path):
    run = plant(tmp_path, market=rose(),
                manifest={"cutoff": "2026-05-08",
                          "dropped_items": [{"item_id": DOWN, "reason": "quote not found"}]})
    with pytest.raises(MarketLabelError, match="names no report"):
        market_labels.write(run)


# --- a blank id is no id, and a drop with no id is still a drop ---------------------------

def test_an_item_whose_id_is_blank_is_the_gates_drop_and_never_cited(tmp_path):
    """The gate's `item_id` strips, so an id of two spaces is none; the gate drops
    that item with `item_id: null` and its report. The run-root copy still holds
    it, and it is set aside, counted, and never an `upstream_item_id`."""
    run = plant(tmp_path, market=rose(),
                manifest={"cutoff": "2026-05-08",
                          "dropped_items": [{"report": "report_numbers.md", "item_id": None,
                                             "reason": "the item carries no id"}]})
    (run / "report_numbers.md").write_text(fenced(item(UP, "up"), item("  ", "up")),
                                           encoding="utf-8")
    assert market_labels.write(run)["items"] == 2
    written = json.loads((run / "market_labels.json").read_text(encoding="utf-8"))
    assert [one["upstream_item_id"] for one in written["items"]] == [UP, DOWN]
    assert "  " not in [one["upstream_item_id"] for one in written["items"]]
    assert written["not_labelled"] == [{"report": "report_numbers.md",
                                        "reason": market_labels.DROPPED_NO_ID}]
    assert written["gate_dropped"] == 1
    assert market_labels.check(run) == {"checked": True, "items": 2}


def test_an_item_with_a_blank_id_the_gate_did_not_record_is_still_not_cited():
    document = market_labels.labels({"report_numbers.md": [item("  ", "up"), item(UP, "up")]},
                                    rose())
    assert [one["upstream_item_id"] for one in document["items"]] == [UP]
    assert document["not_labelled"] == [{"report": "report_numbers.md",
                                         "reason": market_labels.NO_ID}]


# --- the labels file is re-checked after it is written ------------------------------------

def test_a_labels_file_citing_standing_items_passes_the_check(tmp_path):
    run = plant(tmp_path, market=rose())
    market_labels.write(run)
    assert market_labels.check(run) == {"checked": True, "items": 2}


def test_a_labels_file_citing_a_dropped_item_fails_the_check(tmp_path):
    """Written clean, then the drop list grows to name DOWN: the file on record now
    cites an item that does not stand, and the check names the label."""
    run = plant(tmp_path, market=rose())
    market_labels.write(run)
    (run / "input_manifest.json").write_text(json.dumps(
        {"cutoff": "2026-05-08",
         "dropped_items": [{"report": "report_notes_text.md", "item_id": DOWN,
                            "reason": "quote not found"}]}), encoding="utf-8")
    with pytest.raises(MarketLabelError, match=f"{DOWN}_versus_market: cites") as caught:
        market_labels.check(run)
    assert "not a standing item of report_notes_text.md" in str(caught.value)


def test_a_labels_file_citing_an_id_from_the_other_report_fails_the_check(tmp_path):
    """UP stands in the numbers report; a label that says it is the notes report's
    cites an item that report does not hold."""
    run = plant(tmp_path, market=rose())
    market_labels.write(run)
    document = json.loads((run / "market_labels.json").read_text(encoding="utf-8"))
    entry = next(one for one in document["items"] if one["upstream_item_id"] == UP)
    entry["report"] = "report_notes_text.md"
    (run / "market_labels.json").write_text(json.dumps(document), encoding="utf-8")
    with pytest.raises(MarketLabelError, match=f"{UP}_versus_market: cites '{UP}'"):
        market_labels.check(run)


def test_the_check_refuses_a_table_with_no_labels_and_passes_a_run_with_no_table(tmp_path):
    with_table = plant(tmp_path / "table", market=rose())
    with pytest.raises(MarketLabelError, match="no market_labels.json"):
        market_labels.check(with_table)
    without = plant(tmp_path / "none", market=None)
    assert market_labels.check(without)["checked"] is False


# --- a filing window, and known kinds ----------------------------------------------------

def test_a_table_with_only_an_earnings_release_window_is_refused():
    found = table(("earnings_release", EARNINGS_DAYS, [-0.02, 0.0, 0.0], -0.02,
                   NO_SHORT_INTEREST))
    with pytest.raises(MarketLabelError, match="no filing window"):
        market_labels.labels({"report_numbers.md": []}, found, run_cutoff="2026-05-08")


def test_a_window_of_a_kind_the_market_module_never_writes_is_refused():
    found = table(("filling", FILING_DAYS, [0.02, 0.0, 0.01], 0.03, NO_SHORT_INTEREST))
    with pytest.raises(MarketLabelError, match="'filling' is not one the market module writes"):
        market_labels.labels({"report_numbers.md": []}, found)
    market_labels.labels({"report_numbers.md": []}, rose())   # the usual table stands


# --- an early close -------------------------------------------------------------------------

def test_after_a_one_oclock_close_an_afternoon_acceptance_takes_the_next_trading_day():
    """Friday 2026-11-27, the day after Thanksgiving, closes at one. A filing
    accepted at 14:00 that day came after the close, so day zero is Monday the
    30th and the window runs the 30th, the 1st and the 2nd of December; a window
    that starts on the 27th is not that acceptance's. EDGAR's own close is half
    past five, so the filing date is the 27th."""
    friday = table(("filing", ["2026-11-27", "2026-11-30", "2026-12-01"], [0.02, 0.0, 0.01],
                    0.03, NO_SHORT_INTEREST),
                   accepted="2026-11-27T14:00:00-05:00", filing_date="2026-11-27")
    with pytest.raises(MarketLabelError, match="no row for 2026-12-02"):
        market_labels.labels({"report_numbers.md": []}, friday, run_cutoff="2026-11-27")
    monday = table(("filing", ["2026-11-30", "2026-12-01", "2026-12-02"], [0.02, 0.0, 0.01],
                    0.03, NO_SHORT_INTEREST),
                   accepted="2026-11-27T14:00:00-05:00", filing_date="2026-11-27")
    document = market_labels.labels({"report_numbers.md": [item(UP, "up")]}, monday,
                                    run_cutoff="2026-11-27")
    assert document["windows"][0]["day_zero"] == "2026-11-30"
    # the same hour on an ordinary Friday is before the close, and day zero is that day
    ordinary = table(("filing", FILING_DAYS, [0.02, 0.0, 0.01], 0.03, NO_SHORT_INTEREST),
                     accepted="2026-05-08T14:00:00-04:00")
    assert market_labels.labels({"report_numbers.md": []}, ordinary)["windows"][0][
        "day_zero"] == "2026-05-08"


# --- the check reads each label, not only its citation -------------------------------------

def test_an_edited_label_word_window_or_return_fails_the_check_and_the_written_file_passes(
        tmp_path):
    run = plant(tmp_path, market=rose())
    market_labels.write(run)
    assert market_labels.check(run) == {"checked": True, "items": 2}
    written = (run / "market_labels.json").read_text(encoding="utf-8")

    def edited(change) -> str:
        document = json.loads(written)
        change(next(one for one in document["items"] if one["upstream_item_id"] == UP))
        (run / "market_labels.json").write_text(json.dumps(document), encoding="utf-8")
        with pytest.raises(MarketLabelError) as caught:
            market_labels.check(run)
        return str(caught.value)

    def word(entry):
        entry["labels"][0]["label"] = "priced"
    assert "'priced' is not one of priced_in, not_priced, opposite_direction" in edited(word)

    def window(entry):
        entry["labels"][0]["window"] = "earnings_release"
    assert ("the earnings_release window of 2026-05-08 is not one the market table records"
            in edited(window))

    def moved(entry):
        entry["labels"][0]["abnormal_return"] = -0.03
    assert "written -0.03, and the market table records 0.03" in edited(moved)


# --- every other window is an earlier filing's, by the instant it was accepted ----------

def test_a_window_accepted_later_on_the_day_of_the_filing_is_refused_and_the_day_before_stands():
    """The 10-Q accepted Friday the 8th at 09:00 and an 8-K accepted the same day at
    16:30: the same filing date, but the 8-K is the later filing, and its window
    would carry the table's cutoff a trading day past the 10-Q's day two. The
    same 8-K accepted Thursday the 7th at 16:30 is the earlier filing and stands."""
    same_day = table(("filing", FILING_DAYS, [0.02, 0.0, 0.01], 0.03, NO_SHORT_INTEREST))
    same_day["windows"].append({"kind": "earnings_release", "filing_date": "2026-05-08",
                                "accepted": "2026-05-08T16:30:00-04:00", "day_zero": "2026-05-11",
                                "days": ["2026-05-11", "2026-05-12", "2026-05-13"],
                                "reaction_window": -0.02})
    same_day["rows"] += rows(["2026-05-13"], [-0.03], "earnings_release", -0.02)
    same_day["rows"][1]["abnormal_return"] = 0.0     # the 11th: shared by both windows
    same_day["rows"][2]["abnormal_return"] = 0.01    # the 12th
    same_day["cutoff"] = "2026-05-13"
    # the sums: filing 0.02 + 0.0 + 0.01 = 0.03; earnings 0.0 + 0.01 - 0.03 = -0.02
    with pytest.raises(MarketLabelError, match="accepted at 2026-05-08T16:30:00-04:00, after "
                                               "the filing at 2026-05-08T09:00:00-04:00"):
        market_labels.labels({"report_numbers.md": []}, same_day, run_cutoff="2026-05-08")
    day_before = table(("earnings_release", ["2026-05-08", "2026-05-11", "2026-05-12"],
                        [0.02, 0.0, 0.01], 0.03, NO_SHORT_INTEREST),
                       accepted="2026-05-07T16:30:00-04:00", filing_date="2026-05-07")
    day_before["windows"].append({"kind": "filing", "filing_date": "2026-05-08",
                                  "accepted": "2026-05-08T09:00:00-04:00",
                                  "day_zero": "2026-05-08", "days": FILING_DAYS,
                                  "reaction_window": 0.03})
    document = market_labels.labels({"report_numbers.md": [item(UP, "up")]}, day_before,
                                    run_cutoff="2026-05-08")
    assert [(one["window"], one["filing_date"]) for one in document["windows"]] == [
        ("earnings_release", "2026-05-07"), ("filing", "2026-05-08")]


# --- the check recomputes every label and counts every entry ------------------------------

def test_a_flipped_label_word_fails_the_check(tmp_path):
    """UP against `rose`'s +0.03 is priced_in; written opposite_direction, the word
    recomputes from the item's direction, the window's return and the band."""
    run = plant(tmp_path, market=rose())
    market_labels.write(run)
    document = json.loads((run / "market_labels.json").read_text(encoding="utf-8"))
    entry = next(one for one in document["items"] if one["upstream_item_id"] == UP)
    entry["labels"][0]["label"] = "opposite_direction"
    (run / "market_labels.json").write_text(json.dumps(document), encoding="utf-8")
    with pytest.raises(MarketLabelError, match="label opposite_direction recomputes as priced_in"):
        market_labels.check(run)


def test_a_dropped_entry_and_an_extra_entry_each_fail_the_check(tmp_path):
    run = plant(tmp_path, market=rose())
    market_labels.write(run)
    written = (run / "market_labels.json").read_text(encoding="utf-8")
    document = json.loads(written)
    document["items"] = [one for one in document["items"] if one["upstream_item_id"] != DOWN]
    (run / "market_labels.json").write_text(json.dumps(document), encoding="utf-8")
    with pytest.raises(MarketLabelError, match=f"{DOWN}_versus_market: no entry, and {DOWN} "
                                               "stands in report_notes_text.md"):
        market_labels.check(run)
    document = json.loads(written)
    document["items"].append(dict(document["items"][0]))
    (run / "market_labels.json").write_text(json.dumps(document), encoding="utf-8")
    with pytest.raises(MarketLabelError, match=f"{UP}_versus_market: 2 entries for one item"):
        market_labels.check(run)
    document = json.loads(written)
    document["items"][0]["labels"].append(dict(document["items"][0]["labels"][0]))
    (run / "market_labels.json").write_text(json.dumps(document), encoding="utf-8")
    with pytest.raises(MarketLabelError, match="one label per recorded window"):
        market_labels.check(run)
    (run / "market_labels.json").write_text(written, encoding="utf-8")
    assert market_labels.check(run) == {"checked": True, "items": 2}


def test_two_windows_of_one_kind_with_different_filing_dates_are_both_kept(tmp_path):
    """Two earnings releases before the filing: the 24th of April (-0.02, worked in
    `test_each_window_is_labelled_on_its_own`) and Friday the 1st of May, closes
    100.00 then 102.00, 102.00, 102.00 against a flat market and sector, beta
    1.0: +0.02, 0, 0, a window of +0.02. Both are labelled, keyed by their filing
    dates, and the file passes its check with three labels per item."""
    found = table(("earnings_release", EARNINGS_DAYS, [-0.02, 0.0, 0.0], -0.02,
                   NO_SHORT_INTEREST),
                  ("earnings_release", ["2026-05-01", "2026-05-04", "2026-05-05"],
                   [0.02, 0.0, 0.0], 0.02, NO_SHORT_INTEREST),
                  ("filing", FILING_DAYS, [0.02, 0.0, 0.01], 0.03, NO_SHORT_INTEREST))
    run = plant(tmp_path, market=found)
    assert market_labels.write(run)["items"] == 2
    written = json.loads((run / "market_labels.json").read_text(encoding="utf-8"))
    assert [(one["window"], one["filing_date"]) for one in written["windows"]] == [
        ("earnings_release", "2026-04-24"), ("earnings_release", "2026-05-01"),
        ("filing", "2026-05-08")]
    assert labelled(written, UP) == ["opposite_direction", "priced_in", "priced_in"]
    assert market_labels.check(run) == {"checked": True, "items": 2}


# --- the count of the drop list is the count of its rows -----------------------------------

def test_two_id_less_drops_from_one_report_count_two_and_the_file_passes(tmp_path):
    """Two items the gate found no id on, both dropped from the numbers report: one
    (report, None) pair, two rows, and `gate_dropped` counts the rows. The check
    holds the count to the manifest's list, so a file saying one is refused."""
    run = plant(tmp_path, market=rose(),
                manifest={"cutoff": "2026-05-08",
                          "dropped_items": [{"report": "report_numbers.md", "item_id": None,
                                             "reason": "the item carries no id"},
                                            {"report": "report_numbers.md", "item_id": None,
                                             "reason": "the item carries no id"}]})
    (run / "report_numbers.md").write_text(
        fenced(item(UP, "up"), item("  ", "up"), item("", "down")), encoding="utf-8")
    market_labels.write(run)
    written = (run / "market_labels.json").read_text(encoding="utf-8")
    document = json.loads(written)
    assert document["gate_dropped"] == 2
    assert [one["reason"] for one in document["not_labelled"]] == [
        market_labels.DROPPED_NO_ID, market_labels.DROPPED_NO_ID]
    assert market_labels.check(run)["checked"] is True
    document["gate_dropped"] = 1
    (run / "market_labels.json").write_text(json.dumps(document), encoding="utf-8")
    with pytest.raises(MarketLabelError, match="gate_dropped is written 1, and the manifest's "
                                               "drop list holds 2 rows"):
        market_labels.check(run)


# --- the windows block is re-made from the table on re-check -----------------------------

def test_an_edited_window_or_short_interest_fails_the_check_and_the_written_file_passes(
        tmp_path):
    """Short interest 50,000,000 against the median worked above: above is True. The
    written file passes; its `days` edited to end a day early, or its
    `above_two_year_median` flipped, is not what the table gives."""
    found = table(("filing", FILING_DAYS, [0.02, 0.0, 0.01], 0.03,
                   short_interest(50_000_000, True)))
    run = plant(tmp_path, market=found)
    market_labels.write(run)
    assert market_labels.check(run) == {"checked": True, "items": 2}
    written = (run / "market_labels.json").read_text(encoding="utf-8")

    def edited(change) -> str:
        document = json.loads(written)
        change(document["windows"][0])
        (run / "market_labels.json").write_text(json.dumps(document), encoding="utf-8")
        with pytest.raises(MarketLabelError) as caught:
            market_labels.check(run)
        return str(caught.value)

    def days(window):
        window["days"] = ["2026-05-08", "2026-05-11"]
    assert ("the filing window of 2026-05-08: days is written ['2026-05-08', '2026-05-11'], "
            "and the table gives ['2026-05-08', '2026-05-11', '2026-05-12']" in edited(days))

    def flag(window):
        window["short_interest"]["above_two_year_median"] = False
    assert "the filing window of 2026-05-08: short_interest is written" in edited(flag)

    (run / "market_labels.json").write_text(written, encoding="utf-8")
    assert market_labels.check(run) == {"checked": True, "items": 2}
