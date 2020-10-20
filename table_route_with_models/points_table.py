import faust

class Point(faust.Record, serializer='json'):
    x: int
    y: int

app = faust.App('count_points')
pts_topic = app.topic('points-here', key_type=Point, value_type=Point)

point_count = app.Table('point_count', default=int, key_type=Point)

@app.agent(pts_topic)
async def process(pts: faust.Stream[Point]) -> None:
    async for point in pts:
        point_count[point] += 1
        for k, v in point_count.items():
            print(f"key{k} -> {v}")

# to query, misencode the point and use (Note the numbers encoded as strings):
# curl 'localhost:6669/count/?i=\{"x":"1","y":"1"\}'
@app.page('/count/')
@app.table_route(table=point_count, query_param='i')
async def get_count(web, request):
    i = request.query['i']
    print(f"request {i}")
    try:
        print(f"result {point_count[i]}")
        print(f"point {Point.loads(i)}")
        print(f"result {point_count[Point.loads(i)]}")
    except:
        print(f"erro getting {i}")
    return web.json({i: point_count[Point.loads(i)]})

if __name__ == "__main__":
    app.main()
