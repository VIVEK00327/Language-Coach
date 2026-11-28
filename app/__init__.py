"""Flask app factory. OWNER: R4."""
from flask import Flask, render_template
from app.config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404

    from app.routes.practice import bp as practice_bp
    app.register_blueprint(practice_bp)
    return app
