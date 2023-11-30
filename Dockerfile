FROM python:3.12

WORKDIR /app

COPY app.py gunicorn_config.py requirements.txt dst_api.py ./

RUN pip install -r requirements.txt

CMD ["gunicorn", "-c", "gunicorn_config.py", "app:app"]
