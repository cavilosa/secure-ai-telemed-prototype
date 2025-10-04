from flask import Blueprint, request, jsonify, redirect, url_for, render_template, flash
import logging
import jwt
import os
from functools import wraps

from datetime import datetime, timedelta

from models.user import User
from services.redaction import RedactionService
from extensions.auth.utils import token_required

api = Blueprint('api', __name__, template_folder='templates', static_folder='static')

@api.route('/redact', methods=['POST','GET'])
@token_required(permissions='get:redaction')
def redact(current_user, user_role):
    ''' Redact the incoming json data with pii covering techniques '''
    if not request.is_json():
        return jsonify({'success': 'false', 'error': 'Must be JSON'}), 400
    
    try:
        data = request.get_json()
        text_to_redact = data.get('text_to_redact')

        if not text_to_redact:
            return jsonify({'success': 'false', 'error': "Missing 'text_to_redact' key in request"}, 400)
        
        redaction_services = RedactionService()
        final_reduct_text = redaction_services.hybrid_redact(text=text_to_redact)

        return jsonify({
            'success': True,
            'final_reduct_text': final_reduct_text
        })
    except Exception as error:
        logging.error(f"A redaction error has occurred: {error}")
        return jsonify({
            'success': False,
            'error': 'An internal error occurred during redaction.'
        }), 500


@api.route('/login', methods=['GET', 'POST'])
def login():
    """A simple login view function that authenticates a user and returns a JWT token.""" 
    try:    
        logging.info(f"Method {request.method} to /login")
        if request.method == 'POST':
            if request.is_json:
                user_json = request.get_json()
                logging.info(f"User json {user_json} attempting to log in.")
                username = user_json.get('username')
                password = user_json.get('password')
            else:
                logging.info(f"Form data {request.form} attempting to log in.")
                username = request.form.get('username')
                password = request.form.get('password')

            user = User.query.filter_by(
                username=username).first()
            logging.info(f"User found: {user}")

            if user and user.check_password(password):   
                token = jwt.encode(
                    {'username': username,
                     'user_id': user.id,
                    'role': user.role,
                    'permissions': user.permissions,
                    'exp': datetime.now() + timedelta(hours=1)
                    }, 
                    os.environ.get('SECRET_KEY'),
                    algorithm='HS256')
                return jsonify({"token": token}), 200
            else:
                logging.error(f"No user found or incorrect password for username: {username}")
                flash('Check your credentials and try again.')
                return redirect(url_for('home.homepage'))
        else:
            logging.info(f"GET request to /login")
            return render_template(
                'login.html', 
                message="Log into the Telemed")
    except Exception as e:
        logging.error(f"Error during login: {e}")
        return render_template('login.html', message='')