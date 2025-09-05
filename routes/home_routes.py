from flask import Blueprint

# Cteate a Blueprint for home routes
home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    """A simple view function that returns a welcome message."""
    return "Hello, World! The secure AI telemed prototype is running. 🚀"