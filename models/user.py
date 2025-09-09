from extensions.database import db
from models.base import CRUDMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, CRUDMixin):
    
    __tablename__ = "users"

    __table_args__ = (
        db.Index('ix_message_patient_timestamp', 'patient_id', 'timestamp'),
    )

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # e.g., 'admin', 'clinicians', 'translator'
    full_name = db.Column(db.String(100), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    user_meta = db.Column(db.JSON, nullable=True)

    def set_password(self, password):
        """Hashes the password and stores it."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password) -> bool:
        """Verifies the provided password against the stored hash."""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f"<User id={self.id} username={self.username} role={self.role}>"

