FROM python:3.11-slim

ENV PYTHONUNBUFFERED True

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
