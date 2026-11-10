# <Project>: start here

Read this first in any new session. It says what the project is, the goal and strategy, where
everything lives, what is done, what is next, and how the owner wants work done. Last updated
<YYYY-MM-DD>.
Profile: full

## What this is
<Product in two sentences. Who uses it. Owner: name or role, time zone, how technical.>
<What is live, with URLs. Revenue and users so far. Spend per year.>

## Goal and strategy
Why this exists: <one or two sentences>.
Success, in order:
1) <first milestone>
2) <second>
3) <third>
Decision points:
- <date>: <what a miss means and what happens then>
Who buys or uses it: <the person, their job, what they struggle with>.
How we win: <three to six bullets, each a choice we made and why>.
How customers or users arrive, ranked: <channels in order of expected yield, and what is ruled out>.
How the work is run: <who decides, who builds, what runs unattended, what counts as evidence>.

## Map of the folder
- `<path>`: <what it holds>. <How to run or test it.>
- `scripts/`: <run these instead of doing steps by hand, one line each>.

## Secrets and accounts (locations only, never values)
- `<path to env or vault>`: <which secrets live there>.
- Accounts: <service (what it is for, who holds the login)>, ...

## Rules for working with the owner
1) <copy and style rules>
2) <what is never fabricated>
3) <what needs the owner's go before it happens>
4) <how to ask them questions>
5) <where their todos live and how to tick them>

## First ten minutes of a session
1) `python3 <skill path>/scripts/check_handoff.py HANDOFF.md --quiet`. One summary line is clean.
2) Resolve any [?] lines it lists: run the command that proves each, then drop the tag or fix the line. Fix any FAIL and any "maybe shipped" bullet that really shipped.
3) `git log --oneline -5` and `git status --short`. Uncommitted changes you did not make mean another session is open or died mid-work. Ask before touching the same files.
4) <health or status command>. What normal looks like.
5) <where run logs land and what a clean run says>.
6) Read the owner's todo file. <Which items are theirs, which are yours.>
7) <when to run tests and how long they take>.
8) Do not re-plan. Work comes from the todo file, "What is next" below, and today's request.
9) <which command and config dir to use if there is more than one>.

## What is done (short history)
Older entries: HANDOFF-HISTORY.md (<date range>). Newest 6 here, newest last, 5 lines each.
- <YYYY-MM-DD>: <what shipped, what broke and the fix, numbers that changed>.

## What is next (dates matter)
- <date or trigger>: <step>.

## Known weak spots
- <what can break, what is not handled, when it gets fixed>.

## Agents and routines
- <job: schedule, model, log location, how to change it>.

## Decisions and why (do not reopen without new evidence)
- <decision>: <reason>, <date>.

### Tried and rejected, do not retry
- <approach>: <why it failed>, <date>.

## Key numbers
- <prices, limits, caps, schedules, ports, spend>.

## Renewals and expiries
- <thing>: <provider>, <date>, <renewal command or page>, <what breaks if missed>.

## Gotchas that cost time
- <when X happens, do Y>.

## Words we use
- <term>: <meaning>.
