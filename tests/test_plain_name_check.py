"""plain_name_check has to name a planted code and stay silent on kept vocabulary.

Every expected value here is planted by this file. The codes are real tokens
from the archived project's own identifier families, and they are read from
`tests/fixtures/letter_number_codes.txt`, which records where each came from and
how often it appears in `archive/`. They live in a fixture rather than as
literals here for a reason worth stating: the post-write hook runs the check over
everything a branch changed, so literals in this file would make the hook report
this file on every write, for good, and a check that cries wolf about its own
test is one somebody turns off in a week. The kept vocabulary below stays inline,
because none of it is reported.

The kept vocabulary comes from `CLAUDE.md`, `docs/HOW_WE_WORK.md`,
`docs/INPUT_SPEC.md` and the two places on this branch where a kept token already
takes the forbidden shape: `EX-99.1` in `src/fetch_fixtures.py` and `CC-BY-4.0`
in `LICENSE` and `CITATION.cff`.

Every assertion reads the **output the check printed**, never the regular
expression. A no-op regular expression fails quietly -- that is how the
display-name filter passed on 2026-09-07 with word boundaries macOS sed accepts
and silently ignores -- so each test that asserts silence also plants one code
into the same input and asserts that it, and only it, comes back. A check that
never fires must not be able to pass a test about staying quiet.
"""

from __future__ import annotations

import ast
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from src import plain_name_check

REPO_ROOT = Path(__file__).resolve().parent.parent

CODE_LIST = Path(__file__).resolve().parent / "fixtures" / "letter_number_codes.txt"


def invented_families() -> list[str]:
    """The archived project's own codes, in the order the fixture records them."""
    lines = CODE_LIST.read_text(encoding="utf-8").splitlines()
    return [line.split()[0] for line in lines if line.strip() and not line.startswith("#")]


INVENTED_FAMILIES = invented_families()

# Vocabulary this repository has to keep. Nothing here may be reported.
KEPT_VOCABULARY = """\
This filing is a 10-K; the prior one was a 10-Q and the release was an 8-K.
Item 1A and Item 7A, and item 2.02, 4.01, 4.02, 1.01 and 5.02.
Exhibit 21 and Exhibit 10; the earnings release is EX-99.1, and the submission
header sometimes says only EX-99.
us-gaap:AccountsReceivableNetCurrent and us-gaap:Revenues.
Python 3.12, rules v0.1, sha256 and SHA-256, UTF-8, ISO 8601, rule 10-b5.
AAPL, PANW, QCOM, STX, CIEN, CARR, NVDA, CSCO.
Accession 0000320193-26-000001, filed 2026-09-09, accepted after the close.
tests/fixtures/AAPL/10-K/aapl-20250927.htm, and the branch harness/cycle-020.
The prose is CC-BY-4.0 and the legacy encoding table is ISO-8859-1.
"""

PLANTED, SECOND, THIRD = INVENTED_FAMILIES[0], INVENTED_FAMILIES[1], INVENTED_FAMILIES[2]


def run(capsys, *argv):
    """Exit status and the lines the check printed, which is all a caller sees."""
    status = plain_name_check.main(list(argv))
    printed = capsys.readouterr().err
    return status, printed.splitlines()


def git(repo, *args):
    subprocess.run(("git", *args), cwd=repo, check=True, capture_output=True)


# --- naming a planted code ---------------------------------------------------


def test_a_planted_code_is_named_with_its_file_and_its_line(tmp_path, capsys):
    document = tmp_path / "cycle_report.md"
    document.write_text(
        "The receivables ratio outran revenue for two quarters.\n"
        f"Raised as {PLANTED}, and the owner has not read it.\n"
        "Nothing else happened.\n"
    )

    status, lines = run(capsys, str(document))

    assert status == 1
    assert lines == [f"{document}:2: {PLANTED}"]


def test_every_family_the_old_project_invented_is_named(tmp_path, capsys):
    document = tmp_path / "ledger.md"
    document.write_text("".join(f"item {code} carried over\n" for code in INVENTED_FAMILIES))

    status, lines = run(capsys, str(document))

    assert status == 1
    assert lines == [
        f"{document}:{number}: {code}"
        for number, code in enumerate(INVENTED_FAMILIES, start=1)
    ]


def test_a_code_is_named_once_for_every_occurrence(tmp_path, capsys):
    document = tmp_path / "notes.md"
    document.write_text(f"{PLANTED} supersedes {PLANTED}, and closes {SECOND}.\n")

    status, lines = run(capsys, str(document))

    assert status == 1
    assert lines == [
        f"{document}:1: {PLANTED}",
        f"{document}:1: {PLANTED}",
        f"{document}:1: {SECOND}",
    ]


