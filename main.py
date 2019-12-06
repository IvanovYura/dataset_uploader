from app import create_app
from config import Config

if __name__ == '__main__':
    config = Config
    app = create_app(config)
    app.run()
