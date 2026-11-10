Sanitized excerpt of a real handoff from a live one-person SaaS, November 2026. Shortened, personal details removed.

# CoiPatrol: start here

Read this first in any new session. It says what the business is, the goal and strategy,
where everything lives, what is done, what is next, and how the owner wants work done.
Last updated 2026-11-10.

## What this is
CoiPatrol is certificate of insurance (COI) tracking software for small US construction
firms and property managers. An office admin uploads a subcontractor's ACORD 25 PDF, the
app reads carrier, limits and dates, checks them against the company's requirements,
shows a green/yellow/red dashboard, and sends renewal reminders to the sub.
Owner: one person, UTC+4, 10 years IT operations, non-developer. Everything is built and
run by Claude Code sessions in the repo.
Live: site https://coipatrol.com, app https://app.coipatrol.com, billing on Dodo Payments.
Revenue so far: none. Total spend: about $21 a year.

## Goal and strategy
Why this exists: a one-person online business that runs on agents, so the owner's time
goes to decisions, accounts and people. Success, in order:
1) The first paying customer. Then the app moves to a $5 VPS.
2) A steady 1 to 5 replies per 150 cold emails turning into trials.
3) Recurring income that pays for the agents and the API.
Decision points:
- Dec 15 2026: first 150 cold emails out. Zero replies means fix deliverability or copy.
- Jan 31 2027: no paying customer means feature building stops, February goes to the funnel.
- Apr 30 2027: still none means the owner decides whether the product continues.
How we win: match what the $20 to $99 trackers offer at the same price, and feel better.
Paid ads are out, they break even only on the $99 plan.

## Map of the folder
- `app.py`: the whole app (FastAPI + Jinja2 + SQLite, single file). `templates/` pages.
  241 tests: `../../.venv/bin/python -m pytest -q` from this folder.
- `scripts/`: `health.sh` checks the whole stack and prints PASS or FAIL lines.
  `restart-app.sh` restarts only the app by port. `deploy-site.sh "msg"` builds and
  deploys the site and confirms the new build is live.
- `marketing/site/`: the static site. Edit `tools/pages/*.html` sources only.
- `growth/`: `outreach.py` (cold email sender with hard caps and suppression).

## Secrets and accounts (locations only, never copy values into docs)
- A private env file outside the repo, sourced by the start script: SMTP, payments,
  outreach mailbox, webhook secret.
- Tunnel credentials in the cloudflared config folder.
- Accounts: Cloudflare, Spaceship (registrar), GitHub Pages, Dodo Payments, Brevo,
  Zoho Mail, G2, Search Console. The owner holds all logins.

## Rules for working with the owner
1) Copy-paste text: no em-dashes, no semicolons, numbered lists as "1) ".
2) Research is acted on only after its five load-bearing claims are fetched and quoted.
3) No fake statistics, testimonials, reviews, users or experience, anywhere, ever.
4) Questions to the owner: few, concrete, with options to tick. He reads on his phone.

## First ten minutes of a session
1) `git log --oneline -5` and `git status --short`. Uncommitted changes mean a session
   is open right now or died mid-work: ask the owner before touching the same files.
2) `bash saas-lab/coipatrol/scripts/health.sh`. All PASS is normal.
3) Read the last line of yesterday's and today's files in `runs/`. "exit 0" is clean.
4) Read the owner's todo file. "For me" items are his, "Claude" items are yours.
5) Do not re-plan. Work comes from the todo file, "What is next" and today's request.

## What is done (short history)
- Oct 26: Dodo Payments approved (individual, no licence), billing verified with a test
  card, flipped to live.
- Nov 2: six-day tunnel outage found (cloudflared self-update), fixed with
  --no-autoupdate plus a watchdog.
- Nov 5: WSL shut its VM down when the last console closed, taking app and tunnel with
  it. Replaced the Startup-folder launcher with a hidden scheduled task.
- Nov 10: routines moved to per-routine tool allowlists. YEAR10 code at checkout.
  Camera photos on all three certificate upload forms. 241 tests.

## What is next (dates matter)
- Nov 11: first canary results. Read the outreach log in runs/ and check the inbox.
- Nov 16: the 16 vendor-page property managers, then 15 a day.
- Owner tests "Take a photo" on a real phone. Every reader call in the tests is faked.
- First yearly customer with YEAR10: check the renewal a year later is full price.

## Known weak spots
- The app runs on the owner's home PC. Reboots and WSL shutdown are handled by the
  scheduled task, hardware failure is not. Move to a $5 VPS at the first paying customer.
- The demo is one shared account that resets on each click.
- AI extraction runs inside the web request, a slow read blocks other requests briefly.

## Agents and routines
- One-task agents in `.claude/agents/`, each with its model in the frontmatter (haiku
  for ops, opus for the builder, sonnet for the rest).
- Windows schedule through `scripts/run-routine.sh`: ops daily 08:30, outreach weekdays
  17:30, competitor watch monthly. Logs land in `runs/`.
- Each routine runs in dontAsk mode with its own tool allowlist.

## Decisions and why (do not reopen without new evidence)
- Dodo Payments, not Stripe or Paddle: every Stripe-based platform demands a UAE trade
  licence, Dodo verified the owner as an individual. Fee about 5.3%, accepted.
- Home PC through a Cloudflare tunnel, not a VPS: $0 until the first paying customer.
- Reader on Claude Sonnet 5.5: on the 18-certificate eval Sonnet sent 0 to review.
- Never chase TrackMyVendor ($39 unlimited) or SubDoc ($20) on price.

### Tried and rejected, do not retry
- Lemon Squeezy for billing: refused, it needs a UAE trade licence (Oct 20).
- Startup-folder launcher: died with WSL when the last console closed (Nov 5).
- Haiku as the reader: sent 5 of 18 certificates to review (Nov 5).
- Automated UptimeRobot sign-up: blocked by a Cloudflare human check (Nov 10).
- Uptime check polling /demo: it answers 303, every run failed. Poll /login (Nov 6).

## Key numbers
- Plans: Free 20 subs, Growth 50 at $49, Pro 250 at $99, Business 1,000 at $199 a month.
- Uploads: 10 MB cap. Certificates as PDF, JPG or PNG.
- Outreach: 25 per run, 40 a day, 2 touches per lead.
- Ports: app 8030, Ollama 11434, site preview 8040.

## Renewals and expiries
- coipatrol.com: Spaceship, bought Oct 16 2026, auto-renew OFF. Renew by Oct 2027.
- Claude Code token for the routines: made Nov 6 2026, lasts about a year. Renew with
  `claude-work setup-token` and replace the token file.
- Zoho Mail Lite: paid yearly from Nov 2 2026, renews Nov 2027.

## Gotchas that cost time
- The shell's working directory resets between tool calls. Absolute paths everywhere.
- `pkill -f 'uvicorn app:app'` matches the tool's own shell and kills the session.
  restart-app.sh kills by port.
- A template change needs an app restart, the running process renders old templates.
- GitHub scheduled workflows run a few times a day at best, whatever cron you write.

## Words we use
- Sub: a subcontractor or vendor whose certificate we track. COI: certificate of insurance.
- Canaries: the first 3 cold emails a day to lower-tier leads, to test deliverability.
- GO line: "- [x] GO cold email" in the owner's todo, the only thing that lets outreach send.
- Routine: a headless scheduled run. Run: one execution, logged in runs/.
