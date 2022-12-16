from flask import Blueprint

frontend_blueprint = Blueprint('frontend_bp', __name__)


@frontend_blueprint.route("/")
def hello():
    return "frontend"
