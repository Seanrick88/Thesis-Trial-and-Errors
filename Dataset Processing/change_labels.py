import os
import random


def convert_gt_annotations_to_png(input_file, output_file):
    # Open the input file to read the annotations
    with open(input_file, 'r', encoding='utf-8') as infile:
        # Read all lines from the file
        lines = infile.readlines()

    # Open the output file to write the modified annotations
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for line in lines:
            # Replace .jpg with .png in the image path
            modified_line = line.replace('.jpg', '.png')
            # Write the modified line to the output file
            outfile.write(modified_line)

    print(f"Annotations from {input_file} have been converted and saved to {output_file}")

# Example usage
input_gt_file = 'E:\\THESIS\\whole dataset\\IAM\\formatted_gt_test.txt'  # Input annotation file with .jpg
output_gt_file = 'E:\\THESIS\\whole dataset\\IAM\\gt_test_modified.txt'  # Output file with .png




def format_annotations(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            line = line.strip()
            # Split by the first whitespace (tab or space)
            parts = line.split(maxsplit=1)
            if len(parts) == 2:
                image_path, label = parts
                # Write the formatted line with a single space between the image and the label
                outfile.write(f"{image_path} {label}\n")

# Define file paths
input_file = 'E:\\THESIS\\whole dataset\\IAM\\gt_test.txt'  # Your original annotation file
output_file = 'E:\\THESIS\\whole dataset\\IAM\\gt_test_modified.txt'  # Output file with formatted annotations


def generate_train_val_test_txt_from_folders_and_annotations(image_folders, annotations_file1, annotations_file2, output_dir):
    # Read the annotations from both files into dictionaries
    annotations = {}

    def process_file(file_path):
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                # Split by any whitespace (space) into image path and label
                if line:
                    parts = line.split(maxsplit=1)
                    if len(parts) == 2:
                        image_path, label = parts
                        annotations[image_path] = label

    # Process both annotation files
    process_file(annotations_file1)
    process_file(annotations_file2)

    # Initialize lists to hold the image names and labels for train, test, and val
    train_images = []
    test_images = []
    val_images = []

    # Go through the folders and match images with their annotations
    for folder_name, folder_path in image_folders.items():
        for image_name in os.listdir(folder_path):
            image_path = image_name
            if image_path in annotations:
                label = annotations[image_path]
                if folder_name == 'train':
                    train_images.append(f"{image_path} {label}")
                elif folder_name == 'test':
                    test_images.append(f"{image_path} {label}")
                elif folder_name == 'val':
                    val_images.append(f"{image_path} {label}")

    # Write the train, test, and val annotations to respective text files
    with open(os.path.join(output_dir, "train.txt"), 'w') as f:
        f.write('\n'.join(train_images))

    with open(os.path.join(output_dir, "test.txt"), 'w') as f:
        f.write('\n'.join(test_images))

    with open(os.path.join(output_dir, "val.txt"), 'w') as f:
        f.write('\n'.join(val_images))

# Define paths
image_folders = {
    'train': 'E:\\THESIS\\whole dataset\\output\\train',
    'test': 'E:\\THESIS\\whole dataset\\output\\test',
    'val': 'E:\\THESIS\\whole dataset\\output\\val'
}
annotations_file1 = 'E:\\THESIS\\whole dataset\\IAM\\gt_test_modified.txt'  # First processed annotation file
annotations_file2 = 'E:\\THESIS\\whole dataset\\merged_dataset\\formatted_dataset.txt'  # Second processed annotation file
output_dir = 'E:\\THESIS\\whole dataset\\output'  # Folder where the train.txt, test.txt, val.txt will be saved

# Call the function to generate train.txt, test.txt, val.txt
generate_train_val_test_txt_from_folders_and_annotations(image_folders, annotations_file1, annotations_file2, output_dir)



