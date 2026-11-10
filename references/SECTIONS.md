# Handoff sections, in this order

| Section | lite | standard | full |
|---|---|---|---|
| What this is | yes | yes | yes |
| Goal and strategy | | yes | yes |
| Map of the folder | | yes | yes |
| Secrets and accounts | | | yes |
| Rules for working with the owner | | yes | yes |
| First ten minutes of a session | yes | yes | yes |
| What is done | | yes | yes |
| What is next | yes | yes | yes |
| Known weak spots | | | yes |
| Agents and routines | | | yes |
| Decisions and why | yes | yes | yes |
| Key numbers | | yes | yes |
| Renewals and expiries | | | yes |
| Gotchas that cost time | yes | yes | yes |
| Words we use | | | yes |

Declare the size under Last updated, for example `Profile: standard, no-tags`. No line means full.
`no-tags` turns off the [?] check, `no-archive` turns off the history check.

Read this when creating a handoff from scratch or when unsure what belongs in a section.

The test a handoff must pass: a capable stranger who knows the domain but has none of the
chat history can continue the work without asking a question the owner already answered.
Most handoffs fail in three ways: they say what the product is but not why it exists, they
list as pending things that already shipped, and they lose the reasons behind decisions.

1) What this is: product, customer, owner (role, time zone, skill level), what is live,
   revenue and users so far, yearly spend. Ten lines.
2) Goal and strategy: why the project exists, what success is in order, decision dates
   (what happens if a milestone is missed by a date), who buys, how we win, how customers
   arrive, how the work is run. The section most handoffs lack.
3) Map of the folder: every top-level path and what it holds, which scripts to run instead
   of doing steps by hand, where tests are and how to run them.
4) Secrets and accounts: locations only, never values. Which accounts exist, who holds them.
5) Rules for working with the owner: copy rules, what to never fabricate, what needs their
   go, how to ask them questions, where their todos live.
6) First ten minutes of a session: a numbered checklist (git log and status, health check,
   last run logs, the owner's todo file, when to run tests, do not re-plan, what to do if
   another session is open, which command and config dir to use). Name the test command
   here in backticks, evidence.sh prints it.
7) What is done: dated history, one entry per work session, facts and numbers, newest last.
8) What is next: dated steps, nearest first. Nothing that already shipped.
9) Known weak spots: what can break, what is not handled, when it gets fixed.
10) Agents and routines: automated jobs, schedule, model, logs, how to change them.
11) Decisions and why: one line per decision with its reason and date. Marked "do not
    reopen without new evidence". Ends with the subsection "Tried and rejected, do not
    retry": one line per approach that failed, with the reason it failed.
12) Key numbers: prices, limits, caps, schedules, ports, spend. The numbers a session
    would otherwise grep for.
13) Renewals and expiries: domains, tokens, certificates, paid plans, with dates and the
    command or page that renews each.
14) Gotchas that cost time: trigger and action, one line each. Remove one once it is
    fixed in code.
15) Words we use: the project's vocabulary and the owner's shorthand.

## Density and archive rules

The handoff is read in full by every session, so every line costs tokens each time.
1) One fact per line. A long aside in brackets becomes its own line or goes.
2) Numbers go in tables or Key numbers, not in prose.
3) No filler: "basically", "essentially", "in order to", "it is worth noting", "note that".
4) A What is done entry is at most 5 lines. The details live in git and the commits.
5) Keep the newest 6 entries in What is done. Move older ones, unchanged, to
   HANDOFF-HISTORY.md beside the handoff. Keep one pointer line at the top of the
   section, not a bullet, naming the date range it holds.
6) When trimming an entry to 5 lines, move the full text to HANDOFF-HISTORY.md first,
   so no number, name or date is lost.
7) Target under 350 lines. check_handoff.py warns over 400 and fails over 600.
8) A section that outgrows its share moves detail to a linked file, with one pointer
   line on what that file answers.
check_handoff.py warns on 1 to 5 (density, history) and on size. Rules, First ten
minutes, Gotchas and Words are exempt from the density check.

## What the check script cannot judge

- A number or name in the file that the code or status output reports differently
  (a model name, a port, a count, a price) is a stale fact. Compare by hand when a
  session touched it.
- Relative time words in a procedure ("read yesterday's log") are fine. The script skips
  the First ten minutes, Rules and Gotchas sections and possessives like "today's".
- The owner's style rules apply to the handoff too (for example no em-dashes).

## Creating a handoff for a project that has none

1) For lite or standard, run `check_handoff.py --new lite HANDOFF.md` in the project root.
   For full, copy `references/HANDOFF-TEMPLATE.md` there as `HANDOFF.md`.
   See `examples/HANDOFF-example.md` for a filled one.
2) Fill from the repo first: README, git log, config files, scripts, tests, deploy files.
3) Ask the owner only the five questions below, in one message, with options to tick
   where the answer is a choice. Mark anything still unknown as "ask the owner: <question>".
4) Point the project's instruction file (CLAUDE.md, AGENTS.md or equivalent) at the
   handoff with one line: read it first, keep it current with this skill.
5) Run `check_handoff.py HANDOFF.md` and fix every FAIL.

The five owner questions:
1) Why does this exist and what does success look like, in order? Is there a date by
   which "no result" means a change of plan?
2) Who is the user or buyer, and who is the owner (role, time zone, how technical)?
3) What must never happen (fabricated claims, a channel that must not be used, a limit
   that must not be raised)?
4) Where do secrets and accounts live, and who holds the logins?
5) What renews or expires, and when?
