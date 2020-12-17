import aiokafka
import asyncio
import click
from kafka import TopicPartition
from collections import defaultdict
import json
import uuid
from typing import Dict, List
import logging
from logging.config import dictConfig
import yaml
import copy
import time

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

log = logging.getLogger("counter")
log_timings = logging.getLogger("timings")


class Timer:
    def __init__(self, label):
        self.label = label
        self.start = None
        self.end = None
        self.running = False

    def start(self):
        if self.running:
            log.error(f"[{self.label}] starting running timer")
        self.start = time.monotonic()
        self.running = True

    def end(self):
        if not self.running:
            log.error(f"[{self.label}] stopping stopped timer")
        self.end = time.monotonic()
        return self.end - self.start()

    def log(self):
        took = self.end()
        log_timings.info(f"[{self.label}] Took {took}.")


class CustomAdapter(logging.LoggerAdapter):
    def __init__(self, log):
        super().__init__(log, {})
        self.id = "unset"

    def set_id(self, id):
        self.id = str(id)

    def process(self, msg, kwargs):
        return f'id[{self.id}] - {msg}', kwargs


log = CustomAdapter(log)
log_timings = CustomAdapter(log_timings)


class IncorrectMemException(Exception):
    pass


class SnapshotInconsistentException(Exception):
    pass


class UnstartedMemUsed(Exception):
    pass


class Mem:
    def __init__(self, group_id_id, memupdate_topicname="mem-updater"):
        # we should check here existence of the topic and that it has the right number of partitions.
        # maybe even check that when writing the item goes to the right partition
        self.group_id_id = group_id_id
        self._mem: Dict[str, List[int]] = defaultdict(list)
        self.memupdate_topicname = memupdate_topicname
        self.producer = aiokafka.AIOKafkaProducer()
        self.snapshots = [{}]  # start with empty snapshot so that below we can assume there always is a previous
        self.started = False

    async def start(self):
        await self.producer.start()
        self.started = True

    def _snapshot(self):
        self.snapshots.append(copy.deepcopy(self._mem))

    def _check_snapshot_consistency(self):
        # check that current mem is consistent with snapshots
        for key in self._mem.keys():
            # check key in history
            for ss in reversed(self.snapshots):
                if key in ss.keys():
                    # already know the items are internally correct b/c _setitem contains mem_correct
                    old_val = ss[key]
                    new_val = self._mem[key]
                    if not (old_val[0] == new_val[0] and old_val[-1] <= new_val[-1]):
                        raise SnapshotInconsistentException([self._mem, self.snapshots])
                    break

    def _setitem(self, key: str, value: List[int]):
        if not self.started:
            raise UnstartedMemUsed()
        self._mem[key] = value
        log.debug(f"_mem {self}")
        if not self.mem_correct():
            log.error("Mem not correct")
            raise IncorrectMemException(self)

    async def setitem(self, key: str, value: List[int]):
        self._setitem(key, value)
        return await self.producer.send(topic=self.memupdate_topicname,
                                        key=key.encode(),
                                        value=json.dumps(self._mem[key]).encode())

    def __getitem__(self, item: str) -> List[int]:
        if not self.started:
            raise UnstartedMemUsed()
        return self._mem[item]

    @staticmethod
    def shortlist(l):
        l_min, l_max = min(l), max(l)
        if l == list(range(l_min, l_max + 1)) and len(l) > 3:
            # good
            return f"[{l[0]}, ..., {l[-1]}]"
        else:
            # bad, or short
            return str(l)

    @staticmethod
    def value_correct(l):
        return l == list(range(len(l)))

    def mem_correct(self):
        return all(self.value_correct(v) for v in self._mem.values())

    async def update(self, topic_partitions):
        self._snapshot()
        self._mem = defaultdict(list)
        # b/c all on_partitions_revoked have been called nothing is getting produced to the topic anymore
        # that means we can add tokens that we can read back to see we are fully up to date
        log.info(f"Updating mem for partitions {sorted(p.partition for p in topic_partitions)} : {topic_partitions}")
        if not topic_partitions:
            log.info("no partitions so we don't do anything with mem.")
            return

        if len(set(p.topic for p in topic_partitions)) > 1:
            raise Exception("boom: multiple topics reassinged, unexpected")

        partitions_done = {p.partition: False for p in topic_partitions}

        uptodate_token = uuid.uuid4().bytes

        # send token into all partitions
        token_producer = aiokafka.AIOKafkaProducer()
        await token_producer.start()
        for topic_partition in topic_partitions:
            await token_producer.send(self.memupdate_topicname,
                                      partition=topic_partition.partition,
                                      key="token".encode(),  # to allow for compaction, don't need earlier uptodate_token
                                      value=uptodate_token)
        await token_producer.stop()
        log.debug("produced tokens to mem-updater topic.")

        memupdater_consumer = aiokafka.AIOKafkaConsumer(
            group_id=f"mem-updater-{self.group_id_id}", auto_offset_reset='earliest',
        )

        await memupdater_consumer.start()
        parts = [TopicPartition(self.memupdate_topicname, t.partition) for t in topic_partitions]
        memupdater_consumer.assign(
            partitions=[TopicPartition(self.memupdate_topicname, t.partition) for t in topic_partitions])
        await memupdater_consumer.seek_to_beginning(*parts)
        while any(not partitions_done[p.partition] for p in topic_partitions):
            log.debug(f"getting msg from mem-updater topic, state: {partitions_done}.")
            msg = await memupdater_consumer.getone()
            log.debug(f"msg {msg} in partition {msg.partition}")
            if msg.value == uptodate_token:
                log.debug("msg was current uptodate_token.")
                partitions_done[msg.partition] = True
            else:
                try:
                    headers = {k: v.decode() for k, v in
                               msg.headers}  ## not yet used, but for tracing / types / updates
                    key = msg.key.decode()
                    value = json.loads(msg.value.decode())
                    self._setitem(key, value)
                    log.debug(f"Mem updated: {key} with value: {value}")
                except UnicodeDecodeError as e:
                    log.debug(f"Expect decode errors here {e}: {msg} should be outdated uptodate_token.")

        await memupdater_consumer.stop()
        self._check_snapshot_consistency()
        log.info(f"Mem update complete {self}.")

    def __str__(self):
        ks = sorted(self._mem.keys())
        rv = "{\n"
        for k in ks:
            rv += f"{k}: {self.shortlist(self._mem[k])},\n"
        return rv[:-2] + "}"


