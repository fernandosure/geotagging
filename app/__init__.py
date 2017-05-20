from flask import Flask
from flask_pymongo import PyMongo
from flask_bootstrap import Bootstrap

from config import config

mongo = PyMongo()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    mongo.init_app(app)
    Bootstrap(app)

    from .api import api as api_blueprint
    from .main import main as main_blueprint

    app.register_blueprint(api_blueprint)
    app.register_blueprint(main_blueprint)

    return app

