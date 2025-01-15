from PIL import Image, ImageDraw, ImageFont
import os
import random
import csv

# Directory to save the generated images
output_dir = "dataset_with_enye"
os.makedirs(output_dir, exist_ok=True)

# List of sample words or phrases containing "Ñ"
words_with_enye = [
    "Piña", "Niño", "Niña", "Señor", "Señora", "bañeras", 
    "biñan", "piñata", "Señor", "Doña", "castañas", "Español",
    "caviteño", "iñigo" , "dasmariñas" , "parañaque" , "peñafrancia"
]

# Fonts 
fonts = [
    "arial.ttf",
    "verdana.ttf",
    "times.ttf",
    "georgia.ttf",
    "tahoma.ttf",
    "calibri.ttf",
    "couri.ttf"
]

sizes = [
    12,
    16,
    18,
    20,
    22,
    24,
    28,
    30,
    36
]

# Image dimensions and font size
image_size = (300, 100)  # (width, height)

# Create and open a CSV file for storing image paths and labels
csv_file_path = os.path.join(output_dir, "image_labels.csv")
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Image Path", "Text Label"])  # Write the CSV header
    
    # Generate the dataset
    num_samples = 50
    for i in range(num_samples):
        # Randomly select a word or phrase
        text = random.choice(words_with_enye)

        #randomizer keme keme
        font_path = random.choice(fonts)
        font_size = random.choice(sizes)
        # Load the font
        try:
            font = ImageFont.truetype(font_path, font_size)
        except OSError:
            print("Font not found!")
            font = ImageFont.load_default()

        
        # Create a blank white image
        img = Image.new("RGB", image_size, color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        
        # Calculate text position (center the text)
        text_bbox = draw.textbbox((0, 0), text, font=font)  # Get the bounding box
        text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
        position = ((image_size[0] - text_width) // 2, (image_size[1] - text_height) // 2)
        
        # Draw the text on the image
        draw.text(position, text, fill=(0, 0, 0), font=font)
        
        # Save the image
        image_filename = f"enye_image_{i + 1}.png"
        image_path = os.path.join(output_dir, image_filename)
        img.save(image_path)
        
        # Write image path and text label to the CSV file
        writer.writerow([image_path, text])

print(f"Dataset created with {num_samples} images in '{output_dir}' and saved labels to '{csv_file_path}'")
