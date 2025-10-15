FROM python:3.11-alpine
WORKDIR /code
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install uv
RUN uv pip install --system --no-cache -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]