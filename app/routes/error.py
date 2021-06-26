from flask import Blueprint

bp = Blueprint('errors', __name__)


@bp.app_errorhandler(404)
def not_found(error):
    return {'error': 'Not found'}, 404


@bp.app_errorhandler(422)
def unprocessable_entity(error):
    return {"error": "Unprocessable Entity"}, 422


@bp.app_errorhandler(500)
def handle_500(err):
    return {"error": "Internal Error"}, 500
