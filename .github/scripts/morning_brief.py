"""Morning brief built from the vault and sent to Telegram. No LLM, no API tokens, stdlib only.

It reads structured data only: YAML frontmatter (`due`) and open `- [ ]` tasks with their deadline
(`📅 YYYY-MM-DD`; any other date in a task is context). Each task is shown once, in its most urgent
section: overdue → next 7 days → "Now" in the to-do list → project next step.
See README → "Telegram morning brief".

Usage:
  python .github/scripts/morning_brief.py              send (needs TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID)
  python .github/scripts/morning_brief.py --dry-run    print the brief instead of sending it
  add --archive to also save it as today's entry in 00_system/briefs/brief_YYYY_MM.md

Environment (GitHub repository variables in the workflow):
  BRIEF_LANG       en (default) | es
  BRIEF_TIMEZONE   IANA name such as Europe/Madrid (default UTC)
  BRIEF_UTC_OFFSET fallback when the IANA database is missing (e.g. Windows): hours, like -5
If TELEGRAM_CHAT_ID is missing, the script lists the private chats that wrote to the bot in the
last 24 hours (send /start to the bot first) and stops: save your id as the secret. It never sends
the brief to a chat it discovered on its own.
"""
import html
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".claude" / "hooks"))
import validate_frontmatter as vf  # noqa: E402

WINDOW_DAYS = 7
SKIP_DIRS = {".git", ".obsidian", ".claude", ".github", ".trash"}
TASK_RE = re.compile(r"^\s*- \[ \]\s+(.+)$")
ISO_RE = re.compile(r"(?<![\w./-])(\d{4})-(\d{2})-(\d{2})(?![\w/-]|\.\w)")  # standalone dates, not parts of file names
DUE_RE = re.compile(r"\s*📅\s*(\d{4})-(\d{2})-(\d{2})")  # a task's deadline; any other date in it is just context
LINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")

TEXT = {
    "en": {
        "weekdays": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        "upcoming": "Next {n} days", "overdue": "Overdue", "now": "To do now",
        "now_empty": "Nothing under «Now» in your to-do list", "projects": "Active projects — next step",
        "no_step": "(no next step)", "due": "due", "money": "{n} pending payment(s) this month",
        "footer": "Inbox: {inbox} note(s) · ⚠️ {broken} note(s) with frontmatter problems",
        "archive_title": "Morning briefs {month}", "archive_alias": "Morning briefs {month}",
    },
    "es": {
        "weekdays": ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"],
        "upcoming": "Próximos {n} días", "overdue": "Vencidos", "now": "Pendientes ahora",
        "now_empty": "No hay nada en «Now» de tus pendientes", "projects": "Proyectos activos — siguiente paso",
        "no_step": "(sin siguiente paso)", "due": "entrega", "money": "{n} pago(s) pendiente(s) este mes",
        "footer": "Inbox: {inbox} nota(s) · ⚠️ {broken} nota(s) con errores de ficha",
        "archive_title": "Morning briefs {month}", "archive_alias": "Resúmenes matutinos {month}",
    },
}
T = TEXT.get(os.environ.get("BRIEF_LANG", "en").lower(), TEXT["en"])


def local_timezone():
    name = os.environ.get("BRIEF_TIMEZONE", "UTC")
    if name.upper() == "UTC":
        return timezone.utc
    try:
        from zoneinfo import ZoneInfo
        return ZoneInfo(name)
    except Exception:  # no IANA database (Windows without tzdata) or a typo
        hours = float(os.environ.get("BRIEF_UTC_OFFSET", "0"))
        print(f"WARNING: time zone {name!r} not found (typo, or no IANA database here); using UTC{hours:+g}. "
              "Check BRIEF_TIMEZONE or set BRIEF_UTC_OFFSET.", file=sys.stderr)
        return timezone(timedelta(hours=hours))


def notes():
    """(path, frontmatter, text) for every note outside system and template folders."""
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        if "00_system/templates" in Path(dirpath).as_posix():
            continue
        for name in filenames:
            if name.endswith(".md"):
                path = Path(dirpath) / name
                text = vf.read_note(path) or path.read_text(encoding="utf-8", errors="replace")
                data, _ = vf.parse_frontmatter(text)
                yield path, data or {}, text


def clean(text):
    """Plain text for a notification line: wikilinks as their names, no bold markers, no deadline marker
    (the date is already the line's prefix). Never cut."""
    text = LINK_RE.sub(lambda m: m.group(2) or m.group(1), DUE_RE.sub("", text))
    return re.sub(r"\s+([.,;])", r"\1", text.replace("*", "")).strip()


def key(task):
    """Identity of a task across sections: same words, ignoring case, punctuation and the deadline marker."""
    return " ".join(re.findall(r"\w+", DUE_RE.sub("", LINK_RE.sub(lambda m: m.group(1), task)).lower()))


def esc(text):
    """Escape for Telegram's HTML mode; `code` becomes <code> so Telegram doesn't auto-link /commands or file.md."""
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", html.escape(text, quote=False))
    return text.replace("`", "")


