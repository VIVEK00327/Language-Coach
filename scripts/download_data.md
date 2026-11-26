# Dataset Acquisition Guide: Language Coach

> **STRICT RULE:** Raw audio and external datasets are **never committed to Git**.  
> All downloaded datasets reside in `data/eval/` or `data/raw/`, which are ignored by `.gitignore`.

This guide outlines step-by-step instructions for acquiring the evaluation datasets referenced in Section 5 of `docs/PRD.md`.

---

## 1. Directory Structure Setup

Before downloading, ensure local directories exist outside version control:
```bash
mkdir -p data/eval/speechocean762
mkdir -p data/eval/l2arctic
mkdir -p data/eval/common_voice
mkdir -p data/raw
```

---

## 2. speechocean762 (Benchmark Scoring Corpus)

- **Coverage:** ~5,000 non-native English utterances graded by human experts.
- **Source:** OpenSLR resource 101 or via Hugging Face Datasets.
- **Download via Python (Hugging Face):**
  ```python
  # Ensure: pip install datasets soundfile
  from datasets import load_dataset

  # Download metadata and audio
  dataset = load_dataset("speechocean/speechocean762", split="test")
  print("Sample loaded:", dataset[0]["text"])
  ```
- **Direct Archive Download:**
  1. Visit: https://www.openslr.org/101/
  2. Download `speechocean762.tar.gz`.
  3. Extract contents into `data/eval/speechocean762/`.

---

## 3. L2-ARCTIC (L1 Interference & Phoneme Errors)

- **Coverage:** Non-native English recordings across 24 speakers (Hindi, Spanish, Arabic, Mandarin, Korean, Vietnamese).
- **Source:** University of Washington / GitHub repository.
- **Download via Git/Direct Download:**
  ```bash
  # Clone into temporary staging area (do not clone inside git repository)
  git clone https://github.com/psiang/L2-ARCTIC.git /tmp/l2arctic
  # Copy selected speaker recordings (e.g. Hindi L1 speaker 'HKK') to data/eval/
  cp -r /tmp/l2arctic/data/HKK data/eval/l2arctic/
  ```

---

## 4. Mozilla Common Voice (Multilingual Robustness)

- **Coverage:** Verified recordings in English, French, and Hindi under CC0.
- **Source:** https://commonvoice.mozilla.org/datasets
- **Steps:**
  1. Log into Mozilla Common Voice portal.
  2. Select target language (e.g., Hindi or French).
  3. Download the specific language bundle `.tar.gz`.
  4. Extract a small sample subset (10–20 validated clips) into `data/eval/common_voice/<language>/`.

---

## 5. Sanskrit Empirical Recordings

- **Coverage:** Classical Sanskrit shlokas, sandhi variations, and mantras.
- **Procedure:**
  1. Record clips directly using `python scripts/record_clip.py 4 sanskrit_shanti.wav`.
  2. Verify correct phonetic articulation with a qualified Sanskrit instructor.
  3. Save labelled clips in `data/raw/` for local evaluation.
