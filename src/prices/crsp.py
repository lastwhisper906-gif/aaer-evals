"""CRSP through WRDS: the pattern study's backend, and the only one with `dlret`.

A universe drawn from a past date is full of companies that stopped trading, and
what happened on the day they stopped is the number that decides whether the
study measures accounting failure or measures survivorship. CRSP carries it --
`dlret`, the delisting return, with `dlstcd`, the reason -- and it is the
standard the literature reads because of exactly that. Stony Brook subscribes,
so it is free here; a student registers at `wrds-www.wharton.upenn.edu/register`
and the school's representative approves the account.

The credential comes by one of two routes, and nothing is written down here.
On a machine that holds files it is a `.pgpass`, Postgres's own credential
file, outside this tree. A cloud session holds its secrets as environment
variables and never as a file, so where no `.pgpass` exists the two variables
`WRDS_USERNAME` and `WRDS_PASSWORD` are read instead. Until one route is
configured this backend answers `Unconfigured`, naming both routes and the
variable that is missing, and the study does not start, which is the state
recorded in `docs/needs_judgment.md`.

**The credential handed in is the one the login uses.** Left to itself the
`wrds` package logs in through Postgres's client library, which reads the
process's own `PGPASSFILE` or `$HOME/.pgpass`, and `PGHOST` and `PGUSER`
besides -- so a caller that handed in one home was checked against that home's
file and logged in with the process's. `login` reads the WRDS line out of the
file handed in, or the two variables out of the mapping handed in and never
out of `os.environ` in its place, and `history` passes host, port, database,
user and password to `wrds.Connection` explicitly, which is the one route the
package gives that none of those variables can override. If that login is
refused, the package falls back to asking at the terminal; with no terminal
that is an end-of-file, which is reported as `Refused` -- the login refused --
rather than as anything the process holds.

**The host is checked before the package is asked to connect, on the variables
route.** A cloud session's network policy allows named hosts only, and the
`wrds` package, handed a host it cannot reach, waits out the operating system's
connect timeout and then asks at a terminal there is none of -- which would
read as a refused login when nothing was refused. So on that route `history`
first opens a plain TCP connection to `wrds-pgdata.wharton.upenn.edu:9737`
(`reachable`) and, when it cannot, raises `Unreachable` naming the host and the
owner's two steps: the allowed-domains entry, then the two secrets. The
`.pgpass` route is a machine on the owner's own network, where the package's
own error is the right one and its terminal has a person at it; it is not
checked, and the fetch tests that drive this module through that route
(`tests/test_market.py`) never touch the network.

The query
---------

`crsp.dsf` is the daily stock file -- one row per security per trading day.
`crsp.dsedelist` is the delisting event file -- at most one row per security,
carrying `dlret` and `dlstcd`. They are joined on `permno`, which is CRSP's
permanent security identifier and the reason a CRSP series never splices two
companies together the way a ticker-keyed series does.

Three conventions of the daily file that a reader has to know, and that this
module handles rather than passes on:

* **`prc` is negated when it is a bid/ask average** rather than a closing trade.
  CRSP writes the sign to mark the difference; the price is its magnitude. A
  reader that takes the sign at face value gets a negative price, and a reader
  that filters those rows out drops the thin days on purpose.
* **`cfacpr` is the cumulative price adjustment factor.** `prc / cfacpr` is the
  split-adjusted price, which is what the frame's `adjusted_close` carries.
  Where `cfacpr` is zero or missing the row is refused rather than divided.
* **`ret` already carries the delisting return on the delisting day** in the
  CRSP files that merge it. This module does not merge it a second time: it
  hands `dlret` over as its own column and leaves the arithmetic to the study,
  because a return that has been corrected twice looks exactly like one that has
  been corrected once.

One convention of the wire rather than of CRSP: `wrds.Connection.raw_sql`
answers a pandas frame, and `history` hands its rows over with
`to_dict("records")`. A missing value in a numeric column arrives there as
`float('nan')`, not `None`, and the legacy CRSP tables store `permno` and
`dlstcd` as double precision, so a column with one missing value carries every
code as a float -- `574.0`, `90001.0`. `_known` and `_code` turn the first back
into `None` and the second back into the integer CRSP publishes. Without them
every row that is not a delisting day -- nearly every row of every series --
would be refused for a delisting return that "is not finite".

`rows_from` takes the rows the query returned and is what the fixture judges.
`history` is the wire; `tests/test_prices.py` judges it with a stand-in `wrds`
module whose frame answers the shape pandas does, and a stand-in `reachable`.
`wrds` is a runtime dependency (`requirements.txt`) so the fetch can run where
the account works; it is still imported only when it is called, so that the
tests can put a stand-in module in its place and so this module imports on a
machine that has never installed it.
"""

