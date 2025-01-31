import easyocr
import cv2

# Initialize EasyOCR reader for Spanish ('es') if you need the 'ñ' character
reader = easyocr.Reader(['es'])  # You can use ['en'] if you don't need Spanish support

# Specify a test image
image_path = 'C:\\THESIS\\sample_dataset\\enye_image_3891.png'

# Read the image with OpenCV
img = cv2.imread(image_path)

# Run OCR to detect text
result = reader.readtext(image_path)

# Print detected text
print("Detected text:", result)

# Show the image with OpenCV (annotated with text)
for (bbox, text, prob) in result:
    (top_left, top_right, bottom_right, bottom_left) = bbox
    top_left = tuple(map(int, top_left))
    bottom_right = tuple(map(int, bottom_right))
    cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 2)
    cv2.putText(img, text, (top_left[0], top_left[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

# Display the image with OpenCV
cv2.imshow("OCR Result", img)
cv2.waitKey(0)  # Wait for any key to close the window
cv2.destroyAllWindows()  # Close the window after a key press




