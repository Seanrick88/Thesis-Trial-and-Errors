# USAGE
# python easyocr_with_box.py -i image1.jpg

# import necessary packages
import cv2
import easyocr
import argparse

# construct the argument parser
ap = argparse.ArgumentParser()

# determine the languages to be read
reader = easyocr.Reader(['en', 'tl', 'es'])

# load image
img = cv2.imread("test2.PNG")

# convert to text; detail = 0: simple output (just the text); detail = 1: return with details
results = reader.readtext(img, detail = 1)

# bounding boxes
# bbox: bounding boxes coordinates
# txt: recognized text
# prob: confidence lvl
for (bbox, txt, prob) in results:
	tl, tr, br, bl = bbox
	'''
		tl: top-left coordinate
		tr: top-right coordinate
		br: bottom-right coordinate
		bl: bottom-left coordinate
	'''
	tl = (int(tl[0])), (int(tl[1]))
	tr = (int(tr[0])), (int(tr[1]))
	br = (int(br[0])), (int(br[1]))
	bl = (int(bl[0])), (int(bl[1]))

	# remove non-ASCII characters
	# for each character in txt, get the ASCII code and if it is less than 128, replace with ""
	txt = "".join([c if ord(c) < 128 else "" for c in txt]).strip()

	# boxes and words
	cv2.rectangle(img, tl, br, (0, 255, 0), 2)
	cv2.putText(img, txt, (tl[0], tl[1]), cv2.FONT_HERSHEY_DUPLEX, 1.2, (255, 35, 35), 2)


# display 
cv2.imshow("EasyOCR", img)
cv2.waitKey(0)