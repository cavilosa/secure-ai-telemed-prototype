
import jwt
import os
import logging
from datetime import datetime
from flask import Blueprint, request, render_template,jsonify

from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User

# Cteate a Blueprint for home routes
home = Blueprint('home', __name__, template_folder='templates', static_folder='static')

@home.route('/')
def homepage():
    """A simple view function that returns a welcome message."""
    return "Hello, World! The secure AI telemed prototype is running. 🚀"

@home.route('/login', methods=['GET', 'POST'])
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

            if user and user.check_password(password):   
                token = jwt.encode(
                    {'username': username,
                    'role': user.role,
                    'exp': datetime.now() + datetime.timedelta(hours=1)
                    }, 
                    os.environ.get('SECRET_KEY'),
                    algorithm='HS256')
                return jsonify({"token": jsonify(token)}), 200   
            else:
                return render_template(
                    'login.html', 
                    message="Unable to log in with provided credentials.")
        else:
            logging.info(f"GET request to /login")
            return render_template(
                'login.html', 
                message="Log into the Telemed")
    except Exception as e:
        logging.error(f"Error during login: {e}")
        return render_template('login.html', message='')
    

# @home.route('/signup', methods=['GET', 'POST'])
# def signup():
#     """A simple signup view function that creates a new user."""
#     try:
#         if request.method == 'POST':
#             if request.is_json:
#                 user_json = request.get_json()
#                 logging.info(f"User json {user_json} attempting to sign up.")
#                 username = user_json.get('username')
#                 password = user_json.get('password')
#                 role = user_json.get('role', 'user')  # Default role is 'user'
#             else:
#                 username = request.form.get('username')
#                 password = request.form.get('password')
#                 role = request.form.get('role', 'user')  # Default role is 'user'

#             if User.query.filter_by(username=username).first():
#                 return render_template(
#                     'signup.html', 
#                     message="Username already exists. Please choose a different one.")

#             hashed_password = generate_password_hash(password, method='sha256')
#             new_user = User(username=username, password=hashed_password, role=role)
#             new_user.insert()

#             logging.info(f"New user {username} created with role {role}.")
#             return render_template(
#                 'login.html', 
#                 message="User created successfully! Please log in.")
#         else:
#             logging.info(f"GET request to /signup")
#             return render_template('signup.html', message="")
#     except Exception as e:
#         logging.error(f"Error during signup: {e}")
#         return render_template('signup.html', message='An error occurred. Please try again.')


'''That's the perfect question, and it leads directly to the next crucial step in the plan. You've just built the ticket booth; now you need to build the ticket taker.

Returning the JWT to the front-end is the entire goal of the `/login` endpoint. Think of that token as a temporary, secure key card. The user proves who they are *once* with their password, and in return, you give them this key card that they can use to access protected areas for the next hour.

### What's Next: Using the Token to Create Protected Routes

The next step is to make that token *useful*. You will create API endpoints that are only accessible to users who present a valid token. This is the core of API security.

Here's the two-part process:

**1. The Front-End's Responsibility (Conceptual)**

  * **Store the Token:** After a successful login, the front-end (your Jinja2 template, or a future JavaScript app) would immediately save the JWT it received.
  * **Send the Token:** For every subsequent request to a protected part of your API (like fetching patient data), the front-end must include the token in a special request header called `Authorization`. The standard format is `Bearer <token>`.

**2. The Back-End's Responsibility (Your Next Coding Task)**

This is where you'll write new code. You will create **protected routes**. These are endpoints that:

1.  Check for the `Authorization` header in the incoming request.
2.  Extract the JWT from the header.
3.  **Verify the token's signature** using your `SECRET_KEY` to ensure it hasn't been tampered with.
4.  Check that the token has not expired.
5.  If the token is valid, the code extracts the `user_id` from the token's payload and allows the request to proceed.
6.  If the token is missing, invalid, or expired, it immediately rejects the request with a `401 Unauthorized` error.

### Your Next Step in the Roadmap

Looking at your plan, this is exactly what's scheduled for next week:

  * **Day 9 — Monday, Sept 15:** *Core Project (Protected Routes): Implement a decorator in Flask to protect API endpoints, requiring a valid JWT for access.*

You will create a Python **decorator** (e.g., `@token_required`) that contains all the token-checking logic. You can then apply this decorator to any route you want to protect, making your code clean, secure, and reusable.

**Example of what's next:**

```python
# You will create this decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # ... logic to check for and validate the token ...
        # ... if valid, get user_id and pass it to the route ...
        return f(current_user, *args, **kwargs)
    return decorated


# Then you will use it like this:
@app.route('/patients', methods=['GET'])
@token_required  # <-- This protects the route
def get_all_patients(current_user):
    # This code will only run if the user provides a valid token.
    # 'current_user' would be the user object you looked up from the token.
    return jsonify({"message": f"Welcome user {current_user.username}! Here is the patient data."})
```

You've successfully built the gate. Next week, you'll build the lock and give your users the key.'''      