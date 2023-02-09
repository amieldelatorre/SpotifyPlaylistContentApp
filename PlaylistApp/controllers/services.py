import spotipy
from flask import session
from .authController import create_spotify_oauth
from spotipy.oauth2 import SpotifyOAuth


def get_playlists():
    sp = spotipy.Spotify(oauth_manager=create_spotify_oauth())
    results = sp.current_user_playlists(limit=50, offset=100)
