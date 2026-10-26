# Marketplace skill

`second-brain-setup/` is this template packaged as a single `SKILL.md` skill that guides an agent (Claude Code, Cursor, Codex, Copilot…) through creating and setting up the user's own vault from the template. It does not contain the hooks or the installer: it points to this repository and runs `gh repo create --template`, so the template stays the one source of truth.

It is not part of the vault: the validator, the brief and Obsidian ignore this folder.

## Build the zip

```
python marketplace/build_zip.py --version 1.1.0
```

Writes `marketplace/dist/second-brain-setup-1.1.0.zip` after checking the frontmatter, that there is at least one supporting file and that the privacy scan is clean.

## Release checklist

1. Keep `references/` in step with the README (setup, brief, troubleshooting) and with `00_system/vault_conventions.md`.
2. Run the zip builder and the privacy scan.
3. Test the skill in a scratch folder: `python marketplace/second-brain-setup/scripts/check_prereqs.py`, then follow `SKILL.md` end to end with a throw-away private repo.
4. Upload the zip and set the price or "free" in the marketplace's creator dashboard.
