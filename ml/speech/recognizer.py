"""Spoken phoneme recognition from audio. OWNER: Role 2.

Features (R2-04):
- Real phoneme recognition via pretrained wav2vec 2.0 CTC acoustic model on CPU.
- Model name configured via PHONEME_MODEL_NAME (default: facebook/wav2vec2-lv-60-espeak-cv-ft, ~1.18 GB).
- Singleton pattern: model & processor loaded once and cached in memory.
- Decodes directly to IPA phonemes with symbol normalization.
- Strict error handling: when USE_MOCK_ML=0, NEVER silently return mock data; raises RuntimeError on failure.
- When USE_MOCK_ML=1, returns fast mock output for UI/testing.
"""
import logging
import os
import threading
from typing import List, Optional, Tuple
from ml.reference.phoneme_map import normalize_phonemes

log = logging.getLogger(__name__)

DEFAULT_MODEL_NAME = "facebook/wav2vec2-lv-60-espeak-cv-ft"

# Singleton cache and lock
_MODEL = None
_PROCESSOR = None
_LOCK = threading.Lock()


def get_model_and_processor(model_name: Optional[str] = None) -> Tuple[object, object]:
    """Load and cache the wav2vec 2.0 phoneme model and processor on CPU.

    Raises RuntimeError if loading fails when real recognition is requested.
    """
    global _MODEL, _PROCESSOR
    if _MODEL is not None and _PROCESSOR is not None:
        return _MODEL, _PROCESSOR

    with _LOCK:
        if _MODEL is not None and _PROCESSOR is not None:
            return _MODEL, _PROCESSOR

        target_model = model_name or os.getenv("PHONEME_MODEL_NAME", DEFAULT_MODEL_NAME)
        log.info("Loading speech phoneme model '%s' on CPU...", target_model)

        try:
            import torch
            from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

            processor = Wav2Vec2Processor.from_pretrained(target_model)
            model = Wav2Vec2ForCTC.from_pretrained(target_model)
            model.eval()  # Set to inference mode
            # Ensure model runs on CPU
            model.to("cpu")

            _PROCESSOR = processor
            _MODEL = model
            log.info("Successfully loaded and cached phoneme model '%s'.", target_model)
            return _MODEL, _PROCESSOR
        except Exception as exc:
            log.error("Failed to load phoneme model '%s': %s", target_model, exc)
            raise RuntimeError(
                f"Failed to load speech phoneme model '{target_model}': {exc}. "
                f"Ensure internet access to download weights (~1.18 GB) or set USE_MOCK_ML=1 for mock testing."
            ) from exc


def warmup_recognizer(model_name: Optional[str] = None) -> None:
    """Pre-load model weights into memory at application startup."""
    use_mock = os.getenv("USE_MOCK_ML", "0") in ("1", "true", "True")
    if not use_mock:
        get_model_and_processor(model_name)


def recognize_phonemes(audio_path: str, language: str = "english") -> List[str]:
    """Extract spoken IPA phonemes from an audio recording.

    When USE_MOCK_ML=1, returns deterministic mock output.
    When USE_MOCK_ML=0, executes wav2vec2 CTC inference on 16 kHz audio and normalizes symbols.
    """
    use_mock = os.getenv("USE_MOCK_ML", "0") in ("1", "true", "True")

    # Mock mode branch
    if use_mock:
        return ["w", "o", "t", "e", "r"]

    # Real recognition branch: strictly forbidden from falling back silently to mock
    from ml.speech.audio_utils import load_audio, trim_silence, normalise

    try:
        # 1. Load audio at 16 kHz mono
        audio = load_audio(audio_path, sr=16_000)

        # 2. Trim silence
        trimmed = trim_silence(audio)
        if len(trimmed) == 0:
            log.warning("Audio clip '%s' contains only silence.", audio_path)
            return []

        # 3. Peak normalize
        normed = normalise(trimmed)

        # 4. Get cached model & processor
        model, processor = get_model_and_processor()

        # 5. Tokenize and forward pass
        import torch
        inputs = processor(normed, sampling_rate=16_000, return_tensors="pt")
        with torch.no_grad():
            logits = model(inputs.input_values).logits

        # 6. CTC greedy decoding
        predicted_ids = torch.argmax(logits, dim=-1)
        raw_transcription = processor.batch_decode(predicted_ids)[0]
        log.debug("Raw ASR CTC phoneme string: '%s'", raw_transcription)

        # 7. Normalize symbols to match reference IPA convention
        return normalize_phonemes(raw_transcription)

    except Exception as exc:
        log.error("Real speech recognition failed on '%s': %s", audio_path, exc)
        raise RuntimeError(
            f"Speech recognition pipeline error for audio '{audio_path}': {exc}"
        ) from exc
