FROM python:3.13-slim

COPY . .
EXPOSE 8080

RUN pip install poetry

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

RUN poetry install --no-root && rm -rf $POETRY_CACHE_DIR

CMD ["poetry", "run", "python", "app/main.py"]