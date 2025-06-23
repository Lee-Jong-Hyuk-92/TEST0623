# backend/utils/predict_yolo_seg.py
from ultralytics import YOLO
from config import YOLO_MODEL_PATH
import cv2

model = YOLO(YOLO_MODEL_PATH)

def predict_image_with_yolo(image_path):
    results = model(image_path)[0]
    return results