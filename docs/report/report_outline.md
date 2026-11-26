# Project Report Outline: Language Coach
**Title:** Language Coach: AI-Based Multilingual Pronunciation Learning System  
**Department:** Computer Engineering & Applications, B.Tech CSE (2026-27)

---

### Section 1: Introduction
- **Background & Motivation:** Explains the growing demand for self-paced, multilingual pronunciation training and the lack of immediate, fine-grained phonetic feedback in conventional language apps.
- **Problem Statement & Objectives:** Details the goal of building a lightweight, privacy-conscious web application capable of phone-level pronunciation assessment on standard CPU hardware without costly GPU infrastructure.
- **Scope & Limitations:** Clarifies the core target languages (English, Hindi, Sanskrit, French) and sets realistic boundaries (offline local deployment, non-streaming offline assessment, pretrained models).

### Section 2: Literature Survey
- **Computer-Assisted Pronunciation Training (CAPT):** Historical evolution from simple speech-to-text matching to modern Acoustic Model phone log-likelihood ratio scoring.
- **Deep Learning in Speech Processing:** Review of self-supervised acoustic representations (wav2vec 2.0, XLS-R) versus sequence-to-sequence multilingual models (OpenAI Whisper).
- **Phonetic Datasets & Benchmarks:** Survey of standard non-native English corpora (speechocean762, L2-ARCTIC) and community crowdsourced data (Mozilla Common Voice).

### Section 3: Requirements Analysis
- **Functional Requirements:** Language selection, reference audio playback, browser-based microphone recording, phoneme alignment, weighted error scoring, per-word analysis, actionable feedback, and history tracking.
- **Non-Functional Requirements:** Sub-5 second latency per 10-second audio clip on laptop CPU, minimal memory footprint (<2 GB RAM), cross-platform browser support, and zero hardcoded secrets.
- **Hardware & Software Specifications:** Minimal hardware (quad-core x86-64 CPU, 4–8 GB RAM), software stack (Python 3.10+, Flask, Librosa, SoundFile, eSpeak NG, SQLite).

### Section 4: System Design & Architecture
- **Overall System Topology:** Modular separation of concerns into Client/Browser layer, Flask REST API service, and decoupled ML evaluation engine.
- **Data Flow & Pipelines:** Step-by-step transformation from raw client-side PCM audio to resampled 16 kHz mono waveforms, phonetic transcription, SequenceMatcher alignment, and JSON scoring structures.
- **Database Schema:** SQLite lightweight persistent store recording user practice sessions, timestamps, target text, scores, and serialized assessment results.

### Section 5: Implementation Details
- **Audio Preprocessing (`ml.speech.audio_utils`):** In-browser WAV encoding to eliminate server-side ffmpeg dependencies, stereo downmixing, silence trimming, and peak normalisation.
- **Grapheme-to-Phoneme Engine (`ml.reference`):** Integration with eSpeak NG through `phonemizer` for cross-lingual IPA generation with fallback mock support.
- **Speech Recognition Engine (`ml.speech.recognizer`):** Pretrained acoustic model phone decoding with singleton model caching to minimize CPU overhead.
- **Weighted Phoneme Scorer (`ml.scoring.scorer`):** Dynamic sequence alignment applying phonetic similarity weight matrix ($0.5$ credit for voicing and place near-misses) and per-word segmentation.

### Section 6: Evaluation & Results
- **Scoring Accuracy & Reliability:** Evaluation against synthetic test cases and curated non-native test clips with intentional phonetic substitutions.
- **Computational Performance:** Benchmark table measuring latency, peak RAM utilization, and inference speed per language on CPU.
- **User Experience Assessment:** Qualitative feedback from user testing sessions evaluating clarity of feedback chips and usability of the interface.

### Section 7: Conclusion & Future Work
- **Summary of Contributions:** A functional, end-to-end multilingual pronunciation coach working on CPU with sub-word diagnostics and modular design.
- **Future Enhancements:** Native mobile client, expanded language coverage (German, Spanish, Sanskrit rule-based G2P refinement), and learned scoring calibrators.
