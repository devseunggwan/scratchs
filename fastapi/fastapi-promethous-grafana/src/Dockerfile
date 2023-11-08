FROM tiangolo/uvicorn-gunicorn:python3.10-slim
WORKDIR /usr/src
COPY . .
RUN pip install poetry
RUN poetry install
CMD ["python", "-m", "uvicorn", "app.main:app", "--host=0.0.0.0", "--port=8000"]
