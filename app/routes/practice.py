"""API routes and page views. OWNER: Role 4.
Provides Home (/), Practice (/practice), and Progress (/progress) pages,
plus the core /api/assess, /api/languages, /api/content, /api/progress endpoints.
"""
import json
import logging
import os
import tempfile
from pathlib import Path
from flask import Blueprint, jsonify, render_template, request
from app import db
from ml.pipeline import assess
from ml.reference.reference_phonemes import SUPPORTED

log = logging.getLogger(__name__)

bp = Blueprint("practice", __name__)
CONTENT_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "content"

MAX_DURATION_SECONDS = 15.0


# -------------------------------------------------------------------------
# Page Views
# -------------------------------------------------------------------------
@bp.get("/")
def index():
    """Landing page introducing Language Coach."""
    return render_template("home.html")


@bp.get("/practice")
def practice():
    """Interactive practice studio with live audio recording and phoneme scoring."""
    return render_template("practice.html")


@bp.get("/progress")
def progress_view():
    """Learner progress dashboard and attempt history."""
    return render_template("progress.html")


# -------------------------------------------------------------------------
# API Endpoints (Stable Contracts)
# -------------------------------------------------------------------------
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
    language = request.form.get("language", "english").lower().strip()
    text = request.form.get("text", "").strip()

    if not text or language not in SUPPORTED:
        return jsonify({"error": "text and a supported language are required"}), 400

    if not audio or not audio.filename:
        return jsonify({"error": "Audio must be a WAV recording, please try again."}), 400

    # Create temporary file with .wav extension
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    tmp_path = tmp.name
    tmp.close()

    try:
        audio.save(tmp_path)

        file_size = os.path.getsize(tmp_path)
        if file_size < 44:
            return jsonify({"error": "Audio must be a WAV recording, please try again."}), 400

        # Validate RIFF....WAVE signature
        with open(tmp_path, "rb") as f:
            header = f.read(12)
        if len(header) < 12 or header[:4] != b"RIFF" or header[8:12] != b"WAVE":
            return jsonify({"error": "Audio must be a WAV recording, please try again."}), 400

        # Validate audio duration using soundfile
        import soundfile as sf
        try:
            info = sf.info(tmp_path)
        except Exception as read_err:
            log.warning("soundfile failed to inspect '%s': %s", tmp_path, read_err)
            return jsonify({"error": "Audio must be a WAV recording, please try again."}), 400

        if info.duration <= 0.0:
            return jsonify({"error": "Audio recording is empty, please try again."}), 400

        if info.duration > MAX_DURATION_SECONDS:
            return jsonify({
                "error": f"Audio clip is {info.duration:.1f}s long (max limit is {MAX_DURATION_SECONDS}s). Please record a shorter attempt."
            }), 400

        # Execute ML assessment
        try:
            result = assess(tmp_path, text, language).to_dict()
        except Exception as pipeline_err:
            log.exception("Assessment failed on '%s' (%s): %s", text, language, pipeline_err)
            return jsonify({"error": f"Assessment service error: {pipeline_err}"}), 500

        db.save_attempt(result)
        return jsonify(result), 200

    finally:
        try:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
        except Exception as cleanup_err:
            log.warning("Failed to remove temp file '%s': %s", tmp_path, cleanup_err)


@bp.get("/api/progress")
def progress():
    return jsonify(db.list_attempts())
