"""Flask app factory. OWNER: R4."""
from flask import Flask
from app.config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    from app.routes.practice import bp as practice_bp
    app.register_blueprint(practice_bp)
    return app
