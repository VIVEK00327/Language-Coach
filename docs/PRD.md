# PRD: Language Coach (Product Requirements)
> Read only the section you need. Sections: 1 Overview | 2 Features | 3 Requirements | 4 Architecture | 5 Languages | 6 Stack | 7 Timeline | 8 Roles | 9 Decisions

## 1. Overview
**Title:** Language Coach: AI-Based Multilingual Pronunciation Learning System
**Program:** B.Tech CSE, session 2026-27, Dept. of Computer Engineering & Applications. **Team:** 5.
**Duration (synopsis):** Nov 2026 - Apr 2027 (6 months). **Milestone:** 30-40% progress checkpoint completed by 30 Nov 2026. **Deployment:** final phase only (Mar-Apr 2027).
Web app: user picks a language + word/sentence from tiered curricula, hears reference pronunciation, records speech, gets automated sound-by-sound feedback, and a score. Practice activities + progress dashboard. Languages: English, Hindi, Sanskrit, French first; Latin, Spanish, German in future expansion. Motivation: learners lack immediate pronunciation feedback; this unifies practice, recording and diagnostic feedback without costly cloud GPUs.
Out of scope: training speech models from scratch, native mobile app (responsive web instead), real-time streaming scoring, extra languages (unless time permits).

## 2. Features (priority)
| ID | Feature | Priority | Current Status |
|---|---|---|---|
| F1 | Select language (English, Hindi, Sanskrit, French) | Must | **DONE** |
| F2 | Select/enter word or sentence from content list | Must | **DONE** |
| F3 | Reference pronunciation playback (Web Speech Synthesis) | Must | **DONE** |
| F4 | Browser recording and submit (in-browser 16 kHz WAV encoding) | Must | **DONE** |
| F5 | Overall score (0-100), per-word score, per-sound correct/incorrect | Must | **DONE** |
| F6 | Readable feedback (expected vs spoken sound chips) | Must | **DONE** |
| F7 | Attempt history in local SQLite database | Must | **DONE** |
| F8 | Progress dashboard with HTML5 canvas score trend line chart | Should | **DONE** |
| F9 | Practice activities (beginner, intermediate, advanced tiers) | Should | **DONE** |
| F10 | Multi-user authentication & learner accounts | Could | Planned (Spring) |
| F11 | LLM-written extended feedback | Could | Optional Phase 2 |
| F12 | Latin, Spanish, German expansion | Could | Future roadmap |

## 3. Requirements
- Score a clip under 10 s in about 1-2 s on standard laptop CPU (no GPU required). Memory footprint < 2 GB RAM.
- ML code independent of Flask; Flask has no scoring logic. Config only through environment variables (`.env`).
- Adding a language = content JSON (`data/content/<lang>.json`) + reference-phoneme config + recognizer setting.
- Pinned `requirements.txt`; README quick start works on a fresh machine; automated tests for scorer, API, and setup.
- Hardware: 4 GB RAM min (8 GB recommended), microphone, speakers. OS: Windows 10/11, macOS, or Linux.

## 4. Architecture
```
Browser (record, feedback) -> POST /api/assess -> app/routes -> ml/pipeline.assess()
  ml/reference  (expected phonemes) + ml/speech (spoken phonemes) -> ml/scoring (align, score)
  -> AssessmentResult JSON -> UI; attempt saved to SQLite (app/db.py)
```
**Contract (`ml/contracts.py`, do not change without lead):** `PhonemeResult(expected, spoken, correct)`,
`WordResult(word, score, phonemes)`, `AssessmentResult(language, target_text, overall_score, words, feedback, timing)`.
**Stable signatures:**
- `get_reference_phonemes(text, language) -> list[str]` (`ml/reference/reference_phonemes.py`, R3)
- `recognize_phonemes(audio_path, language) -> list[str]` (`ml/speech/recognizer.py`, R2)
- `score_pronunciation(expected, spoken) -> (overall, list[PhonemeResult])` (`ml/scoring/scorer.py`, R3)
- `assess(audio_path, target_text, language) -> AssessmentResult` (`ml/pipeline.py`, R1)
Mocks of the first two exist so everyone works in parallel from day 1 (`USE_MOCK_ML=1`).
**API:** GET `/api/languages`; GET `/api/content/<language>`; POST `/api/assess` (audio, language, text); GET `/api/progress`.
**DB:** table `attempts(id, created_at, language, target_text, overall_score, result_json)`.

