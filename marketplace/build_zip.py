"""Build the marketplace zip of the second-brain-setup skill. Stdlib only.

Usage:  python marketplace/build_zip.py [--version 1.1.0]
Writes marketplace/dist/second-brain-setup-<version>.zip (the dist folder is git-ignored).

Before zipping it checks the things marketplaces reject: SKILL.md has valid frontmatter with `name`
(matching the folder) and `description`, there is at least one supporting file, and the privacy scan
finds nothing. The zip holds one top-level folder, the skill's files and the project's MIT licence.
"""
import re
import subprocess
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SKILL = HERE / "second-brain-setup"
SKIP = {"__pycache__"}


def fail(message):
    sys.exit(f"build_zip: {message}")


def frontmatter(text):
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        fail("SKILL.md must start with a --- frontmatter block")
    return dict(re.findall(r"^([a-z-]+):\s*(.+)$", match.group(1), re.M))


def files():
    return sorted(p for p in SKILL.rglob("*") if p.is_file() and not SKIP & set(p.parts))


def main(argv):
    version = argv[argv.index("--version") + 1] if "--version" in argv else "dev"
    data = frontmatter((SKILL / "SKILL.md").read_text(encoding="utf-8"))
    if data.get("name") != SKILL.name:
        fail(f"frontmatter name {data.get('name')!r} must equal the folder name {SKILL.name!r}")
    if len(data.get("description", "")) < 40:
        fail("frontmatter description is missing or too short")
    support = [p for p in files() if p.name != "SKILL.md"]
    if not support:
        fail("add at least one supporting file (references/ or scripts/)")

    scan = subprocess.run([sys.executable, str(ROOT / ".github" / "scripts" / "privacy_scan.py"), *map(str, files())],
                          capture_output=True, text=True)
    if scan.returncode:
        fail("privacy scan failed:\n" + scan.stdout)

    out = HERE / "dist" / f"{SKILL.name}-{version}.zip"
    out.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in files():
            zf.write(path, f"{SKILL.name}/{path.relative_to(SKILL).as_posix()}")
        zf.write(ROOT / "LICENSE", f"{SKILL.name}/LICENSE")
    print(f"{out.relative_to(ROOT).as_posix()}: {len(files()) + 1} files, {out.stat().st_size / 1024:.1f} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
