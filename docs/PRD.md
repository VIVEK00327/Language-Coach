# PRD: Language Coach (Product Requirements)
> Read only the section you need. Sections: 1 Overview | 2 Features | 3 Requirements | 4 Architecture | 5 Languages | 6 Stack | 7 Timeline | 8 Roles | 9 Decisions

## 1. Overview
**Title:** Language Coach: AI-Based Multilingual Pronunciation Learning System
**Program:** B.Tech CSE, session 2026-27, Dept. of Computer Engineering & Applications. **Team:** 5.
**Duration (synopsis):** Nov 2026 - Apr 2027. **Milestone:** 30-40% done by 30 Nov 2026. **Deployment:** final phase only.
Web app: user picks a language + word/sentence, hears reference pronunciation, records speech, gets automated feedback
and a score. Practice activities + progress dashboard. Languages: English, Hindi, Sanskrit, French first; Latin, Spanish,
German later. Motivation: learners lack immediate pronunciation feedback; this unifies practice, recording and feedback.
Out of scope: training speech models from scratch, mobile app, real-time streaming scoring, extra languages (unless time).

## 2. Features (priority)
| ID | Feature | Priority |
|---|---|---|
| F1 | Select language | Must |
| F2 | Select/enter word or sentence from content list | Must |
| F3 | Reference pronunciation playback | Must |
| F4 | Browser recording and submit | Must |
| F5 | Overall score, per-word score, per-sound correct/incorrect | Must |
| F6 | Readable feedback (expected vs spoken sound) | Must |
| F7 | Attempt history in SQLite | Must |
| F8 | Progress dashboard | Should |
| F9 | Practice activities (levels, daily set) | Should |
| F10 | Login | Could |
| F11 | LLM-written feedback | Could |
| F12 | Latin, Spanish, German | Could |

## 3. Requirements
- Score a clip under 10 s in about 5 s on laptop CPU (no GPU available). Small models only (Whisper tiny/base/small).
- ML code independent of Flask; Flask has no scoring logic. Config only through environment variables (`.env`).
- Adding a language = content JSON + reference-phoneme config + recognizer language setting.
- Pinned `requirements.txt`; README quick start works on a fresh machine; tests for scorer and API.
- Hardware: 4 GB RAM min (8 recommended), mic, speakers. OS: Windows 10/11 or Linux.

## 4. Architecture
```
Browser (record, feedback) -> POST /api/assess -> app/routes -> ml/pipeline.assess()
  ml/reference  (expected phonemes) + ml/speech (spoken phonemes) -> ml/scoring (align, score)
  -> AssessmentResult JSON -> UI; attempt saved to SQLite (app/db.py)
```
**Contract (`ml/contracts.py`, do not change without lead):** `PhonemeResult(expected, spoken, correct)`,
`WordResult(word, score, phonemes)`, `AssessmentResult(language, target_text, overall_score, words, feedback)`.
**Stable signatures:**
- `get_reference_phonemes(text, language) -> list[str]` (ml/reference/reference_phonemes.py, R3)
- `recognize_phonemes(audio_path, language) -> list[str]` (ml/speech/recognizer.py, R2)
- `score_pronunciation(expected, spoken) -> (overall, list[PhonemeResult])` (ml/scoring/scorer.py, R3)
- `assess(audio_path, target_text, language) -> AssessmentResult` (ml/pipeline.py, R1)
Mocks of the first two exist so everyone works in parallel from day 1.
**API:** GET `/api/languages`; GET `/api/content/<language>`; POST `/api/assess` (audio, language, text); GET `/api/progress`.
**DB:** table `attempts(id, created_at, language, target_text, overall_score, result_json)`.

## 5. Languages
Order: English -> French -> Hindi -> Sanskrit.
| Language | Expected phonemes | Recognition | Risk |
|---|---|---|---|
| English | espeak-ng (en-us) | Whisper + phoneme model | Low |
| French | espeak-ng (fr) | Whisper + phoneme model | Low |
| Hindi | espeak-ng (hi), verify quality | Whisper (hi) + phoneme model | Medium |
| Sanskrit | Custom rule-based Devanagari-to-sound G2P (also check espeak-ng `sa`) | Hindi/multilingual phoneme model as approximation | **High** |
Sanskrit: no off-the-shelf ASR or datasets; do not train one. Rule-based G2P is realistic (regular spelling: vowel length,
aspiration, retroflex vs dental, anusvara, visarga). State the approximation honestly in the report. Reference audio: record
a teacher/friend. R5 verifies Sanskrit data availability in Week 1.
Content files: `data/content/<language>.json` with `levels: {beginner, intermediate, advanced}` of `{text, note?}`.
Targets: 20+ items per language by 30 Nov, 100+ later.
Datasets to evaluate (verify license/availability): speechocean762 (human scores), L2-ARCTIC, Common Voice, own recordings.

## 6. Stack
Python 3.10+, Flask + HTML/CSS/JS, SQLite, Librosa/soundfile, Whisper (faster-whisper) and a pretrained wav2vec2/XLS-R
phoneme model, phonemizer + espeak-ng, scikit-learn (optional scoring model), pytest, python-dotenv, VS Code / Antigravity.

## 7. Timeline
Synopsis phases: Requirements & planning (Nov-Dec); Content & setup (Nov-Dec); Audio pipeline & UI (Dec-Jan); Core app & ML
(Dec-Feb); Integration, testing, evaluation (Feb-Mar); Documentation & final demo (Mar-Apr); **Deployment** (Mar-Apr, last).
**30 Nov definition of done:** English works end to end locally; word lists for 4 languages; languages/risks documented;
report draft (problem, literature survey, architecture diagram); 2-minute demo video.
November weeks: W1 5-11 setup/learn/mock running; W2 12-18 real recognizer + reference + recording UI; W3 19-25 real scoring +
feedback UI + first evaluation; W4 26-30 integration freeze 28 Nov, user testing, report, demo video.
Later: Dec Hindi+French, history/dashboard; Jan Sanskrit, better scoring, optional LLM; Feb evaluation; Mar deploy; Apr report/viva.
Open item: team once said 3-4 months, synopsis says Nov-Apr. Synopsis is official until confirmed with guide (see MEMORY).

## 8. Roles (owners; edit only your own folders)
| Role | Name | Owns |
|---|---|---|
| R1 | Lead / integration | `ml/contracts.py`, `ml/pipeline.py`, repo, MEMORY status block, requirements |
| R2 | Speech model | `ml/speech/`, `tests/test_recognizer.py` |
| R3 | Reference + scoring | `ml/reference/`, `ml/scoring/`, `tests/test_scorer.py` |
| R4 | App / UI | `app/`, `tests/test_api.py` |
| R5 | Data, evaluation, report | `data/content/`, `evaluation/`, `scripts/`, `docs/report/` |

## 9. Decisions (append; never delete)
| Date | Decision | Why |
|---|---|---|
| 2026-11-04 | Pretrained models only | Laptops only, short timeline |
| 2026-11-04 | Deploy in final phase, not earlier | Team decision |
| 2026-11-04 | English first, then French, Hindi, Sanskrit | Best tool support first |
| 2026-11-04 | Flask + SQLite | Matches synopsis |
| 2026-11-04 | Secrets only in `.env` (git-ignored); `.env.example` committed | Never publish keys |