## 5. Languages
Order: English -> French -> Hindi -> Sanskrit.
| Language | Expected phonemes | Recognition | Risk | Current Status |
|---|---|---|---|---|
| English | eSpeak NG (`en-us`) via `phonemizer` | `facebook/wav2vec2-lv-60-espeak-cv-ft` (CPU cached) | Low | **Functional** |
| French | eSpeak NG (`fr-fr`) via `phonemizer` | wav2vec 2.0 multilingual / Whisper | Low | Reference ready; ASR in progress |
| Hindi | eSpeak NG (`hi`) via `phonemizer` | Whisper / wav2vec 2.0 | Medium | Reference ready; ASR in progress |
| Sanskrit | Rule-based Devanagari G2P (eSpeak `hi`/`sa` proxy) | Multilingual phoneme model approximation | **High** | Hindi G2P proxy active; rule G2P in dev |

Sanskrit: no off-the-shelf ASR or large labeled corpora exist; do not train one from scratch. Rule-based G2P is realistic due to regular Devanagari phonology (vowel lengths, aspiration, retroflex vs dental, anusvara, visarga). Reference audio is recorded from native speakers/teachers.
Content files: `data/content/<language>.json` with `levels: {beginner, intermediate, advanced}` of `{text, note?}` (22+ items per language completed).

### Datasets for Evaluation
| Dataset | Target Languages | Primary Purpose | Status / Licensing |
|---|---|---|---|
| **speechocean762** | English (non-native learners) | Benchmark scoring algorithm against expert human pronunciation ratings | OpenSLR / Non-commercial research |
| **L2-ARCTIC** | English (L1 interference) | Test phonetic substitution detection across Hindi, Spanish, Mandarin accents | Non-commercial research |
| **Mozilla Common Voice** | English, French, Hindi | Test acoustic model robustness on diverse microphones and accents | CC0 Public Domain |
| **Sanskrit Corpora** | Sanskrit | Evaluate classical pronunciation, sandhi, and chanting | Teacher recordings / Curated evaluation clips |

## 6. Stack
Python 3.10+, Flask 3.1, SQLite 3, Librosa / SoundFile, Hugging Face `transformers` (wav2vec 2.0 `facebook/wav2vec2-lv-60-espeak-cv-ft`), `phonemizer` + eSpeak NG, Web Audio API (`AudioContext`), vanilla HTML5/CSS3, `pytest`, `python-dotenv`.

## 7. Timeline
Synopsis phases: Requirements & planning (Nov-Dec); Content & setup (Nov-Dec); Audio pipeline & UI (Dec-Jan); Core app & ML (Dec-Feb); Integration, testing, evaluation (Feb-Mar); Documentation & final demo (Mar-Apr); **Deployment** (Mar-Apr, last).
**30 Nov milestone completed:** English end-to-end local execution with real wav2vec 2.0 recognizer; 4-language word lists; glassmorphic UI; progress dashboard; in-browser WAV encoding; 40 passing tests.
Later: Dec Hindi/French ASR testing, speechocean762 correlation; Jan Sanskrit rule-based G2P, scoring refinements; Feb user evaluation; Mar packaging; Apr final thesis/viva.

## 8. Roles (owners; edit only your own folders)
| Role | Name | Owns |
|---|---|---|
| R1 | Lead / integration | `ml/contracts.py`, `ml/pipeline.py`, repo, MEMORY status block, requirements |
| R2 | Speech model | `ml/speech/`, `tests/test_recognizer.py`, `tests/test_audio_utils.py` |
| R3 | Reference + scoring | `ml/reference/`, `ml/scoring/`, `tests/test_scorer.py`, `tests/test_phoneme_map.py` |
| R4 | App / UI | `app/`, `tests/test_api.py`, client JS/CSS |
| R5 | Data, evaluation, report | `data/content/`, `evaluation/`, `scripts/`, `docs/report/` |

## 9. Decisions (append; never delete)
| Date | Decision | Why |
|---|---|---|
| 2026-11-04 | Pretrained models only | Laptops only, short timeline |
| 2026-11-04 | Deploy in final phase, not earlier | Team decision |
| 2026-11-04 | English first, then French, Hindi, Sanskrit | Best tool support first |
| 2026-11-04 | Flask + SQLite | Matches synopsis |
| 2026-11-04 | Secrets only in `.env` (git-ignored); `.env.example` committed | Never publish keys |
| 2026-11-26 | Weighted substitution scoring matrix | Minor phonetic near-misses (e.g. s/ʃ) deserve partial credit (0.5) |
| 2026-11-27 | Pretrained wav2vec 2.0 (`lv-60-espeak-cv-ft`) on CPU | Decodes raw IPA without language model over-correction |
| 2026-11-27 | In-browser 16 kHz mono WAV conversion via AudioContext | Eliminates server-side ffmpeg subprocess dependencies |
| 2026-11-28 | Unified glassmorphic SaaS design system | Consistent, accessible visual identity across all views with instant zero-FOUT theme toggle |
