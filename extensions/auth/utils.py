from flask import request, jsonify
from models.user import User
import jwt
import os
import logging
from functools import wraps

def get_user_id_from_token():
    user_id = None
    try:
        if 'Authorization' not in request.headers:
            return user_id
        token = request.headers['Authorization'].split(" ")[1] if " " in request.headers['Authorization'] else request.headers['Authorization']
        data_dict = jwt.decode(token, os.environ.get('SECRET_KEY'), algorithms='HS256')
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
        logging.info(f" : JWT PATYLOAD : {jwt_payload}")
        return jwt_payload
    except Exception as error:
        logging.error(f"Error in getting user from a request {error}")
        return None, None

def get_db_user(jwt_payload):
    current_user = None
    try:
        current_user = User.query.filter_by(username=jwt_payload['username']).one_or_none()
        logging.info(f" DB user {current_user}")
    except Exception as error:
        logging.error(f" Error with gettind db user by the jwt_payload {error}")
    finally:
        return current_user

# decoreator factory
def token_required(permissions): # permissions='get:redaction'
    def decorator(func):
        @wraps(func) # Ensures the original function's metadata is preserved
        def wrapper(*args, **kwargs): # The code that runs before the route
            """A decorator to protect routes that require a valid JWT token."""
            try:        
                jwt_payload = get_request_user()
                user = get_db_user(jwt_payload)
                user_permissions = set(jwt_payload.get('permissions', '').split(" "))
                required_permissions = permissions if isinstance(permissions, list) else [permissions]
                required_permissions_set = set(required_permissions)
                logging.info(f"User perms: {user_permissions}. Required: {required_permissions_set}")
                if not required_permissions_set.issubset(user_permissions):
                    return jsonify({'message': 'Permission denied!'}), 403
                user_role = jwt_payload.get('role')
                logging.info(f" User's role {user_role}")
                if not user:
                    return jsonify({'message': 'User not found!'}), 401
                # func is a placeholder for the original function that you put the 
                # @token_required decorator on top of.
                # func() finally runs the original protected function and passes along the 
                # current_user and user_role that were extracted from the token
                value = func(user, user_role, *args, **kwargs)
                logging.info(f"The user is authorized.")
                return value
            except Exception as e:
                logging.error(f"Token decoding error: {e}")
                return jsonify({'message': 'Token is invalid!'}), 401    
        return wrapper
    return decorator
