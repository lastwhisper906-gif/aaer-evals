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
# A lesson is a line that starts with a date, YYYY-MM-DD and a space. Everything
# above the first lesson is the header and is always printed. When the lessons
# do not all fit, one line says how many older ones were left out and where they
# are, and that line counts toward the sixty.
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
  /^[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] / { lesson[++n] = $0; started = 1; next }
  !started { header[++h] = $0 }
  END {
    for (i = 1; i <= h; i++) print header[i]
    if (h + n <= limit) {
      first = 1
    } else {
      room = limit - h - 1
      if (room < 0) room = 0
      first = n - room + 1
      older = first - 1
      print "(" older " older lessons are in " file " and not printed here.)"
    }
    for (i = first; i <= n; i++) print lesson[i]
  }
' "$file"
