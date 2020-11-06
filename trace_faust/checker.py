import faust

app = faust.App("checker")

count_topic = app.topic("counts")
alert_topic = app.topic("alert")

@app.agent(count_topic)
async def checker(t):
    async for e in t:
        for k, v in e.items():
            if v % 10 == 0:
                val=f"{k} has hapened multiple of 10 times (ct={v})."
                await alert_topic.send(value=val)
                print(val)

if __name__ == "__main__":
    app.main()
