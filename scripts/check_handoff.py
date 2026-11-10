#!/usr/bin/env python3
"""Mechanical checks on a HANDOFF.md. Run with --help for the check list."""
import contextlib
import datetime as dt
import io
import os
import re
import subprocess
import sys

SPEC = [  # (heading prefix the check matches, heading and placeholder for --new)
    ("what this is", "What this is", "<product, customer, owner (role, time zone, skill), what is live, revenue>"),
    ("goal and strategy", "Goal and strategy", "<why it exists, success in order, decision dates, how we win>"),
    ("map of the folder", "Map of the folder", "<each top-level path and what it holds, scripts, how to test>"),
    ("secrets and accounts", "Secrets and accounts", "<locations only, never values: each secret and account>"),
    ("rules for working", "Rules for working with the owner", "<copy rules, never fabricate, what needs their go>"),
    ("first ten minutes", "First ten minutes of a session", "<numbered: quiet check, git status, health, tests>"),
    ("what is done", "What is done (short history)", "<one dated entry per session, at most 5 lines, newest last>"),
    ("what is next", "What is next (dates matter)", "<dated steps, nearest first, nothing that already shipped>"),
    ("known weak spots", "Known weak spots", "<what can break, what is not handled, when it gets fixed>"),
    ("agents and routines", "Agents and routines", "<each automated job: schedule, model, logs, how to change it>"),
    ("decisions and why", "Decisions and why", "<decision, reason, date. Then ### Tried and rejected, do not retry>"),
    ("key numbers", "Key numbers", "<prices, limits, caps, schedules, ports, spend>"),
    ("renewals and expiries", "Renewals and expiries", "<what renews or expires, its date, how to renew it>"),
    ("gotchas", "Gotchas that cost time", "<trigger and action, one line each>"),
    ("words we use", "Words we use", "<the project's vocabulary and the owner's shorthand>")]
SECTIONS = [s[0] for s in SPEC]
LITE = {"what this is", "first ten minutes", "what is next", "decisions and why", "gotchas"}
STANDARD = LITE | {"goal and strategy", "map of the folder", "rules for working", "what is done", "key numbers"}
PROFILES = {"lite": LITE, "standard": STANDARD, "full": set(SECTIONS)}
SKIP = {"lite": {"history", "density", "unverified"}, "standard": {"unverified"}, "full": set()}
SWITCHES = {"no-tags": "unverified", "no-archive": "history"}
PROCEDURE = ("first ten minutes", "rules for working", "gotchas")  # relative words are instructions here
RELATIVE = re.compile(r"\b(yesterday|today|tomorrow|recently|soon|last week|next week)\b(?!')", re.I)
UNKNOWN = re.compile(r"\bTODO\b|\bTBD\b|\?\?\?")
SECRETS = re.compile(r"sk-ant-|sk[-_]live|AKIA[0-9A-Z]{12}|ghp_|xoxb-|password=|token=|"
                     r"-----BEGIN [A-Z ]*PRIVATE KEY", re.I)
B64 = re.compile(r"[A-Za-z0-9+/=_-]{40,}")
MONTHS = "jan feb mar apr may jun jul aug sep oct nov dec".split()
DATE = re.compile(r"\b(\d{4})-(\d\d)-(\d\d)\b|\b(" + "|".join(MONTHS) + r")[a-z]* (\d{1,2})\b(?:,? (\d{4}))?", re.I)
STOP = set("about above after again against because before being below between could doing during "
           "every first having their there these those through under until where which while would "
           "should still today owner check".split())
MAX_HITS = 5
NOT_FACTS = PROCEDURE + ("words we use",)
FILLER = re.compile(r"\b(basically|essentially|in order to|it is worth noting|note that)\b", re.I)
ASIDE = re.compile(r"\([^()]{41,}\)")
HELP = """Usage: check_handoff.py PATH [--repo DIR] [--quiet] | --new PROFILE PATH | --selftest | --help
Profiles: 'Profile: lite|standard|full[, no-tags][, no-archive]' under Last updated, none means full.
 lite 5 sections, 7 checks. standard 10, adds history, density. full 15, adds unverified.
One PASS, WARN or FAIL line per check, exit 1 on any FAIL. Checks:
 last-updated   FAIL: no 'Last updated YYYY-MM-DD', or older than the newest commit
 sections       FAIL: a section of the profile missing or out of order
 relative-time  FAIL: yesterday, today, soon and the like outside procedure sections
 unknowns       FAIL: TODO, TBD or ??? without 'ask the owner'
 maybe-shipped  WARN: a What is next bullet shares 3 words with a commit since Last updated
 secrets        FAIL: key-like strings (values never printed)
 unverified     WARN: a [?] line older than 7 days (no-tags drops it)
 history        WARN (no-archive drops it): over 6 dated What is done entries, or an entry over 5 lines
 density        WARN: fact line over 110 chars with an aside over 40 chars, or filler words
 size           WARN over 400 lines, FAIL over 600, target under 350
--quiet prints only WARN and FAIL lines, then one summary line.
--new writes a skeleton with only that profile's sections, never over an existing file."""


