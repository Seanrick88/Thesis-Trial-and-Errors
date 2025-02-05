import lmdb
import cv2
import numpy as np
import os
from PIL import Image

def check_lmdb_samples(lmdb_path, num_samples=5):
    # Open LMDB database
    env = lmdb.open(lmdb_path, readonly=True, lock=False)
    with env.begin() as txn:
        num_samples = min(num_samples, int(txn.get("num-samples".encode())))
        print(f"Total samples in LMDB: {num_samples}")

        for i in range(1, num_samples + 1):  # LMDB keys start from 1
            img_key = f'image-{i:09d}'.encode()
            label_key = f'label-{i:09d}'.encode()

            img_data = txn.get(img_key)
            label = txn.get(label_key).decode()

            if img_data:
                # Convert binary data to image
                img = cv2.imdecode(np.frombuffer(img_data, np.uint8), cv2.IMREAD_COLOR)
                img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

                # Show image and label
                img.show(title=f"Label: {label}")
                print(f"Sample {i}: {label}")

check_lmdb_samples("lmdb_output", num_samples=10)
