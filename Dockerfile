FROM python:3.9-slim-buster as base
RUN apt-get update
RUN apt-get install -y curl
WORKDIR /app
RUN pip install poetry
COPY poetry.toml .
COPY pyproject.toml .
EXPOSE 5000

FROM base as production
RUN poetry config virtualenvs.create false --local && poetry install --no-dev --no-root
COPY /todo_app ./todo_app
ENTRYPOINT poetry run gunicorn --workers=2 "todo_app.app:create_app()" --bind 0.0.0.0

FROM base as development
RUN poetry install
ENTRYPOINT poetry run flask run --host=0.0.0.0