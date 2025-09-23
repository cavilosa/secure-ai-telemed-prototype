
import jwt
import os
import logging
from datetime import datetime, timedelta
from flask import Blueprint, request, render_template, jsonify, flash, redirect, url_for

from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from models.patient import Patient
from models.language import Language
from models.message import Message

# Cteate a Blueprint for home routes
home = Blueprint('home', __name__, template_folder='templates', static_folder='static')


@home.route('/')
def homepage():
    """A simple view function that returns a welcome message."""

    patients = Patient.query.all()
    logging.info(f"Retrieved {len(patients)} patients from the database.")
    lagnuages = Language.query.all()
    logging.info(f"Retrieved {len(lagnuages)} languages from the database.")    
    messages = Message.query.all()
    logging.info(f"Retrieved {len(messages)} messages from the database.") 

    return render_template('index.html', message="Welcome to the Telemed")
