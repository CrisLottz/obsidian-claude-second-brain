"""Install the second-brain global Claude Code setup on this machine. Safe to re-run.

  ~/.claude/CLAUDE.md      gets a short marked block that imports .claude/global/CLAUDE.md
  ~/.claude/settings.json  gets the vault in permissions.additionalDirectories and the
                           vault hooks in global mode; every other setting is kept and
                           the previous file is backed up next to it when it changes
  ~/.claude/skills/<name>  links (junction on Windows, symlink elsewhere) to each vault
                           skill, so /inbox, /ingest… work in every project and always
                           match the vault's version

What this grants: Claude can read and edit the vault from any project, and the vault's hook
scripts run in every Claude Code session on this machine. Only install it for a vault whose
Git remote you control.

Run from any folder:  python <vault>/.claude/global/install.py   (python3 on macOS/Linux)
Re-run it after moving the vault. Undo everything with --uninstall.
"""
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

VAULT = Path(__file__).resolve().parents[2]
CLAUDE_DIR = Path.home() / ".claude"
HOOK_MARK = ".claude/hooks/run.sh"
BLOCK_START = "<!-- second-brain vault: added by install.py (re-run it after moving the vault; --uninstall removes it) -->"
BLOCK_END = "<!-- /second-brain vault -->"
BLOCK_RE = re.compile(re.escape(BLOCK_START) + r".*?" + re.escape(BLOCK_END) + r"\n?", re.S)
LEGACY_BLOCK_RE = re.compile(r"<!-- Added by the vault installer\.[^\n]*-->\n[^\n]*\n@[^\n]*\n?")
HOOKS = [  # event, matcher, hook command, timeout in seconds
    ("SessionStart", "startup|resume|clear|compact", "session-start", 45),
    ("PostToolUse", "Edit|MultiEdit|Write", "post-edit", 30),
    ("Stop", None, "stop", 90),
    ("UserPromptSubmit", None, "prompt", 10),
]


def home_relative(path):
    """~/... when the vault is under the home folder, else an absolute POSIX path."""
    try:
        return "~/" + path.relative_to(Path.home()).as_posix()
    except ValueError:
        return path.as_posix()


def hook_command(event):
    script = VAULT / ".claude" / "hooks" / "run.sh"
    try:
        location = '"$HOME"/' + shlex.quote(script.relative_to(Path.home()).as_posix())
    except ValueError:
        location = shlex.quote(script.as_posix())
    # Skip silently if the vault isn't on this machine; otherwise keep the exit code (2 = feedback to Claude)
    return f'f={location}; [ -f "$f" ] || exit 0; bash "$f" {event} --global'


def is_ours(hook):
    command = hook.get("command", "")
    return HOOK_MARK in command and "--global" in command


def write_atomic(path, text):
    """Write through a temporary file so an interrupted run never leaves a half-written file."""
    path = Path(os.path.realpath(path))  # keep a symlinked dotfile a symlink
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".install-tmp")
    tmp.write_text(text, encoding="utf-8", newline="\n")
    os.replace(tmp, path)


def save(path, new_text):
    """Write `new_text` if it differs; back up the previous version. Returns True when changed."""
    old_text = path.read_text(encoding="utf-8") if path.exists() else None
    if old_text == new_text:
        return False
    if old_text is not None:
        shutil.copy2(path, path.with_name(f"{path.name}.bak-{datetime.now():%Y%m%d-%H%M%S}"))
    write_atomic(path, new_text)
    return True


def load_settings(path):
    if not path.exists():
        return {}
    try:
        settings = json.loads(path.read_text(encoding="utf-8"))
    except ValueError as error:
        sys.exit(f"{path} is not valid JSON ({error}). Fix it first; nothing was changed.")
    if not isinstance(settings, dict):
        sys.exit(f"{path} does not contain a JSON object. Fix it first; nothing was changed.")
    return settings


def claude_md_text(current, install=True):
    text = LEGACY_BLOCK_RE.sub("", BLOCK_RE.sub("", current)).rstrip()
    if install:
        block = (f"{BLOCK_START}\n"
                 f"My second-brain vault (notes, rules, profile) is at `{VAULT.as_posix()}`.\n"
                 f"@{home_relative(VAULT / '.claude' / 'global' / 'CLAUDE.md')}\n"
                 f"{BLOCK_END}\n")
        return (text + "\n\n" if text else "") + block
    return text + "\n" if text else ""


def update_claude_md(install=True):
    target = CLAUDE_DIR / "CLAUDE.md"
    current = target.read_text(encoding="utf-8") if target.exists() else ""
    if not install and not target.exists():
        return f"{target}: nothing to remove"
    changed = save(target, claude_md_text(current, install))
    if install:
        return f"{target}: {'vault import written' if changed else 'already imports the vault instructions'}"
    return f"{target}: {'vault import removed' if changed else 'no vault import found'}"


def previous_vault():
    """The vault path recorded by an earlier run in ~/.claude/CLAUDE.md (it differs after a move)."""
    target = CLAUDE_DIR / "CLAUDE.md"
    block = BLOCK_RE.search(target.read_text(encoding="utf-8")) if target.exists() else None
    found = re.search(r"is at `([^`]+)`", block.group(0)) if block else None
    return str(Path(found.group(1))) if found else None


