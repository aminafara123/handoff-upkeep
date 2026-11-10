#!/usr/bin/env bash
# Compact evidence pack for the end-of-session handoff update. Usage: evidence.sh PATH/TO/HANDOFF.md
# Runs nothing from the project. Prints under 30 lines, about 250 tokens.
f="${1:?usage: evidence.sh PATH/TO/HANDOFF.md}"
dir="$(cd "$(dirname "$f")" && pwd)"
d="$(tr '\n' ' ' < "$f" | grep -oE 'Last updated[^0-9]{0,5}[0-9]{4}-[0-9]{2}-[0-9]{2}' | grep -oE '[0-9-]{10}' | head -1)"
if git -C "$dir" rev-parse 2>/dev/null; then
  log="$(git -C "$dir" log --since="${d:-1970-01-01} 00:00" --format='%h %s')"
  subj="$(printf '%s\n' "$log" | grep . | head -15 | awk '{h=$1; sub(/^[^ ]+ /, ""); print h, substr($0, 1, 80)}')"
  pre="$(printf '%s\n' "$subj" | cut -d' ' -f2 | sort -u)"  # a prefix every subject shares is printed once
  case "$pre" in *:) [ "$(printf '%s\n' "$subj" | grep -c .)" -gt 1 ] && subj="$(printf '%s\n' "$subj" | sed "s/ $pre / /")" && note=", all start '$pre'" ;; esac
  echo "Last updated ${d:-NOT FOUND}, commits since: $(printf '%s' "$log" | grep -c .)${note}"
  [ -n "$subj" ] && printf '%s\n' "$subj"
  st="$(git -C "$dir" status --short | head -10)"
  echo "git status: ${st:-clean}"
else
  echo "Last updated ${d:-NOT FOUND}, not a git repo"
fi
tests="$(awk '/^## /{p=/First ten minutes/} p' "$f" | grep -oE '`[^`]*(pytest|npm (run )?test)[^`]*`' | head -2)"
echo "Tests (not run): ${tests:-none named in First ten minutes}"
for sub in runs logs; do
  [ -d "$dir/$sub" ] || continue
  newest="$(ls -t "$dir/$sub" | head -1)"
  [ -n "$newest" ] && echo "$sub/$newest: $(tail -n 1 "$dir/$sub/$newest" | cut -c1-100)"
done
