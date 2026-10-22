---
name: journal-close
description: Close a month of the diary — distill it into people_and_context, person notes and the full profile, then archive the diary. Run only when the user asks.
argument-hint: "[YYYY-MM — defaults to the previous month]"
disable-model-invocation: true
---

# Close a diary month

> **Paths:** every path in this skill is relative to the vault root (its path is in the global `~/.claude/CLAUDE.md`). This skill also works from sessions opened in other folders: there, use full paths and run Git as `git -C <vault> …`.

Month: `$ARGUMENTS`, or the previous month if empty. Diary file: `07_personal/diary/diary_YYYY_MM.md` (and `_a` / `_b` halves if split).

1. Read the diary month, `07_personal/people/people_and_context.md` and `07_personal/profile.md`.
2. Extract:
   - Changes in the user's situation, goals, habits and decisions.
   - People: new people, and what changed with existing ones.
   - Recurring themes, moods or patterns.
   - Facts that belong to other areas (work, projects, money, health) — list them as suggestions, don't move diary text.
3. Show the user the proposed changes as a short before → after list per note, in their language. Wait for approval.
4. Apply:
   - Update `people_and_context` (keep it under ~150 lines; compress old detail instead of growing).
   - Update the relevant sections of `profile` with durable changes.
   - For people who appear often and matter, create or update a `person` note in `07_personal/people/` (from `tpl_person.md`), list it in `hub_people` and link it from the People table.
   - Set `author: mixed` where the user had written, and update `updated`.
   - In the diary: set `status: archived` and fill its `summary` with one sentence about the month. Never edit the diary text itself.
   - In `hub_diary`, make sure the month is listed under **Months** (newest first) with a one-line description.
5. Append one line to the session log.
