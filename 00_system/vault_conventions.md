---
title: Vault conventions
type: system
status: active
author: ai
created: 2026-10-22
updated: 2026-10-22
summary: Source of truth for folder layout, file naming, links, dates, YAML schema (type/status/author/up), hubs, inbox and size limits in this vault.
up:
  - "[[00_home]]"
tags: [system, conventions]
aliases: [Vault conventions]
---

# Vault conventions

Every human or AI that writes to this vault follows these rules. If a rule here conflicts with an older note, this file wins. Change them freely — but change them **here first**, because the validator reads the allowed values from this file.

## 1. Folders (max 2 levels)

| Folder | Holds | Main hub |
|---|---|---|
| `/` (root) | `CLAUDE.md`, `00_home.md`, `README.md` | — |
| `00_system/` | These conventions, `templates/`, AI session logs, `briefs/` (archived morning briefs), Web Clipper template, maintenance view | — |
| `01_inbox/` | Raw, unprocessed captures (see §7) | — |
| `02_work/` | Jobs, employers, clients, freelance work, career | `hub_work` |
| `03_projects/` | Projects you build for yourself | `hub_projects` |
| `04_knowledge/` | What you know and study; bookmarks; learning backlog | `hub_knowledge` |
| `05_life/` | Health, fitness, nutrition, hobbies, practical skills | `hub_life` |
| `06_media/` | Books, movies, music, series, games | `hub_media` |
| `07_personal/` | Profile, to-do, wishlist, money, diary, people | `hub_personal` |
| `99_assets/` | Images only | — |

- Each main hub lives at the top of its folder.
- Each **first-level sub-hub** may get its own subfolder holding the sub-hub and its notes: `07_personal/people/hub_people.md`.
- **Deeper sub-hubs never get folders**: they are notes inside their first-level ancestor's subfolder. Two folder levels is the maximum.
- Folders say where a file is stored; hubs say what it relates to. A note lives in one folder but can be linked from many hubs.

## 2. File names and display names

- Lowercase `snake_case`, no spaces, accents or dots: `hub_projects.md`. Use one language for file names (English by default).
- Names must be unique across the whole vault (links depend on it).
- Fixed patterns:
  - Hubs: `hub_<area>.md`.
  - Monthly series: `<series>_YYYY_MM.md` — `diary_2026_10`, `money_2026_10`, `claude_log_2026_10`, `brief_2026_10`.
- `title` holds the human-readable name, as it is (with accents, capitals, proper names).
- **The first item of `aliases` is the display name** — the name the morning brief shows. Write it in the language you want to read; for proper names it is the same name. Other aliases follow it.
- Open tasks (`- [ ]`) are also shown in the brief: write them in the language you want to read.

## 3. Links

- Use `[[wikilinks]]`. They resolve by file name, so moving a note between folders never breaks them.
- Renaming a file outside Obsidian (terminal, agent) breaks links: after any rename, replace every `[[old_name]]` and `[[old_name|...]]` in the vault, including `up` properties.
- Every link inside a hub carries a one-line description: `- [[note_name]] — what is inside and when to open it.`
- No Dataview or other dynamic queries in hubs; links must be literal text so an AI reading the raw file sees them.
- Links go both ways: a note points up to its hub with `up` (§5), and the hub lists the note. When one side is added, add the other.

## 4. Dates

- Stored in ISO format everywhere: `2026-10-22` in YAML, `2026_10` in file names.
- Free text inside a note (e.g. the diary) may use any date format.
- **Deadlines:** write them as a standalone `YYYY-MM-DD` inside an open task (`- [ ] Pay rent 2026-11-05`) or in the `due` property. The morning brief lists those in the next 7 days and the overdue ones; dates inside file names are ignored.

## 5. YAML frontmatter

Every note starts on line 1 with:

```yaml
---
title: Human-readable title
type: note            # see list below
status: draft         # see list below
author: human         # human | ai | mixed
created: 2026-10-22
updated: 2026-10-22
summary: One sentence an AI can read to decide whether to open the file.
up:                   # parent hub(s); always a list, even with one item
  - "[[hub_knowledge]]"
tags: []
aliases: []           # first item = display name (§2)
---
```

Optional properties:

| Property | Used by | Value |
|---|---|---|
| `repo` | project | List of GitHub `owner/name` of its code repos; never local paths. Sessions opened in those repos find the note through it |
| `period` | journal, finance, log | `YYYY-MM` |
| `due` | assignment, project | `YYYY-MM-DD` |
| `source` | resource | URL of the original |
| `medium` | review | `book` \| `movie` \| `series` \| `album` \| `game` |
| `creator` | review | Author, director, artist or studio |
| `rating` | review | 1–5 |
| `relationship` | person | Free text: family, friend, partner, coworker, client… |

YAML rules: a value containing `: ` or ` #` must be wrapped in double quotes. Property types (text, date, list…) are fixed for Obsidian in `.obsidian/types.json`; Web Clipper can import the same file. Templates for every type live in `00_system/templates/tpl_<type>.md`; inside their frontmatter, template variables are always quoted (`title: "{{title}}"`). Edit templates in Source mode.

Validation: `.claude/hooks/validate_frontmatter.py` checks every note the AI edits against this file (allowed values are read from the tables below). Run `python .claude/hooks/validate_frontmatter.py --all` to audit the whole vault.

### `up` — where the note hangs in the graph

- Every note has `up` except `00_home`.
- Main hubs point to `[[00_home]]`; sub-hubs point to their parent hub; regular notes point to the hub(s) that list them.
- `up` lets an AI climb from any note to its context without searching: note → sub-hub → hub → root.
- Inbox notes may leave `up` empty until they are processed (§7).

### `type` — what the note is

