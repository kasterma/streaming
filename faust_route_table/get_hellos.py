import faust

app = faust.App("get-hello")

hello_topic = app.topic("hellos-here")
hello_counts = app.Table('hello_counts', default=int)

@app.agent(hello_topic)
async def get_hello(t):
    async for e in t:
        print(e)
        print(app.conf)
        hello_counts[e.encode()] += 1
        for k,v in hello_counts.items():
            print(f"{k}: {v}")

@app.page('/count/')
@app.table_route(table=hello_counts, query_param='i')
async def get_count(web, request):
    i = request.query['i']
    print(f"request {i}")
    try:
        print(f"result {hello_counts[i]}")
    except:
        print(f"erro getting {i}")
    return web.json({i: hello_counts[i]})

if __name__ == "__main__":
    app.main()
