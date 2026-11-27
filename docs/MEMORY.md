# MEMORY: what has been done (AI reads this to resume; AI writes here when a task is finished)
> Read the STATUS block + only your own role's section. Do not read the whole file. Keep every entry to 3-5 lines.
> Format of an entry: `YYYY-MM-DD | task ID | what was done | files touched | next / blockers`

## STATUS (R1 only edits this block)
- Phase: November Milestone Review (30-40% progress checkpoint). Completion: ~35%.
  Reason: System architecture, decoupled ML pipeline contracts, audio preprocessing (16 kHz, silence trimming, normalisation), real eSpeak NG IPA reference generation, weighted phonetic similarity scoring, multi-word attribution, per-stage timing telemetry, 4-language practice curricula (88+ items), automated smoke test suite, literature survey, 2-minute demo script, 7-slide review deck, and user testing protocol are completed and verified with 24 passing tests.
- Works now:
  - Audio preprocessing (`ml/speech/audio_utils.py`): 16 kHz resample, mono mix, top_db=30 silence trim, peak normalisation.
  - Reference phonemes (`ml/reference/reference_phonemes.py`): Real IPA extraction via phonemizer + eSpeak NG (en-us, fr-fr, hi).
  - Scoring & feedback (`ml/scoring/scorer.py`): Weighted substitution costs (0.5 credit for voicing/sibilant/vowel near-misses), per-word attribution, actionable advice ("You said /s/ in 'ship'; expected /ʃ/").
  - Pipeline telemetry (`ml/pipeline.py`): Per-stage timing logs at INFO level and `timing` dictionary (`reference_sec`, `recognizer_sec`, `scoring_sec`, `total_sec`) returned in `/api/assess`.
  - Smoke testing (`evaluation/smoke_test.py`): CLI automated pipeline evaluation across local .wav audio clips.
  - Curricula: 22+ items across 3 tiers (beginner, intermediate, advanced) in `data/content/` for English, Hindi, Sanskrit, French.
  - Documentation: `docs/report/` containing `report_outline.md`, `architecture.md` (Mermaid diagrams), `literature_survey.md` (10 topics [TO VERIFY]), `demo_script.md` (2-minute script), `review_slides.md` (7 slides), and `user_testing.md` (survey & testing script).
- What is mock or fallback:
  - Speech recognizer (`ml/speech/recognizer.py`): Mock phoneme emission is active fallback (`USE_MOCK_ML=1`) pending neural model integration.
  - Sanskrit reference: Temporary fallback mapping to Hindi eSpeak G2P; custom rule-based G2P planned for January.
  - Web UI frontend: Interactive practice page with in-browser AudioContext 16 kHz WAV encoding is next in queue (R4-03, R4-04).
- Known problems:
  - Sanskrit lacks off-the-shelf acoustic models and corpora; empirical recordings and rule-based phonetic decomposition required.
  - Neural models (wav2vec 2.0 / Whisper) must be evaluated for CPU RAM and latency constraints on consumer laptops.
