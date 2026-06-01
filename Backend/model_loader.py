import os
import json

import torch
import torch.nn as nn

from torchvision import models

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "plant_model.pth"
)

CLASS_PATH = os.path.join(
    BASE_DIR,
    "models",
    "class_names.json"
)

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

with open(CLASS_PATH, "r") as f:

    class_names = json.load(f)

model = models.efficientnet_b0(
    pretrained=False
)

model.classifier[1] = nn.Linear(
    model.classifier[1].in_features,
    len(class_names)
)

model.load_state_dict(
    torch.load(
        MODEL_PATH,
        map_location=device
    )
)

model = model.to(device)

model.eval()