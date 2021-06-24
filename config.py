import os

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI", default="")
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS", default=False)
    FLASK_ENV = os.environ.get("FLASK_ENV", default="development")
    FLASK_APP = os.environ.get("FLASK_APP", default="main.py")
    LOG_TO_STDOUT = os.environ.get("LOG_TO_STDOUT", default=True)
