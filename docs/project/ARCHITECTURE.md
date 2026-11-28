# System Architecture: Language Coach

This document details the modular software architecture, data pipelines, sequence interactions, data contracts, and design rationales for the **Language Coach** pronunciation assessment system.

---

## 1. End-to-End System Pipeline

```mermaid
flowchart TD
    subgraph Client["Client Tier (Browser — No CDNs, Fully Offline)"]
        UI["Web Interface (HTML5 / Vanilla JS / CSS)"]
        TTS["SpeechSynthesis API (Native Reference Audio)"]
        Converter["In-Browser AudioContext (16 kHz Mono PCM WAV Encoder)"]
        Visualizer["AnalyserNode (Live Waveform + RMS Volume Meter)"]
    end

    subgraph Server["Application Tier (Flask REST API)"]
        Router["Flask Blueprint (app/routes/practice.py)"]
        Validation["RIFF WAVE & 15s Duration Validator"]
        DB[(SQLite Database: instance/coach.db)]
    end

    subgraph MLEngine["ML & Scoring Engine (ml/)"]
        Pipeline["ml.pipeline.assess()"]
        
        subgraph ReferenceModule["Reference Engine (ml/reference)"]
            RefG2P["reference_phonemes.get_reference_phonemes()"]
            Espeak["eSpeak NG via phonemizer"]
            SymbolNorm["phoneme_map.normalize_symbol_set()"]
            MockRef["Mock Splitter (USE_MOCK_ML=1)"]
        end

        subgraph SpeechModule["Speech Recognizer (ml/speech)"]
            AudioPrep["audio_utils (16kHz load, trim silence, normalise)"]
            RecEng["recognizer.recognize_phonemes()"]
            Model["wav2vec 2.0 (facebook/wav2vec2-lv-60-espeak-cv-ft)"]
            Singleton["CPU Memory Model Cache (Loaded Once)"]
            MockRec["Mock Recognizer (USE_MOCK_ML=1)"]
        end

        subgraph ScoringModule["Scoring Engine (ml/scoring)"]
            Aligner["SequenceMatcher Dynamic Alignment"]
            Matrix["Weighted Cost Matrix (Similar Sounds: 0.5 Credit)"]
            Attribution["Per-Word Sound Splitter"]
            FeedbackGen["Actionable Advice Generator"]
        end
    end

    UI -->|"1. Select curriculum item"| Router
    Router -->|"Content JSON"| UI
    UI -->|"2. Hear reference speech"| TTS
    UI -->|"3. Record voice"| Visualizer
    Visualizer -->|"Raw mic stream"| Converter
    Converter -->|"4. POST /api/assess (WAV file + text + lang)"| Router
    Router --> Validation
    Validation -->|"5. Temporary .wav file"| Pipeline

    Pipeline -->|"Target phrase"| RefG2P
    RefG2P --> Espeak --> SymbolNorm
    RefG2P -.->|"USE_MOCK_ML=1"| MockRef

    Pipeline -->|"Audio path"| AudioPrep
    AudioPrep --> RecEng
    RecEng --> Singleton --> Model
    RecEng -.->|"USE_MOCK_ML=1"| MockRec

    Pipeline -->|"Expected & Spoken IPA"| Aligner
    Aligner --> Matrix --> Attribution --> FeedbackGen
    FeedbackGen -->|"AssessmentResult JSON"| Router
    Router -->|"Save attempt"| DB
    Router -->|"6. Render sound chips & score ring"| UI
```

---

## 2. Sequence Diagram: A Single Practice Attempt

```mermaid
sequenceDiagram
    autonumber
    actor Learner as User
    participant Browser as Web Browser (UI)
    participant WebAudio as Web Audio API
    participant Server as Flask Server
    participant Pipeline as ML Pipeline
    participant Recognizer as wav2vec 2.0 Recognizer
    participant Scorer as Weighted Scorer
    participant Database as SQLite (coach.db)

    Learner->>Browser: Selects Language & Target ("ship")
    Learner->>Browser: Clicks "Listen" button
    Browser->>Browser: speechSynthesis.speak("ship")
    
    Learner->>Browser: Clicks "Record" (Mic icon)
    Browser->>WebAudio: Captures mic stream (MediaRecorder)
    WebAudio-->>Browser: Feeds AnalyserNode (Live Waveform + Timer)
    
    Learner->>Browser: Clicks "Stop & Check"
    Browser->>WebAudio: Decodes WebM & resamples to 16 kHz Mono WAV
    Browser->>Server: POST /api/assess (FormData: audio.wav, text="ship", language="english")
    
    Server->>Server: Validates RIFF/WAVE header & duration (< 15s)
    Server->>Pipeline: assess(tmp_wav_path, "ship", "english")
    
    Pipeline->>Pipeline: Extract Reference IPA via eSpeak NG -> ["ʃ", "ɪ", "p"]
    Pipeline->>Recognizer: recognize_phonemes(tmp_wav_path)
    Recognizer->>Recognizer: Audio normalisation & CPU acoustic inference
    Recognizer-->>Pipeline: Spoken IPA -> ["s", "ɪ", "p"]
    
    Pipeline->>Scorer: score_pronunciation(["ʃ", "ɪ", "p"], ["s", "ɪ", "p"])
    Scorer->>Scorer: Detects /s/ vs /ʃ/ (Weighted similarity = 0.5)
    Scorer->>Scorer: Computes word score (83%) & feedback tip
    Scorer-->>Pipeline: Returns AssessmentResult
    
    Pipeline-->>Server: JSON object with timing telemetry
    Server->>Database: INSERT attempt into attempts table
    Server->>Server: Deletes temporary WAV file (try/finally)
    Server-->>Browser: HTTP 200 JSON Response
    
    Browser->>Learner: Animates Score Ring, Green/Red Sound Chips & Coaching Tip
```

