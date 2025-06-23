# backend/upload_handler.py
import os
from config import UPLOAD_FOLDER

def save_uploaded_image(file, filename=None):
    if not filename:
        filename = file.filename
    save_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(save_path)
    return save_path