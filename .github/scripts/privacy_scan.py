"""Fail when a tracked file looks like it leaks a secret or personal data. Stdlib only.

Meant for the public template: run it before opening a PR, and in CI on the upstream repo.

  python .github/scripts/privacy_scan.py           scan every file Git tracks
  python .github/scripts/privacy_scan.py FILE...   scan only these files

Built-in checks (generic, safe to publish): private keys, GitHub / Telegram / API tokens, e-mail
addresses that are not placeholders or no-reply, and personal home folders (C:\\Users\\name, /home/name).

Maintainer-specific terms (a real name, a company, a city) must not be written in this public file.
Put them in the environment variable PRIVACY_TERMS, comma-separated (in CI: a repository secret of
that name) and each one is searched case-insensitively.

Exit code 1 when anything is found. Findings print the file, line and rule, never the matched text.
"""
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

RULES = [
    ("private key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("GitHub token", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})\b")),
    ("Telegram bot token", re.compile(r"\b\d{8,10}:[A-Za-z0-9_-]{35}\b")),
    ("API key", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
    ("personal home folder", re.compile(r"[A-Za-z]:\\Users\\(?!<|you\b|your\b|name\b|user\b|username\b)[\w.-]+|/home/(?!<|you\b|your\b|name\b|user\b|username\b|runner\b)[a-z][\w.-]+|/Users/(?!<|you\b|your\b|name\b|user\b|username\b)[A-Za-z][\w.-]+")),
]
EMAIL = re.compile(r"[A-Za-z0-9._+-]+@([A-Za-z0-9-]+\.)+[A-Za-z]{2,}")
EMAIL_OK = re.compile(r"noreply|no-reply|@example\.|@correo\.com|^(you|tu|your|name|user|me)@", re.I)
BINARY_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pdf", ".zip", ".woff", ".woff2"}


def tracked_files():
    out = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=True).stdout
    return [ROOT / p for p in out.decode("utf-8").split("\0") if p]


def scan(path, terms):
    findings = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return findings  # binary or unreadable: nothing to read
    for number, line in enumerate(lines, 1):
        for name, pattern in RULES:
            if pattern.search(line):
                findings.append((number, name))
        for match in EMAIL.finditer(line):
            if not EMAIL_OK.search(match.group(0)):
                findings.append((number, "e-mail address"))
        lowered = line.lower()
        for term in terms:
            if term in lowered:
                findings.append((number, "private term from PRIVACY_TERMS"))
    return findings


def main(argv):
    terms = [t.strip().lower() for t in os.environ.get("PRIVACY_TERMS", "").split(",") if t.strip()]
    files = [Path(a).resolve() for a in argv] or tracked_files()
    total = 0
    for path in files:
        if path.suffix.lower() in BINARY_EXT or not path.is_file():
            continue
        for number, rule in scan(path, terms):
            total += 1
            print(f"{path.relative_to(ROOT).as_posix()}:{number}: {rule}")
    if total:
        print(f"\n{total} finding(s). Remove the data or, for a placeholder, adjust the rule.")
        return 1
    print(f"Privacy scan clean ({len(files)} files, {len(terms)} private term(s) checked).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
