# Use the official Python image as a base
FROM python:3.8

WORKDIR /app

COPY app.py gunicorn_config.py requirements.txt dst_api_test.py ./

# Install Python dependencies
RUN pip install -r requirements.txt

# Start Gunicorn to run your Flask app
CMD ["gunicorn", "-c", "gunicorn_config.py", "app:app"]
