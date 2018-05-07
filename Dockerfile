FROM python:3.6.4

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

WORKDIR /app
