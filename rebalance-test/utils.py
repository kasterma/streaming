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


class EventLoopDelayMonitor:

    def __init__(self, loop=None, start=True, interval=1, logger=None):
        self._interval = interval
        self._log = logger or logging.getLogger("eventloop")
        self._loop = loop or asyncio.get_event_loop()
        if start:
            self.start()

    def run(self):
        self._loop.call_later(self._interval, self._handler, self._loop.time())

    def _handler(self, start_time):
        latency = (self._loop.time() - start_time) - self._interval
        if latency > 0.05:
            self._log.error('    EventLoop delay %.4f', latency)
        else:
            self._log.info('EventLoop delay %.4f', latency)
        if not self.is_stopped():
            self.run()

    def is_stopped(self):
        return self._stopped

    def start(self):
        self._stopped = False
        self.run()

    def stop(self):
        self._stopped = True


async def start_eldm():
    EventLoopDelayMonitor(interval=1)
