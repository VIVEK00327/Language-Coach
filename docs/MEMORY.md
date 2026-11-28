# MEMORY: what has been done (AI reads this to resume; AI writes here when a task is finished)
> Read the STATUS block + only your own role's section. Do not read the whole file. Keep every entry to 3-5 lines.
> Format of an entry: `YYYY-MM-DD | task ID | what was done | files touched | next / blockers`

## STATUS (R1 only edits this block)
- Phase: November Milestone Review (35-40% progress checkpoint). Completion: ~40%.
  Reason: Complete end-to-end decoupled system functional locally on CPU. Audio preprocessing (16 kHz, silence trimming, peak normalisation), in-browser WAV conversion via AudioContext, real eSpeak NG IPA reference extraction, real wav2vec 2.0 acoustic phone decoder with CPU singleton caching, weighted phonetic similarity scoring, per-word attribution, per-stage timing telemetry, 4-language curricula (88+ items), responsive glassmorphic UI across all views with instant light/dark theme switcher, progress dashboard with canvas trend chart, setup doctor script, and comprehensive documentation portal. Verified with 40/40 passing unit tests.
- Works now:
  - Audio preprocessing (`ml/speech/audio_utils.py`): 16 kHz resample, mono mix, top_db=30 silence trim, peak normalisation.
  - In-browser WAV encoder (`app/static/js/wav.js`): Browser AudioContext decodes and resamples audio to 16 kHz mono 16-bit PCM WAV before upload.
  - Reference phonemes (`ml/reference/reference_phonemes.py`): Real IPA extraction via phonemizer + eSpeak NG (en-us, fr-fr, hi) with LRU word caching.
  - Speech recognizer (`ml/speech/recognizer.py`): Real wav2vec 2.0 (`facebook/wav2vec2-lv-60-espeak-cv-ft`) on CPU with singleton model caching.
  - Scoring & feedback (`ml/scoring/scorer.py`): Weighted substitution matrix (0.5 credit for similar pairs), per-word attribution, actionable tips.
  - Symbol normalizer (`ml/reference/phoneme_map.py`): Harmonized IPA representation (vowel lengths, atomic diphthongs, stress stripping).
  - Pipeline telemetry (`ml/pipeline.py`): Per-stage timing logs (`reference_sec`, `recognizer_sec`, `scoring_sec`, `total_sec`).
  - Web UI frontend: Full glassmorphic SaaS design ported across Home (`/`), Practice (`/practice`), Progress (`/progress`), and `404.html`.
  - Diagnostics: `scripts/check_setup.py` cross-platform environment doctor tool.
- What is mock or fallback:
  - Speech recognizer mock fallback: Active only when `USE_MOCK_ML=1` is set in `.env`.
  - Sanskrit reference: Temporary fallback mapping to Hindi eSpeak G2P; custom deterministic rule-based G2P planned for January.
- Known problems:
  - Sanskrit lacks commercial ASR models and corpora; empirical recordings and rule-based phonetic decomposition required.
  - First inference on real acoustic model downloads ~1.18 GB model weights from Hugging Face (subsequent runs use local CPU cache).
- Next three tasks after review:
  1. R2-07 / R2-09: Evaluate French and Hindi speech recognition accuracy on local mic test clips.
  2. R3-06: Benchmark scoring correlation against speechocean762 human pronunciation grades with R5.
  3. R3-08: Begin deterministic rule-based Devanagari G2P for classical Sanskrit.

### Daily check-in (post in group chat by 10 pm)
```
Done: (what you finished today)
Doing: (what you will work on next)
Blocked: (anything stopping you — tag the person)
```

