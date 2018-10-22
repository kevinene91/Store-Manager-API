import os
from flask import Flask
from flask_restful import Api
from config import app_config

from .jwt_instance import jwt
from .api.v1 import apiv1


def create_app(config_name):
    """
        App initialization
    """
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(app_config[config_name])

    jwt.init_app(app)

    app.register_blueprint(apiv1)
    return app
