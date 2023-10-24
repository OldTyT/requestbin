from __future__ import absolute_import

import time  # noqa: F401

import pickle  # noqa: F401
import redis

from requestbin import cfg

from ..models_data import Bin


class RedisStorage:
    prefix = cfg.redis_prefix

    def __init__(self):
        self.redis = redis.StrictRedis(
            host=cfg.redis_host,
            port=cfg.redis_port,
            db=cfg.redis_db,
            password=cfg.redis_password.get_secret_value(),
        )

    def _key(self, name):
        return "{}_{}".format(self.prefix, name)

    def _request_count_key(self):
        return "{}-requests".format(self.prefix)

    def create_bin(self, private=False):
        bin = Bin(private)
        key = self._key(bin.name)
        self.redis.set(key, bin.dump())
        self.redis.expireat(key, int(bin.created + cfg.bin_ttl))
        return bin

    def create_request(self, bin, request):
        bin.add(request)
        key = self._key(bin.name)
        self.redis.set(key, bin.dump())
        self.redis.expireat(key, int(bin.created + cfg.bin_ttl))

        self.redis.setnx(self._request_count_key(), 0)
        self.redis.incr(self._request_count_key())

    def count_bins(self):
        keys = self.redis.keys("{}_*".format(self.prefix))
        return len(keys)

    def count_requests(self):
        return int(self.redis.get(self._request_count_key()) or 0)

    def avg_req_size(self):
        info = self.redis.info()
        if f"db{cfg.redis_db}" not in info:
            return 0
        return info["used_memory"] / info[f"db{cfg.redis_db}"]["keys"] / 1024

    def lookup_bin(self, name):
        key = self._key(name)
        serialized_bin = self.redis.get(key)
        try:
            bin = Bin.load(serialized_bin)
            return bin
        except TypeError:
            self.redis.delete(key)  # clear bad data
            raise KeyError("Bin not found")

    def expiry_time(self, name):
        key = self._key(name)
        try:
            return self.redis.ttl(key)
        except TypeError:
            self.redis.delete(key)  # clear bad data
            raise KeyError(-1)
