import asyncio
import json
import logging
from logging.config import dictConfig

import aiokafka
import click
import yaml

import memconsumer
from utils import get_logger, set_log_id, start_eldm

# Thu: need to ensure that on_partitions_revoked doesn't finish before all msgs in flight have be handled.
# Fri: there may be locking in aiokafka itself, also in ways that are hard to test for.

# Assumption: RL fixes mem, and mem partitions are determined by *one* other topic.
#   Is this true in our use cases?

# TOOD: inner workings log compaction
# TODO: memory updater topic configurable
# TODO: MCGA (make code great again), polish: there are some things clearly not in the right classes
# TODO: error recovery / defensive programming for recovery from errors / how to restart when there is know corrupted data somewhere / how to make world peace

with open("logging.yaml") as f:
    dictConfig(yaml.load(f, Loader=yaml.SafeLoader))

log = get_logger("counter")
log_timings = get_logger("timings")
lock_log = get_logger("locklog")


async def main(group_id_id):
    asyncio.create_task(start_eldm())

    consumer = memconsumer.AIOKafkaMemConsumer(
        group_id="events_cons",
        mem_unique_id=group_id_id,
        auto_offset_reset="earliest",
        topic="events",
    )
    await consumer.start()

    producer = aiokafka.AIOKafkaProducer()
    await producer.start()

    mem = consumer.get_mem()

    async def handle_msg(msg):
        log.info(f"  Handling msg: {msg.offset}-->{msg.key}:{msg.value}.")
        # the key in mem[key] should be the message key, that is how we align mem data with source
        # topic data.  This is also checked in the AIOKafkaMemConsumer.  There are other solutions
        # to this, but for now we have only implemented this one.  Also we work under the assumption
        # that the source topic doesn't do any custom partition assignments.
        val = mem[msg.key.decode()]
        new_val = int(msg.value.decode())
        if (
            not new_val in val
        ):  # make idempotent; so if commit on mem-update happens, but not of read value don't crash
            val.append(new_val)
        setitem_info = await mem.setitem(
            msg.key.decode(), val
        )  # <------ UGLY but needed (for now)
        await producer.send("event-lists", value=json.dumps(val).encode(), key=msg.key)
        log.info(f"  Done handling msg: {msg.value}")

    try:
        async for msg in consumer.items():
            await handle_msg(msg)
            await consumer.commit()  # this commit should happen after the mem.setitem

    finally:
        print("stopping consumer/producer")
        await consumer.stop()
        await producer.stop()
        print("done")


@click.command()
@click.option("--group-id-id", required=True, type=int)
def cli(group_id_id):
    set_log_id(group_id_id)
    loop = asyncio.get_event_loop()
    loop.set_debug(enabled=True)
    logging.getLogger("asyncio").setLevel(logging.DEBUG)
    loop.slow_callback_duration = 1
    asyncio.run(main(group_id_id))


if __name__ == "__main__":
    cli()
