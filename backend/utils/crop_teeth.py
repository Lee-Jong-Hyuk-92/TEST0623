# backend/utils/crop_teeth.py
import cv2
import os
import numpy as np
from config import UPLOAD_FOLDER

def crop_teeth_from_yolo_result(image_path, yolo_result):
    image = cv2.imread(image_path)
    crops = []
    
    crop_dir = os.path.join(UPLOAD_FOLDER, "crop")
    os.makedirs(crop_dir, exist_ok=True)

    for i, seg in enumerate(yolo_result.masks.xy if yolo_result.masks else []):
        mask = np.zeros(image.shape[:2], dtype=np.uint8)
        pts = np.array([seg], dtype=np.int32)
        cv2.fillPoly(mask, pts, 255)

        x, y, w, h = cv2.boundingRect(pts)
        cropped = image[y:y+h, x:x+w]
        crops.append(cropped)

        crop_path = os.path.join(crop_dir, f"crop_{i}.jpg")
        cv2.imwrite(crop_path, cropped)

    return crops