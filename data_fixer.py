# Open the label file and create a new fixed version
input_file = "sample_dataset/sample_dataset.txt"  # Replace with your actual file name
output_file = "labels.txt"  # New file with corrected labels

with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
    for line in infile:
        # Remove "sample_dataset/" from the beginning of each line
        fixed_line = line.replace("sample_dataset/", "", 1)
        outfile.write(fixed_line)

print("✅ Label file fixed! Saved as:", output_file)
