import asyncio
from collections import defaultdict

import aiokafka
import click
import json


async def main(source_topic, sink_topic):
    consumer = aiokafka.AIOKafkaConsumer(
        group_id="events_cons_explain",
        enable_auto_commit=False,
        auto_offset_reset="earliest",
    )
    await consumer.start()
    consumer.subscribe([source_topic])

    producer = aiokafka.AIOKafkaProducer()
    await producer.start()

    mem = defaultdict(list)

    async def handle_msg(msg):
        val = mem[msg.key.decode()]
        new_val = int(msg.value.decode())
        if (
            new_val not in val
        ):  # make idempotent; see the time gap between setting this and the consumer.commit
            val.append(new_val)
        print(f"Out value {msg.key.decode()} -> {val}")
        await producer.send(sink_topic, value=json.dumps(val).encode(), key=msg.key)

    try:
        async for msg in consumer:
            print(f"In value {msg.key.decode()} -> {msg.value.decode()}")
            await handle_msg(msg)
            await consumer.commit()

    finally:
        await consumer.stop()
        await producer.stop()


@click.command()
@click.option("--source-topic", type=str)
@click.option("--sink-topic", type=str)
def cli(source_topic, sink_topic):
    asyncio.run(main(source_topic, sink_topic))


if __name__ == "__main__":
    cli()
