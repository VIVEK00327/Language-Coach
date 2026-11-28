# Language Coach — Live Demonstration & Mentor Presentation Guide

This guide prepares you for a **3-minute live demonstration** before your project mentor or external evaluator, including preparation steps, step-by-step spoken cues, and answers to likely technical questions.

---

## 1. Pre-Demo Preparation Checklist (5 Minutes Before)

- [ ] **Ensure Working Directory:** Open terminal in project root (`Major Project`).
- [ ] **Activate Environment:** Run `.\.venv\Scripts\Activate.ps1` (Windows) or `source .venv/bin/activate` (Mac/Linux).
- [ ] **Run Diagnostic Doctor:** Execute `python scripts/check_setup.py` and confirm all items report `[PASS]`.
- [ ] **Run Test Suite:** Execute `python -m pytest tests` and verify 40/40 tests pass.
- [ ] **Check Real ML Settings in `.env`:**
  - `USE_MOCK_ML=0` (or `1` if demonstrating on low-spec hardware without internet).
  - `PHONEME_MODEL_NAME=facebook/wav2vec2-lv-60-espeak-cv-ft`.
- [ ] **Warm-up Recording (Critical):** Start the server (`python run.py`), open `http://127.0.0.1:5000/practice`, and record one throwaway test clip. This downloads and caches the model weights into memory so your mentor sees an instant sub-second response during the demo.
- [ ] **Browser Setup:** Open `http://127.0.0.1:5000` in a full-screen or half-screen browser window. Keep the terminal running alongside to show the per-stage timing logs.

---

## 2. Three-Minute Live Demo Script

### [0:00 – 0:45] Problem, Solution & Landing Page
- **Action:** Start on the Home page (`/`). Toggle the **Theme Switcher** (sun/moon icon in top-right) to show light and dark glassmorphic styling.
- **Say:**
  > *"Good morning/afternoon, Sir/Ma'am. Today we present Language Coach, an AI-based multilingual pronunciation tutor built for our final-year project. Conventional language apps give students a binary pass/fail score without explaining which exact sound was incorrect. Language Coach diagnoses pronunciation at the individual phoneme level, completely on CPU, with zero cloud dependency."*
- **Action:** Scroll to the 4 language cards (English, Hindi, Sanskrit, French). Click **"Practice English"** on the English card.

---

### [0:45 – 1:45] Accurate Pronunciation Demonstration
- **Action:** You are now on the Practice Studio (`/practice`).
- **Say:**
  > *"Here in the Practice Studio, a learner selects a phrase from tiered difficulty levels. Notice the 'Listen' button powered by native speech synthesis."*
- **Action:** Select word **"ship"**. Click **"Listen"** (browser speaks *"ship"*).
- **Say:**
  > *"Now I will record an accurate pronunciation. Watch the live acoustic waveform and the smoothed volume meter."*
- **Action:** Click the large **Microphone button**. Pronounce *"ship"* clearly. Click **"Stop & Check"**.
- **Action:** Point out the results:
  1. Animated circular score ring showing **high score (80–100%)**.
  2. Word card displaying the word *"ship"*.
  3. Green phonetic chips showing `[ /ʃ/ ] [ /ɪ/ ] [ /p/ ]` all matched.
  4. Coaching feedback: *"Great pronunciation!"*
  5. Latency line showing sub-second execution (e.g., *Latency: 0.62s*).

---

### [1:45 – 2:30] Intentional Mispronunciation & Weighted Scoring
- **Action:** Click **"Try Again"**. Keep the target word as **"ship"**.
- **Say:**
  > *"Now let's see how Language Coach catches phonetic transfer errors. A common mistake for second-language learners is substituting the dental sibilant /s/ for the postalveolar /ʃ/, saying 'sip' instead of 'ship'."*
- **Action:** Click **Microphone**. Pronounce *"sip"* clearly. Click **"Stop & Check"**.
- **Action:** Point out the results:
  1. Score reflects a near-miss (~60–75%).
  2. The first phoneme chip turns **red**, explicitly showing: `/ʃ/ → /s/`.
  3. Actionable coaching tip: *"You said /s/ in 'ship'; the expected sound is /ʃ/."*
- **Say:**
  > *"Instead of failing the entire word, our weighted scoring algorithm awards partial credit (0.5) because /s/ and /ʃ/ share place and manner of articulation, giving the student encouragement while pinpointing the exact sound to fix."*

---

### [2:30 – 3:00] Progress Dashboard & Conclusion
- **Action:** Click **"Progress"** in the top navigation bar.
- **Say:**
  > *"Every attempt is automatically saved to our local SQLite database. The Progress Dashboard tracks total practice attempts, overall average score, most practiced language, and plots an HTML5 canvas trend line. The entire system is built with zero external CDN dependencies, runs on CPU, and is verified by 40 automated unit tests."*
- **Action:** Point to the recent attempts table and score trend chart. Conclude:
  > *"Thank you, Sir/Ma'am. We are happy to take any questions."*

---

## 3. Likely Mentor Questions & Direct Answers

### Q1: "Why did you use wav2vec 2.0 instead of a standard ASR like Google Speech-to-Text?"
> **Answer:** Standard commercial ASR systems use language models and beam search designed to correct speech into valid dictionary words. If a student says *"sip"* when trying to say *"ship"*, standard ASR autocorrects it or recognizes the English word *"sip"*, hiding the phonetic error. Pretrained wav2vec 2.0 decodes raw acoustic representations directly to International Phonetic Alphabet (IPA) phonemes without language model over-correction.

### Q2: "How does the weighted scoring algorithm work mathematically?"
> **Answer:** We use dynamic sequence alignment (modified Levenshtein edit distance). Instead of treating all substitutions with a uniform penalty of $1.0$, our similarity matrix awards partial credit ($0.5$ cost instead of $1.0$) for acoustically similar sounds—such as voiced/unvoiced pairs (`/p/` vs `/b/`, `/t/` vs `/d/`) or sibilant pairs (`/s/` vs `/ʃ/`). The overall word score is calculated as:
> $$\text{Score} = \max\left(0, 100 \times \left(1 - \frac{\text{weighted edit distance}}{\text{expected length}}\right)\right)$$

### Q3: "Can this system run completely offline without an internet connection?"
> **Answer:** Yes. Once the Python dependencies and the initial wav2vec 2.0 weights are downloaded into the local cache, the entire stack—Flask backend, eSpeak NG G2P engine, wav2vec 2.0 PyTorch inference on CPU, SQLite database, and the frontend—runs 100% offline with zero cloud API dependencies.

### Q4: "How are you handling classical Sanskrit pronunciation?"
> **Answer:** Sanskrit lacks commercial ASR models and labeled training datasets. However, classical Sanskrit spelling in Devanagari is almost 100% phonetically regular. We use deterministic rule-based G2P mapping to model visarga (`ः`), anusvara (`ं`), aspiration, and long vs. short vowels, paired with curated test recordings from native Sanskrit teachers.

---

## 4. Backup Plan: What if Hardware Fails?
If the demonstration microphone disconnects or hardware audio fails:
1. **Fallback Video:** Play the 2-minute pre-recorded demo video (`docs/report/demo_script.md`).
2. **Mock Mode CLI:** Run `python evaluation/smoke_test.py` in your terminal to demonstrate the automated pipeline processing pre-recorded `.wav` test audio clips with printed timing and phoneme alignment logs.
