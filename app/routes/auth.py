from flask import session, url_for, request, Blueprint
from app.models import UserModel
from app.oauth2 import authorization, require_oauth

bp = Blueprint('auth', __name__)


def current_user():
    if 'id' in session:
        uid = session['id']
        return UserModel.query.get(uid)
    return None


@bp.route('/authorize', methods=['GET', 'POST'])
def authorize():
    user = current_user()
    # if user log status is not true (Auth server), then to log it in
    if not user:
        return redirect(url_for('app.user.home', next=request.url))

    if request.method == 'GET':
        try:
            grant = authorization.validate_consent_request(end_user=user)

        except OAuth2Error as error:
            return error.error

        return {'user': user, 'grant': grant}, 200

    if not user and 'username' in request.form:
        username = request.form.get('username')
        user = UserModel.query.filter_by(username=username).first()

    if request.form['confirm']:
        grant_user = user
    else:
        grant_user = None

    return authorization.create_authorization_response(grant_user=grant_user)


@bp.route('/token', methods=['POST'])
def issue_token():
    return authorization.create_token_response()


@bp.route('/revoke', methods=['POST'])
def revoke_token():
    return authorization.create_endpoint_response('revocation')


@bp.route('/me')
@require_oauth('profile')
def api_me():
    user = current_token.user
    return {'user': {'user_id': user.user_id, 'username': user.username}}, 200
