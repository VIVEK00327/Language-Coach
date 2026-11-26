# GUIDELINES: how AI (and humans) work in this repo
> Goal: finish tasks correctly while spending as few tokens as possible, and never leak secrets.

## 1. Read order (stop as soon as you have enough)
1. `AI_CONTEXT.md` (root, 20 lines).
2. `docs/MEMORY.md`: STATUS block + your role's log only.
3. `docs/TASKS.md`: header + your role's table only.
4. `docs/PRD.md`: only the section the task needs (sections are numbered).
5. Source files: only the files named in your task's folders. Open a whole folder listing only if you must.

## 2. Token-saving rules
- Do NOT read the entire repo, `data/`, model files, audio, `docs/report/`, or other roles' folders.
- Do not re-read a file already in this conversation; do not paste large files back; show only the changed lines.
- Prefer searching (grep for a function name) over opening files. Open a file range, not the whole file, when possible.
- Do not re-explain the project to the user; it is in the PRD. Keep replies short: what changed, how to run, what is next.
- Work on ONE task at a time (the next one from TASKS.md), finish it, test it, log it, then continue.
- Before writing new code, check whether the function already exists (grep) and reuse it.

## 3. Secrets and private data (strict)
- All keys, tokens and passwords live ONLY in `.env` (git-ignored). `.env.example` lists variable names with empty or fake values and is the only env file committed.
- Read config with `os.getenv(...)` (see `app/config.py`). Never hardcode a key, token, password, or personal URL in code, docs, tests, notebooks, logs, commit messages, or chat.
- Never print, echo, or paste the contents of `.env`. Never ask the user to paste a real key into chat.
- Do not commit: `.env`, datasets, audio recordings of real people, model weights, the SQLite database (`instance/`). All are in `.gitignore`.
- If a secret is ever committed or shared: tell the lead immediately, revoke/rotate the key, and remove it from Git history.
- Before every commit run `git status` and check no `.env` or data file is staged.

## 4. Ownership and interfaces
- Edit only your role's folders (PRD section 8). Cross-role changes go through a GitHub Issue titled `[Rx -> Ry] what you need`.
- Do not change `ml/contracts.py` or function signatures (PRD section 4) without the lead; if approved, update the PRD in the same PR.
- ML code never imports Flask. Flask code contains no scoring logic. It only calls `ml.pipeline.assess`.
- Use the mock (`USE_MOCK_ML=1` in `.env`) when a dependency is not ready.

## 5. Code standards
- Python 3.10+, type hints on public functions, short docstring stating the owner role and the contract.
- Small functions, no dead code, no print debugging left in. Use `logging`, not `print`, in modules.
- Every new function with logic gets a test in `tests/`. Run `python -m pytest tests` before commit.
- Add new dependencies to `requirements.txt` (pinned once working) and mention it in the PR.
- Keep commits small: `R3: add weighted substitution costs`.

## 6. Git workflow
While only one person works: commit directly to `main`. Switch back to branches + PRs when teammates start.
```bash
git add -A && git status        # confirm no .env/data staged
git commit -m "R2: real English phoneme recognizer" && git push
```
Docs conflicts: each role edits only its own TASKS table and its own MEMORY log section, so merges stay clean.

## 7. Finishing a task (always)
1. Tests pass. 2. TASKS row -> `DONE (date)`. 3. One 3-5 line entry in your MEMORY role log (format at top of MEMORY.md).
4. If a decision was made, add a row to PRD section 9. 5. Tell the user what is next from TASKS.md.

## 8. When unsure
Ask one short question rather than guessing, or choose the simplest option, state the assumption in one line, and log it in MEMORY.
