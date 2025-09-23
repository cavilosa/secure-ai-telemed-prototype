from flask import Blueprint, request, jsonify, redirect, url_for, render_template, flash
import logging
import jwt
import os
import functools
from functools import wraps

from datetime import datetime, timedelta

from models.user import User

api = Blueprint('api', __name__, template_folder='templates', static_folder='static')

def token_required(func):
    @wraps(func) # Ensures the original function's metadata is preserved
    def wrapper(*args, **kwargs):
        """A decorator to protect routes that require a valid JWT token."""
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1] if " " in request.headers['Authorization'] else request.headers['Authorization']
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            payload = jwt.decode(token, os.environ.get('SECRET_KEY'), algorithms=['HS256'])
            current_user = User.query.filter_by(username=payload['username']).first()
            permissions_required = kwargs.pop('permissions', {})
            if permissions_required not in payload.get('role', {}):
                return jsonify({'message': 'Permission denied!'}), 403
            user_role = payload.get('role')
            if not current_user:
                return jsonify({'message': 'User not found!'}), 401
            value = func(current_user, user_role, *args, **kwargs)
            return value
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except Exception as e:
            logging.error(f"Token decoding error: {e}")
            return jsonify({'message': 'Token is invalid!'}), 401
    return wrapper


@api.route('/redact', methods=['POST','GET'])
@token_required(permissions={'role': 'admin'})
def redact():
    if not request.is_json:
        return jsonify({"error": "Invalid input, JSON expected"}), 400
    data = request.get_json() 



    return "Redact endpoint"


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
                    'role': user.role,
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