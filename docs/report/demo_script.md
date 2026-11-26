# Two-Minute Demo Video Script: Language Coach

**Time Budget:** 120 seconds (2:00)  
**Presenter:** Project Lead / Team Member  
**Preparation:** Browser open at `http://127.0.0.1:5000` with console/terminal visible in a split screen.

---

### [0:00 - 0:25] Introduction & Motivation
- **Visual:** Title screen or home screen showing the Language Coach interface.
- **Spoken Audio:**
  > *"Hello everyone! Today we present Language Coach, an AI-powered pronunciation feedback system designed to help learners master subtle sounds in foreign and classical languages without requiring expensive GPU servers."*
- **Action:** Point cursor to the language selector dropdown and clean interface.

### [0:25 - 0:50] Architecture & Workflow
- **Visual:** Show the four supported languages in the dropdown: English, Hindi, Sanskrit, and French.
- **Spoken Audio:**
  > *"Existing language apps only give pass-fail scores. Language Coach breaks down words phoneme by phoneme. It extracts reference phonemes using eSpeak NG, aligns them against spoken speech using weighted phonetic distance, and calculates scores per word and sound."*
- **Action:** Select **English**, click a target word like *"ship"*. Click **"Listen"** to play the reference pronunciation.

### [0:50 - 1:25] Live Assessment Demonstration
- **Visual:** Recording audio and immediate scoring feedback.
- **Spoken Audio:**
  > *"Let's record an attempt. I'll click Record and speak."*
- **Action:** Click **Record**, pronounce *"ship"*, click **Stop**.
- **Spoken Audio:**
  > *"Within half a second on our laptop CPU, the pipeline analyzes the waveform, normalizes audio, aligns phonemes, and returns an overall score, per-word score, and visual sound breakdown. Notice the timing breakdown in the console showing sub-second execution across reference extraction, recognition, and scoring stages."*

### [1:25 - 1:45] Intentional Mispronunciation & Weighted Scoring
- **Visual:** Show how the system handles near-misses.
- **Spoken Audio:**
  > *"If a learner substitutes a similar sound—like saying /s/ instead of /ʃ/ in 'ship'—our weighted scoring engine recognizes the phonetic similarity, awards partial credit, and provides human-readable feedback: 'You said /s/ in ship; the expected sound is /ʃ/.'"*
- **Action:** Show the feedback tips and attempt history stored in the SQLite database.

### [1:45 - 2:00] Conclusion & Next Steps
- **Visual:** Summary slide / progress dashboard view.
- **Spoken Audio:**
  > *"The core integration, weighted scorer, and content sets for four languages are fully functioning. In our next phase, we integrate the pretrained neural acoustic recognizer and refine Sanskrit G2P. Thank you!"*
