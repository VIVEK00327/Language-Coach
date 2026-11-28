# Language Coach — Setup & Installation Guide

This guide walks you through setting up and running **Language Coach** from a fresh clone to a working local installation.

---

## 1. System Prerequisites

Before starting, verify that your machine meets these prerequisites:

| Requirement | Minimum Specification | Recommended |
|---|---|---|
| **Operating System** | Windows 10/11, macOS 12+, or Ubuntu/Debian Linux 20.04+ | Windows 11 or Ubuntu 22.04 LTS |
| **Python** | Python 3.10, 3.11, 3.12, 3.13, or 3.14 | Python 3.11 or 3.12 |
| **RAM** | 4 GB | 8 GB or more (for CPU model inference) |
| **Disk Space** | 2 GB free (mock mode) | 5 GB free (for PyTorch + ~1.2 GB wav2vec 2.0 model cache) |
| **Audio Hardware** | Working microphone & speakers / headphones | Built-in or USB microphone |
| **Internet** | Required for initial `pip install` and model download | Offline once packages and models are cached |

### Verify Python and Git
Run these commands in your terminal:

**Windows PowerShell:**
```powershell
python --version
git --version
```

**macOS / Linux:**
```bash
python3 --version
git --version
```
*Note: Python version must report 3.10.0 or higher.*

### Install eSpeak NG (Phoneme G2P Engine)
Language Coach uses eSpeak NG via `phonemizer` to convert reference text into International Phonetic Alphabet (IPA) phonemes:

