import os
from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
import logging
from pythonjsonlogger import jsonlogger

from routes.home_routes import home
from routes.api_routes import api
from extensions.database import setup_db, db


def create_app():
    'Application factory function'
    app = Flask(__name__)
    setup_db(app)
    Migrate(app, db, compare_type=True)
    CORS(app, expose_headers="Authorization")

    logger = logging.getLogger()
    logger.handlers.clear() # Clear Flask logger handlers
    logger.setLevel(logging.DEBUG)

    formatter = jsonlogger.JsonFormatter("{message}{asctime}{name}{levelname}", style='{')

    file_handler = logging.FileHandler('app.log')
    file_handler.setFormatter(formatter)

    console_hanler = logging.StreamHandler()
    console_hanler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_hanler)

    default_config = dict(
        THREADED=True,
        DEBUG='true',
        TEMPLATES_AUTO_RELOAD=True,
        SQLALCHEMY_DATABASE_URI=os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///fallback.db"),
        LOGGING_LEVEL=os.getenv("LOGGING_LEVEL", "DEBUG"),
        SECRET_KEY=os.getenv("SECRET_KEY", "mysecretkey")
    )
    app.config.update(default_config)

    # Register the home blueprint
    app.register_blueprint(home)
    app.register_blueprint(api)
    return app