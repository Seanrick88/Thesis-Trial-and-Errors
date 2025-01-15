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

# Background types
background_types = ["plain", "textured", "noisy"]

def create_textured_background(image_size):
    """Generate a textured background."""
    texture = Image.new("RGB", image_size, color=(200, 200, 200))  # Light gray background
    draw = ImageDraw.Draw(texture)
    for _ in range(100):  # Add random lines as texture
        x1, y1 = random.randint(0, image_size[0]), random.randint(0, image_size[1])
        x2, y2 = random.randint(0, image_size[0]), random.randint(0, image_size[1])
        draw.line((x1, y1, x2, y2), fill=(150, 150, 150), width=1)
    return texture

def create_noisy_background(image_size):
    """Generate a noisy background."""
    noise = Image.new("RGB", image_size, color=(255, 255, 255))
    pixels = noise.load()
    for x in range(image_size[0]):
        for y in range(image_size[1]):
            noise_value = random.randint(200, 255)
            pixels[x, y] = (noise_value, noise_value, noise_value)
    return noise

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

        
        # Create a background image
        background_type = random.choice(background_types)
        if background_type == "plain":
            img = Image.new("RGB", image_size, color=(255, 255, 255))  # Plain white
        elif background_type == "textured":
            img = create_textured_background(image_size)
        elif background_type == "noisy":
            img = create_noisy_background(image_size)

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
