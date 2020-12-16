import aiokafka
import asyncio
import click
from kafka import TopicPartition
from collections import defaultdict
import json
import uuid
from typing import Dict, List

# Thu: need to ensure that on_partitions_revoked doesn't finish before all msgs in flight have be handled.
# Fri: there may be locking in aiokafka itself, also in ways that are hard to test for.

# Assumption: RL fixes mem, and mem partitions are determined by *one* other topic.
#   Is this true in our use cases?

# TODO: logging improve a little bit (is already GREAT, there is no better logging) MLGA
# TODO: active mem cleaned up
# TODO: keep previous versions of mem for MLGA
# DONE: generator from earliest
# TODO: memory updater topic configurable
# TODO: MCGA (make code great again), polish: there are some things clearly not in the right classes


class Mem:
    def __init__(self, producer):
        self._mem: Dict[str, List[int]] = defaultdict(list)
        self.memupdate_topicname = "mem-updater"
        self.producer = producer

    def _setitem(self, key: str, value: List[int]):
        print(f"before {self._mem}")
        self._mem[key] = value
        print(f"after {self._mem}")

    async def setitem(self, key: str, value: List[int]):
        self._setitem(key, value)
        print("before bdvas;fhdvzfsuifhdabvkhfjasldh")
        await self.producer.send(topic=self.memupdate_topicname,
                                 key=key.encode(),
                                 value=json.dumps(self._mem[key]).encode())
        print("after   dlnksagidyoalbdhyaujdlfkasghdfjaskh")

    def __getitem__(self, item: str) -> List[int]:
        return self._mem[item]


class RebalanceListener(aiokafka.ConsumerRebalanceListener):
    def __init__(self, sleepytime, consume_lock: asyncio.Lock, group_id_id, mem):
        self.mem = mem
        self.group_id_id = group_id_id
        self.consume_lock = consume_lock
        self.st = sleepytime

    async def on_partitions_revoked(self, revoked):
        print("Revoked", revoked)
        await self.consume_lock.acquire()  # pause processing of messages, when past this point no messages in flight
        print("now have lock, i.e. no messages in flight")
        await asyncio.sleep(self.st)

    async def on_partitions_assigned(self, assigned):
        print("Assigned", assigned)
        await self.mem_updater(assigned)
        self.consume_lock.release()  # start processing of messages again, partitions assigned are table
        # TODO: is it ok to release lock in on revoked (just ensure there is no message in flight, then ok???)

    async def mem_updater(self, topic_partitions):
        # b/c all on_partitions_revoked have been called nothing is getting produced to the topic anymore
        # that means we can add tokens that we can read back to see we are fully up to date
        print(f"Updating mem for partitions {sorted(p.partition for p in topic_partitions)} : {topic_partitions}")

        if len(set(p.topic for p in topic_partitions)) > 1:
            raise Exception("boom: multiple topics reassinged, unexpected")

        partitions_done = {p.partition: False for p in topic_partitions}

        uptodate_token = uuid.uuid4().bytes

        # send token into all partitions
        producer = aiokafka.AIOKafkaProducer()
        await producer.start()
        for topic_partition in topic_partitions:
            await producer.send(self.mem.memupdate_topicname,
                                partition=topic_partition.partition,
                                key="token".encode(),  # to allow for compaction, don't need earlier uptodate_token
                                value=uptodate_token)
        await producer.stop()
        print("produced ;lhkjdtr67uygkhjco70-yofjccjhkgopu[uhlgkjvbmnlj;op[]")

        consumer = aiokafka.AIOKafkaConsumer(
            group_id=f"mem-updater-{self.group_id_id}", auto_offset_reset='earliest'
        )

        await consumer.start()
        parts = [TopicPartition(self.mem.memupdate_topicname, t.partition) for t in topic_partitions]
        consumer.assign(partitions=[TopicPartition(self.mem.memupdate_topicname, t.partition) for t in topic_partitions])
        while any(not partitions_done[p.partition] for p in topic_partitions):
            print(f"stuff lhgkviuhjcujhcughkjvcguuhkgjvnbmhiop {partitions_done} {[await consumer.committed(p) for p in parts]}")
            msg = await consumer.getone()
            print(f"more sturfff {msg.partition}")
            if msg.value == uptodate_token:
                print(f"xxx")
                partitions_done[msg.partition] = True
                print(f"donedone {partitions_done}")
            else:
                print(f"xxxysssys")
                try:
                    headers = {k: v.decode() for k,v in msg.headers}  ## not yet used, but for tracing / types / updates
                    key = msg.key.decode()
                    value = json.loads(msg.value.decode())
                    # noinspection PyProtectedMember
                    self.mem._setitem(key, value)
                    print(f"Mem updated: {key} with value: {value}")
                except Exception as e:
                    print(f"Expect decode errors here {e}")

        await consumer.stop()
        print(f"het gaat gewoon goed, sukkel")


async def handle_msg(msg, mem):
    print(f"  Handling msg: {msg.offset}-->{msg.key}:{msg.value}.")
    val = mem[msg.key.decode()]
    val.append(int(msg.value.decode()))
    print(f"       Set to value {val}  <--- {int(msg.value.decode())}")
    await mem.setitem(msg.key.decode(),
                      val)
    print(f"  Done handling msg: {msg.value}")


async def main(msg_sleep, rb_sleepytime, group_id_id):
    producer = aiokafka.AIOKafkaProducer()
    await producer.start()
    mem = Mem(producer)
    lock = asyncio.Lock()
    consumer = aiokafka.AIOKafkaConsumer(group_id="events_cons", enable_auto_commit=False, auto_offset_reset='earliest')
    await consumer.start()
    rbl = RebalanceListener(rb_sleepytime, lock, group_id_id, mem)
    consumer.subscribe(["events"], listener=rbl)
    await rbl.mem_updater(consumer.assignment())

    try:
        # for two topics; do we need two locks, are they going to deadlock?
        while True:
            async with lock:
                try:
                    msg = await asyncio.wait_for(consumer.getone(), 1)  # defensive against deadlock with lock
                    await handle_msg(msg, mem)
                    await consumer.commit()
                    print(f"  Committed {await consumer.committed(TopicPartition(msg.topic, msg.partition))}, assigned {sorted([t.partition for t in consumer.assignment()])}")
                except asyncio.TimeoutError as e:
                    # print(f"timeout error {e}")  # this is perfectly fine, maybe no events to handle
                    pass

    except Exception as e:
        print(f"Error encountered: {e}")
    finally:
        await consumer.stop()


@click.command()
@click.option("--msg-sleep", default=1, type=int, help="seconds to sleep per msg")
@click.option("--sleepytime", default=0, type=int)
@click.option("--group-id-id", required=True, type=int)
def cli(msg_sleep, sleepytime, group_id_id):
    asyncio.run(main(msg_sleep, sleepytime, group_id_id))


if __name__ == "__main__":
    cli()
