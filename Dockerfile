# Use a specific, lightweight Python version as the base
FROM python:3.11-alpine

# Set the working directory inside the container
WORKDIR /code

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# --- Build Stage ---

# 1. Install all system dependencies required for building Python packages.
#    These are needed for packages that compile from source code.
RUN apk add --no-cache gcc musl-dev linux-headers cmake build-base pkgconfig

# 2. Copy and install the Python dependencies using the fast `uv` installer.
COPY requirements.txt requirements.txt
RUN pip install uv
RUN uv pip install --system --no-cache -r requirements.txt

# 3. (Best Practice) Clean up the build dependencies.
#    We remove them now that the Python packages are installed to create a smaller final image.
RUN apk del gcc musl-dev linux-headers cmake build-base pkgconfig

# --- Final Stage ---

# 4. Copy the rest of your application's source code into the container.
COPY . .

# 5. Expose the port that Gunicorn will run on.
EXPOSE 5000

# 6. Set the command to run the application using the Gunicorn server.
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
