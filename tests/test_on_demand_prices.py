"""An on-demand run fetches its price folder the way the nightly routine does.

The source is a stand-in that is handed in, never the network, and the token is
a made-up string; nothing here reads the real one. The planted EDGAR is the one
`tests/test_on_demand.py` serves: NVIDIA's 10-Q 0001045810-26-000075, filed
2026-08-26, whose SIC code `universe.json` records as 3674.

Expected values, worked by hand:

* the window is the 400 days before the filing date, through it: 2026-08-26
  less 365 days is 2025-08-26 (no leap day lies between), and 35 days more is
  2025-07-22 (26 days to July 31, 9 more);
* SIC 3674 is in division D, Manufacturing, 2000 to 3999, whose sector fund is
  XLI in `src/sic_to_sector_etf_map_v0.1.json`, and the broad market's series
  is SPY, so the symbols are NVDA, SPY, XLI.
"""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

import pytest

from src import agent_inputs, calculator, nightly, on_demand
from tests.test_agent_inputs import spec_bundle_names
from tests.test_on_demand import ACCESSION, CIK, TICKER, client, server  # noqa: F401

WINDOW = (dt.date(2025, 7, 22), dt.date(2026, 8, 26))
SYMBOLS = ["NVDA", "SPY", "XLI"]
STAND_IN_TOKEN = "stand-in-token"
NO_TOKEN_REASON = "no price series: TIINGO_TOKEN unset"
FETCH_RECORD = {"backend": "tiingo", "fetched_at": "2026-08-27T07:05:00+00:00",
                "asked_for": {"start": "2025-07-22", "end": "2026-08-26"},
                "served": {symbol: {"rows": 270, "first_day": "2025-07-22",
                                    "last_day": "2026-08-26"} for symbol in SYMBOLS}}


class World:
    """The planted run: a stand-in bundle, a stand-in source, a recorded analysis."""

    def __init__(self, tmp_path, server, monkeypatch):
        fetcher = client(tmp_path, server)
        self.server = server
        monkeypatch.setattr(on_demand.edgar_client, "EdgarClient", lambda: fetcher)
        self.out = tmp_path / "runs" / TICKER / ACCESSION
        self.fetcher = fetcher
        # EDGAR's index names the registrant's tickers and SIC at its top level;
        # the planted one is NVIDIA's own, as the live index states it
        path = f"/submissions/CIK{CIK}.json"
        index = json.loads(server.bodies[path][0])
        server.bodies[path] = (json.dumps({**index, "tickers": ["NVDA"], "sic": "3674"}
                                          ).encode(), "")
        self.asked = []
        self.analysed = []

        def bundle(argv):
            run = Path(argv[argv.index("--out") + 1])
            for name in spec_bundle_names() + ("input_controls.md",):
                (run / name).write_text(f"this is {name}\n", encoding="utf-8")
            payload = {"ticker": TICKER, "ratios": {"gross_margin": 0.5},
                       **{section: {"price_at_cutoff": 1.0}
                          for section in calculator.PRICED_SECTIONS}}
            (run / "calculator.json").write_text(json.dumps(payload), encoding="utf-8")
            (run / calculator.FILINGS_ONLY).write_text(
                json.dumps(calculator.filings_only(payload)), encoding="utf-8")
            (run / "input_manifest.json").write_text(
                json.dumps({"accession": ACCESSION, "ticker": TICKER, "dropped_items": []}),
                encoding="utf-8")
            return 0

        def analysis(argv):
            self.analysed.append(argv)
            return 0

        from src import run_analysis
        monkeypatch.setattr(on_demand.assemble_bundle, "main", bundle)
        monkeypatch.setattr(run_analysis, "main", analysis)

    def fetch(self, **kwargs):
        self.asked.append(kwargs)
        folder = kwargs["into"]
        folder.mkdir(parents=True, exist_ok=True)
        for symbol in kwargs["symbols"]:
            (folder / f"{symbol}.csv").write_text("date,close\n2026-08-26,1.0\n")
        return dict(FETCH_RECORD)

    def main(self, *flags, environ, fetch_prices, ticker=TICKER):
        return on_demand.main(["--ticker", ticker, "--accession", ACCESSION,
                               "--out", str(self.out), *flags],
                              environ=environ, fetch_prices=fetch_prices)

    def poison_the_network_after_the_store(self, monkeypatch):
        """Any call to EDGAR once the store is built raises, and is counted."""
        real = on_demand.fetch_store
        self.touched = []

        def after(*args, **kwargs):
            held = real(*args, **kwargs)
            for name in ("get", "get_json", "document"):
                def refuse(*a, _name=name, **k):
                    self.touched.append(_name)
                    raise AssertionError(f"EDGAR was asked ({_name}) after the store was built")
                monkeypatch.setattr(self.fetcher, name, refuse)
            return held

        monkeypatch.setattr(on_demand, "fetch_store", after)

    def run(self, environ=None):
        return self.main("--run", environ={"TIINGO_TOKEN": STAND_IN_TOKEN}
                         if environ is None else environ, fetch_prices=self.fetch)