from __future__ import annotations

import datetime as dt
import os
import socket
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from src.prices import PriceError, Unconfigured, row

NAME = "crsp"
PGPASS = Path.home() / ".pgpass"

# The two variables a cloud session holds the credential in, where no .pgpass
# exists. `src/secret_scan.py` watches the second.
USERNAME_VARIABLE = "WRDS_USERNAME"
PASSWORD_VARIABLE = "WRDS_PASSWORD"

# Where WRDS serves its Postgres, as the `wrds` package's own defaults give it
# (`wrds/sql.py`, 3.5.0: WRDS_POSTGRES_HOST, _PORT and _DB). A `.pgpass` line
# names the server it is for, and these are what it is matched against.
WRDS_HOST = "wrds-pgdata.wharton.upenn.edu"
WRDS_PORT = "9737"
WRDS_DATABASE = "wrds"

# A plain TCP connection to WRDS from anywhere it is allowed opens well under a
# second; one the network policy drops answers nothing at all, and this is how
# long to wait before saying so.
REACH_TIMEOUT_SECONDS = 5.0

REGISTER = ("Register at https://wrds-www.wharton.upenn.edu/register/ with the "
            "school address and wait for the approval")


class Unreachable(PriceError):
    """This environment cannot open a connection to the WRDS host, so it was never asked."""


class Refused(Unconfigured):
    """WRDS refused the login the credential handed in gives.

    An `Unconfigured` because the effect is the same -- the backend was asked
    and no row came -- and its own class because the owner's step is different:
    a refused login is a wrong password or an account not yet approved, not a
    credential that is missing.
    """


DAILY_TABLE = "crsp.dsf"
DELIST_TABLE = "crsp.dsedelist"

QUERY = """
    select  f.permno, f.date, f.prc, f.vol, f.cfacpr, f.ret,
            d.dlret, d.dlstcd, n.ticker, n.exchcd
    from    crsp.dsf as f
    left join crsp.dsedelist as d
           on d.permno = f.permno and d.dlstdt = f.date
    left join crsp.dsenames  as n
           on n.permno = f.permno
          and f.date between n.namedt and coalesce(n.nameendt, current_date)
    where   n.ticker = %(ticker)s
      and   f.date between %(start)s and %(end)s
    order by f.date
"""


def credential(pgpass: Path | None = None) -> Path:
    """The `~/.pgpass` the `wrds` package reads, or Unconfigured.

    The file route alone: a file Postgres already owns, in the user's home
    directory, outside this tree -- which is why this is the one backend whose
    credential cannot be committed by accident. `login` is what tries the
    variables route when the file is not there.
    """
    path = PGPASS if pgpass is None else pgpass
    if not path.exists():
        raise Unconfigured(
            f"{path} does not exist, so the {NAME} backend was never asked. "
            f"{REGISTER}, then write the file the `wrds` package asks for on "
            f"its first connection."
        )
    return path


def reachable(host: str, port: int, timeout: float = REACH_TIMEOUT_SECONDS) -> bool:
    """Whether a plain TCP connection to `host:port` opens from here.

    Nothing is sent. A connection the network policy drops never answers, so
    `timeout` is how long to wait; a port nothing listens on is refused at
    once; a name that does not resolve is as unreachable as a host that does
    not answer.
    """
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def unreachable() -> str | None:
    """The refusal for a WRDS host this environment cannot reach, or None.

    Written for the cloud session, whose network policy allows named hosts
    only: the first step is the host's entry in the environment's allowed
    domains, the second the two secrets. Both are the owner's.
    """
    if reachable(WRDS_HOST, int(WRDS_PORT)):
        return None
    return (f"{WRDS_HOST}:{WRDS_PORT} is unreachable from this environment: add "
            f"it to the environment's Allowed domains (claude.ai/code, the "
            f"environment's settings), then set {USERNAME_VARIABLE} and "
            f"{PASSWORD_VARIABLE} as environment secrets")


