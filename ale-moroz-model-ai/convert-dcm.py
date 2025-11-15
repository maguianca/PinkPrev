import os
import cv2
import pydicom
import numpy as np
from pathlib import Path

# Calea către folderul original cu .dcm
input_dir = Path('../dataINbreast/CC')
# Folderul unde salvăm imaginile convertite
output_dir = Path('../dataINbreast/CC-converted')

for class_name in os.listdir(input_dir):
    class_path = input_dir / class_name
    if not class_path.is_dir():
        continue

    out_class_path = output_dir / class_name
    out_class_path.mkdir(parents=True, exist_ok=True)

    for i, filename in enumerate(os.listdir(class_path)):
        if not filename.lower().endswith('.dcm'):
            continue

        dicom_path = class_path / filename
        ds = pydicom.dcmread(dicom_path)
        img = ds.pixel_array

        img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

        # Convertire la 3 canale dacă e necesar (ViT așteaptă 3 canale RGB)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

        # Salvare ca PNG
        out_path = out_class_path / f"{class_name}_{i}.png"
        cv2.imwrite(str(out_path), img_rgb)