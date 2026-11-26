"""Expected phonemes for a target text. OWNER: Role 3.
Real implementation uses phonemizer + espeak-ng.
Mock fallback: USE_MOCK_ML=1 splits text into letters (original behaviour)."""
import logging
import os
from typing import List

log = logging.getLogger(__name__)

SUPPORTED = ["english", "hindi", "sanskrit", "french"]

# espeak-ng language codes for phonemizer
_LANG_MAP = {
    "english": "en-us",
    "hindi": "hi",
    "french": "fr-fr",
    "sanskrit": "hi",  # closest available; will be replaced by rule-based G2P later
}

_USE_MOCK = os.getenv("USE_MOCK_ML", "0") == "1"


def _phonemize_real(text: str, language: str) -> List[str]:
    """Convert text to a flat list of IPA phoneme characters using espeak-ng.

    Sets PHONEMIZER_ESPEAK_LIBRARY so phonemizer can find espeak-ng on
    Windows even when it is not on PATH.
    """
    # Help phonemizer find espeak-ng on Windows
    espeak_lib = os.getenv("PHONEMIZER_ESPEAK_LIBRARY", "")
    if not espeak_lib:
        default = r"C:\Program Files\eSpeak NG\libespeak-ng.dll"
        if os.path.exists(default):
            os.environ["PHONEMIZER_ESPEAK_LIBRARY"] = default

    from phonemizer import phonemize  # lazy import — heavy first load

    lang_code = _LANG_MAP.get(language, "en-us")
    raw: str = phonemize(
        text,
        language=lang_code,
        backend="espeak",
        strip=True,
        language_switch="remove-flags",
    )
    # raw is a string like "həloʊ wɜːld" — split into individual characters,
    # dropping spaces and stress marks (ˈˌ) for now
    skip = set(" ˈˌ")
    return [ch for ch in raw if ch not in skip]


def _phonemize_mock(text: str) -> List[str]:
    """Mock: split text into lowercase non-space characters."""
    return [c for c in text.lower() if not c.isspace()]


def get_reference_phonemes(text: str, language: str) -> List[str]:
    """Return expected phoneme list for *text* in *language*.

    Uses the mock (letter-split) when USE_MOCK_ML=1, otherwise calls
    phonemizer + espeak-ng for real IPA phonemes.
    """
    if language not in SUPPORTED:
        raise ValueError(f"Unsupported language: {language}")

    if _USE_MOCK:
        log.debug("Using mock reference phonemes for '%s'", text)
        return _phonemize_mock(text)

    return _phonemize_real(text, language)
