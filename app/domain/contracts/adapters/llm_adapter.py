from abc import ABC, abstractmethod
from typing import List

from app.domain.entities.detection import DetectionEntity


class IObjectDetector(ABC):
    @abstractmethod
    def detect(self, image: bytes) -> List[DetectionEntity]:
        ...
