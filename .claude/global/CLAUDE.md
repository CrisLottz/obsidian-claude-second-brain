# Global instructions — second brain

Loaded in every Claude Code session on this machine: `~/.claude/CLAUDE.md` (written by `install.py`) states where the vault lives and imports this file. Edit this file inside the vault, never in `~/.claude/`, so the change syncs to every machine.

## Who I am and the map of my life

@../../00_home.md

## The vault

- Its path is stated in `~/.claude/CLAUDE.md`, right above the import of this file. It is the source of truth about me: profile, work, projects, knowledge, life, media and personal notes.
- Navigate progressively: root note (above) → hub → note. Read frontmatter first (`summary`, `type`, `status`, `up`) and open full notes only when needed.
- Before writing anything in the vault, read its `CLAUDE.md` and `00_system/vault_conventions.md` and follow them (YAML, `author`, `up`, hub links, session log).
- For deep personal context, open `07_personal/profile.md` in the vault. It is long: read it only when the question needs it.
- Durable facts about me go into the vault, not into your internal memory.

## Working in a project folder outside the vault

- At session start a hook says whether this folder's git repos are linked to a vault project note (matched through the note's `repo` list).
- **Linked:** read that note before starting. The project's own `CLAUDE.md` and docs hold the code knowledge; the vault note holds goal, status, decisions and next steps. When the session ends with real progress, update the note's **Current state** and **Next steps** (set `author: mixed` if I wrote it, update `updated`) and add a line to the vault session log. Never copy code documentation into the vault; link to it.
- **Not linked:** when I ask you to connect the project to the vault:
  1. Read the folder's `CLAUDE.md` / README and the `origin` remote of each repo (`git remote get-url origin`).
  2. Search the vault for an existing note (file names, `aliases`, `repo`) — never duplicate.
  3. Create the note from `00_system/templates/tpl_project.md` in `03_projects/` (personal) or `02_work/` (work): `repo` = list of `owner/name`, short Goal, Current state, Next steps, where the docs live.
  4. Add it to its hub's **Active** section and, if active, to the root note's **Active** section; add a session-log line.

## Language

<!-- /interview fills this in. Example: "Talk to me in Spanish; keep proper names in their original language." -->
- Talk to me in the language I write in.

## Working with me

<!-- /interview fills this in with concrete, testable preferences: tone, depth, how to present options, when to ask vs. act. -->
- Be direct and explain the "why" behind recommendations.
- When there are real alternatives, compare them with pros and cons and give a recommendation.
