# TASKS: all work, by role (single source of truth)
> AI: read ONLY the header + the section of the person's role. Statuses: `TODO`, `DOING (name)`, `DONE (date)`.
> Change only your own role's rows. Task IDs are stable: `R<role>-<nn>`. "Needs" = tasks that must be DONE first (or use the mock).

## How the AI builds a person's workflow (when someone says "I am R3, what next?" or "make my tasks")
1. Open the person's role section only. Skip DONE rows.
2. Pick the first row that is TODO whose "Needs" are DONE (or are covered by the mock, marked `mock ok`).
3. Present a single ordered workflow for that person: **Now** (this task, with steps), **Then** (next 2-3 tasks), **Hand-off**
   (who consumes the output and which function/file), **Done when** (test or demo that proves it).
4. Mark the row `DOING (name)`. When finished: mark `DONE (date)`, add one entry to the role log in `MEMORY.md`.
5. If the person has no TODO rows left in the current week, pull the next week's first row; if the role is fully done, suggest
   helping the role with the most open rows (ask the lead first).
6. If new work appears, add a row at the end of that role's table with the next ID. Never renumber.

## Parallel lanes (nobody waits: use mocks)
```
Day 1-2  R1 pushes repo + contract + mocks
Parallel R2 recognizer | R3 reference+scoring | R4 UI+Flask+DB | R5 content+data+eval+report
Sunday   R1 merges all, runs tests, updates MEMORY STATUS
```

## R1: Lead / integration
| ID | Task | Week | Needs | Status |
|---|---|---|---|---|
| R1-01 | Create GitHub repo, push scaffold, add all members, protect `main`; each member creates own `.env` from `.env.example` | W1 | - | DONE (2026-11-25) |
| R1-02 | Run README quick start, confirm mock demo works; share TASKS/GUIDELINES; 30-min kickoff | W1 | R1-01 | DONE (2026-11-25) |
| R1-03 | Set daily check-in + Sunday merge routine; confirm timeline and review date with guide, update MEMORY | W1 | - | DONE (2026-11-25) |
| R1-04 | Review/merge first PRs, keep `main` green | W2 | R1-01 | DONE (2026-11-26) |
| R1-05 | Wire real recognizer and reference into `pipeline.py` | W2 | R2-04, R3-02 | DONE (2026-11-27) |
| R1-06 | Pipeline error handling (empty audio, unsupported language, long clip, temp cleanup) | W2 | R1-05 | DONE (2026-11-27) |
| R1-07 | English end-to-end test on 10 clips; add per-stage timing logs | W3 | R1-05 | DONE (2026-11-26) |
| R1-08 | Integration freeze 28 Nov; bug fixes only | W4 | R1-07 | DONE (2026-11-26) |
| R1-09 | Record 2-min demo video; 5-7 slide review deck; update MEMORY STATUS honestly | W4 | R1-08 | DONE (2026-11-26) |
| R1-10 | (Later, Mar) Deployment: Dockerfile, hosting, env vars, load test | Mar | all Must features | TODO |

## R2: Speech model
| ID | Task | Week | Needs | Status |
|---|---|---|---|---|
| R2-01 | Learn: waveform, 16 kHz, spectrogram/MFCC, phonemes, wav2vec2 vs Whisper; run repo with mock | W1 | - | DONE (2026-11-26) |
| R2-02 | `ml/speech/audio_utils.py`: load at 16 kHz, trim silence, normalise | W1 | - | DONE (2026-11-26) |
| R2-03 | Try Whisper tiny/base on 5 own recordings; note speed + accuracy | W1 | R2-02 | TODO |
| R2-04 | Real `recognize_phonemes` for English with a pretrained phoneme model on CPU; mock stays as fallback (`USE_MOCK_ML=1`) | W2 | R2-02 | DONE (2026-11-27) |
| R2-05 | Compare candidate models on speed/accuracy; record result in PRD section 9 | W2 | R2-04 | TODO |
| R2-06 | Robustness: noise, short clips, silence, different mics; load model once and cache on CPU | W3 | R2-04 | DONE (2026-11-27) |
| R2-07 | Try French; report what works | W3 | R2-04 | TODO |
| R2-08 | Hand final English recognizer to R1; document models and how to run; write report section with R5 | W4 | R2-06 | DONE (2026-11-28) |
| R2-09 | (Dec+) Hindi, French; Sanskrit approach with R3; optional fine-tune on Colab/Kaggle; speed tuning | Dec-Feb | R2-08 | TODO |

