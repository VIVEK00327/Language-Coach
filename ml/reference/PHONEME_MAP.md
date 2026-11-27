# Phoneme Mapping & Normalization Specification (R3-03)

**Author:** Role 3 (Reference Phonemes & Scoring)  
**Modules:** `ml/reference/phoneme_map.py`, `ml/reference/reference_phonemes.py`, `ml/scoring/scorer.py`

---

## 1. Objective
Acoustic speech recognizers (such as wav2vec 2.0 or Whisper) and dictionary/G2P engines (such as eSpeak NG via `phonemizer`) often represent phonetic symbols with minor typographical and convention discrepancies. This specification ensures both pipelines output a **standardized, aligned symbol set** before phonetic distance calculation.

---

## 2. Normalization Rules

### A. Length Mark Binding
- **Convention:** The IPA length mark `ː` (and ASCII `:`) represents elongated vowel duration.
- **Rule:** Length marks must not exist as independent tokens in the phoneme list. They are attached to the immediately preceding vowel:
  - `['i', 'ː']` $\rightarrow$ `['iː']` (as in *sheep* `/ʃ iː p/`)
  - `['u', 'ː']` $\rightarrow$ `['uː']` (as in *pool* `/p uː l/`)
  - `['ɔ', 'ː']` $\rightarrow$ `['ɔː']` (as in *water* `/w ɔː t ə/`)
  - `['ɑ', 'ː']` $\rightarrow$ `['ɑː']` (as in *father* `/f ɑː ð ə/`)

### B. Atomic Diphthongs
- **Convention:** Diphthongs represent a glide between two vowel targets within the same syllable.
- **Rule:** Two-character diphthongs are preserved as atomic tokens:
  - `/oʊ/` (as in *boat*, *hello*)
  - `/aɪ/` (as in *bite*, *wine*)
  - `/eɪ/` (as in *bait*, *day*)
  - `/aʊ/` (as in *cow*, *shout*)
  - `/ɔɪ/` (as in *boy*, *choice*)
  - Centering diphthongs: `/ɪə/`, `/eə/`, `/ʊə/`

### C. Atomic Affricates
- **Rule:** Affricates are treated as single combined consonant phones:
  - `/tʃ/` (voiceless postalveolar affricate, as in *cheap*, *chair*)
  - `/dʒ/` (voiced postalveolar affricate, as in *joy*, *jump*)

### D. Stress and Formatting Stripping
- **Rule:** Primary stress (`ˈ`), secondary stress (`ˌ`), apostrophes (`'`), and whitespace are stripped prior to scoring.
  - eSpeak output `həlˈoʊ` $\rightarrow$ `['h', 'ə', 'l', 'oʊ']`

### E. American Flap (/ɾ/) Handling
- **Convention:** In North American English, intervocalic `/t/` and `/d/` are frequently pronounced as the alveolar flap `/ɾ/` (e.g. *water* $\rightarrow$ `[wɑːɾɚ]`).
- **Scoring Rule:** `/ɾ/` is aligned as phonetically similar to both `/t/` and `/d/` with a similarity weight of $0.5$ (partial credit), ensuring American English speakers are not heavily penalized.

---

## 3. Phonetic Similarity Matrix (Extract)

| Spoken Sound | Expected Sound | Relationship | Similarity Credit |
|---|---|---|---|
| `/s/` | `/ʃ/` | Sibilant place confusion (*sip* vs *ship*) | **0.5** |
| `/ɾ/` | `/t/` | Alveolar flap vs voiceless plosive (*water*) | **0.5** |
| `/ɾ/` | `/d/` | Alveolar flap vs voiced plosive (*ladder*) | **0.5** |
| `/p/` | `/b/` | Voicing pair (bilabial plosive) | **0.5** |
| `/t/` | `/d/` | Voicing pair (alveolar plosive) | **0.5** |
| `/k/` | `/g/` | Voicing pair (velar plosive) | **0.5** |
| `/v/` | `/w/` | Labiodental fricative vs labial-velar approximant | **0.5** |
| `/i/` | `/ɪ/` | Tense vs lax close front vowel (*sheep* vs *ship*) | **0.5** |
| `/u/` | `/ʊ/` | Tense vs lax close back vowel (*fool* vs *full*) | **0.5** |
