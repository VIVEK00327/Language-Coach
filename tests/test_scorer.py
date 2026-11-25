from ml.scoring.scorer import score_pronunciation


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
