# Troubleshooting and extras

## Install links

- Git: https://git-scm.com (Windows: Git for Windows, which includes Git Bash; Claude Code uses it to run the hooks).
- GitHub CLI: https://cli.github.com, then `gh auth login` and `gh auth setup-git`.
- Python 3.8+: Windows launcher `py`, macOS/Linux `python3`. Nothing to `pip install` for the core.
- Obsidian 1.9+: https://obsidian.md. On Linux use the AppImage or `.deb`: Flatpak and Snap sandboxes can stop the Git plugin from running `git`.
- Claude Code: https://claude.com/claude-code (the user needs a paid Claude plan or a Console account with credits).

## Common problems

- **`Author identity unknown`** — set the Git identity: `git config --global user.name "Your Name"` and `git config --global user.email "you@example.com"`.
- **`git push` asks for a password or `Authentication failed`** — `gh auth login` and `gh auth setup-git`.
- **`python` opens the Microsoft Store (Windows)** — use `py`, or turn off the `python.exe` aliases in Settings → Apps → Advanced app settings → App execution aliases.
- **Hooks don't run on Windows** — Git for Windows must be installed and `py` or `python` must work in a new terminal.
- **The cloned folder is empty** — GitHub was still copying the template: delete the folder, wait, clone again.
- **"git pull failed" right after opening Obsidian** — Obsidian Git pulled at the same moment; the hook retries once. If it persists, run `git status` in the vault.
- **"Not auto-committed (code or app config…)"** — expected: changes in `.claude/`, `.github/` and `.obsidian/` wait for the user. Review with `git diff` and commit them.
- **The validator complains after an edit** — the message names the property and the rule in `vault_conventions.md`; the AI fixes it.
- **Claude doesn't know the user in other folders** — re-run `install.py` and restart Claude Code. If the vault path has spaces, move it to one without spaces.
- **Telegram `Unauthorized`** — wrong or revoked token: save it again as `TELEGRAM_BOT_TOKEN`. **`chat not found`** — wrong chat id, or **Start** was never pressed in the bot's chat.
- **The archive commit fails with `403`** — Settings → Actions → General → Workflow permissions → Read and write permissions.
- **The scheduled brief doesn't arrive** — check `BRIEF_ENABLED` is `true` and the workflow is on the default branch; scheduled runs can start late.

## Extras

- **YouTube for `/ingest`:** `py -m pip install --user youtube-transcript-api` (Windows) or `python3 -m pip install --user youtube-transcript-api`. If Linux answers `externally-managed-environment`, add `--break-system-packages`.
- **Obsidian Web Clipper:** Settings → General → Vaults: add the vault's name; Properties → Import: paste `.obsidian/types.json`; Templates → Import: `00_system/web_clipper_resource.json`, and drag it to the top so clips land in `01_inbox/` as `type: resource`.
- **`/day-close` reminders in Claude Code:** environment variable `VAULT_DAY_CLOSE_HOUR` (for example `20`) in `~/.claude/settings.json` under `"env"`.

## Undo

- `python3 <vault>/.claude/global/install.py --uninstall` removes the block in `~/.claude/CLAUDE.md`, the vault hooks and folder access in `~/.claude/settings.json` (backed up first) and the skill links. The vault itself stays.
- To remove everything, delete the vault folder, and the GitHub repo if it is no longer wanted.
