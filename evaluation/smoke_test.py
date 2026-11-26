"""Smoke test runner for real/mock pipeline on local audio clips.
OWNER: Role 1 (Prep for R1-07).

Scans data/raw/ (git-ignored) for .wav files, derives target text and language from
the filename, runs ml.pipeline.assess(), and prints a formatted performance table.

Example file naming conventions:
  ship_correct.wav       -> text: "ship", language: "english"
  water_wrong.wav         -> text: "water", language: "english"
  french_bonjour.wav      -> text: "bonjour", language: "french"
  hindi_namaste.wav       -> text: "नमस्ते", language: "hindi"
"""
import os
import sys
import time
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ml.pipeline import assess


RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
SUPPORTED_LANGUAGES = ["english", "hindi", "sanskrit", "french"]


def parse_filename(filename: str):
    """Derive target text and language from a filename."""
    stem = Path(filename).stem.lower()

    # Detect language prefix if present
    language = "english"
    for lang in SUPPORTED_LANGUAGES:
        if stem.startswith(f"{lang}_"):
            language = lang
            stem = stem[len(lang) + 1:]
            break

    # Strip standard evaluation suffixes
    for suffix in ["_correct", "_wrong", "_test", "-correct", "-wrong", "-test"]:
        if stem.endswith(suffix):
            stem = stem[:-len(suffix)]
            break

    # Clean up underscores into spaces for multi-word targets
    target_text = stem.replace("_", " ").strip()
    return target_text, language


def run_smoke_test():
    print("=" * 80)
    print("Language Coach - Pipeline Smoke Test (R1-07 Prep)")
    print(f"Scanning directory: {RAW_DATA_DIR}")
    print("=" * 80)

    if not RAW_DATA_DIR.exists():
        RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    wav_files = sorted(list(RAW_DATA_DIR.glob("*.wav")))

    if not wav_files:
        print(f"\n[INFO] No .wav files found in {RAW_DATA_DIR}")
        print("Record sample clips using:")
        print("  python scripts/record_clip.py 3 ship_correct.wav")
        print("  python scripts/record_clip.py 3 water_wrong.wav")
        print("\nRunning self-check on synthetic test sample...")

        # Create temporary dummy WAV for self-validation
        import tempfile
        import numpy as np
        import soundfile as sf

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_wav = tmp.name
            t = np.linspace(0, 1.0, 16000, endpoint=False, dtype=np.float32)
            sine = 0.5 * np.sin(2 * np.pi * 440 * t)
            sf.write(tmp_wav, sine, 16000)

        wav_files = [Path(tmp_wav)]
        is_synthetic = True
    else:
        is_synthetic = False

    header = f"{'File':<25} | {'Lang':<9} | {'Target':<15} | {'Score':<7} | {'Time (s)':<9} | {'Feedback Snippet'}"
    print(header)
    print("-" * len(header))

    total_time = 0.0

    for wav_path in wav_files:
        fname = "synthetic_sample.wav" if is_synthetic else wav_path.name
        target_text, language = parse_filename(fname)
        if not target_text:
            target_text = "water"

        start_time = time.perf_counter()
        result = assess(str(wav_path), target_text, language)
        elapsed = time.perf_counter() - start_time
        total_time += elapsed

        first_tip = result.feedback[0] if result.feedback else "No feedback"
        if len(first_tip) > 28:
            first_tip = first_tip[:25] + "..."

        print(
            f"{fname:<25} | {result.language:<9} | {result.target_text:<15} | "
            f"{result.overall_score:<7.1f} | {elapsed:<9.3f} | {first_tip}"
        )

    print("-" * len(header))
    print(f"Processed {len(wav_files)} clip(s) in {total_time:.3f} seconds total.")
    print("=" * 80)


if __name__ == "__main__":
    run_smoke_test()
