# Changelog

## 1.3.0 (2026-11-10)

Three sizes, so a small project carries a small handoff.
- `Profile: lite|standard|full` line under Last updated, with optional `, no-tags` and `, no-archive`. No line means full, existing handoffs work unchanged.
- lite: 5 sections and 7 checks. standard: 10 sections, adds history and density. full: 15 sections and all 10 checks.
- The sections check asks only for the profile's sections, extra ones are allowed, and names any that are missing.
- `check_handoff.py --new PROFILE PATH`: a skeleton with one placeholder per section, never over an existing file.
- `--quiet` summary names the profile. Selftest covers lite, standard, full, no-tags and an unknown profile.
- SECTIONS.md: a table of which section belongs to which size. Template carries `Profile: full`.
- Measured on CoiPatrol (398 lines): a lite read about 2,740 tokens, standard about 6,190, full about 7,760.

## 1.2.0 (2026-11-10)

Cheaper sessions, same information.
- Single load: the start needs only the handoff and `check_handoff.py --quiet`, the skill loads once at the end.
- Template: First ten minutes starts with the quiet check and resolving its [?] lines.
- `check_handoff.py --quiet`: only WARN and FAIL lines, then one summary line.
- `check_handoff.py --help`: the check list in 13 lines.
- New check history: WARN over 6 dated What is done entries or any entry over 5 lines.
- New check density: WARN on long fact lines with a long aside, or filler words.
- `evidence.sh`: subjects cut at 80 characters, 15 commits at most, a shared prefix printed once, no empty headers.
- SKILL.md cut to 649 words and 73 lines, every rule kept.
- Density and archive rules: in SKILL.md Rules, in full in `references/SECTIONS.md`.
- README cost table remeasured: about 22% fewer tokens per session on CoiPatrol.

## 1.1.0 (2026-11-10)

Five additions after comparing 19 similar skills, see README.
- `scripts/check_handoff.py`: one command for the mechanical checks (date, sections, relative time, unknowns, maybe shipped, secrets, claim tags, size), with `--selftest`.
- `scripts/evidence.sh`: one compact evidence pack for the end of a session.
- Claim tags: a fact from chat memory alone ends with "[?]" and is resolved first next session.
- "Tried and rejected, do not retry" subsection under Decisions and why.
- Degradation trigger: write the history entry at once when the session starts repeating settled work or runs low on context.
Also: SKILL.md cut from 141 to 84 lines, section definitions moved to `references/SECTIONS.md`, a sanitized real example in `examples/`.

## 1.0.0 (2026-11-10)

First release. Fifteen sections in a fixed order, start and end of session procedures,
verification greps, creating a handoff with five owner questions, and the template.
