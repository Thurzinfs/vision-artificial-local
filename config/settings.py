import os

from dotenv import load_dotenv


load_dotenv()


BROKER_HOST = os.getenv('BROKER_HOST', '')

BROKER_TOPIC = os.getenv('BROKER_TOPIC', '')

CLOUD_WS_URL = os.getenv('CLOUD_WS_URL', '')

LLM_MODEL = 'yolov8n_openvino_model/'
LLM_CONF = 0.4
