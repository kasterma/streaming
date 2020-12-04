from aiokafka import AIOKafkaConsumer
import asyncio

loop = asyncio.get_event_loop()

bootstrap_servers = 'localhost:9092'
topic_name_compaction = "count-log-compaction"
group_id = "test_group_id2"

mem = {}

async def counter():

    consumer_compaction = AIOKafkaConsumer(topic_name_compaction,
        loop=loop,
        bootstrap_servers=bootstrap_servers,
        group_id=group_id,
        auto_offset_reset="earliest"
    )

    await consumer_compaction.start()

    try:
        print('test')
        async for e_comp in consumer_compaction:
            print("test2")
            print(f"log compaction consume: {e_comp.value}")
            mem[e_comp.key] = e_comp.value

    finally:
        await consumer_compaction.stop()

loop.run_until_complete(counter())
loop.close()