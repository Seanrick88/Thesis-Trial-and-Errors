import os
import lmdb
import cv2
import shutil
from tqdm import tqdm

def check_image_is_valid(image_path):
    """Check if the image is valid and readable."""
    try:
        img = cv2.imread(image_path)
        if img is None:
            print(f"Invalid image: {image_path}")
            return False
    except Exception as e:
        print(f"Error reading image {image_path}: {e}")
        return False
    return True

def write_cache(env, cache):
    """Write data to LMDB."""
    with env.begin(write=True) as txn:
        for k, v in cache.items():
            txn.put(k.encode(), v)

def create_lmdb_dataset(output_path, image_label_list, check_valid=True):
    """
    Create LMDB dataset.

    Parameters:
        output_path (str): Path to save the LMDB database.
        image_label_list (list): List of tuples (image_path, label).
        check_valid (bool): Check if images are valid before processing.
    """
    # Remove the existing LMDB folder if present
    if os.path.exists(output_path):
        print(f"Output path {output_path} already exists. Removing it...")
        shutil.rmtree(output_path)  # Remove the existing directory

    os.makedirs(output_path, exist_ok=True)

    env = lmdb.open(output_path, map_size=5 * 1024 * 1024 * 1024)  # 1TB
    cache = {}
    cnt = 1

    # Loop through the list of image-label pairs
    for image_path, label in tqdm(image_label_list, desc="Processing images"):
        print(f"Processing image: {image_path}")  # Debugging print
        
        # Check if the image exists
        if not os.path.exists(image_path):
            print(f"Image not found: {image_path}")
            continue

        # Check if the image is valid
        if check_valid and not check_image_is_valid(image_path):
            print(f"Invalid image skipped: {image_path}")
            continue

        # Read the image in binary format
        with open(image_path, "rb") as f:
            image_bin = f.read()

        # Assign keys for the image and label in the LMDB
        image_key = f"image-{cnt:09d}"
        label_key = f"label-{cnt:09d}"

        # Add the image and label data to the cache
        cache[image_key] = image_bin
        cache[label_key] = label.encode()

        # Write to the LMDB every 1000 images to optimize performance
        if cnt % 1000 == 0:  
            write_cache(env, cache)
            cache = {}
            print(f"Processed {cnt} images.")

        cnt += 1

    # Write any remaining data to LMDB
    if cache:
        write_cache(env, cache)

    # Store the number of samples in the metadata
    num_samples = cnt - 1
    with env.begin(write=True) as txn:
        txn.put("num-samples".encode(), str(num_samples).encode())

    print(f"Created LMDB dataset with {num_samples} samples.")
    env.close()

# Define paths
dataset_folder = "E:/THESIS/merged_dataset"
output_lmdb_base_path = os.path.join(dataset_folder, "lmdb_dataset")  # Base LMDB output path within the dataset folder

# Paths for the train, validation, and test sets
train_label_file = os.path.join(dataset_folder, "train.txt")
val_label_file = os.path.join(dataset_folder, "val.txt")
test_label_file = os.path.join(dataset_folder, "test.txt")

# Function to read the dataset from a text file
def read_label_file(label_file_path):
    image_label_list = []
    with open(label_file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line:
                image_path, label = line.split(" ", 1)
                image_label_list.append((image_path, label))
    return image_label_list

# Read the image-label pairs for each split
train_data = read_label_file(train_label_file)
val_data = read_label_file(val_label_file)
test_data = read_label_file(test_label_file)

# LMDB paths for training, validation, and test sets
train_lmdb_path = os.path.join(output_lmdb_base_path, "train")
val_lmdb_path = os.path.join(output_lmdb_base_path, "val")
test_lmdb_path = os.path.join(output_lmdb_base_path, "test")

# Create LMDB datasets for each split
print("Creating training LMDB...")
create_lmdb_dataset(train_lmdb_path, train_data)

print("Creating validation LMDB...")
create_lmdb_dataset(val_lmdb_path, val_data)

print("Creating testing LMDB...")
create_lmdb_dataset(test_lmdb_path, test_data)

print("All LMDB datasets created successfully!")
