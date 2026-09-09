"""plain_name_check has to name a planted code and stay silent on kept vocabulary.

Every assertion reads the **output the check printed**, never the regular
expression. A no-op regular expression fails quietly -- that is how the
display-name filter passed on 2026-09-07, with word boundaries macOS sed accepts
and silently ignores -- so a pattern that matches nothing fails the tests that
plant a code, and a pattern that matches everything fails the tests that plant a
plain name beside it. Every test that asserts silence also plants one code into
the same input, so a check that never fires cannot pass a test about staying
quiet.

Where the planted codes come from, all of them written by this project:

* `B1` and `B2` reached `docs/structure_changes.md` and were taken out again in
  commit 4090c9e, "plain names in the structure-change record".
* `B3`, `B4`, `D15`, `GA-001`, `RP-05`, `RP-09`, `INV-03`, `INV-06` are families
  in `archive/`, counted with the check's own patterns over `archive/**/*.md`:
  `B3` 168 times, `B4` 148, `GA-001` 100, `RP-05` 84, `D15` 77, `INV-03` 68,
  `RP-09` 65 and `INV-06` 51.
* `D-P83`, `D-P75`, `E-003`, `PKT-R2`, `INV11`, `TASK_P6A`, `TASK_R101` and
  `P4c` are in the commit subjects of this repository's own history.
* `Q-O10`, `Q-R03` and `D43` sit in `CITATION.cff` and `LICENSE` today.

Where the kept vocabulary comes from is named beside each line below.
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

from src import interpreter_pin, plain_name_check

REPO_ROOT = Path(__file__).resolve().parent.parent

PLANTED = "B2"

# One code per family this project actually wrote. Nothing invented here.
CODES_THIS_PROJECT_WROTE = [
    "B1",
    "B2",
    "B3",
    "B4",
    "D15",
    "D43",
    "GA-001",
    "RP-05",
    "RP-09",
    "INV-03",
    "INV-06",
    "INV11",
    "E-003",
    "D-P83",
    "D-P75",
    "PKT-R2",
    "TASK_P6A",
    "TASK_R101",
    "P4c",
    "Q-O10",
    "Q-R03",
]

# Vocabulary this repository has to keep, and where each line comes from.
# Nothing here may be reported.
KEPT_VOCABULARY = [
    ("This filing is a 10-K; the prior one was a 10-Q and the release was an 8-K.", "README.md"),
    ("Item 1A and Item 7A; item 2.02 and item 4.02.", "docs/INPUT_SPEC.md"),
    ("The earnings release is EX-99.1, and the header sometimes says only EX-99.", "lessons.md"),
    (
        "The section key is item_9a and the finding is receivables_outrun_revenue.",
        "src/split_sections.py for item_9a, docs/HOW_WE_WORK.md line 7 for "
        "receivables_outrun_revenue",
    ),
    ("us-gaap:Revenues and us-gaap:AccountsReceivableNetCurrent.", "src/extract_numbers.py"),
    (
        "Python 3.12 is the pin, rules v0.1 the version, archive-v1 the tag.",
        "the Makefile, src/assemble_bundle.py and docs/structure_changes.md",
    ),
    ("The hash file is runs/MANIFEST.sha256 and the algorithm is sha256.", "lessons.md"),
    (
        "SHA-256, UTF-8 and ISO-8859-1 by their standard names.",
        "the standards bodies -- this repository writes them lowercase, and the "
        "uppercase forms are kept because a standard's name is not ours to change",
    ),
    ("Q4 is derived, never reported, and post-2006 drift is near zero.", "docs/INPUT_SPEC.md"),
    (
        "Post-2006 drift again, and the fiscal year is FY2025.",
        "docs/CHECKLIST.md line 223 for Post-2006, tests/test_trends.py line 278 for FY2025",
    ),
    ("Accession 0000320193-26-000001, filed 2026-09-06, ticker AAPL.", "tests/test_append_check.py"),
    ("The bundle key is AAPL_10K and the document is aapl-20250927.htm.", "tests/test_cutoff_guard.py"),
    ("The prose is CC-BY-4.0 and the dedication is CC0 Public Domain.", "CITATION.cff and LICENSE-docs"),
]

KEPT_LINES = [line for line, _ in KEPT_VOCABULARY]


def run(capsys, *argv):
    """Exit status and the lines the check printed, which is all a caller sees."""
    status = plain_name_check.main(list(argv))
    return status, capsys.readouterr().err.splitlines()


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

    assert status == plain_name_check.FOUND
    assert lines == [f"{document}:2: {PLANTED}"]


@pytest.mark.parametrize("code", CODES_THIS_PROJECT_WROTE)
def test_every_code_this_project_wrote_is_named(tmp_path, capsys, code):
    document = tmp_path / "ledger.md"
    document.write_text(f"the item {code} was carried over from the last cycle\n")

    status, lines = run(capsys, str(document))

    assert status == plain_name_check.FOUND
    assert lines == [f"{document}:1: {code}"]


def test_a_code_is_named_once_for_every_occurrence(tmp_path, capsys):
    document = tmp_path / "notes.md"
    document.write_text(f"{PLANTED} supersedes {PLANTED}, and closes RP-09.\n")

    status, lines = run(capsys, str(document))

    assert status == plain_name_check.FOUND
    assert lines == [
        f"{document}:1: {PLANTED}",
        f"{document}:1: {PLANTED}",
        f"{document}:1: RP-09",
    ]


def test_a_file_with_no_code_prints_nothing_and_exits_zero(tmp_path, capsys):
    document = tmp_path / "notes.md"
    document.write_text("receivables_outrun_revenue fired on two of twelve.\n")

    assert run(capsys, str(document)) == (0, [])


# --- staying silent on the vocabulary the repository keeps -------------------


def test_a_plain_name_beside_a_planted_code_is_not_named(tmp_path, capsys):
    """The guard against a pattern that matches everything."""
    document = tmp_path / "structure_changes.md"
    document.write_text(
        "the branch review-response/2026-09-04 is preserved at tag archive-v1\n"
        f"the cross-tier work {PLANTED} and the response to external review\n"
    )

    status, lines = run(capsys, str(document))

    printed = "\n".join(lines)
    assert status == plain_name_check.FOUND
    assert lines == [f"{document}:2: {PLANTED}"]
    for plain_name in ("review-response", "2026-09-04", "archive-v1", "cross-tier"):
        assert plain_name not in printed


def test_the_vocabulary_the_repository_keeps_is_not_named(tmp_path, capsys):
    document = tmp_path / "vocabulary.md"
    document.write_text("".join(f"{line}\n" for line in KEPT_LINES))

    assert run(capsys, str(document)) == (0, [])

    # The same input with one code added, so a check that never fires cannot
    # pass the assertion above.
    document.write_text("".join(f"{line}\n" for line in KEPT_LINES) + f"Raised as {PLANTED}.\n")
    status, lines = run(capsys, str(document))

    assert status == plain_name_check.FOUND
    assert lines == [f"{document}:{len(KEPT_LINES) + 1}: {PLANTED}"]


@pytest.mark.parametrize("kept,source", KEPT_VOCABULARY)
def test_a_kept_line_alone_is_not_named(tmp_path, capsys, kept, source):
    document = tmp_path / "one_line.md"
    document.write_text(f"{kept}\n")

    assert run(capsys, str(document)) == (0, []), f"reported vocabulary kept in {source}"


# --- a code in the file's own name -------------------------------------------


@pytest.mark.parametrize("dated", ["FY2025", "CY2025", "FY1999", "CY2026"])
def test_the_year_a_period_is_named_by_is_kept(tmp_path, capsys, dated):
    document = tmp_path / "period.md"
    document.write_text(f"the quarter closes in {dated}\n")

    assert run(capsys, str(document)) == (0, [])


@pytest.mark.parametrize("dated_code", ["RP2019", "B2020", "INV1999", "GA2026"])
def test_a_code_whose_number_is_a_year_is_still_a_code(tmp_path, capsys, dated_code):
    """The boundary of the exemption above, planted on purpose. `FY2025` is kept
    as a word; keeping it as a shape -- any capital tag on a four-digit year --
    exempts the archive's own families whenever the serial lands in 1900-2099,
    and a check with that hole in it passes everything it was written to catch."""
    document = tmp_path / "report.md"
    document.write_text(f"the item {dated_code} was closed\n")

    status, lines = run(capsys, str(document))

    assert status == plain_name_check.FOUND
    assert lines == [f"{document}:1: {dated_code}"]


def test_a_code_in_the_file_name_is_named_at_line_zero(tmp_path, capsys):
    document = tmp_path / "GA-001_review.md"
    document.write_text("the text of this file is clean\n")

    status, lines = run(capsys, str(document))

    assert status == plain_name_check.FOUND
    assert lines == [f"{document}:0: GA-001_review.md"]


def test_a_plain_file_name_is_not_named(tmp_path, capsys):
    (tmp_path / "aapl-20250927.htm").write_text("a filing whose name carries a date\n")
    named = tmp_path / "GA-001.md"
    named.write_text("clean\n")

    status, lines = run(capsys, str(tmp_path))

    # The sibling is the positive control: silence on the first name has to mean
    # "read it and found nothing", not "read nothing".
    assert status == plain_name_check.FOUND
    assert lines == [f"{named}:0: GA-001.md"]


# --- the files it reads by name only, and the files it does not read ---------


@pytest.mark.parametrize("source_file", ["trends.py", "notify.sh"])
def test_a_source_file_is_read_by_name_only(tmp_path, capsys, source_file):
    """`Q-1` is a period offset in src/trends.py; code quotes other vocabulary."""
    (tmp_path / source_file).write_text(f"period = 'Q-1'  # and the finding {PLANTED}\n")
    ours = tmp_path / "report.md"
    ours.write_text(f"the finding {PLANTED} again\n")

    status, lines = run(capsys, str(tmp_path))

    assert status == plain_name_check.FOUND
    assert lines == [f"{ours}:1: {PLANTED}"]


def test_a_code_in_a_source_file_name_is_still_named(tmp_path, capsys):
    named = tmp_path / "GA-001.py"
    named.write_text(f"# {PLANTED} is inside, and is not read\n")

    status, lines = run(capsys, str(named))

    assert status == plain_name_check.FOUND
    assert lines == [f"{named}:0: GA-001.py"]


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

    assert status == plain_name_check.FOUND
    assert lines == [f"{ours}:1: {PLANTED}"]


def test_a_file_that_is_not_text_is_not_read(tmp_path, capsys):
    (tmp_path / "prices.bin").write_bytes(b"\xff\xfe\x00" + PLANTED.encode() + b"\x00\xff")
    ours = tmp_path / "notes.md"
    ours.write_text(f"raised as {PLANTED}\n")

    status, lines = run(capsys, str(tmp_path))

    assert status == plain_name_check.FOUND
    assert lines == [f"{ours}:1: {PLANTED}"]


def test_the_check_names_nothing_in_its_own_module_or_test(capsys):
    """The hook runs on every write; a check that reports itself gets turned off."""
    assert run(capsys, str(Path(plain_name_check.__file__)), str(Path(__file__))) == (0, [])


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
    (repo / "docs" / "staged.md").write_text("first line clean\nraised as RP-09\n")
    git(repo, "add", "docs/staged.md")
    (repo / "docs" / "untracked.md").write_text("raised as INV-06\n")

    status, lines = run(capsys, "--changed", "--baseline", "baseline")

    assert status == plain_name_check.FOUND
    assert sorted(lines) == sorted(
        [
            f"docs/committed.md:1: {PLANTED}",
            "docs/staged.md:2: RP-09",
            "docs/untracked.md:1: INV-06",
        ]
    )


def test_changed_leaves_alone_a_published_file_this_branch_did_not_touch(repo, capsys):
    """The baseline file carries a code. It is not this branch's to answer for."""
    (repo / "docs" / "new.md").write_text(f"raised as {PLANTED}\n")

    status, lines = run(capsys, "--changed", "--baseline", "baseline")

    assert status == plain_name_check.FOUND
    assert lines == [f"docs/new.md:1: {PLANTED}"]


