"""Record a short audio clip from the microphone and save as WAV.
OWNER: Role 2.  Usage:  python scripts/record_clip.py [seconds] [filename]

Requires: pip install sounddevice
Saves to data/raw/ (git-ignored). Creates the directory if needed.
"""
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

SAMPLE_RATE = 16_000
DEFAULT_SECONDS = 3
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"


def record(seconds: float = DEFAULT_SECONDS, sr: int = SAMPLE_RATE) -> np.ndarray:
    """Record *seconds* of mono audio at *sr* Hz. Returns float32 array."""
    import sounddevice as sd  # lazy: not everyone has a mic

    print(f"🎙️  Recording for {seconds}s at {sr} Hz … speak now!")
    audio = sd.rec(int(seconds * sr), samplerate=sr, channels=1, dtype="float32")
    sd.wait()
    print("✅  Done recording.")
    return audio.flatten()


def main() -> None:
    seconds = float(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SECONDS
    filename = sys.argv[2] if len(sys.argv) > 2 else "clip.wav"

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / filename

    audio = record(seconds)
    sf.write(str(out_path), audio, SAMPLE_RATE)
    print(f"💾  Saved to {out_path}  ({len(audio)/SAMPLE_RATE:.1f}s, {SAMPLE_RATE} Hz)")


if __name__ == "__main__":
    main()