def profile(text):
    """(name, switches, problem) from the 'Profile:' line in the header. No line means full."""
    m = re.search(r"(?m)^Profile:(.*)$", text.split("\n## ")[0])
    if not m:
        return "full", [], None
    name, *sw = [p.strip().lower() for p in m.group(1).split(",")]
    bad = name not in PROFILES or not set(sw) <= set(SWITCHES)
    return (name if name in PROFILES else "full"), [s for s in sw if s in SWITCHES], bad and \
        f"unknown profile or switch in '{m.group(0).strip()}', use lite, standard or full, no-tags, no-archive"


def skeleton(name, today):
    return (f"# <Project>: start here\n\nRead this first in any new session. It says what the project is, "
            f"what is next, and how the owner wants work done. Last updated {today}.\nProfile: {name}\n" +
            "".join(f"\n## {h}\n{p}\n" for key, h, p in SPEC if key in PROFILES[name]))


def find_date(line, today):
    m = DATE.search(line)
    if not m:
        return None
    if m.group(1):
        return dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    year = int(m.group(6) or today.year)
    try:
        d = dt.date(year, MONTHS.index(m.group(4)[:3].lower()) + 1, int(m.group(5)))
    except ValueError:
        return None
    return d.replace(year=year - 1) if d > today and not m.group(6) else d


def sections(lines):
    """Yield (section name lowercased, line number, line) for every line."""
    name = ""
    for i, line in enumerate(lines, 1):
        if line.startswith("## "):
            name = line[3:].strip().lower()
        yield name, i, line


def bullets(lines, name):
    """[line number, joined text, line count] per bullet in the section starting with name."""
    out, cur = [], None
    for sec, i, l in sections(lines):
        if not sec.startswith(name) or l.startswith("## "):
            continue
        if l.startswith("- "):
            cur = [i, l[2:], 1]
            out.append(cur)
        elif cur and l.strip():
            cur[1] += " " + l.strip()
            cur[2] += 1
    return out


def git(repo, *args):
    try:
        r = subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True, timeout=20)
        return r.stdout.strip() if r.returncode == 0 else None
    except (OSError, subprocess.TimeoutExpired):
        return None


def looks_random(run):
    # ponytail: heuristic, mixed case plus digits and few slashes (paths have many). Entropy check if it misfires.
    return run.count("/") < 3 and all(re.search(p, run) for p in ("[a-z]", "[A-Z]", "[0-9]"))


def words(text):
    return {w for w in re.findall(r"[a-z0-9]{5,}", text.lower()) if w not in STOP}


