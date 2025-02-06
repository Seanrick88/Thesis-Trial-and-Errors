from PIL import Image
import os

def convert_images_to_png(input_folder):
    # Iterate through all files in the input folder and subfolders
    for root, dirs, files in os.walk(input_folder):
        for filename in files:
            if filename.endswith('.jpg'):
                jpg_path = os.path.join(root, filename)
                png_path = os.path.join(root, filename.replace('.jpg', '.png'))
                
                # Open the .jpg image and save it as .png
                with Image.open(jpg_path) as img:
                    img.save(png_path, 'PNG')
                
                print(f"Converted {jpg_path} to {png_path}")
                # Optionally, delete the original .jpg image after conversion
                os.remove(jpg_path)
            elif filename.endswith('.png'):
                print(f"Skipping {filename}, already in PNG format")

# Example usage
output_folder = 'E:\\THESIS\\whole dataset\\output'  # Folder containing train, test, and val with images

# Call the function for all three folders
convert_images_to_png(os.path.join(output_folder, 'train'))
convert_images_to_png(os.path.join(output_folder, 'test'))
convert_images_to_png(os.path.join(output_folder, 'val'))
