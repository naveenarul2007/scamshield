import os
import sys
from flask import Flask, render_template, send_from_directory, jsonify

# Ensure ScamShield root directory is on PYTHONPATH
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from backend.config import Config
from backend.routes import api
from database.db import init_db

def create_app(config_class=Config):
    app = Flask(
        __name__,
        static_folder=os.path.join(ROOT_DIR, "static"),
        template_folder=os.path.join(ROOT_DIR, "templates")
    )
    app.config.from_object(config_class)

    # Initialize SQLite database
    init_db()

    # Register API blueprint
    app.register_blueprint(api)

    # Frontend route
    @app.route("/")
    def index():
        return render_template("index.html")

    # Static sample screenshots route
    @app.route("/static/samples/<path:filename>")
    def serve_samples(filename):
        samples_dir = os.path.join(ROOT_DIR, "static", "samples")
        return send_from_directory(samples_dir, filename)

    # Health check at root level
    @app.route("/health")
    def health():
        return jsonify({"status": "ok", "app": "ScamShield"})

    # Error Handlers
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({"error": "Internal server error"}), 500

    return app

if __name__ == "__main__":
    app = create_app()
    port = int(os.getenv("PORT", 5001))
    print(f"===============================================================")
    print(f"  ScamShield Protection Platform is starting on port {port}")
    print(f"  Access UI at: http://localhost:{port}")
    print(f"===============================================================")
    app.run(host="0.0.0.0", port=port, debug=True)
