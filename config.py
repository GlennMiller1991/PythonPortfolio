import os

localhost = True

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(16)
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://app_user:app_user@localhost/app' if localhost else None
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #REMEMBER_COOKIE_DOMAIN = 'http://127.0.0.1:5000' if localhost else 'https://glennmiller.pythonanywhere.com'
    SQLALCHEMY_POOL_RECYCLE = 200
