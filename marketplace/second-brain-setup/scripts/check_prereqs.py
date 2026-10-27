"""Read-only check of what the second-brain template needs. Changes nothing, sends nothing.

Usage:  python check_prereqs.py        (python3 on macOS/Linux, py on Windows)
Exit code 1 when something required is missing.
"""
import shutil
import subprocess
import sys


def run(*cmd):
    try:
        done = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
    except (OSError, subprocess.TimeoutExpired):
        return None
    return done.stdout.strip() if done.returncode == 0 else None


def git_config(key):
    return run("git", "config", "--global", key)


def main():
    rows = []  # (ok, required, what, detail)

    py = sys.version_info
    rows.append((py >= (3, 8), True, "Python 3.8+", f"found {py.major}.{py.minor}.{py.micro}"))

    git = run("git", "--version")
    rows.append((bool(git), True, "Git", git or "not found: https://git-scm.com (on Windows, Git for Windows)"))
    if git:
        name, email = git_config("user.name"), git_config("user.email")
        rows.append((bool(name and email), True, "Git name and email",
                     "configured" if name and email else
                     'missing: git config --global user.name "Your Name" and git config --global user.email "you@example.com"'))

    gh = run("gh", "--version")
    rows.append((bool(gh), True, "GitHub CLI (gh)", gh.splitlines()[0] if gh else "not found: https://cli.github.com"))
    if gh:
        logged = run("gh", "auth", "status") is not None
        rows.append((logged, True, "gh logged in", "yes" if logged else "no: run `gh auth login` then `gh auth setup-git`"))

    claude = shutil.which("claude") and run("claude", "--version")
    rows.append((bool(claude), False, "Claude Code (optional for other agents)",
                 claude or "not found: https://claude.com/claude-code"))

    bad = 0
    for ok, required, what, detail in rows:
        mark = "OK  " if ok else ("MISS" if required else "skip")
        bad += (not ok) and required
        print(f"[{mark}] {what}: {detail}")
    print("\nObsidian 1.9+ cannot be detected from here: confirm it is installed (https://obsidian.md).")
    print("Everything required is present." if not bad else f"{bad} required item(s) missing.")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
