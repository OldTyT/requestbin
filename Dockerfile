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

EXPOSE 8000
WORKDIR /app/requestbin
COPY . .

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s CMD nc -z 127.0.0.1 8000

# ENTRYPOINT gunicorn -b 0.0.0.0:8000 --worker-class gevent --workers 2 --max-requests 1000 requestbin:app
ENTRYPOINT python web.py
