import re
import logging
from flask import jsonify

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def redact_email(text):
    """
    Redacts email addresses from the given text.
    Args:
        text: The input string to process.
    Returns:
        A new string with email addresses replaced by '[REDACTED EMAIL]'.
    Raises:
        TypeError: If the input is not a string.
    """ 
    if not isinstance(text, str):
            # Raise an error instead of trying to convert. The calling code should handle this.
            raise TypeError("Input must be a string.")     
    try:   
        # Regex pattern is effective for common email formats
        email_regex_pattern = r'[\w\.\-\+]+@[\w\.\-]+\.\w+'

        redacted_text = re.sub(email_regex_pattern, '[REDACTED EMAIL]', text)  

        # Log if a change was made
        if redacted_text != text:
            logging.info("Successfully redacted email(s) from text: {redacted_text}")
        return redacted_text
    except Exception as e:
        # Log any unexpected errors during the regex operation
        logging.error(f"An unexpected error occurred during email redaction: {e}")
        # Re-raise the exception so the caller is aware of the failure.
        raise


def redact_phone(text):
    ''' Redact phone numbers from the given text. 
    Args:
        text: The input string to process.
    Returns:
        A new string with phone numbers replaced by '[REDACTED PHONE]'.
    Raises:
        TypeError: If the input is not a string.'''
    if not isinstance(text, str):
            # Raise an error instead of trying to convert. The calling code should handle this.
            raise TypeError("Input must be a string.")
    try:
        phone_regex_pattern = r''

        redactred_text = re.sub(phone_regex_pattern, '[REDACTED PHONE]', text) 

        if redactred_text != text:
            logging.info("Successfully redacted phone number(s) from text: {redactred_text}")
        return redactred_text
    except (ValueError, BaseException) as error:
        error_message = f"{error.__type__}: {error}"
        logging.error(error_message)
        return jsonify('success', False, 'error': error_message), 400