def display_name(data, path):
    """The first alias is the display name (vault_conventions §2); fall back to the title."""
    aliases = data.get("aliases")
    if isinstance(aliases, list) and aliases:
        return aliases[0]
    return data.get("title") or path.stem


def parse_iso(match):
    try:
        return date(int(match[0]), int(match[1]), int(match[2]))
    except ValueError:
        return None


def section(text, heading):
    """Lines under a `## heading` until the next `## `."""
    lines, inside = [], False
    for line in text.splitlines():
        if line.startswith("## "):
            inside = line[3:].strip().lower() == heading.lower()
            continue
        if inside:
            lines.append(line)
    return lines


def open_tasks(lines):
    return [m.group(1).strip() for m in map(TASK_RE.match, lines) if m and m.group(1).strip()]


def block(heading, items):
    """A section: heading, then bullets with a blank line between them (easier to read on a phone)."""
    lines = ["", heading]
    for k, item in enumerate(items):
        lines += [""] * bool(k) + [f"• {item}"]
    return lines


def build(today):
    dated, project_steps, pending_money = [], [], 0  # dated: (date, label, task — None for a `due` note)
    horizon = today + timedelta(days=WINDOW_DAYS)
    for path, data, text in notes():
        rel = path.relative_to(ROOT).as_posix()
        if rel.startswith(("01_inbox/", "00_system/briefs/")):
            continue
        name = display_name(data, path)
        due = ISO_RE.search(str(data.get("due") or ""))
        if due and data.get("status") not in ("done", "cancelled", "archived"):
            d = parse_iso(due.groups())
            if d:
                dated.append((d, f"{name} ({T['due']})", None))
        for task in open_tasks(text.splitlines()):
            match = DUE_RE.search(task)
            d = parse_iso(match.groups()) if match else None
            if d:
                dated.append((d, f"{clean(task)} — {name}", task))
        if data.get("type") == "project" and data.get("status") == "active":
            project_steps.append((name, open_tasks(section(text, "Next steps"))))
        if data.get("type") == "finance" and str(data.get("period")) == today.strftime("%Y-%m"):
            pending_money += sum(1 for line in text.splitlines()
                                 if line.startswith("|") and line.rstrip().rstrip("|").strip().endswith("pending"))

    todo_path = ROOT / "07_personal" / "todo.md"
    todo = open_tasks(section(vf.read_note(todo_path) or "", "Now")) if todo_path.exists() else []
    inbox = len(list((ROOT / "01_inbox").glob("*.md")))
    names = vf.note_names()
    types, statuses = vf.allowed_values("type"), vf.allowed_values("status")
    broken = sum(1 for p, _, _ in notes() if vf.should_check(p) and vf.check(p, types, statuses, names))

    # Sections in order of urgency; a task already shown is left out of every section below it.
    shown = set()

    def first_time(task):
        if task is None:
            return True
        k = key(task)
        if k in shown:
            return False
        shown.add(k)
        return True

    def take(items, limit):
        """The first `limit` items whose task isn't shown yet. Marking stops at the limit, so a task
        cut by it can still appear in a later section instead of vanishing."""
        picked = []
        for item in items:
            if len(picked) == limit:
                break
            if first_time(item[-1]):
                picked.append(item)
        return picked

    dated.sort(key=lambda x: (x[0], x[1]))
    overdue = [(d, label) for d, label, _ in take([x for x in dated if x[0] < today], 5)]
    upcoming = [(d, label) for d, label, _ in take([x for x in dated if today <= x[0] <= horizon], 8)]
    now = [clean(t) for t, in take([(t,) for t in todo], 8)]
    projects = []
    for name, steps in sorted(project_steps):
        step = next((s for s in steps if key(s) not in shown), None)
        if step:
            shown.add(key(step))
            projects.append(f"<b>{esc(name)}</b>: {esc(clean(step))}")
        elif not steps:
            projects.append(f"<b>{esc(name)}</b>: {T['no_step']}")

    out = [f"☀️ <b>{T['weekdays'][today.weekday()]} {today.isoformat()}</b>"]
    if upcoming:
        out += block(f"📅 <b>{T['upcoming'].format(n=WINDOW_DAYS)}</b>", [f"{d:%m-%d} — {esc(t)}" for d, t in upcoming])
    if overdue:
        out += block(f"⏰ <b>{T['overdue']}</b>", [f"{d:%m-%d} — {esc(t)}" for d, t in overdue])
    out += block(f"✅ <b>{T['now']}</b>", [esc(t) for t in now] or [T["now_empty"]])
    if projects:
        out += block(f"🚀 <b>{T['projects']}</b>", projects)  # every active project, none hidden
    if pending_money:
        out += ["", f"💰 {T['money'].format(n=pending_money)}"]
    out += ["", f"📥 {T['footer'].format(inbox=inbox, broken=broken)}"]
    return "\n".join(out)


