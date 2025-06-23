# backend/config.py
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
YOLO_MODEL_PATH = os.path.join(BASE_DIR, 'model', 'best.pt')
RESNET_MODEL_PATH = os.path.join(BASE_DIR, 'model', 'best.pth')