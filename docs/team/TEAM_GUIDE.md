# Language Coach — Team & Contributor Guide

This guide details the team organization, role ownership, onboarding procedure, and collaboration workflows for **Language Coach**.

---

## 1. Team Structure & Subsystem Ownership

The project is divided across five specialized engineering roles (R1–R5). Each role has strict ownership of specific files and folders:

| Role ID | Role Title | Primary Owner | Owned Folders & Files | Core Responsibilities |
|---|---|---|---|---|
| **R1** | **Lead & System Integration** | Project Lead | `ml/contracts.py`, `ml/pipeline.py`, root `run.py`, `requirements.txt`, `docs/MEMORY.md` (STATUS block) | Architecture glue, inter-module contracts, CI test suite integrity, release freezes, mentor coordination. |
| **R2** | **Speech Modeling & Preprocessing** | Team Member (Vivek) | `ml/speech/`, `tests/test_audio_utils.py`, `tests/test_recognizer.py`, `scripts/record_clip.py` | 16 kHz audio preprocessing (normalisation, silence trimming), wav2vec 2.0 acoustic phone decoder, CPU latency optimization. |
| **R3** | **Reference Phonetics & Scoring** | Team Member | `ml/reference/`, `ml/scoring/`, `tests/test_reference.py`, `tests/test_scorer.py`, `tests/test_phoneme_map.py` | eSpeak NG G2P reference generation, symbol set normalization, weighted phonetic cost matrix, per-word attribution. |
| **R4** | **Web Application & UI/UX** | Team Member | `app/`, `tests/test_api.py`, client JS (`app/static/js/`), CSS (`app/static/css/`) | Flask REST API, SQLite persistence, client-side 16 kHz WAV encoding, live visualizer, glassmorphic UI, progress charts. |
| **R5** | **Data Curation & Academic Reporting** | Team Member | `data/content/`, `evaluation/`, `docs/report/`, `scripts/download_data.md`, `tests/test_content.py` | Multi-tiered word lists (88+ items), volunteer user testing protocols, literature survey, formal B.Tech thesis writing. |

---

## 2. Onboarding Checklist for New Teammates

Follow these steps on your very first day:

1. **Complete Local Setup:**
   Follow [`docs/setup/SETUP.md`](../setup/SETUP.md) from start to finish.
2. **Run Environment Doctor:**
   ```powershell
   python scripts\check_setup.py
   ```
   Confirm all checks return `[PASS]`.
3. **Verify All Unit Tests:**
   ```powershell
   python -m pytest tests
   ```
   Confirm all 40 tests pass.
4. **Locate Your Role in `docs/TASKS.md`:**
   Open `docs/TASKS.md`, find your role section (`R1` through `R5`), and locate the first row that is `TODO` where all prerequisites in "Needs" are `DONE`.
5. **Mark Task as Active:**
   Change status to `DOING (YourName)`.
6. **Implement, Test, and Log:**
   Write code, write unit tests in `tests/`, verify all tests pass, update your task row to `DONE (YYYY-MM-DD)`, and add a 3–5 line log entry to your role's section in `docs/MEMORY.md`.

---

## 3. Version Control & Git Workflow

### Phase A: Single Developer Working Mode (Current Mode)
While one person is actively pushing code, work directly on `main` to avoid unnecessary branch-merging overhead:
```powershell
# 1. Verify tests pass
python -m pytest tests

# 2. Check no secrets or data are staged
git status

# 3. Stage changes
git add -A

# 4. Confirm clean status
git status

# 5. Commit with role prefix
git commit -m "R4: add HTML5 canvas score trend line chart"

# 6. Push to GitHub
git push
```

### Phase B: Multi-Developer Feature Branch Workflow (When Teammates Join)
When multiple members collaborate simultaneously, switch to isolated feature branches:
```powershell
# 1. Update local main
git checkout main
git pull

# 2. Create feature branch
git checkout -b r2-wav2vec-hindi

# 3. Make changes and verify tests
python -m pytest tests

# 4. Commit and push feature branch
git add -A
git commit -m "R2: implement Hindi acoustic decoding"
git push -u origin r2-wav2vec-hindi

# 5. Open a Pull Request on GitHub for R1 review
```

---

## 4. Secrets & Collaboration Rules

- **Zero Secrets in Git:** Never commit `.env`. All passwords, secret keys, and tokens live only in `.env`.
- **Zero Audio in Git:** Never commit `.wav`, `.webm`, or recorded voice files. Use synthetic audio in tests (`_make_wav_bytes`).
- **File Ownership Respect:** Do not edit another role's folder without opening a task issue or coordinating with the owner.
- **PowerShell Syntax Rule:** Always provide one command per line in docs and scripts. Never use bash `&&` chaining syntax.

---

## 5. Team Routines & Communication

### Daily Standup Template (Post in Group Chat by 10:00 PM)
```text
Done: (What specific task was finished today)
Doing: (What task ID from TASKS.md you will work on next)
Blocked: (Any blocker or dependency needed from another role)
```

### Weekly Sunday Merge & Review Checklist (Lead / R1)
1. Verify `main` branch passes `python -m pytest tests`.
2. Run `python run.py` on mock mode and real mode to verify live browser playback and assessment.
3. Update the `STATUS` block in `docs/MEMORY.md` with current completion percentage and working features.
4. Post weekly milestone summary to the group chat.
