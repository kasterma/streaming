import time
import logging
import contextvars

class Timer:
    def __init__(self, label):
        self._label = label
        self._start = None
        self._end = None
        self._running = False

    def start(self):
        if not self._running:
            self._start = time.monotonic()
            self._running = True

    def end(self):
        if self._running:
            self._end = time.monotonic()
            self._running = False

    def duration(self):
        try:
            return self._end - self._start
        except TypeError: # not started or ended
            return None

    def __str__(self):
        if self._running:
            return f"Timer({self._label}, running since {self._start})"
        else:
            return f"Timer({self._label}, duration={self.duration()}"


log_id = -1


def set_log_id(i):
    global log_id
    log_id = i


class CustomAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        return f'id[{log_id}] - {msg}', kwargs


def get_logger(name):
    return CustomAdapter(logging.getLogger(name), {})
