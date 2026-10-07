# What the SessionStart hook prints: the head of lessons.md and its newest
# lessons, newest last, in at most sixty lines.
#
# `cat lessons.md` printed about three hundred and twenty lines into every
# session. The owner's research note of 2026-10-06 (docs/structure_changes.md)
# is that prose rules are followed inconsistently and instructions should stay
# near a hundred lines; CLAUDE.md is twenty-two of them. Lessons a script or a
# test already enforces moved to archive/lessons_enforced.md, and this prints
# the rest from the newest backwards, so the cap costs the oldest lessons first.
#
# A lesson starts with a date, YYYY-MM-DD and a space; a line after the first
# lesson that does not start with a date is a continuation of the lesson before
# it (a wrapped line), printed with it and counted within it, never dropped.
# Everything above the first lesson is the header, printed before any lesson.
# A lesson prints whole or not at all. When the lessons do not all fit, one
# line says how many older ones were left out and where they are, and that
# line counts toward the sixty. When the header alone leaves no room for that
# line, the first fifty-nine header lines print and the sixtieth says how many
# header lines and lessons were left out, so the cap holds through this script
# and not only through the shape of the file it is given. That a lesson line
# carries its date is not this
# script's judgment: src/instruction_length_check.py refuses one that does not,
# in `make check`, so an undated lesson is refused there rather than hidden here.
#
# Invoked as `sh tools/session_start_lessons.sh [file]` from the repository
# root, so a missing execute bit cannot silence it. Exit 2 when the file cannot
# be read: a hook that prints nothing reads exactly like a file with nothing in
# it, and they are not the same.

set -u

file="${1:-lessons.md}"
limit=60

if [ ! -r "$file" ]; then
  echo "session_start_lessons: $file cannot be read" >&2
  exit 2
fi

awk -v limit="$limit" -v file="$file" '
  /^[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] / { lesson[++n] = $0; size[n] = 1; started = 1; next }
  started { lesson[n] = lesson[n] "\n" $0; size[n]++; next }
  { header[++h] = $0 }
  END {
    if (h + (n > 0) > limit) {
      for (i = 1; i < limit; i++) print header[i]
      print "(" h - limit + 1 " header lines and " n " lessons are in " file " and not printed here.)"
      exit
    }
    for (i = 1; i <= h; i++) print header[i]
    total = h
    for (i = 1; i <= n; i++) total += size[i]
    if (total <= limit) {
      first = 1
    } else {
      room = limit - h - 1
      first = n + 1
      used = 0
      while (first > 1 && used + size[first - 1] <= room) {
        first--
        used += size[first]
      }
      older = first - 1
      print "(" older " older lessons are in " file " and not printed here.)"
    }
    for (i = first; i <= n; i++) print lesson[i]
  }
' "$file"
