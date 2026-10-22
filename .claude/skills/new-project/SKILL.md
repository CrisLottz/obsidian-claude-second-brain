---
name: new-project
description: Create a project note wired into the vault — template, hub, root note and code repository pointer. Use when the user starts a new project or asks to register one.
argument-hint: "<project name>"
---

# New project

> **Paths:** every path in this skill is relative to the vault root (its path is in the global `~/.claude/CLAUDE.md`). This skill also works from sessions opened in other folders: there, use full paths and run Git as `git -C <vault> …`.

Project name: `$ARGUMENTS` (ask for it if empty).

1. Ask the user, in one message, only what you can't infer:
   - Goal in one or two sentences, and what "done" looks like.
   - Personal project (`03_projects/`, `hub_projects`) or work (`02_work/`, `hub_work` or one of its sub-hubs)?
   - GitHub repositories (`owner/name`), if any — a project can have several (e.g. API + web client).
   - Status: `idea`, `planned` or `active`.
2. Search the vault for existing notes about it (name, aliases, related terms). If one exists, update it instead of duplicating.
3. Create the note from `00_system/templates/tpl_project.md`:
   - File name: `snake_case`, unique.
   - YAML: `author: ai`, `repo` (list of `owner/name`; this is how sessions opened in those repos find the note), `summary`, `up` = the hub, first alias = display name.
   - Fill **Goal**, **Current state** and the first **Next steps** from the user's answers.
4. Add it to the hub with a one-line description: under **Active** if `active` or `planned`, under **Paused / dormant** if `idea` or `paused`.
5. If the status is `active`, also add or update its line in the **Active** section of `00_home.md`.
6. If the repo is local and has no `CLAUDE.md` or docs folder, mention it; don't create files outside the vault without asking.
7. Append one line to the session log.
