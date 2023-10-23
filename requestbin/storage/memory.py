import operator  # noqa: F401
import time

from requestbin import config

from ..models_data import Bin


class MemoryStorage:
    cleanup_interval = config.CLEANUP_INTERVAL

    def __init__(self):
        self.bins = {}
        self.request_count = 0

    def do_start(self):
        self.spawn(self._cleanup_loop)

    def _cleanup_loop(self):
        while True:
            self.async.sleep(self.cleanup_interval)  # noqa: W606
            self._expire_bins()

    def _expire_bins(self):
        expiry = time.time() - config.BIN_TTL
        for name, bin in self.bins.items():
            if bin.created < expiry:
                self.bins.pop(name)

    def create_bin(self, private=False):
        bin = Bin(private)
        self.bins[bin.name] = bin
        return self.bins[bin.name]

    def create_request(self, bin, request):
        bin.add(request)
        self.request_count += 1

    def count_bins(self):
        return len(self.bins)

    def count_requests(self):
        return self.request_count

    def avg_req_size(self):
        return None

    def lookup_bin(self, name):
        return self.bins[name]

    def expiry_time(self, name):
        expiry = self.bins[name].created - (time.time() - config.BIN_TTL)
        return int(expiry)
