import logging
from flask import request
from extensions.auth import get_user_id_from_token
from pythonjsonlogger import jsonlogger

class ContextFilter(logging.Filter):
    """
    This is a filter which injects contextual information into the log.
    """
    def filter(self, record):
        user_id = get_user_id_from_token()
        record.user_id = user_id
        return True

def set_up_logging():
    logger = logging.getLogger()
    logger.handlers.clear() # Clear Flask logger handlers
    logger.setLevel(logging.DEBUG)

    formatter = jsonlogger.JsonFormatter("{message} - {asctime} - {name} - {levelname} - {user_id}", style='{')

    file_handler = logging.FileHandler('app.log')
    file_handler.setFormatter(formatter)

    console_hanler = logging.StreamHandler()
    console_hanler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_hanler)
    
    context_filter = ContextFilter()
    file_handler.addFilter(context_filter)
    console_hanler.addFilter(context_filter)
    return logger

