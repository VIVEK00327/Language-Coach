"""Glue: audio + text + language -> AssessmentResult. OWNER: Role 1."""
from ml.contracts import AssessmentResult, WordResult
from ml.reference.reference_phonemes import get_reference_phonemes
from ml.speech.recognizer import recognize_phonemes
from ml.scoring.scorer import score_pronunciation


def _feedback(results):
    tips = []
    for r in results:
        if r.correct:
            continue
        if r.expected and r.spoken:
            tips.append(f"You said '{r.spoken}' but the expected sound is '{r.expected}'.")
        elif r.expected:
            tips.append(f"The sound '{r.expected}' was missing.")
        else:
            tips.append(f"Extra sound '{r.spoken}' was added.")
    return tips or ["Great pronunciation!"]


def assess(audio_path: str, target_text: str, language: str) -> AssessmentResult:
    language = language.lower()
    expected = get_reference_phonemes(target_text, language)
    spoken = recognize_phonemes(audio_path, language)
    overall, results = score_pronunciation(expected, spoken)
    # NOTE: per-word splitting comes later; for now the whole text is one WordResult.
    words = [WordResult(word=target_text, score=overall, phonemes=results)]
    return AssessmentResult(language=language, target_text=target_text,
                            overall_score=overall, words=words, feedback=_feedback(results))
