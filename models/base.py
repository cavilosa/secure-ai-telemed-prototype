from sqlalchemy.exc import SQLAlchemyError
import logging
import sys
from datetime import datetime
from extensions.database import db

class CRUDMixin:
    """Mixin that adds convenience methods for CRUD (Create, Read, Update, Delete) operations."""

    def insert(self):
        """Saves a new object to the database."""
        try:
            db.session.add(self)
            db.session.commit()
            db.session.refresh(self)
            return self
        except SQLAlchemyError as error:
            db.session.rollback()
            logging.error(f"ERROR ON INSERT {error}, SELF: {self.__dict__}, sys.exc_info(): {sys.exc_info()}")
            return None

    def delete(self):
        """Deletes the object from the database."""
        try:
            db.session.delete(self)
            db.session.commit()
            logging.info(f"Instance of {self.__class__.__name__} with id={getattr(self, 'id', 'N/A')} was deleted.")
            return True
        except SQLAlchemyError as error:
            db.session.rollback()
            logging.error(f"Database Delete Error: {error}", exc_info=True)
            return False

    def update(self):
        """Commits the current session to save changes made to an existing object."""
        try:
            db.session.commit()
            db.session.refresh(self)
            logging.info(f"_____UPDATED {self.__class__.__name__}")
            return self
        except SQLAlchemyError as error:
            db.session.rollback()
            logging.error(f"ERROR IN UPDATE: {error}, {sys.exc_info()}, SELF {self}")
            return None
            
    def dict_update(self, **kwargs):
        """
        Updates an object with a dictionary of values and commits the changes.
        """
        _protected_attributes = {'id'}
        try:
            for key, value in kwargs.items():
                if key not in _protected_attributes and hasattr(self, key):
                    setattr(self, key, value)
            return self.update()
        except Exception as e:
            logging.error(f"Dictionary Update Error: {e}", exc_info=True)
            return None

    def format(self) -> dict:
        """Serializes the object's attributes into a dictionary."""
        dict_self = dict()
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                try:
                    if isinstance(value, datetime):
                        value = value.isoformat()
                    dict_self[key] = value
                except TypeError as error:
                    logging.error(f"Error during formatting instance: {error}", exc_info=True)
                    continue
        return dict_self

