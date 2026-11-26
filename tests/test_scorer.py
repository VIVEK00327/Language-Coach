from ml.contracts import WordResult, PhonemeResult
from ml.scoring.scorer import (
    score_pronunciation,
    score_words,
    generate_feedback,
    get_similarity_weight,
)


def test_perfect():
    score, res = score_pronunciation(list("water"), list("water"))
    assert score == 100.0 and all(r.correct for r in res)


def test_substitution_and_missing():
    score, res = score_pronunciation(list("water"), list("wotr"))
    assert score < 100
    assert any(not r.correct for r in res)


def test_empty():
    score, res = score_pronunciation([], [])
    assert score == 0.0 and res == []


def test_weighted_similar_sound_scores_higher():
    # Comparing expected ['ʃ', 'ɪ', 'p'] with:
    # 1. similar substitution: spoken ['s', 'ɪ', 'p'] (s vs ʃ is similar)
    # 2. unrelated substitution: spoken ['k', 'ɪ', 'p'] (k vs ʃ is unrelated)
    expected = ["ʃ", "ɪ", "p"]
    similar_spoken = ["s", "ɪ", "p"]
    unrelated_spoken = ["k", "ɪ", "p"]

    score_similar, _ = score_pronunciation(expected, similar_spoken)
    score_unrelated, _ = score_pronunciation(expected, unrelated_spoken)

    # Similar should receive partial credit and score higher than completely unrelated
    assert score_similar > score_unrelated
    # 2 exact matches (1.0 each) + 1 similar (0.5) = 2.5 / 3 = 83.3
    assert score_similar == 83.3
    # 2 exact matches (1.0 each) + 1 unrelated (0.0) = 2.0 / 3 = 66.7
    assert score_unrelated == 66.7


def test_multi_word_scoring():
    words = ["good", "ship"]
    expected_per_word = [["g", "ʊ", "d"], ["ʃ", "ɪ", "p"]]
    # User says "good" perfectly, but says "sip" for "ship"
    spoken = ["g", "ʊ", "d", "s", "ɪ", "p"]

    overall, word_results = score_words(words, expected_per_word, spoken)

    assert len(word_results) == 2
    assert word_results[0].word == "good"
    assert word_results[0].score == 100.0
    assert word_results[1].word == "ship"
    assert word_results[1].score == 83.3
    assert overall == 91.7


def test_readable_feedback_format():
    word = WordResult(
        word="ship",
        score=83.3,
        phonemes=[
            PhonemeResult(expected="ʃ", spoken="s", correct=False),
            PhonemeResult(expected="ɪ", spoken="ɪ", correct=True),
            PhonemeResult(expected="p", spoken="p", correct=True),
        ],
    )
    feedback = generate_feedback([word])
    assert feedback == ["You said /s/ in 'ship'; the expected sound is /ʃ/."]