@pytest.fixture
def world(tmp_path, server, monkeypatch):  # noqa: F811
    return World(tmp_path, server, monkeypatch)


def test_the_run_fetches_the_window_for_the_three_symbols_and_hands_the_folder_on(world):
    environ = {"TIINGO_TOKEN": STAND_IN_TOKEN}
    assert world.run(environ) == 0
    assert world.asked == [{"symbols": SYMBOLS, "start": WINDOW[0], "end": WINDOW[1],
                            "into": world.out / "prices", "environ": environ,
                            "backend": "tiingo"}]
    assert world.asked[0]["environ"] is environ
    assert len(world.analysed) == 1
    argv = world.analysed[0]
    assert argv[argv.index("--prices") + 1] == str(world.out / "prices")
    assert json.loads((world.out / "price_fetch.json").read_text()) == FETCH_RECORD
    assert sorted(p.name for p in (world.out / "prices").iterdir()) == [
        "NVDA.csv", "SPY.csv", "XLI.csv"]


def test_the_token_is_never_written_or_printed(world, capsys):
    assert world.run() == 0
    seen = capsys.readouterr()
    assert STAND_IN_TOKEN not in seen.out + seen.err
    for path in world.out.rglob("*"):
        if path.is_file():
            assert STAND_IN_TOKEN not in path.read_text(), path


def test_no_token_means_the_run_goes_on_without_prices_and_says_why(world, capsys):
    def never(**_):
        pytest.fail("the source was asked with no token")

    assert world.main("--run", environ={}, fetch_prices=never) == 0
    assert "--prices" not in world.analysed[0]
    assert NO_TOKEN_REASON == nightly.NO_PRICES_UNSET
    assert NO_TOKEN_REASON in capsys.readouterr().err
    assert json.loads((world.out / "price_fetch.json").read_text()) == {
        "fetched": False, "reason": NO_TOKEN_REASON}
    assert not (world.out / "prices").exists()


def test_a_source_that_fails_leaves_the_run_without_prices_and_without_the_token(
        world, capsys):
    def fails(**_):
        raise RuntimeError(f"the source refused {STAND_IN_TOKEN}")

    assert world.main("--run", environ={"TIINGO_TOKEN": STAND_IN_TOKEN},
                      fetch_prices=fails) == 0
    assert "--prices" not in world.analysed[0]
    seen = capsys.readouterr()
    assert "RuntimeError: the source refused <TIINGO_TOKEN>" in seen.err
    assert STAND_IN_TOKEN not in seen.out + seen.err + (world.out / "price_fetch.json").read_text()


def test_no_prices_skips_the_fetch_and_passes_nothing(world):
    def never(**_):
        pytest.fail("the fetch ran under --no-prices")

    assert world.main("--run", "--no-prices", environ={"TIINGO_TOKEN": STAND_IN_TOKEN},
                      fetch_prices=never) == 0
    assert "--prices" not in world.analysed[0]
    assert not (world.out / "prices").exists() and not (world.out / "price_fetch.json").exists()


def test_the_price_folder_is_fetched_without_run_too(world):
    assert world.main(environ={"TIINGO_TOKEN": STAND_IN_TOKEN}, fetch_prices=world.fetch) == 0
    assert (world.out / "prices" / "NVDA.csv").is_file()
    assert world.analysed == []


def test_the_sic_and_the_series_come_from_the_registrants_own_record(world):
    # NVDA's record says SIC 3674, so the sector series is XLI; a record that
    # said 3661 (division D too) is no different, and one that said 9995,
    # nonclassifiable, would be asked for SPY once. The record is the one planted.
    assert world.run() == 0
    assert world.asked[0]["symbols"] == SYMBOLS


def test_a_record_that_names_no_sic_means_no_prices_with_the_reason_and_the_run_goes_on(
        world, monkeypatch, capsys):
    path = f"/submissions/CIK{CIK}.json"
    index = json.loads(world.server.bodies[path][0])
    del index["sic"]
    world.server.bodies[path] = (json.dumps(index).encode(), "")
    world.poison_the_network_after_the_store(monkeypatch)

    def never(**_):
        pytest.fail("the source was asked for a company with no SIC")

    assert world.main("--run", environ={"TIINGO_TOKEN": STAND_IN_TOKEN},
                      fetch_prices=never) == 0
    assert "--prices" not in world.analysed[0]
    assert "MarketError" in capsys.readouterr().err
    assert world.touched == []
    assert json.loads((world.out / "price_fetch.json").read_text())["fetched"] is False


def test_the_price_step_makes_no_call_to_edgar_with_a_token_or_without(world, monkeypatch):
    world.poison_the_network_after_the_store(monkeypatch)
    assert world.run() == 0
    assert len(world.asked) == 1 and world.touched == []


