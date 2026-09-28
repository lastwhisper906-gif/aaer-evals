"""Three sources, one frame, and every expected value written out by hand.

The fixtures under `tests/fixtures/prices/` are **hand-written from each
provider's published response format**. Not one of them was captured from a call
this code made, and that is the whole point: a fixture recorded from the wire
agrees with the parser that recorded it however either of them behaves, which is
the circular evidence that put ten of twelve items in `lessons.md`. Nobody here
has a token, so the fixtures could not have been captured even by accident --
but they would still be written this way if somebody did.

Every derived number below is computed in the assertion, term by term, so a
reader can follow the arithmetic without opening the module:

* CRSP's adjusted close is `abs(prc) / cfacpr`. The fixture carries
  `prc = 195.3125` with `cfacpr = 2.0`, and `195.3125 / 2 = 97.65625` exactly --
  both are exact in binary, so the assertion is an equality rather than a
  tolerance and a wrong divisor cannot hide inside a rounding allowance.
* CRSP writes `prc` **negative** when the figure is a bid/ask average rather
  than a closing trade. The fixture carries `-12.50`, and the frame has to read
  `12.50`.
* Tiingo's split-adjusted close is its own `adjClose` column, and the fixture
  separates it from `close` by a two-for-one split so a parser reading the wrong
  column is visible: `close = 200.00` against `adjClose = 100.00`.
* Every provider's rows arrive out of order in the fixtures, on purpose, because
  every return downstream is computed off consecutive days.

* CRSP's delisting-day row carries `dlret = -0.8750`, a value neither of the two
  Shumway defaults (-0.30, -0.55) can produce, so a parser that dropped `dlret`
  and substituted a default would be visible. It is exact in binary, so the
  assertion is an equality.

The wire: each backend's `history` is called here against a stand-in for the
one module it talks through. Tiingo and EODHD talk through `requests`; the
stand-in records the address, the parameters and the headers, and answers the
same hand-written fixtures. CRSP talks through `wrds`, whose `raw_sql` answers a
pandas frame; the stand-in's `to_dict("records")` answers what pandas does for
the legacy CRSP columns -- a missing number is `float('nan')`, not `None`, and
`permno` and `dlstcd` are double precision, so a code arrives as `574.0`. That is
the shape the JSON fixture cannot carry, and the one a `history` that only
passed rows through would refuse. What no test here reaches is the service
itself: `src/probe_price_sources.py` puts each `history` to it with whatever
credential the environment holds, and nobody has a credential yet.
"""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

import pytest

from src import market, prices
from src.prices import crsp, eodhd, tiingo

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "prices"

# The ticker every fixture uses. `tests/fixtures/market/prices/ZZZZ.csv` already
# uses it for the same reason: it is not a company, so no reader can mistake a
# constructed number for a fact about one.
TICKER = "ZZZZ"


def fixture(name: str):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


# --- the one frame ---------------------------------------------------------


def every_backend_frame() -> dict[str, list[dict]]:
    return {
        "crsp": crsp.rows_from(fixture("crsp_daily.json")),
        "tiingo": tiingo.rows_from(
            fixture("tiingo_daily.json"),
            ticker=TICKER,
            security_id=tiingo.permaticker_from(fixture("tiingo_metadata.json")),
        ),
        "eodhd": eodhd.rows_from(fixture("eodhd_daily.json"), ticker=TICKER),
    }


@pytest.mark.parametrize("name", prices.BACKENDS)
def test_every_backend_answers_the_same_keys(name: str) -> None:
    rows = every_backend_frame()[name]
    assert rows, f"{name} shaped no rows out of its own fixture"
    for entry in rows:
        assert tuple(entry) == prices.COLUMNS


@pytest.mark.parametrize("name", prices.BACKENDS)
def test_every_backend_answers_oldest_first(name: str) -> None:
    """Every fixture is written out of order, so a backend that passes the
    provider's order through is visible here."""
    days = [entry["date"] for entry in every_backend_frame()[name]]
    assert days == sorted(days)
    assert len(set(days)) == len(days)


