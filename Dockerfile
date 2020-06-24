FROM python:3.8
MAINTAINER Lars van Rhijn

ENV PYTHONBUFFERED 1
ENV PATH /root/.poetry/bin:${PATH}

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

WORKDIR /sunportal/src

COPY resources/entrypoint.sh /usr/local/bin/entrypoint.sh
COPY poetry.lock pyproject.toml /sunportal/src/

RUN apt-get update && \
    rm --recursive --force /var/lib/apt/lists/* && \
    \
    mkdir --parents /sunportal/src/ && \
    mkdir --parents /sunportal/log/ && \
    mkdir --parents /sunportal/db/ && \
    chmod +x /usr/local/bin/entrypoint.sh && \
    \
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python && \
    poetry config --no-interaction --no-ansi virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-dev

COPY sunportal /sunportal/src/website
