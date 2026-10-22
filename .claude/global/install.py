"""Install the second-brain global Claude Code setup on this machine. Safe to re-run.

  ~/.claude/CLAUDE.md      gets one import line pointing to .claude/global/CLAUDE.md
  ~/.claude/settings.json  gets the vault in permissions.additionalDirectories and the
                           vault hooks in global mode; every other setting is kept and
                           the previous file is backed up next to it
  ~/.claude/skills/<name>  links (junction on Windows, symlink elsewhere) to each vault
                           skill, so /inbox, /ingest… work in every project and always
                           match the vault's version

Run from any folder:  python <vault>/.claude/global/install.py   (python3 on macOS/Linux)
"""
import json
import os
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

VAULT = Path(__file__).resolve().parents[2]
CLAUDE_DIR = Path.home() / ".claude"
HOOK_MARK = ".claude/hooks/run.sh"


def home_relative(path):
    """~/... when the vault is under the home folder, else an absolute POSIX path."""
    try:
        return "~/" + path.relative_to(Path.home()).as_posix()
    except ValueError:
        return path.as_posix()


def hook_command(event):
    script = home_relative(VAULT / ".claude" / "hooks" / "run.sh").replace("~", "$HOME", 1)
    # Skip silently if the vault isn't on this machine; otherwise keep the exit code (2 = feedback to Claude)
    return f'f="{script}"; [ -f "$f" ] || exit 0; bash "$f" {event} --global'


def install_claude_md():
    target = CLAUDE_DIR / "CLAUDE.md"
    line = "@" + home_relative(VAULT / ".claude" / "global" / "CLAUDE.md")
    current = target.read_text(encoding="utf-8") if target.exists() else ""
    if line in current:
        return f"{target}: already imports the vault instructions"
    block = (f"<!-- Added by the vault installer. The second-brain vault lives at {VAULT.as_posix()} -->\n"
             f"My second-brain vault (notes, rules, profile) is at `{VAULT.as_posix()}`.\n{line}\n")
    CLAUDE_DIR.mkdir(parents=True, exist_ok=True)  # fresh machine: Claude Code not run yet
    target.write_text((current.rstrip() + "\n\n" if current.strip() else "") + block, encoding="utf-8", newline="\n")
    return f"{target}: import added"


def install_settings():
    target = CLAUDE_DIR / "settings.json"
    settings = json.loads(target.read_text(encoding="utf-8")) if target.exists() else {}
    if target.exists():
        backup = target.with_name(f"settings.json.bak-{datetime.now():%Y%m%d-%H%M%S}")
        shutil.copy2(target, backup)

    dirs = settings.setdefault("permissions", {}).setdefault("additionalDirectories", [])
    if str(VAULT) not in dirs:
        dirs.append(str(VAULT))

    hooks = settings.setdefault("hooks", {})
    for event, matcher, command, timeout in [
        ("SessionStart", "startup|resume|clear|compact", "session-start", 45),
        ("PostToolUse", "Edit|MultiEdit|Write", "post-edit", 30),
        ("Stop", None, "stop", 120),
    ]:
        groups = [g for g in hooks.get(event, [])
                  if not any(HOOK_MARK in h.get("command", "") and "--global" in h.get("command", "")
                             for h in g.get("hooks", []))]
        group = {"hooks": [{"type": "command", "shell": "bash", "command": hook_command(command), "timeout": timeout}]}
        if matcher:
            group = {"matcher": matcher, **group}
        hooks[event] = groups + [group]

    CLAUDE_DIR.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(settings, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    return f"{target}: vault access and global hooks set (backup kept)"


def install_skills():
    source_root = VAULT / ".claude" / "skills"
    target_root = CLAUDE_DIR / "skills"
    target_root.mkdir(parents=True, exist_ok=True)
    results = []
    for skill in sorted(p for p in source_root.iterdir() if (p / "SKILL.md").exists()):
        link = target_root / skill.name
        if os.path.lexists(link):
            same = os.path.realpath(link) == os.path.realpath(skill)
            results.append(f"/{skill.name}: {'already linked' if same else 'SKIPPED, a different skill with this name exists'}")
            continue
        if os.name == "nt":  # a junction needs no admin rights or Developer Mode
            subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(skill)], check=True, capture_output=True)
        else:
            link.symlink_to(skill, target_is_directory=True)
        results.append(f"/{skill.name}: linked")
    return f"{target_root}: " + "; ".join(results)


if __name__ == "__main__":
    print(install_claude_md())
    print(install_settings())
    print(install_skills())
    print("Done. Restart Claude Code sessions to load the new global setup.")