@pytest.mark.parametrize("name", prices.BACKENDS)
def test_every_backend_names_a_module_by_its_own_name(name: str) -> None:
    assert prices.backend(name).NAME == name


# --- CRSP ------------------------------------------------------------------


def test_crsp_adjusts_the_close_by_the_cumulative_factor() -> None:
    rows = {entry["date"]: entry for entry in crsp.rows_from(fixture("crsp_daily.json"))}
    split_day = rows[dt.date(2008, 9, 15)]
    assert split_day["close"] == 195.3125
    assert split_day["adjusted_close"] == 195.3125 / 2.0 == 97.65625


def test_crsp_reads_a_bid_ask_average_as_a_price() -> None:
    """`prc` is negated to mark the quote; the price is its magnitude."""
    rows = {entry["date"]: entry for entry in crsp.rows_from(fixture("crsp_daily.json"))}
    quoted = rows[dt.date(2008, 9, 16)]
    assert quoted["close"] == 12.50
    assert quoted["adjusted_close"] == 12.50 / 1.0


def test_crsp_carries_the_delisting_return_and_its_reason() -> None:
    rows = {entry["date"]: entry for entry in crsp.rows_from(fixture("crsp_daily.json"))}
    last = rows[dt.date(2008, 9, 17)]
    assert last["delisting_return"] == -0.875
    assert last["delisting_return"] not in (
        prices.DELISTING_DEFAULT,
        prices.DELISTING_DEFAULT_NASDAQ,
    )
    assert last["delisting_code"] == "574"
    assert rows[dt.date(2008, 9, 15)]["delisting_return"] is None


def test_crsp_carries_the_permanent_identifier_and_not_only_the_ticker() -> None:
    rows = crsp.rows_from(fixture("crsp_daily.json"))
    assert {entry["security_id"] for entry in rows} == {"90001"}
    assert {entry["ticker"] for entry in rows} == {TICKER}


def test_crsp_refuses_a_zero_adjustment_factor_rather_than_dividing() -> None:
    payload = fixture("crsp_daily.json")
    payload[0]["cfacpr"] = 0
    with pytest.raises(prices.PriceError, match="cfacpr is zero"):
        crsp.rows_from(payload)


def test_crsp_refuses_a_row_with_no_price() -> None:
    payload = fixture("crsp_daily.json")
    payload[0]["prc"] = None
    with pytest.raises(prices.PriceError, match="prc is null"):
        crsp.rows_from(payload)


def test_crsp_without_a_pgpass_file_is_unconfigured(tmp_path: Path) -> None:
    with pytest.raises(prices.Unconfigured, match="does not exist"):
        crsp.credential(tmp_path / "nothing")


def test_crsp_with_a_pgpass_file_is_configured(tmp_path: Path) -> None:
    pgpass = tmp_path / ".pgpass"
    pgpass.write_text(WRDS_LINE, encoding="utf-8")
    pgpass.chmod(0o600)
    assert crsp.credential(pgpass) == pgpass


def test_the_crsp_query_joins_on_the_permanent_identifier() -> None:
    """A ticker join splices two companies together at a reassignment."""
    assert "d.permno = f.permno" in crsp.QUERY
    assert "dlret" in crsp.QUERY and "dlstcd" in crsp.QUERY


class StandInFrame:
    """What `wrds.Connection.raw_sql` answers, reduced to the one call made on it."""

    def __init__(self, records: list[dict]) -> None:
        self.records = records

    def to_dict(self, orient: str) -> list[dict]:
        assert orient == "records"
        return [dict(entry) for entry in self.records]


def stand_in_wrds(monkeypatch: pytest.MonkeyPatch, records: list[dict]) -> dict:
    """Install a `wrds` module whose one connection answers `records`."""
    import sys
    import types

    seen: dict = {}

    class Connection:
        def __init__(self, **arguments) -> None:
            seen["connected_with"] = arguments

        def raw_sql(self, sql: str, params: dict) -> StandInFrame:
            seen["sql"], seen["params"] = sql, params
            return StandInFrame(records)

        def close(self) -> None:
            seen["closed"] = True

    module = types.ModuleType("wrds")
    module.Connection = Connection
    monkeypatch.setitem(sys.modules, "wrds", module)
    return seen


