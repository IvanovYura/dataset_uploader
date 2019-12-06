import os

from psycopg2 import DatabaseError
from unittest import TestCase

from app import create_app
from config import TestConfig
from service.core.database import open_admin_connection, open_user_connection

config = TestConfig


class TestBase(TestCase):
    """
    Test base class responsible for tests initialization
    """
    # path to test directory
    TEST_DIR = os.path.dirname(os.path.abspath(__file__))
    # path to fixtures
    RESOURCES_DIR = os.path.join(TEST_DIR, 'fixture')

    FIXTURE_NAME = 'fixture.sql'

    app = create_app(config)

    def setUp(self):
        self.client = self.app.test_client()
        self.client.__enter__()

        # admin connection is needed to create DB user and test DB
        self.admin_conn = open_admin_connection(config)

        with self.admin_conn.cursor() as cursor:
            create_db_user(config.DB_USER, config.DB_PASSWORD, cursor)
            create_db(config.DB_NAME, config.DB_USER, cursor)

        # user connection for the rest of operations
        self.connection = open_user_connection(config)

        with self.connection.cursor() as cursor:
            execute_sql(self.FIXTURE_NAME, cursor)

        self.connection.commit()

    def tearDown(self):
        self.connection.close()

        with self.admin_conn.cursor() as cursor:
            drop_db(config.DB_NAME, cursor)

        self.admin_conn.close()


def execute_sql(fixture_name, cursor):
    path_to_resource = os.path.join(TestBase.RESOURCES_DIR, fixture_name)

    with open(path_to_resource, 'r') as fixture:
        cursor.execute(fixture.read())


def create_db_user(user, password, cursor):
    query = f'CREATE USER {user} WITH PASSWORD \'{password}\';'

    try:
        cursor.execute(query)
    except DatabaseError:
        # ignore user exists
        pass


def create_db(dbname, user, cursor):
    try:
        drop_db(dbname, cursor)
        cursor.execute(f'CREATE DATABASE {dbname} WITH OWNER={user};')
    except DatabaseError:
        raise Exception('Something went wrong')


def drop_db(dbname, cursor):
    try:
        cursor.execute(f'DROP DATABASE IF EXISTS {dbname};')
    except DatabaseError:
        raise Exception(f'Could not remove test DB {dbname}.')
