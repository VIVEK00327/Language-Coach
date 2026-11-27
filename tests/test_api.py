"""API endpoint tests (R4-07)."""
import io
import numpy as np
import pytest
import soundfile as sf
from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def _make_wav_bytes(duration_sec: float = 0.5, sr: int = 16000) -> bytes:
    """Generate in-memory 16 kHz mono 16-bit PCM WAV bytes."""
    t = np.linspace(0, duration_sec, int(sr * duration_sec), endpoint=False, dtype=np.float32)
    sine = 0.5 * np.sin(2 * np.pi * 440 * t)
    buf = io.BytesIO()
    sf.write(buf, sine, sr, format="WAV", subtype="PCM_16")
    buf.seek(0)
    return buf.read()


def test_languages_and_content(client):
    assert "english" in client.get("/api/languages").get_json()
    assert client.get("/api/content/english").status_code == 200
    assert client.get("/api/content/klingon").status_code == 404


def test_assess_valid_wav_returns_200(client, monkeypatch):
    monkeypatch.setenv("USE_MOCK_ML", "1")
    wav_bytes = _make_wav_bytes(duration_sec=0.5)

    data = {
        "text": "water",
        "language": "english",
        "audio": (io.BytesIO(wav_bytes), "recording.wav", "audio/wav"),
    }

    res = client.post("/api/assess", data=data, content_type="multipart/form-data")
    assert res.status_code == 200
    json_data = res.get_json()
    assert "overall_score" in json_data
    assert "words" in json_data
    assert "feedback" in json_data
    assert "timing" in json_data


def test_assess_rejects_non_wav_upload(client):
    # Upload webm/raw text instead of RIFF WAV
    data = {
        "text": "water",
        "language": "english",
        "audio": (io.BytesIO(b"GBLOB_DATA_NOT_A_VALID_RIFF_WAVE"), "recording.webm", "audio/webm"),
    }

    res = client.post("/api/assess", data=data, content_type="multipart/form-data")
    assert res.status_code == 400
    json_data = res.get_json()
    assert "Audio must be a WAV recording, please try again." in json_data["error"]


def test_assess_rejects_empty_file(client):
    data = {
        "text": "water",
        "language": "english",
        "audio": (io.BytesIO(b""), "empty.wav", "audio/wav"),
    }

    res = client.post("/api/assess", data=data, content_type="multipart/form-data")
    assert res.status_code == 400
    json_data = res.get_json()
    assert "Audio must be a WAV recording" in json_data["error"]


def test_assess_rejects_overly_long_clip(client):
    # Generate 16.0s clip (exceeds 15.0s maximum limit)
    long_wav = _make_wav_bytes(duration_sec=16.0)

    data = {
        "text": "water",
        "language": "english",
        "audio": (io.BytesIO(long_wav), "long.wav", "audio/wav"),
    }

    res = client.post("/api/assess", data=data, content_type="multipart/form-data")
    assert res.status_code == 400
    json_data = res.get_json()
    assert "max limit is 15.0s" in json_data["error"]
