# Use the Debian-based 'slim' image which is compatible with PyTorch
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /code

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# --- Build Stage ---

# 1. Install system dependencies required for building Python packages using Debian's package manager.
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    cmake \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

# 2. Install the fast `uv` installer.
COPY requirements.txt requirements.txt
RUN pip install uv

# 2a. Increase the HTTP timeout for the package installer to handle slow connections.
ENV UV_HTTP_TIMEOUT=300

# 3. Install Python dependencies, telling 'uv' to also look in the PyTorch CPU repository.
RUN uv pip install --system --no-cache --index-strategy unsafe-best-match --extra-index-url https://download.pytorch.org/whl/cpu -r requirements.txt
# --- Final Stage ---

# 4. Copy the rest of your application's source code into the container.
COPY . .

# 5. Expose the port that Gunicorn will run on.
EXPOSE 5000

# 6. Set the command to run the application using the Gunicorn server.
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:create_app()"]

