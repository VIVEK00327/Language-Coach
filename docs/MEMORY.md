# MEMORY: what has been done (AI reads this to resume; AI writes here when a task is finished)
> Read the STATUS block + only your own role's section. Do not read the whole file. Keep every entry to 3-5 lines.
> Format of an entry: `YYYY-MM-DD | task ID | what was done | files touched | next / blockers`

## STATUS (R1 only edits this block)
- Phase: Setup, Week 1 (Nov 2026). Completion: ~5% (scaffold + mock pipeline verified).
- Works now: mock pipeline end to end (mock reference + mock recognizer + real alignment scorer), Flask starter app, tests.
- Not started: real recognizer, real reference phonemes, real UI, dashboard, datasets, report.
- Open questions: (1) synopsis says Nov-Apr but team said 3-4 months: confirm with guide. (2) exact date of the 30-40% review.
- Dataset/audio locations (never in Git): _fill in_

### Daily check-in (post in group chat by 10 pm)
```
Done: (what you finished today)
Doing: (what you will work on next)
Blocked: (anything stopping you — tag the person)
```

### Sunday merge checklist (R1)
1. `git checkout main && git pull`
2. Merge each role branch; resolve conflicts with the author.
3. `python -m pytest tests` — all must pass.
4. `python run.py` (USE_MOCK_ML=1) — smoke-test the 3 API endpoints.
5. Update STATUS block above (phase, completion %, what works, what doesn't).
6. Post a 3-line summary to the group: what merged, what's next, any blockers.

### Questions for guide (R1 to ask)
1. The synopsis says Nov 2026 – Apr 2027 (6 months), but the team discussed 3-4 months. Which end date should we plan for?
2. What is the exact date of the 30-40% progress review?
3. Any specific deliverables expected at that review (demo, report draft, slides)?

## R1 log
2026-11-04 | SETUP | repo scaffold, docs, contract, mock pipeline, tests | whole repo | each role starts its Week 1 tasks in TASKS.md
2026-11-25 | R1-01, R1-02 | Repo created and pushed to GitHub. Installed deps, ran pytest (6/6 pass). Started app with USE_MOCK_ML=1, verified GET /api/languages (4 langs), GET /api/content/english (3 beginner words), POST /api/assess with text=hello+language=english returns per-phoneme scores and feedback. Mock pipeline confirmed end to end. | docs/TASKS.md, docs/MEMORY.md | R1-03: set daily check-in + Sunday merge; all roles start W1 tasks
2026-11-25 | R1-03 | Drafted team routine: daily check-in template (done/doing/blocked), Sunday merge checklist (6 steps: pull, merge, pytest, smoke-test, update STATUS, post summary), and 3 questions for guide (end date, review date, review deliverables). All saved under STATUS in MEMORY.md. | docs/MEMORY.md, docs/TASKS.md | R1-04: review/merge first PRs; ask guide the 3 questions

## R2 log
2026-11-26 | R2-01, R2-02 | Built `ml/speech/audio_utils.py` with `load_audio` (16 kHz mono conversion via soundfile + librosa resample), `trim_silence` (librosa top_db=30), and `normalise` (peak scaling). Created `scripts/record_clip.py` to record mic clips into data/raw/ using sounddevice. Added comprehensive unit tests with synthetic sine waves in `tests/test_audio_utils.py`, all 20 project tests pass. | ml/speech/audio_utils.py, scripts/record_clip.py, tests/test_audio_utils.py, docs/TASKS.md | R2-04 next: real English phoneme recognizer

## R3 log
2026-11-26 | R3-01, R3-02 | Installed espeak-ng (Windows MSI) + phonemizer pip package. Rewrote `get_reference_phonemes` to call phonemizer with espeak backend for real IPA output (e.g. "hello" → `h ə l oʊ`). Mock fallback preserved via `USE_MOCK_ML=1`. Added `_LANG_MAP` for en-us, hi, fr-fr; Sanskrit mapped to hi as placeholder. Tested English, French, Hindi — all return valid IPA. 7 new tests in `test_reference.py`, 13/13 pass. | ml/reference/reference_phonemes.py, tests/test_reference.py, docs/TASKS.md | R3-03 next (phoneme mapping); R2-02 unblocked
2026-11-26 | R3-04, R3-05 | Implemented weighted substitution scoring in `ml/scoring/scorer.py` giving partial credit (0.5) to phonetically similar pairs (s/ʃ, p/b, t/d, ɪ/i, etc.). Implemented `score_words` to attribute phonemes and compute per-word scores (0-100) for multi-word sentences. Built `generate_feedback` producing readable tips (e.g. "You said /s/ in 'ship'; the expected sound is /ʃ/."). Connected to `ml/pipeline.py`. 23/23 tests pass. | ml/scoring/scorer.py, ml/pipeline.py, tests/test_scorer.py, docs/TASKS.md | R4 UI tasks next

## R4 log
(empty)

## R5 log
(empty)
