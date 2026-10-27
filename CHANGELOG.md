# Changelog

All notable changes to this template. Dates are ISO (YYYY-MM-DD). Versions follow [Semantic Versioning](https://semver.org/): a change that makes existing notes or settings behave differently bumps the minor or major number and is listed under **Upgrading**.

## [1.1.0] — 2026-10-26

### Upgrading from 1.0.0

- **Deadlines need the `📅` marker.** A task is a deadline only when it ends with `📅 YYYY-MM-DD` (`- [ ] Pay rent 📅 2026-11-05`). A bare date inside a task is now context and is ignored (before, `CV sent 2026-10-23` appeared as overdue). The `due` property is unchanged.
- Re-run `install.py` once to register the new `prompt` hook (it does nothing until you set `VAULT_DAY_CLOSE_HOUR`).
- Optional: the `author` values now live in a table in `00_system/vault_conventions.md` (§5). Add a row there for each AI agent you use.

### Added

- `/day-close`: end-of-day review that checks open tasks against evidence (session log, commits, GitHub), closes what is done and previews tomorrow's brief.
- Optional reminders for it: a Claude Code hook (`VAULT_DAY_CLOSE_HOUR`) and a Telegram message (`DAY_CLOSE_ENABLED`, same bot, `BRIEF_LANG` and `BRIEF_TIMEZONE` as the brief).
- `AGENTS.md` with the non-negotiable rules and a table that translates Claude-only features for other agents; `GEMINI.md` and `QWEN.md` pointers; `00_system/connecting_ai_agents.md`.
- "One task, one note" rule.
- `skills/second-brain-setup/`: the template packaged as a single `SKILL.md` skill for agent marketplaces (guide, references and a read-only prerequisites check), with `marketplace/build_zip.py` to build the zip. It holds no hooks or installer: it points to this repository.
- Claude Code plugin marketplace: `/plugin marketplace add CrisLottz/obsidian-claude-second-brain`, then `/plugin install second-brain-setup --marketplace CrisLottz/obsidian-claude-second-brain`.
- CI: scripts compile, notes pass the validator; on the upstream repo, a privacy scan for secrets and personal data (`.github/scripts/privacy_scan.py`, which you can also run by hand).

### Changed

- The morning brief shows each task once, in its most urgent section (overdue, next 7 days, to-do *Now*, project next step) and lists every active project.
- The validator reads the allowed `author` values from `vault_conventions.md`.
- Obsidian hides the instruction files, session logs and archived briefs from link suggestions.

## [1.0.0] — 2026-10-22

First public release.

- Vault skeleton: six areas with hubs, conventions, templates for 20 note types, Obsidian Bases views and Web Clipper template.
- Claude Code layer: hooks (session start, validate on edit, commit and push on stop), a global installer with `--uninstall`, and the skills `/inbox`, `/ingest`, `/new-project`, `/weekly-review`, `/journal-close`, `/interview`.
- Telegram morning brief with GitHub Actions, no LLM and no tokens; opt-in schedule, language, time zone and archive configured with repository variables.
- Security hardening: the stop hook commits only the AI's own changes and never `.claude/`, `.github/` or `.obsidian/`; the chat id is never discovered and used automatically; pinned actions and Dependabot.
- README in English and Spanish with a step-by-step setup.
