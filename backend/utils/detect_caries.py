# backend/utils/detect_caries.py
import torch
import torchvision.transforms as transforms
from torchvision import models
import numpy as np
import cv2
from config import RESNET_MODEL_PATH

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = models.resnet18()
model.fc = torch.nn.Linear(model.fc.in_features, 2)  # 이진 분류
model.load_state_dict(torch.load(RESNET_MODEL_PATH, map_location=device))
model.to(device).eval()

transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

def detect_caries(crops):
    results = []
    for crop in crops:
        input_tensor = transform(crop).unsqueeze(0).to(device)
        output = model(input_tensor)
        pred = torch.argmax(output, dim=1).item()
        results.append(pred)  # 0: 정상, 1: 충치
    return results