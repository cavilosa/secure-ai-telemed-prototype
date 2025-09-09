from flask_migrate import Migrate
import os
from dotenv.main import load_dotenv
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, text
from sqlalchemy.pool import QueuePool

load_dotenv()

SECURE_URL = os.environ.get("SECURE_DATABASE_URL")
DATABASE_URL = SECURE_URL or os.environ.get("DATABASE_URL")

Base = declarative_base()

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)

def setup_db(application, database_url=DATABASE_URL):
    if database_url[0:10] != "postgresql":
        database_url = database_url.replace("postgres", "postgresql")
    engine = create_engine(
        database_url,
        echo=False,  # Set to False in production if you don't want SQL logs
        poolclass=QueuePool,
        pool_size=5,         # Max persistent connections in pool
        max_overflow=3,       # Extra temporary connections
        pool_timeout=30,      # Seconds to wait before giving up on a connection
        pool_pre_ping=True,   # Automatically check connection liveness
        pool_recycle=280 
    )

    with engine.connect() as conn:
        conn.execute(text("SET search_path TO public;"))

    application.config["SQLALCHEMY_DATABASE_URI"] = database_url
    application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = application
    with application.app_context():
        db.init_app(application)
        db.create_all()  # Heroku deployment doesn't need this line
        engine.dispose()


migrate = Migrate()
