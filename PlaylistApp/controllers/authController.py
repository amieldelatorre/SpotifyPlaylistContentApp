import os, secrets
from flask import Blueprint, session, redirect, request
from spotipy.oauth2 import SpotifyOAuth

auth_blueprint = Blueprint('auth_bp', __name__)


@auth_blueprint.route("/login")
def login():
    spotify_oauth = create_spotify_oauth()
    oauth_url = spotify_oauth.get_authorize_url()
    return redirect(oauth_url)


@auth_blueprint.route("/callback")
def callback():
    if request.args.get("error") is not None:
        return redirect("/")

    spotify_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token = spotify_oauth.get_access_token(code)
    session["token"] = token
    return redirect("/")


@auth_blueprint.route("/logout")
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect("/")


def create_spotify_oauth():
    spotify_oauth = SpotifyOAuth(
        client_id=os.environ.get("SPOTIPY_CLIENT_ID"),
        client_secret=os.environ.get("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.environ.get("SPOTIPY_REDIRECT_URI"),
        scope=os.environ.get("SPOTIPY_SCOPE"),
        state=secrets.token_urlsafe() # How to generate secret that is persistent between creating the spotify oauth?
    )
    return spotify_oauth
