from zoneinfo import ZoneInfo
from ..extensions.database import db
from sqlalchemy.orm import column_property
from sqlalchemy import select
from sqlalchemy.orm import Mapped
from typing import List
from datetime import datetime
import pytz
from main import CRUDMixin


languages_patients = db.Table(
    'languages_patients',
    # {'extend_existing': True},
    db.Column('language_id', db.Integer, db.ForeignKey('languages.id'), primary_key=True),
    db.Column('patient_id', db.Integer, db.ForeignKey('patients.id'), primary_key=True)
    )

class Language(db.Model, CRUDMixin):
    """Represents a language that patients can speak."""
    __tablename__ = "languages"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    # Many-to-many relationship with patients.
    patients: Mapped[List["Patient"]] = db.relationship(
        secondary=languages_patients,
        back_populates="languages"
    )

    def __repr__(self):
        return f"<Language id={self.id} name={self.name}>"