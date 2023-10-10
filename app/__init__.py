from flask import Flask
import os

from .blueprints.auth import auth_bp
from .blueprints.web import home_bp

app = Flask(__name__)

app.secret_key = os.environ.get('FLASK_SECRET_KEY')


def create_app():

    # Load the configuration from the file
    app.config.from_pyfile("config.py")

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)

    return app
