from flask import g
from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.extras import RealDictCursor
from werkzeug.local import LocalProxy

from config import config


def open_connection():
    """
    Flask App context connection
    """
    connection = g.get('connection')

    if connection is None:
        connection = g.connection = open_user_connection(config)
    return connection


def open_admin_connection(config):
    """
    Returns Admin connection to make operations outside of transaction block
    """
    connection = connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        dbname=None,
        user=config.DB_ADMIN_USER,
        password=config.DB_ADMIN_PASSWORD,
    )
    # to create DB or DB user, operation should be outside of transaction
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    return connection


def open_user_connection(config):
    """
    User connection to service DB
    """
    return connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        dbname=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
    )


def get_dict_cursor(connection):
    """
    Returns cursor with RealDictCursor factory
    to access fetched data from DB as Python dictionary
    """
    return connection.cursor(cursor_factory=RealDictCursor)


def close_connection():
    connection = g.get('connection')

    if connection is not None:
        connection.close()


# forward all connection requests to proxy method
conn = LocalProxy(open_connection)
