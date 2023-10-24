# Requestbin [WIP]

# Docker develop

```
docker build -t test:local .
docker run --rm --name tester --workdir /app -v ".":"/app" --entrypoint ash -it test:local
docker exec -ti tester ash
```

## Description

Requestbin service

See `/api/v1/stats` for view runtime info.

## ENV Vars

* `MAX_REQUESTS` - Max requests per `bins`, default: `20`.
* `CLEANUP_INTERVAL` - Cleanup interval, default: `3600`.
* `MAX_RAW_SIZE` - Maximum raw size on request, default `10240`.
* `BIN_TTL` - Time to life `bins`, default `172800`.
* `REALM` - current realm, default: `local`.
* `ROOT_URL` - Root URL, default: `http://requestb.in`.
* `REDIS_URL` - Redis URL.
* `BUGSNAG_KEY` - API KEY Bugsnag.
* `FLASK_SESSION_SECRET_KEY` - Flask session secret key.
