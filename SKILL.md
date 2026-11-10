---
name: handoff-upkeep
description: |
  Keep a project's start-here file (HANDOFF.md) complete and current, in three sizes, lite,
  standard and full, so every new AI session starts with full context instead of re-asking,
  re-planning or rebuilding what already shipped.
  A check script, claim tags for unverified facts and a do-not-retry list keep it honest.
  Use at the end of any session where real work happened, right after any decision, outage,
  new account, renewal date or changed number, and to create a handoff where none exists.
  The start of a session needs only the handoff and check_handoff.py --quiet. Triggers:
  "update the handoff", "is the handoff up to date", "what does a new session need",
  "write a start-here file", "end of session", "wrap up", "make sure the next session is not lost".
version: 1.3.0
docs_url: https://claude.ai/artifact/RVWvmKjjiap2FvYyEZKz5W
summary: One start-here file per project, kept true, so no AI session is ever lost or rebuilds what shipped.
tags: [handoff, context, documentation, claude-code, agents, memory, onboarding, runbook]
keywords: [handoff, HANDOFF.md, session context, start here, project memory, decisions log, runbook]
use_cases:
  - End a session with the handoff updated, checked and committed
  - Start a session from the handoff and quiet check
  - Create a handoff, asking the owner five questions
  - Keep decisions, numbers and renewals settled
---

# Handoff upkeep

`H` is the handoff, `S` this skill's folder. references/SECTIONS.md: the fifteen sections,
creating a handoff, the five owner questions. check_handoff.py explains each check in --help.

## Profiles

Three sizes: lite (5 sections), standard (10), full (15). Declare one on its own line under
"Last updated": `Profile: standard`. No line means full. To upgrade, change the line and add
the sections the check names as missing. Switches: `, no-tags` drops the [?] check,
`, no-archive` drops the history check. Start one with `check_handoff.py --new lite H`.

## Start of a session

The start needs only the handoff and `check_handoff.py --quiet`. Load this skill once, at the end, or when creating a handoff.
1) Read H, then `python3 S/scripts/check_handoff.py H --quiet` (`--repo DIR` if H is outside the repo).
2) Resolve each "[?]" line with a command that proves it. Fix each FAIL and each truly
   shipped "maybe shipped" bullet in its own commit.
3) Run its "First ten minutes". Another session active within the hour: the owner picks one.

## End of a session

Also after any decision, outage, account, renewal or changed number.
1) Run `bash S/scripts/evidence.sh H` and edit from its output, not from chat memory.
2) What is done: one dated entry, at most 5 lines: shipped, broken and fixed, new numbers.
3) What is next: drop shipped bullets, nearest date first, add what the owner agreed.
4) Decisions and why: today's, each with reason and date. Failed approaches, with the
   reason, go under "Tried and rejected, do not retry".
5) Update numbers, renewals, gotchas and words. Drop gotchas fixed in code. Goal and
   strategy change only with a reason in Decisions.
6) Set "Last updated" to today. One line to the owner's notes app, if any.
7) Rerun the check until no FAIL, and quote it.
8) Commit the handoff, with its work or alone.

## Claim tags

A fact from chat memory alone, not confirmed this session by a command, file read or tool
result, ends with "[?]". The next session resolves those first. The check warns past 7 days.

## Degradation trigger

Contradicted a decision, re-derived a settled fact, misremembered a path or asked
what the handoff answers? Say so to the owner and write the history entry now. Same when
context runs low or the session runs long.

## Rules

- Facts over narrative. Absolute dates ("Nov 6, 2026"), never "yesterday".
- Nothing pending that shipped, nothing shipped listed as pending.
- A decision without its reason gets reopened.
- Secret locations, never values: the file is shared.
- Unknowns read "ask the owner: <question>", never TODO or TBD.
- Paths and commands, not code. One handoff per project, detail in linked files.
- Short lines, plain words, the owner's style rules.
- One fact per line, numbers in tables not prose. History entries at most 5 lines, details in git.
- Keep the newest 6 history entries, archive the rest to HANDOFF-HISTORY.md with one pointer
  line. Under 350 lines (warn 400, fail 600).
