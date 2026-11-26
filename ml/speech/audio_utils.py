"""Audio loading and preprocessing utilities. OWNER: Role 2.

Provides three functions used before feeding audio to the speech model:
  load_audio   – load any audio file as a 16 kHz mono float32 numpy array
  trim_silence – remove leading/trailing silence
  normalise    – scale waveform to [-1, 1]
"""
import logging
from pathlib import Path
from typing import Union

import numpy as np

log = logging.getLogger(__name__)

TARGET_SR = 16_000  # 16 kHz – the standard sample rate for speech models


def load_audio(path: Union[str, Path], sr: int = TARGET_SR) -> np.ndarray:
    """Load an audio file and return a 1-D float32 array at *sr* Hz.

    Uses soundfile (fast, no ffmpeg needed for wav/flac).
    Stereo is mixed down to mono by averaging channels.
    """
    import soundfile as sf

    data, file_sr = sf.read(str(path), dtype="float32", always_2d=True)
    # Mix to mono: average across channels (axis 1)
    if data.shape[1] > 1:
        data = data.mean(axis=1)
    else:
        data = data[:, 0]

    # Resample if sample rate differs
    if file_sr != sr:
        import librosa
        data = librosa.resample(data, orig_sr=file_sr, target_sr=sr)
        log.debug("Resampled %s from %d Hz to %d Hz", path, file_sr, sr)

    return data


def trim_silence(
    audio: np.ndarray,
    threshold_db: float = 30.0,
    frame_length: int = 2048,
    hop_length: int = 512,
) -> np.ndarray:
    """Remove leading and trailing silence from a waveform.

    *threshold_db* is how many dB below the peak counts as silence.
    Returns the trimmed waveform (may be empty if the whole clip is silent).
    """
    import librosa

    trimmed, _ = librosa.effects.trim(
        audio, top_db=threshold_db, frame_length=frame_length, hop_length=hop_length
    )
    return trimmed


def normalise(audio: np.ndarray) -> np.ndarray:
    """Peak-normalise a waveform to [-1, 1].

    If the signal is all zeros (silent), returns it unchanged.
    """
    peak = np.max(np.abs(audio))
    if peak < 1e-8:
        return audio
    return audio / peak
