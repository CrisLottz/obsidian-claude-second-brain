---
name: interview
description: Interview the user in seven rounds to build or refresh their full profile, the summary in the root note, people_and_context, the hubs and the "Working with me" section of the global instructions. Run only when the user asks.
argument-hint: "[round number or topic — optional, to redo only part of it]"
disable-model-invocation: true
---

# Profile interview

> **Paths:** every path in this skill is relative to the vault root (its path is in the global `~/.claude/CLAUDE.md`). This skill also works from sessions opened in other folders: there, use full paths and run Git as `git -C <vault> …`.

Goal: give every future session the context it needs about the user. The full detail goes to `07_personal/profile.md`; the root note keeps only a short summary. Conduct it in the user's language, one round at a time.

## Before starting

Read `00_home.md`, `07_personal/profile.md`, the main hubs, `07_personal/people/people_and_context.md` and the **Language** and **Working with me** sections of `.claude/global/CLAUDE.md`. If they already have content, this is a refresh: ask about what changed or is missing, don't repeat known facts. If `$ARGUMENTS` names a round or topic, run only that.

## Rounds

Ask 3–5 questions per round, wait for the answers, ask brief follow-ups only where an answer is vague, then move on. Tell the user they can skip any question.

1. **Identity and work** — role, employers or clients, responsibilities, what a normal week looks like, career goals, what frustrates them.
2. **Education and learning** — studies, what they learn on their own, how they learn best.
3. **Projects and goals** — active personal and work projects, goals for the next 3 months and the next year, what success looks like.
4. **Health, habits and skills** — training, nutrition, routines, hobbies and practical skills; health facts worth knowing.
5. **Personality, tastes and interests** — values, strengths and weaknesses; books, movies, music, series, games; likes and dislikes.
6. **People and context** — the important people in their life and work, and their current situation.
7. **How to work with them** — language, tone, level of detail, how they like options presented, what annoys them in AI answers, when to ask vs. act.

## Write it down

Draft everything, show the drafts, and apply only after the user approves:

- `07_personal/profile.md` → every section, with the full detail (limit ~12,000 words). Set `status: active` once most sections have content.
- `00_home.md` → **Profile**: max ~25 lines, dense bullets summarizing the profile (who, work, goals, interests), ending with the link to it.
- `07_personal/people/people_and_context.md` → Current situation, Goals, People table.
- Hubs → sharpen the one-line purpose of each hub with what you learned.
- `.claude/global/CLAUDE.md` → **Language** and **Working with me**: concrete, testable instructions (e.g. "give a recommendation, not just options"). This file is loaded in every session, in any project.
- Set `author: mixed` where the user's words are kept, update `updated`, and append one line to the session log.
