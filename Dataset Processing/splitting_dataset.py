import os
import shutil
import random

def split_images(src_folder, dest_folder, num_images=1500, train_ratio=0.8, test_ratio=0.1, val_ratio=0.1):
    # Ensure the ratios sum to 1
    assert train_ratio + test_ratio + val_ratio == 1, "Ratios must sum to 1."

    # Create destination folders for train, test, and val if they don't exist
    train_folder = os.path.join(dest_folder, "train")
    test_folder = os.path.join(dest_folder, "test")
    val_folder = os.path.join(dest_folder, "val")

    os.makedirs(train_folder, exist_ok=True)
    os.makedirs(test_folder, exist_ok=True)
    os.makedirs(val_folder, exist_ok=True)

    # Get all image files in the source folder
    all_images = [img for img in os.listdir(src_folder) if img.endswith(('.jpg', '.png'))]

    # Randomly select 'num_images' images from the folder
    selected_images = random.sample(all_images, num_images)

    # Split the selected images based on the provided ratios
    num_train = int(num_images * train_ratio)
    num_test = int(num_images * test_ratio)
    num_val = num_images - num_train - num_test  # Remaining images go to validation

    # Move images to respective folders
    for i, img_file in enumerate(selected_images):
        src_img_path = os.path.join(src_folder, img_file)

        if i < num_train:
            dest_img_path = os.path.join(train_folder, img_file)
        elif i < num_train + num_test:
            dest_img_path = os.path.join(test_folder, img_file)
        else:
            dest_img_path = os.path.join(val_folder, img_file)

        # Move the image
        shutil.move(src_img_path, dest_img_path)

        # Also move the corresponding label file (assuming label file is in the same format and same location)
        label_file = img_file.replace('.jpg', '.txt').replace('.png', '.txt')
        src_label_path = os.path.join(src_folder, label_file)
        
        if os.path.exists(src_label_path):
            shutil.move(src_label_path, os.path.join(os.path.dirname(dest_img_path), label_file))

# Define source and destination folders
src_folder = "E:\\THESIS\\whole dataset\\IAM\\image"  # Folder containing the images
dest_folder = "E:\\THESIS\\whole dataset\\output"

split_images(src_folder, dest_folder)