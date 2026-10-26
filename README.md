# Obsidian + Claude Second Brain

**An AI-ready second brain for Obsidian.** Plain Markdown and Git, built for Claude Code, usable by any AI agent — with a morning brief on Telegram that costs zero tokens.

**English** · [Español](#español)

---

## Table of contents

- [What is this?](#what-is-this)
- [Works with any AI, built for Claude](#works-with-any-ai-built-for-claude)
- [Why it's different](#why-its-different)
- [What's inside](#whats-inside)
- [Requirements](#requirements)
- [Setup, step by step](#setup-step-by-step) (about 20 minutes)
- [Telegram morning brief](#telegram-morning-brief) (5 more minutes)
- [Daily workflow](#daily-workflow)
- [Customize it](#customize-it)
- [A second machine](#a-second-machine)
- [Security and privacy](#security-and-privacy)
- [Uninstall](#uninstall)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## What is this?

A ready-to-use Obsidian vault that works as **one place for your whole life** — work, projects, knowledge, health, books and movies, money, diary, people — designed so an AI can find its way around it the way you do.

The AI never reads your whole vault. It reads a short **root note** (who you are and a map of your areas), then the **hub** of the area it needs, then only the notes that matter, choosing them by the one-line `summary` in each note's properties (YAML frontmatter). That's *progressive disclosure*: the AI knows you in ~1,000–2,000 tokens and opens the rest only on demand.

Everything is plain Markdown in a Git repository: your notes are yours, they sync across Windows, macOS and Linux, and every change the AI makes is committed, so it can always be reviewed and undone.

**Goal of this project:** give anyone a second brain that an AI can actually use — structured, validated, versioned and safe — in about 20 minutes, instead of the usual "point the AI at a messy folder and hope".

## Works with any AI, built for Claude

- **Claude Code** gets the full experience: hooks that sync, validate and commit, six slash-command skills, and a global setup so Claude knows you in *any* project folder.
- **Other AI agents with file access** (Codex, Cursor, Aider, Gemini CLI, a local model through an agent) can use the vault too: the notes, hubs and rules are plain Markdown and YAML, and `AGENTS.md` tells them where to start. They don't run the hooks, so they validate notes with one command and your Obsidian Git plugin commits the changes.
- **Chat apps** (ChatGPT, Gemini, Claude.ai) can't open a folder on your computer: attach `00_home.md` and the notes you need to the conversation.
- **The Telegram brief uses no AI at all**: a plain Python script reads your notes on GitHub Actions.

## Why it's different

What most people do: open an AI in their Obsidian folder and let it read and write whatever it finds. It works for a week, then context gets wasted, notes get messy and nobody knows what the AI changed.

| | Basic "Obsidian + AI" setup | This template |
|---|---|---|
| **Context** | The AI greps random notes or you paste context every time | A root map and hubs with one-line descriptions; each note has a `summary`. The AI knows where everything is in ~1,000–2,000 tokens |
| **Structure** | Folders invented on the fly | 6 areas, hubs, `up` links from every note to its hub, sub-hubs that appear only when a topic grows (~10 notes) |
| **Metadata** | Free-form, inconsistent | A YAML schema with closed lists of `type` and `status`, **checked by a validator hook** every time Claude edits a note; errors go straight back to Claude to fix |
| **Safety** | AI edits overwrite notes silently | After each response, the notes Claude touched are **committed and pushed** with its session-log line as the message — only its files, never what you had staged, and never code or config in `.claude/`, `.github/` or `.obsidian/` (those wait for your review). Review or revert anything |
| **Authorship** | Unknown who wrote what | `author: human \| ai \| mixed` in every note, plus a `claude:` prefix and a co-author line on AI commits |
| **Memory between sessions** | Gone | A monthly session log; each session starts with its latest entries and the inbox count |
| **Outside the vault** | Only works inside the vault folder | A **global install**: in any code project Claude knows you, finds the project's note by its git remote, and keeps it updated |
| **Capture** | You file everything by hand | Notes land in an inbox; `/inbox` files them. Web Clipper template, `/ingest` for articles and YouTube videos |
| **Daily overview** | None | A **Telegram morning brief** — deadlines, overdue items, next steps, inbox — via GitHub Actions, PC off, zero tokens |
| **Dynamic queries** | Dataview tables the AI can't see in the raw file | Literal links in hubs; Obsidian **Bases** only for human views, reading the same YAML |
| **Multi-OS** | Windows quirks, broken line endings | LF everywhere, Python standard library only, hooks through Git Bash on Windows, one installer per machine |

## What's inside

```
.
├── 00_home.md                 ← root note: your profile summary + map of the areas (loaded in every session)
├── CLAUDE.md                  ← rules for the AI inside the vault
├── AGENTS.md                  ← where other AI agents start
├── 00_system/
│   ├── vault_conventions.md   ← THE rules: folders, names, links, dates, YAML, types, statuses, sizes
│   ├── templates/             ← 20 note templates (project, note, howto, incident, review, person, recipe…)
│   ├── maintenance.base       ← inbox, drafts, outdated notes and authorship at a glance
│   └── web_clipper_resource.json
├── 01_inbox/                  ← new notes land here (create first, organize later)
├── 02_work/  03_projects/  04_knowledge/  05_life/  06_media/  07_personal/   ← the 6 areas, one hub each
├── 99_assets/                 ← images only
├── .obsidian/                 ← links, templates folder, property types, core plugins, Obsidian Git settings
├── .claude/
│   ├── settings.json          ← hooks: pull at start, validate on edit, commit + push after each response
│   ├── hooks/                 ← run.sh (finds Python), vault_hooks.py, validate_frontmatter.py
│   ├── skills/                ← /inbox /ingest /new-project /weekly-review /journal-close /interview
│   └── global/                ← CLAUDE.md for every session + install.py
└── .github/
    ├── workflows/morning_brief.yml
    ├── scripts/morning_brief.py
    └── dependabot.yml         ← keeps the pinned GitHub Action up to date
```

## Requirements

- [Obsidian](https://obsidian.md) **1.9 or newer** (free; Bases need 1.9). On Linux use the AppImage or `.deb`: the Flatpak and Snap sandboxes can stop the Git plugin from running `git`.
- [Git](https://git-scm.com). On Windows, **Git for Windows**: it includes Git Bash, which Claude Code uses to run the hooks.
- A GitHub account and the [GitHub CLI](https://cli.github.com) (`gh`).
- Python 3.8+ — on Windows the launcher is `py`; on macOS/Linux it's `python3`. Nothing to `pip install` for the core.
- [Claude Code](https://claude.com/claude-code) with a paid Claude plan (Pro, Max, Team or Enterprise) or a Claude Console account with API credits — or another AI agent for the parts that aren't Claude-specific.
- Optional: Telegram, for the morning brief.

## Setup, step by step

Commands are given for **PowerShell** (Windows) and **bash/zsh** (macOS, Linux). `"$HOME/second-brain"` works in both.

### 0. Install the tools and sign in to GitHub

**Windows** (PowerShell):

```powershell
winget install --id Git.Git -e
winget install --id GitHub.cli -e
winget install --id Python.Python.3.12 -e
winget install --id Obsidian.Obsidian -e
```

**macOS** ([Homebrew](https://brew.sh)):

```bash
brew install git gh python
brew install --cask obsidian
```

**Linux** (Debian/Ubuntu; for other distros see each tool's site):

```bash
sudo apt install git gh python3
```

…and Obsidian's AppImage or `.deb` from [obsidian.md/download](https://obsidian.md/download).

Then **open a new terminal** (so it sees the new programs) and run, one line at a time:

```bash
gh auth login
gh auth setup-git
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

`gh auth login`: choose *GitHub.com* and *HTTPS*, and log in with the browser. `gh auth setup-git` lets `git` push with that login. The name and email sign your commits — the hooks can't commit without them. To keep your email private, use the `…@users.noreply.github.com` address from *GitHub → Settings → Emails*.

### 1. Create your own vault from this template

Click **Use this template → Create a new repository** at the top of this page and make it **Private** — it will hold your life. Or from the terminal:

```bash
gh repo create my-second-brain --private --template CrisLottz/obsidian-claude-second-brain
```

### 2. Clone it

```bash
gh repo clone my-second-brain "$HOME/second-brain"
```

(If the folder comes out empty, GitHub was still copying the template: delete the folder, wait a few seconds and clone again.)

Where to put it: a path **without spaces, accents or symbols**, and **never inside OneDrive, iCloud Drive or Dropbox** — Git is the only sync. The rest of this guide assumes `~/second-brain` (`C:\Users\<you>\second-brain` on Windows).

### 3. Open it in Obsidian

1. In Obsidian: **Open folder as vault** → pick the `second-brain` folder.
2. Obsidian asks whether you trust the vault's author (it has a community plugin listed): choose **Trust author and enable plugins**.
3. **Settings → Community plugins → Browse** → search **Git** (by Vinzent03) → **Install** → **Enable**. Its settings already come with the vault: commit-and-sync 15 minutes after you stop editing, and pull when Obsidian starts.

Links, the templates folder (`00_system/templates`), the attachments folder and the property types are already configured.

### 4. Install Claude Code

**Windows** (PowerShell):

```powershell
irm https://claude.ai/install.ps1 | iex
```

**macOS / Linux**:

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

Open a **new terminal**, check it with `claude --version`, then run `claude` once, sign in, and leave with `/exit`.

### 5. Run the installer (once per machine)

**Windows:**

```powershell
py "$HOME/second-brain/.claude/global/install.py"
```

**macOS / Linux:**

```bash
python3 "$HOME/second-brain/.claude/global/install.py"
```

You should see one line per item, ending in `Done`:

```
…/.claude/CLAUDE.md: vault import written
…/.claude/settings.json: vault access and global hooks set (previous file backed up)
…/.claude/skills: /inbox: linked; /ingest: linked; /interview: linked; …
Done. Restart Claude Code sessions to load the new global setup. Undo it with: install.py --uninstall
```

What it does (safe to re-run; re-run it if you move the vault):
- adds to `~/.claude/CLAUDE.md` a short, marked block with the vault's path and an import of `.claude/global/CLAUDE.md`, so **every** Claude session knows you and your vault;
- gives every session access to the vault folder and installs the vault hooks globally; your previous `~/.claude/settings.json` is backed up next to it whenever it changes;
- links the vault skills into `~/.claude/skills`, so `/inbox`, `/ingest`… work in any project.

If it prints a `WARNING` (Git not found, no Git identity), fix that and run it again. See [Security and privacy](#security-and-privacy) for what this grants, and [Uninstall](#uninstall) to undo it.

### 6. First session

```bash
cd "$HOME/second-brain"
claude
```

1. Claude Code asks whether you trust this folder: **yes** — that's what lets the vault's hooks run.
2. The start-of-session hook pulls from GitHub and hands Claude a short report (pull status, latest session-log lines, inbox count, today's date). It goes into Claude's context, not onto your screen: ask *"What did the vault hook report?"* to see it.
3. Run **`/interview`**: Claude asks you seven short rounds of questions and writes your profile, the summary in `00_home.md`, your people and context, and your preferences for how it should work with you.

### 7. Optional extras

- **Telegram morning brief** — [setup below](#telegram-morning-brief).
- **End-of-day review (`/day-close`)** — run it in the evening so tomorrow's brief only lists what is really pending. To get a nudge, set the environment variable `VAULT_DAY_CLOSE_HOUR` (for example `20`) in `~/.claude/settings.json` under `"env"`: from that hour, until the review is in the log, Claude reminds you once every 90 minutes. A Telegram version also exists: set the repository variable `DAY_CLOSE_ENABLED` = `true` (same bot secrets, `BRIEF_LANG` and `BRIEF_TIMEZONE` as the brief); GitHub may start it late, so it skips runs that begin before 18:00.
- **YouTube for `/ingest`** — `py -m pip install --user youtube-transcript-api` on Windows, `python3 -m pip install --user youtube-transcript-api` on macOS/Linux. If Linux answers `externally-managed-environment`, add `--break-system-packages` (with `--user` it only installs for your account).
- **Obsidian Web Clipper** (browser extension), in its settings:
  1. **General → Vaults**: add your vault's name (`second-brain`).
  2. **Properties → Import**: paste the contents of `.obsidian/types.json`.
  3. **Templates → Import**: choose `00_system/web_clipper_resource.json`, then drag that template to the top of the list so it is the default. Clips land in `01_inbox/` as `type: resource`.

### Verify

1. Validator — in the vault folder: `py .claude/hooks/validate_frontmatter.py --all` (Windows) or `python3 .claude/hooks/validate_frontmatter.py --all` → ends with `0 with problems`.
2. Auto-commit — ask Claude *"Create a test note in the inbox called hello"*. When it finishes answering, `git log -1 --format=%s` shows a commit starting with `claude:`. Then ask it to delete the note.
3. Global setup — open `claude` in any other folder and ask *"What do you know about me?"*: it answers from your root note (after `/interview`).

## Telegram morning brief

Every morning a Telegram message with: deadlines in the next 7 days, overdue items, your to-do *Now* list, the next step of each active project, pending payments this month, the inbox size and the vault's health. It runs on **GitHub Actions** (free at this usage), so your computer can be off, and it uses **no AI and no tokens**: a Python script reads the properties and tasks of your notes.

### Set it up (about 5 minutes)

1. **Create the bot.** In Telegram, open **@BotFather** → `/newbot` → give it a name and a username ending in `bot`. Copy the **token** it gives you. Then send `/setjoingroups`, choose your bot and pick **Disable**, so nobody can add it to a group.
2. **Start a chat with it.** Open `t.me/<your_bot_username>` and press **Start**. Check the `@username` at the top of the chat: several bots can share the same display name.
3. **Save the token as a secret.** In your vault's repo on GitHub: **Settings → Secrets and variables → Actions → Secrets → New repository secret** → Name `TELEGRAM_BOT_TOKEN`, paste the token → **Add secret**. Never paste it into a note or a chat; if it leaks, `/revoke` it in BotFather and save the new one.
4. **Set the variables** in the **Variables** tab of the same page (**New repository variable**), before the first run:

   | Variable | Example | What it does |
   |---|---|---|
   | `BRIEF_LANG` | `en` or `es` | Language of the brief's labels (default `en`) |
   | `BRIEF_TIMEZONE` | `Europe/Madrid` | Your time zone, for "today" and deadlines — a name from the [IANA list](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) (default `UTC`) |
   | `BRIEF_ARCHIVE` | `true` | Also saves each brief in `00_system/briefs/brief_YYYY_MM.md` and commits it, so the vault keeps a dated history of your briefs (one commit per day) |
   | `BRIEF_GIT_NAME` / `BRIEF_GIT_EMAIL` | your name / your noreply email | Author of that commit. Default: the GitHub Actions bot. With your name and your `…@users.noreply.github.com` email the commit is attributed to your account |
   | `BRIEF_ENABLED` | `true` | Turns the **daily schedule** on — set it in step 6. Manual runs always work |

5. **Find your chat id and send the first brief.**
   1. Open the **Actions** tab (if GitHub asks, enable workflows) → **Morning brief** → **Run workflow** → **Run workflow**.
   2. Open the run → job **brief** → step **Build and send the brief**. Without a chat id it lists the private chats that wrote to the bot, like `123456789  @you`, and stops without sending anything (the run shows as failed — expected).
   3. Save **your** number as a second secret, `TELEGRAM_CHAT_ID`, and run the workflow again. The step now ends with `Sent` and the brief arrives.

   Telegram only keeps a bot's messages for 24 hours: if the list is empty, press **Start** (or send `/start`) again and re-run.
6. **Turn on the daily schedule**: add the variable `BRIEF_ENABLED` = `true`.
7. **Pick the time.** It's the one line to edit in `.github/workflows/morning_brief.yml` (variables can't set it):

   ```yaml
   - cron: "37 6 * * *"        # minute hour * * * → 06:37 every day
     timezone: "Europe/Madrid" # your IANA time zone; daylight saving is handled
   ```

   Commit and push the change. GitHub can start scheduled runs a few minutes late (more at busy times, especially on the hour), so an off-peak minute like `:37` is a good choice.

Optional: give the bot a picture with BotFather → `/setuserpic` — **choose the bot first**, then send the image as a photo.

Preview it on your computer, without sending anything: `py .github/scripts/morning_brief.py --dry-run` (Windows) or `python3 .github/scripts/morning_brief.py --dry-run`.

### How your notes feed it

- **Deadlines:** mark them with `📅 YYYY-MM-DD` at the end of an open task — `- [ ] Pay rent 📅 2026-11-05` — or in a note's `due` property. The next 7 days go under the upcoming list; past dates of open tasks and unfinished notes go under *Overdue*. Any other date in a task is just context and is ignored. Each task is shown once, so keep it in one note only (*one task, one note*).
- **To do now:** the open tasks under `## Now` in `07_personal/todo.md`.
- **Next steps:** the first open task under `## Next steps` of each project with `status: active`.
- **Names:** the brief shows each note's **first alias** — write it in the language you want to read (see [Customize it](#customize-it)).

## Daily workflow

1. **Capture without thinking:** `Ctrl+N` (`Cmd+N` on macOS) in Obsidian — the note lands in `01_inbox/` — the Web Clipper for articles, or `/ingest <url>` for articles and YouTube videos.
2. **File it:** `/inbox` shows a plan (new name, type, folder, hub) and files everything after your OK.
3. **Work on code:** open `claude` inside a project. The first time, ask it to *"connect this project to my vault"*: it creates the project note with the repo's `owner/name`, and from then on every session in that repo starts with it.
4. **Review:** `/weekly-review` once a week, `/journal-close` once a month.
5. **Every morning:** read the brief on your phone.

| Skill | What it does |
|---|---|
| `/inbox` | Files raw captures: renames, completes the properties, moves them and links them from their hub |
| `/ingest <url>` | Turns an article or YouTube video into a `resource` note with key points and links |
| `/new-project <name>` | Creates a project note wired to its hub, the root note and its GitHub repos |
| `/weekly-review` | Done, blocked, deadlines, money, vault health and proposed priorities |
| `/day-close` | Checks each open task against evidence (log, commits, GitHub), closes what is done and previews tomorrow's brief |
| `/journal-close [YYYY-MM]` | Distills a month of diary into your profile, people and context |
| `/interview` | Builds or refreshes your profile and how the AI should work with you |

## Customize it

- **Areas and hubs:** to add or rename an area, create its folder and its `hub_<area>.md` (from `tpl_hub`), update the folder table in `00_system/vault_conventions.md` §1, and list the hub under *Active* in `00_home.md`. Sub-hubs appear when ~10 notes share a topic.
- **Types and statuses:** edit the tables in `vault_conventions.md` §5 — the validator reads the allowed values from there.
- **Your language:** write each note's first alias and your tasks in your language (that's what the brief shows); set `BRIEF_LANG`; `/interview` fills the *Language* section of `.claude/global/CLAUDE.md`. File names, YAML keys and section headings (`## Now`, `## Next steps`) stay in English so the scripts can rely on them.
- **The co-author line on AI commits:** `CO_AUTHOR` at the top of `.claude/hooks/vault_hooks.py` (set it to `""` to drop it).
- **Other AI agents:** they start at `AGENTS.md`; if yours only reads its own file name (such as `GEMINI.md`), copy it under that name.

## A second machine

1. Install the tools and sign in ([step 0](#0-install-the-tools-and-sign-in-to-github)), then `gh repo clone my-second-brain "$HOME/second-brain"`.
2. Open the folder in Obsidian → **Trust author and enable plugins** → install and enable the **Git** plugin (its settings come with the repo).
3. Install Claude Code ([step 4](#4-install-claude-code)) and run the installer ([step 5](#5-run-the-installer-once-per-machine)).

## Security and privacy

- **Keep your vault repo private — forever.** Git history keeps every version of every note: making the repo public later publishes all of it, including what you deleted.
- **What the global install grants.** Claude Code sessions opened in any folder can read and edit your vault, and the vault's hook scripts run at the start and end of every session on that machine. Install it only on your own computers; `install.py --uninstall` removes it.
- **Your Git remote is trusted code.** The hooks, skills and workflow come from your repo and run on your computer and on GitHub, so anyone who can push to it can change what runs. Keep it private and don't add collaborators you wouldn't hand your computer to. When a pull changes `.claude/`, `.github/` or `.obsidian/plugins/`, the start-of-session hook tells Claude, so it can tell you; review with `git log -p`. The AI's own changes there are never auto-committed.
- **Content you ingest is untrusted.** Web pages and transcripts can hide instructions aimed at AIs (prompt injection). `/ingest` treats them as data to summarize and tells you when a page contains such text; still, skim what it writes, and never let an AI run commands a page suggests.
- **Secrets never go in notes.** `.gitignore` blocks common key, credential and password-database files as a second line of defense. Obsidian plugin settings (`.obsidian/plugins/*/data.json`), where plugins keep API keys, are not synced — except Obsidian Git's, which holds none.
- **The brief leaves your vault.** It travels through Telegram's servers (bot chats are not end-to-end encrypted) and the run logs stay in your repo's Actions tab. Keep in it only what you'd put in a phone notification, and keep groups disabled for the bot (`/setjoingroups` → Disable).

## Uninstall

```powershell
py "$HOME/second-brain/.claude/global/install.py" --uninstall
```

(`python3 …` on macOS/Linux.) It removes the block from `~/.claude/CLAUDE.md`, the vault hooks and folder access from `~/.claude/settings.json` (backed up first) and the skill links; your other settings and the vault itself are left as they are. To remove everything, delete the vault folder afterwards, and the GitHub repo if you no longer want it.

## Troubleshooting

- **`Author identity unknown` / `Please tell me who you are`** — Git has no name and email: run the two `git config --global` lines of [step 0](#0-install-the-tools-and-sign-in-to-github).
- **`git push` asks for a password or fails with `Authentication failed`** — run `gh auth login` and `gh auth setup-git`.
- **`python` opens the Microsoft Store (Windows)** — use `py`, or turn off the `python.exe` aliases in *Settings → Apps → Advanced app settings → App execution aliases*.
- **Hooks don't run on Windows** — Claude Code runs them through Git Bash: install Git for Windows and make sure `py` or `python` works in a new terminal.
- **"git pull failed" right after opening Obsidian** — Obsidian Git pulled at the same moment; the hook retries once. If it persists, run `git status` in the vault.
- **"Not auto-committed (code or app config…)"** — expected: changes in `.claude/`, `.github/` and `.obsidian/` wait for you. Review them with `git diff` and commit them yourself.
- **The validator complains after an edit** — the message says which property breaks which rule in `vault_conventions.md`; Claude fixes it on the spot.
- **Warnings on `{{title}}` or dates inside templates** — normal: they become real values when you insert the template. Edit templates in Source mode.
- **Claude doesn't know you in other folders** — re-run the installer and restart Claude Code. If the vault path has spaces, move it to one without spaces (the installer warns about this).
- **Telegram: `Unauthorized`** — the token is wrong or was revoked: save it again as `TELEGRAM_BOT_TOKEN`. **`chat not found`** — the chat id is wrong, or you never pressed **Start** in your bot's chat.
- **Telegram: the chat list is empty** — send `/start` to your bot (the right `@username`) and re-run within 24 hours.
- **The archive commit fails with `403` / `Permission denied to github-actions[bot]`** — *Settings → Actions → General → Workflow permissions* → **Read and write permissions** (an organization can lock this setting).
- **The scheduled brief doesn't arrive** — check that `BRIEF_ENABLED` is `true` and the workflow change is on the default branch; scheduled runs can start late at busy times.

## License

[MIT](LICENSE).

---

# Español

**Un segundo cerebro para Obsidian listo para la IA.** Markdown y Git, pensado para Claude Code, utilizable por cualquier agente de IA — con un resumen matutino en Telegram que no gasta ni un token.

[English](#obsidian--claude-second-brain) · **Español**

Los nombres de menús y botones están en inglés, como en la interfaz por defecto de Obsidian, GitHub y Telegram.

## Índice

- [¿Qué es esto?](#qué-es-esto)
- [Funciona con cualquier IA, pensado para Claude](#funciona-con-cualquier-ia-pensado-para-claude)
- [En qué se diferencia](#en-qué-se-diferencia)
- [Qué incluye](#qué-incluye)
- [Requisitos](#requisitos)
- [Configuración paso a paso](#configuración-paso-a-paso) (unos 20 minutos)
- [Resumen matutino en Telegram](#resumen-matutino-en-telegram) (5 minutos más)
- [Flujo diario](#flujo-diario)
- [Personalízalo](#personalízalo)
- [Una segunda computadora](#una-segunda-computadora)
- [Seguridad y privacidad](#seguridad-y-privacidad)
- [Desinstalar](#desinstalar)
- [Solución de problemas](#solución-de-problemas)
- [Licencia](#licencia)

## ¿Qué es esto?

Un vault de Obsidian listo para usar que funciona como **un solo lugar para toda tu vida** — trabajo, proyectos, conocimiento, salud, libros y películas, dinero, diario, personas — diseñado para que una IA se oriente en él igual que tú.

La IA nunca lee todo tu vault. Lee una **nota raíz** corta (quién eres y un mapa de tus áreas), luego el **hub** del área que necesita y después solo las notas que importan, eligiéndolas por el `summary` de una línea que tiene cada nota en sus propiedades (frontmatter YAML). Eso es *divulgación progresiva*: la IA te conoce con ~1000–2000 tokens y abre lo demás solo cuando hace falta.

Todo es Markdown en un repositorio Git: tus notas son tuyas, se sincronizan entre Windows, macOS y Linux, y cada cambio que hace la IA queda en un commit, así que siempre se puede revisar y deshacer.

**Objetivo del proyecto:** que cualquiera tenga en unos 20 minutos un segundo cerebro que una IA pueda usar de verdad — estructurado, validado, versionado y seguro — en vez del típico "apuntar la IA a una carpeta desordenada y cruzar los dedos".

## Funciona con cualquier IA, pensado para Claude

- **Claude Code** tiene la experiencia completa: hooks que sincronizan, validan y hacen commit, seis skills como comandos, y una configuración global para que Claude te conozca en *cualquier* carpeta de proyecto.
- **Otros agentes de IA con acceso a archivos** (Codex, Cursor, Aider, Gemini CLI, un modelo local a través de un agente) también pueden usar el vault: las notas, los hubs y las reglas son Markdown y YAML, y `AGENTS.md` les dice por dónde empezar. No ejecutan los hooks, así que validan las notas con un comando y tu plugin Obsidian Git hace los commits.
- **Las apps de chat** (ChatGPT, Gemini, Claude.ai) no pueden abrir una carpeta de tu computadora: adjunta a la conversación `00_home.md` y las notas que necesites.
- **El resumen de Telegram no usa IA**: un script de Python lee tus notas en GitHub Actions.

## En qué se diferencia

Lo que hace la mayoría: abrir una IA en su carpeta de Obsidian y dejar que lea y escriba lo que encuentre. Funciona una semana; después se desperdicia contexto, las notas se desordenan y nadie sabe qué cambió la IA.

| | Configuración básica "Obsidian + IA" | Esta plantilla |
|---|---|---|
| **Contexto** | La IA busca notas al azar o tú pegas contexto cada vez | Un mapa raíz y hubs con descripciones de una línea; cada nota tiene `summary`. La IA sabe dónde está todo con ~1000–2000 tokens |
| **Estructura** | Carpetas inventadas sobre la marcha | 6 áreas, hubs, enlaces `up` de cada nota a su hub, sub-hubs que aparecen solo cuando un tema crece (~10 notas) |
| **Metadatos** | Libres e inconsistentes | Un esquema YAML con listas cerradas de `type` y `status`, **revisado por un hook validador** cada vez que Claude edita una nota; los errores le vuelven a Claude para que los corrija |
| **Seguridad** | La IA sobrescribe notas sin avisar | Al terminar cada respuesta, las notas que tocó Claude se **guardan en un commit y se suben**, con su línea de bitácora como mensaje — solo sus archivos, nunca lo que tú tenías en stage, y nunca código ni configuración en `.claude/`, `.github/` u `.obsidian/` (eso espera tu revisión). Revisa o deshaz lo que sea |
| **Autoría** | No se sabe quién escribió qué | `author: human \| ai \| mixed` en cada nota, más el prefijo `claude:` y la línea de coautor en los commits de la IA |
| **Memoria entre sesiones** | Se pierde | Una bitácora mensual; cada sesión empieza con sus últimas entradas y cuántas notas hay en el inbox |
| **Fuera del vault** | Solo funciona dentro de la carpeta del vault | Una **instalación global**: en cualquier proyecto de código Claude te conoce, encuentra la nota del proyecto por su repo de git y la mantiene al día |
| **Captura** | Archivas todo a mano | Las notas caen en un inbox; `/inbox` las archiva. Plantilla para Web Clipper y `/ingest` para artículos y videos de YouTube |
| **Resumen diario** | Ninguno | Un **resumen matutino en Telegram** — plazos, vencidos, siguientes pasos, inbox — con GitHub Actions, PC apagada y cero tokens |
| **Consultas dinámicas** | Tablas de Dataview que la IA no ve en el archivo | Enlaces escritos en los hubs; **Bases** de Obsidian solo para vistas humanas, leyendo el mismo YAML |
| **Varios sistemas** | Rarezas de Windows, saltos de línea rotos | LF en todo, solo la biblioteca estándar de Python, hooks por Git Bash en Windows, un instalador por máquina |

## Qué incluye

```
.
├── 00_home.md                 ← nota raíz: resumen de tu perfil + mapa de las áreas (se carga en cada sesión)
├── CLAUDE.md                  ← reglas para la IA dentro del vault
├── AGENTS.md                  ← por dónde empiezan otros agentes de IA
├── 00_system/
│   ├── vault_conventions.md   ← LAS reglas: carpetas, nombres, enlaces, fechas, YAML, tipos, estados, tamaños
│   ├── templates/             ← 20 plantillas de nota (proyecto, nota, guía, incidente, reseña, persona, receta…)
│   ├── maintenance.base       ← inbox, borradores, notas desactualizadas y autoría de un vistazo
│   └── web_clipper_resource.json
├── 01_inbox/                  ← las notas nuevas caen aquí (primero crea, después organiza)
├── 02_work/  03_projects/  04_knowledge/  05_life/  06_media/  07_personal/   ← las 6 áreas, un hub cada una
├── 99_assets/                 ← solo imágenes
├── .obsidian/                 ← enlaces, carpeta de plantillas, tipos de propiedades, plugins y ajustes de Obsidian Git
├── .claude/
│   ├── settings.json          ← hooks: pull al iniciar, validar al editar, commit + push tras cada respuesta
│   ├── hooks/                 ← run.sh (busca Python), vault_hooks.py, validate_frontmatter.py
│   ├── skills/                ← /inbox /ingest /new-project /weekly-review /journal-close /interview
│   └── global/                ← CLAUDE.md para todas las sesiones + install.py
└── .github/
    ├── workflows/morning_brief.yml
    ├── scripts/morning_brief.py
    └── dependabot.yml         ← mantiene al día la GitHub Action fijada
```

## Requisitos

- [Obsidian](https://obsidian.md) **1.9 o más reciente** (gratis; las Bases necesitan la 1.9). En Linux usa el AppImage o el `.deb`: los sandbox de Flatpak y Snap pueden impedir que el plugin Git ejecute `git`.
- [Git](https://git-scm.com). En Windows, **Git for Windows**: incluye Git Bash, que Claude Code usa para ejecutar los hooks.
- Una cuenta de GitHub y el [GitHub CLI](https://cli.github.com) (`gh`).
- Python 3.8+ — en Windows el lanzador es `py`; en macOS/Linux es `python3`. Para lo básico no hay que instalar nada con `pip`.
- [Claude Code](https://claude.com/claude-code) con un plan de pago de Claude (Pro, Max, Team o Enterprise) o una cuenta de Claude Console con créditos de API — u otro agente de IA para lo que no es exclusivo de Claude.
- Opcional: Telegram, para el resumen matutino.

## Configuración paso a paso

Los comandos vienen para **PowerShell** (Windows) y **bash/zsh** (macOS, Linux). `"$HOME/second-brain"` funciona en ambos.

### 0. Instala las herramientas e inicia sesión en GitHub

**Windows** (PowerShell):

```powershell
winget install --id Git.Git -e
winget install --id GitHub.cli -e
winget install --id Python.Python.3.12 -e
winget install --id Obsidian.Obsidian -e
```

**macOS** ([Homebrew](https://brew.sh)):

```bash
brew install git gh python
brew install --cask obsidian
```

**Linux** (Debian/Ubuntu; para otras distribuciones mira el sitio de cada herramienta):

```bash
sudo apt install git gh python3
```

…y el AppImage o `.deb` de Obsidian desde [obsidian.md/download](https://obsidian.md/download).

Después **abre una terminal nueva** (para que vea los programas recién instalados) y ejecuta, una línea a la vez:

```bash
gh auth login
gh auth setup-git
git config --global user.name "Tu Nombre"
git config --global user.email "tu@correo.com"
```

`gh auth login`: elige *GitHub.com* y *HTTPS*, e inicia sesión con el navegador. `gh auth setup-git` permite que `git` suba cambios con esa sesión. El nombre y el correo firman tus commits — sin ellos los hooks no pueden hacer commit. Si quieres mantener tu correo privado, usa la dirección `…@users.noreply.github.com` de *GitHub → Settings → Emails*.

### 1. Crea tu propio vault desde esta plantilla

Haz clic en **Use this template → Create a new repository** arriba en esta página y créalo **Private** — va a guardar tu vida. O desde la terminal:

```bash
gh repo create mi-segundo-cerebro --private --template CrisLottz/obsidian-claude-second-brain
```

### 2. Clónalo

```bash
gh repo clone mi-segundo-cerebro "$HOME/second-brain"
```

(Si la carpeta queda vacía, GitHub todavía estaba copiando la plantilla: borra la carpeta, espera unos segundos y vuelve a clonar.)

Dónde ponerlo: una ruta **sin espacios, acentos ni símbolos**, y **nunca dentro de OneDrive, iCloud Drive o Dropbox** — Git es la única sincronización. El resto de esta guía asume `~/second-brain` (`C:\Users\<tú>\second-brain` en Windows).

### 3. Ábrelo en Obsidian

1. En Obsidian: **Open folder as vault** → elige la carpeta `second-brain`.
2. Obsidian pregunta si confías en el autor del vault (trae un plugin de la comunidad en la lista): elige **Trust author and enable plugins**.
3. **Settings → Community plugins → Browse** → busca **Git** (de Vinzent03) → **Install** → **Enable**. Sus ajustes ya vienen en el vault: guarda y sincroniza 15 minutos después de que dejes de escribir, y trae los cambios al abrir Obsidian.

Los enlaces, la carpeta de plantillas (`00_system/templates`), la de adjuntos y los tipos de propiedades ya están configurados.

### 4. Instala Claude Code

**Windows** (PowerShell):

```powershell
irm https://claude.ai/install.ps1 | iex
```

**macOS / Linux**:

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

Abre una **terminal nueva**, compruébalo con `claude --version`, luego ejecuta `claude` una vez, inicia sesión y sal con `/exit`.

### 5. Ejecuta el instalador (una vez por máquina)

**Windows:**

```powershell
py "$HOME/second-brain/.claude/global/install.py"
```

**macOS / Linux:**

```bash
python3 "$HOME/second-brain/.claude/global/install.py"
```

Deberías ver una línea por elemento, terminando en `Done`:

```
…/.claude/CLAUDE.md: vault import written
…/.claude/settings.json: vault access and global hooks set (previous file backed up)
…/.claude/skills: /inbox: linked; /ingest: linked; /interview: linked; …
Done. Restart Claude Code sessions to load the new global setup. Undo it with: install.py --uninstall
```

Qué hace (puedes ejecutarlo varias veces; vuelve a ejecutarlo si mueves el vault):
- agrega a `~/.claude/CLAUDE.md` un bloque corto y marcado con la ruta del vault y un import de `.claude/global/CLAUDE.md`, para que **todas** las sesiones de Claude te conozcan a ti y a tu vault;
- da a todas las sesiones acceso a la carpeta del vault e instala sus hooks de forma global; tu `~/.claude/settings.json` anterior se respalda junto al archivo cada vez que cambia;
- enlaza los skills del vault en `~/.claude/skills`, para que `/inbox`, `/ingest`… funcionen en cualquier proyecto.

Si muestra un `WARNING` (Git no encontrado, Git sin identidad), corrígelo y vuelve a ejecutarlo. En [Seguridad y privacidad](#seguridad-y-privacidad) está lo que esto concede, y en [Desinstalar](#desinstalar) cómo deshacerlo.

### 6. Primera sesión

```bash
cd "$HOME/second-brain"
claude
```

1. Claude Code pregunta si confías en esta carpeta: **sí** — es lo que permite que corran los hooks del vault.
2. El hook de inicio hace pull desde GitHub y le pasa a Claude un reporte corto (estado del pull, últimas líneas de la bitácora, notas en el inbox, fecha de hoy). Va al contexto de Claude, no a tu pantalla: pregúntale *"¿Qué reportó el hook del vault?"* para verlo.
3. Ejecuta **`/interview`**: Claude te hace siete rondas cortas de preguntas y escribe tu perfil, el resumen de `00_home.md`, tus personas y contexto, y tus preferencias sobre cómo quieres que trabaje contigo.

### 7. Extras opcionales

- **Resumen matutino en Telegram** — [configuración abajo](#resumen-matutino-en-telegram).
- **Revisión de fin de día (`/day-close`)** — ejecútala por la tarde para que el brief de mañana solo liste lo que de verdad queda pendiente. Para recibir un aviso, define la variable de entorno `VAULT_DAY_CLOSE_HOUR` (por ejemplo `20`) en `~/.claude/settings.json`, bajo `"env"`: desde esa hora, hasta que la revisión esté en el log, Claude te lo recuerda una vez cada 90 minutos. También hay versión por Telegram: define la variable del repositorio `DAY_CLOSE_ENABLED` = `true` (mismos secretos del bot, `BRIEF_LANG` y `BRIEF_TIMEZONE` que el brief); GitHub puede iniciarla tarde, así que omite las ejecuciones que empiezan antes de las 18:00.
- **YouTube para `/ingest`** — `py -m pip install --user youtube-transcript-api` en Windows, `python3 -m pip install --user youtube-transcript-api` en macOS/Linux. Si Linux responde `externally-managed-environment`, agrega `--break-system-packages` (con `--user` solo se instala para tu cuenta).
- **Obsidian Web Clipper** (extensión del navegador), en sus ajustes:
  1. **General → Vaults**: agrega el nombre de tu vault (`second-brain`).
  2. **Properties → Import**: pega el contenido de `.obsidian/types.json`.
  3. **Templates → Import**: elige `00_system/web_clipper_resource.json` y arrastra esa plantilla al primer lugar de la lista para que sea la predeterminada. Los recortes caen en `01_inbox/` como `type: resource`.

### Verifica

1. Validador — en la carpeta del vault: `py .claude/hooks/validate_frontmatter.py --all` (Windows) o `python3 .claude/hooks/validate_frontmatter.py --all` → termina con `0 with problems`.
2. Commit automático — pídele a Claude *"Crea una nota de prueba en el inbox llamada hola"*. Cuando termine de responder, `git log -1 --format=%s` muestra un commit que empieza con `claude:`. Después pídele que la borre.
3. Configuración global — abre `claude` en cualquier otra carpeta y pregúntale *"¿Qué sabes de mí?"*: responde con tu nota raíz (después de `/interview`).

## Resumen matutino en Telegram

Cada mañana un mensaje de Telegram con: plazos de los próximos 7 días, vencidos, tu lista *Now* de pendientes, el siguiente paso de cada proyecto activo, pagos pendientes del mes, el tamaño del inbox y la salud del vault. Corre en **GitHub Actions** (gratis con este uso), así que tu computadora puede estar apagada, y **no usa IA ni tokens**: un script de Python lee las propiedades y las tareas de tus notas.

### Configúralo (unos 5 minutos)

1. **Crea el bot.** En Telegram abre **@BotFather** → `/newbot` → ponle un nombre y un usuario que termine en `bot`. Copia el **token** que te da. Después envía `/setjoingroups`, elige tu bot y selecciona **Disable**, para que nadie pueda agregarlo a un grupo.
2. **Abre un chat con él.** Entra a `t.me/<usuario_de_tu_bot>` y pulsa **Start** (Iniciar). Revisa el `@usuario` arriba del chat: varios bots pueden tener el mismo nombre visible.
3. **Guarda el token como secreto.** En el repo de tu vault en GitHub: **Settings → Secrets and variables → Actions → Secrets → New repository secret** → Name `TELEGRAM_BOT_TOKEN`, pega el token → **Add secret**. Nunca lo pegues en una nota ni en un chat; si se filtra, revócalo con `/revoke` en BotFather y guarda el nuevo.
4. **Configura las variables** en la pestaña **Variables** de la misma página (**New repository variable**), antes de la primera ejecución:

   | Variable | Ejemplo | Qué hace |
   |---|---|---|
   | `BRIEF_LANG` | `en` o `es` | Idioma de las etiquetas del resumen (por defecto `en`) |
   | `BRIEF_TIMEZONE` | `Europe/Madrid` | Tu zona horaria, para "hoy" y los plazos — un nombre de la [lista IANA](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) (por defecto `UTC`) |
   | `BRIEF_ARCHIVE` | `true` | Además guarda cada resumen en `00_system/briefs/brief_YYYY_MM.md` y hace commit, así el vault conserva un historial fechado de tus resúmenes (un commit por día) |
   | `BRIEF_GIT_NAME` / `BRIEF_GIT_EMAIL` | tu nombre / tu correo noreply | Autor de ese commit. Por defecto: el bot de GitHub Actions. Con tu nombre y tu correo `…@users.noreply.github.com`, el commit queda atribuido a tu cuenta |
   | `BRIEF_ENABLED` | `true` | Activa el **horario diario** — configúrala en el paso 6. Las ejecuciones manuales siempre funcionan |

5. **Encuentra tu chat id y envía el primer resumen.**
   1. Abre la pestaña **Actions** (si GitHub lo pide, activa los workflows) → **Morning brief** → **Run workflow** → **Run workflow**.
   2. Abre la ejecución → job **brief** → paso **Build and send the brief**. Sin chat id, lista los chats privados que le escribieron al bot, como `123456789  @tú`, y se detiene sin enviar nada (la ejecución aparece como fallida — es lo esperado).
   3. Guarda **tu** número como segundo secreto, `TELEGRAM_CHAT_ID`, y vuelve a ejecutar el workflow. Ahora el paso termina con `Sent` y llega el resumen.

   Telegram solo guarda los mensajes de un bot durante 24 horas: si la lista sale vacía, pulsa **Start** (o envía `/start`) de nuevo y vuelve a ejecutarlo.
6. **Activa el horario diario**: agrega la variable `BRIEF_ENABLED` = `true`.
7. **Elige la hora.** Es la única línea que hay que editar en `.github/workflows/morning_brief.yml` (las variables no pueden cambiarla):

   ```yaml
   - cron: "37 6 * * *"        # minuto hora * * * → 06:37 todos los días
     timezone: "Europe/Madrid" # tu zona horaria IANA; el horario de verano se maneja solo
   ```

   Haz commit y push del cambio. GitHub puede iniciar las tareas programadas con unos minutos de retraso (más en horas de mucha carga, sobre todo en punto), así que un minuto poco usado como `:37` es buena idea.

Opcional: ponle foto al bot con BotFather → `/setuserpic` — **elige primero el bot** y después envía la imagen como foto.

Previsualízalo en tu computadora, sin enviar nada: `py .github/scripts/morning_brief.py --dry-run` (Windows) o `python3 .github/scripts/morning_brief.py --dry-run`.

### Cómo lo alimentan tus notas

- **Plazos:** márcalos con `📅 AAAA-MM-DD` al final de una tarea abierta — `- [ ] Pagar el alquiler 📅 2026-11-05` — o en la propiedad `due` de una nota. Los próximos 7 días van a la lista de próximos; las fechas pasadas de tareas abiertas y de notas sin terminar van a *Vencidos*. Cualquier otra fecha en una tarea es solo contexto y se ignora. Cada tarea se muestra una sola vez, así que déjala en una sola nota (*una tarea, una nota*).
- **Pendientes ahora:** las tareas abiertas bajo `## Now` en `07_personal/todo.md`.
- **Siguientes pasos:** la primera tarea abierta bajo `## Next steps` de cada proyecto con `status: active`.
- **Nombres:** el resumen muestra el **primer alias** de cada nota — escríbelo en el idioma que quieras leer (ver [Personalízalo](#personalízalo)).

## Flujo diario

1. **Captura sin pensar:** `Ctrl+N` (`Cmd+N` en macOS) en Obsidian — la nota cae en `01_inbox/` —, el Web Clipper para artículos, o `/ingest <url>` para artículos y videos de YouTube.
2. **Archívalo:** `/inbox` te muestra un plan (nombre nuevo, tipo, carpeta, hub) y archiva todo con tu OK.
3. **Trabaja en código:** abre `claude` dentro de un proyecto. La primera vez pídele que *"conecte este proyecto con mi vault"*: crea la nota del proyecto con el `owner/name` del repo, y desde entonces cada sesión en ese repo arranca con ella.
4. **Revisa:** `/weekly-review` una vez por semana y `/journal-close` una vez al mes.
5. **Cada mañana:** lee el resumen en tu celular.

| Skill | Qué hace |
|---|---|
| `/inbox` | Archiva las capturas: renombra, completa las propiedades, las mueve y las enlaza desde su hub |
| `/ingest <url>` | Convierte un artículo o video de YouTube en una nota `resource` con puntos clave y enlaces |
| `/new-project <nombre>` | Crea una nota de proyecto conectada a su hub, a la nota raíz y a sus repos de GitHub |
| `/weekly-review` | Hecho, bloqueado, plazos, dinero, salud del vault y prioridades propuestas |
| `/day-close` | Revisa cada tarea abierta contra evidencia (log, commits, GitHub), cierra lo hecho y muestra cómo quedará el brief de mañana |
| `/journal-close [AAAA-MM]` | Resume un mes de diario en tu perfil, tus personas y tu contexto |
| `/interview` | Crea o actualiza tu perfil y cómo quieres que trabaje la IA contigo |

## Personalízalo

- **Áreas y hubs:** para agregar o renombrar un área, crea su carpeta y su `hub_<área>.md` (desde `tpl_hub`), actualiza la tabla de carpetas de `00_system/vault_conventions.md` §1 y pon el hub en *Active* de `00_home.md`. Los sub-hubs aparecen cuando ~10 notas comparten un tema.
- **Tipos y estados:** edita las tablas de `vault_conventions.md` §5 — el validador lee de ahí los valores permitidos.
- **Tu idioma:** escribe el primer alias de cada nota y tus tareas en tu idioma (es lo que muestra el resumen); configura `BRIEF_LANG`; `/interview` llena la sección *Language* de `.claude/global/CLAUDE.md`. Los nombres de archivo, las claves YAML y los encabezados de sección (`## Now`, `## Next steps`) se quedan en inglés para que los scripts puedan apoyarse en ellos.
- **La línea de coautor en los commits de la IA:** `CO_AUTHOR` al inicio de `.claude/hooks/vault_hooks.py` (ponlo en `""` para quitarla).
- **Otros agentes de IA:** empiezan por `AGENTS.md`; si el tuyo solo lee su propio nombre de archivo (como `GEMINI.md`), cópialo con ese nombre.

## Una segunda computadora

1. Instala las herramientas e inicia sesión ([paso 0](#0-instala-las-herramientas-e-inicia-sesión-en-github)), y después `gh repo clone mi-segundo-cerebro "$HOME/second-brain"`.
2. Abre la carpeta en Obsidian → **Trust author and enable plugins** → instala y activa el plugin **Git** (sus ajustes vienen en el repo).
3. Instala Claude Code ([paso 4](#4-instala-claude-code)) y ejecuta el instalador ([paso 5](#5-ejecuta-el-instalador-una-vez-por-máquina)).

## Seguridad y privacidad

- **Mantén privado el repo de tu vault — siempre.** El historial de Git guarda cada versión de cada nota: hacer público el repo más adelante publica todo, incluso lo que borraste.
- **Lo que concede la instalación global.** Las sesiones de Claude Code abiertas en cualquier carpeta pueden leer y editar tu vault, y los scripts de hooks del vault corren al inicio y al final de cada sesión en esa máquina. Instálalo solo en tus propias computadoras; `install.py --uninstall` lo quita.
- **Tu remoto de Git es código de confianza.** Los hooks, los skills y el workflow vienen de tu repo y corren en tu computadora y en GitHub, así que quien pueda hacer push puede cambiar lo que se ejecuta. Mantenlo privado y no agregues colaboradores a quienes no les darías tu computadora. Cuando un pull cambia `.claude/`, `.github/` u `.obsidian/plugins/`, el hook de inicio se lo dice a Claude para que te avise; revísalo con `git log -p`. Los cambios de la propia IA ahí nunca se guardan en commit automáticamente.
- **El contenido que ingieres no es de confianza.** Las páginas web y las transcripciones pueden esconder instrucciones dirigidas a IAs (prompt injection). `/ingest` las trata como datos para resumir y te avisa cuando una página trae ese tipo de texto; aun así, revisa lo que escribe y nunca dejes que una IA ejecute comandos que sugiere una página.
- **Los secretos nunca van en las notas.** `.gitignore` bloquea los archivos comunes de llaves, credenciales y bases de contraseñas como segunda línea de defensa. Los ajustes de los plugins de Obsidian (`.obsidian/plugins/*/data.json`), donde los plugins guardan API keys, no se sincronizan — salvo los de Obsidian Git, que no tienen ninguna.
- **El resumen sale de tu vault.** Viaja por los servidores de Telegram (los chats con bots no tienen cifrado de extremo a extremo) y los logs de las ejecuciones quedan en la pestaña Actions de tu repo. Pon en él solo lo que pondrías en una notificación del celular, y deja desactivados los grupos para el bot (`/setjoingroups` → Disable).

## Desinstalar

```powershell
py "$HOME/second-brain/.claude/global/install.py" --uninstall
```

(`python3 …` en macOS/Linux.) Quita el bloque de `~/.claude/CLAUDE.md`, los hooks y el acceso a la carpeta del vault de `~/.claude/settings.json` (antes lo respalda) y los enlaces de los skills; tus demás ajustes y el propio vault quedan como estaban. Para quitarlo todo, borra después la carpeta del vault, y el repo de GitHub si ya no lo quieres.

## Solución de problemas

- **`Author identity unknown` / `Please tell me who you are`** — Git no tiene nombre ni correo: ejecuta las dos líneas `git config --global` del [paso 0](#0-instala-las-herramientas-e-inicia-sesión-en-github).
- **`git push` pide contraseña o falla con `Authentication failed`** — ejecuta `gh auth login` y `gh auth setup-git`.
- **`python` abre la Microsoft Store (Windows)** — usa `py`, o desactiva los alias de `python.exe` en *Configuración → Aplicaciones → Configuración avanzada de aplicaciones → Alias de ejecución de aplicaciones*.
- **Los hooks no corren en Windows** — Claude Code los ejecuta con Git Bash: instala Git for Windows y asegúrate de que `py` o `python` funcionen en una terminal nueva.
- **"git pull failed" justo después de abrir Obsidian** — Obsidian Git hizo pull al mismo tiempo; el hook reintenta una vez. Si sigue, ejecuta `git status` en el vault.
- **"Not auto-committed (code or app config…)"** — es lo esperado: los cambios en `.claude/`, `.github/` y `.obsidian/` te esperan a ti. Revísalos con `git diff` y haz el commit tú.
- **El validador se queja después de una edición** — el mensaje dice qué propiedad rompe qué regla de `vault_conventions.md`; Claude lo corrige en el momento.
- **Avisos en `{{title}}` o en las fechas dentro de las plantillas** — es normal: se convierten en valores reales al insertar la plantilla. Edita las plantillas en modo Fuente (*Source mode*).
- **Claude no te conoce en otras carpetas** — vuelve a ejecutar el instalador y reinicia Claude Code. Si la ruta del vault tiene espacios, muévelo a una sin espacios (el instalador avisa de esto).
- **Telegram: `Unauthorized`** — el token está mal o fue revocado: guárdalo de nuevo como `TELEGRAM_BOT_TOKEN`. **`chat not found`** — el chat id está mal, o nunca pulsaste **Start** en el chat de tu bot.
- **Telegram: la lista de chats sale vacía** — envía `/start` a tu bot (el `@usuario` correcto) y vuelve a ejecutarlo antes de 24 horas.
- **El commit del archivo falla con `403` / `Permission denied to github-actions[bot]`** — *Settings → Actions → General → Workflow permissions* → **Read and write permissions** (una organización puede bloquear este ajuste).
- **El resumen programado no llega** — revisa que `BRIEF_ENABLED` sea `true` y que el cambio del workflow esté en la rama principal; las tareas programadas pueden retrasarse en horas de mucha carga.

## Licencia

[MIT](LICENSE).
