"""instruction_length_check has to pass 22 lines and name the 23rd, name an undated lesson, a missing path and an empty deny list.

The cap is `docs/HOW_WE_WORK.md`'s: "`CLAUDE.md` is capped at 22 lines". The
files below are planted by this file with a line count written out by hand.

The date rule is `lessons.md`'s header's: every lesson starts with its date,
YYYY-MM-DD and a space. The planted lessons file has a two-line header, three
dated lessons, one indented line under the second (the shape of
`archive/lessons_enforced.md`, whose note sits under each lesson), and the
undated line is planted at a line number written out by hand.

The path rule's second lens, fourth reading: `CLAUDE.md` line 19 writes
`tools/session_start_lessons.sh).`, and a token stripped of brackets but not of
the full stop was never checked, so the one path that change added was the one
the rule could not see. The tests below plant a path before `).` and read the
real `CLAUDE.md` for that line. The deny half of line 12 is the same reading:
`.claude/settings.json denies the tools` was true if the file existed, so the
tests plant settings files with and without the two deny entries.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from src import instruction_length_check

REPO_ROOT = Path(__file__).resolve().parent.parent
DATED_LESSONS = [
    "# Lessons",
    "",
    "2026-09-06 the first lesson.",
    "2026-09-07 the second lesson.",
    "  (was line 8) enforced by: `src/append_check.py`, run by `make check`.",
    "2026-09-08 the third lesson.",
]


def plant(tmp_path: Path, lines: int) -> Path:
    path = tmp_path / "CLAUDE.md"
    path.write_text("".join(f"- rule {n}\n" for n in range(1, lines + 1)), encoding="utf-8")
    return path


def plant_lessons(tmp_path: Path, lines: list[str]) -> Path:
    path = tmp_path / "lessons.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def test_twenty_two_lines_are_within_the_cap(tmp_path, capsys):
    assert instruction_length_check.main(["--file", str(plant(tmp_path, 22))]) == 0
    assert capsys.readouterr().err == ""


def test_twenty_three_lines_are_named(tmp_path, capsys):
    path = plant(tmp_path, 23)

    assert instruction_length_check.main(["--file", str(path)]) == instruction_length_check.FOUND
    assert capsys.readouterr().err.splitlines() == [
        f"{path}:23: 23 lines, over the cap of 22; replace a line rather than append one"]


def test_a_last_line_with_no_newline_still_counts(tmp_path):
    path = plant(tmp_path, 22)
    path.write_text(path.read_text(encoding="utf-8") + "- one more", encoding="utf-8")

    assert instruction_length_check.main(["--file", str(path)]) == instruction_length_check.FOUND


def test_a_file_that_is_not_there_cannot_be_judged(tmp_path):
    assert (instruction_length_check.main(["--file", str(tmp_path / "CLAUDE.md")])
            == instruction_length_check.CANNOT_RUN)


def test_dated_lessons_with_an_indented_note_pass(tmp_path, capsys):
    lessons = plant_lessons(tmp_path, DATED_LESSONS)

    assert instruction_length_check.main(
        ["--file", str(plant(tmp_path, 22)), "--lessons", str(lessons)]) == 0
    assert capsys.readouterr().err == ""


def test_an_undated_lesson_is_named_with_its_line(tmp_path, capsys):
    lessons = plant_lessons(tmp_path, DATED_LESSONS + ["a lesson written without its date."])

    assert instruction_length_check.main(
        ["--file", str(plant(tmp_path, 22)), "--lessons", str(lessons)]
    ) == instruction_length_check.FOUND
    assert capsys.readouterr().err.splitlines() == [
        f"{lessons}:7: a lesson starts with its date, YYYY-MM-DD and a space; "
        "this line does not: a lesson written without its date."]


def test_a_heading_after_the_lessons_is_not_a_lesson(tmp_path, capsys):
    """The archive's `## Moved back` section: a heading, then dated lines."""
    lessons = plant_lessons(tmp_path, DATED_LESSONS + [
        "", "## Moved back", "", "2026-10-07 (was line 2) the second lesson went back."])

    assert instruction_length_check.main(
        ["--file", str(plant(tmp_path, 22)), "--lessons", str(lessons)]) == 0
    assert capsys.readouterr().err == ""


def test_an_undated_line_under_a_heading_is_still_named(tmp_path, capsys):
    lessons = plant_lessons(tmp_path, DATED_LESSONS + ["", "## Moved back", "", "a line with no date."])

    assert instruction_length_check.main(
        ["--file", str(plant(tmp_path, 22)), "--lessons", str(lessons)]
    ) == instruction_length_check.FOUND
    assert capsys.readouterr().err.splitlines() == [
        f"{lessons}:10: a lesson starts with its date, YYYY-MM-DD and a space; "
        "this line does not: a line with no date."]


