import faust
from traceutils import init_tracer
import asyncio
import aiohttp

from opentracing.propagation import Format
from opentracing.tracer import follows_from

tracer = init_tracer('alert')

app = faust.App("checker")

count_topic = app.topic("counts")
alert_topic = app.topic("alert")
mod_url = "http://localhost:8000/items/"

async def get_modulo(key, span):
    headers = {}
    tracer.inject(span, Format.HTTP_HEADERS, headers)
    async with aiohttp.ClientSession() as session:
        async with session.get(mod_url + key, headers=headers) as response:
            return int(await response.text())
 

@app.agent(count_topic)
async def checker(t):
    async for e in t.events():
        headers = e.headers
        headers = {k: v.decode() for k, v in headers.items()}
        print(headers)
        span_ctx = tracer.extract(Format.HTTP_HEADERS, headers)
        with tracer.start_span('check', references=follows_from(span_ctx)) as span:
            for k, v in e.value.items():
                modulo = await get_modulo(k, span)
                span.set_tag("alert", v % modulo == 0)
                span.log_kv({"key": k, "val": v})
                if v % 10 == 0:
                    val=f"{k} has happened multiple of {modulo} times (ct={v})."
                    await alert_topic.send(value=val)
                    print(val)
                    # await asyncio.sleep(1)

if __name__ == "__main__":
    app.main()
