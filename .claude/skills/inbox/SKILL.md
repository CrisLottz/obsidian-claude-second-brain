---
name: inbox
description: Process the notes in 01_inbox — rename them, complete their YAML, move them to their area folder and link them from their hub. Use when the user asks to process, clean or triage the inbox.
argument-hint: "[note_name — optional, to process only that note]"
---

# Process the inbox

> **Paths:** every path in this skill is relative to the vault root (its path is in the global `~/.claude/CLAUDE.md`). This skill also works from sessions opened in other folders: there, use full paths and run Git as `git -C <vault> …`.

Turn raw captures in `01_inbox/` into proper vault notes, following `00_system/vault_conventions.md` (§2 names, §3 links, §5 YAML, §7 inbox).

## Steps

1. Read `00_system/vault_conventions.md` and `00_home.md`.
2. List `01_inbox/` (ignore `.gitkeep`). If `$ARGUMENTS` names a note, process only that one.
3. Read each note and decide:
   - **Action:** move as a new note, merge into an existing note (search the vault first), or discard if empty.
   - **type** and **status** from the allowed lists.
   - **Destination folder** and **hub(s)**.
   - **New file name:** `snake_case`, unique in the vault.
4. Show the user a plan table before touching anything:

   | Inbox file | Action | New name | type | Folder | Hub |
   |---|---|---|---|---|---|

   Wait for their approval, unless they already said to go ahead.
5. Apply the approved plan, note by note:
   - Rename/move with `git mv` (or `git rm` for discarded files).
   - Complete the YAML: `title`, `type`, `status`, `created` (keep the original date if known), `updated` (today), `summary`, `up`, `tags`, `aliases` (first alias = display name).
   - `author`: keep `human` if you only organized it; `mixed` if you rewrote or expanded their text; `ai` only if you generated the content.
   - Use the matching template in `00_system/templates/` for structure, without discarding the user's content.
   - Add the note to its hub's **Active** section with a one-line description.
   - When merging, append the fragment to the target note under a dated heading, then `git rm` the inbox file.
   - **Web clips** (`type: resource` with a `source` URL, tag `clippings`): replace the full article with a resource note in the `tpl_resource` structure — key points, why it matters to the user, related notes — under ~1,500 words. Fill `summary`, keep `source`, set `status: draft` and `author: ai`. The original stays at its URL; keep the full text only if the user asks.
6. Fix any links that pointed to the old names.
7. Append one line to the session log and report what moved where.
