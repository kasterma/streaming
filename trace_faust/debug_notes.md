Setup: generator and 2 counters reading from the same topic with the same consumer-group

After starting up a counter2, crash on the first counter (first time seen):
```
[2020-11-26 11:08:33,820] [24520] [ERROR] [^---Recovery]: Crashed reason=ValueError('Offset must be a positive integer')
Traceback (most recent call last):
  File "/Users/wouter/kpn/examples/streaming/trace_faust/venv/lib/python3.8/site-packages/mode/services.py", line 802, in _execute_task
    await task
  File "/Users/wouter/kpn/examples/streaming/trace_faust/venv/lib/python3.8/site-packages/faust/tables/recovery.py", line 459, in _restart_recovery
    await self._wait(
  File "/Users/wouter/kpn/examples/streaming/trace_faust/venv/lib/python3.8/site-packages/faust/tables/recovery.py", line 556, in _wait
    wait_result = await self.wait_first(coro, signal, timeout=timeout)
  File "/Users/wouter/kpn/examples/streaming/trace_faust/venv/lib/python3.8/site-packages/mode/services.py", line 715, in wait_first
    f.result()  # propagate exceptions
  File "/Users/wouter/kpn/examples/streaming/trace_faust/venv/lib/python3.8/site-packages/faust/tables/recovery.py", line 697, in _seek_offsets
    await consumer.seek_wait(new_offsets)
  File "/Users/wouter/kpn/examples/streaming/trace_faust/venv/lib/python3.8/site-packages/faust/transport/consumer.py", line 1323, in seek_wait
    return await self._thread.seek_wait(partitions)
  File "/Users/wouter/kpn/examples/streaming/trace_faust/venv/lib/python3.8/site-packages/faust/transport/drivers/aiokafka.py", line 725, in seek_wait
    await self.call_thread(self._seek_wait, consumer, partitions)
  File "/Users/wouter/kpn/examples/streaming/trace_faust/venv/lib/python3.8/site-packages/mode/threads.py", line 436, in call_thread
    result = await promise
  File "/Users/wouter/kpn/examples/streaming/trace_faust/venv/lib/python3.8/site-packages/mode/threads.py", line 383, in _process_enqueued
    result = await maybe_async(method(*args, **kwargs))
  File "/Users/wouter/kpn/examples/streaming/trace_faust/venv/lib/python3.8/site-packages/mode/utils/futures.py", line 134, in maybe_async
    return await res
  File "/Users/wouter/kpn/examples/streaming/trace_faust/venv/lib/python3.8/site-packages/faust/transport/drivers/aiokafka.py", line 732, in _seek_wait
    consumer.seek(tp, offset)
  File "/Users/wouter/kpn/examples/streaming/trace_faust/venv/lib/python3.8/site-packages/aiokafka/consumer/consumer.py", line 741, in seek
    raise ValueError("Offset must be a positive integer")
ValueError: Offset must be a positive integer
```

behavior has changed, now both agents have access to all keys, thats might actually be what to expect

Multiple downing agents and bringing them up results in:
```
[^---Recovery]: Crashed reason=KeyError(TP(topic='count-events-event_counts-changelog', partition=0))
Traceback (most recent call last):
  File "/Users/wouter/kpn/examples/streaming/trace_faust/venv/lib/python3.8/site-packages/mode/services.py", line 802, in _execute_task
    await task
  File "/Users/wouter/kpn/examples/streaming/trace_faust/venv/lib/python3.8/site-packages/faust/tables/recovery.py", line 396, in _restart_recovery
    await self._wait(
  File "/Users/wouter/kpn/examples/streaming/trace_faust/venv/lib/python3.8/site-packages/faust/tables/recovery.py", line 556, in _wait
    wait_result = await self.wait_first(coro, signal, timeout=timeout)
  File "/Users/wouter/kpn/examples/streaming/trace_faust/venv/lib/python3.8/site-packages/mode/services.py", line 715, in wait_first
    f.result()  # propagate exceptions
  File "/Users/wouter/kpn/examples/streaming/trace_faust/venv/lib/python3.8/site-packages/faust/tables/recovery.py", line 660, in _build_offsets
    new_value = earliest[tp]
KeyError: TP(topic='count-events-event_counts-changelog', partition=0)
```


More strange behavior:
- seen with GlobalTable: rebalance timeouts
- seen with GlobalTable: timeouts, worker/agent just hangs

Shutting down multiple agents quickly in succession:
```
[2020-11-26 14:33:17,777] [34831] [ERROR] [^---Recovery]: Crashed reason=KeyError(TP(topic='count-events-event_counts-changelog', partition=0))
Traceback (most recent call last):
  File "/Users/wouter/kpn/examples/streaming/trace_faust/venv/lib/python3.8/site-packages/mode/services.py", line 802, in _execute_task
    await task
  File "/Users/wouter/kpn/examples/streaming/trace_faust/venv/lib/python3.8/site-packages/faust/tables/recovery.py", line 374, in _restart_recovery
    await self._wait(
  File "/Users/wouter/kpn/examples/streaming/trace_faust/venv/lib/python3.8/site-packages/faust/tables/recovery.py", line 556, in _wait
    wait_result = await self.wait_first(coro, signal, timeout=timeout)
  File "/Users/wouter/kpn/examples/streaming/trace_faust/venv/lib/python3.8/site-packages/mode/services.py", line 715, in wait_first
    f.result()  # propagate exceptions
  File "/Users/wouter/kpn/examples/streaming/trace_faust/venv/lib/python3.8/site-packages/faust/tables/recovery.py", line 660, in _build_offsets
    new_value = earliest[tp]
KeyError: TP(topic='count-events-event_counts-changelog', partition=0)
```