# Telegram morning brief (optional, about 5 minutes)

A Telegram message every morning with deadlines in the next 7 days, overdue items, the to-do *Now* list, the next step of each active project, pending payments, the inbox size and the vault's health. It runs on GitHub Actions with a plain Python script: **no AI, no tokens**. The user's computer can be off.

The brief leaves the vault: it travels through Telegram's servers (bot chats are not end-to-end encrypted). Keep in it only what the user would put in a phone notification.

## Steps (the user does them; never ask for the token in the chat)

1. **Create the bot.** In Telegram, open **@BotFather** → `/newbot` → name and a username ending in `bot`. Copy the token. Then send `/setjoingroups`, choose the bot and pick **Disable**.
2. **Start a chat with it.** Open `t.me/<bot_username>` and press **Start**. Check the `@username` at the top of the chat: several bots can share a display name.
3. **Save the token as a secret** in the vault's GitHub repo: Settings → Secrets and variables → Actions → Secrets → New repository secret, named `TELEGRAM_BOT_TOKEN`. Or, in their own terminal: `gh secret set TELEGRAM_BOT_TOKEN`. If it ever leaks, `/revoke` it in BotFather.
4. **Set the variables** (Variables tab, same page), before the first run:

   | Variable | Example | What it does |
   |---|---|---|
   | `BRIEF_LANG` | `en` or `es` | Language of the labels (default `en`) |
   | `BRIEF_TIMEZONE` | `Europe/Madrid` | IANA time zone for "today" and deadlines (default `UTC`) |
   | `BRIEF_ARCHIVE` | `true` | Also saves each brief in `00_system/briefs/` and commits it (one commit per day) |
   | `BRIEF_GIT_NAME` / `BRIEF_GIT_EMAIL` | name / noreply email | Author of that commit (default: the Actions bot) |
   | `BRIEF_ENABLED` | `true` | Turns the daily schedule on. Manual runs always work |

5. **Find the chat id and send the first brief.** Actions tab → **Morning brief** → **Run workflow**. Without a chat id the step `Build and send the brief` lists the private chats that wrote to the bot (`123456789  @you`) and stops without sending (the run shows as failed: expected). Save that number as the secret `TELEGRAM_CHAT_ID` and run it again: it ends with `Sent`. Telegram keeps a bot's messages for 24 hours: if the list is empty, press **Start** again and re-run.
6. **Turn on the schedule:** variable `BRIEF_ENABLED` = `true`.
7. **Pick the time** in `.github/workflows/morning_brief.yml`:

   ```yaml
   - cron: "37 6 * * *"        # minute hour * * * -> 06:37 every day
     timezone: "Europe/Madrid" # your IANA time zone
   ```

   Commit and push. GitHub can start scheduled runs late; an off-peak minute such as `:37` helps.

Preview without sending: `python3 .github/scripts/morning_brief.py --dry-run` (`py` on Windows).

## How notes feed it

- Deadlines: `📅 YYYY-MM-DD` at the end of an open task, or a note's `due` property.
- To do now: open tasks under `## Now` in `07_personal/todo.md`.
- Next steps: the first open task under `## Next steps` of each project with `status: active`.
- Each task is shown once, in its most urgent section.

## End-of-day reminder (optional)

`DAY_CLOSE_ENABLED` = `true` turns on a Telegram reminder to run `/day-close` (same bot, language and time zone). A Claude Code version needs the environment variable `VAULT_DAY_CLOSE_HOUR` (for example `20`) in `~/.claude/settings.json` under `"env"`.
