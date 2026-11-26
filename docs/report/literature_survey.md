# Literature Survey: Multilingual Pronunciation Learning Systems

This survey outlines 10 core topics, algorithms, datasets, and tools relevant to the **Language Coach** project.  
*Note: In accordance with academic integrity guidelines, specific publication years, citation numbers, and author lists are not assumed or fabricated here; each entry specifies the core concepts to study, their architectural relevance, and is marked `[TO VERIFY]` for future formal bibliographic citation.*

---

### 1. Computer-Assisted Pronunciation Training (CAPT) Frameworks
- **What to look up:** Pedagogical principles of automated phonetic feedback, user interface designs for speech learners, difference between holistic fluency scoring versus fine-grained diagnostic phonetic feedback.
- **Why it is relevant:** Establishes the foundational requirements and educational workflow of Language Coach (providing actionable, phone-level guidance rather than just a pass/fail grade).
- **Status:** `[TO VERIFY]` — *Find canonical survey papers on CAPT system design and learner feedback efficacy.*

### 2. Goodness of Pronunciation (GOP) Scoring Algorithms
- **What to look up:** The formulation of Goodness of Pronunciation (GOP) metrics using acoustic model posterior probabilities (log-likelihood ratios of the target phone vs. all phonemes) calculated over forced alignments.
- **Why it is relevant:** GOP is the historical gold-standard baseline in pronunciation assessment; understanding its mathematical principles informs our similarity-weighted phonetic scoring and confidence calibration.
- **Status:** `[TO VERIFY]` — *Find foundational papers defining the GOP metric (e.g., Witt and Young).*

### 3. wav2vec 2.0 Self-Supervised Acoustic Representations
- **What to look up:** Self-supervised learning on raw speech audio, contrastive task pretraining, and subsequent fine-tuning with Connectionist Temporal Classification (CTC) for phoneme recognition.
- **Why it is relevant:** Pretrained wav2vec 2.0 and multilingual variants (such as XLS-R) allow high-accuracy phoneme emission on CPU without requiring massive task-specific labeled training datasets.
- **Status:** `[TO VERIFY]` — *Find primary publications introducing wav2vec 2.0 and multilingual XLS-R architectures.*

### 4. OpenAI Whisper and Weakly-Supervised Speech Models
- **What to look up:** Encoder-decoder Transformer architectures trained on large-scale multilingual audio with sequence-to-sequence objectives; quantized and optimized runtimes (such as faster-whisper / whisper.cpp).
- **Why it is relevant:** Serves as a robust primary or fallback acoustic model for non-English speech (French, Hindi) that can reliably operate on low-power consumer laptop hardware.
- **Status:** `[TO VERIFY]` — *Find original publication detailing the Whisper architecture and multilingual evaluation.*

### 5. Phoneme Recognition vs. Word-Level Automatic Speech Recognition (ASR)
- **What to look up:** The distinction between standard ASR (which relies on language models and beam search to correct phonetic errors into valid dictionary words) and phone recognition (which detects raw, ungrammatical, or mispronounced sounds).
- **Why it is relevant:** Language Coach must avoid language-model over-correction (which hides pronunciation errors); we need raw phonetic transcriptions to detect substitutions.
- **Status:** `[TO VERIFY]` — *Find literature addressing phone error rate (PER) and lexicon-free acoustic decoding in language education.*

### 6. speechocean762 Benchmark Dataset
- **What to look up:** Dataset composition, non-native English speaker demographics, expert human phonetic and fluency annotation schemes (pronunciation, completeness, fluency scores per phone, word, and sentence).
- **Why it is relevant:** Provides the benchmark ground truth needed to validate and correlate our automated scoring algorithm against human teacher grades.
- **Status:** `[TO VERIFY]` — *Find official documentation, release papers, and license agreement on OpenSLR.*

### 7. L2-ARCTIC Speech Corpus
- **What to look up:** Phonetically-balanced non-native English speech corpus recorded across multiple native language backgrounds (e.g., Hindi, Spanish, Mandarin, Arabic, Vietnamese); manual phone-level error annotations (substitutions, deletions, additions).
- **Why it is relevant:** Directly targets the phonetic transfer errors (L1 interference) that our weighted substitution matrix is designed to catch and evaluate.
- **Status:** `[TO VERIFY]` — *Find official publication describing the L2-ARCTIC corpus design and annotation standards.*

### 8. Mozilla Common Voice Crowdsourced Multilingual Corpus
- **What to look up:** The open-source, community-driven recording and validation pipeline, license model (Creative Commons Zero / CC0), and language coverage for regional and low-resource languages (Hindi, French).
- **Why it is relevant:** Provides diverse, real-world test audio containing varying acoustic environments, accents, and microphone hardware.
- **Status:** `[TO VERIFY]` — *Find published articles on Common Voice methodology and dataset releases.*

### 9. eSpeak NG Multilingual Grapheme-to-Phoneme (G2P) Engine
- **What to look up:** Rule-based grapheme-to-phoneme conversion algorithms, International Phonetic Alphabet (IPA) output representations, and dictionary lookup mechanisms across European and Indic languages.
- **Why it is relevant:** Powers `ml.reference.get_reference_phonemes` via `phonemizer`, generating standardized expected IPA target sequences without requiring heavy neural G2P models.
- **Status:** `[TO VERIFY]` — *Find software documentation and academic references describing eSpeak NG G2P rules.*

### 10. Phonetic Distance & Weighted Sequence Alignment
- **What to look up:** Levenshtein edit distance, Needleman-Wunsch sequence alignment, and phonological feature distance matrices (such as feature-weighted alignment using place, manner, and voicing).
- **Why it is relevant:** Justifies the mathematical weighting of our substitution penalties (e.g., granting partial credit for voicing and sibilant near-misses such as /s/ vs. /ʃ/) in `ml.scoring.scorer`.
- **Status:** `[TO VERIFY]` — *Find research papers applying phonological feature distance to alignment and pronunciation scoring.*
