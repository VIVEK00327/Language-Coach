# Review Presentation Slides: Language Coach
**Project:** Language Coach — AI-Based Multilingual Pronunciation Learning System  
**Team:** 5 Members (B.Tech CSE, Session 2026-27)  
**Milestone:** 30–40% Progress Review (November 2026)

---

### Slide 1: Title & Overview
- **Header:** Language Coach: Multilingual Pronunciation Learning System
- **Subtitle:** AI-Driven Phonetic Feedback for Modern and Classical Languages
- **Team Roles:**
  - R1: Lead / System Integration
  - R2: Speech Modeling & Audio Preprocessing
  - R3: Reference Phonemes & Weighted Scoring
  - R4: Web Application & Practice Interface
  - R5: Dataset Curation, Evaluation & Documentation
- **Core Goal:** Provide immediate, phoneme-level diagnostic feedback on standard CPU hardware without external GPU dependencies.

---

### Slide 2: Problem Statement & Motivation
- **The Challenge:** Conventional language learning applications focus on vocabulary recall or phrase-level matching using standard ASR. Learners receive binary pass/fail grades without knowing *which specific sound* was mispronounced.
- **Why Phoneme-Level Feedback Matters:**
  - Learners frequently transfer mother-tongue phonology (e.g., confusing `/s/` and `/ʃ/`, or confusing dental and retroflex plosives).
  - Fine-grained diagnostic advice empowers targeted pronunciation correction.
- **Target Languages:** English, Hindi, Sanskrit, and French.

---

### Slide 3: Approach & System Architecture
- **Decoupled Architecture:** Clean separation of concerns between Flask HTTP routes and standalone ML processing modules (`ml/`).
- **Pipeline Dataflow (Reference: `docs/report/architecture.md`):**
  1. **Audio Ingestion:** In-browser 16 kHz mono WAV conversion, server-side silence trimming, and peak normalisation.
  2. **Grapheme-to-Phoneme (G2P):** Expected IPA sequence generation via `phonemizer` and eSpeak NG.
  3. **Acoustic Recognition:** Extraction of spoken phoneme sequences.
  4. **Weighted Sequence Alignment:** Dynamic programming alignment awarding partial credit ($0.5$) for phonetically similar sound pairs (e.g., voicing and place near-misses).
  5. **Attribution & Diagnostic Feedback:** Segmenting scores per word and generating readable advice.

---

### Slide 4: Current Progress & Accomplishments (November Milestone)
- **Integration & Tooling (R1):**
  - Scaffold, testing infrastructure, and end-to-end pipeline glue with per-stage timing metrics (`reference`, `recognizer`, `scoring`).
  - Automated smoke test runner (`evaluation/smoke_test.py`) operating on local audio.
- **Audio Preprocessing (R2):**
  - `ml/speech/audio_utils.py`: 16 kHz resampler, stereo downmixer, top-dB silence trimmer, and peak normaliser.
  - Recording utility (`scripts/record_clip.py`).
- **Phonetics & Scoring Engine (R3):**
  - Real IPA reference extraction for English, French, and Hindi via eSpeak NG.
  - Weighted similarity scoring matrix and multi-word attribution engine.
- **Curricula & Benchmarks (R5):**
  - 88+ curated practice items across English, Hindi, Sanskrit, and French with 3 difficulty tiers.
  - Architecture specifications, literature review, and 5-minute volunteer testing protocol.
- **Validation:** 23/23 unit tests passing in under 3 seconds on CPU.

---

### Slide 5: Live System Demonstration
- **Demonstration Walkthrough (2-Minute Protocol):**
  - Input sample: English target text *"ship"*.
  - Execution of `ml.pipeline.assess` on local sample WAV.
  - Terminal / API output highlighting:
    - Overall score: $83.3\%$
    - Spoken phoneme `/s/` aligned against expected phoneme `/ʃ/`
    - Actionable feedback generated: *"You said /s/ in 'ship'; the expected sound is /ʃ/."*
    - Stage latency telemetry: `<0.5 s` total pipeline execution time on CPU.

---

### Slide 6: Sanskrit Strategy & Technical Risk Management
- **The Sanskrit Challenge:** Off-the-shelf ASR models and labeled non-native acoustic corpora for Sanskrit are nonexistent.
- **Honest Engineering Approach:**
  - **Reference Phase:** eSpeak NG `hi` approximation currently in place; custom rule-based Devanagari-to-IPA mapping (covering visarga `ः`, anusvara `ं`, and vowel lengths) scheduled for January.
  - **Acoustic Phase:** Multilingual phonetic acoustic models (wav2vec 2.0 / XLS-R) evaluated as acoustic feature extractors.
  - **Data Collection:** Partnering with local Sanskrit educators to record validated reference clips.

---

### Slide 7: Roadmap (December 2026 – April 2027)
- **Phase 2 (Dec – Jan): Neural Acoustic Model & Interactive UI**
  - Real wav2vec 2.0 / Whisper phoneme recognizer integration on CPU with model caching.
  - Full browser recording frontend with AudioContext WAV encoder and feedback chips.
- **Phase 3 (Jan – Feb): Multilingual Scoring & Corpus Evaluation**
  - Benchmark automated scores against human ratings on speechocean762 (calculating Pearson/Spearman correlation).
  - Rule-based Sanskrit G2P implementation.
- **Phase 4 (Mar – Apr): Polish & Deployment**
  - Practice dashboard, historical progress charts, and containerized deployment.
