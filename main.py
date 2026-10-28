import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.dependencies.frames import (
    get_adapter_websocket_client,
    get_receive_frame_use_case,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    client = get_adapter_websocket_client()
    use_case = get_receive_frame_use_case()

    task = asyncio.create_task(client.listen(use_case.execute))
    yield
    task.cancel()


app = FastAPI(lifespan=lifespan)
