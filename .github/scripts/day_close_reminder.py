"""End-of-day Telegram reminder to run /day-close, unless today's review is already in the session log.
No LLM, no API tokens, stdlib only; reuses the morning brief's helpers and bot.

Usage:
  python .github/scripts/day_close_reminder.py             send (needs TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID)
  python .github/scripts/day_close_reminder.py --dry-run   print the message instead of sending it
  add --evening-only to skip it before 18:00 local time (a scheduled run GitHub started hours late)

Language and time zone come from the same BRIEF_LANG and BRIEF_TIMEZONE variables as the morning brief.
"""
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import morning_brief as mb  # noqa: E402

LIST_MAX = 5  # due items named in the message; the rest are only counted

TEXT = {
    "en": {
        "title": "Day close", "due": "Overdue or due tomorrow ({n}):",
        "total": "Plus {n} more open task(s) in your to-do list and projects.",
        "cta": "Open Claude Code and type <code>/day-close</code>: it checks what is already done so tomorrow's "
               "brief starts up to date.",
    },
    "es": {
        "title": "Cierre del día", "due": "Vencidas o para mañana ({n}):",
        "total": "Además hay {n} tarea(s) abiertas en tus pendientes y proyectos.",
        "cta": "Abre Claude Code y escribe <code>/day-close</code>: reviso qué ya está hecho para que "
               "el brief de mañana salga al día.",
    },
}
R = TEXT.get(os.environ.get("BRIEF_LANG", "en").lower(), TEXT["en"])


def day_close_done(today):
    """Same marker as the `prompt` hook: a log line starting with "- YYYY-MM-DD — Day close"."""
    log = mb.ROOT / "00_system" / f"claude_log_{today:%Y_%m}.md"
    marker = f"- {today.isoformat()} — Day close"
    return log.exists() and any(l.startswith(marker) for l in log.read_text(encoding="utf-8").splitlines())


def build(today):
    """The reminder text, or None when today's review is done."""
    if day_close_done(today):
        return None
    tomorrow, due, total = today + timedelta(days=1), [], 0
    for path, data, text in mb.notes():
        rel = path.relative_to(mb.ROOT).as_posix()
        if rel.startswith("01_inbox/"):
            continue
        for task in mb.open_tasks(text.splitlines()):
            match = mb.DUE_RE.search(task)
            d = mb.parse_iso(match.groups()) if match else None
            if d and d <= tomorrow:
                due.append((d, mb.clean(task)))
        # the rest is counted where /day-close looks: to-do "Now" and active projects' "Next steps"
        if rel == "07_personal/todo.md":
            rest = mb.open_tasks(mb.section(text, "Now"))
        elif data.get("type") == "project" and data.get("status") == "active":
            rest = mb.open_tasks(mb.section(text, "Next steps"))
        else:
            rest = []
        total += sum(1 for t in rest if not ((m := mb.DUE_RE.search(t)) and (d := mb.parse_iso(m.groups())) and d <= tomorrow))
    out = [f"🌙 <b>{R['title']}</b>", ""]
    if due:
        out.append(R["due"].format(n=len(due)))
        out += [f"• {d:%m-%d} — {mb.esc(t)}" for d, t in sorted(due)[:LIST_MAX]]
        out.append("")
    out.append(R["total"].format(n=total))
    out += ["", R["cta"]]
    return "\n".join(out)


def main():
    now = datetime.now(mb.local_timezone())
    today = now.date()
    if "--evening-only" in sys.argv and now.hour < 18:
        print(f"It is {now:%H:%M}: too early for the end-of-day reminder; skipping.")
        return 0
    message = build(today)
    if message is None:
        print(f"Day close already done on {today}; nothing to send.")
        return 0
    if "--dry-run" in sys.argv:
        print(message)
        return 0
    token, chat_id = os.environ.get("TELEGRAM_BOT_TOKEN"), os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        sys.exit("TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID must be set")
    result = mb.telegram("sendMessage", token, chat_id=chat_id, text=message, parse_mode="HTML",
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
