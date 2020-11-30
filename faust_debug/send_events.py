import faust
import random
from collections import defaultdict
import json

app = faust.App("send-events")

event_topic = app.topic("raw-events")
event_counts_send = defaultdict(int)

id = 0

@app.timer(interval=1)
async def send_events():
    global id
    val = random.choice(["a", "b", "c", "d", "e", "f"])
    event_counts_send[val] += 1
    await event_topic.send(key=val, value=val, headers={'id': str(id).encode()})
    id += 1
    print(json.dumps(event_counts_send, sort_keys=True))


if __name__ == "__main__":
    app.main()