NAN = float("nan")

# A `.pgpass` line for WRDS, in Postgres's own format
# (hostname:port:database:username:password), with the host, port and database
# the `wrds` package's own defaults name (wrds/sql.py, 3.5.0).
WRDS_LINE = "wrds-pgdata.wharton.upenn.edu:9737:wrds:handed-in-user:handed-in-pw\n"

# The fixture's three rows as pandas hands them over from the legacy CRSP
# tables: every numeric column double precision, every missing number NaN, and
# the date a `datetime.date` as the Postgres driver returns it.
CRSP_FRAME_RECORDS = [
    {"permno": 90001.0, "date": dt.date(2008, 9, 16), "prc": -12.50, "vol": 471504.0,
     "cfacpr": 1.0, "ret": -0.4000, "dlret": NAN, "dlstcd": NAN, "ticker": "ZZZZ",
     "exchcd": 3.0},
    {"permno": 90001.0, "date": dt.date(2008, 9, 15), "prc": 195.3125, "vol": NAN,
     "cfacpr": 2.0, "ret": -0.0500, "dlret": NAN, "dlstcd": NAN, "ticker": "ZZZZ",
     "exchcd": 3.0},
    {"permno": 90001.0, "date": dt.date(2008, 9, 17), "prc": 0.21, "vol": 120000.0,
     "cfacpr": 1.0, "ret": -0.9832, "dlret": -0.8750, "dlstcd": 574.0, "ticker": "ZZZZ",
     "exchcd": 3.0},
]


