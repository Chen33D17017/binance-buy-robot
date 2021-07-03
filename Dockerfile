FROM python:3.9-slim-buster

WORKDIR /app
RUN touch /app/config.yml
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
