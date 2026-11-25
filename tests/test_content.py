import json
from pathlib import Path

CONTENT = Path(__file__).resolve().parent.parent / "data" / "content"


def test_content_files_valid():
    for lang in ["english", "hindi", "sanskrit", "french"]:
        data = json.loads((CONTENT / f"{lang}.json").read_text(encoding="utf-8"))
        assert data["language"] == lang
        assert data["levels"]["beginner"]
