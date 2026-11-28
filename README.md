# Language Coach: AI-Based Multilingual Pronunciation Learning System

> **B.Tech Computer Science & Engineering — Final Year Major Project (2026–27)**  
> *Department of Computer Engineering & Applications*

---

## Project Overview

**Language Coach** is a lightweight, privacy-preserving web application designed to help language learners master native-like pronunciation through fine-grained, sound-by-sound feedback. Unlike conventional language apps that only provide holistic pass/fail ratings or autocorrect errors via language models, Language Coach decodes spoken acoustics directly into International Phonetic Alphabet (IPA) phonemes, aligns them with expected target sounds using a phonetically-weighted edit distance, and pinpoints exact substitutions (e.g., distinguishing between postalveolar `/ʃ/` and dental `/s/` in *"ship"*). The entire pipeline runs locally on consumer laptop CPUs with zero cloud API dependencies.

---

## Key Features

- **Sound-by-Sound IPA Diagnostics:** Green chips for correct phonemes, red chips showing expected &rarr; spoken substitutions with actionable coaching tips.
- **Weighted Phonetic Scoring:** Dynamic alignment matrix awards partial credit ($0.5$) for acoustically similar sounds (voicing and sibilant near-misses).
- **Four Supported Languages:** Curated tiered curriculums (beginner, intermediate, advanced) across English, Hindi, Sanskrit, and French.
- **Client-Side WAV Encoding:** In-browser Web Audio conversion decodes and resamples audio to 16 kHz mono 16-bit PCM WAV, eliminating server ffmpeg dependencies.
- **CPU-Optimized Acoustic AI:** Pretrained wav2vec 2.0 acoustic phone decoder cached in memory as a singleton for fast sub-second inference.
- **Learner Progress Dashboard:** Local SQLite attempt history paired with HTML5 canvas score trend line charts.
- **Glassmorphic UI Design:** Translucent glass cards, ambient glowing background, and instant zero-FOUT dark/light theme switching.

---

## Application Previews

| Light Mode Practice Studio | Dark Mode Dashboard |
|---|---|
| ![Practice Studio Light](docs/assets/home-light.png)<br>*(TODO: Add screenshot `docs/assets/home-light.png`)* | ![Dashboard Dark](docs/assets/progress-dashboard.png)<br>*(TODO: Add screenshot `docs/assets/progress-dashboard.png`)* |

---

## Quick Start in 6 Commands

### Windows PowerShell (one command per line):
```powershell
# 1. Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create local environment configuration
Copy-Item .env.example .env

# 4. Run automated environment diagnostics
python scripts\check_setup.py

# 5. Run automated test suite (40 tests)
python -m pytest tests

# 6. Launch application
python run.py
```

### macOS / Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python3 scripts/check_setup.py
python3 -m pytest tests
python3 run.py
```

Open your browser at **`http://127.0.0.1:5000`** to access Language Coach.

---

## Documentation Directory

For in-depth guides, architectural blueprints, and contributor workflows, consult the [Documentation Portal](docs/README.md):

- **Mentor & Evaluator Materials:**
  - [Project Overview](docs/project/OVERVIEW.md) — 1-page executive summary.
  - [System Architecture](docs/project/ARCHITECTURE.md) — Mermaid system and sequence flow diagrams.
  - [Milestone Progress Report](docs/project/PROGRESS_REPORT.md) — Detailed feature audit and Nov–Apr timeline.
  - [Live Demo Script](docs/project/DEMO_GUIDE.md) — 3-minute presentation script and mentor Q&A.
- **Developer & Teammate Guides:**
  - [Installation Guide](docs/setup/SETUP.md) — Zero-to-running walkthrough.
  - [Troubleshooting Matrix](docs/setup/TROUBLESHOOTING.md) — Solutions for 14+ common local errors.
  - [Team Contributor Guide](docs/team/TEAM_GUIDE.md) — Roles R1–R5 and daily git workflows.
  - [Design System Guide](docs/design/DESIGN.md) — CSS tokens, color palettes, and glass components.

---

## Project Status & Milestone Audit

- **Current Milestone:** November Review Checkpoint (~40% of Final Academic Year Scope).
- **Core Engine:** Preprocessing, eSpeak NG IPA reference, wav2vec 2.0 acoustic recognizer on CPU, weighted scorer, and multi-word attribution are fully functional.
- **Test Suite:** 40/40 tests passing across API, preprocessing, contracts, and scoring.
- **Next Planned Deliverables:** Benchmark validation against speechocean762 human ratings, Sanskrit deterministic rule-based G2P refinements, and expanded language corpora.

---

## Team & Role Ownership

| Role | Title | Primary Owner | Subsystem Responsibility |
|---|---|---|---|
| **R1** | Lead / System Integration | Project Lead | Architecture contracts (`ml/contracts.py`), pipeline glue (`ml/pipeline.py`), release freezes. |
| **R2** | Speech Modeling & Audio Preprocessing | Vivek | Preprocessing (`ml/speech/audio_utils.py`), wav2vec 2.0 CPU recognizer (`ml/speech/recognizer.py`). |
| **R3** | Reference Phonetics & Scoring | Team Member | eSpeak NG IPA G2P (`ml/reference/`), weighted phoneme scoring (`ml/scoring/scorer.py`). |
| **R4** | Web Application & UI/UX | Team Member | Flask routes (`app/`), glassmorphic frontend, client WAV converter, progress dashboard. |
| **R5** | Data Curation & Academic Reporting | Team Member | Multi-tiered curricula (`data/content/`), user testing protocols, literature survey, thesis drafting. |

---

## License & Credits
- **License:** TODO: Academic open-source license to be finalized by the project team.
- **Acoustic Pretrained Model:** `facebook/wav2vec2-lv-60-espeak-cv-ft` via Hugging Face.
- **G2P Engine:** eSpeak NG and `phonemizer`.
