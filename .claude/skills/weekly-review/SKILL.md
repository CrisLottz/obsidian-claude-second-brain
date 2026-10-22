---
name: weekly-review
description: Weekly review of the user's projects, work, money and diary, plus a vault health check, ending with proposed priorities. Run only when the user asks for it.
disable-model-invocation: true
---

# Weekly review

> **Paths:** every path in this skill is relative to the vault root (its path is in the global `~/.claude/CLAUDE.md`). This skill also works from sessions opened in other folders: there, use full paths and run Git as `git -C <vault> …`.

Cover the last 7 days (or the period in `$ARGUMENTS`). Read frontmatter first and open full notes only when needed.

## Gather

1. `00_home.md` and every hub's **Active** section.
2. Notes with `status: active` or `blocked` (projects, courses, assignments, incidents); anything with `due` in the next 14 days.
3. `git -C <vault> log --since="7 days ago" --stat` — what changed in the vault, by the user and by the AI.
4. The current `00_system/claude_log_YYYY_MM.md`.
5. The current `07_personal/diary/diary_YYYY_MM.md` (this week's entries) and `07_personal/people/people_and_context.md`.
6. The current `07_personal/money/money_YYYY_MM.md`: `pending` items and the half-month totals.
7. Open items in `07_personal/todo.md`.
8. Vault health:
   - Run `python <vault>/.claude/hooks/validate_frontmatter.py --all` (or `python3`).
   - Count notes in `01_inbox/`.
   - Hubs and root over ~150 lines.

## Report to the user (in their language)

1. **Done this week.**
2. **In progress / blocked** — and what unblocks each.
3. **Upcoming deadlines.**
4. **Money** — pending payments and totals.
5. **Personal** — patterns from the diary worth noticing, said with care and brevity.
6. **Vault health** — validation errors, inbox size, oversized notes.
7. **Proposed priorities for next week** (max 5) and suggested Active ↔ Paused moves.

## After the report

Apply only the changes the user approves (status updates, Active/Paused moves, fixes). Append one line to the session log.
