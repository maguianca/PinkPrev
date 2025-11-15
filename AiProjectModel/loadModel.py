import torch
from model import MammoVit

# Incarca modelul si il trece in modul de evaluare
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = MammoVit().to(device)
model.load_state_dict(torch.load("saved_progress/mammo_vit_epoch05.pth", map_location=device))  # or the epoch you want
model.eval()

from PIL import Image
from torchvision import transforms

# Acelasi transform la imagine ca si pentru training
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.5]*3, [0.5]*3)
])

# Incarcare si procesare de imagine
image_path = "C:\\Files\\UBB an 2 sem 2\\AdditionalMammoVitData\\2017_BC0020761_ CC_R.jpg"
image = Image.open(image_path).convert("RGB")
input_tensor = transform(image).unsqueeze(0).to(device)  

with torch.no_grad():
    output = model(input_tensor)
    probs = torch.softmax(output, dim=1)
    pred_class = torch.argmax(probs, dim=1).item()

# Predictie
label_map = {0: "Benign", 1: "Malignant"}
print(f"Prediction: {label_map[pred_class]} (Confidence: {probs[0][pred_class]:.4f})")