import pytest

flask = pytest.importorskip("flask")
from app import create_app  # noqa: E402


def test_languages_and_content():
    client = create_app().test_client()
    assert "english" in client.get("/api/languages").get_json()
    assert client.get("/api/content/english").status_code == 200
    assert client.get("/api/content/klingon").status_code == 404
