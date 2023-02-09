from flask import Blueprint, render_template
from .authController import create_login_url, login_required
from .services import get_playlists

frontend_blueprint = Blueprint('frontend_bp', __name__)


@frontend_blueprint.route("/")
@login_required
def hello():
    get_playlists()
    return render_template('default.html',
                           title='Home')


@frontend_blueprint.route("/login")
def login():
    return render_template('login.html',
                           title="Login",
                           login_link=create_login_url())
