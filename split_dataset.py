import os
from sklearn.model_selection import train_test_split

def read_label_file(label_file_path):
    """Read the label file and prepare image-label pairs."""
    image_label_list = []
    with open(label_file_path, "r", encoding = "utf-8") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line:
                # Assuming each line is "image_path label"
                image_path, label = line.split(" ", 1)
                image_label_list.append((image_path, label))
    return image_label_list

def split_data_by_category(image_label_pairs, split_ratios):
    """Split the dataset into train, validation, and test based on the category of the text."""
    # Split normal text and enye text into separate lists
    normal_data = [pair for pair in image_label_pairs if "ñ" not in pair[1]]
    enye_data = [pair for pair in image_label_pairs if "ñ" in pair[1]]

    # Split each category into training, validation, and test sets
    normal_train, normal_temp = train_test_split(normal_data, test_size=(1 - split_ratios['train']), random_state=42)
    normal_val, normal_test = train_test_split(normal_temp, test_size=(split_ratios['test'] / (split_ratios['val'] + split_ratios['test'])), random_state=42)

    enye_train, enye_temp = train_test_split(enye_data, test_size=(1 - split_ratios['train']), random_state=42)
    enye_val, enye_test = train_test_split(enye_temp, test_size=(split_ratios['test'] / (split_ratios['val'] + split_ratios['test'])), random_state=42)

    # Combine the splits from both categories
    train_data = normal_train + enye_train
    val_data = normal_val + enye_val
    test_data = normal_test + enye_test

    return train_data, val_data, test_data

def save_split_data(data, output_file):
    """Save split data into a text file."""
    with open(output_file, "w", encoding= "utf-8") as f:
        for image_path, label in data:
            f.write(f"{image_path} {label}\n")

# Define paths
dataset_folder = "E:/THESIS/merged_dataset"
label_file_path = os.path.join(dataset_folder, "merged_dataset.txt")

# Read image-label pairs from the label file
image_label_pairs = read_label_file(label_file_path)

# Define split ratios for training, validation, and test
split_ratios = {
    'train': 0.8,
    'val': 0.1,
    'test': 0.1
}

# Split the data into train, validation, and test sets
train_data, val_data, test_data = split_data_by_category(image_label_pairs, split_ratios)

# Save the split data into text files
save_split_data(train_data, os.path.join(dataset_folder, "train.txt"))
save_split_data(val_data, os.path.join(dataset_folder, "val.txt"))
save_split_data(test_data, os.path.join(dataset_folder, "test.txt"))

print("Dataset split completed and saved.")