def test_no_token_asks_edgar_nothing_either(world, monkeypatch):
    world.poison_the_network_after_the_store(monkeypatch)
    assert world.main("--run", environ={}, fetch_prices=world.fetch) == 0
    assert world.asked == [] and world.touched == []


def test_a_name_that_is_not_the_registrants_ticker_prices_nothing(world, monkeypatch, capsys):
    """The refuter's case: AAPL given as the run's name on NVIDIA's filing, by --cik.
    The series would be AAPL's, and the SIC the universe's for AAPL, not NVIDIA's."""
    world.poison_the_network_after_the_store(monkeypatch)

    def never(**_):
        pytest.fail("the source was asked for a series named by a label")

    out = world.out.parent.parent / "AAPL" / ACCESSION
    assert on_demand.main(["--ticker", "AAPL", "--cik", CIK, "--accession", ACCESSION,
                           "--out", str(out), "--run"],
                          environ={"TIINGO_TOKEN": STAND_IN_TOKEN}, fetch_prices=never) == 0
    reason = "the run's name is not one of the registrant's tickers at the cutoff"
    assert reason in capsys.readouterr().err
    assert "--prices" not in world.analysed[0]
    assert json.loads((out / "price_fetch.json").read_text()) == {
        "fetched": False, "reason": reason}
    assert not (out / "prices").exists()


def test_a_name_that_is_the_registrants_ticker_is_priced_under_cik(world):
    assert on_demand.main(["--ticker", "nvda", "--cik", CIK, "--accession", ACCESSION,
                           "--out", str(world.out), "--run"],
                          environ={"TIINGO_TOKEN": STAND_IN_TOKEN},
                          fetch_prices=world.fetch) == 0
    assert world.asked[0]["symbols"] == SYMBOLS


def test_an_empty_environment_handed_in_is_not_the_process_environment(world, monkeypatch):
    monkeypatch.setenv("TIINGO_TOKEN", STAND_IN_TOKEN)

    def never(**_):
        pytest.fail("the process's own token was used though an empty mapping was handed in")

    assert world.main("--run", environ={}, fetch_prices=never) == 0
    assert "--prices" not in world.analysed[0]


def test_the_process_environment_is_used_when_none_is_handed_in(world, monkeypatch):
    monkeypatch.setenv("TIINGO_TOKEN", STAND_IN_TOKEN)
    assert world.main("--run", environ=None, fetch_prices=world.fetch) == 0
    assert world.asked and world.asked[0]["environ"] is on_demand.os.environ


AGENTS_WITHOUT_PRICES = ("numbers-reader", "notes-text-reader", "accounting-analyst",
                         "financial-analyst")


def _routed_files(root: Path):
    return [path for path in sorted(root.rglob("*")) if path.is_file()]


def test_no_reader_and_no_accounting_or_financial_analyst_receives_a_price(world):
    """By content, not by name: a price line or the fetch record's text in any file
    routed to the four, under any name, is a leak."""
    assert world.run() == 0
    assert (world.out / "prices").is_dir() and (world.out / "price_fetch.json").is_file()
    price_lines = {line.strip() for path in (world.out / "prices").glob("*.csv")
                   for line in path.read_text().splitlines() if line.strip()}
    record_text = (world.out / "price_fetch.json").read_text()
    record_lines = {line.strip() for line in record_text.splitlines() if len(line.strip()) > 10}
    assert price_lines and record_lines
    for agent in AGENTS_WITHOUT_PRICES:
        agent_inputs.build(world.out, agent)
        root = agent_inputs.session_root(world.out, agent)
        files = _routed_files(root)
        assert files, agent
        for path in files:
            text = path.read_text(encoding="utf-8")
            lines = {line.strip() for line in text.splitlines()}
            assert not lines & price_lines, (agent, path.name, "holds a line of a price series")
            assert record_text not in text, (agent, path.name)
            assert not lines & record_lines, (agent, path.name, "holds text of the fetch record")
            assert ".csv" not in path.name and "price" not in path.name.lower(), (agent, path)


@pytest.mark.parametrize("agent", ["accounting-analyst", "financial-analyst"])
def test_the_calculator_the_two_analysts_hold_has_no_priced_section(world, agent):
    assert world.run() == 0
    agent_inputs.build(world.out, agent)
    root = agent_inputs.session_root(world.out, agent)
    held = [path for path in _routed_files(root) if path.name.startswith("calculator")]
    assert [path.name for path in held] == [calculator.FILINGS_ONLY]
    for path in held:
        view = json.loads(path.read_text(encoding="utf-8"))
        assert view["ratios"] == {"gross_margin": 0.5}      # the view is the payload's, trimmed
        assert [key for key in calculator.PRICED_SECTIONS if key in view] == []
