"""
Table example from https://faust.readthedocs.io/en/latest/introduction.html expanded to test some items.
"""

import faust

# this model describes how message values are serialized
# in the Kafka "orders" topic.
class Order(faust.Record, serializer='json'):
    account_id: str
    product_id: str
    amount: int
    price: float

app = faust.App('hello-app', broker='kafka://localhost')
orders_kafka_topic = app.topic('orders', key_type=Order, value_type=Order)
orders_by_id_topic = app.topic('orders-by-id', key_type=str, value_type=Order)

# our table is sharded amongst worker instances, and replicated
# with standby copies to take over if one of the nodes fail.
order_count_by_account = app.Table('order_count', default=int, key_type=str, schema=faust.Schema(key_type=str, key_serializer="raw"))

@app.agent(orders_kafka_topic)
async def process(orders: faust.Stream[Order]) -> None:
    async for order in orders.group_by(Order.account_id, topic=orders_by_id_topic):
        order_count_by_account[order.account_id] += 1
        for k, v in order_count_by_account.items():
            print(f"key{k} -> {v}")

@app.page('/count/')
@app.table_route(table=order_count_by_account, query_param='i')
async def get_count(web, request):
    i = request.query['i']
    print(f"request {i}")
    try:
        print(f"result {order_count_by_account[i]}")
    except:
        print(f"erro getting {i}")
    return web.json({i: order_count_by_account[i]})

if __name__ == "__main__":
    app.main()
