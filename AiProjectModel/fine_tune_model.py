import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader
import torch.optim as optim
from torchvision import transforms
import matplotlib.pyplot as plt

from custom_dataset import MammogramDataset
from model import MammoVit

# Antrenare pe CPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)

# Transform pe 224x224
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.5]*3, [0.5]*3)
])

# Creare Dataset si DataLoader
dataset = MammogramDataset(root_dir="C:\\Files\\UBB an 2 sem 2\\rawDataMammoVit", transform=transform)
dataloader = DataLoader(dataset, batch_size=8, shuffle=True)

# Instantiere Model
model = MammoVit().to(device)
optimizer = optim.AdamW(model.parameters(), lr=1e-4, weight_decay=1e-4)

# Plot data
train_losses = []
train_accuracies = []

# Training loop
for epoch in range(5):
    model.train()
    total_loss = 0
    total_correct = 0
    total_samples = 0

    for imgs, labels, paths in dataloader:
        for path in paths:
            print(f"Training on file: {path}")
        imgs, labels = imgs.to(device), labels.to(device)
        logits = model(imgs)
        loss = F.cross_entropy(logits, labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()
        preds = logits.argmax(dim=1)
        total_correct += (preds == labels).sum().item()
        total_samples += labels.size(0)

    avg_loss = total_loss / len(dataloader)
    accuracy = total_correct / total_samples

    train_losses.append(avg_loss)
    train_accuracies.append(accuracy)

    print(f"Epoch {epoch+1}, Loss: {avg_loss:.4f}, Accuracy: {accuracy:.4f}")
    torch.save(model.state_dict(), f"saved_progress/mammo_vit_epoch{epoch+1:02}.pth")

# Plot Pentru Loss function si Accuracy
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(train_losses, marker='o')
plt.title("Training Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")

plt.subplot(1, 2, 2)
plt.plot(train_accuracies, marker='o', color='green')
plt.title("Training Accuracy")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")

plt.tight_layout()
plt.show()
plt.tight_layout()
plt.savefig("training_curves.png") 
plt.show()