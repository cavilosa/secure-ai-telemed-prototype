from transformers import pipeline

# 1. Load the model you chose from the Hub
# The 'model' argument is just the model's name from the website.
generator = pipeline(task="text-generation", model="gpt2")

# 2. Use the loaded model to perform a task
# This will return a dictionary with the generated text.
result = generator("The first step into model integration is", max_length=20)
print(result)

def generate_text(prompt):
    '''Create a function, something like generate_text(prompt), that takes a user's text as input, 
    passes it to the loaded model, and returns the model's output.'''
    pass

'''How It Connects to Everything Else: routes/

Your API endpoints, which live in the routes/ directory, will be the "front door" for model requests. Here's how it will work:

    A user sends a request with a text prompt to an API endpoint you create (e.g., /api/generate).

    The code in your route file (e.g., routes/generation_routes.py) will receive that request.

    It will then call the generate_text() function from your new services/model_service.py file.

    The model_service will run the prompt through the AI model and return the generated text.

    Finally, your route will send that generated text back to the user as a JSON response.

This structure is excellent because it keeps your project clean and organized. 
Your routes handle the web traffic, and your services handle the complex "thinking" part.'''