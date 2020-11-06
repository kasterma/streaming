import faust
from traceutils import init_tracer

from opentracing.propagation import Format
from opentracing.tracer import follows_from

tracer = init_tracer('alert')

app = faust.App("checker")

count_topic = app.topic("counts")
alert_topic = app.topic("alert")

@app.agent(count_topic)
async def checker(t):
    async for e in t.channel:
        headers = e.headers #???
        headers = {k: v.decode() for k, v in headers.items()}
        print(headers)
        span_ctx = tracer.extract(Format.HTTP_HEADERS, headers)
        with tracer.start_span('check', references=follows_from(span_ctx)):
            for k, v in e.value.items():
                if v % 10 == 0:
                    val=f"{k} has hapened multiple of 10 times (ct={v})."
                    await alert_topic.send(value=val)
                    print(val)

if __name__ == "__main__":
    app.main()