def test_the_header_above_the_first_lesson_is_not_a_lesson(tmp_path, capsys):
    lessons = plant_lessons(tmp_path, ["# Lessons", "", "One line per mistake.", ""] + DATED_LESSONS[2:])

    assert instruction_length_check.main(
        ["--file", str(plant(tmp_path, 22)), "--lessons", str(lessons)]) == 0
    assert capsys.readouterr().err == ""


def test_a_lessons_file_with_no_dated_line_is_refused_not_passed(tmp_path, capsys):
    lessons = plant_lessons(tmp_path, ["# Lessons", "", "One line per mistake.", ""])

    assert instruction_length_check.main(
        ["--file", str(plant(tmp_path, 22)), "--lessons", str(lessons)]
    ) == instruction_length_check.CANNOT_RUN
    assert capsys.readouterr().err.splitlines() == [
        f"{lessons}: no dated lesson; a lessons file that yields no lesson is not an empty one"]


def test_a_lessons_file_with_one_dated_line_is_judged(tmp_path, capsys):
    lessons = plant_lessons(tmp_path, ["# Lessons", "", "2026-09-06 the only lesson."])

    assert instruction_length_check.main(
        ["--file", str(plant(tmp_path, 22)), "--lessons", str(lessons)]) == 0
    assert capsys.readouterr().err == ""


def test_a_lessons_file_that_is_not_there_cannot_be_judged(tmp_path):
    assert instruction_length_check.main(
        ["--file", str(plant(tmp_path, 22)), "--lessons", str(tmp_path / "lessons.md")]
    ) == instruction_length_check.CANNOT_RUN


def test_this_repository_s_lessons_files_are_dated():
    for path in instruction_length_check.LESSONS:
        assert instruction_length_check.undated_lessons(path) == []


# The planted CLAUDE.md for the path rule: twenty-two lines, two of which name
# paths. Line 3 names a script and a directory that the test plants; line 7
# names a script and a directory that it does not.
PRESENT = "- plain names (src/present_check.py, make check; the record: runs/)"
ABSENT = "- evals/ is the owner's (src/absent_guard.py in CI; the tools are denied)"


def plant_with_paths(tmp_path: Path, present: bool) -> Path:
    lines = [f"- rule {n}" for n in range(1, 23)]
    lines[2] = PRESENT
    if not present:
        lines[6] = ABSENT
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "present_check.py").write_text("", encoding="utf-8")
    (tmp_path / "runs").mkdir()
    path = tmp_path / "CLAUDE.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def test_paths_that_exist_pass(tmp_path, capsys):
    lessons = plant_lessons(tmp_path, DATED_LESSONS)
    path = plant_with_paths(tmp_path, present=True)

    assert instruction_length_check.named_paths(path) == [(3, "src/present_check.py"), (3, "runs/")]
    assert instruction_length_check.main(["--file", str(path), "--lessons", str(lessons)]) == 0
    assert capsys.readouterr().err == ""


def test_a_path_that_is_not_in_the_tree_is_named(tmp_path, capsys):
    lessons = plant_lessons(tmp_path, DATED_LESSONS)
    path = plant_with_paths(tmp_path, present=False)

    assert instruction_length_check.main(
        ["--file", str(path), "--lessons", str(lessons)]) == instruction_length_check.FOUND
    assert capsys.readouterr().err.splitlines() == [
        f"{path}:7: names evals/, which is not in the tree; a rule naming a file that is not "
        "there names nothing",
        f"{path}:7: names src/absent_guard.py, which is not in the tree; a rule naming a file "
        "that is not there names nothing"]


def test_no_paths_turns_the_path_rule_off(tmp_path, capsys):
    lessons = plant_lessons(tmp_path, DATED_LESSONS)
    path = plant_with_paths(tmp_path, present=False)

    assert instruction_length_check.main(
        ["--file", str(path), "--lessons", str(lessons), "--no-paths"]) == 0
    assert capsys.readouterr().err == ""


def test_the_gate_runs_the_check():
    printed = subprocess.run(
        ("make", "-n", "check", f"PYTHON={sys.executable}", "BASELINE=origin/main"),
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    ).stdout
    assert [line for line in printed.splitlines() if "src.instruction_length_check" in line]


