## faustex

import faust
import asyncio
import random
from collections import defaultdict
import json

app = faust.App("send-hello")

hello_topic = app.topic("hellos-here")
hello_counts_send = defaultdict(int)
    
@app.timer(interval=2)
async def hello():
    key = str(random.randint(0, 10))
    val = f"hellohello-{key}"
    hello_counts_send[val] += 1
    await hello_topic.send(key=val, value=val)
    print(json.dumps(hello_counts_send, sort_keys=True))

if __name__ == "__main__":
    app.main()
