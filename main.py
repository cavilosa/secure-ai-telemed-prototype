from flask import Flask
from routes.home_routes import home_bp

def create_app()
    'Application factory function'
    app = Flask(__name__)
    # Register the home blueprint
    app.register_blueprint(home_bp)
    return app

@app.route('/')
def home():
    """A simple view function that returns a welcome message."""
    return "Hello, World! The secure AI telemed prototype is running. 🚀"

# This conditional ensures the server only runs when the script is executed directly
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)