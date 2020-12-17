testing the setup for a log topic

generate events in order per partition
collect these in a list, appending to mem[parition]
then can check at any stage that state is [0, 1, ...., n] with maybe repetitions, but no missing
then go to town on this with restarting all over the place



One error happened in code

    commit f1ff898ac75bd7692daafa46568bdc9be79d2cb9 (HEAD -> feature/rebalance)
    Author: Bart Kastermans <kasterma@kasterma.net>
    Date:   Thu Dec 17 15:18:49 2020 +0100
    
        WIP mem updater (more partitions/keys)

we running quickly in tmux, terminal was frozen to read something, then when unfrozen received error:

Traceback (most recent call last):
  File "/Users/kasterma/projects/streaming/rebalance-test/venv/lib/python3.8/site-packages/aiokafka/consumer/group_coordinator.py", line 953, in commit_offsets
    await asyncio.shield(
  File "/Users/kasterma/projects/streaming/rebalance-test/venv/lib/python3.8/site-packages/aiokafka/consumer/group_coordinator.py", line 1066, in _do_commit_offsets
    raise first_error
kafka.errors.UnknownMemberIdError: [Error 25] UnknownMemberIdError: events_cons

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "counter.py", line 260, in <module>
    cli()
  File "/Users/kasterma/projects/streaming/rebalance-test/venv/lib/python3.8/site-packages/click/core.py", line 829, in __call__
    return self.main(*args, **kwargs)
  File "/Users/kasterma/projects/streaming/rebalance-test/venv/lib/python3.8/site-packages/click/core.py", line 782, in main
    rv = self.invoke(ctx)
  File "/Users/kasterma/projects/streaming/rebalance-test/venv/lib/python3.8/site-packages/click/core.py", line 1066, in invoke
    return ctx.invoke(self.callback, **ctx.params)
  File "/Users/kasterma/projects/streaming/rebalance-test/venv/lib/python3.8/site-packages/click/core.py", line 610, in invoke
    return callback(*args, **kwargs)
  File "counter.py", line 256, in cli
    asyncio.run(main(group_id_id))
  File "/Users/kasterma/.pyenv/versions/3.8.5/lib/python3.8/asyncio/runners.py", line 43, in run
    return loop.run_until_complete(main)
  File "/Users/kasterma/.pyenv/versions/3.8.5/lib/python3.8/asyncio/base_events.py", line 616, in run_until_complete
    return future.result()
  File "counter.py", line 240, in main
    await consumer.commit()
  File "/Users/kasterma/projects/streaming/rebalance-test/venv/lib/python3.8/site-packages/aiokafka/consumer/consumer.py", line 550, in commit
    await self._coordinator.commit_offsets(assignment, offsets)
  File "/Users/kasterma/projects/streaming/rebalance-test/venv/lib/python3.8/site-packages/aiokafka/consumer/group_coordinator.py", line 958, in commit_offsets
    raise Errors.CommitFailedError(
kafka.errors.CommitFailedError: CommitFailedError: ('Commit cannot be completed since the group has already\n            rebalanced and assigned the partitions to another member.\n            This means that the time between subsequent calls to poll()\n            was longer than the configured max_poll_interval_ms, which\n            typically implies that the poll loop is spending too much\n            time message processing. You can address this either by\n            increasing the rebalance timeout with max_poll_interval_ms,\n            or by reducing the maximum size of batches returned in poll()\n            with max_poll_records.\n            ', 'Commit cannot be completed since the group has already rebalanced and may have assigned the partitions to another member')
make: *** [counter5] Error 1



----------------

source venv/bin/activate ; python counter.py --group-id-id 5
2020-12-17 15:46:47,087 - INFO - id[5] - Updating mem for partitions [] : set()
2020-12-17 15:46:47,105 - INFO - id[5] - Revoked set()
2020-12-17 15:46:50,640 - INFO - id[5] - Assigned {TopicPartition(topic='events', partition=6), TopicPartition(topic='events', partition=2)}
2020-12-17 15:46:50,640 - INFO - id[5] - Updating mem for partitions [2, 6] : {TopicPartition(topic='events', partition=6), TopicPartition(topic='events', partition=2)}
2020-12-17 15:46:50,651 - INFO - id[5] -   Handling msg: 7903-->b'key-587':b'91'.
2020-12-17 15:46:50,651 - ERROR - id[5] - Mem not correct
2020-12-17 15:46:50,753 - ERROR - id[5] - Mem not correct
Traceback (most recent call last):
  File "counter.py", line 292, in <module>
    cli()
  File "/Users/kasterma/projects/streaming/rebalance-test/venv/lib/python3.8/site-packages/click/core.py", line 829, in __call__
    return self.main(*args, **kwargs)
  File "/Users/kasterma/projects/streaming/rebalance-test/venv/lib/python3.8/site-packages/click/core.py", line 782, in main
    rv = self.invoke(ctx)
  File "/Users/kasterma/projects/streaming/rebalance-test/venv/lib/python3.8/site-packages/click/core.py", line 1066, in invoke
    return ctx.invoke(self.callback, **ctx.params)
  File "/Users/kasterma/projects/streaming/rebalance-test/venv/lib/python3.8/site-packages/click/core.py", line 610, in invoke
    return callback(*args, **kwargs)
  File "counter.py", line 288, in cli
    asyncio.run(main(group_id_id))
  File "/Users/kasterma/.pyenv/versions/3.8.5/lib/python3.8/asyncio/runners.py", line 43, in run
    return loop.run_until_complete(main)
  File "/Users/kasterma/.pyenv/versions/3.8.5/lib/python3.8/asyncio/base_events.py", line 616, in run_until_complete
    return future.result()
  File "counter.py", line 270, in main
    await handle_msg(msg, mem)
  File "counter.py", line 244, in handle_msg
    setitem_info = await mem.setitem(msg.key.decode(), val)
  File "counter.py", line 125, in setitem
    self._setitem(key, value)
  File "counter.py", line 122, in _setitem
    raise IncorrectMemException(self)
__main__.IncorrectMemException: {
key-163: [0, ..., 67],
key-587: [91]}
make: *** [counter5] Error 1
