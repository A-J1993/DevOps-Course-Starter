FROM python:3.9-buster as base
RUN apt-get update
RUN apt-get install -y curl
WORKDIR /app
RUN curl https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py
RUN pip install poetry
COPY poetry.toml .
COPY pyproject.toml .
RUN poetry add gunicorn
RUN poetry install
#COPY .env .
COPY /todo_app ./todo_app
#COPY pyproject.toml .
#COPY poetry.toml .
#COPY poetry.lock .
#RUN poetry install
EXPOSE 5000
ENTRYPOINT poetry run gunicorn --workers=2 "todo_app.app:create_app()" --bind 0.0.0.0

FROM base as production
CMD poetry run gunicorn --workers=2 "todo_app.app:create_app()" --bind 0.0.0.0

FROM base as development
CMD poetry run flask run --host=0.0.0.0