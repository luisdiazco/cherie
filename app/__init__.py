from flask import Flask
import os

from .blueprints.auth import auth_bp
from .blueprints.web import home_bp


def create_app():

    app = Flask(__name__)
    app.secret_key = os.environ.get('FLASK_SECRET_KEY')
    # Load the configuration from the file
    app.config.from_pyfile("config.py")

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='')
    app.register_blueprint(home_bp)

    return app
