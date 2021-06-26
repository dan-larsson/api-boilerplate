import os


class Config(object):
    FLASK_ENV = os.environ.get("FLASK_ENV", default="development")
    FLASK_APP = os.environ.get("FLASK_APP", default="main.py")
    LOG_TO_STDOUT = os.environ.get("LOG_TO_STDOUT", default=True)
    # Oauth2 Settings
    GOOGLE_REQUEST_TOKEN_URL = os.environ.get(
        "GOOGLE_REQUEST_TOKEN_URL",
        default='https://accounts.google.com/.well-known/openid-configuration',
    )
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
    # Sqlalchemy settings
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI", default="")
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get(
        "SQLALCHEMY_TRACK_MODIFICATIONS", default=False
    )
