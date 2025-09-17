import os
from flask import Flask
from routes.home_routes import home
from extensions.database import setup_db, db
from flask_migrate import Migrate
from flask_cors import CORS
import logging


def create_app():
    'Application factory function'
    app = Flask(__name__)
    setup_db(app)
    Migrate(app, db, compare_type=True)
    CORS(app, expose_headers="Authorization")
    logging.basicConfig(level=logging.INFO)

    default_config = dict(
        THREADED=True,
        DEBUG='true',
        TEMPLATES_AUTO_RELOAD=True,
        SQLALCHEMY_DATABASE_URI=os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///fallback.db"),
        LOGGING_LEVEL=os.getenv("LOGGING_LEVEL", "INFO"),
        SECRET_KEY=os.getenv("SECRET_KEY", "mysecretkey")
    )
    app.config.update(default_config)

    # Register the home blueprint
    app.register_blueprint(home)
    return app

# This conditional ensures the server only runs when the script is executed directly
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)