def archive(brief, today):
    """Save the brief as plain Markdown under today's heading of the monthly series (replaced if re-run)."""
    path = ROOT / "00_system" / "briefs" / f"brief_{today:%Y_%m}.md"
    body = re.sub(r"<code>(.*?)</code>", r"`\1`", brief)
    body = html.unescape(re.sub(r"</?b>", "", body)).split("\n", 1)[1].strip()
    body = re.sub(r"^• ", "- ", body, flags=re.M)
    entry = f"## {today:%Y-%m-%d} ({T['weekdays'][today.weekday()].lower()})\n\n{body}\n"
    month = f"{today:%Y-%m}"
    if path.exists():
        text = path.read_text(encoding="utf-8")
        text = re.sub(r"^updated: .*$", f"updated: {today:%Y-%m-%d}", text, count=1, flags=re.M)
        text = re.sub(rf"^## {today:%Y-%m-%d} .*?(?=^## |\Z)", "", text, flags=re.M | re.S).rstrip() + "\n"
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        text = (
            "---\n"
            f"title: {T['archive_title'].format(month=month)}\n"
            "type: log\n"
            "status: active\n"
            "author: ai\n"
            f"created: {today:%Y-%m-%d}\n"
            f"updated: {today:%Y-%m-%d}\n"
            f"summary: Daily morning briefs of {month} — a snapshot of deadlines, pending items and next steps per day.\n"
            f"period: {month}\n"
            "up:\n"
            '  - "[[00_home]]"\n'
            "tags: [log, brief]\n"
            f"aliases: [{T['archive_alias'].format(month=month)}]\n"
            "---\n\n"
            f"# {T['archive_title'].format(month=month)}\n"
        )
    path.write_text(f"{text}\n{entry}", encoding="utf-8", newline="\n")
    return path


def pieces(text, size):
    """Paragraphs no longer than `size`; a longer one is split into lines, and a longer line into
    plain-text slices (never inside an HTML tag or entity)."""
    for para in text.split("\n\n"):
        if len(para) <= size:
            yield para
            continue
        for line in para.split("\n"):
            if len(line) <= size:
                yield line
                continue
            plain = html.unescape(re.sub(r"<[^>]+>", "", line))
            step = size // 5  # escaping can make a character up to 5 times longer (& → &amp;)
            yield from (html.escape(plain[i:i + step], quote=False) for i in range(0, len(plain), step))


def chunks(text, size=4000):
    """Split at blank lines so a long brief goes out as several messages (Telegram's limit is 4096)."""
    parts, current = [], ""
    for piece in pieces(text, size):
        candidate = f"{current}\n\n{piece}" if current else piece
        if len(candidate) > size:
            parts.append(current)
            current = piece
        else:
            current = candidate
    return parts + [current] if current else parts


def telegram(method, token, **params):
    """Call the Bot API; errors come back as {"ok": false, "description": ...} (never with the token)."""
    url = f"https://api.telegram.org/bot{token}/{method}"
    data = urllib.parse.urlencode(params).encode()
    try:
        with urllib.request.urlopen(urllib.request.Request(url, data=data), timeout=30) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as error:  # 401 Unauthorized, 400 chat not found… explained in the body
        try:
            return json.loads(error.read().decode())
        except ValueError:
            return {"ok": False, "description": f"HTTP {error.code}"}
    except urllib.error.URLError as error:
        return {"ok": False, "description": f"network error: {error.reason}"}


def private_chats(token):
    """{chat id: who} for the private chats that wrote to the bot recently, or an error description."""
    updates = telegram("getUpdates", token)
    if not updates.get("ok"):
        return updates.get("description", "getUpdates failed")
    chats = {}
    for update in updates.get("result", []):
        chat = (update.get("message") or {}).get("chat") or {}
        if chat.get("type") == "private":
            chats[chat["id"]] = f"@{chat['username']}" if chat.get("username") else chat.get("first_name", "")
    return chats


def main():
    today = datetime.now(local_timezone()).date()
    brief = build(today)
    if "--archive" in sys.argv:
        print(f"Archived in {archive(brief, today).relative_to(ROOT).as_posix()}")
    if "--dry-run" in sys.argv:
        print(brief)
        return 0
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not token:
        sys.exit("TELEGRAM_BOT_TOKEN is not set: add it as a repository secret (see README)")
    if not chat_id:
        chats = private_chats(token)
        if isinstance(chats, str):
            print(f"Telegram error: {chats}")
            return 1
        if not chats:
            print("TELEGRAM_CHAT_ID is not set and nobody wrote to the bot in the last 24 hours: "
                  "send /start to your bot and run this again. Nothing was sent.")
            return 1
        print("TELEGRAM_CHAT_ID is not set. Private chats that wrote to the bot recently:")
        for found, who in chats.items():
            print(f"  {found}  {who}")
        print("Save YOUR id as the TELEGRAM_CHAT_ID secret and run this again. Nothing was sent.")
        return 1
    for part in chunks(brief):
        result = telegram("sendMessage", token, chat_id=chat_id, text=part, parse_mode="HTML",
                          disable_web_page_preview="true")
        if not result.get("ok"):
            print(f"Telegram error: {result.get('description', result)}")
            return 1
    print("Sent")
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
