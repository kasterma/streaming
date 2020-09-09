import faust
import asyncio
import random

app = faust.App("get-hello")

hello_topic = app.topic("hellos-here")
hello_counts = app.Table('hello_counts', default=int)

@app.agent(hello_topic)
async def get_hello(t):
    async for e in t:   # .group_by(lambda ee: str(ee), name="value_grouped"):
        print(e)
        hello_counts[e] += 1
        for i in range(11):  # print the whole table
            hh2 = f"hellohello-{i}"
            print(f"count {i} is {hello_counts[hh2]}")
        #await asyncio.sleep(1)  # this was here to see about comits of messages, didn't finish the experiment to see reprocessing happening
        #print(f"commit {e}")

@app.page('/count/')
@app.table_route(table=hello_counts, query_param='i')
async def get_count(web, request):
    i = request.query['i']
    print(f"request {i}")
    return web.json({i: hello_counts[i]})
