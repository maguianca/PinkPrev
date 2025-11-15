import os
from PIL import Image
from torch.utils.data import Dataset

#Dataset definit prin denumirile fisierelor din datasetul cu denumirile fisierelor aferente 
#root_dir -> contine fisiere de tipul benign_cc, benign_mlo, malign_cc, malign_mlo
class MammogramDataset(Dataset):
    def __init__(self, root_dir, transform=None):
        self.root_dir = root_dir
        self.transform = transform
        self.samples = []

        for subdir in os.listdir(root_dir):
            label = 1 if "malign" in subdir.lower() else 0
            view = "cc" if "cc" in subdir.lower() else "mlo"
            full_path = os.path.join(root_dir, subdir)

            for fname in os.listdir(full_path):
                if fname.lower().endswith(('.png', '.jpg', '.jpeg')):
                    fpath = os.path.join(full_path, fname)
                    self.samples.append((fpath, label, view))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        fpath, label, view = self.samples[idx]
        image = Image.open(fpath).convert("RGB")

        if self.transform:
            image = self.transform(image)

        return image, label, fpath 
