from transformers import pipeline
import logging

# --- Model Loading (Happens only ONCE at startup) ---

class LLMService:
    """
    A service class to encapsulate the text generation model and its logic.
    """
    def __init__(self):
        """
        Initializes the service and loads the text-generation model once.
        """
        self.generator = None
        try:
            logging.info("Loading text-generation model...")
            # Using 'distilgpt2' is recommended for development as it's much smaller and faster than 'gpt2'.
            self.generator = pipeline('text-generation', model='distilgpt2')
            logging.info("Model loaded successfully.")
        except Exception as e:
            # If the model fails to load, log a critical error and create a placeholder.
            logging.critical(f"Failed to load language model: {e}")

    # --- Text Generation Function ---
    def generate(self, prompt: str) -> str:
        """
        Generates text using the pre-loaded model.

        Args:
            prompt: The input text to continue.

        Returns:
            The generated text string, or an error message if something goes wrong.
        """
        # Check if the model failed to load during startup.
        if self.generator is None:
            logging.error("Text generation unavailable: Model not loaded.")
            return "Sorry, the text generation service is currently unavailable."

        try:
            # The pipeline returns a list of dictionaries, e.g.: [{'generated_text': '...'}].
            output = self.generator(
                prompt, 
                max_new_tokens=70, # Controls how many new tokens to generate.
                truncation=True    # Explicitly allows truncating long prompts.
            )
            
            # We need to access the first element of the list and then get the value 
            # from the 'generated_text' key.
            generated_text = output[0]['generated_text']
            
            logging.info(f"Successfully generated text for prompt: '{prompt}'")
            return generated_text

        except Exception as error:
            logging.error(f"An error occurred during text generation: {error}")
            return "Sorry, an error occurred while generating the text."
        
# --- Singleton Instance ---
# Create a single, pre-initialized instance of the service that the rest of the
# application can import and use. This ensures the model is loaded only once.
llm_service = LLMService()
