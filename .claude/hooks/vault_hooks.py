"""Claude Code hooks for the second-brain vault. Cross-platform, stdlib only.

  session-start  git pull, then print the latest log lines, inbox count and
                 today's date (SessionStart stdout is added to Claude's context);
                 records what was already staged, and warns when the pull changed
                 executable config (.claude/, .github/, .obsidian/plugins/)
  post-edit      remember the edited file for the next commit and validate its
                 frontmatter (exit 2 sends the problems back to Claude)
  stop           commit only the AI's own changes (files it edited, plus what it
                 staged with git mv / git rm during the session), using the latest
                 session log line as message, then push. Files under .claude/,
                 .github/ and .obsidian/ are never auto-committed: the user is asked
                 to review and commit them.
  prompt         optional (off by default): from the hour in VAULT_DAY_CLOSE_HOUR, until
                 today's `/day-close` is in the session log, ask Claude to remind the
                 user once (at most every 90 minutes, across all sessions) so tomorrow's
                 morning brief starts up to date

With --global (hooks installed in ~/.claude/settings.json) the same commands run
in sessions opened in any other folder: session-start reports which vault
project note matches the folder's git remotes instead of the log and inbox.
Inside the vault, --global does nothing: the vault's own hooks handle it.
"""
import json
import os
import re
import subprocess
import sys
import time
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate_frontmatter  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
STATE = ROOT / ".claude" / "state"
TOUCHED = STATE / "touched.txt"
BASELINE = STATE / "staged_at_start.txt"
CO_AUTHOR = "Claude <noreply@anthropic.com>"  # co-author trailer on AI commits; "" to disable
PROTECTED = (".claude/", ".github/", ".obsidian/")  # code and app config: reviewed by a human, never auto-committed
REMOTE_RE = re.compile(r"[:/]([^/:]+)/([^/]+?)(?:\.git)?/?$")
SCAN_SKIP = {"node_modules", "vendor", "venv", ".venv", "dist", "build", "__pycache__"}
GIT_ENV = {**os.environ, "GIT_TERMINAL_PROMPT": "0", "GCM_INTERACTIVE": "never"}  # never hang on a credential prompt
NET_TIMEOUT = 25


def git(*args, timeout=30, repo=None):
    """Run git in the vault (or `repo`) with literal pathspecs; cwd is the vault so no executable
    planted in an opened project folder can shadow git on Windows."""
    return subprocess.run(
        ["git", "--literal-pathspecs", "-c", "core.quotepath=off", "-C", str(repo or ROOT), *args],
        capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout,
        cwd=str(ROOT), env=GIT_ENV,
    )


def wait_for_index_lock(seconds=10):
    """Obsidian Git may be committing at the same moment."""
    lock = ROOT / ".git" / "index.lock"
    deadline = time.time() + seconds
    while lock.exists() and time.time() < deadline:
        time.sleep(0.5)


def read_stdin_json():
    try:
        return json.load(sys.stdin)
    except (ValueError, OSError):
        return {}


def read_lines(path):
    if not path.exists():
        return []
    return [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def to_vault_rel(file_path):
    """Vault-relative POSIX path, or None if the file is outside the vault (symlinks resolved)."""
    if os.name == "nt" and re.match(r"^/[a-zA-Z]/", file_path):
        file_path = f"{file_path[1]}:{file_path[2:]}"
    real = os.path.realpath(file_path)
    root = os.path.realpath(str(ROOT))
    if os.path.normcase(real) != os.path.normcase(root) and not os.path.normcase(real).startswith(
        os.path.normcase(root) + os.sep
    ):
        return None
    return Path(os.path.relpath(real, root)).as_posix()


def staged_paths():
    """Paths in the index, with renames split into old + new so both can be committed."""
    out = git("diff", "--cached", "--name-only", "--no-renames").stdout
    return [s for s in out.splitlines() if s.strip()]


def latest_log():
    logs = sorted((ROOT / "00_system").glob("claude_log_*.md"))
    return logs[-1] if logs else None


def project_dir():
    return os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()


def remote_slug(directory):
    """`owner/name` of a repo's origin remote, or None."""
    try:
        r = git("remote", "get-url", "origin", timeout=10, repo=directory)
    except (OSError, subprocess.TimeoutExpired):
        return None
    match = REMOTE_RE.search(r.stdout.strip()) if r.returncode == 0 else None
    return f"{match.group(1)}/{match.group(2)}" if match else None


def subdirs(directory):
    try:
        return sorted(p for p in Path(directory).iterdir()
                      if p.is_dir() and not p.name.startswith(".") and p.name not in SCAN_SKIP)
    except OSError:
        return []


def workspace_repos(directory):
    """The folder's own repo plus the repos up to two levels below it (a workspace repo can hold the
    code repos inside, like a workspace folder with several repos)."""
    own = remote_slug(directory)
    repos = [own] if own else []
    for child in subdirs(directory):
        for candidate in [child] + subdirs(child):
            if (candidate / ".git").exists():
                slug = remote_slug(candidate)
                if slug and slug not in repos:
                    repos.append(slug)
    return repos


def notes_for_repos(repos):
    """Vault notes whose `repo` property lists any of the repos."""
    wanted = {r.lower() for r in repos}
    matches = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in validate_frontmatter.SKIP_DIRS]
        for name in filenames:
            path = Path(dirpath) / name
            if not name.endswith(".md") or not validate_frontmatter.should_check(path):
                continue
            text = validate_frontmatter.read_note(path)
            if text is None or not any(w in text.lower() for w in wanted):
                continue
            data, _ = validate_frontmatter.parse_frontmatter(text)
            repo = (data or {}).get("repo") or []
            values = repo if isinstance(repo, list) else [repo]
            if any(v.strip().lower() in wanted for v in values):
                matches.append(path)
    return matches


