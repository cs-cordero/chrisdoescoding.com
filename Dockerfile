FROM python:3.7
LABEL MAINTAINER="Christopher Cordero <ccordero@protonmail.com>"
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code
COPY . /code/

EXPOSE 8000

RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python \
        && . $HOME/.poetry/env \
        && $HOME/.poetry/bin/poetry self update \
        && $HOME/.poetry/bin/poetry install --no-dev

ENV PATH="/root/.poetry/bin:${PATH}"

CMD $HOME/.poetry/bin/poetry run gunicorn config.wsgi --bind 0.0.0.0:8000 --workers 4 --log-file=- --access-logfile=- --error-logfile=-
