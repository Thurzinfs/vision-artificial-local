from typing import Any, Awaitable, Callable, Coroutine, Dict
from uuid import UUID

from fastapi import WebSocket
import websockets
import asyncio

from app.domain.contracts.adapters.websockets_adapter import (
    IWebSocketClientadapter,
    IWebSocketManagerAdapter,
)


class WebsocketManagerAdapter(IWebSocketManagerAdapter):
    def __init__(self) -> None:
        self.active_connections: Dict[UUID, WebSocket] = {}

    async def connect(self, client: UUID, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections[client] = websocket

    async def send_pessoal_message(self, client: UUID, message: bytes) -> None:
        if client in self.active_connections:
            websocket = self.active_connections[client]
            await websocket.send_bytes(message)

    async def broadcast_to_local_servers(self, message: bytes) -> None:
        for connection in self.active_connections.values():
            await connection.send_bytes(message)

    def disconnect(self, client: UUID) -> None:
        if client in self.active_connections:
            del self.active_connections[client]


class WebSocketClientAdapter(IWebSocketClientadapter):
    def __init__(self, uri: str) -> None:
        self.uri = uri
        self._ws = None
        self._tasks: set[asyncio.Task] = set()

    async def listen(
        self, on_message: Callable[[bytes], Coroutine[Any, Any, None]]
    ) -> None:
        while True:
            try:
                async with websockets.connect(self.uri) as ws:
                    self._ws = ws

                    print(f'conectado: {self.uri}')

                    async for message in ws:
                        data = (
                            message.encode()
                            if isinstance(message, str)
                            else message
                        )
                        task = asyncio.create_task(on_message(data))

                        self._tasks.add(task)

                        task.add_done_callback(self._tasks.discard)

            except (OSError, websockets.ConnectionClosed) as e:
                await asyncio.sleep(5)

            except Exception as e:
                await asyncio.sleep(5)

            finally:
                self._ws = None

    async def send(self, payload: str) -> None:
        ws = self._ws
        if ws is None:
            return

        try:
            await ws.send(payload)
        except websockets.ConnectionClosed:
            return