def link_report(directory):
    repos = workspace_repos(directory)
    if not repos:
        return []
    notes = notes_for_repos(repos)
    if notes:
        listed = ", ".join(str(n) for n in notes)
        return [f"This workspace (repos: {', '.join(repos)}) is linked to the vault project note: {listed}. "
                "Read it before starting. When the session ends with real progress, update its Current state "
                f"and Next steps following the vault rules ({ROOT / 'CLAUDE.md'})."]
    return [f"This workspace's repos ({', '.join(repos)}) are not linked to any vault note. If the user works on it "
            "regularly, offer once to connect it to the vault."]


def pull_vault():
    """git pull --ff-only (one retry: Obsidian Git may pull at the same moment). Returns status lines."""
    out = []
    before = git("rev-parse", "HEAD").stdout.strip()
    try:
        pull = git("pull", "--ff-only", "--quiet", timeout=NET_TIMEOUT)
        if pull.returncode != 0:
            time.sleep(3)
            wait_for_index_lock()
            pull = git("pull", "--ff-only", "--quiet", timeout=10)
    except subprocess.TimeoutExpired:
        return ["WARNING: vault git pull timed out (offline?). Tell the user before editing vault notes."]
    if pull.returncode != 0:
        return ["WARNING: vault git pull failed. Tell the user before editing vault notes.\n" + pull.stderr.strip()]
    out.append(f"Second-brain vault ({ROOT}): git pull OK.")
    if before:
        changed = [s for s in git("diff", "--name-only", f"{before}..HEAD", "--",
                                  ".claude", ".github", ".obsidian/plugins").stdout.splitlines() if s.strip()]
        if changed:
            out.append("NOTE: the pull changed executable vault config, which the hooks now run: "
                       f"{', '.join(changed[:8])}. Tell the user so they can review it (`git log -p`).")
    return out


def session_start(global_mode=False):
    wait_for_index_lock()
    STATE.mkdir(parents=True, exist_ok=True)
    BASELINE.write_text("\n".join(staged_paths()) + "\n", encoding="utf-8")  # the user's own staging, left alone
    out = pull_vault()

    if global_mode:
        out += link_report(project_dir())
        out.append(f"Today: {date.today().isoformat()}")
        print("\n\n".join(out))
        return 0

    log = latest_log()
    if log:
        entries = [l for l in log.read_text(encoding="utf-8", errors="replace").splitlines() if l.startswith("- ")][-5:]
        if entries:
            out.append(f"Latest entries in {log.stem}:\n" + "\n".join(entries))
    inbox = [p for p in (ROOT / "01_inbox").glob("*.md")]
    if inbox:
        out.append(f"Inbox: {len(inbox)} unprocessed note(s). Suggest /inbox when it fits.")
    out.append(f"Today: {date.today().isoformat()}")
    print("\n\n".join(out))
    return 0


def post_edit():
    payload = read_stdin_json()
    file_path = (payload.get("tool_input") or {}).get("file_path") or (payload.get("tool_response") or {}).get(
        "filePath"
    )
    if not file_path:
        return 0
    rel = to_vault_rel(file_path)
    if rel is None:
        return 0

    STATE.mkdir(parents=True, exist_ok=True)
    if rel not in read_lines(TOUCHED):
        with TOUCHED.open("a", encoding="utf-8") as f:
            f.write(rel + "\n")

    path = ROOT / rel
    if path.exists() and validate_frontmatter.should_check(path):
        errors = validate_frontmatter.check(path)
        if errors:
            print(f"Frontmatter problems in {rel} (rules: 00_system/vault_conventions.md):", file=sys.stderr)
            for e in errors:
                print(f"  - {e}", file=sys.stderr)
            return 2
    return 0


def commit_message(paths):
    log = latest_log()
    if log and log.relative_to(ROOT).as_posix() in paths:
        entries = [l for l in log.read_text(encoding="utf-8", errors="replace").splitlines() if l.startswith("- ")]
        if entries:
            text = re.sub(r"^- \d{4}-\d{2}-\d{2} — ", "", entries[-1])
            text = re.sub(r" — (\[\[.*)$", "", text).strip()
            if text:
                return "claude: " + (text if len(text) <= 64 else text[:61] + "...")
    return f"claude: update {len(paths)} file(s)"


