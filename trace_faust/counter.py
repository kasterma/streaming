import faust
from traceutils import init_tracer
from opentracing.propagation import Format

tracer = init_tracer('counter')

app = faust.App("count-events")

event_topic = app.topic("raw-events")
count_topic = app.topic("counts")
event_counts = app.GlobalTable('event_counts', default=int)

updated = []
ids = []

@app.agent(event_topic)
async def counter(t):
    async for e in t.events():
        with tracer.start_span('send-event') as span:
            id = e.headers['id'].decode()
            if id in ids:
                print("ERROR dup vdkfjaklhaflkjashdflkjashdfkjldhaslkjfhaslk ERROR")
            ids.append(id)
            print(f"ids {ids}")
            e = e.value
            event_counts[e] += 1
            updated.append(e)
            print(f"Updated just {e} last 40 {set(updated[-40:])}")
            span.set_tag("count", event_counts[e])
            span.set_tag("key", e)
            with tracer.start_span('send', span):
                headers = {}
                tracer.inject(span, Format.HTTP_HEADERS, headers)
                print(headers)
                headers = {k: v.encode() for k, v in headers.items()}
                await count_topic.send(value={e: event_counts[e]}, headers=headers)
            with tracer.start_span('print-table', span):
                for k,v in sorted(event_counts.items()):
                    print(f"{k}: {v}")

if __name__ == "__main__":
    app.main()
