FROM python:3.11.3-slim-bullseye

COPY poetry.lock pyproject.toml ./

RUN pip install poetry

WORKDIR /app

COPY . /app

RUN poetry install
CMD flask db upgrade
CMD poetry run python -m flask --app backend run -h 0.0.0.0 -p $PORT
