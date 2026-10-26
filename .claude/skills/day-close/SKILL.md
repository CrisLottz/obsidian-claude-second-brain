---
name: day-close
description: End-of-day review of the user's open tasks — checks each one against evidence (vault log and commits, GitHub issues/PRs/runs of the linked repos), closes what is done, asks about the rest in one batch and previews tomorrow's morning brief. Use when the user runs /day-close or accepts the end-of-day reminder.
---

# Day close

> **Paths:** every path in this skill is relative to the vault root (its path is in the global `~/.claude/CLAUDE.md`). This skill also works from sessions opened in other folders: there, use full paths and run Git as `git -C <vault> …`.

Goal: tomorrow's morning brief (`.github/scripts/morning_brief.py`) shows only what is really pending. Be quick: this runs at night.

## 1. Gather the open tasks

- `07_personal/todo.md` → section **Now**.
- Every note with `type: project` and `status: active` → section **Next steps**.
- Any `- [ ]` with `📅 YYYY-MM-DD` up to tomorrow (overdue or due).

## 2. Gather the evidence (today and the last few days)

- Today's lines in the newest `00_system/claude_log_YYYY_MM.md` and `git -C <vault> log --since=midnight --stat`.
- Today's entry in `07_personal/diary/diary_YYYY_MM.md`, if there is one.
- For each project's `repo:` list, the GitHub state the task names (needs the `gh` CLI; skip this step without it): `gh issue view <n> -R <repo>`, `gh pr list -R <repo> --state all --limit 10`, `gh run list -R <repo> --limit 3`.
- A task that points to another note (`[[note]]`): that note's own tasks (`[x]` there means done here).

Only read-only commands. Don't open notes or repos a task doesn't need.

## 3. Classify each task

| Class | Rule | Action |
|---|---|---|
| **Done** | Hard evidence (closed issue, merged PR, `[x]` elsewhere, log line, file present) | Mark `[x]` and append ` — done YYYY-MM-DD (<evidence>)` |
| **Partly done** | Evidence covers only part of it | Rewrite the task to what is left |
| **Still open** | Evidence shows it isn't done (open issue, failing run) | Leave it |
| **Can't tell** | No evidence either way (waiting on a person, offline work) | Ask the user |

Never mark a task done without evidence or the user's answer.

## 4. Ask the user once

One short message in the user's language: what you closed (with the evidence, one line each) and a numbered list of the **Can't tell** tasks, to answer with "done / still open / change to …". Also flag:
- tasks whose `📅` date is today or past — move the date, or keep them overdue?
- the same task written in two notes (`vault_conventions` §4, one task one note) — say which copy you'll remove.

## 5. Apply and close

- Apply their answers (`author: mixed` and `updated` on notes the user wrote).
- Run `python .github/scripts/morning_brief.py --dry-run` (`PYTHONIOENCODING=utf-8` on Windows) and show them the sections that changed.
- Append the log line — **it must start with `Day close`**, which stops the end-of-day reminders for today:
  `- YYYY-MM-DD — Day close: closed N, updated M, K still open — [[note_a]], [[note_b]]`
