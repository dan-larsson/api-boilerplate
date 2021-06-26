import logging
import sys

from flask import Flask
from app.response import JSONResponse
from app.routes import auth_blueprint, user_blueprint, post_blueprint, error_blueprint
from app.models import db
from app.oauth2 import init_oauth

from authlib.integrations.flask_client import OAuth
from config import Config


def create_app():
    flask_app = Flask(__name__)
    flask_app.config.from_object(Config())
    flask_app.response_class = JSONResponse

    db.init_app(flask_app)
    init_oauth(flask_app)

    if flask_app.config['LOG_TO_STDOUT']:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        flask_app.logger.addHandler(stream_handler)

    else:
        if not os.path.exists('logs'):
            os.mkdir('logs')

        file_handler = RotatingFileHandler(
            'logs/app.log', maxBytes=10240, backupCount=10
        )
        file_handler.setFormatter(
            logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
            )
        )
        file_handler.setLevel(logging.INFO)
        flask_app.logger.addHandler(file_handler)

    flask_app.logger.setLevel(logging.INFO)
    flask_app.logger.info('App startup')

    flask_app.register_blueprint(error_blueprint, url_prefix='')
    flask_app.register_blueprint(auth_blueprint, url_prefix='/oauth')
    flask_app.register_blueprint(user_blueprint, url_prefix='/users')
    flask_app.register_blueprint(post_blueprint, url_prefix='/posts')

    return flask_app