def test_changed_on_a_branch_that_touched_nothing_prints_nothing(repo, capsys):
    assert run(capsys, "--changed", "--baseline", "baseline") == (0, [])


def test_changed_names_the_same_code_from_a_subdirectory(repo, capsys, monkeypatch):
    """Run it from anywhere. `git ls-files --others` prints names relative to the
    working directory, so without --full-name an untracked file's name was joined
    onto the repository root, resolved to nothing, and was skipped in silence --
    a clean exit from inside docs/ for the file that failed from the root."""
    (repo / "docs" / "untracked.md").write_text(f"raised as {PLANTED}\n")

    from_root = run(capsys, "--changed", "--baseline", "baseline")
    monkeypatch.chdir(repo / "docs")
    from_subdirectory = run(capsys, "--changed", "--baseline", "baseline")

    assert from_root == (plain_name_check.FOUND, [f"docs/untracked.md:1: {PLANTED}"])
    assert from_subdirectory == (plain_name_check.FOUND, [f"untracked.md:1: {PLANTED}"])


def test_a_name_git_hands_back_that_is_not_a_file_is_not_a_pass(repo, capsys, monkeypatch):
    """The same silence, reached the other way: whatever produces the list, a name
    in it that does not resolve to a file is not a clean file."""
    monkeypatch.setattr(
        plain_name_check, "changed_files", lambda baseline: [repo / "docs" / "gone.md"]
    )

    status, lines = run(capsys, "--changed", "--baseline", "baseline")

    assert status == plain_name_check.CANNOT_RUN
    assert lines == [f"plain_name_check: {repo / 'docs' / 'gone.md'} is not there"]