def _fields(line: str) -> list[str]:
    """One `.pgpass` line's five fields, with `\\:` and `\\\\` read as Postgres reads them."""
    fields, current, escaped = [], [], False
    for character in line:
        if escaped:
            current.append(character)
            escaped = False
        elif character == "\\":
            escaped = True
        elif character == ":":
            fields.append("".join(current))
            current = []
        else:
            current.append(character)
    fields.append("".join(current))
    return fields


def login(pgpass: Path, environ: Mapping[str, str] | None = None) -> dict[str, str]:
    """The `wrds.Connection` arguments the credential handed in gives, or Unconfigured.

    Two routes, the file first. When `pgpass` exists its WRDS line is read as
    below. When it does not, `WRDS_USERNAME` and `WRDS_PASSWORD` are read out
    of `environ` -- the mapping handed in, and never `os.environ` in its place:
    `None` is no environment at all, so a caller that hands in nothing logs in
    with nothing. With neither route configured the refusal names both and the
    variable that is missing, and never the value of the one that is set.

    The file route: the first line whose host, port and database match WRDS's
    -- a `*` matches anything, as Postgres reads it -- is the one Postgres
    itself would use. Two more of Postgres's own readings: it ignores a
    `.pgpass` that its group or anyone else can read, and so does this; and a
    `*` in the user field matches any user rather than naming one, so a line
    whose user is `*` gives no user to log in as and is Unconfigured, not a
    login as the user `*`.

    What the connection is handed is `wrds.Connection`'s own keywords, read off
    the package's source (`wrds/sql.py`, 3.5.0, `Connection.__init__`):
    `wrds_username`, `wrds_password`, `wrds_hostname`, `wrds_port` and
    `wrds_dbname`, which it puts into the connection address it hands the
    driver, so the password in the address is the one used. The stand-ins in
    `tests/test_prices.py` record what they were handed, and the keyword names
    are the source's.
    """
    if not pgpass.exists():
        return _login_from_variables(pgpass, {} if environ is None else environ)
    return _login_from_pgpass(credential(pgpass))


def _arguments(user: str, password: str) -> dict[str, str]:
    return {"wrds_hostname": WRDS_HOST, "wrds_port": int(WRDS_PORT),
            "wrds_dbname": WRDS_DATABASE, "wrds_username": user,
            "wrds_password": password}


def _login_from_variables(pgpass: Path, environ: Mapping[str, str]) -> dict[str, str]:
    """The variables route, taken when `pgpass` does not exist."""
    user = (environ.get(USERNAME_VARIABLE) or "").strip()
    password = (environ.get(PASSWORD_VARIABLE) or "").strip()
    missing = [name for name, value in ((USERNAME_VARIABLE, user),
                                        (PASSWORD_VARIABLE, password)) if not value]
    if missing:
        raise Unconfigured(
            f"{pgpass} does not exist and {' and '.join(missing)} "
            f"{'is' if len(missing) == 1 else 'are'} not set, so the {NAME} backend "
            f"was never asked. Two routes log in: a .pgpass line for "
            f"{WRDS_HOST}:{WRDS_PORT}:{WRDS_DATABASE} on a machine that holds "
            f"files, or {USERNAME_VARIABLE} and {PASSWORD_VARIABLE} set as "
            f"environment secrets in a cloud session. {REGISTER} first."
        )
    return _arguments(user, password)


def _login_from_pgpass(path: Path) -> dict[str, str]:
    """The file route: the WRDS line of a `.pgpass` that exists."""
    if path.stat().st_mode & 0o077:
        raise Unconfigured(
            f"{path} can be read by others than its owner, and Postgres ignores "
            f"such a file; chmod 600 it")
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        fields = _fields(line)
        if len(fields) != 5:
            continue
        host, port, database, user, password = fields
        if host in ("*", WRDS_HOST) and port in ("*", WRDS_PORT) and \
                database in ("*", WRDS_DATABASE):
            if user == "*" or not user:
                raise Unconfigured(
                    f"{path}'s line for {WRDS_HOST} names no user (a `*` matches "
                    f"any), so there is no one for the {NAME} backend to log in as")
            return _arguments(user, password)
    raise Unconfigured(
        f"{path} has no line for {WRDS_HOST}:{WRDS_PORT}:{WRDS_DATABASE}, so the "
        f"{NAME} backend was never asked")


def _known(value: Any) -> Any:
    """`None` for a missing value, whether it arrived as `None` or as pandas' NaN."""
    if isinstance(value, float) and value != value:
        return None
    return value


