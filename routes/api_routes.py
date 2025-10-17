from flask import Blueprint, request, jsonify, redirect, url_for, render_template, flash
import logging
import jwt
import os

from datetime import datetime, timedelta

from models.user import User
from services.redaction import RedactionService
from services.llm_service import llm_service
from extensions.auth.utils import token_required
from services.prompt_filters import validator

api = Blueprint('api', __name__, template_folder='templates', static_folder='static')

@api.route('/redact', methods=['POST','GET'])
@token_required(permissions=['get:redaction'])
def redact(user):
    ''' Redact the incoming json data with pii covering techniques '''
    # logging.info(f" Redact has been activated {request.get_json()}")
    if not request.is_json:
        logging.error(f" Request is not json.")
        return jsonify({'success': 'false', 'error': 'Must be JSON'}), 400
    try:
        data = request.get_json()
        text_to_redact = data.get('text_to_redact')

        if not text_to_redact:
            logging.error(f" No text to redact. ")
            return jsonify({'success': 'false', 'error': "Missing 'text_to_redact' key in request"}, 400)
        
        redaction_services = RedactionService()
        final_redact_text = redaction_services.hybrid_redact(text=text_to_redact)
        logging.info(f" Final redact text {final_redact_text}")

        return jsonify({
            'success': True,
            'final_redact_text': final_redact_text
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
                logging.info(f" Token - {token[0:5]}")
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
    

# LLM model integration endpoint
@api.route('/generate', methods=['POST'])
@token_required(permissions=['get:redaction']) # The decorator passes the user object to the function
def generate_response(user):
    """
    Accepts a JSON payload with a 'prompt' and returns a model-generated text completion.
    This is a protected endpoint and requires a valid JWT with appropriate permissions.
    """
    # Validate the incoming request
    if not request.is_json:
        logging.error("Request received is not in JSON format.")
        return jsonify({
            "success": False,
            "error": "Bad Request: payload must be in JSON format."
        }), 400

    data = request.get_json()
    prompt = data.get('prompt')

    if not prompt:
        logging.warning("Request received with an empty prompt.")
        return jsonify({
            "success": False,
            "error": "Bad Request: 'prompt' field cannot be empty."
        }), 400
    
    # Guard the input
    validator.validate_prompt(prompt)

    # Call the service layer to perform the core logic
    try:
        generated_text = llm_service.generate(prompt)
        
        # Check if the service layer itself returned a known error message
        if "Sorry" in generated_text:
            return jsonify({
                "success": False,
                "error": "An internal error occurred while generating the text."
            }), 500

        logging.info(f"Successfully generated response for user: {user.username}")

        validated_output = validator.filter_output(generated_text)
        
        # Return a successful response
        return jsonify({
            "success": True,
            "generated_text": validated_output
        }), 200

    except Exception as e:
        # Catch any other unexpected errors
        logging.critical(f"An unexpected critical error occurred in /generate endpoint: {e}")
        return jsonify({
            "success": False,
            "error": "Internal Server Error"
        }), 500