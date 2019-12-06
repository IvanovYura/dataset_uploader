import os


class Config:
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


class TestConfig(Config):
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = int(os.environ.get('DB_PORT', 5432))
    DB_NAME = os.environ.get('DB_NAME', f'test_{Config.SERVICE_NAME}')
    DB_USER = os.environ.get('DB_USER', f'test_{Config.SERVICE_NAME}')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', f'test_{Config.SERVICE_NAME}')
