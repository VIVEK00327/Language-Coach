# System Architecture: Language Coach

This document details the architectural components, data pipelines, and interaction flows for the **Language Coach** multilingual pronunciation assessment system.

---

## 1. End-to-End System Pipeline

```mermaid
flowchart TD
    subgraph Client["Client Tier (Browser)"]
        UI["Web Interface (HTML5 / Vanilla JS / CSS)"]
        TTS["SpeechSynthesis API (Audio Reference)"]
        REC["MediaRecorder + Web Audio API (16 kHz Mono WAV)"]
    end

    subgraph Server["Application Tier (Flask REST API)"]
        Router["Flask Routes (/api/assess, /api/languages, /api/content)"]
        DB[(SQLite Database instance/coach.db)]
    end

    subgraph MLEngine["ML & Scoring Engine (ml/)"]
        Pipeline["ml.pipeline.assess()"]
        
        subgraph ReferenceModule["Reference Phonemes (R3)"]
            RefEng["ml.reference.get_reference_phonemes()"]
            Espeak["phonemizer + eSpeak NG"]
            MockRef["Mock Character Splitter (Fallback)"]
        end

        subgraph SpeechModule["Speech Recognizer (R2)"]
            AudioPrep["ml.speech.audio_utils (load, trim, normalise)"]
            RecEng["ml.speech.recognize_phonemes()"]
            Model["wav2vec 2.0 / Whisper Phoneme Model (Cached on CPU)"]
            MockRec["Mock Recognizer (Fallback)"]
        end

        subgraph ScoringModule["Scoring & Feedback (R3)"]
            Aligner["Sequence Alignment (difflib / Levenshtein)"]
            WeightMatrix["Weighted Similarity Matrix (Voicing / Sibilants / Vowels)"]
            WordSplitter["Per-Word Sound Attribution"]
            FeedbackGen["Actionable Feedback Generator"]
        end
    end

    UI -->|"1. Request content & target text"| Router
    Router -->|"Content JSON"| UI
    UI -->|"2. Hear target pronunciation"| TTS
    UI -->|"3. Record voice"| REC
    REC -->|"4. POST /api/assess (multipart WAV + text + lang)"| Router

    Router -->|"5. assess(audio, text, lang)"| Pipeline
    Pipeline -->|"Extract target phonemes"| RefEng
    RefEng --> Espeak
    RefEng -.->|"USE_MOCK_ML=1"| MockRef

    Pipeline -->|"Extract spoken phonemes"| RecEng
    RecEng --> AudioPrep --> Model
    RecEng -.->|"USE_MOCK_ML=1"| MockRec

    RefEng -->|"Expected IPA list"| Aligner
    RecEng -->|"Spoken IPA list"| Aligner

    Aligner --> WeightMatrix --> WordSplitter --> FeedbackGen
    FeedbackGen -->|"AssessmentResult Object"| Pipeline
    Pipeline -->|"AssessmentResult JSON"| Router
    Router -->|"Save attempt record"| DB
    Router -->|"Return JSON response"| UI
    UI -->|"6. Render visual score chips & feedback tips"| UI
```

---

## 2. Sequence Diagram: Single Practice Attempt

```mermaid
sequenceDiagram
    autonumber
    actor Learner as User
    participant Browser as Client UI (Browser)
    participant WebAudio as Web Audio API
    participant Flask as Flask Server (app/routes)
    participant Pipeline as ML Pipeline (ml.pipeline)
    participant Ref as Reference Engine (ml.reference)
    participant ASR as Speech Recognizer (ml.speech)
    participant Scorer as Scorer Engine (ml.scoring)
    participant DB as SQLite DB (app/db)

    Learner->>Browser: Selects Language & Target Text (e.g., "ship")
    Browser->>Learner: Plays Reference Pronunciation via Web Speech Synthesis
    Learner->>Browser: Clicks "Record" and speaks into microphone
    Learner->>Browser: Clicks "Stop Recording"
    Browser->>WebAudio: Decodes PCM & Encodes into 16 kHz Mono WAV
    Browser->>Flask: POST /api/assess (WAV file, text="ship", language="english")
    
    Flask->>Pipeline: assess(temp_wav_path, "ship", "english")
    
    par Extract Expected Phonemes
        Pipeline->>Ref: get_reference_phonemes("ship", "english")
        Ref-->>Pipeline: Expected IPA: ['ʃ', 'ɪ', 'p']
    and Extract Spoken Phonemes
        Pipeline->>ASR: recognize_phonemes(temp_wav_path, "english")
        ASR-->>Pipeline: Spoken IPA: ['s', 'ɪ', 'p']
    end

    Pipeline->>Scorer: score_words(["ship"], [['ʃ', 'ɪ', 'p']], ['s', 'ɪ', 'p'])
    Note over Scorer: Aligns /ʃ/ with /s/ -> Phonetically similar (weight 0.5)<br/>Aligns /ɪ/ with /ɪ/ -> Match (1.0)<br/>Aligns /p/ with /p/ -> Match (1.0)<br/>Word score = 83.3%
    Scorer-->>Pipeline: WordResult + Feedback: "You said /s/ in 'ship'; expected /ʃ/."
    
    Pipeline-->>Flask: AssessmentResult(overall_score=83.3, words=[...], feedback=[...])
    Flask->>DB: save_attempt(AssessmentResult)
    DB-->>Flask: Confirmation
    Flask-->>Browser: JSON response (200 OK)
    
    Browser->>Learner: Displays overall score (83%), color-coded sound chips, and advice
```
