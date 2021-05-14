FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev libxml2-dev libxslt-dev libffi-dev libz-dev python3-dev \
    build-essential

COPY Pipfile* ./

RUN pip install pipenv

RUN pipenv install --system

# Remove system build dependencies
RUN apt-get remove -y build-essential

COPY src/ ./

EXPOSE 8000

ENTRYPOINT ["python3", "main.py"]