### Sunday merge checklist (R1)
1. `git checkout main && git pull`
2. Merge each role branch; resolve conflicts with the author.
3. Run `python -m pytest tests` (all must pass).
4. Run `python scripts/check_setup.py` (confirm all checks pass).
5. Run `python run.py` (verify localhost:5000 in browser).
6. Update STATUS block above (phase, completion %, what works, what doesn't).

## R1 log
2026-11-04 | SETUP | repo scaffold, docs, contract, mock pipeline, tests | whole repo | each role starts its Week 1 tasks in TASKS.md
2026-11-25 | R1-01, R1-02 | Repo created and pushed to GitHub. Installed deps, ran pytest (6/6 pass). Started app with USE_MOCK_ML=1, verified GET /api/languages (4 langs), GET /api/content/english (3 beginner words), POST /api/assess with text=hello+language=english returns per-phoneme scores and feedback. Mock pipeline confirmed end to end. | docs/TASKS.md, docs/MEMORY.md | R1-03: set daily check-in + Sunday merge; all roles start W1 tasks
2026-11-25 | R1-03 | Drafted team routine: daily check-in template (done/doing/blocked), Sunday merge checklist (6 steps: pull, merge, pytest, smoke-test, update STATUS, post summary), and 3 questions for guide (end date, review date, review deliverables). All saved under STATUS in MEMORY.md. | docs/MEMORY.md, docs/TASKS.md | R1-04: review/merge first PRs; ask guide the 3 questions
2026-11-26 | R1-07, R1-08, R1-09 | Added stage timing telemetry (reference_sec, recognizer_sec, scoring_sec, total_sec) at INFO level and in /api/assess timing response. Pinned requirements.txt and audited .gitignore (models, data/raw, .cache). Rebuilt clean UTF-8 README.md. Authored 2-min demo script (`docs/report/demo_script.md`), 7-slide review deck (`docs/report/review_slides.md`), and updated STATUS for 35% review checkpoint. 24/24 tests pass. | ml/contracts.py, ml/pipeline.py, README.md, requirements.txt, .gitignore, docs/report/*, docs/TASKS.md, docs/MEMORY.md | R4 UI tasks next (R4-03, R4-04)
2026-11-28 | R1-05, R1-06 | Hardened pipeline integration and error handling. Verified temporary WAV deletion under try/finally and duration cap. Created cross-platform environment diagnostic doctor `scripts/check_setup.py` with passing unit test. Restructured master documentation portal in `docs/README.md`. 40/40 tests pass. | scripts/check_setup.py, tests/test_check_setup.py, docs/README.md, docs/TASKS.md, docs/MEMORY.md | Step 3 verification & mentor presentation

## R2 log
2026-11-26 | R2-01, R2-02 | Built `ml/speech/audio_utils.py` with `load_audio` (16 kHz mono conversion via soundfile + librosa resample), `trim_silence` (librosa top_db=30), and `normalise` (peak scaling). Created `scripts/record_clip.py` to record mic clips into data/raw/ using sounddevice. Added comprehensive unit tests with synthetic sine waves in `tests/test_audio_utils.py`, all 20 project tests pass. | ml/speech/audio_utils.py, scripts/record_clip.py, tests/test_audio_utils.py, docs/TASKS.md | R2-04 next: real English phoneme recognizer
2026-11-27 | R2-04, R2-06 | Implemented real recognizer in `ml/speech/recognizer.py` using wav2vec 2.0 (facebook/wav2vec2-lv-60-espeak-cv-ft, ~1.18 GB) on CPU with singleton model caching. Raises clear RuntimeError on failure when USE_MOCK_ML=0 (never silently falls back to mock). Tested on synthetic audio and real clips. | ml/speech/recognizer.py, tests/test_recognizer.py, docs/TASKS.md | R2-07 French evaluation
2026-11-28 | R2-08 | Documented model architecture, memory singleton caching, CPU latency performance, and download requirements in `docs/project/ARCHITECTURE.md` and `docs/setup/SETUP.md`. | docs/project/ARCHITECTURE.md, docs/setup/SETUP.md, docs/TASKS.md | R2-09 French/Hindi testing

## R3 log
2026-11-26 | R3-01, R3-02 | Installed espeak-ng (Windows MSI) + phonemizer pip package. Rewrote `get_reference_phonemes` to call phonemizer with espeak backend for real IPA output (e.g. "hello" → `h ə l oʊ`). Mock fallback preserved via `USE_MOCK_ML=1`. Added `_LANG_MAP` for en-us, hi, fr-fr; Sanskrit mapped to hi as placeholder. Tested English, French, Hindi — all return valid IPA. 7 new tests in `test_reference.py`, 13/13 pass. | ml/reference/reference_phonemes.py, tests/test_reference.py, docs/TASKS.md | R3-03 next (phoneme mapping); R2-02 unblocked
2026-11-26 | R3-04, R3-05 | Implemented weighted substitution scoring in `ml/scoring/scorer.py` giving partial credit (0.5) to phonetically similar pairs (s/ʃ, p/b, t/d, ɪ/i, etc.). Implemented `score_words` to attribute phonemes and compute per-word scores (0-100) for multi-word sentences. Built `generate_feedback` producing readable tips (e.g. "You said /s/ in 'ship'; the expected sound is /ʃ/."). Connected to `ml/pipeline.py`. 23/23 tests pass. | ml/scoring/scorer.py, ml/pipeline.py, tests/test_scorer.py, docs/TASKS.md | R4 UI tasks next
2026-11-27 | R3-03 | Built symbol normalizer `ml/reference/phoneme_map.py` and documented rules in `ml/reference/PHONEME_MAP.md`: vowel length binding (iː), atomic diphthongs (oʊ, aɪ, eɪ), stress mark stripping, and American flap /ɾ/ scoring (0.5 similarity with t/d). Optimized eSpeak backend with persistent singleton + word LRU caching (dropping latency from 3.8s to <1ms). Updated feedback to output "not detected" when >70% sounds fail. | ml/reference/phoneme_map.py, ml/reference/PHONEME_MAP.md, ml/reference/reference_phonemes.py, ml/scoring/scorer.py, tests/test_phoneme_map.py | Complete R2-04 live evaluation
2026-11-28 | R3-07 | Froze English phoneme reference extraction and weighted scoring engine. Documented mathematical edit-distance formulation and similarity weight matrix in `docs/project/ARCHITECTURE.md`. | ml/scoring/scorer.py, docs/project/ARCHITECTURE.md, docs/TASKS.md | R3-06 speechocean762 correlation

## R4 log
2026-11-27 | R4-01, R4-03, R4-04 | Implemented client-side audio conversion in `app/static/js/app.js` (Web Audio API decode + OfflineAudioContext resample to 16 kHz mono 16-bit PCM WAV) eliminating server ffmpeg dependencies. Hardened `app/routes/practice.py` with RIFF/WAVE signature check, 15-second cap, and guaranteed temp file deletion via try/finally. Wrapped pipeline errors in JSON 500 responses with UI error banner. Added 4 API tests in `tests/test_api.py`, 37/37 tests pass. | app/routes/practice.py, app/static/js/app.js, app/templates/index.html, tests/test_api.py, docs/TASKS.md | R4-05, R4-06 (results view & history list)
2026-11-27 | R4-02, R4-05, R4-06, R4-07 | Built full modern responsive UI in `index.html` and `style.css` (centered card, soft gradients, dark mode support via prefers-color-scheme, reduced-motion compliance). Added 4-stage flow (Ready -> Listening -> Checking -> Result) with live Web Audio waveform, smoothed volume bar, 10s auto-stop circular progress ring, and quiet warning. Built animated circular score ring, per-word cards with IPA sound chips (green correct, red wrong), coaching feedback list, and SQLite history table from /api/progress. 37/37 tests pass. | app/templates/index.html, app/static/css/style.css, app/static/js/app.js, docs/TASKS.md, docs/MEMORY.md | R4 tasks complete; verify live mic recording with R2-04
2026-11-28 | R4-08 | Ported glassmorphic SaaS design across all pages (Home, Practice, Progress, 404). Split JS into modular files (theme.js, wav.js, waveform.js, practice.js, progress.js). Implemented canvas score trend line chart, pre-paint theme script, and accessible dark/light switcher. All 40 tests pass. | app/templates/*, app/static/css/style.css, app/static/js/*, tests/test_api.py, docs/TASKS.md | R4-09 practice activities polish

## R5 log
2026-11-26 | R5-01, R5-02, R5-03, R5-04, R5-05, R5-07, R5-08, R5-09 | Populated 22+ items across beginner/intermediate/advanced levels for English, Hindi, Sanskrit, French in `data/content/*.json` with native-speaker verification notes. Created `docs/report/report_outline.md` and `docs/report/architecture.md` (with system and sequence Mermaid diagrams). Compiled 10-topic literature review in `docs/report/literature_survey.md` marked [TO VERIFY]. Documented evaluation datasets in PRD Section 5 and `scripts/download_data.md`. Built `evaluation/smoke_test.py` and created `docs/report/user_testing.md` (6-question survey & 5-min protocol). | data/content/*.json, docs/report/*, docs/PRD.md, scripts/download_data.md, evaluation/smoke_test.py, tests/test_content.py | R4 UI tasks next (R4-03, R4-04)
2026-11-28 | R5-07, R5-08 | Reorganized documentation suite: authored `docs/project/OVERVIEW.md`, `docs/project/PROGRESS_REPORT.md`, `docs/project/DEMO_GUIDE.md`, and `docs/team/TEAM_GUIDE.md`. Preserved literature survey and testing protocols in `docs/report/`. Created screenshot registry in `docs/assets/`. | docs/project/*, docs/team/*, docs/assets/*, docs/TASKS.md | R5-06 scoring evaluation
