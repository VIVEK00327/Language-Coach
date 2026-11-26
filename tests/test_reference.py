"""Tests for real reference phonemes (R3-02). Requires espeak-ng installed."""
import os
import pytest
from ml.reference.reference_phonemes import get_reference_phonemes, SUPPORTED


class TestMockFallback:
    """When USE_MOCK_ML=1, the old letter-split behaviour must still work."""

    @pytest.fixture(autouse=True)
    def _set_mock(self, monkeypatch):
        monkeypatch.setenv("USE_MOCK_ML", "1")
        # reload flag at module level
        import ml.reference.reference_phonemes as mod
        monkeypatch.setattr(mod, "_USE_MOCK", True)

    def test_mock_returns_letters(self):
        result = get_reference_phonemes("hi", "english")
        assert result == ["h", "i"]

    def test_mock_unsupported_language(self):
        with pytest.raises(ValueError):
            get_reference_phonemes("hi", "klingon")


class TestRealPhonemes:
    """Real phonemizer + espeak-ng tests (skip if espeak-ng not installed)."""

    @pytest.fixture(autouse=True)
    def _unset_mock(self, monkeypatch):
        monkeypatch.delenv("USE_MOCK_ML", raising=False)
        import ml.reference.reference_phonemes as mod
        monkeypatch.setattr(mod, "_USE_MOCK", False)

    def _espeak_available(self):
        try:
            from phonemizer.backend import EspeakBackend
            EspeakBackend.is_available()
            return True
        except Exception:
            return False

    @pytest.fixture(autouse=True)
    def _skip_no_espeak(self):
        if not self._espeak_available():
            pytest.skip("espeak-ng not installed")

    def test_hello_english(self):
        result = get_reference_phonemes("hello", "english")
        assert isinstance(result, list)
        assert len(result) > 0
        # Should contain IPA characters, not plain ASCII letters like the mock
        joined = "".join(result)
        assert any(ord(c) > 127 for c in joined), f"Expected IPA chars, got: {joined}"

    def test_water_english(self):
        result = get_reference_phonemes("water", "english")
        assert isinstance(result, list)
        assert len(result) >= 3

    def test_french(self):
        result = get_reference_phonemes("bonjour", "french")
        assert isinstance(result, list)
        assert len(result) > 0

    def test_hindi(self):
        result = get_reference_phonemes("namaste", "hindi")
        assert isinstance(result, list)
        assert len(result) > 0

    def test_unsupported_language(self):
        with pytest.raises(ValueError):
            get_reference_phonemes("test", "klingon")
