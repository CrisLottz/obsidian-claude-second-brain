# Obsidian + Claude Second Brain

**An AI-ready second brain for Obsidian.** Plain Markdown and Git, built for Claude Code, readable by any AI — with a morning brief on Telegram that costs zero tokens.

**English** · [Español](#español)

---

## Table of contents

- [What is this?](#what-is-this)
- [Works with any AI, built for Claude](#works-with-any-ai-built-for-claude)
- [Why it's different](#why-its-different)
- [What's inside](#whats-inside)
- [Requirements](#requirements)
- [Setup, step by step](#setup-step-by-step)
- [Telegram morning brief](#telegram-morning-brief)
- [Daily workflow](#daily-workflow)
- [Customize it](#customize-it)
- [A second machine](#a-second-machine)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## What is this?

A ready-to-use Obsidian vault that works as **one place for your whole life** — work, projects, knowledge, health, books and movies, money, diary, people — designed so an AI can find its way around it the way you do.

The AI never reads your whole vault. It reads a short **root note** (who you are and a map of your areas), then the **hub** of the area it needs, then only the notes that matter, choosing them by a one-line `summary` in each note's frontmatter. That's *progressive disclosure*: the AI knows you in ~1–2k tokens and opens the rest only on demand.

Everything is plain Markdown in a Git repository: your notes are yours, they sync across Windows, macOS and Linux, and every change an AI makes is committed, so it can always be reviewed and undone.

**Goal of this project:** give anyone a second brain that an AI can actually use — structured, validated, versioned and safe — in about 15 minutes, instead of the usual "point the AI at a messy folder and hope".

## Works with any AI, built for Claude

- **Any AI** can use the vault: the notes, hubs and conventions are plain Markdown and YAML. ChatGPT, Gemini, Codex, Cursor or a local model can read them. Copy `CLAUDE.md` as `AGENTS.md` (or `GEMINI.md`) for agents that look for those names.
- **Claude Code** gets the full experience: hooks that sync and validate, six slash-command skills, and a global setup so Claude knows you in *any* project folder.
- **The Telegram brief uses no AI at all**: a plain Python script reads your notes on GitHub Actions.

## Why it's different

What most people do: open an AI in their Obsidian folder and let it read and write whatever it finds. It works for a week, then context gets wasted, notes get messy and nobody knows what the AI changed.

| | Basic "Obsidian + AI" setup | This template |
|---|---|---|
| **Context** | The AI greps random notes or you paste context every time | A root map and hubs with one-line descriptions; each note has a `summary`. The AI knows where everything is in ~1–2k tokens |
| **Structure** | Folders invented on the fly | 7 areas, hubs, `up` links from every note to its hub, sub-hubs that appear only when a topic grows (~10 notes) |
| **Metadata** | Free-form, inconsistent | A YAML schema with closed lists of `type` and `status`, **enforced by a validator hook** on every AI edit |
| **Safety** | AI edits overwrite notes silently | Every AI note edit is **auto-committed and pushed** after each response, with the session log as message (changes to `.claude/`, `.github/` and `.obsidian/` are left for you to review). Review or revert anything |
| **Authorship** | Unknown who wrote what | `author: human \| ai \| mixed` in every note, plus a `claude:` prefix and co-author trailer on AI commits |
| **Memory between sessions** | Gone | A monthly session log; each session starts with the latest entries and the inbox count |
| **Outside the vault** | Only works inside the vault folder | A **global install**: in any code project Claude knows you, finds the project's note by its git remote, and keeps it updated |
| **Capture** | You file everything by hand | Notes land in an inbox; `/inbox` files them. Web Clipper template, `/ingest` for articles and YouTube videos |
| **Daily overview** | None | A **Telegram morning brief** — deadlines, overdue tasks, next steps, inbox — via GitHub Actions, PC off, zero tokens |
| **Dynamic queries** | Dataview tables the AI can't see in the raw file | Literal links in hubs; Obsidian **Bases** only for human views, reading the same YAML |
| **Multi-OS** | Windows quirks, broken line endings | LF everywhere, Python stdlib only, hooks through Git Bash, one installer per machine |

## What's inside

```
.
├── 00_home.md                 ← root note: your profile summary + map of the areas (loaded in every session)
├── CLAUDE.md                  ← rules for the AI inside the vault
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
│   ├── hooks/                 ← vault_hooks.py, validate_frontmatter.py (stdlib Python)
│   ├── skills/                ← /inbox /ingest /new-project /weekly-review /journal-close /interview
│   └── global/                ← CLAUDE.md for every session + install.py
└── .github/
    ├── workflows/morning_brief.yml
    └── scripts/morning_brief.py
```

## Requirements

- [Obsidian](https://obsidian.md) (free).
- [Git](https://git-scm.com) — on Windows, **Git for Windows**, which includes Git Bash (the hooks use it).
- A GitHub account and the [GitHub CLI](https://cli.github.com) (`gh`).
- Python 3.8+ (`python` on Windows, `python3` on macOS/Linux).
- [Claude Code](https://claude.com/claude-code) with a Claude plan or API key — or any other AI agent for the non-Claude parts.
- Optional: Telegram, for the morning brief.

## Setup, step by step

### 1. Create your own vault from this template

Click **Use this template → Create a new repository** at the top of this page and make it **private** — it will hold your personal notes. Or with the CLI:

```bash
gh repo create my-second-brain --private --template CrisLottz/obsidian-claude-second-brain
```

### 2. Clone it into your home folder

```bash
gh auth login              # once per machine (HTTPS is fine)
gh auth setup-git          # lets git use your gh login
git clone https://github.com/<your-user>/my-second-brain ~/second-brain
```

Use a path without spaces, and **never inside OneDrive, iCloud Drive or Dropbox**: Git is the only sync.

### 3. Open it in Obsidian

1. *Open folder as vault* → `~/second-brain`, and trust the vault when asked.
2. *Settings → Community plugins → Browse* → install and enable **Git** (by Vinzent03). Its settings are already in the vault: auto commit-and-sync 15 minutes after you stop editing, and pull on startup.

Links, the templates folder (`00_system/templates`), the attachments folder and property types are already configured.

### 4. Install Claude Code

```bash
# Windows (PowerShell)
irm https://claude.ai/install.ps1 | iex
# macOS / Linux
curl -fsSL https://claude.ai/install.sh | bash
```

Then run `claude` once and sign in.

### 5. Run the installer (once per machine)

```bash
python ~/second-brain/.claude/global/install.py      # python3 on macOS/Linux
```

It is safe to re-run. It:
- adds to `~/.claude/CLAUDE.md` the vault's path and an import of `.claude/global/CLAUDE.md`, so **every** Claude session knows you and your vault;
- gives every session file access to the vault and installs the vault hooks globally (your previous `~/.claude/settings.json` is backed up next to it);
- links the vault skills into `~/.claude/skills`, so `/inbox`, `/ingest`… work in any project.

### 6. First session

```bash
cd ~/second-brain
claude
```

The session starts with `git pull OK`. Then run **`/interview`**: Claude asks you seven short rounds of questions and writes your profile, the summary in `00_home.md`, your people and context, and your preferences for how it should work with you.

### 7. Optional extras

- **Telegram morning brief** — [setup below](#telegram-morning-brief).
- **YouTube for `/ingest`**: `python -m pip install --user youtube-transcript-api`.
- **Obsidian Web Clipper** (browser extension): set the vault name, then in *Properties → Import* paste `.obsidian/types.json`, and in *Templates → Import* drop `00_system/web_clipper_resource.json` and move it to the top of the list. Clips land in `01_inbox/`.

### Verify

- `python .claude/hooks/validate_frontmatter.py --all` → `0 with problems`.
- Ask Claude to create a test note: after its answer, `git log -1` shows a commit starting with `claude:`.
- Open Claude in any other folder and ask "what do you know about me?" — it answers from your root note.

## Telegram morning brief

Every morning a Telegram message with: deadlines in the next 7 days, overdue tasks, your to-do "Now" list, the next step of each active project, pending payments this month, inbox size and vault health. It runs on **GitHub Actions** (free for this use), so your computer can be off, and it uses **no AI and no tokens**: a Python script reads the YAML and tasks of your notes.

### Set it up (about 5 minutes)

1. **Create the bot.** In Telegram, open **@BotFather** → `/newbot` → give it a name and a username ending in `bot`. Copy the **token**.
2. **Say hi to your bot.** Open `t.me/<your_bot_username>` and press **Start**. Check the `@username` at the top of the chat: several bots can share the same display name.
3. **Save the token as a secret.** In your vault repo on GitHub: *Settings → Secrets and variables → Actions → New repository secret* → name `TELEGRAM_BOT_TOKEN`. Never paste it into a note or a chat; if it leaks, `/revoke` it in BotFather.
4. **Find your chat id.** *Actions → Morning brief → Run workflow*. Without `TELEGRAM_CHAT_ID` the run lists the private chats that wrote to the bot (id and name) in its log and stops without sending anything. Save **your** id as a second secret, `TELEGRAM_CHAT_ID`, and run it again.
5. **Configure it** in *Settings → Secrets and variables → Actions → Variables*:

| Variable | Example | What it does |
|---|---|---|
| `BRIEF_ENABLED` | `true` | **Turns the daily schedule on.** Off by default so a fresh copy doesn't fail every morning; manual runs always work |
| `BRIEF_LANG` | `en` or `es` | Language of the brief's labels |
| `BRIEF_TIMEZONE` | `America/Mexico_City` | Your time zone, for "today" and deadlines |
| `BRIEF_ARCHIVE` | `true` | Also save each brief in `00_system/briefs/` and commit it — one real commit per day, even with your PC off |
| `BRIEF_GIT_NAME` / `BRIEF_GIT_EMAIL` | your name / `ID+user@users.noreply.github.com` | Author of that commit. Default is the GitHub Actions bot; use your noreply email if you want the commit on your contribution graph |

6. **Pick the time.** Edit the `cron` line in `.github/workflows/morning_brief.yml`. Cron is always **UTC**: for 6:30 in UTC-6 use `30 12 * * *`; for 7:00 in UTC+1 use `0 6 * * *`. GitHub may start scheduled runs a few minutes late.

Optional: give the bot a picture with BotFather `/setuserpic` — **choose the bot first**, then send the image as a photo.

### How your notes feed it

- **Deadlines:** write the date as a standalone `YYYY-MM-DD` inside an open task — `- [ ] Pay rent 2026-11-05` — or in a note's `due` property. Dates inside file names are ignored.
- **Next steps:** the first open task under `## Next steps` of each project with `status: active`.
- **Names:** the brief shows each note's **first alias** — write it in the language you want to read (see [Customize](#customize-it)).

## Daily workflow

1. **Capture without thinking:** `Ctrl+N` in Obsidian (the note lands in `01_inbox/`), the Web Clipper for articles, or `/ingest <url>` for articles and YouTube videos.
2. **File it:** `/inbox` shows a plan (new name, type, folder, hub) and files everything after your OK.
3. **Work on code:** open `claude` inside a project. The first time, ask it to "connect this project to my vault": it creates the project note with the repo's `owner/name`, and from then on every session in that repo opens with it.
4. **Review:** `/weekly-review` on Fridays, `/journal-close` once a month.
5. **Every morning:** read the brief on your phone.

| Skill | What it does |
|---|---|
| `/inbox` | Files raw captures: renames, completes YAML, moves them and links them from their hub |
| `/ingest <url>` | Turns an article or YouTube video into a `resource` note with key points and links |
| `/new-project <name>` | Creates a project note wired to its hub, the root note and its GitHub repos |
| `/weekly-review` | Done, blocked, deadlines, money, vault health and proposed priorities |
| `/journal-close [YYYY-MM]` | Distills a month of diary into your profile, people and context |
| `/interview` | Builds or refreshes your profile and how the AI should work with you |

## Customize it

- **Areas and hubs:** rename or add areas in `vault_conventions.md` §1, then update `00_home.md`. Sub-hubs appear when ~10 notes share a topic.
- **Types and statuses:** edit the tables in `vault_conventions.md` §5 — the validator reads them from there.
- **Your language:** write each note's first alias and your tasks in your language (that's what the brief shows); set `BRIEF_LANG`; `/interview` fills the *Language* section of `.claude/global/CLAUDE.md`. File names, YAML keys and section headings stay in one language so scripts can rely on them.
- **The co-author line on AI commits:** `CO_AUTHOR` at the top of `.claude/hooks/vault_hooks.py` (set it to `""` to drop it).
- **Other AI agents:** copy `CLAUDE.md` as `AGENTS.md` / `GEMINI.md`.

## A second machine

```bash
gh auth login && gh auth setup-git
git clone https://github.com/<your-user>/my-second-brain ~/second-brain
# install Claude Code (step 4), then:
python ~/second-brain/.claude/global/install.py
```

Open the folder in Obsidian and install the Git plugin; everything else comes with the repo.

## Troubleshooting

- **Hooks don't run on Windows** — Claude Code runs hooks through Git Bash: install Git for Windows and make sure Python is on your `PATH`.
- **"git pull failed" right after opening Obsidian** — Obsidian Git pulled at the same moment; the hook retries once. If it persists, run `git status` in the vault.
- **Warnings on `{{title}}` or dates inside templates** — normal: they become real values when you insert the template. Edit templates in Source mode.
- **"TELEGRAM_CHAT_ID is not set and the bot has no recent messages"** — send `/start` to your bot (the right `@username`) and run the workflow again within 24 hours.
- **The validator complains after an edit** — the message says which field breaks which rule in `vault_conventions.md`; the AI fixes it on the spot.
- **Should my vault repo be private?** Yes. This template is public; your copy holds your life.

## License

[MIT](LICENSE).

---

# Español

**Un segundo cerebro para Obsidian listo para la IA.** Markdown y Git, pensado para Claude Code, legible por cualquier IA — con un resumen matutino en Telegram que no gasta ni un token.

[English](#obsidian--claude-second-brain) · **Español**

## Índice

- [¿Qué es esto?](#qué-es-esto)
- [Funciona con cualquier IA, pensado para Claude](#funciona-con-cualquier-ia-pensado-para-claude)
- [En qué se diferencia](#en-qué-se-diferencia)
- [Qué incluye](#qué-incluye)
- [Requisitos](#requisitos)
- [Configuración paso a paso](#configuración-paso-a-paso)
- [Resumen matutino en Telegram](#resumen-matutino-en-telegram)
- [Flujo diario](#flujo-diario)
- [Personalízalo](#personalízalo)
- [Una segunda computadora](#una-segunda-computadora)
- [Solución de problemas](#solución-de-problemas)
- [Licencia](#licencia)

## ¿Qué es esto?

Un vault de Obsidian listo para usar que funciona como **un solo lugar para toda tu vida** — trabajo, proyectos, conocimiento, salud, libros y películas, dinero, diario, personas — diseñado para que una IA se oriente en él igual que tú.

La IA nunca lee todo tu vault. Lee una **nota raíz** corta (quién eres y un mapa de tus áreas), luego el **hub** del área que necesita y después solo las notas que importan, eligiéndolas por el `summary` de una línea que tiene la ficha de cada nota. Eso es *divulgación progresiva*: la IA te conoce con ~1–2 mil tokens y abre lo demás solo cuando hace falta.

Todo es Markdown en un repositorio Git: tus notas son tuyas, se sincronizan entre Windows, macOS y Linux, y cada cambio que hace una IA queda en un commit, así que siempre se puede revisar y deshacer.

**Objetivo del proyecto:** que cualquiera tenga en unos 15 minutos un segundo cerebro que una IA pueda usar de verdad — estructurado, validado, versionado y seguro — en vez del típico "apuntar la IA a una carpeta desordenada y cruzar los dedos".

## Funciona con cualquier IA, pensado para Claude

- **Cualquier IA** puede usar el vault: las notas, los hubs y las convenciones son Markdown y YAML. ChatGPT, Gemini, Codex, Cursor o un modelo local pueden leerlos. Copia `CLAUDE.md` como `AGENTS.md` (o `GEMINI.md`) para los agentes que buscan esos nombres.
- **Claude Code** tiene la experiencia completa: hooks que sincronizan y validan, seis skills como comandos, y una configuración global para que Claude te conozca en *cualquier* carpeta de proyecto.
- **El resumen de Telegram no usa IA**: un script de Python lee tus notas en GitHub Actions.

## En qué se diferencia

Lo que hace la mayoría: abrir una IA en su carpeta de Obsidian y dejar que lea y escriba lo que encuentre. Funciona una semana; después se desperdicia contexto, las notas se desordenan y nadie sabe qué cambió la IA.

| | Configuración básica "Obsidian + IA" | Esta plantilla |
|---|---|---|
| **Contexto** | La IA busca notas al azar o tú pegas contexto cada vez | Un mapa raíz y hubs con descripciones de una línea; cada nota tiene `summary`. La IA sabe dónde está todo con ~1–2 mil tokens |
| **Estructura** | Carpetas inventadas sobre la marcha | 7 áreas, hubs, enlaces `up` de cada nota a su hub, sub-hubs que aparecen solo cuando un tema crece (~10 notas) |
| **Metadatos** | Libres e inconsistentes | Un esquema YAML con listas cerradas de `type` y `status`, **vigiladas por un hook validador** en cada edición de la IA |
| **Seguridad** | La IA sobrescribe notas sin avisar | Cada edición de notas de la IA se **guarda en un commit y se sube** al terminar cada respuesta, con la bitácora como mensaje (los cambios en `.claude/`, `.github/` y `.obsidian/` quedan para que tú los revises). Revisa o deshaz lo que sea |
| **Autoría** | No se sabe quién escribió qué | `author: human \| ai \| mixed` en cada nota, más el prefijo `claude:` y la línea de coautor en los commits de la IA |
| **Memoria entre sesiones** | Se pierde | Una bitácora mensual; cada sesión empieza mostrando las últimas entradas y cuántas notas hay en el inbox |
| **Fuera del vault** | Solo funciona dentro de la carpeta del vault | Una **instalación global**: en cualquier proyecto de código Claude te conoce, encuentra la nota del proyecto por su repo de git y la mantiene al día |
| **Captura** | Archivas todo a mano | Las notas caen en un inbox; `/inbox` las archiva. Plantilla para Web Clipper y `/ingest` para artículos y videos de YouTube |
| **Resumen diario** | Ninguno | Un **resumen matutino en Telegram** — plazos, tareas vencidas, siguientes pasos, inbox — con GitHub Actions, PC apagada y cero tokens |
| **Consultas dinámicas** | Tablas de Dataview que la IA no ve en el archivo | Enlaces escritos en los hubs; **Bases** de Obsidian solo para vistas humanas, leyendo la misma ficha YAML |
| **Varios sistemas** | Rarezas de Windows, saltos de línea rotos | LF en todo, Python sin dependencias, hooks por Git Bash, un instalador por máquina |

## Qué incluye

```
.
├── 00_home.md                 ← nota raíz: resumen de tu perfil + mapa de las áreas (se carga en cada sesión)
├── CLAUDE.md                  ← reglas para la IA dentro del vault
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
│   ├── hooks/                 ← vault_hooks.py, validate_frontmatter.py (Python sin dependencias)
│   ├── skills/                ← /inbox /ingest /new-project /weekly-review /journal-close /interview
│   └── global/                ← CLAUDE.md para todas las sesiones + install.py
└── .github/
    ├── workflows/morning_brief.yml
    └── scripts/morning_brief.py
```

## Requisitos

- [Obsidian](https://obsidian.md) (gratis).
- [Git](https://git-scm.com) — en Windows, **Git for Windows**, que incluye Git Bash (lo usan los hooks).
- Una cuenta de GitHub y el [GitHub CLI](https://cli.github.com) (`gh`).
- Python 3.8+ (`python` en Windows, `python3` en macOS/Linux).
- [Claude Code](https://claude.com/claude-code) con un plan de Claude o una API key — u otro agente de IA para lo que no es de Claude.
- Opcional: Telegram, para el resumen matutino.

## Configuración paso a paso

### 1. Crea tu propio vault desde esta plantilla

Haz clic en **Use this template → Create a new repository** arriba en esta página y créalo **privado** — va a tener tus notas personales. O con la terminal:

```bash
gh repo create mi-segundo-cerebro --private --template CrisLottz/obsidian-claude-second-brain
```

### 2. Clónalo en tu carpeta de usuario

```bash
gh auth login              # una vez por máquina (HTTPS está bien)
gh auth setup-git          # para que git use tu sesión de gh
git clone https://github.com/<tu-usuario>/mi-segundo-cerebro ~/second-brain
```

Usa una ruta sin espacios y **nunca dentro de OneDrive, iCloud Drive o Dropbox**: Git es la única sincronización.

### 3. Ábrelo en Obsidian

1. *Open folder as vault* → `~/second-brain`, y confía en el vault cuando lo pregunte.
2. *Settings → Community plugins → Browse* → instala y activa **Git** (de Vinzent03). Sus ajustes ya vienen en el vault: guarda y sincroniza 15 minutos después de que dejas de escribir, y trae cambios al abrir Obsidian.

Los enlaces, la carpeta de plantillas (`00_system/templates`), la de adjuntos y los tipos de propiedades ya están configurados.

### 4. Instala Claude Code

```bash
# Windows (PowerShell)
irm https://claude.ai/install.ps1 | iex
# macOS / Linux
curl -fsSL https://claude.ai/install.sh | bash
```

Luego ejecuta `claude` una vez e inicia sesión.

### 5. Ejecuta el instalador (una vez por máquina)

```bash
python ~/second-brain/.claude/global/install.py      # python3 en macOS/Linux
```

Puedes ejecutarlo varias veces sin problema. Hace esto:
- agrega a `~/.claude/CLAUDE.md` la ruta del vault y un import de `.claude/global/CLAUDE.md`, para que **todas** las sesiones de Claude te conozcan a ti y a tu vault;
- da a todas las sesiones acceso al vault e instala sus hooks de forma global (respalda tu `~/.claude/settings.json` anterior junto al archivo);
- enlaza los skills del vault en `~/.claude/skills`, para que `/inbox`, `/ingest`… funcionen en cualquier proyecto.

### 6. Primera sesión

```bash
cd ~/second-brain
claude
```

La sesión empieza con `git pull OK`. Después ejecuta **`/interview`**: Claude te hace siete rondas cortas de preguntas y escribe tu perfil, el resumen de `00_home.md`, tus personas y contexto, y tus preferencias sobre cómo quieres que trabaje contigo.

### 7. Extras opcionales

- **Resumen matutino en Telegram** — [configuración abajo](#resumen-matutino-en-telegram).
- **YouTube para `/ingest`**: `python -m pip install --user youtube-transcript-api`.
- **Obsidian Web Clipper** (extensión del navegador): pon el nombre del vault; en *Properties → Import* pega `.obsidian/types.json`; en *Templates → Import* arrastra `00_system/web_clipper_resource.json` y súbela al primer lugar de la lista. Los recortes caen en `01_inbox/`.

### Verifica

- `python .claude/hooks/validate_frontmatter.py --all` → `0 with problems`.
- Pídele a Claude que cree una nota de prueba: después de su respuesta, `git log -1` muestra un commit que empieza con `claude:`.
- Abre Claude en cualquier otra carpeta y pregúntale "¿qué sabes de mí?" — responde con tu nota raíz.

## Resumen matutino en Telegram

Cada mañana un mensaje de Telegram con: plazos de los próximos 7 días, tareas vencidas, tu lista "Now" de pendientes, el siguiente paso de cada proyecto activo, pagos pendientes del mes, el tamaño del inbox y la salud del vault. Corre en **GitHub Actions** (gratis para este uso), así que tu computadora puede estar apagada, y **no usa IA ni tokens**: un script de Python lee la ficha YAML y las tareas de tus notas.

### Configúralo (unos 5 minutos)

1. **Crea el bot.** En Telegram abre **@BotFather** → `/newbot` → ponle un nombre y un usuario que termine en `bot`. Copia el **token**.
2. **Salúdalo.** Abre `t.me/<usuario_de_tu_bot>` y pulsa **Start**. Revisa el `@usuario` arriba del chat: varios bots pueden tener el mismo nombre visible.
3. **Guarda el token como secreto.** En el repo de tu vault en GitHub: *Settings → Secrets and variables → Actions → New repository secret* → nombre `TELEGRAM_BOT_TOKEN`. Nunca lo pegues en una nota ni en un chat; si se filtra, revócalo con `/revoke` en BotFather.
4. **Encuentra tu chat id.** *Actions → Morning brief → Run workflow*. Sin `TELEGRAM_CHAT_ID`, la ejecución lista en su log los chats privados que le escribieron al bot (id y nombre) y se detiene sin enviar nada. Guarda **tu** id como segundo secreto, `TELEGRAM_CHAT_ID`, y vuelve a ejecutarlo.
5. **Configúralo** en *Settings → Secrets and variables → Actions → Variables*:

| Variable | Ejemplo | Qué hace |
|---|---|---|
| `BRIEF_ENABLED` | `true` | **Activa el horario diario.** Viene apagado para que una copia nueva no falle cada mañana; las ejecuciones manuales siempre funcionan |
| `BRIEF_LANG` | `en` o `es` | Idioma de las etiquetas del resumen |
| `BRIEF_TIMEZONE` | `America/Mexico_City` | Tu zona horaria, para "hoy" y los plazos |
| `BRIEF_ARCHIVE` | `true` | Guarda cada resumen en `00_system/briefs/` y hace commit — un commit real por día, aunque tu PC esté apagada |
| `BRIEF_GIT_NAME` / `BRIEF_GIT_EMAIL` | tu nombre / `ID+usuario@users.noreply.github.com` | Autor de ese commit. Por defecto es el bot de GitHub Actions; usa tu correo noreply si quieres que el commit cuente en tu gráfica de contribuciones |

6. **Elige la hora.** Edita la línea `cron` de `.github/workflows/morning_brief.yml`. El cron siempre está en **UTC**: para las 6:30 en UTC-6 usa `30 12 * * *`; para las 7:00 en UTC+1 usa `0 6 * * *`. GitHub puede iniciar las tareas programadas con unos minutos de retraso.

Opcional: ponle foto al bot con `/setuserpic` en BotFather — **elige primero el bot** y después envía la imagen como foto.

### Cómo lo alimentan tus notas

- **Plazos:** escribe la fecha suelta en formato `AAAA-MM-DD` dentro de una tarea abierta — `- [ ] Pagar el alquiler 2026-11-05` — o en la propiedad `due` de una nota. Las fechas dentro de nombres de archivo se ignoran.
- **Siguientes pasos:** la primera tarea abierta bajo `## Next steps` de cada proyecto con `status: active`.
- **Nombres:** el resumen muestra el **primer alias** de cada nota — escríbelo en el idioma que quieras leer (ver [Personalízalo](#personalízalo)).

## Flujo diario

1. **Captura sin pensar:** `Ctrl+N` en Obsidian (la nota cae en `01_inbox/`), el Web Clipper para artículos, o `/ingest <url>` para artículos y videos de YouTube.
2. **Archívalo:** `/inbox` te muestra un plan (nombre nuevo, tipo, carpeta, hub) y archiva todo con tu OK.
3. **Trabaja en código:** abre `claude` dentro de un proyecto. La primera vez pídele que "conecte este proyecto con mi vault": crea la nota del proyecto con el `owner/name` del repo, y desde entonces cada sesión en ese repo arranca con ella.
4. **Revisa:** `/weekly-review` los viernes y `/journal-close` una vez al mes.
5. **Cada mañana:** lee el resumen en tu celular.

| Skill | Qué hace |
|---|---|
| `/inbox` | Archiva las capturas: renombra, completa la ficha, mueve y enlaza desde su hub |
| `/ingest <url>` | Convierte un artículo o video de YouTube en una nota `resource` con puntos clave y enlaces |
| `/new-project <nombre>` | Crea una nota de proyecto conectada a su hub, a la nota raíz y a sus repos de GitHub |
| `/weekly-review` | Hecho, bloqueado, plazos, dinero, salud del vault y prioridades propuestas |
| `/journal-close [AAAA-MM]` | Resume un mes de diario en tu perfil, tus personas y tu contexto |
| `/interview` | Crea o actualiza tu perfil y cómo quieres que trabaje la IA contigo |

## Personalízalo

- **Áreas y hubs:** renombra o agrega áreas en `vault_conventions.md` §1 y actualiza `00_home.md`. Los sub-hubs aparecen cuando ~10 notas comparten un tema.
- **Tipos y estados:** edita las tablas de `vault_conventions.md` §5 — el validador las lee de ahí.
- **Tu idioma:** escribe el primer alias de cada nota y tus tareas en tu idioma (es lo que muestra el resumen); configura `BRIEF_LANG`; `/interview` llena la sección *Language* de `.claude/global/CLAUDE.md`. Los nombres de archivo, las claves YAML y los encabezados se quedan en un solo idioma para que los scripts puedan apoyarse en ellos.
- **La línea de coautor en los commits de la IA:** `CO_AUTHOR` al inicio de `.claude/hooks/vault_hooks.py` (ponlo en `""` para quitarla).
- **Otros agentes de IA:** copia `CLAUDE.md` como `AGENTS.md` / `GEMINI.md`.

## Una segunda computadora

```bash
gh auth login && gh auth setup-git
git clone https://github.com/<tu-usuario>/mi-segundo-cerebro ~/second-brain
# instala Claude Code (paso 4) y después:
python ~/second-brain/.claude/global/install.py
```

Abre la carpeta en Obsidian e instala el plugin Git; todo lo demás viene en el repo.

## Solución de problemas

- **Los hooks no corren en Windows** — Claude Code ejecuta los hooks con Git Bash: instala Git for Windows y asegúrate de que Python esté en tu `PATH`.
- **"git pull failed" justo después de abrir Obsidian** — Obsidian Git hizo pull al mismo tiempo; el hook reintenta una vez. Si sigue, ejecuta `git status` en el vault.
- **Avisos en `{{title}}` o en las fechas dentro de las plantillas** — es normal: se convierten en valores reales al insertar la plantilla. Edita las plantillas en modo Source.
- **"TELEGRAM_CHAT_ID is not set and the bot has no recent messages"** — envía `/start` a tu bot (el `@usuario` correcto) y vuelve a ejecutar el workflow en menos de 24 horas.
- **El validador se queja después de una edición** — el mensaje dice qué campo rompe qué regla de `vault_conventions.md`; la IA lo corrige en el momento.
- **¿El repo de mi vault debe ser privado?** Sí. Esta plantilla es pública; tu copia guarda tu vida.

## Licencia

[MIT](LICENSE).
