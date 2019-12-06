from typing import List

from flask import Flask, Blueprint
from flask_restplus import Api, Namespace

from service.apis.api import namespace
from service.core.database import close_connection


def create_app(config):
    """
    Creates Flask application with specified config
    """
    app = Flask(__name__)

    app.config.from_object(config)

    app.teardown_appcontext(_close_connection)

    blueprint = _create_blueprint(config, [namespace])
    app.register_blueprint(blueprint, url_prefix='/api')

    return app


def _close_connection(exception=None):
    """
    Closes DB connection when app context ends
    """
    close_connection()


def _create_blueprint(config, namespaces: List[Namespace]) -> Blueprint:
    """
    Creates blueprint and returns it with assigned namespace and registered models
    """
    api_blueprint = Blueprint(config.SERVICE_NAME, __name__)

    api = Api(
        api_blueprint,
        title=config.SERVICE_NAME,
        version=config.API_VERSION,
        description=config.API_DESCRIPTION,
    )

    # to get rid of default ns
    api.namespaces.clear()

    for ns in namespaces:
        api.add_namespace(ns)

    return api_blueprint
