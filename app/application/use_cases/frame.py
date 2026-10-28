import asyncio
import json
from uuid import UUID

from app.domain.contracts.adapters.llm_adapter import IObjectDetector
from app.domain.contracts.adapters.websockets_adapter import (
    IWebSocketClientadapter,
)


class ReceiveFrameUseCase:
    def __init__(
        self,
        llm_adapter: IObjectDetector,
        websocket_client_adapter: IWebSocketClientadapter,
    ) -> None:
        self.detector = llm_adapter
        self.sender = websocket_client_adapter
        self._busy = False

    async def execute(self, data: bytes) -> None:
        if not data or self._busy:
            return

        device_id = UUID(bytes=data[:16])
        image = data[16:]

        self._busy = True

        try:
            detections = await asyncio.to_thread(self.detector.detect, image)

        except Exception as e:
            return

        finally:
            self._busy = False

        if not detections:
            return

        payload = json.dumps(
            {
                'device': str(device_id),
                'detections': [
                    {
                        'label': d.label,
                        'position': d.position,
                        'confidence': d.confidence,
                        'area_ratio': d.area_ratio,
                    }
                    for d in detections
                ],
            }
        )

        print("payload: ", payload)

        await self.sender.send(payload)
