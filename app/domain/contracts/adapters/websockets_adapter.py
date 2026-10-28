from abc import ABC, abstractmethod
from typing import Any, Awaitable, Callable, Coroutine
from uuid import UUID

from fastapi import WebSocket


class IWebSocketManagerAdapter(ABC):
    @abstractmethod
    async def connect(self, client: UUID, websocket: WebSocket) -> None:
        ...

    @abstractmethod
    async def send_pessoal_message(self, client: UUID, message: bytes) -> None:
        ...

    @abstractmethod
    async def broadcast_to_local_servers(self, message: bytes | str) -> None:
        ...

    @abstractmethod
    def disconnect(self, client: UUID) -> None:
        ...


class IWebSocketClientadapter(ABC):
    @abstractmethod
    async def listen(
        self, on_message: Callable[[bytes], Coroutine[Any, Any, None]]
    ) -> None:
        ...

    @abstractmethod
    async def send(self, payload: str) -> None:
        ...
