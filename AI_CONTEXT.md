# AI_CONTEXT (read first, then stop reading until needed)
Project: **Language Coach**, multilingual pronunciation coach (Flask + Python ML), team of 5 (roles R1-R5), deploy at the very end.

Read ONLY, in this exact order, and only the parts you need:
1. `docs/MEMORY.md` : STATUS block + your role log only (what is done, where we stopped).
2. `docs/TASKS.md`  : Header + your role table only (what to do next; build the person's workflow from it).
3. `docs/PRD.md`    : ONLY the one numbered section the task needs (sections are numbered 1-9).
4. `docs/GUIDELINES.md` : Rules for token use, secrets, git, code (read once per session).

TOKEN SAVING RULES:
- Never read `docs/setup/`, `docs/project/`, `docs/team/`, `docs/design/`, or `docs/report/` unless a task explicitly targets those human-facing documents.
- Never read the whole repo, `data/`, or other roles' folders.
- Never open, print or commit `.env`; read configuration only via `os.getenv` or `app/config.py`.
- When a task is finished: update its row in `docs/TASKS.md` to `DONE (YYYY-MM-DD)`, add a 3-5 line entry in your role's `docs/MEMORY.md` log, then say what is next.
