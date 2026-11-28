# Language Coach — Project Overview

> **Executive Summary for Project Mentors & Evaluators**  
> **Course:** B.Tech Computer Science & Engineering (Final Year Major Project, 2026–27)  
> **Department:** Department of Computer Engineering & Applications  

---

## 1. Problem Statement
Language learners struggle with pronunciation because conventional language apps (Duolingo, Babbel) only evaluate holistic phrase correctness or word-level ASR matching. A student receives a binary pass/fail grade without knowing **which sound was mispronounced**. Furthermore, existing commercial speech engines rely on cloud APIs with recurring costs and latency, or require expensive GPU servers that cannot run locally on consumer student laptops.

## 2. Our Solution
**Language Coach** is a lightweight, privacy-preserving web application for multilingual pronunciation training. It extracts the expected International Phonetic Alphabet (IPA) phonemes of a target phrase, analyzes the user's spoken voice using an acoustic neural model, aligns the two sound sequences using weighted phonetic distance, and delivers **sound-by-sound visual diagnostics** (e.g., showing that the user substituted `/s/` for expected `/ʃ/` in *"ship"*).

## 3. How It Works in 5 Steps
1. **Curriculum Selection:** Learner selects a language and difficulty tier (beginner, intermediate, advanced) from the curated JSON word lists.
2. **Audio Reference:** Learner clicks **"Listen"** to hear native speech synthesis and internalize correct articulation.
3. **Local Recording:** Learner records their voice; the browser visualizes the live acoustic waveform and resamples audio locally to **16 kHz mono 16-bit PCM WAV**.
4. **Phonetic Analysis:** The backend extracts reference phonemes via eSpeak NG G2P and spoken phonemes via pretrained wav2vec 2.0 on CPU.
5. **Weighted Alignment & Feedback:** Dynamic programming aligns phonemes, awards partial credit ($0.5$) for acoustically similar sounds (voicing and sibilant near-misses), calculates scores (0–100), and renders color-coded phonetic chips.

## 4. Key Features
- **Sound-by-Sound IPA Diagnostics:** Green chips for correct sounds, red chips showing expected &rarr; spoken substitutions.
- **Multilingual Support:** English, Hindi, Sanskrit, and French curriculums (88+ curated practice items).
- **In-Browser Audio Conversion:** Resampling and WAV header encoding run in JavaScript (`AudioContext`), eliminating server-side ffmpeg dependencies.
- **Zero-Cloud & Privacy First:** All acoustic inference runs on local CPU. Audio recordings are deleted immediately after evaluation.
- **Learner Dashboard:** Tracks historical attempts in SQLite with interactive HTML5 canvas score trend charts.
- **Accessible Glassmorphism UI:** Modern SaaS aesthetic with instant zero-FOUT dark/light theme switching.

## 5. Technology Stack
- **Backend Service:** Python 3.10+, Flask 3.1, SQLite 3.
- **Speech & Audio ML:** Librosa 1.0, SoundFile 0.14, Hugging Face `transformers` (wav2vec 2.0 `facebook/wav2vec2-lv-60-espeak-cv-ft`).
- **Phonetics & G2P:** `phonemizer` 3.6, eSpeak NG.
- **Frontend Client:** Vanilla ES6+ JavaScript (Web Audio API, `MediaRecorder`), modern CSS variables, HTML5.
- **Quality Assurance:** `pytest` (40 automated unit tests covering API, contracts, preprocessing, and scoring).

## 6. What Is Complete vs. What Is Next
- **Completed (November Review Checkpoint):** End-to-end decoupled pipeline, 16 kHz audio preprocessing, eSpeak IPA reference extraction, weighted substitution matrix, per-word attribution, wav2vec 2.0 recognizer with CPU caching, multi-page glassmorphic UI, progress dashboard, and 40 passing tests.
- **Next Phases (December–April):** Extended Sanskrit rule-based G2P refinements, benchmark validation against speechocean762 human scores, expanding curricula to 100+ items per language, and final production packaging.

---

## 7. Documentation Quick Links
- **[System Architecture](ARCHITECTURE.md)** — Detailed Mermaid sequence and flow diagrams.
- **[Progress Report](PROGRESS_REPORT.md)** — Honest completion breakdown, timeline, and risk mitigations.
- **[Live Demo Guide](DEMO_GUIDE.md)** — 3-minute presentation script and mentor Q&A.
- **[Setup & Installation Guide](../setup/SETUP.md)** — Step-by-step instructions for running on a clean laptop.
- **[Design System](../design/DESIGN.md)** — Color tokens, glassmorphism components, and accessibility.
