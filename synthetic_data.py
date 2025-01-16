from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import random
import csv
import math

# Directory to save the generated images
output_dir = "ñ_dataset"
os.makedirs(output_dir, exist_ok=True)

# List of sample words or phrases containing "Ñ"
words_with_enye = [
    "Acuña", "Alfonso Castañeda", "Año", "Añonuevo", "Arañas", "Avanceña", "Avendaño", "Azaña",
    "Bañaga", "Batangueña", "Batangueño", "Biñan", "Bolaños", "boñgang arao", "Cañedo", "Cañeso",
    "Cañete", "Cardiño", "Cariño", "cariñosa", "Castañeda", "Cedeño", "Cendaña", "Dasmariñas",
    "dela Peña", "Dela Peña", "Diño", "Doña Remedios Trinidad", "Dueñas", "El Niño", "eñe",
    "Escaño", "España", "Fandiño", "Fariñas", "Godiñez", "Ibañez", "Iñigo", "Iñiguez", 
    "La Niña", "La Viña", "Lapeña", "Las Piñas", "Laviña", "Los Baños", "Malacañang", 
    "Mañalac", "Maño", "Mariñas", "Mendez-Nuñez", "Montañez", "Montaño", "Muñoz", "Nuñez", 
    "ñu", "Oñate", "Opeña", "Ordoñez", "Osmeña", "Pacaña", "Parañaque", "Pareño", 
    "Parreño", "Patiño", "Peñaflor", "Peñaflorida", "Peñalosa", "Peñaranda", "Peñarrubia", 
    "Piñol", "Piñon", "Quiñones", "Reaño", "Riñon", "Roño", "Sagñay", "Saldaña", 
    "Santo Niño", "Semaña", "Señeres", "señor", "Sobrepeña", "Sofronio Española", "Tañada", 
    "Tañong", "Tayabeña", "Tayabeño", "Teñoso", "Traqueña", "Triviño", "Villaseñor", 
    "Viñas", "Ybañez", "Yñiguez", "Zamboangueña", "Zamboangueño", "Zuñiga", "ñ"

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
    14,
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
image_size = (300, 200)  # (width, height)

# Background types
background_types = ["plain", "textured", "noisy"]

# Creation of textured background function
def create_textured_background(image_size):
    """Generate a textured background."""
    texture = Image.new("RGB", image_size, color=(200, 200, 200))  
    draw = ImageDraw.Draw(texture)
    for _ in range(100):  # Add random lines as texture
        x1, y1 = random.randint(0, image_size[0]), random.randint(0, image_size[1])
        x2, y2 = random.randint(0, image_size[0]), random.randint(0, image_size[1])
        draw.line((x1, y1, x2, y2), fill=(150, 150, 150), width=1)
    return texture

# Creation of noisy background function
def create_noisy_background(image_size):
    """Generate a noisy background."""
    noise = Image.new("RGB", image_size, color=(255, 255, 255))
    pixels = noise.load()
    for x in range(image_size[0]):
        for y in range(image_size[1]):
            noise_value = random.randint(200, 255)
            pixels[x, y] = (noise_value, noise_value, noise_value)
    return noise

# Creation of the Plain text with no variation
def plain_text(draw, text, font, image_width, image_height):
    text_bbox = draw.textbbox((0, 0), text, font = font)
    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
    position = ((image_width - text_width) // 2, (image_height - text_height) // 2)
    draw.text(position, text, fill=(0, 0, 0), font=font)

#Creation of the Wavy text
def wavy_text(draw, text, font, image_width, image_height):
    """Draw text in a wavy pattern."""
    amplitude = random.randint(3, 7)  # Wave height
    frequency = random.uniform(0.1, 0.3)  # Wave frequency
    # Use font.getbbox() to get the bounding box of each character
    total_width = sum(draw.textbbox((0, 0), char, font=font)[2] - draw.textbbox((0, 0), char, font=font)[0] for char in text)
    x_offset = (image_width - total_width) // 2
    y_offset = image_height // 2

    current_x = x_offset
    for i, char in enumerate(text):
        bbox = draw.textbbox((0, 0), char, font=font)  # Get the bounding box of the character
        char_width = bbox[2] - bbox[0]  # Calculate the character width from the bbox
        y_pos = y_offset + int(amplitude * math.sin(frequency * current_x))
        draw.text((current_x, y_pos), char, font=font, fill=(0, 0, 0))
        current_x += char_width + 2.5 # Update x position for the next character
        
#Creation of the Wavy text
def skewed_text(draw, text, font, image_width, image_height):
    skew_amount = random.uniform(0.02, 0.05)  # Random skew value 
    # total width of the text
    total_width = sum(draw.textbbox((0, 0), char, font=font)[2] - draw.textbbox((0, 0), char, font=font)[0] for char in text)
    x_offset = (image_width - total_width) // 2
    y_offset = image_height // 2

    current_x = x_offset
    for i, char in enumerate(text):
        bbox = draw.textbbox((0, 0), char, font=font)  # Get the bounding box of the character
        char_width = bbox[2] - bbox[0]  # Calculate the character width from the bbox
        
        # Apply skew by modifying the x position with a random skew factor
        skewed_x = current_x + int(random.uniform(-skew_amount, skew_amount) * current_x)
        
        draw.text((skewed_x, y_offset), char, font=font, fill=(0, 0, 0))
        current_x += char_width  # Update x position for the next character
        

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
        
        # Random style
        text_style = random.random()
        if text_style < 0.33:
            plain_text(draw, text, font, image_size[0], image_size[1])
        elif text_style < 0.66:
            wavy_text(draw, text, font, image_size[0], image_size[1])
        else:
            skewed_text(draw, text, font, image_size[0], image_size[1])


        # Random Blurring 
        blurring = random.random()
        if blurring < 0.3:
            img = img.filter(ImageFilter.GaussianBlur(radius=random.uniform(0.5,1.5)))
        elif blurring < 0.50:
            img = img.filter(ImageFilter.GaussianBlur(radius=random.uniform(1,2)))
        


        # Save the image
        image_filename = f"enye_image_{i + 1}.png"
        image_path = os.path.join(output_dir, image_filename)
        img.save(image_path)
        
        # Write image path and text label to the CSV file
        writer.writerow([image_path, text])

print(f"Dataset created with {num_samples} images in '{output_dir}' and saved labels to '{csv_file_path}'")