class RebalanceListener(aiokafka.ConsumerRebalanceListener):
    def __init__(self, consume_lock: asyncio.Lock, mem: Mem):
        self.mem = mem
        self.consume_lock = consume_lock
        self.timer = Timer("rebalance")

    async def on_partitions_revoked(self, revoked):
        log.info(f"Revoked {revoked}")
        self.timer.start()
        await self.consume_lock.acquire()  # pause processing of messages, when past this point no messages in flight
        log.debug("now have lock, i.e. no messages in flight")

    async def on_partitions_assigned(self, assigned):
        log.info(f"Assigned {assigned}")
        await self.mem.update(assigned)
        self.consume_lock.release()  # start processing of messages again, partitions assigned are table
        self.timer.log()
        log.debug("lock released; msg can fly again")
        # TODO: is it ok to release lock in on revoked (just ensure there is no message in flight, then ok???)



async def handle_msg(msg, mem):
    log.info(f"  Handling msg: {msg.offset}-->{msg.key}:{msg.value}.")
    val = mem[msg.key.decode()]
    val.append(int(msg.value.decode()))
    setitem_info = await mem.setitem(msg.key.decode(), val)
    #log.info(f"setiteminfo ={setitem_info.result()}")   # check partition here  msg.partition == partition of result
    log.info(f"  Done handling msg: {msg.value}")


async def main(group_id_id):
    mem = Mem(group_id_id=group_id_id)
    await mem.start()
    lock = asyncio.Lock()

    # we read keyed msg from consumer, collate the into lists that we produce
    consumer = aiokafka.AIOKafkaConsumer(group_id="events_cons", enable_auto_commit=False, auto_offset_reset='earliest')
    await consumer.start()
    producer = aiokafka.AIOKafkaProducer()
    await producer.start()

    rbl = RebalanceListener(lock, mem)
    consumer.subscribe(["events"], listener=rbl)
    await mem.update(consumer.assignment())

    log.info("STARTUP COMPLETE")

    # await asyncio.sleep(10)

    try:
        # for two topics; do we need two locks, are they going to deadlock?
        while True:
            async with lock:
                try:
                    msg = await asyncio.wait_for(consumer.getone(), 1)  # defensive against deadlock with lock
                    await handle_msg(msg, mem)
                    await consumer.commit()    # can we make a transaction of produced in handle_msg and this commit?
                    log.debug(
                        f"  Committed {await consumer.committed(TopicPartition(msg.topic, msg.partition))}, assigned {sorted([t.partition for t in consumer.assignment()])}")
                except asyncio.TimeoutError as e:
                    # no messages in timeout time, this is normal behavior in case you produce less than 1 a second.
                    pass

    finally:
        await consumer.stop()
        await producer.stop()


@click.command()
@click.option("--group-id-id", required=True, type=int)
def cli(group_id_id):
    log.set_id(group_id_id)
    log_timings.set_id(group_id_id)
    asyncio.run(main(group_id_id))


if __name__ == "__main__":
    cli()
