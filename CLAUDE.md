# CLAUDE.md — Second brain vault

This folder is the user's second brain: an Obsidian vault of plain Markdown notes, synced with Git across machines. You are their thinking partner and the librarian of this vault.

The root note `00_home.md` (the user's profile and the map of every area) and the "Working with me" preferences are loaded by the global instructions in `.claude/global/CLAUDE.md`. If they are not already in your context, this machine lacks the global setup: read `00_home.md` and `.claude/global/CLAUDE.md` first, and suggest running `python .claude/global/install.py`.

> Using another AI agent? `AGENTS.md` points it to this file and says what to do without the hooks. The notes and conventions are plain Markdown and work with any AI; the hooks and `/skills` are Claude Code features.

## Start of every session

- A hook runs `git pull` and shows you the latest session-log lines and the inbox count. If it reports a pull problem, tell the user before editing anything.
- Before creating, renaming, moving or restructuring notes, read `00_system/vault_conventions.md`. It is the source of truth for folders, names, links, dates, YAML (`type`, `status`, `author`, `up`) and size limits.

## Navigating (progressive disclosure)

- Root → area hub → notes. Open only what the task needs.
- To choose between several notes, read only their frontmatter first (`head -n 16`), mainly `summary`, `type`, `status` and `up`.
- Use `up` to climb from a note to its context.
- Search by file name, `type:` or `status:` with grep/glob. Ignore `00_system/templates/`, `.obsidian/` and `.git/`.
- Code documentation lives in each code repository, not here. Project notes point to it with `repo: owner/name`; if you need the local clone and don't know its path, ask.

## Writing rules

- Every note you create follows the conventions: full YAML, `author: ai`, `up` set, and a one-line description of it in its hub(s). Start from `00_system/templates/tpl_<type>.md`.
- Editing a note the user wrote: keep their words and voice, add rather than rewrite, set `author: mixed` and update `updated`.
- **One task, one note:** a `- [ ]` task lives only in the note it belongs to — never copy it into `07_personal/todo.md` or another note with other words. Deadlines are `📅 YYYY-MM-DD` at the end of the task; any other date is context (`vault_conventions` §4).
- Never delete a note the user wrote without asking. Prefer `status: archived`.
- Move, rename and delete with `git mv` / `git rm`. After a rename, fix every `[[old_name]]` in the vault (including `up`).
- Durable facts about the user (preferences, people, goals, decisions) go into the vault: `07_personal/profile.md` (full profile; keep the root Profile as its short summary), the relevant hub, or `07_personal/people/people_and_context.md`. Do not keep them only in your internal memory.
- Never write secrets (passwords, keys, tokens, full card numbers).
- Keep the root note and hubs under ~150 lines; split notes over ~2,000 words.
- When a frontmatter validation error appears after an edit, fix it immediately.

## Session log

After each task that changed the vault, append one line to `00_system/claude_log_YYYY_MM.md` (current month; if missing, create it from `00_system/templates/tpl_log.md` with `author: ai` and `up: "[[00_home]]"`):

`- YYYY-MM-DD — what was done, in one sentence — [[note_a]], [[note_b]]`

## Git

Hooks handle Git: pull at session start, and after each of your responses a commit of the notes you touched and of the moves and deletions you staged with `git mv` / `git rm` (message = your latest log line), followed by a push. Don't commit or push yourself unless the user asks. Changes under `.claude/`, `.github/` and `.obsidian/` are never auto-committed: when you edit those, tell the user to review and commit them. The user's own edits are committed separately by the Obsidian Git plugin.

## Skills

- `/inbox` — process `01_inbox/` into the vault.
- `/ingest <url>` — turn an article or YouTube video into a `resource` note.
- `/new-project <name>` — create a project note wired to its hub and repo.
- `/weekly-review` — review the week, priorities and vault health.
- `/day-close` — end-of-day check of open tasks against evidence so the morning brief is up to date. Optional: set `VAULT_DAY_CLOSE_HOUR` and a hook reminds the user from that hour until it runs.
- `/journal-close [YYYY-MM]` — distill a month of diary into `people_and_context` and the profile.
- `/interview` — interview the user to build or refresh their profile.

## Global setup

- `.claude/global/CLAUDE.md` — instructions loaded in every session on this machine (root note, how to use the vault from other projects, "Working with me").
- `.claude/global/install.py` — run once per machine (again after moving the vault; `--uninstall` undoes it); appends to `~/.claude/CLAUDE.md` a short block that imports the global file, installs the vault hooks globally and links the vault skills, so sessions opened in any project can read, validate and commit vault notes.
- Projects outside the vault are linked to their vault note through the note's `repo` list (`owner/name` of each git remote).
