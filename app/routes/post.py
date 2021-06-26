from flask import url_for, request, abort, Blueprint
from app.models import PostModel
from app.oauth2 import require_oauth

bp = Blueprint('post', __name__)


def _post_response(post: dict) -> dict:
    return {
        "post_id": post.post_id,
        "published_at": post.published_at,
        "subject": post.subject,
        "body": post.body,
        "url": url_for('post.handle_post', post_id=post.post_id),
    }


def _form_error(field: str, error: str) -> dict:
    return {"field": field, "error": error}


@require_oauth
@bp.route('/', methods=['POST', 'GET'])
def handle_posts():
    if request.method == 'POST':
        if not request.is_json:
            abort(422)

        data = request.get_json()

        post = PostModel(subject=data['subject'], body=data['body'])
        post.save()

        response = _post_response(post)
        return {"post": response}, 200

    elif request.method == 'GET':
        posts = PostModel.query.filter_by(status='published').all()
        results = [_post_response(post) for post in posts]

        return {"posts": results}, 200


@require_oauth
@bp.route('/<post_id>', methods=['GET', 'PUT', 'DELETE'])
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

        post.save()

        response = _post_response(post)
        return {"post": response}, 200

    elif request.method == 'DELETE':
        post.delete()

        return {}, 200
