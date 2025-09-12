import json
from flask import request, jsonify, redirect
from ..models import Interpreter
from ..models import Patient
from functools import wraps
from jose import jwt
from urllib.request import urlopen
import os
from dotenv import load_dotenv
from flask import session, abort
import requests
import logging
from typing import Union

from ..utils import check_login

load_dotenv()

AUTH0_DOMAIN = os.environ['AUTH0_DOMAIN']
ALGORITHMS = os.getenv('ALGORITHMS')
API_AUDIENCE = os.getenv('API_AUDIENCE')
# AUTH0_CALLBACK_URL = os.getenv("AUTH0_CALLBACK_URL")


# Auth Header

def get_token_auth_header() -> str:
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    parts = auth.split()
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    token = parts[1]
    return token

def check_permissions(permission, payload) -> bool:
    if "permissions" not in payload:
        raise AuthError({
                        'code': 'invalid_claims',
                        'description': 'Permissions not included in JWT.'
                        }, 400)

    if permission not in payload["permissions"]:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 401)

    return True


def verify_decode_jwt(token, domain) -> dict:
    # on signup token has no permissions yet
    jsonurl = urlopen(f'https://{domain}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            session.clear()
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Ivalid claims. Check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
        'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
    }, 401)


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_db_user(payload, role) -> Union[Patient, Interpreter, None]:
    """Get user from the db by the role and payload returned by @requires_auth"""

    if role == "patient":
        user = Patient.query.filter_by(auth0_id=payload["sub"]).first()
    elif role == 'interpreter':
        user = Interpreter.query.filter_by(auth0_id=payload["sub"]).first()
    elif role == 'translator':
        user = Interpreter.query.filter_by(auth0_id=payload["sub"]).first()
    else:
        user = None
    return user


def requires_auth(permission="", role=""):
    """ Gets the permissions required by the route and verifies if token has
    the necessary scope of permissions, checks the login and find the user in the db.
    Returns the payload, login and the user."""
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            """ Get token from session or generate it """
            if "token" in session:
                token = session["token"]
            else:
                token = get_token_auth_header()
            payload = verify_decode_jwt(token, AUTH0_DOMAIN)
            login = check_login()
            check_permissions(permission, payload)
            user = get_db_user(payload, role)
            return f(payload, login, user, *args, **kwargs)
        return wrapper
    return requires_auth_decorator


def _get_management_token():
    """ GET Management API Access Token """
    AUTH0_ID = os.environ.get("AUTH0_ID")
    JWT_CODE_SIGNING_SECRET = os.environ.get("JWT_CODE_SIGNING_SECRET")
    AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")

    payload = {
        "grant_type": "client_credentials",
        "client_id": AUTH0_ID,
        "client_secret": JWT_CODE_SIGNING_SECRET,
        "audience": f"https://{AUTH0_DOMAIN}/api/v2/"
    }

    headers = {'content-type': "application/x-www-form-urlencoded"}

    url = f'https://{AUTH0_DOMAIN}/oauth/token'

    response = requests.post(
        url, headers=headers, data=payload
    )

    data = response.json()

    if data.get("access_token"):
        return data["access_token"]
    else:
        return redirect("/logout")


def get_auth0_user(user_id):
    """
    Auth0 Management API ->
    machine to machine applications ->
    Choose application ->
    Scopes/permissions needed: read:users && read:user_idp_tokens
    """

    AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")

    management_token = _get_management_token()

    HEADERS = {
        'authorization': f"Bearer {management_token} ",
    }

    url = f'https://{AUTH0_DOMAIN}/api/v2/users/{user_id}'

    response = requests.get(
        url, headers=HEADERS
    )

    return response.json()


def add_role(USER_ID, ROLE_ID) -> Union[None, dict]:
    """ Adding role to a user by user_id and role_id """

    AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")

# Access Token for the Management API with the scopes read:roles and
# update:users
    management_token = _get_management_token()

    HEADERS = {
        'content-type': "application/json",
        'authorization': f"Bearer {management_token} ",
        'cache-control': "no-cache"
    }

    url = f'https://{AUTH0_DOMAIN}/api/v2/users/{USER_ID}/roles'

    payload = {"roles": [f"{ROLE_ID}"]}

    response = requests.post(
        url, headers=HEADERS, json=payload
    )
    logging.info("response from add role %s", response)

    if response.status_code != 204:
        abort(400, description="Couldn't assign a role at AUTH0.")
    elif response.status_code == 204:
        data = {
            "response": response,
            "description": "The user has been assigned new role  - patient.",
            "success": True
        }

    return data


def refresh_token(code) -> None:
    """ Refreshing token at auth0 """

    headers = {'content-type': "application/x-www-form-urlencoded"}

    url = f'https://{AUTH0_DOMAIN}/oauth/token'

    payload = {
        "grant_type": 'authorization_code',
        "client_id": os.environ.get("AUTH0_ID"),
        "client_secret": os.environ.get("JWT_CODE_SIGNING_SECRET"),
        "code": code,
        "redirect_uri": os.environ.get("AUTH0_CALLBACK_URL")
    }

    requests.post(
        url, headers=headers, data=payload
    )


def delete_user(USER_ID) -> Union[None, dict]:
    """ Deleting users from auth0,
    will work only for production api with delete:users,,delete:current_user permission """

    AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")

    # Access Token for the Management API with the scopes read:roles and
    # update:users
    management_token = _get_management_token()

    HEADERS = {
        'content-type': "application/json",
        'authorization': f"Bearer {management_token} ",
        'cache-control': "no-cache"
    }

    url = f'https://{AUTH0_DOMAIN}/api/v2/users/{USER_ID}'

    response = requests.delete(
        url, headers=HEADERS
    )

    if response.status_code != 204:
        logging.error("Deleting %s", response.json())
    elif response.status_code == 204:
        data = {
            "response": response,
            "description": f"The user has been deleted{USER_ID} ",
            "success": True
        }
        logging.info(data)

        return data
