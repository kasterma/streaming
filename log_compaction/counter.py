from collections import defaultdict
from random import random
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import asyncio
import sys

import logging

logging.basicConfig()
logger = logging.getLogger("example")

loop = asyncio.get_event_loop()

bootstrap_servers = 'localhost:9092'
topic_name_raw = "raw-events"
topic_name_compaction = "count-log-compaction"
group_id = "test_group_id"

mem = defaultdict(int)

async def mem_updater():
    consumer = AIOKafkaConsumer(topic_name_compaction,
        loop=loop,
        bootstrap_servers=bootstrap_servers,
        group_id=group_id + sys.argv[1]
    )

    await consumer.start()
    try:
        async for e in consumer:
            headers = {k: v.decode() for k,v in e.headers}
            key = e.key.decode()
            partition = e.partition
            value = e.value.decode()
            if headers["action_type"] == "compacted_log_update":
                mem[key] = int(value)
                print(f"Mem updated: {key} with value: {value}")
    finally:
        consumer.stop()

loop.create_task(mem_updater())


async def counter():

    consumer = AIOKafkaConsumer(topic_name_raw,
        loop=loop,
        bootstrap_servers=bootstrap_servers,
        group_id=group_id
    )
    producer_compaction = AIOKafkaProducer(
        loop=loop, 
        bootstrap_servers=bootstrap_servers
    )

    await consumer.start()
    await producer_compaction.start()

    try:
        while True:
            async for e in consumer:
                headers = {k: v.decode() for k,v in e.headers}
                print("Consuming(counter) ...")
                key = e.key.decode()
                partition = e.partition
                value = e.value.decode()
                if headers["action_type"] == "generator":
                    print(f"Consuming generator event: {key} {value} {partition}")
                    cv = mem[key] + 1
                    headers = [('action_type', 'compacted_log_update'.encode())]
                    await producer_compaction.send(topic_name_compaction, value=str(cv).encode(), key=key.encode(), headers=headers)

    finally:
        await consumer.stop()
        await producer_compaction.stop()

loop.run_until_complete(counter())
loop.close()
