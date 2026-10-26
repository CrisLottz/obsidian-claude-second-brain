# AGENTS.md — Second brain vault

Rules for every AI agent working in this vault (Codex, Cursor, Copilot, Gemini CLI, Qwen Code, Aider, OpenCode…). Claude Code reads `CLAUDE.md` instead; this file adapts those same rules for everyone else. If your agent only reads its own file name, such as `GEMINI.md`, copy this file under that name (see `00_system/connecting_ai_agents.md`).

## 1. Non-negotiable rules (read before anything else)

- Never write secrets (passwords, keys, tokens, full card numbers).
- **One task, one note:** a `- [ ]` task lives only in the note it belongs to — never copy it into `07_personal/todo.md` or another note with other words. Deadlines are `📅 YYYY-MM-DD` at the end of the task; any other date is context (`vault_conventions` §4).
- Never delete a note the user wrote without asking; prefer `status: archived`.
- Inside the vault, act without asking. Confirm before outward-facing or hard-to-reverse actions: pushing, opening PRs, sending messages or emails, anything that spends money.

## 2. The rules of this vault

The full rules live in `CLAUDE.md`, written for Claude Code. They apply to you in full, translated with section 3. Read it now, then read `00_home.md` — the owner's profile and the map of every area. Before creating, renaming or moving notes, read `00_system/vault_conventions.md`.

## 3. Translation for agents other than Claude Code

| Where `CLAUDE.md` says… | You do… |
|---|---|
| "Claude", "you" | You, whatever agent you are |
| `author: ai` | `author: <your agent>` (`codex`, `gemini`…). It must be a row of the `author` table in `vault_conventions` (§5); if yours is missing, add the row first. Editing a note the user wrote: `mixed` |
| "A hook runs `git pull`…" at session start | Run `git pull --ff-only` yourself; if it fails, tell the user before editing. Then read the last lines of the newest `00_system/claude_log_YYYY_MM.md` and count the notes in `01_inbox/` |
| Frontmatter validation after each edit | Run `python .claude/hooks/validate_frontmatter.py <files you edited>` (`python3` on macOS/Linux) and fix every error |
| Session log line | Same file as Claude (`claude_log_YYYY_MM.md`, shared by all agents). Tag your line: `- YYYY-MM-DD — (codex) what was done, in one sentence — [[note_a]]` |
| "Hooks commit and push after each response" | Commit only when the user asks; otherwise their Obsidian Git plugin saves the changes. When asked: `git add -- <only the files you touched>` (never `-A` on the whole vault), commit with one sentence of what was done, then `git pull --no-rebase` and `git push` |
| `Co-Authored-By: Claude …` | Don't add it: it would credit Claude for your work. Your authorship lives in the notes' `author` property |
| `.claude/`, `.github/`, `.obsidian/` are never auto-committed | Same for you: tell the user to review changes there before committing them |
| Slash skills (`/inbox`, `/ingest`…) | Plain-Markdown procedures in `.claude/skills/<name>/SKILL.md`. Open the file and follow it. `${CLAUDE_SKILL_DIR}` = that skill's folder; `$ARGUMENTS` = what the user typed after the skill name |
| `head -n 16`, grep/glob | The equivalent in your environment (PowerShell: `Get-Content -TotalCount 16`, `Select-String`) |
| `~/.claude/…`, `install.py`, "restart Claude Code" | Claude-only setup; ignore it |

How to connect a new AI to this vault: `00_system/connecting_ai_agents.md`.
