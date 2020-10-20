## faustex

import faust
import asyncio
import random
from collections import defaultdict
import json

app = faust.App("send-points")

class Point(faust.Record, serializer='json', coerce=True):
    x: int
    y: int

pts_topic = app.topic("points-here", key_type=Point, value_type=Point)
pts_counts_send = defaultdict(int)

@app.timer(interval=1)
async def hello():
    coord = str(random.randint(0, 10))
    val = Point(x=coord, y=coord)
    pts_counts_send[coord] += 1
    await pts_topic.send(key=val, value=val)
    print(json.dumps(pts_counts_send, sort_keys=True))

if __name__ == "__main__":
    app.main()
