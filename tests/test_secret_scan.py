"""A planted credential has to be named, and the repository has to stay quiet.

Every credential in this file is **planted by the test**. None of them is a real
token, none was ever issued, and none is a value read out of the environment --
the strings below are the expected values, and they are expected because this
file wrote them.

The two halves matter equally. A scan that names a planted token and also names
`TOKEN_VARIABLE = "TIINGO_TOKEN"` is a scan somebody turns off in a week, so
every test that plants a secret also asserts silence on the lines this
repository actually contains, and the whole tree is scanned in one test for
exactly that reason.

The third rule, the exact one, can only fire where the variable is set. That is
asserted by setting it in the test's own environment mapping rather than in the
process, because a test that exported a token would be doing the thing the check
forbids.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

from src import interpreter_pin, secret_scan

REPO_ROOT = Path(__file__).resolve().parent.parent

# Forty characters, the shape Tiingo documents, and not a token: it is this
# sentence's own text with the spaces taken out, so nobody can mistake it.
PLANTED = "notatokenjustfortyplaincharactersherexx"
PLANTED_SHORT = "short"


def test_a_planted_token_assigned_to_a_token_name_is_named() -> None:
    assert secret_scan.findings_in(f'token = "{PLANTED}"', {}) == [
        "a credential assigned to a credential name"
    ]


@pytest.mark.parametrize(
    "line",
    [
        f'api_token = "{PLANTED}"',
        f"api_key: '{PLANTED}'",
        f'PASSWORD="{PLANTED}"',
        f'"accessToken": "{PLANTED}"',
        f'apikey = "{PLANTED}"',
    ],
)
def test_every_credential_name_this_project_could_write_is_read(line: str) -> None:
    assert secret_scan.findings_in(line, {})


def test_a_credential_in_a_query_string_is_named() -> None:
    line = f"curl 'https://eodhd.com/api/eod/LEH.US?api_token={PLANTED}&fmt=json'"
    assert secret_scan.findings_in(line, {}) == ["a credential in a query string"]


def test_the_value_of_a_variable_this_shell_holds_is_named_by_its_variable() -> None:
    """The exact check, and the only one that cannot be fooled by a new shape."""
    secrets = secret_scan.credentials_in_the_environment({"TIINGO_TOKEN": PLANTED})
    assert secrets == {"TIINGO_TOKEN": PLANTED}
    assert secret_scan.findings_in(f"a note to self: {PLANTED}", secrets) == [
        "the value of $TIINGO_TOKEN"
    ]


def test_the_report_never_carries_the_credential_itself() -> None:
    """A check that quotes what it found has written it down one more time."""
    secrets = secret_scan.credentials_in_the_environment({"EODHD_TOKEN": PLANTED})
    for finding in secret_scan.findings_in(f'token = "{PLANTED}"', secrets):
        assert PLANTED not in finding


def test_a_short_value_is_not_a_credential() -> None:
    assert secret_scan.findings_in(f'token = "{PLANTED_SHORT}"', {}) == []
    assert secret_scan.credentials_in_the_environment({"TIINGO_TOKEN": PLANTED_SHORT}) == {}


@pytest.mark.parametrize(
    "line",
    [
        'TOKEN_VARIABLE = "TIINGO_TOKEN"',
        'token = os.environ["TIINGO_TOKEN"]',
        'headers={"Authorization": f"Token {token}"}',
        'params={"api_token": token, "fmt": "json"}',
        'export TIINGO_TOKEN=your-token-goes-here',
        'api_token = "<your token>"',
        'password = "changeme-placeholder-value"',
        'api_token=${EODHD_TOKEN}',
    ],
)
def test_the_lines_this_repository_actually_contains_stay_quiet(line: str) -> None:
    assert secret_scan.findings_in(line, {}) == []


def test_the_whole_repository_is_quiet_today(tmp_path: Path) -> None:
    """The check runs on every gate, so one false positive turns it off."""
    result = subprocess.run(
        [sys.executable, "-m", "src.secret_scan", "src", "docs", "tools", "tests", "Makefile"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        env={**os.environ, "PYTHONPATH": str(REPO_ROOT)},
    )
    assert result.returncode == 0, result.stderr


def test_a_planted_file_is_reported_with_its_path_and_line(tmp_path: Path) -> None:
    planted = tmp_path / "notes.md"
    planted.write_text(f"first line\nsecond line\napi_token = \"{PLANTED}\"\n", encoding="utf-8")
    result = subprocess.run(
        [sys.executable, "-m", "src.secret_scan", str(planted)],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        env={**os.environ, "PYTHONPATH": str(REPO_ROOT)},
    )
    assert result.returncode == secret_scan.FOUND
    assert f"{planted}:3:" in result.stderr
    assert PLANTED not in result.stderr


def test_a_source_file_is_read_where_the_plain_name_check_skips_it(tmp_path: Path) -> None:
    """The likeliest file to carry a token is the one that uses it."""
    planted = tmp_path / "fetch.py"
    planted.write_text(f'TOKEN = "{PLANTED}"\n', encoding="utf-8")
    assert secret_scan.occurrences([planted], {})


def test_a_path_that_is_not_there_is_not_a_pass(tmp_path: Path) -> None:
    result = subprocess.run(
        [sys.executable, "-m", "src.secret_scan", str(tmp_path / "nothing")],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        env={**os.environ, "PYTHONPATH": str(REPO_ROOT)},
    )
    assert result.returncode == secret_scan.CANNOT_RUN


def test_neither_route_nor_both_is_refused() -> None:
    for argv in ([], ["--changed", "src"]):
        with pytest.raises(SystemExit):
            secret_scan.main(argv)


def test_the_gate_runs_it() -> None:
    """A check the Makefile does not call is a check nobody runs."""
    makefile = (REPO_ROOT / "Makefile").read_text(encoding="utf-8")
    assert "secret-check" in makefile.split("check: ")[1].split("\n")[0]
    assert "src.secret_scan --changed" in makefile


def test_every_backend_credential_is_on_the_list() -> None:
    """A backend whose variable is not listed is one nothing watches."""
    from src.prices import eodhd, tiingo

    assert tiingo.TOKEN_VARIABLE in secret_scan.CREDENTIAL_VARIABLES
    assert eodhd.TOKEN_VARIABLE in secret_scan.CREDENTIAL_VARIABLES


def test_it_refuses_the_wrong_interpreter() -> None:
    assert interpreter_pin.mismatch((3, 11)) is not None
