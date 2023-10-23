import feedparser  # noqa: F401
import time  # noqa: F401
import re
from requestbin import config

bin_ttl = config.BIN_TTL
storage_backend = config.STORAGE_BACKEND

storage_module, storage_class = storage_backend.rsplit('.', 1)

try:
    klass = getattr(__import__(storage_module, fromlist=[storage_class]), storage_class)  # noqa: E501
except ImportError, e:
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