def check(text, newest_commit, subjects, today):
    """Return a list of (status, name, summary, hits). subjects: git log subjects since Last updated."""
    lines = text.splitlines()
    out = []
    pname, switches, problem = profile(text)
    m = re.search(r"Last updated\W*(\d{4}-\d\d-\d\d)", text)
    updated = dt.date.fromisoformat(m.group(1)) if m else None
    if not updated:
        out.append(("FAIL", "last-updated", "no 'Last updated YYYY-MM-DD' found", []))
    elif newest_commit is None:
        out.append(("WARN", "last-updated", f"{updated}, no git repo to compare", []))
    elif updated < newest_commit:
        out.append(("FAIL", "last-updated", f"{updated} is older than newest commit {newest_commit}", []))
    else:
        out.append(("PASS", "last-updated", f"{updated}, newest commit {newest_commit}", []))

    heads = [line[3:].strip().lower() for line in lines if line.startswith("## ")]
    pos, missing = 0, []
    want = [s for s in SECTIONS if s in PROFILES[pname]]
    for s in want:
        idx = next((j for j in range(pos, len(heads)) if heads[j].startswith(s)), None)
        if idx is None:
            missing.append(s)
        else:
            pos = idx + 1
    out.append(("FAIL" if missing or problem else "PASS", "sections", f"{len(want) - len(missing)} of {len(want)} "
                f"{pname} sections in order" + (f", missing: {', '.join(missing)}" if missing else ""),
                [problem] * bool(problem) + [f"missing or out of order: {s}" for s in missing]))

    rel = [f"L{i}: {l.strip()}" for sec, i, l in sections(lines)
           if not sec.startswith(PROCEDURE) and RELATIVE.search(l)]
    out.append(("FAIL" if rel else "PASS", "relative-time", f"{len(rel)} in fact sections", rel))

    unk = [f"L{i}: {l.strip()}" for i, l in enumerate(lines, 1)
           if UNKNOWN.search(l) and "ask the owner" not in l]
    out.append(("FAIL" if unk else "PASS", "unknowns", f"{len(unk)} TODO/TBD/??? without 'ask the owner'", unk))

    nxt = bullets(lines, "what is next")
    shipped, sw = [], [words(s) for s in subjects]
    noise = {w for w in set().union(*sw) if len(sw) >= 4 and sum(w in x for x in sw) > len(sw) / 2}
    for i, b, _ in nxt:
        bw = words(b) - noise  # noise: words in most subjects, like the project name
        for s in subjects:
            common = bw & words(s)
            if len(common) >= 3:
                shipped.append(f"L{i}: {b[:45]}... [{', '.join(sorted(common))}] ~ {s[:50]}")
                break
    out.append(("WARN" if shipped else "PASS", "maybe-shipped",
                f"{len(shipped)} of {len(nxt)} next bullets match a commit since Last updated", shipped))

    sec_hits = []
    for i, l in enumerate(lines, 1):
        if SECRETS.search(l) or any(looks_random(t) for t in B64.findall(l)):
            sec_hits.append(f"L{i}: possible secret, value not printed")
    out.append(("FAIL" if sec_hits else "PASS", "secrets", f"{len(sec_hits)} hits", sec_hits))

    tagged, old, last = [], 0, None
    for sec, i, l in sections(lines):
        if l.startswith("## "):
            last = None
        last = find_date(l, today) or last
        if "[?]" in l:
            age = (today - last).days if last else None
            old += age is not None and age > 7
            tagged.append(f"L{i}: {'undated' if age is None else f'{age}d old'}: {l.strip()[:70]}")
    out.append(("WARN" if old else "PASS", "unverified", f"{len(tagged)} [?] lines, {old} older than 7 days", tagged))

    hist = [b for b in bullets(lines, "what is done") if "HANDOFF-HISTORY" not in b[1]]
    dated = sum(bool(find_date(t[:30], today)) for _, t, _ in hist)
    long = [f"L{i}: {n} lines: {t[:60]}" for i, t, n in hist if n > 5]
    bad = dated > 6 or long
    out.append(("WARN" if bad else "PASS", "history", f"{dated} dated entries, {len(long)} over 5 lines" +
                (": move entries older than the newest 6 to HANDOFF-HISTORY.md beside this file and keep one "
                 "pointer line, trim long entries to 5 lines, details live in git" if bad else ""), long))

    dense = [f"L{i}: {l.strip()[:70]}" for sec, i, l in sections(lines) if not sec.startswith(NOT_FACTS)
             and (len(l) > 110 and ASIDE.search(l) or FILLER.search(l))]
    out.append(("WARN" if dense else "PASS", "density", f"{len(dense)} dense lines in fact sections" +
                (": one fact per line, cut the aside or make it its own line" if dense else ""), dense))

    n = len(lines)
    out.append(("FAIL" if n > 600 else "WARN" if n > 400 else "PASS", "size",
                f"{n} lines (target 350, warn 400, fail 600)", []))
    skip = SKIP[pname] | {SWITCHES[s] for s in switches}
    return [r for r in out if r[1] not in skip]


def report(results, quiet=False, label="full"):
    for status, name, summary, hits in results:
        if quiet and status == "PASS":
            continue
        print(f"{status} {name}: {summary}")
        for h in hits[:MAX_HITS]:
            print(f"  {h[:150]}")
        if len(hits) > MAX_HITS:
            print(f"  ... {len(hits) - MAX_HITS} more")
    if quiet:
        n = [sum(r[0] == s for r in results) for s in ("PASS", "WARN", "FAIL")]
        print(f"profile {label}, {len(results)} checks: {n[0]} pass, {n[1]} warn, {n[2]} fail")
    return 1 if any(r[0] == "FAIL" for r in results) else 0


FIXTURE = """# Demo: start here
Last updated 2026-01-01.
## What this is
Launched recently. Owner TBD.
It is basically a tracker.
## Goal and strategy
## Map of the folder
key: sk-ant-abc123
## Secrets and accounts
## Rules for working with the owner
Read today's log, ask today.
## First ten minutes of a session
1) Read yesterday's run log.
## What is done (short history)
- 2026-01-01: shipped the invoice export button.
## What is next (dates matter)
- Build the invoice export button for accountants.
- Price review in March.
## Known weak spots
## Agents and routines
## Decisions and why
- Picked SQLite (2025-12-01): one file. [?]
## Key numbers
## Renewals and expiries
## Gotchas that cost time
- Note that the shell resets.
## Words we use
"""


