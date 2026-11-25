"""Expected phonemes for a target text. OWNER: Role 3.
MOCK: splits into letters. Replace with phonemizer + espeak-ng (keep the signature)."""
import os

SUPPORTED = ["english", "hindi", "sanskrit", "french"]


def get_reference_phonemes(text: str, language: str) -> list:
    if language not in SUPPORTED:
        raise ValueError(f"Unsupported language: {language}")
    # TODO (Role 3): real implementation, e.g. phonemizer.phonemize(text, language=..., backend="espeak")
    return [c for c in text.lower() if not c.isspace()]
