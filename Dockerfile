FROM python:3.12

RUN pip install pipenv

WORKDIR /app

COPY src/ config/ Pipfile Pipfile.lock ./

RUN pipenv install

CMD ["pipenv", "run", "gunicorn", "-c", "gunicorn_config.py", "app:app"]
