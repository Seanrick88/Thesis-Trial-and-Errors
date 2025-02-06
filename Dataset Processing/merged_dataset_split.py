import os
import shutil
import random

def split_images(src_folder, dest_folder, num_printed=1500, num_enye=1500, train_ratio=0.8, test_ratio=0.1, val_ratio=0.1):
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

    # Separate printed text images (those not containing 'enye_image')
    printed_images = [img for img in all_images if 'enye_image' not in img]
    # Separate enye images (those containing 'enye_image')
    enye_images = [img for img in all_images if 'enye_image' in img]

    # Randomly select 'num_printed' and 'num_enye' images
    selected_printed_images = random.sample(printed_images, num_printed)
    selected_enye_images = random.sample(enye_images, num_enye)

    # Combine the selected printed and enye images
    selected_images = selected_printed_images + selected_enye_images

    # Split the selected images based on the provided ratios
    num_images = num_printed + num_enye  # Total selected images
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

# Define source and destination folders
src_folder = "E:\\THESIS\\whole dataset\\merged_dataset"  # Folder containing the images (printed and enye)
dest_folder = "E:\\THESIS\\whole dataset\\output"  # Folder where you want to save train, test, val data

# Call the function to split and move the images
split_images(src_folder, dest_folder)
