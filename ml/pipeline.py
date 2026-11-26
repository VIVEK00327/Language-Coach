"""Glue: audio + text + language -> AssessmentResult. OWNER: Role 1."""
from ml.contracts import AssessmentResult, WordResult
from ml.reference.reference_phonemes import get_reference_phonemes
from ml.speech.recognizer import recognize_phonemes
from ml.scoring.scorer import score_words, score_pronunciation, generate_feedback


def assess(audio_path: str, target_text: str, language: str) -> AssessmentResult:
    language = language.lower()
    words_list = target_text.split()

    if len(words_list) > 1:
        # Multi-word assessment: attribute phonemes to each word
        expected_per_word = [get_reference_phonemes(w, language) for w in words_list]
        spoken = recognize_phonemes(audio_path, language)
        overall, word_results = score_words(words_list, expected_per_word, spoken)
        feedback = generate_feedback(word_results)
        return AssessmentResult(
            language=language,
            target_text=target_text,
            overall_score=overall,
            words=word_results,
            feedback=feedback,
        )
    else:
        # Single-word assessment
        expected = get_reference_phonemes(target_text, language)
        spoken = recognize_phonemes(audio_path, language)
        overall, results = score_pronunciation(expected, spoken)
        word_results = [WordResult(word=target_text, score=overall, phonemes=results)]
        feedback = generate_feedback(word_results)
        return AssessmentResult(
            language=language,
            target_text=target_text,
            overall_score=overall,
            words=word_results,
            feedback=feedback,
        )
