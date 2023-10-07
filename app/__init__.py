from flask import Flask
import os


def create_app():
    app = Flask(__name__)

    # Load the configuration from the file
    app.config.from_pyfile("config.py")

    # Register blueprints
    from .blueprints import auth, web
    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(web.home_bp)

    return app
