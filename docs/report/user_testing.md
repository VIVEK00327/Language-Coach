# User Testing Protocol: Language Coach

This document details the standardized 5-minute volunteer testing protocol, survey instrument, and evaluation recording sheet for preliminary user validation.  
*Note: In accordance with project integrity guidelines, no volunteer results or scores are fabricated. The evaluation table remains empty until volunteer trials are conducted.*

---

## 1. Five-Minute Testing Script (Facilitator Guide)

### Preparation (1 minute)
1. Launch the application: `python run.py`.
2. Ensure the microphone is connected and working.
3. Open `http://127.0.0.1:5000` in the browser.
4. Welcome the volunteer and explain the purpose:
   > *"We are developing Language Coach, an AI system that listens to your pronunciation and provides sound-by-sound feedback. We would love your honest feedback on whether the interface and advice are clear."*

### Practice Walkthrough (3 minutes)
1. **Language & Word Selection:**
   - Ask the participant to select **English** from the dropdown.
   - Ask them to pick a beginner word (e.g., *"ship"* or *"think"*).
2. **Listen:**
   - Instruct the volunteer to click **"Listen"** to hear the target pronunciation.
3. **Record Attempt 1 (Natural):**
   - Ask the volunteer to click **"Record"**, speak clearly into the mic, and click **"Stop"**.
   - Observe the score and feedback chips generated.
4. **Record Attempt 2 (Intentional Variation):**
   - Ask the volunteer to deliberately mispronounce a sound (e.g., say *"sip"* instead of *"ship"*).
   - Check if the system correctly highlights the substitution (`You said /s/ in 'ship'; expected /ʃ/`).
5. **Multilingual Test (Optional):**
   - If familiar, have them try a Hindi word (e.g., *"नमस्ते"*) or French word (*"bonjour"*).

### Survey Completion (1 minute)
- Have the participant complete the 6-question feedback form below.

---

## 2. Six-Question Volunteer Feedback Form

| Q# | Question | Response Scale / Type |
|---|---|---|
| **Q1** | How easy was it to navigate the practice screen and record your voice? | 1 (Very Difficult) to 5 (Very Easy) |
| **Q2** | Was the phonetic feedback clear and understandable? | 1 (Not Clear) to 5 (Extremely Clear) |
| **Q3** | Did the pronunciation score feel believable and fair for your attempt? | 1 (Unbelievable / Random) to 5 (Very Believable) |
| **Q4** | Would you use this tool to practice a foreign language? | 1 (Definitely Not) to 5 (Definitely Yes) |
| **Q5** | What was confusing or did not work as expected? | Open-ended text |
| **Q6** | What is the single most important improvement you would suggest? | Open-ended text |

---

## 3. Volunteer Results Recording Table (To Be Populated)

| Participant ID | Date | Language Tested | Words Attempted | Avg Score | Q1 (1-5) | Q2 (1-5) | Q3 (1-5) | Q4 (1-5) | Confusing Elements (Q5) | Suggested Improvements (Q6) |
|---|---|---|---|---|---|---|---|---|---|---|
| *P01* | | | | | | | | | | |
| *P02* | | | | | | | | | | |
| *P03* | | | | | | | | | | |
| *P04* | | | | | | | | | | |
| *P05* | | | | | | | | | | |