def push_vault():
    """push; if rejected, merge-pull and push again. Returns a warning or None."""
    try:
        if git("push", "-q", timeout=NET_TIMEOUT).returncode == 0:
            return None
        if git("pull", "--no-rebase", "--no-edit", "-q", timeout=NET_TIMEOUT).returncode != 0:
            git("merge", "--abort")
            return "Vault commit saved locally, but pull/merge failed; resolve it before the next sync."
        if git("push", "-q", timeout=NET_TIMEOUT).returncode != 0:
            return "Vault commit saved locally, but push failed."
    except subprocess.TimeoutExpired:
        return "Vault commit saved locally; push timed out (offline?). Obsidian Git will push it later."
    return None


def stop():
    read_stdin_json()
    touched = read_lines(TOUCHED)
    baseline = set(read_lines(BASELINE))
    wait_for_index_lock()
    for rel in touched:
        if not rel.startswith(PROTECTED):
            git("add", "-A", "--", rel)  # -A also stages deletions; untracked/ignored paths just fail quietly
    staged = staged_paths()
    ours = [s for s in staged if (s in touched or s not in baseline) and not s.startswith(PROTECTED)]
    held = sorted({r for r in touched if r.startswith(PROTECTED)}
                  | {s for s in staged if s.startswith(PROTECTED) and s not in baseline})
    warnings = []
    if held:
        warnings.append("Not auto-committed (code or app config — review and commit it yourself): " + ", ".join(held))
    if ours:
        body = "Files:\n" + "\n".join(f"- {s}" for s in ours)
        # You are the author (it counts on your GitHub contribution graph); the "claude:" prefix and
        # the optional co-author trailer mark the commit as the AI's. Set CO_AUTHOR = "" to drop it.
        message = ["-m", commit_message(ours), "-m", body] + (["-m", f"Co-Authored-By: {CO_AUTHOR}"] if CO_AUTHOR else [])
        commit = git("commit", "-q", "--only", *message, "--", *ours)
        if commit.returncode != 0:
            warnings.append("Vault auto-commit failed: " + commit.stderr.strip()[:300])
        else:
            warning = push_vault()
            if warning:
                warnings.append(warning)
    TOUCHED.unlink(missing_ok=True)
    if warnings:
        print(json.dumps({"systemMessage": " | ".join(warnings)}))
    return 0


DAY_CLOSE_EVERY = 90 * 60  # seconds between reminders while the review is still pending
LAST_REMINDER = STATE / "day_close_reminded.txt"


def day_close_hour():
    """Hour (0-23) from which the reminder starts, from VAULT_DAY_CLOSE_HOUR; None when unset or invalid (off)."""
    try:
        hour = int(os.environ.get("VAULT_DAY_CLOSE_HOUR", ""))
    except ValueError:
        return None
    return hour if 0 <= hour <= 23 else None


def day_close_done(today):
    """True when today's session log already has the `/day-close` line."""
    log = latest_log()
    if not log:
        return False
    marker = f"- {today.isoformat()} — Day close"
    return any(l.startswith(marker) for l in log.read_text(encoding="utf-8", errors="replace").splitlines())


def prompt():
    hour, now = day_close_hour(), datetime.now()
    if hour is None or now.hour < hour or day_close_done(now.date()):
        return 0
    try:
        if time.time() - float(LAST_REMINDER.read_text(encoding="utf-8")) < DAY_CLOSE_EVERY:
            return 0
    except (OSError, ValueError):
        pass  # never reminded, or an unreadable file: remind now
    STATE.mkdir(parents=True, exist_ok=True)
    LAST_REMINDER.write_text(str(time.time()), encoding="utf-8")
    context = (f"It is {now:%H:%M} and today's end-of-day review has not run yet. First answer the user's message "
               "as usual; then, in one short line at the end, in the language the user writes in, remind them and "
               "offer to run /day-close (it checks which open tasks are done so tomorrow's morning brief is up to "
               "date). Don't repeat it in later replies of this conversation unless they ask.")
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": context}}))
    return 0


COMMANDS = {"session-start": session_start, "post-edit": post_edit, "stop": stop, "prompt": prompt}

if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    args = sys.argv[1:]
    global_mode = "--global" in args
    args = [a for a in args if a != "--global"]
    if len(args) != 1 or args[0] not in COMMANDS:
        sys.exit(f"usage: vault_hooks.py {{{'|'.join(COMMANDS)}}} [--global]")
    if global_mode and to_vault_rel(project_dir()) is not None:
        sys.exit(0)  # session inside the vault: its project hooks already run
    if args[0] == "session-start":
        sys.exit(session_start(global_mode))
    sys.exit(COMMANDS[args[0]]())
