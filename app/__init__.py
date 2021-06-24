import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from app.response import JSONResponse
from config import Config

flask_app = Flask(__name__)
flask_app.config.from_object(Config())
flask_app.response_class = JSONResponse

db = SQLAlchemy(flask_app)
login = LoginManager(flask_app)

if flask_app.config['LOG_TO_STDOUT']:
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    flask_app.logger.addHandler(stream_handler)
else:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    flask_app.logger.addHandler(file_handler)

flask_app.logger.setLevel(logging.INFO)
flask_app.logger.info('App startup')

import app.views