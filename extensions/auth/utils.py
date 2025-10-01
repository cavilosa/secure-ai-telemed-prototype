from flask import request, jsonify
from models.user import User
import jwt
import os
import logging
from functools import wraps

def get_user_id_from_token():
    user_id = None
    try:
        token = request.headers['Authorization'].split(" ")[1] if " " in request.headers['Authorization'] else request.headers['Authorization']
        data_dict = jwt.decode(token, os.environ.get('SECRET_KEY'), algorithm='HS256')
        user_id = data_dict.get("user_id")
    except Exception as error:
        logging.error(f" Error gettign user id from token {error}")
    finally:
        return user_id

def get_request_user():
    token = None
    try:
        # Extract the JWT token from the 'Authorization' header. It expects a "Bearer <token>" format.
        if 'Authorization' in request.headers: # Make sure the Authorization Header is present
            token = request.headers['Authorization'].split(" ")[1] if " " in request.headers['Authorization'] else request.headers['Authorization']
        if not token:
            return None, None 
            # Verify the signature is valid and Decode payload into a readable format
        jwt_payload = jwt.decode(token, os.environ.get('SECRET_KEY'), algorithms=['HS256'])
        current_user = User.query.filter_by(username=jwt_payload['username']).oneornone()
        return current_user, jwt_payload
    except Exception as error:
        logging.error(f"Error in gettinf user from a request {error}")
        return None, None


# decoreator factory
def token_required(permissions): # permissions=['get:redaction']
    def decorator(func):
        @wraps(func) # Ensures the original function's metadata is preserved
        def wrapper(*args, **kwargs): # The code that runs before the route
            """A decorator to protect routes that require a valid JWT token."""
            try:
                
                current_user, jwt_payload = get_request_user()
                user_permissions = jwt_payload.get('permissions', '').split(" ")
                if permissions not in user_permissions:
                    return jsonify({'message': 'Permission denied!'}), 403
                user_role = jwt_payload.get('role')
                if not current_user:
                    return jsonify({'message': 'User not found!'}), 401
                # func is a placeholder for the original function that you put the 
                # @token_required decorator on top of.
                # func() finally runs the original protected function and passes along the 
                # current_user and user_role that were extracted from the token
                value = func(current_user, user_role, *args, **kwargs)
                return value
            except Exception as e:
                logging.error(f"Token decoding error: {e}")
                return jsonify({'message': 'Token is invalid!'}), 401    
        return wrapper
    return decorator
