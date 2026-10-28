from tabnanny import verbose
from typing import List, cast

import cv2
import numpy as np
from ultralytics import YOLO

from ultralytics.engine.results import Results

from app.domain.contracts.adapters.llm_adapter import IObjectDetector
from app.domain.entities.detection import DetectionEntity


class YoloDetectorAdapter(IObjectDetector):
    def __init__(self, model: str, conf: float) -> None:
        self.model = YOLO(model)
        self.conf = conf
        self.model(np.zeros((240, 320, 3), dtype=np.uint8), verbose=False)

    def detect(self, image: bytes) -> List[DetectionEntity]:
        frame = cv2.imdecode(np.frombuffer(image, np.uint8), cv2.IMREAD_COLOR)
        if frame is None:
            return []

        height, width = frame.shape[:2]

        results = cast(
            list[Results], self.model(frame, conf=self.conf, verbose=False)
        )
        result = results[0]
        if result.boxes is None:
            return []

        detections = []
        for box in result.boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            center_x = (x1 + x2) / 2

            if center_x < width / 3:
                position = 'esquerda'
            elif center_x > 2 * width / 3:
                position = 'direita'
            else:
                position = 'centro'

            detections.append(
                DetectionEntity(
                    label=result.names[int(box.cls[0])],
                    confidence=float(box.conf),
                    position=position,
                    area_ratio=((x2 - x1) * (y2 - y1)) / (width * height),
                )
            )
        return detections
