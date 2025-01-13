# USAGE
# python normal_OCR.py -i image1.jpg

# import necessary packages
import cv2
import easyocr
import argparse


# construct the argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the Input Image")
args = vars(ap.parse_args())

# determine the languages to be read
reader = easyocr.Reader(['en', 'tl'])

# load image
image = cv2.imread(args["image"])

# convert to text
txt = reader.readtext(image, detail = 0)

# display text
print(txt)
