import asyncio
from collections import defaultdict

import aiokafka
import click
import json

mem = defaultdict(list)


async def main(source_topic, sink_topic):
    consumer = aiokafka.AIOKafkaConsumer(group_id="events_cons", enable_auto_commit=False, auto_offset_reset='earliest')
    await consumer.start()
    consumer.subscribe([source_topic])

    producer = aiokafka.AIOKafkaProducer()
    await producer.start()

    async def handle_msg(msg):
        val = mem[msg.key.decode()]
        new_val = int(msg.value.decode())
        if new_val not in val:  # make idempotent
            val.append(new_val)
        await producer.send(sink_topic, value=json.dumps(val).encode(), key=msg.key)


    try:
        while True:
            try:
                msg = await asyncio.wait_for(consumer.getone(), 1)  # defensive against deadlock with lock
                await handle_msg(msg)
                await consumer.commit()    # can we make a transaction of produced in handle_msg and this commit?
            except asyncio.TimeoutError as e:
                # no messages in timeout time, this is normal behavior in case you produce less than 1 a second.
                pass

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