def _code(value: Any) -> Any:
    """A code CRSP publishes as an integer, back from the float pandas made of it."""
    value = _known(value)
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return value


def _price(value: Any) -> float:
    """The magnitude of `prc`, whose sign marks a bid/ask average."""
    if _known(value) is None:
        raise PriceError("prc is null, so the row carries no price")
    try:
        return abs(float(value))
    except (TypeError, ValueError) as error:
        raise PriceError(f"prc={value!r} is not a number") from error


def _day(value: Any) -> dt.date:
    if isinstance(value, dt.datetime):
        return value.date()
    if isinstance(value, dt.date):
        return value
    try:
        return dt.date.fromisoformat(str(value)[:10])
    except ValueError as error:
        raise PriceError(f"date={value!r} is not a date") from error


def rows_from(payload: Any, *, ticker: str | None = None) -> list[dict]:
    """The rows the query returned, as the shared frame. Judged by the fixture."""
    if not isinstance(payload, list):
        raise PriceError(f"the {NAME} result is not a list of rows")
    out = []
    for entry in payload:
        if not isinstance(entry, dict):
            raise PriceError(f"a {NAME} row is not an object")
        missing = [key for key in ("permno", "date", "prc", "cfacpr") if key not in entry]
        if missing:
            raise PriceError(
                f"a {NAME} row has no {', '.join(missing)} -- refused, because the "
                f"adjusted close is prc over cfacpr and neither can be guessed"
            )
        close = _price(entry["prc"])
        factor = _known(entry["cfacpr"])
        try:
            factor = float(factor)
        except (TypeError, ValueError) as error:
            raise PriceError(f"cfacpr={factor!r} is not a number") from error
        if factor == 0:
            raise PriceError(
                f"cfacpr is zero on {entry['date']}, so the adjusted close would be a "
                f"division by zero -- refused rather than dropped"
            )
        symbol = ticker or entry.get("ticker")
        if not symbol:
            raise PriceError("a row with no ticker cannot be attributed to a company")
        out.append(
            row(
                date=_day(entry["date"]),
                security_id=_code(entry["permno"]),
                ticker=str(symbol).upper(),
                close=close,
                adjusted_close=close / factor,
                volume=_known(entry.get("vol")),
                delisting_return=_known(entry.get("dlret")),
                delisting_code=_code(entry.get("dlstcd")),
            )
        )
    return sorted(out, key=lambda entry: entry["date"])


def history(
    ticker: str,
    start: dt.date | None = None,
    end: dt.date | None = None,
    *,
    pgpass: Path | None = None,
    environ: Mapping[str, str] | None = None,
) -> list[dict]:
    """The daily history, from WRDS.

    `pgpass` is the file to read, `~/.pgpass` by default; `environ` the mapping
    the two variables are read from when that file does not exist, the
    process's environment by default -- the default sits here, at the wire, as
    it does in the other two backends, and `login` itself is handed a mapping
    or nothing.

    Judged by `tests/test_prices.py` against a stand-in `wrds` module answering
    the frame shape pandas does, NaN included, and recording what the
    connection was handed, and a stand-in `reachable`. Against the real service
    it has never been run: the account was approved on 2026-10-07 and the host
    is not yet in the cloud session's allowed domains.
    """
    path = PGPASS if pgpass is None else pgpass
    arguments = login(path, os.environ if environ is None else environ)
    if not path.exists():  # the variables route: the cloud session, checked first
        blocked = unreachable()
        if blocked:
            raise Unreachable(blocked)
    try:
        import wrds
    except ImportError as error:
        raise Unconfigured(
            "the `wrds` package is not installed, so the crsp backend was never "
            "asked. It is in requirements.txt: `.venv/bin/pip install -r "
            "requirements.txt`."
        ) from error
    try:
        connection = wrds.Connection(**arguments)
    except EOFError:
        raise Refused(
            f"WRDS refused the login the credential handed in gives, and the "
            f"package's fallback asked at a terminal there is none of") from None
    try:
        frame = connection.raw_sql(
            QUERY,
            params={
                "ticker": ticker.strip().upper(),
                "start": (start or dt.date(1926, 1, 1)).isoformat(),
                "end": (end or dt.date.today()).isoformat(),
            },
        )
    finally:
        connection.close()
    return rows_from(frame.to_dict("records"), ticker=ticker.strip().upper())
