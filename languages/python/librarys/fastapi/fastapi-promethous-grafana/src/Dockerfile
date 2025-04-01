FROM python:3.10-slim
WORKDIR /usr/src
COPY . .
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-root
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "--bind", "0.0.0.0:8000"]