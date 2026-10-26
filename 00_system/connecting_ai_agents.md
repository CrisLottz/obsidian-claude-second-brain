---
title: Connecting AI agents to the vault
type: howto
status: draft
author: ai
created: 2026-10-26
updated: 2026-10-26
summary: How an AI other than Claude Code (Codex, Cursor, Copilot, Gemini CLI, Qwen Code, Aider, OpenCode…) reads the vault rules through AGENTS.md, what each tool needs, and the privacy limits.
up:
  - "[[00_home]]"
tags: [system, setup, ai]
aliases: [Connecting AI agents]
---

# Connecting AI agents to the vault

## When to use

You want to work on the vault with an AI that is not Claude Code, or you add a new one.

## How it works

- `CLAUDE.md` and `.claude/global/CLAUDE.md` stay the single source of the rules, written for Claude Code, which keeps hooks, skills and the global setup.
- `AGENTS.md` is the entry point for every other agent: the non-negotiable rules inline, the order to read the files, and a table that translates what only Claude does (hooks, `author`, commit, skills).
- `GEMINI.md` and `QWEN.md` are three-line pointers to `AGENTS.md` for tools that don't read it by default.
- These agents don't run the hooks. They pull, validate and (when you ask) commit by hand following `AGENTS.md`. If they forget, your Obsidian Git plugin saves the files later.

## What each tool needs

| Tool | Reads | Setup |
|---|---|---|
| Claude Code | `CLAUDE.md` | `python <vault>/.claude/global/install.py` once per machine |
| Gemini CLI | `GEMINI.md` | None |
| Qwen Code | `QWEN.md` | None (or `contextFileName: ["AGENTS.md"]` in `.qwen/settings.json`) |
| Codex CLI, Cursor, GitHub Copilot, OpenCode, Zed, Windsurf, Amp | `AGENTS.md` | None |
| Aider | Nothing by default | `aider --read AGENTS.md`, or `read: AGENTS.md` in `.aider.conf.yml` |
| Local or hosted models (DeepSeek, Llama…) | Nothing: they are models, not agents | Run them inside one of the tools above (for example OpenCode or Aider with Ollama or LM Studio), or paste `AGENTS.md` as the system prompt |

## Adding a new AI

1. If its tool reads `AGENTS.md`, skip to step 3.
2. Otherwise create a pointer `<NAME>.md` at the root with the same three lines as `GEMINI.md`, and add it to `SKIP_FILES` in `.claude/hooks/validate_frontmatter.py`, to the root row of §1 in [[vault_conventions]] and to `userIgnoreFilters` in `.obsidian/app.json`.
3. Add its row to the `author` table in [[vault_conventions]] (§5), so the validator accepts it.
4. Tooling changes (`.claude/`, `.github/`, `.obsidian/`): review and commit them yourself.

## Limits (read before connecting a model you don't trust)

- The rules are **instructions, not locks**. Strong models follow them well; small local models often miss conventions. A model built to ignore instructions will ignore them.
- Connecting the vault means **sending it** the notes the agent reads: money, health, diary, people. A third-party API receives that data under its own policy. For models you don't trust, run them locally, or give them one folder instead of the whole vault.

## Verify

- Ask the agent which `author` value it uses and which skills the vault has: it must answer its own value and the list in `.claude/skills/`.

## Rollback

- Delete the pointer file and the `author` row. `AGENTS.md` keeps working for the other agents.