def settings_text(settings, install=True, previous=None):
    permissions = settings.setdefault("permissions", {})
    dirs = [d for d in permissions.get("additionalDirectories", []) if d not in (str(VAULT), previous)]
    if install:
        dirs.append(str(VAULT))
    if dirs:
        permissions["additionalDirectories"] = dirs
    else:
        permissions.pop("additionalDirectories", None)
    if not permissions:
        settings.pop("permissions")

    hooks = settings.setdefault("hooks", {})
    for event, matcher, command, timeout in HOOKS:
        groups = []
        for group in hooks.get(event, []):  # drop only our own hook entries, keep everything else
            kept = [h for h in group.get("hooks", []) if not is_ours(h)]
            if kept:
                groups.append({**group, "hooks": kept})
            elif not group.get("hooks"):
                groups.append(group)
        if install:
            group = {"hooks": [{"type": "command", "shell": "bash", "command": hook_command(command), "timeout": timeout}]}
            groups.append({"matcher": matcher, **group} if matcher else group)
        if groups:
            hooks[event] = groups
        else:
            hooks.pop(event, None)
    if not hooks:
        settings.pop("hooks")
    return json.dumps(settings, indent=2, ensure_ascii=False) + "\n"


def update_settings(settings, install=True, previous=None):
    target = CLAUDE_DIR / "settings.json"
    if not install and not target.exists():
        return f"{target}: nothing to remove"
    changed = save(target, settings_text(settings, install, previous))
    if install:
        return f"{target}: {'vault access and global hooks set (previous file backed up)' if changed else 'already set'}"
    return f"{target}: {'vault access and hooks removed (previous file backed up)' if changed else 'nothing to remove'}"


def is_link(path):
    """Symlink or Windows junction (never a real folder)."""
    if os.path.islink(path) or (hasattr(os.path, "isjunction") and os.path.isjunction(path)):
        return True
    real = os.path.realpath(path)
    return os.path.normcase(real) != os.path.normcase(os.path.join(os.path.realpath(path.parent), path.name))


def same_path(a, b):
    return os.path.normcase(os.path.realpath(a)) == os.path.normcase(os.path.realpath(b))


def vault_skill_link(path, name):
    """True when `path` is a link to `<some vault>/.claude/skills/<name>` (another copy or an old location)."""
    target = Path(os.path.realpath(path))
    return target.name == name and target.parent.as_posix().endswith(".claude/skills")


def remove_link(path):
    if os.name == "nt":
        os.rmdir(path)  # removes the junction or directory symlink itself, never the files it points to
    else:
        os.unlink(path)


def make_link(link, target):
    if os.name == "nt":  # a junction needs no admin rights or Developer Mode
        import _winapi
        _winapi.CreateJunction(str(target), str(link))
    else:
        link.symlink_to(target, target_is_directory=True)


def update_skills(install=True):
    source_root = VAULT / ".claude" / "skills"
    target_root = CLAUDE_DIR / "skills"
    results = []
    skills = sorted(p for p in source_root.iterdir() if (p / "SKILL.md").exists())
    if install:
        target_root.mkdir(parents=True, exist_ok=True)
    for skill in skills:
        link = target_root / skill.name
        exists = os.path.lexists(link)
        if not install:
            if exists and is_link(link) and same_path(link, skill):
                remove_link(link)
                results.append(f"/{skill.name}: unlinked")
            continue
        if exists and same_path(link, skill):
            results.append(f"/{skill.name}: already linked")
            continue
        if exists:
            dangling = not os.path.exists(link)
            if not is_link(link) or not (dangling or vault_skill_link(link, skill.name)):
                results.append(f"/{skill.name}: SKIPPED, a different skill with this name exists")
                continue
            remove_link(link)  # broken link or a link to this vault's old location: point it here
        make_link(link, skill)
        results.append(f"/{skill.name}: {'relinked' if exists else 'linked'}")
    return f"{target_root}: " + ("; ".join(results) or "no vault skill links found")


def checks():
    """Problems that would make the hooks fail later, reported now."""
    notes = []
    if re.search(r"\s", str(VAULT)):
        notes.append(f"NOTE: the vault path has spaces ({VAULT}); if the @import in ~/.claude/CLAUDE.md "
                     "doesn't load, move the vault to a path without spaces and re-run this installer.")
    try:
        email = subprocess.run(["git", "config", "--get", "user.email"], capture_output=True, text=True,
                               cwd=str(VAULT), timeout=10).stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        return notes + ["WARNING: git was not found on PATH. The vault hooks need it: install Git and re-run."]
    if not email:
        notes.append('WARNING: Git has no identity, so the auto-commits will fail. Run:\n'
                     '  git config --global user.name "Your Name"\n'
                     '  git config --global user.email "you@example.com"')
    return notes


def main(argv):
    if argv not in ([], ["--uninstall"]):
        sys.exit("usage: install.py [--uninstall]")
    install = not argv
    settings = load_settings(CLAUDE_DIR / "settings.json")  # fail before changing anything
    previous = previous_vault()
    print(update_claude_md(install))
    print(update_settings(settings, install, previous))
    print(update_skills(install))
    if install:
        for note in checks():
            print(note)
        print("Done. Restart Claude Code sessions to load the new global setup. Undo it with: install.py --uninstall")
    else:
        print("Done. The vault itself was not touched. Restart Claude Code sessions.")
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main(sys.argv[1:]))
