
# initialization
from .sdd_config import NMS_THRESH
from .sdd_config import MIN_CONF
import numpy as np
import cv2

def detect_people(frame, net, ln, personIdx=0):
	# Grab frame and initialize
	(H, W) = frame.shape[:2]
	results = []

	# Make a Blob -> binary large object (?)
	blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
	net.setInput(blob)
	layerOutputs = net.forward(ln)

	boxes = []
	centroids = []
	confidences = []

	for output in layerOutputs:
		
		for detection in output:
			
			scores = detection[5:]
			classID = np.argmax(scores)
			confidence = scores[classID]

			# Check if it is a person and minimum confidence is met
			if classID == personIdx and confidence > MIN_CONF:

				box = detection[0:4] * np.array([W, H, W, H])
				(centerX, centerY, width, height) = box.astype("int")

				x = int(centerX - (width / 2))
				y = int(centerY - (height / 2))

				boxes.append([x, y, int(width), int(height)])
				centroids.append((centerX, centerY))
				confidences.append(float(confidence))

	# Applying Non-Maxima Suppression
	idxs = cv2.dnn.NMSBoxes(boxes, confidences,	MIN_CONF, NMS_THRESH)

	# At least one detected
	if len(idxs) > 0:
		# keep searching
		for i in idxs.flatten():
			# Extract bounding boxes coordinates
			(x, y) = (boxes[i][0], boxes[i][1])
			(w, h) = (boxes[i][2], boxes[i][3])

			#update results, isinya -> prediction prob, box coord, centroids
			r = (confidences[i], (x, y, x + w, y + h), centroids[i])
			results.append(r)

	return results
