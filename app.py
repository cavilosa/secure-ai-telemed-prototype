import os
from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS


from routes.home_routes import home
from routes.api_routes import api
from extensions.database import setup_db, db
from extensions.logger import set_up_logging


def create_app():
    'Application factory function'
    app = Flask(__name__)
    setup_db(app)
    Migrate(app, db, compare_type=True)
    CORS(app, expose_headers="Authorization")

    set_up_logging()
 
    default_config = dict(
        THREADED=True,
        DEBUG='true',
        TEMPLATES_AUTO_RELOAD=True,
        SQLALCHEMY_DATABASE_URI=os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///fallback.db"),
        LOGGING_LEVEL=os.getenv("LOGGING_LEVEL", "DEBUG"),
        SECRET_KEY=os.getenv("SECRET_KEY", "mysecretkey"), 
    )
    app.config.update(default_config)

    # Register the home blueprint
    app.register_blueprint(home)
    app.register_blueprint(api)
    
    return app