def selftest():
    today = dt.date(2026, 1, 20)
    r = {name: (status, hits) for status, name, _, hits in
         check(FIXTURE, dt.date(2026, 1, 5), ["add invoice export button for accountants"], today)}
    assert r["last-updated"][0] == "FAIL", r["last-updated"]
    assert r["sections"][0] == "PASS", r["sections"]
    assert r["relative-time"][0] == "FAIL" and len(r["relative-time"][1]) == 1, r["relative-time"]
    assert r["unknowns"][0] == "FAIL" and len(r["unknowns"][1]) == 1, r["unknowns"]
    assert r["maybe-shipped"][0] == "WARN" and len(r["maybe-shipped"][1]) == 1, r["maybe-shipped"]
    assert r["secrets"][0] == "FAIL", r["secrets"]
    assert r["unverified"][0] == "WARN", r["unverified"]
    assert r["size"][0] == "PASS"
    assert r["history"][0] == "PASS", r["history"]
    assert r["density"][0] == "WARN" and len(r["density"][1]) == 1, r["density"]
    many = "".join(f"- 2026-01-0{d}: x\n" for d in range(2, 8))
    h = {x[1]: x for x in check(FIXTURE.replace("## What is next", many + "## What is next"), None, [], today)}
    assert h["history"][0] == "WARN" and "7 dated" in h["history"][2], h["history"]
    h = {x[1]: x for x in check(FIXTURE.replace("button.\n", "button.\n" + "  more\n" * 5), None, [], today)}
    assert h["history"][0] == "WARN" and len(h["history"][3]) == 1, h["history"]
    bad = check(FIXTURE.replace("## Key numbers\n", "") + "x\n" * 601, None, [], today)
    assert [x[0] for x in bad if x[1] in ("sections", "size", "last-updated")] == ["WARN", "FAIL", "FAIL"]
    clean = check("Last updated 2026-01-20\n" + "\n".join("## " + s for s in SECTIONS) +
                  "\npath /home/user/projects/SomeLongFolderName123/sub/x.py", dt.date(2026, 1, 20), [], today)
    assert all(x[0] == "PASS" for x in clean), clean
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        report(clean, quiet=True), report(check(FIXTURE, None, [], today), quiet=True)
    q = buf.getvalue().splitlines()
    assert q[0] == f"profile full, {len(clean)} checks: {len(clean)} pass, 0 warn, 0 fail", q
    assert not any(x.startswith("PASS") for x in q) and q[-1].endswith("fail"), q
    std = {x[1]: x for x in check(skeleton("standard", today).replace("## Key numbers", "## Prices"), None, [], today)}
    assert std["sections"][0] == "FAIL" and "missing: key numbers" in std["sections"][2], std["sections"]
    for name, n in (("lite", 7), ("standard", 9), ("full", 10)):  # lite: 5 sections, no history, density, [?]
        sk = check(skeleton(name, today), today, [], today)
        assert len(sk) == n and all(x[0] == "PASS" for x in sk), (name, sk)
    nt = check(FIXTURE.replace("2026-01-01.\n", "2026-01-01.\nProfile: full, no-tags\n", 1), None, [], today)
    assert len(nt) == 9 and not any("[?]" in h for x in nt for h in x[3]), nt
    na = {x[1]: x for x in check(FIXTURE.replace("01.\n", "01.\nProfile: huge, no-archive\n", 1), None, [], today)}
    assert na["sections"][0] == "FAIL" and "unknown profile" in na["sections"][3][0] and "history" not in na, na
    print("selftest ok")


def main(argv):
    if "--selftest" in argv:
        return selftest()
    if "--help" in argv:
        return print(HELP)
    if "--new" in argv:
        name, path = (argv[argv.index("--new") + 1:] + ["", ""])[:2]
        if name not in PROFILES or not path:
            return print(HELP) or 2
        if os.path.exists(path):
            return print(f"{path} exists, not overwritten") or 1
        open(path, "w", encoding="utf-8").write(skeleton(name, dt.date.today()))
        return print(f"wrote {path}: profile {name}, {len(PROFILES[name])} sections")
    if not argv or argv[0].startswith("-"):
        return print(HELP) or 2
    path = argv[0]
    repo = argv[argv.index("--repo") + 1] if "--repo" in argv else os.path.dirname(os.path.abspath(path))
    text = open(path, encoding="utf-8").read()
    newest = git(repo, "log", "-1", "--format=%cs")
    m = re.search(r"Last updated\W*(\d{4}-\d\d-\d\d)", text)
    subjects = (git(repo, "log", f"--since={m.group(1)} 00:00", "--format=%s") or "").splitlines() if m else []
    results = check(text, dt.date.fromisoformat(newest) if newest else None, subjects, dt.date.today())
    pname, switches, _ = profile(text)
    return report(results, "--quiet" in argv, " ".join([pname] + switches))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]) or 0)