def test_the_wrong_interpreter_stops_it_before_it_reads_anything(repo, capsys, monkeypatch):
    """The pin is the first statement of main(), not a comment about one. Told the
    interpreter is wrong, it returns that status and does not go on to read the
    file with the code in it."""
    (repo / "docs" / "untracked.md").write_text(f"raised as {PLANTED}\n")
    monkeypatch.setattr(
        plain_name_check.interpreter_pin, "enforce", lambda: interpreter_pin.WRONG_INTERPRETER
    )

    status, lines = run(capsys, "--changed", "--baseline", "baseline")

    assert status == interpreter_pin.WRONG_INTERPRETER
    assert lines == []


def test_an_unresolvable_baseline_is_not_a_pass(repo, capsys):
    status, _ = run(capsys, "--changed", "--baseline", "no-such-ref")

    assert status == plain_name_check.CANNOT_RUN


def test_a_path_that_is_not_there_is_not_a_pass(tmp_path, capsys):
    """Silence about a file it never opened reads like silence about a clean one."""
    status, lines = run(capsys, str(tmp_path / "no_such_report.md"))

    assert status == plain_name_check.CANNOT_RUN
    assert lines == [f"plain_name_check: {tmp_path / 'no_such_report.md'} is not there"]


def test_neither_changed_nor_a_path_is_refused():
    with pytest.raises(SystemExit):
        plain_name_check.main([])


