from flask import Flask
from .blueprints.auth import auth_bp
from .blueprints.web import home_bp


def create_app():
    app = Flask(__name__)

    # Load the configuration from the file
    app.config.from_pyfile("config.py")

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)

    return app
