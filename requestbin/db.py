import re
import time  # noqa: F401

import feedparser  # noqa: F401

from requestbin import cfg

bin_ttl = cfg.bin_ttl
storage_backend = cfg.storage_backend

storage_module, storage_class = storage_backend.rsplit('.', 1)

try:
    klass = getattr(__import__(storage_module, fromlist=[storage_class]), storage_class)  # noqa: E501
except ImportError as e:
    raise ImportError("Unable to load storage backend '{}': {}".format(storage_backend, e))  # noqa: E501

db = klass()


def create_bin(private=False):
    return db.create_bin(private)


def create_request(bin, request):
    return db.create_request(bin, request)


def lookup_bin(name):
    name = re.split(r"[/.]", name)[0]
    return db.lookup_bin(name)


def expiry_time(name):
    return db.expiry_time(name)


def count_bins():
    return db.count_bins()


def count_requests():
    return db.count_requests()


def avg_req_size():
    return db.avg_req_size()
