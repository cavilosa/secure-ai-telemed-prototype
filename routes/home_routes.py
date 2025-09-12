from flask import Blueprint, request, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User

# Cteate a Blueprint for home routes
home_bp = Blueprint('home', __name__, template_folder='templates')

@home_bp.route('/')
def home():
    """A simple view function that returns a welcome message."""
    return "Hello, World! The secure AI telemed prototype is running. 🚀"

@home_bp.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        user_json = request.get_json()
        username = user_json.get('username')
        password = user_json.get('password')
        password_hash = generate_password_hash(password)

        user = User.query.filter_by(
            username=username,
            password_hash=password_hash).first()
        
        if not user:
            return render_template('login.html', message = "Unable to log in with provided credentials.")

    return render_template('login.html', message = "Log into the Telemed")

    