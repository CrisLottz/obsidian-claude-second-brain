"""Validate note frontmatter against 00_system/vault_conventions.md.

Usage:
  python validate_frontmatter.py --all            check every note in the vault
  python validate_frontmatter.py FILE [FILE ...]  check specific notes

Allowed `type` and `status` values are read from the tables in
vault_conventions.md, so adding a value there is enough. Stdlib only.
Exit code 1 when any error is found.
"""
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONVENTIONS = ROOT / "00_system" / "vault_conventions.md"
SKIP_DIRS = {".git", ".obsidian", ".claude", ".trash"}
SKIP_PREFIXES = ("00_system/templates/",)
SKIP_FILES = {"CLAUDE.md", "README.md", "AGENTS.md", "GEMINI.md", "QWEN.md", "CHANGELOG.md"}  # agent instruction files, not notes
INBOX = "01_inbox/"
REQUIRED = ["title", "type", "status", "author", "created", "updated", "summary", "up"]
SCALAR = ["title", "type", "status", "author", "created", "updated", "summary", "due", "period"]
LISTS = ["aliases", "tags"]
AUTHORS = {"human", "ai", "mixed"}  # fallback when the `author` table in vault_conventions.md is not found
NAME_RE = re.compile(r"^[a-z0-9][a-z0-9_]*\.md$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
PERIOD_RE = re.compile(r"^\d{4}-\d{2}$")
WIKILINK_RE = re.compile(r"^\[\[([^\]|#]+)(?:[#|][^\]]*)?\]\]$")
KEY_RE = re.compile(r"^([A-Za-z_][\w-]*):(?:\s+(.*))?$")


def allowed_values(heading):
    """First-column `values` of the table under the '### `heading`' section."""
    text = CONVENTIONS.read_text(encoding="utf-8")
    section = re.search(rf"^### `{heading}`.*?$(.*?)(?=^#)", text, re.S | re.M)
    if not section:
        return set()
    return set(re.findall(r"^\| `([a-z0-9_-]+)` \|", section.group(1), re.M))


def read_note(path):
    """Note text (a UTF-8 BOM is dropped), or None when the file is not UTF-8."""
    try:
        return Path(path).read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        return None


def unquote(value):
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def parse_frontmatter(text):
    """Return (data, error). Handles the flat schema used in this vault."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, "missing frontmatter (line 1 must be ---)"
    try:
        end = lines.index("---", 1)
    except ValueError:
        return None, "frontmatter is not closed with ---"
    data, errors, key = {}, [], None
    for raw in lines[1:end]:
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if raw[0] in " \t-":
            if stripped.startswith("-") and key is not None:
                if not isinstance(data[key], list):
                    data[key] = []
                item = stripped[1:].strip()
                if item.startswith("[["):  # YAML reads an unquoted [[link]] as a nested list
                    errors.append(f'`{key}` item {item} must be quoted: - "{item}"')
                data[key].append(unquote(item))
            continue
        match = KEY_RE.match(raw)
        if not match:
            errors.append(f"invalid YAML line: {raw!r}")
            continue
        key, value = match.group(1), (match.group(2) or "").strip()
        if value.startswith("[["):
            errors.append(f'`{key}` value {value} must be quoted: "{value}"')
        elif value and value[0] not in "\"'[" and (": " in value or " #" in value):
            errors.append(f"`{key}` contains ': ' or ' #' — wrap the value in double quotes")
        if value.startswith("[") and value.endswith("]"):
            data[key] = [unquote(v.strip()) for v in value[1:-1].split(",") if v.strip()]
        else:
            data[key] = unquote(value)
    return data, "; ".join(errors) or None


def note_names():
    """File names (without .md; with extension for other files) present in the vault."""
    names = set()
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for f in filenames:
            names.add(f[:-3] if f.endswith(".md") else f)
    return names


def relpath(path):
    return Path(os.path.relpath(os.path.abspath(path), ROOT)).as_posix()


def should_check(path):
    rel = relpath(path)
    if rel.startswith("..") or not rel.endswith(".md") or rel in SKIP_FILES:
        return False
    if rel.split("/")[0] in SKIP_DIRS:
        return False
    return not rel.startswith(SKIP_PREFIXES)


def check(path, types=None, statuses=None, names=None):
    rel = relpath(path)
    in_inbox = rel.startswith(INBOX)
    types = types if types is not None else allowed_values("type")
    statuses = statuses if statuses is not None else allowed_values("status")
    errors = []
    if not in_inbox and not NAME_RE.match(Path(rel).name):
        errors.append("file name must be lowercase snake_case: a-z, 0-9 and _")
    text = read_note(path)
    if text is None:
        return errors + ["file is not valid UTF-8 — re-save it with UTF-8 encoding"]
    data, err = parse_frontmatter(text)
    if data is None:
        return [] if in_inbox else errors + [err]
    if err:
        errors.append(err)
    for key in SCALAR:
        if isinstance(data.get(key), list):
            errors.append(f"`{key}` must be a single value, not a list")
            data[key] = ""
    for key in LISTS:
        if data.get(key) not in (None, "") and not isinstance(data[key], list):
            errors.append(f'`{key}` must be a list, one item per line: - "value"')

    if not in_inbox:
        for key in REQUIRED:
            if key == "up" and rel == "00_home.md":
                continue
            if data.get(key) in (None, "", []):
                errors.append(f"missing or empty `{key}`")
    if data.get("type") and data["type"] not in types:
        errors.append(f"type `{data['type']}` is not allowed; valid: {', '.join(sorted(types))}")
    if data.get("status") and data["status"] not in statuses:
        errors.append(f"status `{data['status']}` is not allowed; valid: {', '.join(sorted(statuses))}")
    if data.get("author"):
        authors = allowed_values("author") or AUTHORS  # one row per agent in vault_conventions.md
        if data["author"] not in authors:
            errors.append(f"author `{data['author']}` must be one of: {', '.join(sorted(authors))}")
    for key in ("created", "updated", "due"):
        if data.get(key) and not DATE_RE.match(str(data[key])):
            errors.append(f"`{key}` must be YYYY-MM-DD, got `{data[key]}`")
    if data.get("period") and not PERIOD_RE.match(str(data["period"])):
        errors.append(f"`period` must be YYYY-MM, got `{data['period']}`")

    up = data.get("up")
    if up not in (None, ""):
        if not isinstance(up, list):
            errors.append('`up` must be a list of quoted wikilinks, one per line: - "[[hub_name]]"')
        else:
            names = names if names is not None else note_names()
            for link in up:
                match = WIKILINK_RE.match(link)
                if not match:
                    errors.append(f'`up` item `{link}` must be a quoted wikilink like "[[hub_name]]"')
                elif match.group(1).strip() not in names:
                    errors.append(f"`up` points to [[{match.group(1)}]], which does not exist")
    return errors


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    if argv == ["--all"]:
        paths = []
        for dirpath, dirnames, filenames in os.walk(ROOT):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            paths += [Path(dirpath) / f for f in filenames if f.endswith(".md")]
    else:
        paths = [Path(a) for a in argv]
    types, statuses, names = allowed_values("type"), allowed_values("status"), note_names()
    failed = 0
    for path in sorted(paths):
        if not should_check(path):
            continue
        errors = check(path, types, statuses, names)
        if errors:
            failed += 1
            print(f"{relpath(path)}")
            for e in errors:
                print(f"  - {e}")
    checked = sum(1 for p in paths if should_check(p))
    print(f"\n{checked} notes checked, {failed} with problems.")
    return 1 if failed else 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main(sys.argv[1:]))
