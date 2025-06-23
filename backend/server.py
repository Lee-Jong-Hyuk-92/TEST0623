# backend/server.py

from flask import Flask, request, jsonify, send_from_directory
from upload_handler import save_uploaded_image
from utils.predict_yolo_seg import predict_image_with_yolo
from utils.crop_teeth import crop_teeth_from_yolo_result
from utils.detect_caries import detect_caries
from config import UPLOAD_FOLDER
import os
import cv2
import numpy as np
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return "✅ Flask 서버 실행 중!"

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': '파일 없음'}), 400

    file = request.files['file']
    filename = f"{uuid.uuid4().hex}.jpg"
    image_path = save_uploaded_image(file, filename)  # 👉 저장된 경로 반환

    try:
        # 1. YOLO 세그멘테이션
        yolo_result = predict_image_with_yolo(image_path)

        # 2. crop 이미지 리스트
        crops = crop_teeth_from_yolo_result(image_path, yolo_result)

        # 3. 충치 예측
        predictions = detect_caries(crops)

        # 4. 원본 이미지에 세그멘트 라벨 그리기
        image = cv2.imread(image_path)
        for i, seg in enumerate(yolo_result.masks.xy if yolo_result.masks else []):
            color = (0, 0, 255) if predictions[i] == 1 else (255, 0, 0)
            pts = np.array([seg], dtype=np.int32)
            cv2.polylines(image, pts, isClosed=True, color=color, thickness=2)

        # 5. 결과 이미지 저장 (파일명 구분)
        result_filename = f"result_{uuid.uuid4().hex}.jpg"
        result_path = os.path.join(app.config['UPLOAD_FOLDER'], result_filename)
        cv2.imwrite(result_path, image)

        # 6. 절대 경로로 응답
        result_url = request.host_url + "uploads/" + result_filename
        return jsonify({'message': '처리 완료', 'result_url': result_url})

    except Exception as e:
        return jsonify({'error': '예측 중 오류', 'details': str(e)}), 500

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)