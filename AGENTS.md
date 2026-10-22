# AGENTS.md — Second brain vault

For AI agents other than Claude Code (Codex, Cursor, Aider, Gemini CLI…). If your agent only reads its own file name, such as `GEMINI.md`, copy this file under that name.

1. Read `CLAUDE.md` in this folder: it is the rulebook for this vault (navigation, writing rules, session log). Then read `00_home.md` (the owner's profile and the map of every area) and, before creating or moving notes, `00_system/vault_conventions.md`.
2. The **Git** and **Skills** sections of `CLAUDE.md` describe Claude Code hooks and slash commands. Without them:
   - Run `git pull --ff-only` before you start.
   - After editing a note, run `python .claude/hooks/validate_frontmatter.py <file>` (`python3` on macOS/Linux) and fix every problem it reports.
   - Each skill is a plain-Markdown procedure in `.claude/skills/<name>/SKILL.md`: when the user asks for that task, read the file and follow it.
   - Commit only when the user asks; otherwise their Obsidian Git plugin commits the changes.
