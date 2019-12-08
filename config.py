import os
import sys


class DevelopmentConfig:
    SERVICE_NAME = 'skeleton'
    API_VERSION = 1
    API_DESCRIPTION = 'Skeleton API'

    PROJECT_DIR = os.path.dirname(__file__)

    UPLOAD_DIRECTORY = os.environ.get('UPLOAD_DIRECTORY', '/file_storage/')
    STORAGE_DIRECTORY = f'{PROJECT_DIR}{UPLOAD_DIRECTORY}'

    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = int(os.environ.get('DB_PORT', 5432))
    DB_NAME = os.environ.get('DB_NAME', SERVICE_NAME)
    DB_USER = os.environ.get('DB_USER', SERVICE_NAME)
    DB_PASSWORD = os.environ.get('DB_PASSWORD', SERVICE_NAME)

    DB_ADMIN_USER = 'postgres'
    DB_ADMIN_PASSWORD = 'postgres'

    RESTPLUS_MASK_SWAGGER = False


class TestConfig(DevelopmentConfig):
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = int(os.environ.get('DB_PORT', 5432))
    DB_NAME = os.environ.get('DB_NAME', f'test_{DevelopmentConfig.SERVICE_NAME}')
    DB_USER = os.environ.get('DB_USER', f'test_{DevelopmentConfig.SERVICE_NAME}')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', f'test_{DevelopmentConfig.SERVICE_NAME}')


def get_config(name: str):
    """
    Returns the config by its name
    """
    # get the current module as an object
    current_module = sys.modules[__name__]
    try:
        return getattr(current_module, name)
    except (AttributeError, TypeError) as e:
        raise ValueError(f'The config "{name}" is invalid: {str(e)}')


config = get_config(os.environ.get('APP_CONFIG', 'DevelopmentConfig'))
