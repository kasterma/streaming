import faust
from traceutils import init_tracer
import asyncio

from opentracing.propagation import Format
from opentracing.tracer import follows_from

tracer = init_tracer('alert')

app = faust.App("checker")

count_topic = app.topic("counts")
alert_topic = app.topic("alert")

@app.agent(count_topic)
async def checker(t):
    async for e in t:
        for k, v in e.value.items():
            if v % 10 == 0:
                val=f"{k} has happened multiple of 10 times (ct={v})."
                await alert_topic.send(value=val)
                print(val)
                await asyncio.sleep(1)

if __name__ == "__main__":
    app.main()
