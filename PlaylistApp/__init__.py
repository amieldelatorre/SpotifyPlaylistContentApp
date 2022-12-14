"""Initialise Flask app"""

from flask import Flask
from flask_cors import CORS
from spotipy import Spotify, SpotifyOAuth
from os import environ
from dotenv import load_dotenv

load_dotenv()

spotify_scope = environ.get('SPOTIPY_SCOPE')
sp = Spotify(auth_manager=SpotifyOAuth(scope=spotify_scope))


def create_app():
    """Making the core Flask application"""

    app = Flask(__name__)
    CORS(app)

    app.config.from_object('config.Config')

    with app.app_context():
        # initialise the blueprints in the controller folder
        from PlaylistApp.controller import playlistController
        app.register_blueprint(playlistController.playlist_blueprint)

    return app