| Value | Use for |
|---|---|
| `hub` | Index note that maps an area or topic (including `00_home`) |
| `project` | A project with a goal and an end state |
| `note` | Atomic note on one concept, or a living note about one subject |
| `reference` | Cheat sheet, command list, config snippet |
| `howto` | Step-by-step procedure / runbook |
| `incident` | Troubleshooting log of a specific failure and its fix |
| `decision` | Why something was chosen |
| `meeting` | Meeting notes |
| `course` | A course you are taking or took |
| `assignment` | Homework, exam, deliverable |
| `resource` | Summary of an article, video, paper or talk |
| `review` | Book, movie, album, series or game |
| `person` | Someone relevant in your life or work |
| `profile` | The full profile of the owner (`profile`) |
| `recipe` | A cooking or drink recipe |
| `routine` | A training program or practice routine |
| `list` | A living list kept up to date — to-do, wishlist, bookmarks, learning backlog |
| `journal` | Monthly diary file |
| `finance` | Monthly money file |
| `log` | Append-only monthly log — AI session log, training log, archived briefs |
| `idea` | Loose idea not yet a project |
| `inbox` | Raw capture waiting to be processed |
| `template` | Template in `00_system/` |
| `system` | Vault configuration and conventions |

### `status` — what state it is in

| Value | Meaning | Typical types |
|---|---|---|
| `idea` | Not started, just a thought | project, idea |
| `planned` | Committed, not started / want to read-watch | project, course, assignment, review, hub |
| `active` | In progress / currently reading-watching / in use | project, course, review, hub, list, log, routine, system |
| `paused` | On hold by choice | project, course, hub, routine |
| `blocked` | Waiting on something external | project, assignment |
| `done` | Finished | project, course, assignment, review, incident |
| `cancelled` | Abandoned or dropped | project, assignment, review |
| `archived` | Kept for history, no longer relevant | any |
| `draft` | Content incomplete | note, reference, howto, resource, recipe, profile |
| `evergreen` | Mature, trusted content | note, reference, howto, recipe |
| `outdated` | Known to be stale; needs review | note, reference, howto |
| `unprocessed` | Not yet triaged | inbox |

Only these values are valid. To add one, add it here first.

### `author`

- `human` — written by you.
- `ai` — created by an AI.
- `mixed` — written by you and later edited by an AI. The AI switches `human` → `mixed` when it edits a note.

## 6. Hubs, notes and the root note

### Root note (`00_home.md`)

Loaded in every AI session (through the global instructions). It stays short (~150 lines) and has, in this order:

1. **Profile** — a ~25-line summary of who you are and your current goals, plus a link to the full `profile`.
2. **Active** — main hubs and projects that need attention now, each with a one-line description.
3. **Paused / dormant** — hubs and projects not being worked on. Nothing is deleted: items move between Active and Paused as priorities change.

### Three kinds of notes under a hub

- **Hub** — an index of several notes or sub-hubs.
- **Living note** — a single document kept up to date (`todo`, `wishlist`, `profile`). Usually `type: list`, `note` or `profile`.
- **Monthly series** — one note per month (`diary_YYYY_MM`, `money_YYYY_MM`). The sub-hub lists the months, newest first.

### Hub layout

- Sections: **Views** (optional, `.base` files), **Active**, **Paused / dormant**, **Sub-hubs**. Same Active/Paused logic as the root.

### New sub-hubs (bottom-up)

- Do not create a hub for a topic in advance. When ~10 notes under a hub share a topic, promote it: create `hub_<topic>.md` (following the subfolder rules of §1).
- The new sub-hub sets `up` to its parent; the parent lists it under **Sub-hubs**; the grouped notes change their `up` to the sub-hub and leave the parent's list.
- A project with many notes can become its own sub-hub the same way.

## 7. Inbox: create first, organize later

- New notes land in `01_inbox/` (Obsidian is configured to do this). You never have to decide where a note goes while writing.
- Inbox notes need no YAML; if they have it, it is `type: inbox`, `status: unprocessed`.
- Processing an inbox note (`/inbox`) means: rename to `snake_case`, fill the full YAML, move it to its folder, and add it with a description to its hub(s). Fragments that belong to an existing note get merged into it instead.
- The inbox should be emptied regularly; a note sitting there is invisible to the graph.
- Web Clipper saves articles here as `type: resource`, `status: unprocessed` (template: `00_system/web_clipper_resource.json`).

## 7b. Bases (table views)

- `.base` files are views for humans: `projects.base`, `media.base`, `people.base`, `maintenance.base`.
- They read the YAML of the notes, so the data stays visible to AIs. Hubs never depend on a Base: they keep their literal links.

## 8. Size limits

Measure prose in words, not lines (a paragraph is one line in Markdown).

| Kind | Limit |
|---|---|
| Root note / hub | ~150 lines |
| Regular note | ~2,000 words; split into linked notes beyond that |
| `profile` | ~12,000 words; past that, move detail into the relevant hub |
| Monthly diary | ~10,000 words; split into halves (`diary_YYYY_MM_a/_b`) beyond that |

## 9. Assets

- Images only, in `99_assets/`, compressed (WebP or JPG, aim for < 500 KB each).
- No PDFs, videos, ZIPs, ISOs or database dumps in the vault: store them outside and link to them. `.gitignore` blocks them.

## 10. Money notes

One file per month (`07_personal/money/money_YYYY_MM.md`, `type: finance`), one section per half-month, from `tpl_finance`. Amounts as plain numbers, any currency in its own column. There are no formulas: the AI calculates totals on request.

Row `status`: `pending` | `paid` | `cancelled`. The morning brief counts the `pending` rows of the current month.

## 11. Secrets

Never write passwords, API keys, tokens, private keys or full card numbers in any note. Last 4 digits of a card are fine.