# The sentence-punctuation case: the path is the last word of its sentence, so
# the token is `tools/planted_hook.sh).` as CLAUDE.md's line 19 writes its own.
SENTENCED = "- read lessons.md at session start (the hook prints it: tools/planted_hook.sh)."


def plant_sentenced(tmp_path: Path, present: bool) -> Path:
    lines = [f"- rule {n}" for n in range(1, 23)]
    lines[18] = SENTENCED
    if present:
        (tmp_path / "tools").mkdir()
        (tmp_path / "tools" / "planted_hook.sh").write_text("", encoding="utf-8")
    path = tmp_path / "CLAUDE.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def test_sentence_punctuation_comes_off_the_end_of_a_token_and_not_the_front():
    assert instruction_length_check.token_of("tools/x.sh).") == "tools/x.sh"
    assert instruction_length_check.token_of("(tools/x.sh.)") == "tools/x.sh"
    assert instruction_length_check.token_of("`src/x.py`!") == "src/x.py"
    assert instruction_length_check.token_of("src/x.py?") == "src/x.py"
    assert instruction_length_check.token_of("evals/\u2026") == "evals/"
    assert instruction_length_check.token_of(".claude/settings.json") == ".claude/settings.json"
    assert instruction_length_check.token_of("(.claude/settings.json).") == ".claude/settings.json"


def test_a_path_that_ends_a_sentence_is_still_checked(tmp_path, capsys):
    lessons = plant_lessons(tmp_path, DATED_LESSONS)
    path = plant_sentenced(tmp_path, present=False)

    assert instruction_length_check.named_paths(path) == [(19, "tools/planted_hook.sh")]
    assert instruction_length_check.main(
        ["--file", str(path), "--lessons", str(lessons)]) == instruction_length_check.FOUND
    assert capsys.readouterr().err.splitlines() == [
        f"{path}:19: names tools/planted_hook.sh, which is not in the tree; a rule naming a "
        "file that is not there names nothing"]


def test_a_path_that_ends_a_sentence_passes_when_it_is_there(tmp_path, capsys):
    lessons = plant_lessons(tmp_path, DATED_LESSONS)
    path = plant_sentenced(tmp_path, present=True)

    assert instruction_length_check.main(
        ["--file", str(path), "--lessons", str(lessons), "--list"]) == 0
    printed = capsys.readouterr()
    assert printed.err == ""
    assert printed.out.splitlines() == [f"{path}:19: tools/planted_hook.sh in the tree"]


def test_a_ledger_path_is_checked(tmp_path, capsys):
    """`.jsonl` is a path suffix: CLAUDE.md line 7 names `evals/scoreboard.jsonl`."""
    lessons = plant_lessons(tmp_path, DATED_LESSONS)
    lines = [f"- rule {n}" for n in range(1, 23)]
    lines[6] = "- Append-only under runs/ · evals/scoreboard.jsonl: never changed. (src/append_check.py)"
    (tmp_path / "runs").mkdir()
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "append_check.py").write_text("", encoding="utf-8")
    path = tmp_path / "CLAUDE.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    assert instruction_length_check.named_paths(path) == [
        (7, "runs/"), (7, "evals/scoreboard.jsonl"), (7, "src/append_check.py")]
    assert instruction_length_check.main(
        ["--file", str(path), "--lessons", str(lessons)]) == instruction_length_check.FOUND
    assert capsys.readouterr().err.splitlines() == [
        f"{path}:7: names evals/scoreboard.jsonl, which is not in the tree; a rule naming a "
        "file that is not there names nothing"]

    (tmp_path / "evals").mkdir()
    (tmp_path / "evals" / "scoreboard.jsonl").write_text("", encoding="utf-8")
    assert instruction_length_check.main(["--file", str(path), "--lessons", str(lessons)]) == 0
    assert capsys.readouterr().err == ""


def test_this_repository_s_claude_md_names_its_scoreboard_ledger():
    """Line 7 of CLAUDE.md names `evals/scoreboard.jsonl`; the check has to see it."""
    assert (7, "evals/scoreboard.jsonl") in instruction_length_check.named_paths(REPO_ROOT / "CLAUDE.md")


def test_this_repository_s_claude_md_names_the_session_start_hook_and_it_is_there(capsys):
    """Line 19 of CLAUDE.md ends `tools/session_start_lessons.sh).`; the check has to see it."""
    path = REPO_ROOT / "CLAUDE.md"
    hook = "tools/session_start_lessons.sh"

    assert (19, hook) in instruction_length_check.named_paths(path)
    assert (REPO_ROOT / hook).is_file()
    instruction_length_check.main(["--file", str(path), "--list"])
    assert f"{path}:19: {hook} in the tree" in capsys.readouterr().out.splitlines()


