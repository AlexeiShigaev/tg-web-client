FROM python:3.11.7-alpine

WORKDIR /mytelethon/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN set -eux \
    && pip install --upgrade pip poetry \
    && poetry config virtualenvs.create false --local

COPY pyproject.toml poetry.lock /mytelethon/
COPY config.ini /mytelethon/app/

RUN poetry install