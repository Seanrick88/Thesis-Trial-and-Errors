# USAGE
# python normal_OCR.py -i image1.jpg

# import necessary packages
import cv2
import pytesseract
from pytesseract import Output
import argparse

def video_processing(img_array):
	results = pytesseract.image_to_data(img_array, output_type = Output.DICT)

	# loop
	for i in range(0, len(results["text"])):
		txt = results["text"][i]
		conf = int(results["conf"][i])
		# coordinates
		x, y, w, h = (results["left"][i], results["top"][i], results["width"][i], results["height"][i])

		if conf > 90 and txt.strip():
			print("Confidence: " + str(conf))
			print("Text: " + txt)
			print("")

			# remove non-ASCII characters
			txt = "".join(txt).strip()
			# bounding rectangle per word
			cv2.rectangle(img_array, (x, y), (x + w, y + h), (20, 255, 57), 2)
			# place text
			cv2.putText(img_array, txt, (x, y - 10), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 35, 35), 2)
	return img_array

def main_program():
	# open camera; 0 - main cam, 1 - 2nd cam
	cam = cv2.VideoCapture(0)

	# check camera status
	while True:
		if cam.read()[0] == False:
			print("Camera is not connected / cannot be detected")
			break
		else:
			# ret: boolean to check if frame is successfully captured
			# img_array: captured frame 
			ret, img_array = cam.read()
			processed_frame = video_processing(img_array)
			cv2.imshow('Camera', processed_frame)
			if cv2.waitKey(1) & 0xff == ord('q'): # wait for keypress for 1 ms
				break
	cam.release()
	cv2.destroyAllWindows()

main_program()