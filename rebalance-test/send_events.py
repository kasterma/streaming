import aiokafka
import asyncio
import click
import random


async def main():
    producer = aiokafka.AIOKafkaProducer()
    await producer.start()
    keys = [f"key-{i}" for i in range(10)]
    next_item = {k: 0 for k in keys}

    try:
        while True:
            key = random.choice(keys)
            msg = str(next_item[key]).encode()
            await producer.send("events", key=key.encode(), value=msg)
            next_item[key] += 1
            await asyncio.sleep(20)
    except Exception as e:
        print(f"Error encountered: {repr(e)}")
    finally:
        await producer.stop()


@click.command()
def cli():
    asyncio.run(main())


if __name__ == "__main__":
    cli()
