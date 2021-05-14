FROM python:3.9-slim

WORKDIR /app

COPY Pipfile* ./

RUN pip install pipenv

RUN pipenv install --system

COPY src/ ./

EXPOSE 8000

ENTRYPOINT ["python3", "main.py"]
