from flask import Blueprint

backend_blueprint = Blueprint('backend_bp', __name__)


@backend_blueprint.route("/be")
def hello():
    return "backend"
