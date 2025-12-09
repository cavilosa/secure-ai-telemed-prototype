from .pii_detector import NNPModel
from .injections_detector import is_direct_injection_attempt

def validate_prompt(prompt: str):
    """
    Runs all checks on a user's input before sending to the LLM.
    Raises an exception if the prompt is malicious.
    """
    if is_direct_injection_attempt(prompt):
        raise ValueError("Malicious prompt detected: Direct injection attempt.")

    if NNPModel.is_pii_extraction_attempt(prompt):
        raise ValueError("Malicious prompt detected: PII extraction attempt.")
    
    # If all checks pass, do nothing.

def filter_output(output: str) -> str:
    """
    Scans and sanitizes the AI model's output before sending to the user.
    """
    # Redact any accidental PII leaks
    sanitized_output = NNPModel.find_pii_in_output(output, redact=True)
    
    return sanitized_output