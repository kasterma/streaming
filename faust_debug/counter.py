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
        id = e.headers['id'].decode()
        if id in ids:
            print("ERROR dup vdkfjaklhaflkjashdflkjashdfkjldhaslkjfhaslk ERROR")
        ids.append(id)
        print(f"ids {ids}")
        e = e.value
        event_counts[e] += 1
        updated.append(e)
        print(f"Updated just {e} last 40 {set(updated[-40:])}")
        await count_topic.send(value={e: event_counts[e]})
        for k,v in sorted(event_counts.items()):
            print(f"{k}: {v}")

if __name__ == "__main__":
    app.main()