# The deny half: the planted CLAUDE.md names a settings file as denying the
# tools, and the settings file planted beside it either holds the two deny
# entries or does not. Everything else the line names is planted present, so
# the only finding left is the one about the deny list.
DENYING = "- evals/ is the owner's (src/eval_guard.py in CI; .claude/settings.json denies the tools)"
DENY_ENTRIES = ["Edit(evals/**)", "Write(evals/**)"]


def plant_denying(tmp_path: Path, settings) -> Path:
    lines = [f"- rule {n}" for n in range(1, 23)]
    lines[11] = DENYING
    (tmp_path / "evals").mkdir()
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "eval_guard.py").write_text("", encoding="utf-8")
    (tmp_path / ".claude").mkdir()
    (tmp_path / ".claude" / "settings.json").write_text(
        settings if isinstance(settings, str) else json.dumps(settings), encoding="utf-8")
    path = tmp_path / "CLAUDE.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def test_a_settings_file_holding_both_deny_entries_passes(tmp_path, capsys):
    lessons = plant_lessons(tmp_path, DATED_LESSONS)
    path = plant_denying(tmp_path, {"hooks": {}, "permissions": {"deny": DENY_ENTRIES}})

    assert instruction_length_check.denying_settings(path) == [(12, ".claude/settings.json")]
    assert instruction_length_check.main(["--file", str(path), "--lessons", str(lessons)]) == 0
    assert capsys.readouterr().err == ""


def test_a_settings_file_with_no_permissions_key_is_named(tmp_path, capsys):
    lessons = plant_lessons(tmp_path, DATED_LESSONS)
    path = plant_denying(tmp_path, {"hooks": {}})

    assert instruction_length_check.main(
        ["--file", str(path), "--lessons", str(lessons)]) == instruction_length_check.FOUND
    assert capsys.readouterr().err.splitlines() == [
        f"{path}:12: says .claude/settings.json denies the tools, but it has no permissions "
        "key; a settings file that denies nothing enforces nothing"]


def test_a_permissions_key_with_no_deny_list_is_named(tmp_path, capsys):
    lessons = plant_lessons(tmp_path, DATED_LESSONS)
    path = plant_denying(tmp_path, {"permissions": {"allow": ["Bash(ls)"]}})

    assert instruction_length_check.main(
        ["--file", str(path), "--lessons", str(lessons)]) == instruction_length_check.FOUND
    assert capsys.readouterr().err.splitlines() == [
        f"{path}:12: says .claude/settings.json denies the tools, but it has no "
        "permissions.deny list; a settings file that denies nothing enforces nothing"]


def test_each_missing_deny_entry_is_named(tmp_path, capsys):
    lessons = plant_lessons(tmp_path, DATED_LESSONS)
    path = plant_denying(tmp_path, {"permissions": {"deny": ["Edit(evals/**)"]}})

    assert instruction_length_check.main(
        ["--file", str(path), "--lessons", str(lessons)]) == instruction_length_check.FOUND
    assert capsys.readouterr().err.splitlines() == [
        f"{path}:12: says .claude/settings.json denies the tools, but it permissions.deny "
        "lacks Write(evals/**); a settings file that denies nothing enforces nothing"]


def test_a_settings_file_that_is_not_json_is_named(tmp_path, capsys):
    lessons = plant_lessons(tmp_path, DATED_LESSONS)
    path = plant_denying(tmp_path, "{not json")

    assert instruction_length_check.main(
        ["--file", str(path), "--lessons", str(lessons)]) == instruction_length_check.FOUND
    assert capsys.readouterr().err.splitlines() == [
        f"{path}:12: says .claude/settings.json denies the tools, but it is not JSON; "
        "a settings file that denies nothing enforces nothing"]


def test_no_paths_turns_the_deny_rule_off_too(tmp_path, capsys):
    lessons = plant_lessons(tmp_path, DATED_LESSONS)
    path = plant_denying(tmp_path, {"hooks": {}})

    assert instruction_length_check.main(
        ["--file", str(path), "--lessons", str(lessons), "--no-paths"]) == 0
    assert capsys.readouterr().err == ""


def test_this_repository_s_claude_md_says_its_settings_file_denies_the_tools():
    """Line 12 of CLAUDE.md makes the claim, so the deny rule reads .claude/settings.json."""
    assert instruction_length_check.denying_settings(REPO_ROOT / "CLAUDE.md") == [
        (12, ".claude/settings.json")]
