# check_env.py
# This script directly tests if the python-dotenv library can read a .env file.

import os
from dotenv import load_dotenv

# Explicitly load the .env file in the current directory
load_dotenv()

# Try to get the variable we expect
test_variable = os.getenv("SECRET_KEY")

if test_variable:
    print(f"Success! Found the variable: {test_variable}")
else:
    print("Failure. Could not find the 'SECRET_KEY' variable in the .env file.")