def test_a_file_with_no_code_prints_nothing_and_exits_zero(tmp_path, capsys):
    document = tmp_path / "notes.md"
    document.write_text("receivables_outrun_revenue fired on two of twelve.\n")

    assert run(capsys, str(document)) == (0, [])


# --- staying silent on the vocabulary the repository keeps -------------------


def test_the_vocabulary_the_repository_keeps_is_not_named(tmp_path, capsys):
    document = tmp_path / "vocabulary.md"
    document.write_text(KEPT_VOCABULARY)

    assert run(capsys, str(document)) == (0, [])

    # The same input with one code added, so a check that never fires cannot
    # pass the paragraph above.
    document.write_text(KEPT_VOCABULARY + f"Raised as {PLANTED}.\n")
    planted_line = len(KEPT_VOCABULARY.splitlines()) + 1
    status, lines = run(capsys, str(document))

    assert status == 1
    assert lines == [f"{document}:{planted_line}: {PLANTED}"]


@pytest.mark.parametrize(
    "kept",
    ["10-K", "8-K", "EX-99.1", "EX-99", "SHA-256", "UTF-8", "ISO-8859-1", "CC-BY-4.0"],
)
def test_a_kept_token_alone_on_a_line_is_not_named(tmp_path, capsys, kept):
    document = tmp_path / "one_token.md"
    document.write_text(f"{kept}\n")

    assert run(capsys, str(document)) == (0, [])

    # The same line with a code beside it: the exemption has to skip the kept
    # token, not the line, and the check has to still be capable of firing.
    document.write_text(f"{kept} and {PLANTED}\n")
    status, lines = run(capsys, str(document))

    assert status == 1
    assert lines == [f"{document}:1: {PLANTED}"]


# --- the files it does not read ---------------------------------------------


@pytest.mark.parametrize(
    "unread",
    [
        "archive/RESULTS.md",
        "tests/fixtures/AAPL/10-K/aapl-20250927.htm",
        "runs/AAPL/0000320193-26-000001/input_notes.md",
    ],
)
def test_a_file_whose_text_is_not_ours_to_correct_is_not_read(tmp_path, capsys, unread):
    frozen = tmp_path / unread
    frozen.parent.mkdir(parents=True, exist_ok=True)
    frozen.write_text(f"the finding was raised as {PLANTED}\n")
    ours = tmp_path / "docs" / "structure_changes.md"
    ours.parent.mkdir(parents=True, exist_ok=True)
    ours.write_text(f"the finding was raised as {PLANTED}\n")

    status, lines = run(capsys, str(tmp_path))

    # The sibling is the positive control: silence here has to mean "skipped
    # that file", not "found nothing anywhere".
    assert status == 1
    assert lines == [f"{ours}:1: {PLANTED}"]


def test_a_file_that_is_not_text_is_not_read(tmp_path, capsys):
    (tmp_path / "prices.bin").write_bytes(b"\xff\xfe\x00" + PLANTED.encode() + b"\x00\xff")
    ours = tmp_path / "notes.md"
    ours.write_text(f"raised as {PLANTED}\n")

    status, lines = run(capsys, str(tmp_path))

    assert status == 1
    assert lines == [f"{ours}:1: {PLANTED}"]


def test_the_check_names_no_code_in_its_own_test(capsys):
    """Otherwise the hook reports this file on every write on any branch that

    touches it, for good, and nobody leaves a check like that switched on. This
    is why the codes are read from a fixture instead of written here.
    """
    assert run(capsys, str(Path(__file__).resolve())) == (0, [])


def test_the_check_names_no_code_in_its_own_module(tmp_path, capsys):
    """The hook runs on every write; a check that reports itself gets turned off."""
    module = Path(plain_name_check.__file__)

    assert run(capsys, str(module)) == (0, [])

    # A copy of the same module with one code appended, so the silence above
    # cannot be silence about that file rather than about its text.
    copy = tmp_path / "plain_name_check_copy.py"
    text = module.read_text(encoding="utf-8")
    copy.write_text(f"{text}# raised as {PLANTED}\n")
    status, lines = run(capsys, str(copy))

    assert status == 1
    assert lines == [f"{copy}:{len(text.splitlines()) + 1}: {PLANTED}"]


# --- selecting what this branch changed --------------------------------------


@pytest.fixture
def repo(tmp_path, monkeypatch):
    """A repo whose baseline already carries a code, in a file nobody touched."""
    git(tmp_path, "init", "-q", "-b", "baseline")
    git(tmp_path, "config", "user.email", "test@example.invalid")
    git(tmp_path, "config", "user.name", "test")
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "already_published.md").write_text(f"closed as {PLANTED}\n")
    git(tmp_path, "add", "-A")
    git(tmp_path, "commit", "-qm", "baseline")

    git(tmp_path, "checkout", "-q", "-b", "work")
    monkeypatch.chdir(tmp_path)
    return tmp_path


