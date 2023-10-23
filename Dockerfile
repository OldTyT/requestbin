FROM python:2.7.18-alpine3.10 AS Flake8

WORKDIR /app/requestbin

COPY . .

RUN /usr/local/bin/python -m pip install --upgrade pip \
    && pip install flake8 && flake8

FROM python:2.7.18-alpine3.10 AS compile-image

COPY requirements.txt .

RUN apk update && apk upgrade && \
    apk add \
        gcc python python-dev py-pip \
        musl-dev g++ \
        bsd-compat-headers \
        libevent-dev \
    && /usr/local/bin/python -m pip install --upgrade pip \
    && pip install --user -r requirements.txt \
    && pip freeze

FROM python:2.7.18-alpine3.10 AS build-image
COPY --from=compile-image /root/.local /root/.local

ARG REALM="local" \
    SESSION_SECRET_KEY="N1BKhJLnBqLpexOZdklsfDKFJDKFadsfs9a3r324YB7B73AglRmrHMDQ9RhXz35" \
    MAX_RAW_SIZE="10240" \
    ROOT_URL="http://requestb.in" \
    SESSION_SECRET_KEY="N1BKhJLnBqLpexOZdklsfDKFJDKFadsfs9a3r324YB7B73AglRmrHMDQ9RhXz35" \
    BIN_TTL="172800" \
    REDIS_URL="REDIS_URL" \
    BUGSNAG_KEY="BUGSNAG_KEY"

ENV REALM=$REALM \
    SESSION_SECRET_KEY=$SESSION_SECRET_KEY \
    MAX_RAW_SIZE=$MAX_RAW_SIZE \
    ROOT_URL=$ROOT_URL \
    SESSION_SECRET_KEY=$SESSION_SECRET_KEY \
    BIN_TTL=$BIN_TTL \
    REDIS_URL=$REDIS_URL \
    BUGSNAG_KEY=$BUGSNAG_KEY

EXPOSE 8000
WORKDIR /app/requestbin
COPY . .

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s CMD nc -z 127.0.0.1 8000

# ENTRYPOINT gunicorn -b 0.0.0.0:8000 --worker-class gevent --workers 2 --max-requests 1000 requestbin:app
ENTRYPOINT python web.py
