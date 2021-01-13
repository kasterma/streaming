"""
Red Paint

A simple but effective way to check if a sewer is functioning well is to throw red coloring in the flow and see how
quickly if appears in different places downstream.  Here we use a similar idea, in the *identical* topics and
transformers we add some items for which we know the behavior that follow, and for which we can then record timing
results, and check correctness.  Idea is that such red paint jobs will also run in production to have constant
monitoring of throughput and correctness.

Here we are given a key that is not used for other jobs (think a dummy customer key) and for that key we generate
events.
"""
from typing import Tuple

import aiokafka
import asyncio
import click
import random
import time
import logging
from logging.config import dictConfig
from collections import defaultdict
import yaml
import json
import sys


with open("logging.yaml") as f:
    dictConfig(yaml.load(f, Loader=yaml.SafeLoader))


class RedPaint:
    """Generate the "customer(s)" behavior where we know downstream results for that we then check for.{key: len(self._in_flight[key].keys()) for key in self._keys}
    While checking these results, also record some timing info.  In this implementation when passed a tuple of
    keys, randomly select the next key to send a value for.
    """

    def __init__(self, keys: Tuple[int, ...], delay=1.0):
        self._keys = keys
        self._delay = delay
        self._next_value = defaultdict(int)
        self._in_flight = defaultdict(dict)
        self._lock: asyncio.Lock = asyncio.Lock()
        self._log = logging.getLogger("redpaint")

    async def pause_sending(self):
        """Stop sending events (if already stopped NOP)"""
        if not self._lock.locked():
            await self._lock.acquire()
            self._log.info("Paused sending of events")

    def start_sending(self):
        """Start sending events again (if not paused NOP)"""
        if self._lock.locked():
            self._lock.release()
            self._log.info("Started sending of events again")

    def is_sending(self):
        return not self._lock.locked()

    def __aiter__(self):
        return self

    async def __anext__(self):
        await asyncio.sleep(self._delay)  # delay between sending values
        async with self._lock:
            key = random.choice(self._keys)
            val = self._next_value[key]
            self._in_flight[key][
                val
            ] = (
                time.monotonic()
            )  # we measure time from the moment of generating the behavior
            self._next_value[key] += 1
            inflight_counts = {
                key: len(self._in_flight[key].keys()) for key in self._keys
            }
            self._log.info(f"In flight event counts {inflight_counts}")
            return (str(key).encode(), str(val).encode())

    def validate(self, pair):
        """Check that the pair is a consistent result of send behavior (may be delayed obviously).

        If there are multiple downstream points to check they will each have their own validate obviously.
        """
        key = int(pair[0].decode())
        val = json.loads(pair[1].decode())
        if key not in self._keys:
            self._log.debug(
                f"Recvd value with key for other user {pair} should have key in {self._keys}."
            )
            return None  # not relevant for this user; will be most messages

        if not val[-1] in self._in_flight[key].keys():
            self._log.error(f"Recvd value not in flight {val} for key {key}")
        else:
            time_taken = time.monotonic() - self._in_flight[key][val[-1]]
            del self._in_flight[key][
                val[-1]
            ]  # remove from dict to keep memory requirement low
            self._log.info(f"Recvd value took {time_taken:.3f} seconds for key {key}")
        valid = self._next_value[key] > val[-1] and val == list(range(val[-1] + 1))
        if not valid:
            self._log.error(
                f"Recvd value was invalid {pair} {self._next_value[key] > val[-1]} {list(range(val[-1]))}"
            )
        return valid


async def send_paint(paint: RedPaint, producer: aiokafka.AIOKafkaProducer):
    async for msg in paint:
        await producer.send("events", key=msg[0], value=msg[1])


async def recv_paint(paint: RedPaint, consumer: aiokafka.AIOKafkaConsumer, wait_notice):
    last_time = time.monotonic()
    wait_ct = (
        1  # if count gets too high, stop generating new events.  Something is broken.
    )
    while True:
        if time.monotonic() - last_time > 10 * wait_ct:
            if paint.is_sending():
                print(f"No valid message in {wait_notice}*{wait_ct} seconds")
            wait_ct += 1
            if wait_ct > 1:
                await paint.pause_sending()
            print("here")
        try:
            msg = await asyncio.wait_for(consumer.getone(), 1)
            if paint.validate((msg.key, msg.value)):
                last_time = time.monotonic()
                wait_ct = 1
                paint.start_sending()
        except asyncio.TimeoutError as e:
            # We are expecting this when there is no big flow of messages through the system
            pass


async def main(delay_ms, red_paint_key):
    consumer = aiokafka.AIOKafkaConsumer(
        group_id="red_paint", enable_auto_commit=True, auto_offset_reset="earliest"
    )
    await consumer.start()
    consumer.subscribe(["event-lists"])
    producer = aiokafka.AIOKafkaProducer()
    await producer.start()
    delay_s = delay_ms / 1000
    paint = RedPaint(keys=red_paint_key, delay=delay_s)

    try:
        # start Task sending events
        send_task = asyncio.create_task(send_paint(paint, producer))
        # start Task receiving events
        recv_task = asyncio.create_task(recv_paint(paint, consumer, delay_s * 10))

        # wait for tasks
        await asyncio.gather(send_task, recv_task, return_exceptions=False)
    finally:
        await consumer.stop()
        await producer.stop()


@click.command()
@click.option(
    "--delay-ms", default=5000, type=int, help="delay between sending different values"
)
@click.option(
    "--red-paint-key", type=int, help="key for the red paint values", multiple=True
)
@click.option(
    "--num-keys",
    type=int,
    help="shortcut for --red-paint-key 0 ... --red-paint-key num-keys-1",
)
def cli(delay_ms, red_paint_key, num_keys):
    if red_paint_key and num_keys:
        print("Please only provide one of red_paint_key or num_keys")
        sys.exit(1)
    if num_keys:
        red_paint_key = tuple(range(num_keys))
    asyncio.run(main(delay_ms, red_paint_key))


if __name__ == "__main__":
    cli()
