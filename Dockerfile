FROM python:3.8-slim-buster

RUN pip install pipenv

RUN mkdir -p /opt/app

WORKDIR /opt/app

COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv install --system

COPY . .

CMD flask run --host=0.0.0.0
