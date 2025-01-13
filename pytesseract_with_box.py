# USAGE
# python pytesseract_with_box.py -i image1.jpg

# import necessary packages
import cv2
import pytesseract
from pytesseract import Output
import argparse

# construct the argument parser
ap = argparse.ArgumentParser()
args = vars(ap.parse_args())

# load image
image = cv2.imread("E:\THESIS\sample.jpg")
rgb_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# draw box and display text
imageBox = pytesseract.image_to_data(rgb_img, output_type = Output.DICT)

# loop 
for i in range(0, len(imageBox["text"])):
	# coordinates
	x, y, w, h = (imageBox["left"][i], imageBox["top"][i], imageBox["width"][i], imageBox["height"][i])
	txt = imageBox["text"][i]
	confidence = int(imageBox["conf"][i])

	if confidence > 95:
		print("Confidence: " + str(confidence))
		print("Text: " + txt)
		print("")

		# remove non-ASCII characters
		txt = "".join(txt).strip()
		# bounding rectangle per word
		cv2.rectangle(image, (x, y), (x + w, y + h), (20, 255, 57), 3)
		# place text
		cv2.putText(image, txt, (x, y - 10), cv2.FONT_HERSHEY_DUPLEX, 1.2, (255, 35, 35), 2)

# display output
cv2.imshow("Image", image)
cv2.waitKey(0)