- Next three tasks after review:
  1. R4-03 + R4-04: Practice web UI (in-browser 16 kHz mono WAV conversion, speech synthesis audio playback, assess loading state).
  2. R2-04: Real English phoneme recognizer using pretrained wav2vec 2.0 on CPU with singleton model caching.
  3. R3-03: Phoneme symbol mapping between recognizer output and eSpeak reference in `ml/reference/PHONEME_MAP.md`.

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
2026-11-26 | R1-07, R1-08, R1-09 | Added stage timing telemetry (reference_sec, recognizer_sec, scoring_sec, total_sec) at INFO level and in /api/assess timing response. Pinned requirements.txt and audited .gitignore (models, data/raw, .cache). Rebuilt clean UTF-8 README.md. Authored 2-min demo script (`docs/report/demo_script.md`), 7-slide review deck (`docs/report/review_slides.md`), and updated STATUS for 35% review checkpoint. 24/24 tests pass. | ml/contracts.py, ml/pipeline.py, README.md, requirements.txt, .gitignore, docs/report/*, docs/TASKS.md, docs/MEMORY.md | R4 UI tasks next (R4-03, R4-04)

## R2 log
2026-11-26 | R2-01, R2-02 | Built `ml/speech/audio_utils.py` with `load_audio` (16 kHz mono conversion via soundfile + librosa resample), `trim_silence` (librosa top_db=30), and `normalise` (peak scaling). Created `scripts/record_clip.py` to record mic clips into data/raw/ using sounddevice. Added comprehensive unit tests with synthetic sine waves in `tests/test_audio_utils.py`, all 20 project tests pass. | ml/speech/audio_utils.py, scripts/record_clip.py, tests/test_audio_utils.py, docs/TASKS.md | R2-04 next: real English phoneme recognizer
2026-11-27 | R2-04 | Implemented real recognizer in `ml/speech/recognizer.py` using wav2vec 2.0 (facebook/wav2vec2-lv-60-espeak-cv-ft, ~1.18 GB) on CPU with singleton model caching. Raises clear RuntimeError on failure when USE_MOCK_ML=0 (never silently falls back to mock). Marked DOING until tested on real mic clips. | ml/speech/recognizer.py, tests/test_recognizer.py, docs/TASKS.md | Verify on live microphone clips (ship / sip)

## R3 log
2026-11-26 | R3-01, R3-02 | Installed espeak-ng (Windows MSI) + phonemizer pip package. Rewrote `get_reference_phonemes` to call phonemizer with espeak backend for real IPA output (e.g. "hello" → `h ə l oʊ`). Mock fallback preserved via `USE_MOCK_ML=1`. Added `_LANG_MAP` for en-us, hi, fr-fr; Sanskrit mapped to hi as placeholder. Tested English, French, Hindi — all return valid IPA. 7 new tests in `test_reference.py`, 13/13 pass. | ml/reference/reference_phonemes.py, tests/test_reference.py, docs/TASKS.md | R3-03 next (phoneme mapping); R2-02 unblocked
2026-11-26 | R3-04, R3-05 | Implemented weighted substitution scoring in `ml/scoring/scorer.py` giving partial credit (0.5) to phonetically similar pairs (s/ʃ, p/b, t/d, ɪ/i, etc.). Implemented `score_words` to attribute phonemes and compute per-word scores (0-100) for multi-word sentences. Built `generate_feedback` producing readable tips (e.g. "You said /s/ in 'ship'; the expected sound is /ʃ/."). Connected to `ml/pipeline.py`. 23/23 tests pass. | ml/scoring/scorer.py, ml/pipeline.py, tests/test_scorer.py, docs/TASKS.md | R4 UI tasks next
2026-11-27 | R3-03 | Built symbol normalizer `ml/reference/phoneme_map.py` and documented rules in `ml/reference/PHONEME_MAP.md`: vowel length binding (iː), atomic diphthongs (oʊ, aɪ, eɪ), stress mark stripping, and American flap /ɾ/ scoring (0.5 similarity with t/d). Optimized eSpeak backend with persistent singleton + word LRU caching (dropping latency from 3.8s to <1ms). Updated feedback to output "not detected" when >70% sounds fail. | ml/reference/phoneme_map.py, ml/reference/PHONEME_MAP.md, ml/reference/reference_phonemes.py, ml/scoring/scorer.py, tests/test_phoneme_map.py | Complete R2-04 live evaluation

## R4 log
2026-11-27 | R4-01, R4-03, R4-04 | Implemented client-side audio conversion in `app/static/js/app.js` (Web Audio API decode + OfflineAudioContext resample to 16 kHz mono 16-bit PCM WAV) eliminating server ffmpeg dependencies. Hardened `app/routes/practice.py` with RIFF/WAVE signature check, 15-second cap, and guaranteed temp file deletion via try/finally. Wrapped pipeline errors in JSON 500 responses with UI error banner. Added 4 API tests in `tests/test_api.py`, 37/37 tests pass. | app/routes/practice.py, app/static/js/app.js, app/templates/index.html, tests/test_api.py, docs/TASKS.md | R4-05, R4-06 (results view & history list)
2026-11-27 | R4-02, R4-05, R4-06, R4-07 | Built full modern responsive UI in `index.html` and `style.css` (centered card, soft gradients, dark mode support via prefers-color-scheme, reduced-motion compliance). Added 4-stage flow (Ready -> Listening -> Checking -> Result) with live Web Audio waveform, smoothed volume bar, 10s auto-stop circular progress ring, and quiet warning. Built animated circular score ring, per-word cards with IPA sound chips (green correct, red wrong), coaching feedback list, and SQLite history table from /api/progress. 37/37 tests pass. | app/templates/index.html, app/static/css/style.css, app/static/js/app.js, docs/TASKS.md, docs/MEMORY.md | R4 tasks complete; verify live mic recording with R2-04

## R5 log
2026-11-26 | R5-01, R5-02, R5-03, R5-04, R5-05, R5-07, R5-08, R5-09 | Populated 22+ items across beginner/intermediate/advanced levels for English, Hindi, Sanskrit, French in `data/content/*.json` with native-speaker verification notes. Created `docs/report/report_outline.md` and `docs/report/architecture.md` (with system and sequence Mermaid diagrams). Compiled 10-topic literature review in `docs/report/literature_survey.md` marked [TO VERIFY]. Documented evaluation datasets in PRD Section 5 and `scripts/download_data.md`. Built `evaluation/smoke_test.py` and created `docs/report/user_testing.md` (6-question survey & 5-min protocol). | data/content/*.json, docs/report/*, docs/PRD.md, scripts/download_data.md, evaluation/smoke_test.py, tests/test_content.py | R4 UI tasks next (R4-03, R4-04)