def test_crsp_history_reads_the_frame_the_wire_answers(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    pgpass = tmp_path / ".pgpass"
    pgpass.write_text(WRDS_LINE, encoding="utf-8")
    pgpass.chmod(0o600)
    seen = stand_in_wrds(monkeypatch, CRSP_FRAME_RECORDS)
    rows = crsp.history(
        "zzzz", dt.date(2008, 9, 1), dt.date(2008, 9, 30), pgpass=pgpass
    )
    assert seen["params"] == {"ticker": "ZZZZ", "start": "2008-09-01", "end": "2008-09-30"}
    assert seen["sql"] == crsp.QUERY
    assert seen["closed"] is True
    by_day = {entry["date"]: entry for entry in rows}
    assert list(by_day) == [dt.date(2008, 9, 15), dt.date(2008, 9, 16), dt.date(2008, 9, 17)]
    # A missing number is "this source does not know", never a refusal.
    assert by_day[dt.date(2008, 9, 15)]["delisting_return"] is None
    assert by_day[dt.date(2008, 9, 15)]["delisting_code"] is None
    assert by_day[dt.date(2008, 9, 15)]["volume"] is None
    assert by_day[dt.date(2008, 9, 16)]["delisting_return"] is None
    # A double-precision code is the integer CRSP publishes, not "574.0".
    assert by_day[dt.date(2008, 9, 17)]["delisting_code"] == "574"
    assert {entry["security_id"] for entry in rows} == {"90001"}
    assert by_day[dt.date(2008, 9, 17)]["delisting_return"] == -0.875
    assert by_day[dt.date(2008, 9, 15)]["adjusted_close"] == 195.3125 / 2.0


def test_crsp_history_and_the_fixture_agree_row_for_row(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """The JSON fixture and the pandas frame are one set of rows in two shapes."""
    pgpass = tmp_path / ".pgpass"
    pgpass.write_text(WRDS_LINE, encoding="utf-8")
    pgpass.chmod(0o600)
    stand_in_wrds(monkeypatch, CRSP_FRAME_RECORDS)
    wire = crsp.history(TICKER, pgpass=pgpass)
    shaped = crsp.rows_from(fixture("crsp_daily.json"), ticker=TICKER)
    for from_wire, from_fixture in zip(wire, shaped, strict=True):
        for column in prices.COLUMNS:
            if column == "volume":
                continue  # the frame's 2008-09-15 volume is missing on purpose
            assert from_wire[column] == from_fixture[column], column


def test_crsp_history_refuses_a_missing_price_rather_than_reading_nan(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    pgpass = tmp_path / ".pgpass"
    pgpass.write_text(WRDS_LINE, encoding="utf-8")
    pgpass.chmod(0o600)
    records = [dict(entry) for entry in CRSP_FRAME_RECORDS]
    records[0]["prc"] = NAN
    stand_in_wrds(monkeypatch, records)
    with pytest.raises(prices.PriceError, match="prc is null"):
        crsp.history(TICKER, pgpass=pgpass)


def test_crsp_history_without_a_pgpass_never_imports_wrds(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    seen = stand_in_wrds(monkeypatch, CRSP_FRAME_RECORDS)
    with pytest.raises(prices.Unconfigured):
        crsp.history(TICKER, pgpass=tmp_path / "nothing")
    assert seen == {}


class StandInResponse:
    def __init__(self, payload, status_code: int = 200) -> None:
        self.payload = payload
        self.status_code = status_code
        self.text = json.dumps(payload)

    def json(self):
        return self.payload


def stand_in_requests(monkeypatch: pytest.MonkeyPatch, answers: dict) -> list[dict]:
    """Install a `requests` module that answers by address and records each call."""
    import sys
    import types

    calls: list[dict] = []

    class RequestException(OSError):
        pass

    class Session:
        trust_env = True

        def get(self, url, params=None, headers=None, timeout=None):
            calls.append({"url": url, "params": params, "headers": headers,
                          "timeout": timeout, "trust_env": self.trust_env})
            answer = answers[url]
            if isinstance(answer, Exception):
                raise answer
            return answer

    module = types.ModuleType("requests")
    module.Session = Session
    module.RequestException = RequestException
    monkeypatch.setitem(sys.modules, "requests", module)
    return calls


# --- Tiingo ----------------------------------------------------------------


def test_tiingo_history_asks_the_documented_addresses_with_the_token_in_a_header(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls = stand_in_requests(
        monkeypatch,
        {
            "https://api.tiingo.com/tiingo/daily/zzzz": StandInResponse(
                fixture("tiingo_metadata.json")
            ),
            "https://api.tiingo.com/tiingo/daily/zzzz/prices": StandInResponse(
                fixture("tiingo_daily.json")
            ),
        },
    )
    rows = tiingo.history(
        "ZZZZ", dt.date(2023, 10, 11), dt.date(2023, 10, 13),
        environ={"TIINGO_TOKEN": "stand-in"},
    )
    assert [call["url"] for call in calls] == [
        "https://api.tiingo.com/tiingo/daily/zzzz",
        "https://api.tiingo.com/tiingo/daily/zzzz/prices",
    ]
    assert calls[1]["params"] == {"startDate": "2023-10-11", "endDate": "2023-10-13"}
    for call in calls:
        assert call["headers"]["Authorization"] == "Token stand-in"
        assert "stand-in" not in json.dumps(call["params"])
        # a session that reads no ~/.netrc and no proxy variable of the process
        assert call["trust_env"] is False
    assert {entry["security_id"] for entry in rows} == {"US000000000999"}
    assert {entry["ticker"] for entry in rows} == {TICKER}
    assert [entry["adjusted_close"] for entry in rows] == [100.00, 97.65625, 94.42]


def test_tiingo_history_refuses_an_answer_that_is_not_a_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    stand_in_requests(
        monkeypatch,
        {"https://api.tiingo.com/tiingo/daily/zzzz": StandInResponse({"detail": "Not found."}, 404)},
    )
    with pytest.raises(prices.PriceError, match="404"):
        tiingo.history("ZZZZ", environ={"TIINGO_TOKEN": "stand-in"})



def test_tiingo_takes_the_adjusted_column_and_not_the_close() -> None:
    rows = {
        entry["date"]: entry
        for entry in tiingo.rows_from(fixture("tiingo_daily.json"), ticker=TICKER)
    }
    split_day = rows[dt.date(2023, 10, 11)]
    assert split_day["close"] == 200.00
    assert split_day["adjusted_close"] == 100.00


def test_tiingo_drops_the_time_rather_than_converting_it() -> None:
    """The stamp is always midnight universal time; a daily bar is a calendar day."""
    rows = tiingo.rows_from(fixture("tiingo_daily.json"), ticker=TICKER)
    assert [entry["date"] for entry in rows] == [
        dt.date(2023, 10, 11),
        dt.date(2023, 10, 12),
        dt.date(2023, 10, 13),
    ]


def test_tiingo_carries_the_permaticker_as_the_identifier() -> None:
    assert tiingo.permaticker_from(fixture("tiingo_metadata.json")) == "US000000000999"


def test_tiingo_carries_no_delisting_return_at_all() -> None:
    """None is *this source does not know*, and is never zero."""
    rows = tiingo.rows_from(fixture("tiingo_daily.json"), ticker=TICKER)
    assert all(entry["delisting_return"] is None for entry in rows)
    assert not any(entry["delisting_return"] == 0 for entry in rows)


def test_tiingo_refuses_a_row_with_no_adjusted_close() -> None:
    payload = fixture("tiingo_daily.json")
    del payload[0]["adjClose"]
    with pytest.raises(prices.PriceError, match="adjClose"):
        tiingo.rows_from(payload, ticker=TICKER)


def test_tiingo_without_a_token_is_unconfigured() -> None:
    with pytest.raises(prices.Unconfigured, match="TIINGO_TOKEN"):
        tiingo.credential({})


def test_tiingo_treats_a_blank_token_as_no_token() -> None:
    with pytest.raises(prices.Unconfigured):
        tiingo.credential({"TIINGO_TOKEN": "   "})


# --- EODHD -----------------------------------------------------------------


def test_eodhd_reads_its_own_adjusted_close_column() -> None:
    rows = {
        entry["date"]: entry
        for entry in eodhd.rows_from(fixture("eodhd_daily.json"), ticker=TICKER)
    }
    assert rows[dt.date(2008, 9, 17)]["adjusted_close"] == 0.125
    assert rows[dt.date(2008, 9, 17)]["close"] == 0.125


def test_eodhd_puts_the_exchange_suffix_on_a_bare_symbol() -> None:
    assert eodhd.symbol("leh") == "LEH.US"
    assert eodhd.symbol("LEH.US") == "LEH.US"


def test_eodhd_delisted_listing_carries_the_exchange() -> None:
    """The exchange decides which of the two defaults a missing return takes."""
    listing = eodhd.delisted_from(fixture("eodhd_delisted.json"))
    assert listing["ZZZZ"]["exchange"] == "NASDAQ"
    assert listing["ZZZY"]["exchange"] == "NYSE"


def test_eodhd_without_a_token_is_unconfigured() -> None:
    with pytest.raises(prices.Unconfigured, match="EODHD_TOKEN"):
        eodhd.credential({})


def test_eodhd_history_asks_the_documented_address_with_the_exchange_suffix(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls = stand_in_requests(
        monkeypatch,
        {"https://eodhd.com/api/eod/ZZZZ.US": StandInResponse(fixture("eodhd_daily.json"))},
    )
    rows = eodhd.history(
        "zzzz", dt.date(2008, 9, 15), dt.date(2008, 9, 17),
        environ={"EODHD_TOKEN": "stand-in"},
    )
    assert calls[0]["params"] == {
        "from": "2008-09-15",
        "to": "2008-09-17",
        "api_token": "stand-in",
        "fmt": "json",
    }
    assert [entry["date"] for entry in rows] == [
        dt.date(2008, 9, 15),
        dt.date(2008, 9, 16),
        dt.date(2008, 9, 17),
    ]
    assert {entry["ticker"] for entry in rows} == {TICKER}
    assert [entry["adjusted_close"] for entry in rows] == [0.21, 0.25, 0.125]
    assert all(entry["delisting_return"] is None for entry in rows)


def test_eodhd_delisted_asks_for_the_delisted_listing(monkeypatch: pytest.MonkeyPatch) -> None:
    calls = stand_in_requests(
        monkeypatch,
        {
            "https://eodhd.com/api/exchange-symbol-list/US": StandInResponse(
                fixture("eodhd_delisted.json")
            )
        },
    )
    listing = eodhd.delisted(environ={"EODHD_TOKEN": "stand-in"})
    assert calls[0]["params"]["delisted"] == "1"
    assert listing["ZZZZ"]["exchange"] == "NASDAQ"


# --- the delisting-return default ------------------------------------------


def test_a_delisting_return_the_source_carries_is_used_unchanged() -> None:
    value, reason = prices.delisting_return_with_default(-0.9832, exchange="NYSE")
    assert (value, reason) == (-0.9832, "source")


def test_a_missing_delisting_return_takes_the_shumway_default() -> None:
    """Shumway (1997), Journal of Finance 52(1)."""
    assert prices.delisting_return_with_default(None, exchange="NYSE") == (
        -0.30,
        "shumway-1997",
    )


def test_a_missing_delisting_return_on_nasdaq_takes_the_wider_default() -> None:
    """Shumway and Warther (1999), Journal of Finance 54(6)."""
    assert prices.delisting_return_with_default(None, exchange="NASDAQ") == (
        -0.55,
        "shumway-and-warther-1999",
    )
    assert prices.delisting_return_with_default(None, exchange="Nasdaq Global Select") == (
        -0.55,
        "shumway-and-warther-1999",
    )


def test_a_delisting_return_of_zero_is_not_a_missing_one() -> None:
    """The bias this correction exists for is a flat row, and a flat row is
    exactly what a source that knows nothing looks like."""
    assert prices.delisting_return_with_default(0.0, exchange="NASDAQ") == (0.0, "source")


def test_the_two_defaults_are_the_published_numbers() -> None:
    assert prices.DELISTING_DEFAULT == -0.30
    assert prices.DELISTING_DEFAULT_NASDAQ == -0.55


# --- choosing a backend ----------------------------------------------------


def test_the_default_backend_is_the_forward_track_s() -> None:
    assert prices.name_from_environment({}) == "tiingo"
    assert prices.DEFAULT_BACKEND == "tiingo"


def test_the_environment_names_the_backend() -> None:
    assert prices.name_from_environment({"PRICE_BACKEND": "crsp"}) == "crsp"


def test_a_backend_nobody_built_is_refused_rather_than_defaulted() -> None:
    with pytest.raises(prices.PriceError, match="stooq"):
        prices.name_from_environment({"PRICE_BACKEND": "stooq"})


# --- the shape the market module already reads -----------------------------


def test_the_frame_writes_out_as_the_columns_market_already_reads() -> None:
    """`src/market.py:read_prices` and its hand-computed expected values do not
    move when the source underneath changes."""
    rows = tiingo.rows_from(fixture("tiingo_daily.json"), ticker=TICKER)
    written = prices.as_csv_rows(rows)
    for column in market.PRICE_COLUMNS:
        assert column in written[0]
    assert [entry["date"] for entry in written] == [
        "2023-10-11",
        "2023-10-12",
        "2023-10-13",
    ]
    assert float(written[0]["adjusted_close"]) == 100.00


def test_a_written_frame_reads_back_through_the_market_module(tmp_path: Path) -> None:
    """End to end on the one path that matters: the frame out, the reader in."""
    import csv

    rows = crsp.rows_from(fixture("crsp_daily.json"))
    folder = tmp_path / "prices"
    folder.mkdir()
    with (folder / f"{TICKER}.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["date", "close", "adjusted_close"])
        writer.writeheader()
        writer.writerows(prices.as_csv_rows(rows))
    series = market.read_prices(folder)
    assert [day for day, _ in series[TICKER]] == [
        dt.date(2008, 9, 15),
        dt.date(2008, 9, 16),
        dt.date(2008, 9, 17),
    ]
    assert series[TICKER][0][1] == 97.65625


# --- the frame refuses what is not a price ---------------------------------


def test_a_row_builder_refuses_a_price_that_is_not_one() -> None:
    for bad in (0, -1.0, "not a number", None, float("nan")):
        with pytest.raises(prices.PriceError):
            prices.row(
                date=dt.date(2020, 1, 2),
                security_id=None,
                ticker=TICKER,
                close=bad,
                adjusted_close=1.0,
                volume=1.0,
            )


def test_a_row_builder_refuses_a_timestamp_where_a_day_belongs() -> None:
    with pytest.raises(prices.PriceError, match="calendar date"):
        prices.row(
            date=dt.datetime(2020, 1, 2, 16, 0),
            security_id=None,
            ticker=TICKER,
            close=1.0,
            adjusted_close=1.0,
            volume=1.0,
        )


def test_a_row_builder_refuses_a_row_with_no_ticker() -> None:
    with pytest.raises(prices.PriceError, match="no ticker"):
        prices.row(
            date=dt.date(2020, 1, 2),
            security_id="90001",
            ticker="",
            close=1.0,
            adjusted_close=1.0,
            volume=1.0,
        )


# --- the credential handed in is the one that logs in -------------------------
#
# PR #60's refute-check: `wrds.Connection()` took no argument, so Postgres's
# client library logged in with the process's own .pgpass, PGPASSFILE, PGHOST
# and PGUSER, whatever file was handed in; and `requests` read the process's
# ~/.netrc, which replaces an Authorization header. Each test below sets the
# process to say something else, so a read of the wrong one shows.

def _the_process_says_otherwise(monkeypatch, tmp_path):
    elsewhere = tmp_path / "the-process"
    elsewhere.mkdir()
    (elsewhere / ".pgpass").write_text(
        "wrds-pgdata.wharton.upenn.edu:9737:wrds:process-user:process-pw\n",
        encoding="utf-8")
    monkeypatch.setenv("HOME", str(elsewhere))
    monkeypatch.setenv("PGPASSFILE", str(elsewhere / ".pgpass"))
    monkeypatch.setenv("PGUSER", "process-user")
    monkeypatch.setenv("PGHOST", "process-host.invalid")


def test_crsp_logs_in_with_the_line_of_the_pgpass_handed_in(monkeypatch, tmp_path):
    _the_process_says_otherwise(monkeypatch, tmp_path)
    pgpass = tmp_path / "handed-in.pgpass"
    pgpass.write_text("# a comment\n"
                      "other.example.org:5432:other:someone:not-this\n" + WRDS_LINE,
                      encoding="utf-8")
    pgpass.chmod(0o600)
    seen = stand_in_wrds(monkeypatch, CRSP_FRAME_RECORDS)
    crsp.history(TICKER, dt.date(2008, 9, 1), dt.date(2008, 9, 30), pgpass=pgpass)
    assert seen["connected_with"] == {
        "wrds_hostname": "wrds-pgdata.wharton.upenn.edu", "wrds_port": 9737,
        "wrds_dbname": "wrds", "wrds_username": "handed-in-user",
        "wrds_password": "handed-in-pw"}


def test_a_pgpass_line_is_read_as_postgres_reads_it(tmp_path):
    """A `*` matches any host, and a backslash escapes a colon inside a field."""
    pgpass = tmp_path / ".pgpass"
    pgpass.write_text("*:*:wrds:some\\:one:pass\\:word\\\\x\n", encoding="utf-8")
    pgpass.chmod(0o600)
    assert crsp.login(pgpass)["wrds_username"] == "some:one"
    assert crsp.login(pgpass)["wrds_password"] == "pass:word\\x"


def test_a_pgpass_with_no_wrds_line_is_unconfigured_and_never_connects(
        monkeypatch, tmp_path):
    _the_process_says_otherwise(monkeypatch, tmp_path)
    pgpass = tmp_path / "handed-in.pgpass"
    pgpass.write_text("other.example.org:5432:other:someone:not-this\n", encoding="utf-8")
    pgpass.chmod(0o600)
    seen = stand_in_wrds(monkeypatch, CRSP_FRAME_RECORDS)
    with pytest.raises(prices.Unconfigured, match="no line for wrds-pgdata"):
        crsp.history(TICKER, pgpass=pgpass)
    assert seen == {}


def test_a_refused_login_with_no_terminal_is_unconfigured(monkeypatch, tmp_path):
    """The package falls back to asking at the terminal; with none, that is an
    end-of-file, reported as the login refused."""
    import sys
    import types

    class Connection:
        def __init__(self, **arguments):
            raise EOFError

    module = types.ModuleType("wrds")
    module.Connection = Connection
    monkeypatch.setitem(sys.modules, "wrds", module)
    pgpass = tmp_path / ".pgpass"
    pgpass.write_text(WRDS_LINE, encoding="utf-8")
    pgpass.chmod(0o600)
    with pytest.raises(prices.Unconfigured, match="refused the login"):
        crsp.history(TICKER, pgpass=pgpass)


@pytest.mark.parametrize("backend, variable, address", [
    (eodhd, "EODHD_TOKEN", "https://eodhd.com/api/eod/ZZZZ.US"),
    (tiingo, "TIINGO_TOKEN", "https://api.tiingo.com/tiingo/daily/zzzz"),
])
def test_a_request_that_fails_carries_no_token_into_its_error(
        monkeypatch, backend, variable, address):
    """EODHD sends the token in the query string, and `requests` puts the
    address of a failed request into its message."""
    import sys

    token = "planted-tok"
    answers: dict = {}
    stand_in_requests(monkeypatch, answers)
    answers[address] = sys.modules["requests"].RequestException(
        f"Max retries exceeded with url: {address}?api_token={token}")
    with pytest.raises(prices.PriceError) as caught:
        backend.history(TICKER, environ={variable: token})
    assert token not in str(caught.value)
    assert caught.value.__cause__ is None and caught.value.__suppress_context__


def test_an_error_answer_echoing_the_token_is_printed_without_it(monkeypatch):
    token = "planted-tok"
    address = "https://eodhd.com/api/eod/ZZZZ.US"
    stand_in_requests(monkeypatch, {address: StandInResponse(
        {"error": f"invalid api_token={token}"}, status_code=401)})
    with pytest.raises(prices.PriceError) as caught:
        eodhd.history(TICKER, environ={"EODHD_TOKEN": token})
    assert "401" in str(caught.value)
    assert token not in str(caught.value)


def test_a_pgpass_others_can_read_is_ignored_as_postgres_ignores_it(tmp_path):
    pgpass = tmp_path / ".pgpass"
    pgpass.write_text(WRDS_LINE, encoding="utf-8")
    pgpass.chmod(0o644)
    with pytest.raises(prices.Unconfigured, match="read by others"):
        crsp.login(pgpass)


def test_a_wildcard_user_names_no_one_to_log_in_as(tmp_path):
    pgpass = tmp_path / ".pgpass"
    pgpass.write_text("wrds-pgdata.wharton.upenn.edu:9737:wrds:*:stand-in\n",
                      encoding="utf-8")
    pgpass.chmod(0o600)
    with pytest.raises(prices.Unconfigured, match="names no user"):
        crsp.login(pgpass)


def test_eodhd_asks_through_a_session_that_trusts_nothing_in_the_process(monkeypatch):
    """EODHD's token rides in the query string, so a proxy the process names
    would see it."""
    calls = stand_in_requests(monkeypatch, {
        "https://eodhd.com/api/eod/ZZZZ.US": StandInResponse(fixture("eodhd_daily.json"))})
    eodhd.history(TICKER, environ={"EODHD_TOKEN": "stand-in"})
    assert [call["trust_env"] for call in calls] == [False]


def test_a_token_across_the_cut_is_taken_out_before_the_message_is_cut(monkeypatch):
    """Cut first and a token straddling character 200 leaves its head behind."""
    token = "planted-tok"
    address = "https://eodhd.com/api/eod/ZZZZ.US"
    body = "x" * 195 + token
    answer = StandInResponse({}, status_code=500)
    answer.text = body
    stand_in_requests(monkeypatch, {address: answer})
    with pytest.raises(prices.PriceError) as caught:
        eodhd.history(TICKER, environ={"EODHD_TOKEN": token})
    assert "plant" not in str(caught.value)

