from ml.pipeline import assess


def test_mock_pipeline_runs():
    r = assess("fake.wav", "water", "english")
    assert 0 <= r.overall_score <= 100
    assert r.words and r.feedback
    assert "reference_sec" in r.timing
    assert "recognizer_sec" in r.timing
    assert "scoring_sec" in r.timing
    assert "total_sec" in r.timing
    assert r.timing["total_sec"] >= 0


def test_multi_word_pipeline_runs():
    r = assess("fake.wav", "good ship", "english")
    assert 0 <= r.overall_score <= 100
    assert len(r.words) == 2
    assert r.feedback
    assert "total_sec" in r.timing
