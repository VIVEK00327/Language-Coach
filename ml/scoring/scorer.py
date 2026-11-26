"""Align expected vs spoken phonemes, score with weighted penalties, and generate feedback.
OWNER: Role 3.

Features (R3-04, R3-05):
1. Weighted substitution costs: phonetically similar sounds (s/ʃ, p/b, t/d, ɪ/i)
   receive partial credit (0.5), costing less than completely dissimilar sounds.
2. Per-word scores: attributes aligned phonemes to individual words and scores each word 0-100.
3. Readable feedback: generates actionable suggestions like:
   "You said /s/ in 'ship'; the expected sound is /ʃ/."
"""
from difflib import SequenceMatcher
from typing import List, Optional, Tuple
from ml.contracts import PhonemeResult, WordResult

# Phonetically similar sound pairs (symmetric).
# Pairs share place or manner of articulation, or differ only by voicing or vowel closeness.
_SIMILAR_PAIRS_RAW = [
    # Voicing pairs
    ("p", "b"), ("t", "d"), ("k", "g"),
    ("s", "z"), ("f", "v"), ("θ", "ð"),
    ("ʃ", "ʒ"), ("tʃ", "dʒ"), ("ʧ", "ʤ"),
    # Sibilant / fricative confusions
    ("s", "ʃ"), ("z", "ʒ"), ("s", "θ"), ("z", "ð"),
    ("tʃ", "ʃ"), ("dʒ", "ʒ"), ("t", "θ"), ("d", "ð"),
    # Vowel confusions (tense vs lax, centralisation)
    ("i", "ɪ"), ("iː", "ɪ"), ("u", "ʊ"), ("uː", "ʊ"),
    ("e", "ɛ"), ("eɪ", "e"), ("eɪ", "ɛ"),
    ("ə", "ʌ"), ("æ", "a"), ("æ", "ɛ"),
    ("o", "ɔ"), ("oʊ", "o"), ("oʊ", "ɔ"), ("ɑ", "ɔ"),
    # Liquid / glide / nasal confusions
    ("w", "v"), ("l", "r"), ("m", "n"),
]

SIMILAR_PAIRS = {frozenset((a, b)) for a, b in _SIMILAR_PAIRS_RAW}


def get_similarity_weight(expected: Optional[str], spoken: Optional[str]) -> float:
    """Return similarity weight in [0.0, 1.0].

    1.0 = exact match
    0.5 = phonetically similar (partial credit)
    0.0 = completely different, insertion, or deletion
    """
    if expected is None or spoken is None:
        return 0.0
    if expected == spoken:
        return 1.0

    # Strip length / stress markers for fuzzy phoneme pair matching
    e_clean = expected.replace("ː", "").replace("'", "")
    s_clean = spoken.replace("ː", "").replace("'", "")
    if e_clean == s_clean:
        return 0.8

    if frozenset((expected, spoken)) in SIMILAR_PAIRS or frozenset((e_clean, s_clean)) in SIMILAR_PAIRS:
        return 0.5

    return 0.0


def score_pronunciation(expected: list, spoken: list) -> Tuple[float, List[PhonemeResult]]:
    """Align expected vs spoken phonemes and calculate weighted score (0-100).

    Returns (overall_score, list[PhonemeResult]).
    Exact matches get 1.0 credit.
    Phonetically similar sounds get 0.5 credit (costing less penalty).
    Unrelated substitutions, omissions, and extra sounds get 0.0 credit.
    """
    results: List[PhonemeResult] = []
    sm = SequenceMatcher(a=expected, b=spoken, autojunk=False)

    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for e, s in zip(expected[i1:i2], spoken[j1:j2]):
                results.append(PhonemeResult(expected=e, spoken=s, correct=True))
        elif tag == "replace":
            exp, spk = expected[i1:i2], spoken[j1:j2]
            for k in range(max(len(exp), len(spk))):
                e = exp[k] if k < len(exp) else None
                s = spk[k] if k < len(spk) else None
                results.append(PhonemeResult(expected=e, spoken=s, correct=(e == s and e is not None)))
        elif tag == "delete":
            for e in expected[i1:i2]:
                results.append(PhonemeResult(expected=e, spoken=None, correct=False))
        elif tag == "insert":
            for s in spoken[j1:j2]:
                results.append(PhonemeResult(expected=None, spoken=s, correct=False))

    if not results:
        return 0.0, results

    total_credits = sum(get_similarity_weight(r.expected, r.spoken) for r in results)
    overall_score = round(100.0 * total_credits / len(results), 1)
    return overall_score, results


def score_words(
    words: List[str],
    expected_per_word: List[List[str]],
    spoken: List[str],
) -> Tuple[float, List[WordResult]]:
    """Attribute spoken phonemes to individual words and compute per-word scores.

    Returns (overall_score, list[WordResult]).
    """
    if not words or not expected_per_word:
        return 0.0, []

    all_expected = [ph for w_ph in expected_per_word for ph in w_ph]
    overall_score, all_results = score_pronunciation(all_expected, spoken)

    # Attribute aligned phonemes to words based on expected phoneme boundaries
    word_results: List[WordResult] = []
    res_idx = 0
    total_res = len(all_results)

    for word_idx, (word, w_expected) in enumerate(zip(words, expected_per_word)):
        current_word_phonemes: List[PhonemeResult] = []
        expected_consumed = 0
        target_expected_count = len(w_expected)
        is_last_word = (word_idx == len(words) - 1)

        while res_idx < total_res:
            r = all_results[res_idx]

            # If this is not the last word and we have satisfied all expected phonemes,
            # stop consuming unless the next sound is an insertion tightly bound to this word
            if not is_last_word and expected_consumed >= target_expected_count:
                # If next is an insertion but we reached word boundary, let next word take it
                if r.expected is not None:
                    break
                # Only consume insertion if we haven't consumed any expected yet
                break

            current_word_phonemes.append(r)
            if r.expected is not None:
                expected_consumed += 1
            res_idx += 1

            if not is_last_word and expected_consumed >= target_expected_count:
                break

        # If it's the last word, consume any trailing insertions
        if is_last_word:
            while res_idx < total_res:
                current_word_phonemes.append(all_results[res_idx])
                res_idx += 1

        # Calculate score for this word
        if current_word_phonemes:
            word_credits = sum(get_similarity_weight(p.expected, p.spoken) for p in current_word_phonemes)
            word_score = round(100.0 * word_credits / len(current_word_phonemes), 1)
        else:
            word_score = 0.0

        word_results.append(WordResult(word=word, score=word_score, phonemes=current_word_phonemes))

    return overall_score, word_results


def generate_feedback(words: List[WordResult]) -> List[str]:
    """Generate readable, actionable feedback strings for a list of WordResults.

    Examples:
      "You said /s/ in 'ship'; the expected sound is /ʃ/."
      "The sound /θ/ was missing in 'think'."
      "Extra sound /r/ was added in 'cat'."
    """
    tips: List[str] = []
    for w in words:
        for r in w.phonemes:
            if r.correct:
                continue
            if r.expected and r.spoken:
                tips.append(f"You said /{r.spoken}/ in '{w.word}'; the expected sound is /{r.expected}/.")
            elif r.expected:
                tips.append(f"The sound /{r.expected}/ was missing in '{w.word}'.")
            elif r.spoken:
                tips.append(f"Extra sound /{r.spoken}/ was added in '{w.word}'.")

    return tips or ["Great pronunciation!"]
