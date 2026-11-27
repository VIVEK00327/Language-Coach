"""Expected phonemes for a target text. OWNER: Role 3.

Features (R3-02, R3-03):
- Fast sentence & word phonemization using singleton eSpeak NG backend.
- LRU caching at the word level for sub-millisecond repeated lookups.
- Standardized symbol normalization (length marks, diphthongs, stress stripping).
- Mock fallback: USE_MOCK_ML=1 splits text into letters.
"""
import functools
import logging
import os
from typing import Dict, List, Tuple
from ml.reference.phoneme_map import normalize_phonemes

log = logging.getLogger(__name__)

SUPPORTED = ["english", "hindi", "sanskrit", "french"]

# espeak-ng language codes for phonemizer
_LANG_MAP = {
    "english": "en-us",
    "hindi": "hi",
    "french": "fr-fr",
    "sanskrit": "hi",  # placeholder until custom rule-based G2P
}

_USE_MOCK = os.getenv("USE_MOCK_ML", "0") in ("1", "true", "True")

# Singleton backend cache per language to avoid heavy re-initialization (saves ~3-4s per call)
_BACKENDS: Dict[str, object] = {}


def _get_espeak_backend(lang_code: str):
    """Retrieve or initialize a persistent EspeakBackend singleton."""
    global _BACKENDS
    if lang_code not in _BACKENDS:
        # Help phonemizer locate libespeak-ng on Windows
        espeak_lib = os.getenv("PHONEMIZER_ESPEAK_LIBRARY", "")
        if not espeak_lib:
            default_path = r"C:\Program Files\eSpeak NG\libespeak-ng.dll"
            if os.path.exists(default_path):
                os.environ["PHONEMIZER_ESPEAK_LIBRARY"] = default_path

        from phonemizer.backend import EspeakBackend
        _BACKENDS[lang_code] = EspeakBackend(lang_code)
    return _BACKENDS[lang_code]


@functools.lru_cache(maxsize=2048)
def _phonemize_word_cached(word: str, language: str) -> Tuple[str, ...]:
    """Phonemize and normalize an individual word with LRU memory caching."""
    lang_code = _LANG_MAP.get(language, "en-us")
    backend = _get_espeak_backend(lang_code)
    raw = backend.phonemize([word], strip=True)[0]
    return tuple(normalize_phonemes(raw))


def _phonemize_real(text: str, language: str) -> List[str]:
    """Phonemize arbitrary text using cached word lookups or single batch execution."""
    words = text.strip().split()
    if not words:
        return []

    # Fast path for single word: use word-level LRU cache
    if len(words) == 1:
        return list(_phonemize_word_cached(words[0].lower(), language))

    # Multi-word sentence: phonemize in one batch if any words are missing from cache
    result: List[str] = []
    lang_code = _LANG_MAP.get(language, "en-us")
    backend = _get_espeak_backend(lang_code)

    # Perform a single batch call for all words to maximize speed
    raw_list = backend.phonemize(words, strip=True)
    for w, raw in zip(words, raw_list):
        norm = normalize_phonemes(raw)
        result.extend(norm)

    return result


def _phonemize_mock(text: str) -> List[str]:
    """Mock fallback: split text into lowercase non-space characters."""
    return [c for c in text.lower() if not c.isspace()]


def get_reference_phonemes(text: str, language: str) -> List[str]:
    """Return expected phoneme list for *text* in *language*.

    Uses the mock when USE_MOCK_ML=1, otherwise calls the optimized
    phonemizer + eSpeak NG pipeline with symbol normalization.
    """
    if language not in SUPPORTED:
        raise ValueError(f"Unsupported language: {language}")

    # Check environment variable dynamically
    use_mock = os.getenv("USE_MOCK_ML", "0") in ("1", "true", "True")
    if use_mock:
        return _phonemize_mock(text)

    return _phonemize_real(text, language)
