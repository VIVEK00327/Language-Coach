"""Central config. Reads settings from environment / .env. NEVER hardcode secrets here."""
import os
from pathlib import Path

try:  # python-dotenv is optional; env vars still work without it
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent.parent / ".env")
except ImportError:
    pass


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY") or os.urandom(24).hex()
    DEBUG = os.getenv("FLASK_DEBUG", "0") == "1"
    DATABASE_PATH = os.getenv("DATABASE_PATH", "instance/coach.db")
    MAX_CONTENT_LENGTH = int(os.getenv("UPLOAD_MAX_MB", "10")) * 1024 * 1024
    USE_MOCK_ML = os.getenv("USE_MOCK_ML", "1") == "1"
