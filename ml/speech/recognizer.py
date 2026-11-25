"""Spoken phonemes from audio. OWNER: Role 2.
MOCK: returns a slightly wrong fake result so the UI has something to show.
Replace with a real model (keep the signature). Set USE_MOCK_ML=1 to force the mock."""
import os


def recognize_phonemes(audio_path: str, language: str) -> list:
    # TODO (Role 2): load audio (16 kHz), run Whisper / wav2vec2 phoneme model, return phoneme list.
    # Mock: pretend the user said "water" slightly wrong.
    return ["w", "o", "t", "e", "r"]
