from typing import List

from app.domain.contracts.adapters.llm_adapter import IObjectDetector
from app.domain.entities.detection import DetectionEntity


class YoloTranslatorAdapter(IObjectDetector):
    CLASS_TRANSLATIONS = {
        'person': 'pessoa',
        'bicycle': 'bicicleta',
        'car': 'carro',
        'motorcycle': 'motocicleta',
        'airplane': 'avião',
        'bus': 'ônibus',
        'train': 'trem',
        'truck': 'caminhão',
        'boat': 'barco',
        'traffic light': 'semáforo',
        'fire hydrant': 'hidrante',
        'stop sign': 'placa de pare',
        'parking meter': 'parquímetro',
        'bench': 'banco',
        'bird': 'pássaro',
        'cat': 'gato',
        'dog': 'cachorro',
        'horse': 'cavalo',
        'sheep': 'ovelha',
        'cow': 'vaca',
        'elephant': 'elefante',
        'bear': 'urso',
        'zebra': 'zebra',
        'giraffe': 'girafa',
        'backpack': 'mochila',
        'umbrella': 'guarda-chuva',
        'handbag': 'bolsa',
        'tie': 'gravata',
        'suitcase': 'mala',
        'frisbee': 'frisbee',
        'skis': 'esquis',
        'snowboard': 'prancha de snowboard',
        'sports ball': 'bola esportiva',
        'kite': 'pipa',
        'baseball bat': 'taco de beisebol',
        'baseball glove': 'luva de beisebol',
        'skateboard': 'skate',
        'surfboard': 'prancha de surfe',
        'tennis racket': 'raquete de tênis',
        'bottle': 'garrafa',
        'wine glass': 'taça de vinho',
        'cup': 'xícara',
        'fork': 'garfo',
        'knife': 'faca',
        'spoon': 'colher',
        'bowl': 'tigela',
        'banana': 'banana',
        'apple': 'maçã',
        'sandwich': 'sanduíche',
        'orange': 'laranja',
        'broccoli': 'brócolis',
        'carrot': 'cenoura',
        'hot dog': 'cachorro-quente',
        'pizza': 'pizza',
        'donut': 'rosquinha',
        'cake': 'bolo',
        'chair': 'cadeira',
        'couch': 'sofá',
        'potted plant': 'planta em vaso',
        'bed': 'cama',
        'dining table': 'mesa de jantar',
        'toilet': 'vaso sanitário',
        'tv': 'televisão',
        'laptop': 'notebook',
        'mouse': 'mouse',
        'remote': 'controle remoto',
        'keyboard': 'teclado',
        'cell phone': 'celular',
        'microwave': 'micro-ondas',
        'oven': 'forno',
        'toaster': 'torradeira',
        'sink': 'pia',
        'refrigerator': 'geladeira',
        'book': 'livro',
        'clock': 'relógio',
        'vase': 'vaso',
        'scissors': 'tesoura',
        'teddy bear': 'urso de pelúcia',
        'hair drier': 'secador de cabelo',
        'toothbrush': 'escova de dentes',
    }

    def __init__(self, detector: IObjectDetector) -> None:
        self.detector = detector

    def detect(self, image: bytes) -> List[DetectionEntity]:
        detections = self.detector.detect(image)
        return [
            DetectionEntity(
                label=self.CLASS_TRANSLATIONS.get(detection.label, detection.label),
                confidence=detection.confidence,
                position=detection.position,
                area_ratio=detection.area_ratio,
            )
            for detection in detections
        ]