---

## 3. Module Responsibilities & Folder Boundaries

| Module | Files | Responsibility | Role Owner |
|---|---|---|---|
| **API & Routing** | `app/routes/practice.py` | Validates file uploads, handles page routing (`/`, `/practice`, `/progress`), invokes ML pipeline, returns JSON. | R4 |
| **Web Presentation** | `app/templates/*`, `app/static/*` | Glassmorphic UI, theme toggle, live waveform visualizer, client WAV conversion, progress chart. | R4 |
| **Database Access** | `app/db.py` | Thread-safe SQLite attempt persistence and querying. | R4 |
| **ML Glue** | `ml/pipeline.py` | Orchestrates reference extraction, recognition, and scoring with per-stage timing metrics. | R1 |
| **Data Contracts** | `ml/contracts.py` | Immutable dataclasses defining interchange formats. | R1 |
| **Speech Preprocessing** | `ml/speech/audio_utils.py` | 16 kHz mono loading, silence trimming (top-db=30), peak normalisation. | R2 |
| **Acoustic Recognizer** | `ml/speech/recognizer.py` | Pretrained wav2vec 2.0 acoustic phone decoder with singleton CPU model cache. | R2 |
| **Reference Phonemes** | `ml/reference/reference_phonemes.py` | Cross-lingual IPA generation via eSpeak NG / phonemizer with LRU cache. | R3 |
| **Phoneme Normalizer** | `ml/reference/phoneme_map.py` | Symbol set harmonization (vowel lengths, atomic diphthongs, stress stripping). | R3 |
| **Weighted Scorer** | `ml/scoring/scorer.py` | Levenshtein alignment with similarity cost matrix, multi-word scoring, and human feedback. | R3 |
| **Curriculum Content** | `data/content/*.json` | Curated beginner, intermediate, and advanced phrases across 4 languages. | R5 |

---

## 4. API Endpoints

| Endpoint | Method | Input Parameters | Output Format | Description |
|---|---|---|---|---|
| `/` | `GET` | None | HTML | Landing page with hero section and language cards. |
| `/practice` | `GET` | Optional query: `?lang=english` | HTML | Interactive practice studio. |
| `/progress` | `GET` | None | HTML | Learner dashboard with stats and canvas chart. |
| `/api/languages` | `GET` | None | JSON `list[str]` | Lists supported languages (`["english", "hindi", "sanskrit", "french"]`). |
| `/api/content/<language>` | `GET` | Language path param | JSON `object` | Returns tiered word curriculum for the specified language. |
| `/api/assess` | `POST` | `multipart/form-data`: `audio` (WAV file), `language` (str), `text` (str) | JSON `AssessmentResult` | Executes end-to-end pronunciation assessment. |
| `/api/progress` | `GET` | None | JSON `list[dict]` | Returns historical practice attempts ordered by date desc. |

---

## 5. Database Schema

The system uses an embedded SQLite database (`instance/coach.db`) with a single table:

```sql
CREATE TABLE IF NOT EXISTS attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    language TEXT,
    target_text TEXT,
    overall_score REAL,
    result_json TEXT
);
```

---

## 6. Data Contracts (`ml/contracts.py`)

Inter-module communication is governed by three strictly typed dataclasses:

```python
@dataclass
class PhonemeResult:
    expected: str      # Expected IPA phoneme symbol (e.g. "ʃ")
    spoken: str        # Spoken IPA phoneme detected (e.g. "s")
    correct: bool      # True if matched or close phonetic equivalent

@dataclass
class WordResult:
    word: str                     # Individual word in target phrase
    score: float                  # Word accuracy score (0.0 to 100.0)
    phonemes: list[PhonemeResult] # Attributed phoneme breakdown

@dataclass
class AssessmentResult:
    language: str              # Target language
    target_text: str           # Full target phrase
    overall_score: float       # Overall pronunciation score (0.0 to 100.0)
    words: list[WordResult]    # Sound-by-sound word attribution
    feedback: list[str]        # Human-readable coaching tips
    timing: dict = None        # Sub-second latency breakdown (seconds)
```

---

## 7. Key Architectural Decisions & Rationales

| Decision | Alternative Considered | Rationale |
|---|---|---|
| **Pretrained Models Only** | Training ASR from scratch | Training requires massive GPU clusters, labeled audio datasets, and months of compute. Pretrained models provide state-of-the-art representations immediately on CPU. |
| **CPU-Only Execution** | GPU / CUDA dependencies | Final-year evaluation laptops vary widely; student hardware often lacks NVIDIA GPUs. Forcing CPU compatibility ensures 100% portable, reproducible demonstrations. |
| **Client-Side WAV Resampling** | Server-side ffmpeg transcoding | Eliminates server-side subprocess calls, avoids external binary dependencies, and reduces backend server load by offloading audio decoding to the browser `AudioContext`. |
| **Flask Microframework** | Django / FastAPI | Minimal overhead, zero boilerplate, built-in Jinja2 templating, and ideal for single-node embedded desktop / localhost demonstrations. |
| **SQLite Embedded Database** | PostgreSQL / MySQL | Zero external service setup, file-based portability, and sub-millisecond query performance for individual learner history. |
| **Weighted Substitution Matrix** | Strict Binary String Match | In natural human articulation, substituting `/s/` for `/ʃ/` is a minor sibilant near-miss, whereas substituting `/k/` is a severe error. Weighted scoring reflects pedagogical phonetic reality. |
