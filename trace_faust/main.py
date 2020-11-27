from typing import Optional
from fastapi import FastAPI
from fastapi_contrib.tracing.middlewares import OpentracingMiddleware
from fastapi_contrib.tracing.utils import setup_opentracing


from fastapi_contrib.conf import settings

settings.service_name="fastapi-server"
settings.jaeger_host="localhost"

app = FastAPI()

@app.on_event('startup')
async def startup():
    setup_opentracing(app)
    app.add_middleware(OpentracingMiddleware)

@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
