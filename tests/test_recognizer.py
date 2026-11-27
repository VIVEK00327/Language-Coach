"""Tests for speech recognizer (R2-04): mock vs real execution."""
import os
from unittest.mock import MagicMock
import numpy as np
import pytest
import soundfile as sf
import torch

from ml.speech.recognizer import recognize_phonemes


def _make_dummy_wav(path: str) -> None:
    t = np.linspace(0, 0.5, 8000, endpoint=False, dtype=np.float32)
    tone = 0.5 * np.sin(2 * np.pi * 440 * t)
    sf.write(path, tone, 16000)


def test_mock_recognizer_returns_mock_data(monkeypatch, tmp_path):
    monkeypatch.setenv("USE_MOCK_ML", "1")
    wav_file = str(tmp_path / "test.wav")
    _make_dummy_wav(wav_file)

    res = recognize_phonemes(wav_file, language="english")
    assert res == ["w", "o", "t", "e", "r"]


def test_real_recognizer_never_silently_returns_mock_on_failure(monkeypatch, tmp_path):
    """When USE_MOCK_ML=0, any failure must raise RuntimeError instead of silently returning mock."""
    monkeypatch.setenv("USE_MOCK_ML", "0")
    monkeypatch.setenv("PHONEME_MODEL_NAME", "invalid/nonexistent-model-name")

    wav_file = str(tmp_path / "test.wav")
    _make_dummy_wav(wav_file)

    # Reset any cached model to trigger fresh loading
    import ml.speech.recognizer as rec_mod
    rec_mod._MODEL = None
    rec_mod._PROCESSOR = None

    with pytest.raises(RuntimeError) as exc_info:
        recognize_phonemes(wav_file, language="english")

    assert "Failed to load speech phoneme model" in str(exc_info.value)
    # Ensure it NEVER returned the mock data
    assert "w,o,t,e,r" not in str(exc_info.value)


def test_real_recognizer_decodes_model_output(monkeypatch, tmp_path):
    """Verify that when real model inference runs, its decoded output is returned."""
    monkeypatch.setenv("USE_MOCK_ML", "0")

    wav_file = str(tmp_path / "test.wav")
    _make_dummy_wav(wav_file)

    # Mock processor and model to simulate successful wav2vec2 CTC inference
    mock_processor = MagicMock()
    mock_inputs = MagicMock()
    mock_inputs.input_values = torch.zeros((1, 8000))
    mock_processor.return_value = mock_inputs
    mock_processor.batch_decode.return_value = ["ʃ ɪ p"]

    mock_model = MagicMock()
    mock_logits = MagicMock()
    mock_logits.logits = torch.zeros((1, 25, 32))
    mock_model.return_value = mock_logits

    import ml.speech.recognizer as rec_mod
    monkeypatch.setattr(rec_mod, "_MODEL", mock_model)
    monkeypatch.setattr(rec_mod, "_PROCESSOR", mock_processor)

    result = recognize_phonemes(wav_file, language="english")
    # Must decode the simulated model output, NOT the mock ['w', 'o', 't', 'e', 'r']
    assert result == ["ʃ", "ɪ", "p"]
    assert result != ["w", "o", "t", "e", "r"]
