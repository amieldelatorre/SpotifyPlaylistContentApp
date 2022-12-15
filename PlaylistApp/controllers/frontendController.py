from flask import Blueprint

frontend_blueprint = Blueprint('frontend_bp', __name__)


@frontend_blueprint.route("/fe")
def hello():
    return "frontend"
