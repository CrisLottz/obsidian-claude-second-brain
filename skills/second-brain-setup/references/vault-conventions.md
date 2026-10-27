# How the vault is organized

A short map of the rules in the vault's `00_system/vault_conventions.md`, which is the source of truth (the validator reads its tables). Read the real file before restructuring anything.

## Folders (two levels at most)

| Folder | Holds | Main hub |
|---|---|---|
| `/` | `00_home.md` (profile and map of the vault), `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `QWEN.md`, `README.md` | none |
| `00_system/` | Conventions, templates, AI session logs, archived briefs, Web Clipper template | none |
| `01_inbox/` | Raw captures, processed later by `/inbox` | none |
| `02_work/` | Jobs, clients, freelance, career | `hub_work` |
| `03_projects/` | Projects you build for yourself | `hub_projects` |
| `04_knowledge/` | What you know and study | `hub_knowledge` |
| `05_life/` | Health, fitness, hobbies, practical skills | `hub_life` |
| `06_media/` | Books, movies, music, series, games | `hub_media` |
| `07_personal/` | Profile, to-do, wishlist, money, diary, people | `hub_personal` |

New Obsidian notes land in `01_inbox/`: the user never decides where a note goes while writing.

## Every note

- File name: lowercase `snake_case`, no spaces or accents (`graduation_project.md`).
- Frontmatter on line 1: `title`, `type`, `status`, `author` (`human`, `ai`, `mixed`, or a row added for another agent), `created`, `updated`, `summary`, `up` (the hub that lists it), optionally `tags` and `aliases`.
- Wikilinks in YAML are quoted: `- "[[hub_projects]]"`.
- Links go both ways: the note points up to its hub with `up`, and the hub lists the note.
- The first `aliases` item is the display name the morning brief shows.

## Tasks and dates

- An open task is `- [ ] text`.
- A deadline is `📅 YYYY-MM-DD` at the end of the task, or the `due` property. Any other date in a task is context.
- **One task, one note**: a task lives only in the note it belongs to; `07_personal/todo.md` holds only tasks with no other home.

## What the AI does

- Reads the root note, then the hub, then the note (progressive disclosure).
- Edits the user's own notes by adding, never rewriting; sets `author: mixed`.
- Never deletes a note the user wrote without asking (prefers `status: archived`).
- Appends one line per task to `00_system/claude_log_YYYY_MM.md`.
- Changes under `.claude/`, `.github/` and `.obsidian/` are never auto-committed: the user reviews them.

## Customizing

- Add an area: create its folder and `hub_<area>.md`, update the folder table in `vault_conventions.md`, list the hub in `00_home.md`.
- Add a note `type` or `status`: edit the tables in `vault_conventions.md` §5; the validator picks them up.
- Add another AI agent: add its row to the `author` table; see `00_system/connecting_ai_agents.md`.
