"""Glue: audio + text + language -> AssessmentResult. OWNER: Role 1.
Logs each stage's timing at INFO level and populates the timing dictionary.
"""
import logging
import time
from ml.contracts import AssessmentResult, WordResult
from ml.reference.reference_phonemes import get_reference_phonemes
from ml.speech.recognizer import recognize_phonemes
from ml.scoring.scorer import score_words, score_pronunciation, generate_feedback

log = logging.getLogger(__name__)


def assess(audio_path: str, target_text: str, language: str) -> AssessmentResult:
    start_total = time.perf_counter()
    language = language.lower()
    words_list = target_text.split()

    # Stage 1: Reference phoneme generation
    t0 = time.perf_counter()
    if len(words_list) > 1:
        expected_per_word = [get_reference_phonemes(w, language) for w in words_list]
    else:
        expected = get_reference_phonemes(target_text, language)
    t_ref = time.perf_counter() - t0
    log.info("Stage [reference] took %.4f s for '%s' (%s)", t_ref, target_text, language)

    # Stage 2: Speech recognition
    t0 = time.perf_counter()
    spoken = recognize_phonemes(audio_path, language)
    t_rec = time.perf_counter() - t0
    log.info("Stage [recognizer] took %.4f s for '%s' (%s)", t_rec, target_text, language)

    # Stage 3: Scoring & feedback generation
    t0 = time.perf_counter()
    if len(words_list) > 1:
        overall, word_results = score_words(words_list, expected_per_word, spoken)
        feedback = generate_feedback(word_results)
    else:
        overall, results = score_pronunciation(expected, spoken)
        word_results = [WordResult(word=target_text, score=overall, phonemes=results)]
        feedback = generate_feedback(word_results)
    t_score = time.perf_counter() - t0
    log.info("Stage [scoring] took %.4f s for '%s' (%s)", t_score, target_text, language)

    total_time = time.perf_counter() - start_total
    log.info("Total assessment pipeline took %.4f s", total_time)

    timing_dict = {
        "reference_sec": round(t_ref, 4),
        "recognizer_sec": round(t_rec, 4),
        "scoring_sec": round(t_score, 4),
        "total_sec": round(total_time, 4),
    }

    return AssessmentResult(
        language=language,
        target_text=target_text,
        overall_score=overall,
        words=word_results,
        feedback=feedback,
        timing=timing_dict,
    )
