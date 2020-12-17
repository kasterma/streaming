import aiokafka
import asyncio
import click
import random


async def main(delay_ms, num_keys):
    producer = aiokafka.AIOKafkaProducer()
    await producer.start()
    keys = [f"key-{i}" for i in range(num_keys)]
    next_item = {k: 0 for k in keys}

    try:
        while True:
            key = random.choice(keys)
            msg = str(next_item[key]).encode()
            await producer.send("events", key=key.encode(), value=msg)
            next_item[key] += 1
            await asyncio.sleep(delay_ms/1000)
    except Exception as e:
        print(f"Error encountered: {repr(e)}")
    finally:
        await producer.stop()


@click.command()
@click.option("--delay-ms", default=1000, type=int)
@click.option("--num-keys", default=5, type=int)
def cli(delay_ms, num_keys):
    asyncio.run(main(delay_ms, num_keys))


if __name__ == "__main__":
    cli()
