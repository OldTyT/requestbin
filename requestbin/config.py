import os
import urlparse
import logging

logging.basicConfig(level=logging.WARNING)


def get_int_env(env, int_value):
    if not isinstance(env, str):
        logging.critical("Error get ENV name: " + str(env) + " isn't string")
        exit(1)
    if not isinstance(int_value, int):
        logging.critical("Error default ENV value: " + str(env) + " isn't int")
        exit(1)
    env = os.environ.get(env, int_value)
    if str(env).isdigit():
        my_int = int(env)
        if my_int > 0:
            return int(env)
    logging.critical("Error get ENV value: " + str(env) + " isn't int")
    exit(1)


DEBUG = True
ENABLE_CORS = False

bin_ttl_default = 172800  # 48*3600
MAX_REQUESTS = get_int_env("MAX_REQUESTS", 20)
CLEANUP_INTERVAL = get_int_env("CLEANUP_INTERVAL", 3600)
PORT_NUMBER = 8000

VERSION = "v0.0.1"
STORAGE_BACKEND = "requestbin.storage.memory.MemoryStorage"
BUGSNAG_KEY = ""
CORS_ORIGINS = "*"

REDIS_URL = ""
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_PASSWORD = None
REDIS_DB = 9
REDIS_PREFIX = "requestbin"

BIN_TTL = bin_ttl_default

ROOT_URL = "http://localhost:" + str(PORT_NUMBER)

FLASK_SESSION_SECRET_KEY = os.environ.get("SESSION_SECRET_KEY", "N1BKhJLnBqLpexOZdklsfDKFJDKFadsfs9a3r324YB7B73AglRmrHMDQ9RhXz35")  # noqa: E501
MAX_RAW_SIZE = get_int_env('MAX_RAW_SIZE', 10240)
REALM = os.environ.get('REALM', 'local')

IGNORE_HEADERS = []

if REALM == 'prod':
    DEBUG = False
    ROOT_URL = os.environ.get("ROOT_URL", "http://requestb.in")
    FLASK_SESSION_SECRET_KEY = os.environ.get("SESSION_SECRET_KEY", FLASK_SESSION_SECRET_KEY)  # noqa: E501

    BIN_TTL = get_int_env('BIN_TTL', bin_ttl_default)

    REDIS_URL = os.environ.get("REDIS_URL")
    url_parts = urlparse.urlparse(REDIS_URL)
    REDIS_HOST = url_parts.hostname
    REDIS_PORT = url_parts.port
    REDIS_PASSWORD = url_parts.password
    REDIS_DB = url_parts.fragment

    BUGSNAG_KEY = os.environ.get("BUGSNAG_KEY", BUGSNAG_KEY)
    STORAGE_BACKEND = "requestbin.storage.redis.RedisStorage"

    IGNORE_HEADERS = """
X-Varnish
X-Forwarded-For
X-Heroku-Dynos-In-Use
X-Request-Start
X-Heroku-Queue-Wait-Time
X-Heroku-Queue-Depth
X-Real-Ip
X-Forwarded-Proto
X-Via
X-Forwarded-Port
""".split("\n")[1:-1]
