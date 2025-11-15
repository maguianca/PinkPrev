from collections import Counter
from timm import create_model
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader, random_split
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
import matplotlib.pyplot as plt
from torch.utils.data import WeightedRandomSampler
import seaborn as sns

import torch
import torch.nn as nn

# Transformări
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.Grayscale(num_output_channels=3),  # Ensure 3 channels for pretrained models
    transforms.ToTensor(),
    transforms.Normalize([0.5]*3, [0.5]*3)
])

# Încărcare dataset complet
full_dataset = datasets.ImageFolder('../dataINbreast/CC-converted', transform=transform)

# Împărțire 80-20 pentru train și val
train_size = int(0.7 * len(full_dataset))
val_size = len(full_dataset) - train_size
train_dataset, val_dataset = random_split(
    full_dataset, [train_size, val_size],
    generator=torch.Generator().manual_seed(42)  # reproducibilitate
)

# Extragem etichetele doar pentru subsetul de training
train_targets = [full_dataset.targets[i] for i in train_dataset.indices]

# Calculează ponderile inverse în funcție de frecvența claselor
class_counts = Counter(train_targets)
class_weights = [1.0 / class_counts[t] for t in train_targets]
sample_weights = torch.DoubleTensor(class_weights)

# Sampler ponderat pentru datele de antrenare
sampler = WeightedRandomSampler(sample_weights, num_samples=len(sample_weights), replacement=True)

# DataLoader pentru train și val
train_loader = DataLoader(train_dataset, batch_size=32, sampler=sampler)
val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)

# Model Vision Transformer preantrenat
# model = create_model('vit_tiny_patch16_224', pretrained=True)
# Înlocuirea claselor de ieșire
# model.head = nn.Linear(model.head.in_features, 2)  # 2 clase: benign vs malign

from torchvision.models import resnet50
model = resnet50(pretrained=True)
model.fc = nn.Linear(model.fc.in_features, 2)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# model.to(device)

# criterion = CrossEntropyLoss()
class_weights = torch.tensor([1.0,1.05]).to(device)
criterion = nn.CrossEntropyLoss(weight=class_weights)

optimizer = optim.Adam(model.parameters(), lr=0.001)

for epoch in range(5):
    model.train()
    total_loss = 0
    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)
        optimizer.zero_grad()
        output = model(images)
        loss = criterion(output, labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()

    print(f"Epoch {epoch + 1}, Loss: {total_loss / len(train_loader):.4f}")

model.eval()

torch.save(model.state_dict(), 'resnet50_mammo_new.pth')

model.eval()
all_preds = []
all_labels = []

with torch.no_grad():
    for images, labels in val_loader:
        images = images.to(device)
        outputs = model(images)
        preds = torch.argmax(outputs, dim=1).cpu()
        all_preds.extend(preds.numpy())
        all_labels.extend(labels.numpy())

# ⬇️ Matricea de confuzie și scorurile
cm = confusion_matrix(all_labels, all_preds)
report = classification_report(all_labels, all_preds, target_names=['benign', 'malign'])
accuracy = accuracy_score(all_labels, all_preds)

# 📊 Afișare în consolă
print("=== Clasificare ===")
print(report)
print(f"Acuratețe totală: {accuracy:.2f}")

# 📈 Grafic: matrice de confuzie
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['Pred benign', 'Pred malign'],
            yticklabels=['True benign', 'True malign'])
plt.title('Matrice de Confuzie')
plt.xlabel('Etichetă prezisă')
plt.ylabel('Etichetă reală')
plt.tight_layout()
plt.show()