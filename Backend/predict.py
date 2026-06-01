import torch

from torchvision import transforms

from model_loader import (
    model,
    class_names,
    device
)

transform = transforms.Compose([

    transforms.Resize((224, 224)),

    transforms.ToTensor(),

    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

def predict_image(image):

    image = transform(image)

    image = image.unsqueeze(0)

    image = image.to(device)

    with torch.no_grad():

        outputs = model(image)

        probabilities = torch.softmax(
            outputs,
            dim=1
        )

        confidence, predicted = torch.max(
            probabilities,
            1
        )

    predicted_class = class_names[
        predicted.item()
    ]

    crop, disease = predicted_class.split("___")

    disease = disease.replace("_", " ")

    disease = disease.title()

    confidence_score = confidence.item() * 100

    if disease.lower() == "healthy":

        message = f"{crop} leaf is healthy"

    else:

        message = (
            f"{crop} leaf is infected "
            f"with {disease}"
        )

    return {
        "crop": crop,
        "disease": disease,
        "confidence": round(
            confidence_score,
            2
        ),
        "message": message
    }