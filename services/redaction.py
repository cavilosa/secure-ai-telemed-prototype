import re
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def redact_email(text: str) -> str:
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
        # Raise an error as the function expects a string.
        raise TypeError("Input must be a string.")
    try:
        # Pattern for common email formats, including those with '+' aliases.
        email_pattern = re.compile(r"\b[A-Za-z0-9._%=+-]+@([A-Za-z0-9-]+\.)+[A-Z|a-z]+\b")
        redacted_text = re.sub(email_pattern, '[REDACTED EMAIL]', text)
        if redacted_text != text:
            logging.info("Successfully redacted email(s) from text.")
        return redacted_text
    except Exception as e:
        # Log any unexpected errors during the regex operation and re-raise.
        logging.error(f"An unexpected error occurred during email redaction: {e}")
        raise

def redact_phone_number(text: str) -> str:
    """
    Redacts North American phone numbers from the given text using a two-pattern approach.

    Args:
        text: The input string to process.

    Returns:
        A new string with phone numbers replaced by '[REDACTED PHONE]'.

    Raises:
        TypeError: If the input is not a string.
    """
    if not isinstance(text, str):
        raise TypeError("Input must be a string.")
    try:
        # Pattern 1: A complex pattern for various formats with separators.
        # Handles formats like (xxx) xxx-xxxx, xxx-xxx-xx-xx, etc.
        phone_pattern = re.compile(r'(?<!\w)(?:\+?1[\s.-]*)?(?:(?:\(\d{3}\))|\d{3})[\s.-]?(?:\d{3}[\s.-]?(?:\d{4}|\d{2}[\s-]\d{2}))\b')
        
        # Pattern 2: A simpler, stricter pattern for purely numeric strings (10 or 11 digits).
        # The \b word boundaries are crucial to prevent matching parts of longer numbers.
        numeric_pattern = r"\b(1?)(\d{10})\b"
        
        # First pass: Handle the complex, formatted numbers.
        redacted_text = re.sub(phone_pattern, '[REDACTED PHONE]', text)
        
        # Second pass: Handle the simple, numeric-only strings on the already processed text.
        redacted_text = re.sub(numeric_pattern, '[REDACTED PHONE]', redacted_text)

        if redacted_text != text:
            logging.info("Successfully redacted phone number(s) from text.")
        return redacted_text
    except Exception as e:
        logging.error(f"An unexpected error occurred during phone redaction: {e}")
        raise

