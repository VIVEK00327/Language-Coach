# Language Coach — Progress Report & Milestone Evaluation

> **Formal Milestone:** 30–40% Progress Checkpoint (November 2026)  
> **Evaluation Period:** November 2026 – April 2027 (6 Months Academic Schedule)  

---

## 1. Feature Completion Status

| Feature ID | Feature Description | Priority | Current Status | Implemented In |
|---|---|---|---|---|
| **F1** | Language selection (English, Hindi, Sanskrit, French) | Must | **DONE** | `app/routes/practice.py`, `app/templates/practice.html` |
| **F2** | Select word/sentence from tiered curriculum lists | Must | **DONE** | `data/content/*.json`, `app/static/js/practice.js` |
| **F3** | Reference audio playback via Web Speech Synthesis | Must | **DONE** | `app/static/js/practice.js` |
| **F4** | In-browser mic recording, live waveform, 16 kHz WAV encoding | Must | **DONE** | `app/static/js/wav.js`, `app/static/js/waveform.js` |
| **F5** | Overall score (0–100), per-word score, per-sound correct/incorrect | Must | **DONE** | `ml/scoring/scorer.py`, `ml/pipeline.py` |
| **F6** | Readable diagnostic feedback ("You said /s/, expected /ʃ/") | Must | **DONE** | `ml/scoring/scorer.py`, `app/templates/practice.html` |
| **F7** | Attempt history persistence in local SQLite database | Must | **DONE** | `app/db.py`, `app/routes/practice.py` |
| **F8** | Learner progress dashboard with HTML5 canvas trend chart | Should | **DONE** | `app/templates/progress.html`, `app/static/js/progress.js` |
| **F9** | Curriculum levels (beginner, intermediate, advanced) | Should | **DONE** | `data/content/*.json` (22+ items per language) |
| **F10** | Multi-user authentication & learner accounts | Could | *Not Started (Planned)* | Scheduled for Spring Phase |
| **F11** | Extended LLM-generated coaching explanations | Could | *Not Started (Planned)* | Optional Phase 2 deliverable |
| **F12** | Expanded language coverage (German, Spanish, Latin) | Could | *Not Started (Planned)* | Future roadmap |

---

## 2. Quantitative Progress Assessment

To provide an honest, mathematical completion estimate for academic mentors, progress is calculated by weighting functional subsystems by engineering effort:

$$\text{Total Completion} = \sum (\text{Component Weight} \times \text{Component Completion})$$

| Subsystem Component | Weight | Completion % | Weighted Contribution | Verification Evidence |
|---|---|---|---|---|
| **Project Setup & Architecture Contracts** | 10% | 100% | 10.0% | `ml/contracts.py`, `run.py`, clean CI test runner |
| **Audio Preprocessing & In-Browser WAV** | 15% | 100% | 15.0% | `ml/speech/audio_utils.py`, `app/static/js/wav.js` |
| **Reference Phoneme Engine (eSpeak G2P)** | 15% | 85% | 12.75% | Real IPA for English/French/Hindi; Sanskrit proxy |
| **Speech Recognizer (wav2vec 2.0 on CPU)** | 25% | 75% | 18.75% | Real English model cached on CPU; French/Hindi in progress |
| **Weighted Scorer & Multi-Word Attribution** | 15% | 95% | 14.25% | Similarity matrix, sound chips, word scores |
| **Web Frontend & Dashboard UI** | 10% | 100% | 10.0% | Glassmorphic pages (`/`, `/practice`, `/progress`, `404`) |
| **Empirical Evaluation & Human Correlation** | 10% | 20% | 2.0% | Volunteer test protocol ready; formal trials pending |
| **Total Progress Estimate** | **100%** | — | **~82.75% of Phase 1 / ~40% of Final Project** | **40 automated tests passing (100%)** |

---

## 3. Real vs. Mock Subsystem Truth Table

| Subsystem | What Is Real in Code Today | What Is Mock or Temporary Fallback |
|---|---|---|
| **Audio Processing** | 100% real: Web Audio API decodes audio blob, resamples to 16 kHz mono 16-bit PCM in browser; server trims silence with librosa and normalizes peak amplitude. | None. Server-side ffmpeg dependency completely eliminated. |
| **Reference Phonemes** | 100% real: eSpeak NG extracts true IPA via `phonemizer` for English, French, and Hindi. LRU cached. | Sanskrit references temporarily map to Hindi eSpeak G2P until rule-based Sanskrit decomposition is built. Mock character splitter used only when `USE_MOCK_ML=1`. |
| **Speech Recognizer** | Real English acoustic decoding via Hugging Face `facebook/wav2vec2-lv-60-espeak-cv-ft` running locally on CPU with singleton model caching. | Simulated static phonemes returned only when explicitly toggled via `USE_MOCK_ML=1`. French and Hindi acoustic fine-tuning planned for January. |
| **Scoring Engine** | 100% real: Dynamic programming alignment using weighted substitution costs ($0.5$ credit for similar pairs like `/s/` & `/ʃ/`, `/t/` & `/d/`, `/p/` & `/b/`). | Optional learned regression calibrator (scikit-learn) planned for February evaluation phase. |
| **Web UI & Database** | 100% real: Responsive glassmorphic layout, live Web Audio waveform, circular timer, animated score ring, SQLite database, and canvas score chart. | None. Fully functional on localhost. |

---

## 4. Risks & Mitigations

| Identified Risk | Severity | Real-World Impact | Engineering Mitigation |
|---|---|---|---|
| **Sanskrit Corpus Scarcity** | **High** | Off-the-shelf ASR models and phoneme datasets for classical Sanskrit are virtually non-existent. | Sanskrit spelling in Devanagari is almost 100% phonetically regular. We are developing a deterministic rule-based G2P algorithm (handling visarga, anusvara, and vowel lengths) and recording native Sanskrit teachers for validation. |
| **CPU Latency on Laptops** | **Medium** | Large neural models (like Whisper large or wav2vec XLSR) can take 10+ seconds per clip on dual-core CPUs. | We selected `wav2vec2-lv-60-espeak-cv-ft` (~1.18 GB), initialize it once as a memory singleton, and keep audio clips strictly under 10 seconds. Execution takes ~0.5–1.5s on modern quad-core CPUs. |
| **Microphone Variation** | **Low** | Different hardware mics produce clipping, low volume, or background noise. | Server-side `audio_utils.py` applies top-db=30 silence trimming and peak amplitude normalization to scale all signals to a standard $[-1.0, 1.0]$ range. Client UI alerts users if speech is too quiet. |

---

## 5. Development Timeline (November 2026 – April 2027)

```text
[Nov 2026] Architecture, Decoupled ML Pipeline, Mock UI, Real eSpeak Reference, wav2vec2 CPU Recognizer (35-40% DONE)
   │
[Dec 2026] French & Hindi Recognition Testing, speechocean762 Benchmark Correlation (50% Milestone)
   │
[Jan 2027] Deterministic Sanskrit Rule-Based G2P Engine, Sound Mapping Optimization (65% Milestone)
   │
[Feb 2027] Comprehensive User Testing (15-20 Volunteers), Evaluation Metrics & Accuracy Tables (80% Milestone)
   │
[Mar 2027] Performance Profiling, Multi-User Auth, Packaging & Containerization (90% Milestone)
   │
[Apr 2027] Final Project Thesis, Mentor Demonstration, and University Viva Presentation (100% Final Deliverable)
```
