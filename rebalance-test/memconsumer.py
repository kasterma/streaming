import asyncio
import copy
import json
import threading
import uuid
from collections import defaultdict
from typing import Dict, List

import aiokafka
from kafka import TopicPartition

from utils import get_logger, Timer

log = get_logger("counter")
log_timings = get_logger("timings")
lock_log = get_logger("locklog")


class IncorrectMemException(Exception):
    pass


class SnapshotInconsistentException(Exception):
    pass


class UnstartedMemUsed(Exception):
    pass


class MemKeyFatalError(Exception):
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
        self._current_key = None

    def set_current_key(self, key: str):
        self._current_key = key

    async def start(self):
        await self.producer.start()
        self.started = True

    async def stop(self):
        await self.producer.stop()

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
            # raise IncorrectMemException(self)  for now we are not throwing this error, b/c it means an error
            # becomes unrecoverable.  No processor can start that attempts to load the incorrect entry.  Just logging
            # and continuing seems the better process for now.

    async def setitem(self, key: str, value: List[int]):
        if not key == self._current_key:
            raise MemKeyFatalError(f"Using key {key} in context of key {self._current_key}")
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
        self._timer: Timer = Timer("rebalance")

    async def on_partitions_revoked(self, revoked):
        log.info(f"revoked thread id {threading.get_ident()}")
        log.info(f"Revoked {revoked}")
        lock_log.info(f"[rbal] before")
        self._timer.start()
        lock_log.info(f"[rbal] acquire")
        await self.consume_lock.acquire()  # pause processing of messages, when past this point no messages in flight
        lock_log.info(f"[rbal] LOCK")
        log.debug("now have lock, i.e. no messages in flight")

    async def on_partitions_assigned(self, assigned):
        log.info(f"assigned thread id {threading.get_ident()}")
        log.info(f"Assigned {assigned}")
        await self.mem.update(assigned)
        lock_log.info(f"[rbal] release")
        self.consume_lock.release()  # start processing of messages again, partitions assigned are table
        lock_log.info(f"[rbal] UNLOCK")
        self._timer.end()
        log_timings.info(self._timer)
        log.debug("lock released; msg can fly again")
        # TODO: is it ok to release lock in on revoked (just ensure there is no message in flight, then ok???)


class AIOKafkaMemConsumer:
    def __init__(self, group_id, mem_unique_id, auto_offset_reset, topic):
        self._consumer = aiokafka.AIOKafkaConsumer(group_id=group_id, enable_auto_commit=False, auto_offset_reset=auto_offset_reset)
        self._topic = topic
        self._mem = Mem(group_id_id=mem_unique_id)
        self._lock = asyncio.Lock()
        self._rbl = RebalanceListener(self._lock, self._mem)

    async def start(self):
        await self._mem.start()
        await self._consumer.start()
        self._consumer.subscribe([self._topic], listener=self._rbl)
        await self._mem.update(self._consumer.assignment())

    def get_mem(self):
        return self._mem

    async def items(self):
        while True:
            async with self._lock:
                lock_log.info(f"[main] LOCK")
                try:
                    msg = await asyncio.wait_for(
                        self._consumer.getone(), 1
                    )  # defensive against deadlock with lock
                    self._mem.set_current_key(msg.key.decode())   # check key assumption on this; using the same keys
                    yield msg
                except asyncio.TimeoutError as e:
                    # no messages in timeout time, this is normal behavior in case you produce less than 1 a second.
                    pass
                lock_log.info(f"[main] release")

    async def commit(self):
        await self._consumer.commit()

    async def stop(self):
        await self._mem.stop()
        await self._consumer.stop()
