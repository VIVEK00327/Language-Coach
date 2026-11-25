"""Align expected vs spoken phonemes and score. OWNER: Role 3.
Current version: simple edit-distance alignment (works now). Improve with weighted substitution costs."""
from difflib import SequenceMatcher
from ml.contracts import PhonemeResult


def score_pronunciation(expected: list, spoken: list):
    """Returns (overall_score 0-100, list[PhonemeResult])."""
    results = []
    sm = SequenceMatcher(a=expected, b=spoken, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for e, s in zip(expected[i1:i2], spoken[j1:j2]):
                results.append(PhonemeResult(e, s, True))
        elif tag == "replace":
            exp, spk = expected[i1:i2], spoken[j1:j2]
            for k in range(max(len(exp), len(spk))):
                e = exp[k] if k < len(exp) else None
                s = spk[k] if k < len(spk) else None
                results.append(PhonemeResult(e, s, False))
        elif tag == "delete":
            for e in expected[i1:i2]:
                results.append(PhonemeResult(e, None, False))
        elif tag == "insert":
            for s in spoken[j1:j2]:
                results.append(PhonemeResult(None, s, False))
    if not results:
        return 0.0, results
    correct = sum(r.correct for r in results)
    return round(100.0 * correct / len(results), 1), results
