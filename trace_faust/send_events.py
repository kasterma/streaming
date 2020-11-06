import faust
import random
from collections import defaultdict
import json
from traceutils import init_tracer

tracer = init_tracer('send_events')

app = faust.App("send-events")

event_topic = app.topic("raw-events")
event_counts_send = defaultdict(int)

@app.timer(interval=1)
async def send_events():
    with tracer.start_span('send-event') as span:
        val = random.choice(["a", "b", "c", "d", "e", "f"])
        event_counts_send[val] += 1
        await event_topic.send(value=val)
        print(json.dumps(event_counts_send, sort_keys=True))


if __name__ == "__main__":
    app.main()
