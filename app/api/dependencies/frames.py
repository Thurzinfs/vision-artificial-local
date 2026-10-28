from functools import lru_cache

from fastapi import Depends

from app.application.use_cases.frame import ReceiveFrameUseCase
from app.domain.contracts.adapters.llm_adapter import IObjectDetector
from app.domain.contracts.adapters.websockets_adapter import (
    IWebSocketClientadapter,
)
from app.infrastructure.adapters.websockets_adapter import (
    WebSocketClientAdapter,
)
from app.infrastructure.adapters.yolo_detector_adapter import (
    YoloDetectorAdapter,
)
from app.infrastructure.adapters.yolo_translator_adapter import (
    YoloTranslatorAdapter,
)
from app.infrastructure.adapters.window_frame_adapter import WindowFrameAdapter
from config import settings


def get_yolo_adapter() -> IObjectDetector:
    return YoloTranslatorAdapter(
        YoloDetectorAdapter(model=settings.LLM_MODEL, conf=settings.LLM_CONF)
    )


def get_window_adapter() -> WindowFrameAdapter:
    return WindowFrameAdapter()


@lru_cache
def get_adapter_websocket_client() -> IWebSocketClientadapter:
    return WebSocketClientAdapter(settings.CLOUD_WS_URL)


@lru_cache
def get_receive_frame_use_case() -> ReceiveFrameUseCase:
    return ReceiveFrameUseCase(
        llm_adapter=get_yolo_adapter(),
        websocket_client_adapter=get_adapter_websocket_client(),
    )
