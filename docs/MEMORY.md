# MEMORY: what has been done (AI reads this to resume; AI writes here when a task is finished)
> Read the STATUS block + only your own role's section. Do not read the whole file. Keep every entry to 3-5 lines.
> Format of an entry: `YYYY-MM-DD | task ID | what was done | files touched | next / blockers`

## STATUS (R1 only edits this block)
- Phase: Setup, Week 1 (Nov 2026). Completion: ~5% (scaffold + mock pipeline verified).
- Works now: mock pipeline end to end (mock reference + mock recognizer + real alignment scorer), Flask starter app, tests.
- Not started: real recognizer, real reference phonemes, real UI, dashboard, datasets, report.
- Open questions: (1) synopsis says Nov-Apr but team said 3-4 months: confirm with guide. (2) exact date of the 30-40% review.
- Dataset/audio locations (never in Git): _fill in_

## R1 log
2026-11-04 | SETUP | repo scaffold, docs, contract, mock pipeline, tests | whole repo | each role starts its Week 1 tasks in TASKS.md
2026-11-25 | R1-01, R1-02 | Repo created and pushed to GitHub. Installed deps, ran pytest (6/6 pass). Started app with USE_MOCK_ML=1, verified GET /api/languages (4 langs), GET /api/content/english (3 beginner words), POST /api/assess with text=hello+language=english returns per-phoneme scores and feedback. Mock pipeline confirmed end to end. | docs/TASKS.md, docs/MEMORY.md | R1-03: set daily check-in + Sunday merge; all roles start W1 tasks

## R2 log
(empty)

## R3 log
(empty)

## R4 log
(empty)

## R5 log
(empty)
