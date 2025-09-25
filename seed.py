# seed.py
# This script is used to add an initial user to the database for testing purposes.

from app import create_app
from extensions.database import db         
from models.user import User 
from models.language import Language    
from werkzeug.security import generate_password_hash

app = create_app()
app.app_context().push()

# This function will create a test user
def seed_data():
    print("Seeding database...")

    test_user = User.query.filter_by(username='testuser').first()

    # Check if the user already exists to avoid duplicates
    if test_user:
        print("Test user already exists.")

    # Create a new user object
    # IMPORTANT: Always hash passwords, never store them as plain text.
    hashed_password = generate_password_hash("password123", method='pbkdf2:sha256')

    if not test_user:    
        new_user = User(
            username='testuser',
            role='Health Navigator', 
            password_hash=hashed_password,
            is_active=True,
            permissions='get:redaction'
        )

        # Add the new user to the session and commit to the database
        db.session.add(new_user)
        print("Staged test user for creation.")

    # --- Seed Languages ---
    languages_to_seed = ['English', 'Ukrainian', 'Spanish']
    for lang_name in languages_to_seed:
        if not Language.query.filter_by(name=lang_name).first():
            print(f"Staging new language for creation: {lang_name}")
            new_language = Language(name=lang_name)
            db.session.add(new_language)
        else:
            print(f"Language already exists: {lang_name}")

    # --- Commit the Session ---
    # A single commit writes all the staged changes (users, languages, etc.)
    # to the database in one transaction. This is more efficient and safer.
    try:
        db.session.commit()
        print("\nSuccessfully committed changes to the database.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Rolling back database session.")
        db.session.rollback()

    print("Database has been seeded with a test user.")
    print("Username: testuser")
    print("Password: password123")


if __name__ == '__main__':
    # The app.app_context() is crucial here. 
    # It makes the application context available, which SQLAlchemy needs to operate.
    with app.app_context():
        # First, ensure all database tables are created
        db.create_all()
        # Then, run the seeding function
        seed_data()
