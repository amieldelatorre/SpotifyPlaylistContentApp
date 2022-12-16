from flask import Blueprint

backend_blueprint = Blueprint('backend_bp', __name__, url_prefix="/api")


@backend_blueprint.route("/")
def hello():
    return "backend"
