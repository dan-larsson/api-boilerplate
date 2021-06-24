from flask import url_for, request, abort
from app import flask_app, db
from app.models import PostModel, UserModel


@flask_app.errorhandler(404)
def not_found(error):
    return {'error': 'Not found'}, 404


@flask_app.errorhandler(422)
def unprocessable_entity(error):
    return {"error": "Unprocessable Entity"}, 422


def _post_response(post: dict) -> dict:
    return {
        "post_id": post.post_id,
        "published_at": post.published_at,
        "subject": post.subject,
        "body": post.body,
        "url": url_for('handle_post', post_id=post.post_id),
    }


def _form_error(field: str, error: str) -> dict:
    return {"field": field, "error": error}


@flask_app.route('/users/<user_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_user(user_id):
    return {"user_id": user_id}, 200


@flask_app.route('/posts', methods=['POST', 'GET'])
def handle_posts():
    if request.method == 'POST':
        if not request.is_json:
            abort(422)

        data = request.get_json()

        post = PostModel(subject=data['subject'], body=data['body'])
        db.session.add(post)
        db.session.commit()

        response = _post_response(post)
        return {"post": response}, 200

    elif request.method == 'GET':
        posts = PostModel.query.filter_by(status='published').all()
        results = [_post_response(post) for post in posts]

        return {"posts": results}, 200


@flask_app.route('/posts/<post_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_post(post_id):
    if (
        post := PostModel.query.filter_by(post_id=post_id, status='published').first()
    ) is None:
        abort(404)

    if request.method == 'GET':
        response = _post_response(post)
        return {"post": response}, 200

    elif request.method == 'PUT':
        if not request.is_json:
            abort(422)

        data = request.get_json()
        post.subject = data['subject']
        post.body = data['body']

        db.session.add(post)
        db.session.commit()

        response = _post_response(post)
        return {"post": response}, 200

    elif request.method == 'DELETE':
        db.session.delete(post)
        db.session.commit()

        return {}, 200


@flask_app.route('/register', methods=['POST'])
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

    db.session.add(user)
    db.session.commit()

    return (
        {'username': user.username},
        201,
        {'Location': url_for('handle_user', user_id=user.user_id, _external=True)},
    )
