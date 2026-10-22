"""Claude Code hooks for the second-brain vault. Cross-platform, stdlib only.

  session-start  git pull, then print the latest log lines, inbox count and
                 today's date (SessionStart stdout is added to Claude's context)
  post-edit      remember the edited file for the next commit and validate its
                 frontmatter (exit 2 sends the problems back to Claude)
  stop           commit only the files Claude touched, using the latest session
                 log line as message, then push

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
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate_frontmatter  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
STATE = ROOT / ".claude" / "state"
TOUCHED = STATE / "touched.txt"
CO_AUTHOR = "Claude <noreply@anthropic.com>"  # co-author trailer on AI commits; "" to disable
REMOTE_RE = re.compile(r"[:/]([^/:]+)/([^/]+?)(?:\.git)?/?$")
SCAN_SKIP = {"node_modules", "vendor", "venv", ".venv", "dist", "build", "__pycache__"}


def git(*args, timeout=30):
    return subprocess.run(
        ["git", "-c", "core.quotepath=off", "-C", str(ROOT), *args],
        capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout,
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


def to_vault_rel(file_path):
    """Vault-relative POSIX path, or None if the file is outside the vault."""
    if os.name == "nt" and re.match(r"^/[a-zA-Z]/", file_path):
        file_path = f"{file_path[1]}:{file_path[2:]}"
    abs_path = os.path.abspath(file_path)
    root = str(ROOT)
    if os.path.normcase(abs_path) != os.path.normcase(root) and not os.path.normcase(abs_path).startswith(
        os.path.normcase(root) + os.sep
    ):
        return None
    return Path(os.path.relpath(abs_path, root)).as_posix()


def read_touched():
    if not TOUCHED.exists():
        return []
    return [line for line in TOUCHED.read_text(encoding="utf-8").splitlines() if line.strip()]


def latest_log():
    logs = sorted((ROOT / "00_system").glob("claude_log_*.md"))
    return logs[-1] if logs else None


def project_dir():
    return os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()


def remote_slug(directory):
    """`owner/name` of a repo's origin remote, or None."""
    try:
        r = subprocess.run(["git", "-C", str(directory), "remote", "get-url", "origin"],
                           capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=10)
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
            text = path.read_text(encoding="utf-8", errors="replace")
            if not any(w in text.lower() for w in wanted):
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


def session_start(global_mode=False):
    out = []
    wait_for_index_lock()
    try:
        pull = git("pull", "--ff-only", "--quiet", timeout=30)
        if pull.returncode != 0:
            # Obsidian Git pulls on startup too; two fetches at once can leave FETCH_HEAD ambiguous
            time.sleep(3)
            wait_for_index_lock()
            pull = git("pull", "--ff-only", "--quiet", timeout=30)
        if pull.returncode == 0:
            out.append(f"Second-brain vault ({ROOT}): git pull OK.")
        else:
            out.append("WARNING: vault git pull failed. Tell the user before editing vault notes.\n" + pull.stderr.strip())
    except subprocess.TimeoutExpired:
        out.append("WARNING: vault git pull timed out (offline?). Tell the user before editing vault notes.")

    if global_mode:
        out += link_report(project_dir())
        out.append(f"Today: {date.today().isoformat()}")
        print("\n\n".join(out))
        return 0

    log = latest_log()
    if log:
        entries = [l for l in log.read_text(encoding="utf-8").splitlines() if l.startswith("- ")][-5:]
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
    if rel not in read_touched():
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


def commit_message(staged):
    log = latest_log()
    if log and log.relative_to(ROOT).as_posix() in staged:
        entries = [l for l in log.read_text(encoding="utf-8").splitlines() if l.startswith("- ")]
        if entries:
            text = re.sub(r"^- \d{4}-\d{2}-\d{2} — ", "", entries[-1])
            text = re.sub(r" — (\[\[.*)$", "", text).strip()
            if text:
                return "claude: " + (text if len(text) <= 64 else text[:61] + "...")
    return f"claude: update {len(staged)} file(s)"


def stop():
    read_stdin_json()
    touched = read_touched()
    wait_for_index_lock()
    for rel in touched:
        git("add", "-A", "--", rel)  # -A also stages deletions; untracked/ignored paths just fail quietly
    staged = [s for s in git("diff", "--cached", "--name-only").stdout.splitlines() if s.strip()]
    if not staged:
        TOUCHED.unlink(missing_ok=True)
        return 0

    body = "Files:\n" + "\n".join(f"- {s}" for s in staged)
    # You are the author (it counts on your GitHub contribution graph); the "claude:" prefix and
    # the optional co-author trailer mark the commit as the AI's. Set CO_AUTHOR = "" to drop it.
    message = ["-m", commit_message(staged), "-m", body] + (["-m", f"Co-Authored-By: {CO_AUTHOR}"] if CO_AUTHOR else [])
    commit = git("commit", "-q", *message)
    if commit.returncode != 0:
        print(json.dumps({"systemMessage": "Vault auto-commit failed: " + commit.stderr.strip()[:300]}))
        return 0
    TOUCHED.unlink(missing_ok=True)

    warning = None
    try:
        push = git("push", "-q", timeout=45)
        if push.returncode != 0:
            pull = git("pull", "--no-rebase", "--no-edit", "-q", timeout=45)
            if pull.returncode != 0:
                git("merge", "--abort")
                warning = "Vault commit saved locally, but pull/merge failed; resolve it before the next sync."
            elif git("push", "-q", timeout=45).returncode != 0:
                warning = "Vault commit saved locally, but push failed."
    except subprocess.TimeoutExpired:
        warning = "Vault commit saved locally; push timed out (offline?). Obsidian Git will push it later."
    if warning:
        print(json.dumps({"systemMessage": warning}))
    return 0


COMMANDS = {"session-start": session_start, "post-edit": post_edit, "stop": stop}

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
