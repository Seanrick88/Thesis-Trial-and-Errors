import cv2
import pytesseract
import numpy as np
import os

# Load EAST model
net = cv2.dnn.readNet('frozen_east_text_detection.pb')

# Read the image
image = cv2.imread('sample.jpg')
orig_image = image.copy()
height, width, _ = image.shape

# Prepare the image for EAST (convert to blob)
blob = cv2.dnn.blobFromImage(image, 1.0, (width, height), (123.68, 116.78, 103.94), True, crop=False)

# Run EAST text detector
net.setInput(blob)
scores, geometry = net.forward(['scores', 'geometry'])

# Decode the detections
boxes = []
confidences = []

for y in range(0, scores.shape[2]):
    for x in range(0, scores.shape[3]):
        score = scores[0, 0, y, x]
        if score > 0.5:  # threshold for confidence
            offset_x, offset_y, angle, width, height = geometry[0, :, y, x]
            end_x = int(x * 4 + offset_x)
            end_y = int(y * 4 + offset_y)
            start_x = int((x * 4) - width / 2)
            start_y = int((y * 4) - height / 2)
            boxes.append(((start_x, start_y), (end_x, end_y)))

# Crop the text regions and apply OCR
for box in boxes:
    start, end = box
    crop_img = orig_image[start[1]:end[1], start[0]:end[0]]  # Crop the detected region
    text = pytesseract.image_to_string(crop_img)  # Apply Tesseract OCR
    print("Detected Text: ", text)