# --- the two entry points, and the hook that calls one of them ---------------


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


def _without_pythonpath() -> dict[str, str]:
    return {key: value for key, value in os.environ.items() if key != "PYTHONPATH"}


@pytest.mark.skipif(shutil.which("python3.12") is None, reason="no bare python3.12 here")
@pytest.mark.parametrize(
    "entry_point",
    [("-m", "src.plain_name_check"), ("src/plain_name_check.py",)],
)
def test_both_entry_points_run_under_the_bare_pinned_interpreter(tmp_path, entry_point):
    """The module form is what the hook calls; the script form is what a person types."""
    document = tmp_path / "notes.md"
    document.write_text(f"raised as {PLANTED}\n")

    result = subprocess.run(
        ("python3.12", *entry_point, str(document)),
        cwd=REPO_ROOT,
        env=_without_pythonpath(),
        capture_output=True,
        text=True,
    )

    assert result.returncode == plain_name_check.FOUND
    assert result.stderr.splitlines() == [f"{document}:1: {PLANTED}"]


def _post_write_hooks() -> list[tuple[str, str]]:
    """Every post-write hook that runs this module, as (matcher, command)."""
    settings = json.loads((REPO_ROOT / ".claude" / "settings.json").read_text(encoding="utf-8"))
    return [
        (entry.get("matcher", ""), hook["command"])
        for entry in settings["hooks"]["PostToolUse"]
        for hook in entry["hooks"]
        if "plain_name_check" in hook["command"]
    ]