## R3: Reference phonemes + scoring
| ID | Task | Week | Needs | Status |
|---|---|---|---|---|
| R3-01 | Learn IPA, G2P, edit distance; read `ml/scoring/scorer.py`; install espeak-ng + phonemizer | W1 | - | DONE (2026-11-26) |
| R3-02 | Real `get_reference_phonemes` for English (phonemizer+espeak-ng); check French and Hindi | W2 | R3-01 | DONE (2026-11-26) |
| R3-03 | Phoneme symbol mapping between recognizer and reference; document in `ml/reference/PHONEME_MAP.md` | W2 | R3-02, R2-04 (mock ok) | DONE (2026-11-27) |
| R3-04 | Weighted scoring (similar sounds cost less), per-word scores, overall 0-100 | W3 | R3-03 | DONE (2026-11-26) |
| R3-05 | Readable feedback text ("You said /s/, expected /ʃ/") | W3 | R3-04 | DONE (2026-11-26) |
| R3-06 | Compare scores with speechocean762 human scores with R5 (correlation) | W3 | R3-04, R5-06 | TODO |
| R3-07 | Freeze English scoring, edge-case tests (empty, extra, missing); write scoring section for report | W4 | R3-05 | DONE (2026-11-28) |
| R3-08 | (Dec+) Hindi/French rules; Sanskrit rule-based G2P (Jan); optional learned scorer; feedback wording | Dec-Feb | R3-07 | TODO |

## R4: App / UI
| ID | Task | Week | Needs | Status |
|---|---|---|---|---|
| R4-01 | Learn Flask routes/templates, `MediaRecorder`, fetch/FormData, SQLite; run starter app on mock | W1 | - | DONE (2026-11-27) |
| R4-02 | Sketch screens: practice, results, dashboard | W1 | - | DONE (2026-11-27) |
| R4-03 | Practice page: language dropdown, word list from `/api/content/<language>`, reference audio playback | W2 | R4-01 | DONE (2026-11-27) |
| R4-04 | Browser recording to `/api/assess` with loading state; client-side WAV encoding in JavaScript | W2 | R4-03 | DONE (2026-11-27) |
| R4-05 | Results view: overall score, per-word score, wrong sounds in red, feedback text | W3 | R4-04 | DONE (2026-11-27) |
| R4-06 | Save every attempt in SQLite; basic history list | W3 | R4-04 | DONE (2026-11-27) |
| R4-07 | Mobile-friendly layout; errors (mic blocked, empty recording); API tests | W4 | R4-05 | DONE (2026-11-27) |
| R4-08 | Progress dashboard with canvas charts; modular client JS; 404 page; full design system port | W4 | R4-06 | DONE (2026-11-28) |
| R4-09 | (Dec+) Practice activities, levels, daily set; optional login; polish | Dec-Feb | R4-08 | TODO |

## R5: Data, evaluation, report
| ID | Task | Week | Needs | Status |
|---|---|---|---|---|
| R5-01 | Read PRD; start literature survey list (10 papers/tools on pronunciation assessment, wav2vec2, Whisper) | W1 | - | DONE (2026-11-26) |
| R5-02 | Verify datasets + licenses (speechocean762, L2-ARCTIC, Common Voice; Sanskrit availability); record in PRD section 5 | W1 | - | DONE (2026-11-26) |
| R5-03 | Word lists in `data/content/*.json`, 20+ items per language, 4 languages | W1 | - | DONE (2026-11-26) |
| R5-04 | `scripts/download_data.md` with download steps (data never committed) | W1 | R5-02 | DONE (2026-11-26) |
| R5-05 | Levels (beginner/intermediate/advanced); 20-30 own labelled test recordings stored outside Git | W2 | R5-03 | DONE (2026-11-26) |
| R5-06 | `evaluation/evaluate_scoring.py`: correlation with human scores, per-phoneme accuracy | W3 | R5-05 | TODO |
| R5-07 | Report outline (Intro, Literature, Requirements, Design, Implementation, Evaluation, Conclusion) | W2 | R5-01 | DONE (2026-11-26) |
| R5-08 | User testing protocol with 5-10 people + short feedback form | W4 | R1-07 | DONE (2026-11-26) |
| R5-09 | Report draft in `docs/report/` with architecture + flow diagrams | W4 | R5-07 | DONE (2026-11-26) |
| R5-10 | (Dec+) Grow lists to 100+ per language; full evaluation per language (Feb); record Sanskrit reference clips; final report | Dec-Apr | R5-09 | TODO |
