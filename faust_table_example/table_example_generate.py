"""
Table example from https://faust.readthedocs.io/en/latest/introduction.html expanded to test some items.
"""

import faust
import random
import string

def rand_str(k=10):
    return "".join(random.choices(string.ascii_letters, k=k))

# this model describes how message values are serialized
# in the Kafka "orders" topic.
class Order(faust.Record, serializer='json'):
    account_id: str
    product_id: str
    amount: int
    price: float

app = faust.App('hello-app-generate', broker='kafka://localhost')
orders_kafka_topic = app.topic('orders', key_type=Order, value_type=Order)

# our table is sharded amongst worker instances, and replicated
# with standby copies to take over if one of the nodes fail.
order_count_by_account = app.Table('order_count', default=int)

@app.timer(interval=1)
async def generate() -> None:
    order = Order(account_id=rand_str(), product_id=rand_str(), amount=random.randint(1, 30), price=random.random())
    print(order)
    await orders_kafka_topic.send(key=order, value=order)

if __name__ == "__main__":
    app.main()
