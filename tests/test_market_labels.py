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

def test_a_table_with_no_window_labels_every_item_not_priced():
    found = {"ticker": "ZZZZ", "cutoff": None, "windows": [], "rows": []}
    document = labelled_numbers(found, item(UP, "up"))
    entry = document["items"][0]
    assert entry["labels"] == [{"window": None, "abnormal_return": None,
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
    document = market_labels.labels({"report_numbers.md": [item(UP, "up"), item("gone", "up")]},
                                    rose(), dropped={"gone"})
    assert [one["upstream_item_id"] for one in document["items"]] == [UP]
    assert document["not_labelled"] == [{"report": "report_numbers.md", "id": "gone",
                                         "reason": "dropped by the quote gate; nothing cites it"}]


def test_a_table_with_no_cutoff_is_refused():
    found = rose()
    found["cutoff"] = None
    with pytest.raises(MarketLabelError, match="names no cutoff"):
        labelled_numbers(found, item(UP, "up"))


def test_a_window_is_held_to_its_own_acceptance_stamp():
    """Rows 2026-05-08, 05-11 and 05-12. Accepted Friday the 8th at 09:00: day zero
    is the 8th and the window is the 8th, 11th and 12th. Accepted the 8th at 16:30,
    after the close: day zero is the next trading row, the 11th, so a window that
    starts on the 8th is not that acceptance's window."""
    good = rose()
    market_labels.labels({"report_numbers.md": [item(UP, "up")]}, good)
    wrong = table(("filing", FILING_DAYS, [0.02, 0.01, 0.0], 0.03, NO_SHORT_INTEREST),
                  accepted="2026-05-08T16:30:00-04:00")
    # day zero moves to the 11th, and the three rows then end before day two
    with pytest.raises(MarketLabelError, match="rows end before reaction day two"):
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
    """Cut the table off at day one, the 11th: the window cannot reach its day two."""
    found = rose()
    found["cutoff"] = "2026-05-11"
    found["rows"] = [row for row in found["rows"] if row["date"] <= "2026-05-11"]
    with pytest.raises(MarketLabelError, match="rows end before reaction day two"):
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


# --- the rows are the only calendar: the acceptance is held to the calendar it implies --

def test_a_table_missing_the_row_for_its_own_day_zero_is_refused():
    """Accepted Friday the 8th at 09:00, before the close: the 8th is day zero and
    has to be a row. A table with rows for the 11th, 12th and 13th only would read
    its own day zero as the 11th and pass one trading day late; it is refused.
    `rose`, whose rows start on the 8th, stands."""
    market_labels.labels({"report_numbers.md": []}, rose())
    late = table(("filing", ["2026-05-11", "2026-05-12", "2026-05-13"], [0.02, 0.0, 0.01],
                  0.03, NO_SHORT_INTEREST),
                 accepted="2026-05-08T09:00:00-04:00", filing_date="2026-05-08")
    with pytest.raises(MarketLabelError, match="no row for its acceptance day 2026-05-08"):
        market_labels.labels({"report_numbers.md": []}, late)


def test_after_the_close_day_zero_may_be_a_weekend_and_a_holiday_away_and_no_more():
    """Accepted Friday the 8th at 16:35, after the close: day zero is the next
    trading row. Rows for Tuesday the 12th on, four calendar days out, read as
    Monday the 11th being a holiday and stand -- the slack the rows leave. Rows
    for Wednesday the 13th on are five days out, more than a weekend and a
    holiday, and are refused. EDGAR's own close is half past five, so the filing
    date is the 8th either way."""
    holiday = table(("filing", ["2026-05-12", "2026-05-13", "2026-05-14"], [0.02, 0.0, 0.01],
                     0.03, NO_SHORT_INTEREST),
                    accepted="2026-05-08T16:35:00-04:00", filing_date="2026-05-08")
    document = market_labels.labels({"report_numbers.md": [item(UP, "up")]}, holiday,
                                    run_cutoff="2026-05-08")
    assert document["windows"][0]["day_zero"] == "2026-05-12"
    five_out = table(("filing", ["2026-05-13", "2026-05-14", "2026-05-15"], [0.02, 0.0, 0.01],
                      0.03, NO_SHORT_INTEREST),
                     accepted="2026-05-08T16:35:00-04:00", filing_date="2026-05-08")
    with pytest.raises(MarketLabelError, match="5 days after the acceptance"):
        market_labels.labels({"report_numbers.md": []}, five_out)


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
    with_record = plant(tmp_path / "ran", market=rose(), manifest={"dropped_items": []})
    assert market_labels.write(with_record)["written"] is True
    no_key = plant(tmp_path / "no_key", market=rose(), manifest={"cutoff": "2026-05-08"})
    with pytest.raises(MarketLabelError, match="no dropped_items list"):
        market_labels.write(no_key)
    assert not (no_key / "market_labels.json").exists()


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
                          "dropped_items": [{"item_id": DOWN, "reason": "quote not found"}]})
    assert market_labels.write(run)["items"] == 1
    written = json.loads((run / "market_labels.json").read_text(encoding="utf-8"))
    assert [one["upstream_item_id"] for one in written["items"]] == [UP]
    assert written["not_labelled"][0]["id"] == DOWN
