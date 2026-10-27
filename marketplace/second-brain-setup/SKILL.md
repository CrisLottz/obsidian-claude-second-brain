---
name: second-brain-setup
description: Guides the user through setting up an AI-ready second brain - an Obsidian vault of plain Markdown synced with Git, with rules, hooks and skills for Claude Code (and AGENTS.md for other agents) - from the free obsidian-claude-second-brain template. Use when the user wants to create a second brain, a personal knowledge base or an Obsidian vault that an AI agent can read and maintain, or asks how to set up Claude Code with Obsidian.
---

# Second brain setup

Sets up the open-source template `CrisLottz/obsidian-claude-second-brain` (MIT, https://github.com/CrisLottz/obsidian-claude-second-brain) as the user's own private vault. Total time for the user: about 20 minutes.

This skill only guides and runs the steps below. **Ask before every step that creates or changes something outside the current folder** (a GitHub repo, files in `~/.claude`, repository secrets). Say what the step does, then wait for a yes.

## 0. What the user gets (say it in two lines)

- A folder of Markdown notes (areas, hubs, 20 note templates, conventions) that Obsidian opens and any AI agent can read.
- With Claude Code: hooks that pull, validate and commit the notes the AI edits, plus the skills `/inbox`, `/ingest`, `/new-project`, `/weekly-review`, `/day-close`, `/journal-close` and `/interview`.
- Optional Telegram morning brief from GitHub Actions: no AI, no tokens.

Other agents (Codex, Cursor, Gemini CLI, Qwen Code, Aider…) use the same notes through `AGENTS.md`; they don't get the hooks.

## 1. Check the prerequisites

Run (read-only):

```
python "${CLAUDE_SKILL_DIR}/scripts/check_prereqs.py"
```

(`python3` on macOS/Linux, `py` on Windows.) It reports Git, Python, the GitHub CLI, whether `gh` is logged in, Git identity and the Claude Code CLI. Fix what it flags before going on: details and install links are in `references/troubleshooting.md`. Obsidian 1.9+ cannot be detected: ask the user to confirm it is installed.

## 2. Create the user's own vault

Ask for a repository name (default `my-second-brain`) and a folder to clone it into. The folder path must have **no spaces or accents** and must **not be inside OneDrive, iCloud Drive or Dropbox**. Confirm, then:

```
gh repo create <name> --private --template CrisLottz/obsidian-claude-second-brain
gh repo clone <name> <folder>
```

- Always `--private`: the vault will hold the user's life, and Git history keeps every version. Never change it to public without the user explicitly asking, and warn them that making it public later publishes the whole history.
- If the clone comes out empty, GitHub was still copying the template: delete the folder, wait a few seconds and clone again.

## 3. Open it in Obsidian (the user does this)

1. Obsidian → **Open folder as vault** → the cloned folder.
2. Choose **Trust author and enable plugins**.
3. **Settings → Community plugins → Browse** → search **Git** (by Vinzent03) → Install → Enable. Its settings come with the vault.

## 4. Claude Code: run the installer (once per machine)

Skip this step for agents other than Claude Code. Before running it, explain what it does and ask for a yes:

- adds a marked block to `~/.claude/CLAUDE.md` with the vault's path;
- gives Claude sessions access to the vault folder and installs the vault hooks globally in `~/.claude/settings.json` (the previous file is backed up);
- links the vault's skills into `~/.claude/skills`.

Install it only on the user's own computer. Then:

```
python <folder>/.claude/global/install.py
```

It prints one line per item and ends with `Done`. If it prints a `WARNING`, fix that and run it again. It is safe to re-run, and `install.py --uninstall` undoes it.

## 5. First session

Tell the user to open a new terminal in the vault folder, run `claude`, trust the folder (that lets the hooks run) and type `/interview`: seven short rounds of questions that write their profile, the summary in `00_home.md` and how the AI should work with them. For other agents: open the folder in the agent and ask it to read `AGENTS.md`.

## 6. Verify

```
python <folder>/.claude/hooks/validate_frontmatter.py --all
```

It must end with `0 with problems`. Then ask the AI to create a test note called `hello` in `01_inbox/`: after it answers, `git log -1 --format=%s` should show a commit starting with `claude:`; then ask it to delete the note.

## 7. Optional extras (offer, don't push)

- **Telegram morning brief** — `references/telegram-brief.md`. Never ask the user to paste the bot token into the chat: tell them to save it in the GitHub repository secrets page, or have them run `gh secret set TELEGRAM_BOT_TOKEN` themselves in their terminal.
- **`/day-close` reminders**, **YouTube for `/ingest`**, **Web Clipper** — `references/troubleshooting.md` lists the commands.
- **How the vault is organized** and how to customize it — `references/vault-conventions.md`.

## Rules for you while following this skill

- Never ask the user to share secrets, tokens or the contents of their notes.
- Never make the repository public, add collaborators or push anything the user didn't ask for.
- If a step fails, show the exact error, check `references/troubleshooting.md` and fix the cause; don't skip the step.
- When done, summarize in a few lines what was created and where, and how to undo it (`install.py --uninstall`, delete the folder, delete the GitHub repo).
