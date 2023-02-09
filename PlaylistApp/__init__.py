""" Initialise Flask app """
import os

from flask import Flask
from dotenv import load_dotenv


def create_app():
    """ Create the core Flask application """
    load_dotenv()

    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY")

    with app.app_context():
        # Initialise the controllers
        from PlaylistApp.controllers import frontendController, authController
        app.register_blueprint(frontendController.frontend_blueprint)
        app.register_blueprint(authController.auth_blueprint)

    return app
