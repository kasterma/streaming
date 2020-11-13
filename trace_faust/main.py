from typing import Optional
from fastapi import FastAPI, Request
from fastapi_contrib.tracing.middlewares import OpentracingMiddleware, request_span
from fastapi_contrib.tracing.utils import setup_opentracing
from fastapi_contrib.conf import settings
from opentracing.propagation import Format
import contextvars
import random
import asyncio
import aiohttp

app = FastAPI()

@app.on_event('startup')
async def startup():
    setup_opentracing(app)
    app.add_middleware(OpentracingMiddleware)

store = {}

@app.get("/")
async def read_root():
    return {"Hello": "World"}

mod_url = "http://localhost:8000/test/"

async def call_test(request):
    tracer = request.app.state.tracer
    headers = {}
    tracer.inject(request_span.get(), Format.HTTP_HEADERS, headers)
    async with aiohttp.ClientSession() as session:
        async with session.get(mod_url, headers=headers) as response:
            return await response.text()


@app.get("/items/{item_id}")
async def read_item(item_id: str, request: Request, q: Optional[str] = None, ):
    await call_test(request)
    print(request.headers)
    return store.get(item_id, 10)

@app.post("/items/{item_id}")
async def set_item_value(item_id: str, value: int):
    store[item_id] = value
    return "ok"

@app.get("/test/")
async def test_test():
    # await asyncio.sleep(random.uniform(0.0, 0.5))
    print("test")
    return "ok"


settings.service_name="fastapi_webserver"
settings.jaeger_host="localhost"
settings.trace_id_header="uber-trace-id"