def test_the_post_write_hook_calls_this_module():
    hooks = _post_write_hooks()

    assert len(hooks) == 1
    matcher, _ = hooks[0]
    assert matcher == "Write|Edit"


def _repo_that_can_run_the_check(tmp_path):
    """A throwaway repository carrying the module, a baseline, and a planted code."""
    (tmp_path / "src").mkdir(exist_ok=True)
    for name in ("__init__.py", "interpreter_pin.py", "plain_name_check.py"):
        shutil.copy(REPO_ROOT / "src" / name, tmp_path / "src" / name)
    git(tmp_path, "init", "-q", "-b", "main")
    git(tmp_path, "config", "user.email", "test@example.invalid")
    git(tmp_path, "config", "user.name", "test")
    git(tmp_path, "add", "-A")
    git(tmp_path, "commit", "-qm", "baseline")
    git(tmp_path, "update-ref", "refs/remotes/origin/main", "HEAD")
    (tmp_path / "report.md").write_text(f"the finding was raised as {PLANTED}\n")
    return tmp_path


def _names_the_planted_code(command: str, repo: Path):
    """Run one gate command in the throwaway repository and read what it said."""
    result = subprocess.run(
        ("sh", "-c", command),
        cwd=repo,
        env=_without_pythonpath(),
        capture_output=True,
        text=True,
    )
    assert result.stderr.splitlines() == [f"report.md:1: {PLANTED}"]
    assert result.returncode == plain_name_check.FOUND


def test_the_gate_runs_the_check(tmp_path):
    """A code named on stderr is for whoever is at the keyboard; the gate is what
    makes a pull request red. Proof by running the command make says it will run,
    not by reading the Makefile and believing it."""
    printed = subprocess.run(
        ("make", "-n", "check", f"PYTHON={sys.executable}", "BASELINE=origin/main"),
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    command, = [line for line in printed.splitlines() if "plain_name_check" in line]

    _names_the_planted_code(command, _repo_that_can_run_the_check(tmp_path))


def test_the_workflow_runs_that_same_gate():
    """One gate, defined once. If the workflow listed the steps itself, this check
    could be added to the Makefile and never run on a pull request. Read only the
    steps -- a comment naming what the gate contains is a comment, not a step."""
    workflow = (REPO_ROOT / ".github" / "workflows" / "ci.yml").read_text()
    steps = [line.split("run:", 1)[1].strip() for line in workflow.splitlines() if "run:" in line]

    assert "make check PYTHON=python BASELINE=origin/main" in steps
    assert not [step for step in steps if "src.append_check" in step or "pytest" in step]


@pytest.mark.skipif(shutil.which("python3.12") is None, reason="no bare python3.12 here")
def test_the_post_write_hook_names_a_planted_code_and_keeps_the_exit_status(tmp_path):
    """Proof that the hook is wired in, not just written: run the line itself."""
    (_, command), = _post_write_hooks()

    _names_the_planted_code(command, _repo_that_can_run_the_check(tmp_path))