def test_changed_names_the_committed_the_staged_and_the_untracked(repo, capsys):
    (repo / "docs" / "committed.md").write_text(f"raised as {PLANTED}\n")
    git(repo, "add", "docs/committed.md")
    git(repo, "commit", "-qm", "work")
    (repo / "docs" / "staged.md").write_text(f"first line clean\nraised as {SECOND}\n")
    git(repo, "add", "docs/staged.md")
    (repo / "docs" / "untracked.md").write_text(f"raised as {THIRD}\n")

    status, lines = run(capsys, "--changed", "--baseline", "baseline")

    assert status == 1
    assert sorted(lines) == sorted(
        [
            f"docs/committed.md:1: {PLANTED}",
            f"docs/staged.md:2: {SECOND}",
            f"docs/untracked.md:1: {THIRD}",
        ]
    )


def test_changed_leaves_alone_a_published_file_this_branch_did_not_touch(repo, capsys):
    """The baseline file carries a code. It is not this branch's to answer for."""
    (repo / "docs" / "new.md").write_text(f"raised as {PLANTED}\n")

    status, lines = run(capsys, "--changed", "--baseline", "baseline")

    assert status == 1
    assert lines == [f"docs/new.md:1: {PLANTED}"]


def test_changed_on_a_branch_that_touched_nothing_prints_nothing(repo, capsys):
    assert run(capsys, "--changed", "--baseline", "baseline") == (0, [])


def test_an_unresolvable_baseline_is_not_a_pass(repo, capsys):
    status, _ = run(capsys, "--changed", "--baseline", "no-such-ref")

    assert status == 2


def test_neither_changed_nor_a_path_is_refused():
    with pytest.raises(SystemExit):
        plain_name_check.main([])


# --- the hook runs it under bare python3.12, which has no site-packages ------


def test_it_imports_nothing_outside_the_standard_library():
    """A third-party import makes the post-write hook inert, silently."""
    module = ast.parse(Path(plain_name_check.__file__).read_text(encoding="utf-8"))
    imported = set()
    for node in ast.walk(module):
        if isinstance(node, ast.Import):
            imported |= {alias.name.split(".")[0] for alias in node.names}
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            imported.add(node.module.split(".")[0])

    assert imported
    assert imported <= sys.stdlib_module_names | {"src"}


def post_write_hook_command() -> str:
    """The command .claude/settings.json actually runs after a Write or an Edit."""
    settings = json.loads((REPO_ROOT / ".claude" / "settings.json").read_text(encoding="utf-8"))
    matched = [
        hook["command"]
        for entry in settings["hooks"]["PostToolUse"]
        if entry["matcher"] == "Write|Edit"
        for hook in entry["hooks"]
    ]
    assert len(matched) == 1
    return matched[0]


@pytest.mark.skipif(shutil.which("python3.12") is None, reason="no bare python3.12 here")
def test_the_configured_hook_names_a_planted_code(tmp_path):
    """Run the command before trusting the config: the 2026-09-07 lesson."""
    repo = tmp_path / "repo"
    shutil.copytree(REPO_ROOT / "src", repo / "src", ignore=shutil.ignore_patterns("__pycache__"))
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.email", "test@example.invalid")
    git(repo, "config", "user.name", "test")
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", "baseline")
    git(repo, "update-ref", "refs/remotes/origin/main", "HEAD")
    (repo / "docs").mkdir()
    (repo / "docs" / "note.md").write_text(f"raised as {PLANTED}\n")

    result = subprocess.run(
        post_write_hook_command(), shell=True, cwd=repo, capture_output=True, text=True
    )

    assert result.returncode == 1
    assert result.stderr.splitlines() == [f"docs/note.md:1: {PLANTED}"]


@pytest.mark.skipif(shutil.which("python3.12") is None, reason="no bare python3.12 here")
def test_the_configured_hook_is_silent_where_the_module_does_not_exist(tmp_path):
    """A worktree branched before this landed must not get an import error."""
    result = subprocess.run(
        post_write_hook_command(), shell=True, cwd=tmp_path, capture_output=True, text=True
    )

    assert (result.returncode, result.stdout, result.stderr) == (0, "", "")


@pytest.mark.skipif(shutil.which("python3.12") is None, reason="no bare python3.12 here")
def test_it_runs_as_a_module_under_the_bare_pinned_interpreter(tmp_path):
    """`python3.12 -m src.plain_name_check` is what .claude/settings.json calls."""
    document = tmp_path / "notes.md"
    document.write_text(f"raised as {PLANTED}\n")
    environment = {key: value for key, value in os.environ.items() if key != "PYTHONPATH"}

    result = subprocess.run(
        ("python3.12", "-m", "src.plain_name_check", str(document)),
        cwd=REPO_ROOT,
        env=environment,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert result.stderr.splitlines() == [f"{document}:1: {PLANTED}"]
