import json
from pathlib import Path

CONTENT = Path(__file__).resolve().parent.parent / "data" / "content"
EXPECTED_LANGUAGES = ["english", "hindi", "sanskrit", "french"]


def test_content_files_valid():
    for lang in EXPECTED_LANGUAGES:
        file_path = CONTENT / f"{lang}.json"
        assert file_path.exists(), f"Missing content file for {lang}"

        data = json.loads(file_path.read_text(encoding="utf-8"))
        assert data["language"] == lang
        levels = data.get("levels", {})

        # Ensure all three tiers are present
        assert "beginner" in levels
        assert "intermediate" in levels
        assert "advanced" in levels

        # Each level must be a non-empty list of items
        assert len(levels["beginner"]) > 0
        assert len(levels["intermediate"]) > 0
        assert len(levels["advanced"]) > 0

        # Total item count must be 20 or more
        total_items = (
            len(levels["beginner"])
            + len(levels["intermediate"])
            + len(levels["advanced"])
        )
        assert total_items >= 20, f"{lang} has only {total_items} items, expected at least 20"

        # Verify items have non-empty text strings
        for tier in ["beginner", "intermediate", "advanced"]:
            for item in levels[tier]:
                assert isinstance(item.get("text"), str) and len(item["text"].strip()) > 0

        # Non-English languages must indicate verification note
        if lang in ["hindi", "sanskrit", "french"]:
            assert "note" in data
            assert "checked by a native speaker or teacher" in data["note"]
