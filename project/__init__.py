import os, logging

from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from config import Config, localhost

app = Flask(__name__)
if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    handler = RotatingFileHandler(os.path.join('logs', 'PythonPortfolio.log'), maxBytes=10000, backupCount=10)
    handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s: %(lineno)d]'))
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.logger.warning(' * PythonPortfolio startup')
app.config.from_object(Config)
app.instance_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                 'text_files')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
login.login_message = 'Для получения доступа на эту страницу, пожалуйста, войдите'

from project import models
''', routes

app.register_blueprint(routes.file_proc_bp)
'''
