from collections import defaultdict
import time
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import asyncio
import random

import logging

logging.basicConfig()
logger = logging.getLogger("example")

loop = asyncio.get_event_loop()

bootstrap_servers = 'localhost:9092'
topic_name = "raw-events"

totals = defaultdict(int)

async def generator():
    producer = AIOKafkaProducer(
    loop=loop, bootstrap_servers=bootstrap_servers)
    await producer.start()

    try:
        while True:
            choice = random.choice(['a', 'b', 'c', 'd', 'e', 'f'])
            headers = [("action_type", "generator".encode())]
            await producer.send_and_wait(topic_name, choice.encode(), key=choice.encode(), headers=headers)
            print(f"produced: {choice}")
            totals[choice] += 1
            totals["sums"] += 1
            if totals["sums"] % 100 == 0:
                print(f"These are the totals: {totals}")
            time.sleep(0.5)
    finally:
        # Wait for all pending messages to be delivered or expire.
        await producer.stop()

loop.run_until_complete(generator())