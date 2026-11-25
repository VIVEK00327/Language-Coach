"""API routes. OWNER: Role 4. Calls ml.pipeline.assess only."""
import json
import tempfile
from pathlib import Path
from flask import Blueprint, jsonify, render_template, request
from app import db
from ml.pipeline import assess
from ml.reference.reference_phonemes import SUPPORTED

bp = Blueprint("practice", __name__)
CONTENT_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "content"


@bp.get("/")
def index():
    return render_template("index.html")


@bp.get("/api/languages")
def languages():
    return jsonify(SUPPORTED)


@bp.get("/api/content/<language>")
def content(language):
    path = CONTENT_DIR / f"{language}.json"
    if language not in SUPPORTED or not path.exists():
        return jsonify({"error": "unknown language"}), 404
    return jsonify(json.loads(path.read_text(encoding="utf-8")))


@bp.post("/api/assess")
def assess_route():
    audio = request.files.get("audio")
    language = request.form.get("language", "english")
    text = request.form.get("text", "")
    if not text or language not in SUPPORTED:
        return jsonify({"error": "text and a supported language are required"}), 400
    suffix = Path(audio.filename).suffix if audio and audio.filename else ".wav"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        if audio:
            audio.save(tmp.name)
        result = assess(tmp.name, text, language).to_dict()
    db.save_attempt(result)
    return jsonify(result)


@bp.get("/api/progress")
def progress():
    return jsonify(db.list_attempts())
