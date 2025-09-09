from zoneinfo import ZoneInfo
from extensions.database import db
from datetime import datetime
from babel.dates import format_datetime
from .appointment import languages_patients # Assuming this is correctly defined elsewhere
from sqlalchemy.orm import Mapped
from typing import List
from .base import CRUDMixin


class Patient(db.Model, CRUDMixin):
    """Represents a patient in the telemedicine system."""
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)
    year_of_birth = db.Column(db.Integer, nullable=True, default=None)
    first_name = db.Column(db.String(), nullable=True)
    last_name = db.Column(db.String(), nullable=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    phone = db.Column(db.String(), nullable=True)
    tz = db.Column(db.String(), nullable=False, default='UTC')
    notes = db.Column(db.String(), nullable=True)
    
    # IDs for integration with external systems
    cliniko_medical_id = db.Column(db.BigInteger, nullable=True, unique=True)
    cliniko_mental_id = db.Column(db.BigInteger, nullable=True, unique=True)
    auth0_id = db.Column(db.String(), nullable=True)
    
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=datetime.now
    )

    preferred_messenger = db.Column(db.String(20), default='WA')

    # Many-to-many relationship for languages. This is the correct approach.
    languages: Mapped[List["Language"]] = db.relationship(
        secondary=languages_patients,
        back_populates="patients"
    )

    # One-to-many relationship with messages.
    messages = db.relationship(
        "Message", 
        backref="patient", 
        lazy=True)

    def format(self):
        """Formats the patient object as a dictionary, safe for JSON serialization."""
        
        try:
            patient_tz = ZoneInfo(self.tz)
            formatted_created_at = format_datetime(self.created_at.astimezone(patient_tz), format="long", locale='en_US')
        except Exception:
            # Fallback if the timezone string is invalid for any reason
            formatted_created_at = self.created_at.isoformat()

        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "tz": self.tz,
            "notes": self.notes,
            "cliniko_medical_id": self.cliniko_medical_id,
            "cliniko_mental_id": self.cliniko_mental_id,
            "year_of_birth": self.year_of_birth,
            "auth0_id": self.auth0_id,
            "created_at": formatted_created_at,
            "languages": [lang.name for lang in self.languages]
        }

