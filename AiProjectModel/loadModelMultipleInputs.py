import os
import random
from PIL import Image
import torch
from torchvision import transforms
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

from model import MammoVit

# Setup
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Incarcare model
model = MammoVit().to(device)
model.load_state_dict(torch.load("saved_progress/mammo_vit_epoch05.pth", map_location=device))
model.eval()

# Transformer pt imagini
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.5]*3, [0.5]*3)
])

# Directoare
benign_dir = "C:\\Files\\UBB an 2 sem 2\\ai-projects-pinkprev\\dataMIAS\\benign"
malign_dir = "C:\\Files\\UBB an 2 sem 2\\ai-projects-pinkprev\\dataMIAS\\malign"

def sample_images_from_dir(directory, label, count):
    imgs = [os.path.join(directory, f) for f in os.listdir(directory)
            if f.lower().endswith(('.pgm','.png', '.jpg', '.jpeg'))]
    return random.sample([(img, label) for img in imgs], min(count, len(imgs)))

# Sample 50 img benigne, 50 maligne
benign_samples = sample_images_from_dir(benign_dir, label=0, count=50)
malign_samples = sample_images_from_dir(malign_dir, label=1, count=50)

# merge si shuffle
all_samples = benign_samples + malign_samples
random.shuffle(all_samples)

y_true = []
y_pred = []

with torch.no_grad():
    for img_path, true_label in all_samples:
        image = Image.open(img_path).convert("RGB")
        input_tensor = transform(image).unsqueeze(0).to(device)

        output = model(input_tensor)
        probs = torch.softmax(output, dim=1)
        pred_class = torch.argmax(probs, dim=1).item()

        y_true.append(true_label)
        y_pred.append(pred_class)

# Confusion Matrix
cm = confusion_matrix(y_true, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Benign", "Malignant"])
disp.plot(cmap=plt.cm.Blues)
plt.title("Confusion Matrix")

# Salvare in fisier
plt.savefig("confusion_matrix.png", dpi=300, bbox_inches='tight')
print("Confusion matrix saved as 'confusion_matrix.png'")

# Display
plt.show()
