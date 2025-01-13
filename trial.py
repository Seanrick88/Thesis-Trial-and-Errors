import cv2

# Load EAST model
net = cv2.dnn.readNet('frozen_east_text_detection.pb')

# Print layer names to check correct names
layer_names = net.getLayerNames()
print("Layer names:", layer_names)