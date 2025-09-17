from extensions.database import db
from models.base import CRUDMixin


class Message(db.Model, CRUDMixin):
    """Represents a message sent to or from a patient via a messaging platform."""
    __tablename__ = "messages"

    # Database index for optimizing queries that filter or sort messages by patient and time.
    __table_args__ = (
        db.Index('ix_message_patient_timestamp', 'patient_id', 'timestamp'),
    )
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(20), nullable=False)
    # Establishes the many-to-one relationship: many messages belong to one patient.
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    # Specifies who sent the message, e.g., 'admin' for staff or 'patient' for the patient.
    sender = db.Column(db.String(20))   
    # The text content of the message.
    content = db.Column(db.Text)    
    # The date and time when the message was sent or received.
    timestamp = db.Column(db.DateTime)   
    # The messaging platform used, e.g., "WhatsApp", "SMS".
    messenger = db.Column(db.String(20), default='WhatsApp')   
    # Stores raw metadata from the messaging provider (e.g., the full WhatsApp API response).
    msg_metadata = db.Column(db.JSON, nullable=True)   
    # Unique message identifier provided by the WhatsApp API, used for tracking.
    wa_id = db.Column(db.String(200), nullable=True)   
    # The key/path to the associated media file stored in an S3 bucket, if any.
    media_s3_key = db.Column(db.String(500), nullable=True)   
    # The type of media attached, if any (e.g., 'image', 'audio', 'video', 'document').
    media_type = db.Column(db.String(50), nullable=True)   
    # The delivery status of the message (e.g., 'sent', 'delivered', 'read').
    status = db.Column(db.String(50), nullable=True)   
    # Flag to track whether an administrator has viewed the message in the dashboard.
    is_read_by_admin = db.Column(db.Boolean, default=False, nullable=False)

