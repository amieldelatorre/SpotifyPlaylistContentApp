from flask import Blueprint

auth_blueprint = Blueprint('auth_bp', __name__)


@auth_blueprint.route("/auth")
def hello():
    return "Auth"
