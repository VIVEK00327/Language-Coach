"""Tests for phoneme mapping, symbol normalization, flap scoring, and high-error feedback (R3-03)."""
from ml.contracts import PhonemeResult, WordResult
from ml.reference.phoneme_map import normalize_phonemes
from ml.scoring.scorer import (
    generate_feedback,
    get_similarity_weight,
    score_pronunciation,
)


def test_length_mark_attaches_to_vowel():
    # String input
    assert normalize_phonemes("iː") == ["iː"]
    assert normalize_phonemes("wɔːtə") == ["w", "ɔː", "t", "ə"]

    # List of individual character tokens
    assert normalize_phonemes(["s", "i", "ː", "p"]) == ["s", "iː", "p"]
    assert normalize_phonemes(["u", ":"]) == ["uː"]


def test_diphthongs_kept_as_atomic_units():
    # Diphthong oʊ in hello
    assert normalize_phonemes("həloʊ") == ["h", "ə", "l", "oʊ"]
    # Diphthong aɪ in time
    assert normalize_phonemes("taɪm") == ["t", "aɪ", "m"]
    # Diphthong eɪ in day
    assert normalize_phonemes("deɪ") == ["d", "eɪ"]


def test_stress_marks_stripped():
    # Primary and secondary stress marks stripped
    assert normalize_phonemes("həlˈoʊ") == ["h", "ə", "l", "oʊ"]
    assert normalize_phonemes("ˌɪnfərˈmeɪʃən") == [
        "ɪ", "n", "f", "ə", "r", "m", "eɪ", "ʃ", "ə", "n"
    ]


def test_american_flap_scoring():
    # American flap /ɾ/ vs /t/ and /d/
    assert get_similarity_weight("t", "ɾ") == 0.5
    assert get_similarity_weight("d", "ɾ") == 0.5
    assert get_similarity_weight("ɾ", "t") == 0.5

    # Flap vs unrelated sound
    assert get_similarity_weight("k", "ɾ") == 0.0

    # Pronunciation score with flap
    score_flap, _ = score_pronunciation(["w", "ɔː", "t", "ə"], ["w", "ɔː", "ɾ", "ə"])
    score_unrelated, _ = score_pronunciation(["w", "ɔː", "t", "ə"], ["w", "ɔː", "k", "ə"])

    # Flap gets partial credit: 3 exact matches (3.0) + 1 flap (0.5) = 3.5 / 4 = 87.5
    assert score_flap == 87.5
    # Unrelated gets zero credit: 3 exact matches (3.0) + 1 mismatch (0.0) = 3.0 / 4 = 75.0
    assert score_unrelated == 75.0
    assert score_flap > score_unrelated


def test_high_error_word_generates_single_not_detected_line():
    # Word 'thirty' where 4 out of 5 sounds are wrong (80% wrong > 70% threshold)
    bad_word = WordResult(
        word="thirty",
        score=20.0,
        phonemes=[
            PhonemeResult(expected="θ", spoken="s", correct=False),
            PhonemeResult(expected="ɜː", spoken="ɑː", correct=False),
            PhonemeResult(expected="t", spoken="p", correct=False),
            PhonemeResult(expected="i", spoken="u", correct=False),
            PhonemeResult(expected="d", spoken="d", correct=True),
        ],
    )
    feedback = generate_feedback([bad_word])
    assert feedback == ["'thirty' was not detected."]


def test_low_error_word_gives_sound_by_sound_feedback():
    # Word 'ship' where only 1 out of 3 sounds is wrong (33% wrong <= 70%)
    good_word = WordResult(
        word="ship",
        score=83.3,
        phonemes=[
            PhonemeResult(expected="ʃ", spoken="s", correct=False),
            PhonemeResult(expected="ɪ", spoken="ɪ", correct=True),
            PhonemeResult(expected="p", spoken="p", correct=True),
        ],
    )
    feedback = generate_feedback([good_word])
    assert feedback == ["You said /s/ in 'ship'; the expected sound is /ʃ/."]
