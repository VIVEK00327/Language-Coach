from ml.pipeline import assess


def test_mock_pipeline_runs():
    r = assess("fake.wav", "water", "english")
    assert 0 <= r.overall_score <= 100
    assert r.words and r.feedback
