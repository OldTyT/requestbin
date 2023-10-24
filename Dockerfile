FROM python:3.12.0-alpine3.18 AS builder

WORKDIR /app
COPY requirements.txt .

RUN apk add gcc musl-dev bsd-compat-headers libevent-dev && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

FROM python:3.12.0-alpine3.18

WORKDIR /app
COPY --from=builder /app/wheels /wheels

RUN pip install --no-cache /wheels/*

COPY requestbin/ /app/requestbin
COPY launcher.py /app

ENTRYPOINT python3 launcher.py
