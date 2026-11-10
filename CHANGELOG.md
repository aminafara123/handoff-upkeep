# Changelog

## 1.4.1 (2026-11-11)

Size estimate calibrated against Claude's own tokenizer.
- Why: on 2026-11-11 the count_tokens endpoint (model claude-sonnet-5-5) counted the CoiPatrol hot handoff at 18,904 chars as 7,774 tokens, HANDOFF-REFERENCE.md at 13,616 chars as 5,181, and SKILL.md 1.4.0 at 4,697 chars as 1,725. That is about 2.5 characters per token on English prose, so chars/4 undercounted by about 1.56x. Claude Code's 5,000-token compaction cap is in Claude tokens.
- Size check: tokens as chars/2.5. Thresholds unchanged, WARN over 5,000, FAIL over 12,000. The WARN names the second fix: a SessionStart hook matching compact can print the handoff back after compaction.
- SKILL.md and SECTIONS.md: the cap stated in Claude tokens with the calibration.
- README: one calibration line under Cost per session. The report figures stay chars/4 so the comparisons stay like for like.

## 1.4.0 (2026-11-10)

Size counted in tokens, not lines, because that is what a session pays and what Claude Code caps.
- Why: measured with a BPE tokenizer on 2026-11-10, every hard-wrapped line cost 2 tokens for the break and indent plus a line number in the Read view. The CoiPatrol handoff had 189 wrapped lines, about 10 percent of the file. Unwrapped with the same words it went from 399 to 210 lines and from 8,077 to 7,755 tokens.
- Why: Claude Code's docs (code.claude.com/docs/en/context-window) say that after compaction up to five recently read files are re-read, and a file over 5,000 tokens comes back as a path without content. A start-here file over 5,000 tokens silently drops out of a long session.
- Size check: tokens as chars/4, main file only. PASS under 5,000, WARN over 5,000 naming the cap and the cold sections to move, FAIL over 12,000. The line count stays in the message.
- HANDOFF-REFERENCE.md beside the handoff: its sections count toward the profile, the sections summary says how many came from it.
- Density check: long-line limit raised from 110 to 220 characters, so an unwrapped single bullet is not flagged for length alone. The filler test is unchanged.
- Selftest: size PASS, WARN and FAIL by character count, and a temp-dir fixture with a sibling HANDOFF-REFERENCE.md.
- SKILL.md: rule "one bullet, one line, never hard-wrap", and the 5,000-token target with HANDOFF-REFERENCE.md for cold sections.
- SECTIONS.md: the size rule in tokens with the 5,000 cap. Template and example unwrapped, same words.
- README: cost line with the 1.4.0 figures.

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