- **Windows:**
  1. Download the installer `.msi` from [eSpeak NG GitHub Releases](https://github.com/espeak-ng/espeak-ng/releases).
  2. Run the installer (defaults to `C:\Program Files\eSpeak NG`).
  3. Ensure `C:\Program Files\eSpeak NG` is added to your system `PATH`.
  4. *Windows Note:* If `phonemizer` cannot locate the library, set the environment variable in your terminal:
     ```powershell
     $env:PHONEMIZER_ESPEAK_LIBRARY="C:\Program Files\eSpeak NG\libespeak-ng.dll"
     ```
- **macOS (Homebrew):**
  ```bash
  brew install espeak-ng
  ```
- **Ubuntu / Debian Linux:**
  ```bash
  sudo apt-get update
  sudo apt-get install -y espeak-ng libespeak-ng-dev
  ```

---

## 2. Clone and Virtual Environment

### Clone Repository
```bash
git clone <repository-url>
cd "Major Project"
```

### Create and Activate Virtual Environment

**Windows PowerShell (one command per line):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
*(If PowerShell restricts script execution, run: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` then activate again).*

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install Python Dependencies

Install the pinned dependencies from `requirements.txt`:

**Windows PowerShell:**
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**macOS / Linux:**
```bash
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## 4. Environment Configuration (`.env`)

Configuration settings live exclusively in `.env`. Never commit `.env` to Git.

### Create Local Configuration
Copy the template `.env.example` to `.env`:

**Windows PowerShell:**
```powershell
Copy-Item .env.example .env
```

**macOS / Linux:**
```bash
cp .env.example .env
```

### What Each Variable Means

| Variable Name | Purpose & Allowed Values | Default in `.env.example` |
|---|---|---|
| `SECRET_KEY` | Flask session cryptographic key. Generate locally with: `python -c "import secrets; print(secrets.token_hex(24))"` | Empty (auto-generates transient key if omitted) |
| `FLASK_DEBUG` | Flask debug mode and hot-reloader (`1` = enabled, `0` = production mode). | `1` |
| `DATABASE_PATH` | Path to the SQLite practice database file. | `instance/coach.db` |
| `UPLOAD_MAX_MB` | Maximum allowed audio upload file size in megabytes. | `10` |
| `USE_MOCK_ML` | **Core toggle**: `1` = instant mock recognizer (zero model download, fast local testing); `0` = real wav2vec 2.0 acoustic neural model on CPU. | `1` |
| `PHONEME_MODEL_NAME` | Hugging Face pretrained acoustic model ID for English phoneme decoding. | `facebook/wav2vec2-lv-60-espeak-cv-ft` |
| `WHISPER_MODEL_SIZE` | Model size for Whisper fallback (`tiny`, `base`, `small`). | `base` |
| `HF_TOKEN` | Optional Hugging Face access token (only needed if accessing gated private models; public models do not need this). | *(leave empty)* |
| `LLM_API_KEY` | Optional LLM API key for future extended coaching feedback (Phase 2). | *(leave empty)* |

---

## 5. Validate Environment with the Doctor Script

Language Coach includes an automated diagnostic tool to verify your environment:

**Windows PowerShell:**
```powershell
python scripts\check_setup.py
```

**macOS / Linux:**
```bash
python3 scripts/check_setup.py
```

Expected output:
```text
=================================================================
 Language Coach — Environment Diagnostic Doctor
=================================================================
Checking Python Version...
  [PASS] Python version: 3.14.2 (>= 3.10 required)

Checking Core Python Packages...
  [PASS] Core Python packages imported successfully (6 packages)

Checking eSpeak NG Phonemizer...
  [PASS] eSpeak NG G2P engine found

Checking Environment Configuration...
  [PASS] .env file exists
         Variables configured: FLASK_DEBUG, DATABASE_PATH, UPLOAD_MAX_MB, USE_MOCK_ML, WHISPER_MODEL_SIZE

Checking Microphone Recording Lib...
  [PASS] Microphone audio capture library (sounddevice) is available

Checking Acoustic Model Storage...
  [PASS] Acoustic model storage: will download on first real inference request (~1.2 GB)
=================================================================
 Diagnostic Result: HEALTHY. Ready to run Language Coach.
 Command to start: python run.py
=================================================================
```

---

## 6. Run Automated Test Suite

Run the full pytest suite (all tests execute on CPU using mocks or synthetic audio):

**Windows PowerShell:**
```powershell
python -m pytest tests -v
```

**macOS / Linux:**
```bash
python3 -m pytest tests -v
```
*Expected: 40/40 passed.*

---

## 7. Starting the Application

### Mode A: Mock Mode (Recommended for Instant First Run)
Ensure `.env` contains:
```ini
USE_MOCK_ML=1
```

Run the application:
```powershell
python run.py
```
Open your browser at:
```text
http://127.0.0.1:5000
```
*(Use `http://127.0.0.1:5000` rather than a remote hostname; modern browsers automatically grant microphone permissions to `localhost` and `127.0.0.1` without requiring an SSL certificate).*

### Mode B: Real ML Acoustic Model Mode
To use the real wav2vec 2.0 neural acoustic model:
1. Open `.env` and set:
   ```ini
   USE_MOCK_ML=0
   PHONEME_MODEL_NAME=facebook/wav2vec2-lv-60-espeak-cv-ft
   ```
2. Restart the server:
   ```powershell
   python run.py
   ```
3. **First Request Download:** The first time you record and submit an audio clip in real mode, the server downloads the pretrained weights (~1.18 GB) from Hugging Face into `~/.cache/huggingface/hub/`. The UI will display:
   *"First run loads the model... This can take a minute while neural weights load into CPU memory. Please wait."*
   Subsequent attempts reuse the singleton cached in CPU memory and execute in ~0.5–1.5 seconds.

---

## 8. "How to Know It Is Working" Checklist

When testing in your browser (`http://127.0.0.1:5000`):

1. **Landing Page (`/`):**
   - [x] Ambient glowing purple/cyan background renders smoothly.
   - [x] Clicking the sun/moon icon toggles light and dark modes instantly without page reload.
   - [x] Clicking **"Practice Hindi"** opens `/practice?lang=hindi` with Hindi preselected.
2. **Practice Studio (`/practice`):**
   - [x] Click **"Listen"**: Browser native speech synthesis speaks the selected phrase.
   - [x] Click **Microphone**: Browser asks for mic permission (click "Allow").
   - [x] Speak into mic: Live green/cyan waveform reacts and the circular timer counts down.
   - [x] Click **"Stop & Check"**: Spinner shows, then circular score ring animates (0–100%).
   - [x] Breakdown shows word cards with green (correct) or red (substituted) IPA sound chips.
3. **Progress Dashboard (`/progress`):**
   - [x] Summary stat cards (Total Attempts, Average Score, Top Language) update.
   - [x] Score trend line chart renders on HTML5 canvas.
   - [x] Attempt history table lists timestamp, language, target, and score badge.

---

## 9. Daily Git Routine for Teammates

While developing on the project:

### Windows PowerShell (one command per line, never use `&&`):
```powershell
python -m pytest tests
git status
git add -A
git status
git commit -m "R4: add feature description"
git push
```

### Safety Rules:
- Never commit `.env` (check `git status` output before committing).
- Never commit audio files (`.wav`, `.webm`, `.mp3`) or SQLite databases (`instance/coach.db`).
- Always run `python -m pytest tests` before pushing.

---

## 10. Setup Completion Checklist

- [ ] Python 3.10+ installed and verified
- [ ] eSpeak NG installed and working
- [ ] Virtual environment `.venv` active
- [ ] Dependencies installed via `pip install -r requirements.txt`
- [ ] `.env` created from `.env.example`
- [ ] `python scripts/check_setup.py` outputs `[PASS]` on all items
- [ ] `python -m pytest tests` passes 100%
- [ ] Application starts on `http://127.0.0.1:5000`
