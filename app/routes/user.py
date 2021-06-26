from flask import url_for, request, abort, Blueprint
from app.models import UserModel

bp = Blueprint('user', __name__)


@bp.route('/<user_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_user(user_id):
    return {"user_id": user_id}, 200


@bp.route('/register', methods=['POST'])
def register():
    # if current_user.is_authenticated:
    #    return redirect(url_for('main.index'))

    if not request.is_json:
        abort(422)

    data = request.get_json()
    errors = []

    user = UserModel.query.filter_by(username=data['username']).first()
    if user is not None:
        errors.append(_form_error("username", "Please use a different username."))

    user = UserModel.query.filter_by(email=data['email']).first()
    if user is not None:
        errors.append(_form_error("email", "Please use a different email."))

    if errors:
        return {"error": errors}, 400

    user = UserModel(username=data['username'], email=data['email'])
    user.set_password(data['password'])

    user.save()

    return (
        {'username': user.username},
        201,
        {'Location': url_for('handle_user', user_id=user.user_id, _external=True)},
    )
