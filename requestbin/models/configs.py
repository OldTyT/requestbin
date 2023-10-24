"""Class global configs."""

import re
import os
from urllib.parse import urlparse
from pydantic import BaseSettings, SecretStr


class GlobalConfigs(BaseSettings):
    """Class global configs."""

    version = "v0.0.1"
    log_level : str = os.getenv("LOG_LEVEL", "DEBUG")
    log_format_json: bool = os.getenv("LOG_FORMAT_JSON", False)
    debug : bool = os.getenv("DEBUG", True)
    enable_cors : bool = os.getenv("DEBUG", False)
    bin_ttl_default : int= os.getenv("BIN_TTL_DEFAULT", 172800)  # 48*3600
    max_requests : int = os.getenv("MAX_REQUESTS", 20)
    cleanup_interval : int = os.getenv("CLEANUP_INTERVAL", 3600)
    port_number : int = os.getenv("PORT_NUMBER", 8000)
    bugsnag_key : SecretStr = os.getenv("BUGSNAG_KEY", "")
    cors_origins : str = os.getenv("CORS_ORIGINS", "*")
    redis_host :str = os.getenv("REDIS_HOST","localhost")
    redis_port:int = os.getenv("REDIS_PORT",6379)
    redis_password : SecretStr = os.getenv("REDIS_PASSWORD", "")
    redis_db :int= os.getenv("REDIS_DB", 0)
    redis_prefix :str= os.getenv("REDIS_PREFIX", "requestbin")
    flask_session_secret_key : SecretStr= os.getenv(
        "FLASK_SESSION_SECRET_KEY",
        "N1BKhJLnBqLpexOZdklsfDKFJDKFadsfs9a3r324YB7B73AglRmrHMDQ9RhXz35"
    ) 
    max_raw_size :int= os.getenv("MAX_RAW_SIZE", 10240)
    realm = os.getenv("REALM", "prod")
    bin_ttl : int= os.getenv("BIN_TTL", bin_ttl_default)
    # storage_backend = "requestbin.storage.memory.MemoryStorage"
    storage_backend = "requestbin.storage.redis.RedisStorage"
    ignore_headers = """
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
Cf-Visitor
Cf-Ray
Cf-Ipcountry
Cf-Connecting-Ip
""".split(
        "\n"
    )[
        1:-1
    ]
    secrets: list = []

    def get_secrets_list(self) -> list:
        if not self.secrets:
            self.secrets = []
            for i in self:
                if bool(isinstance(i[1], SecretStr)):
                    if len(i[1].get_secret_value()) > 0:
                        self.secrets.append(i[1])
        return self.secrets

    def delete_secrets(self, msg: str) -> str:
        secrets = self.get_secrets_list()
        for secret in secrets:
            msg = re.sub(secret.get_secret_value(), '******', msg)
        return msg
