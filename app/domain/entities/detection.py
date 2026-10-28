from dataclasses import dataclass


@dataclass
class DetectionEntity:
    label: str
    confidence: float
    position: str
    area_ratio: float
