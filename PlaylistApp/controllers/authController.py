import os, secrets
from functools import wraps
from flask import Blueprint, session, redirect, request, url_for
from spotipy.oauth2 import SpotifyOAuth

auth_blueprint = Blueprint('auth_bp', __name__)


@auth_blueprint.route("/callback")
def callback():
    # print("saved:", session["state"])
    if request.args.get("error") is not None:
        return redirect("/login")
    # if request.args.get("state") != session["state"]:
    #     return "asdf"  # broken for now, will need proper handler

    spotify_oauth = create_spotify_oauth()
    session.clear()
    session["logged_in"] = True
    code = request.args.get('code')
    token = spotify_oauth.get_access_token(code)
    session["token"] = token
    return redirect("/")


@auth_blueprint.route("/logout")
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect("/")


def create_login_url():
    spotify_oauth = create_spotify_oauth()
    oauth_url = spotify_oauth.get_authorize_url()
    return oauth_url


def create_spotify_oauth():
    state = secrets.token_urlsafe()
    session["state"] = state
    spotify_oauth = SpotifyOAuth(
        client_id=os.environ.get("SPOTIPY_CLIENT_ID"),
        client_secret=os.environ.get("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.environ.get("SPOTIPY_REDIRECT_URI"),
        scope=os.environ.get("SPOTIPY_SCOPE"),
        state=state # Still need someway to check state
    )
    return spotify_oauth


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'logged_in' not in session:
            return redirect(url_for("frontend_bp.login"))
        return view(**kwargs)
    return wrapped_view
