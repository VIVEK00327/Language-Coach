"""Tests for audio_utils.py (R2-02). Uses a generated sine wave — no real audio needed."""
import numpy as np
import pytest
import tempfile
import soundfile as sf
from pathlib import Path

from ml.speech.audio_utils import load_audio, trim_silence, normalise, TARGET_SR


def _make_sine_wav(path: str, freq: float = 440.0, duration: float = 0.5,
                   sr: int = TARGET_SR, channels: int = 1) -> None:
    """Write a sine-wave WAV file for testing."""
    t = np.linspace(0, duration, int(sr * duration), endpoint=False, dtype=np.float32)
    wave = 0.5 * np.sin(2 * np.pi * freq * t)
    if channels > 1:
        wave = np.column_stack([wave] * channels)
    sf.write(path, wave, sr)


class TestLoadAudio:
    def test_loads_mono_16k(self, tmp_path):
        wav = str(tmp_path / "mono.wav")
        _make_sine_wav(wav, sr=TARGET_SR, channels=1)
        audio = load_audio(wav)
        assert audio.ndim == 1
        assert audio.dtype == np.float32
        assert len(audio) == int(TARGET_SR * 0.5)

    def test_stereo_to_mono(self, tmp_path):
        wav = str(tmp_path / "stereo.wav")
        _make_sine_wav(wav, sr=TARGET_SR, channels=2)
        audio = load_audio(wav)
        assert audio.ndim == 1

    def test_resamples_from_44100(self, tmp_path):
        wav = str(tmp_path / "hi_sr.wav")
        _make_sine_wav(wav, sr=44100, channels=1, duration=0.5)
        audio = load_audio(wav, sr=TARGET_SR)
        # Should be roughly 0.5s at 16 kHz
        expected_len = int(TARGET_SR * 0.5)
        assert abs(len(audio) - expected_len) < 100  # allow small rounding


class TestTrimSilence:
    def test_trims_leading_trailing(self):
        silence = np.zeros(TARGET_SR, dtype=np.float32)  # 1s silence
        tone = 0.5 * np.sin(2 * np.pi * 440 * np.linspace(0, 0.3, int(TARGET_SR * 0.3),
                            dtype=np.float32))
        audio = np.concatenate([silence, tone, silence])
        trimmed = trim_silence(audio)
        # Trimmed should be much shorter than original
        assert len(trimmed) < len(audio)
        assert len(trimmed) > 0

    def test_all_silent_returns_short(self):
        silent = np.zeros(TARGET_SR, dtype=np.float32)
        trimmed = trim_silence(silent)
        assert len(trimmed) <= len(silent)


class TestNormalise:
    def test_peak_becomes_one(self):
        audio = np.array([0.0, 0.25, -0.5, 0.1], dtype=np.float32)
        normed = normalise(audio)
        assert pytest.approx(np.max(np.abs(normed)), abs=1e-6) == 1.0

    def test_silent_unchanged(self):
        silent = np.zeros(100, dtype=np.float32)
        normed = normalise(silent)
        assert np.allclose(normed, silent)
