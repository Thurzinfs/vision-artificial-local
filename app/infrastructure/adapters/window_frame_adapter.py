import os
import time
from typing import List, cast

import cv2
import numpy as np

from app.domain.contracts.adapters.llm_adapter import IObjectDetector
from app.domain.entities.detection import DetectionEntity


class WindowFrameAdapter(IObjectDetector):
    def __init__(self):
        os.makedirs('images', exist_ok=True)

    def detect(self, image: bytes):
        print('teste')
        frame = cv2.imdecode(np.frombuffer(image, np.uint8), cv2.IMREAD_COLOR)

        if frame is None:
            return

        filename = f'images/frame_{int(time.time() * 1000)}.jpg'

        cv2.imwrite(filename, frame)
        print(f'Frame salvo em: {filename}')
