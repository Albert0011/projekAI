# USAGE
# python sdd_main.py --input pedestrians.mp4
# python sdd_main.py --input pedestrians.mp4 --output output2.avi --birdview birdview.avi
# import the necessary packages
from detect import sdd_config as config
from detect.detection import detect_people
from scipy.spatial import distance as dist
import numpy as np
import argparse
import imutils
import cv2
import os
import utills
import draw

mouse_pts = []

def get_mouse_points(event, x, y, flags, param):

    global mouse_pts
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(mouse_pts) < 4:
            cv2.circle(image, (x, y), 5, (0, 0, 255), 10)
        else:
            cv2.circle(image, (x, y), 5, (0, 255, 0), 10)
            
        if len(mouse_pts) >= 1 and len(mouse_pts) <= 3:
            cv2.line(image, (x, y), (mouse_pts[len(mouse_pts)-1][0], mouse_pts[len(mouse_pts)-1][1]), (70, 70, 70), 2)
            if len(mouse_pts) == 3:
                cv2.line(image, (x, y), (mouse_pts[0][0], mouse_pts[0][1]), (70, 70, 70), 2)
        
        if "mouse_pts" not in globals():
            mouse_pts = []
        mouse_pts.append((x, y))
        #print("Mouse detected")
        #print(mouse_pts)

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", type=str, default="",
	help="path to (optional) input video file")
ap.add_argument("-o", "--output", type=str, default="",
	help="path to (optional) output video file")
ap.add_argument("-v", "--birdview", type=str, default="birdview.avi",
	help="path to (optional) output video file")
ap.add_argument("-d", "--display", type=int, default=1,
	help="whether or not output frame should be displayed")
args = vars(ap.parse_args())

# load the COCO class labels our YOLO model was trained on
labelsPath = os.path.sep.join([config.MODEL_PATH, "coco.names"])
LABELS = open(labelsPath).read().strip().split("\n")

# derive the paths to the YOLO weights and model configuration
weightsPath = os.path.sep.join([config.MODEL_PATH, "yolov3.weights"])
configPath = os.path.sep.join([config.MODEL_PATH, "yolov3.cfg"])

# load our YOLO object detector trained on COCO dataset (80 classes)
print("[INFO] loading YOLO from disk...")
net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)


# determine only the *output* layer names that we need from YOLO
ln = net.getLayerNames()
ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]


# initialize the video stream and pointer to output video file
print("[INFO] accessing video stream...")
vs = cv2.VideoCapture(args["input"] if args["input"] else 0)
writer = None
writer2 = None

height2 = int(vs.get(cv2.CAP_PROP_FRAME_HEIGHT))
width2 = int(vs.get(cv2.CAP_PROP_FRAME_WIDTH))
scale_w, scale_h = utills.get_scale(width2, height2)

cv2.namedWindow("image")
cv2.setMouseCallback("image", get_mouse_points)

points = []
global image
count = 0


# loop over the frames from the video stream
while True:
	# read the next frame from the file
	(grabbed, frame) = vs.read()
	# kalau ga ada frame berarti selesai
	if not grabbed:
		print("ga kebaca")
		break
	# resize the frame and then detect people in it
	#print("ini awal banget bro2")
	frame = imutils.resize(frame, width=700)
	#results = detect_people(frame, net, ln,
		#personIdx=LABELS.index("person"))
	# initialize the set of indexes that violate the minimum distance
	violate = set()


	#detection
	# Grab frame and initialize
	personIdx=LABELS.index("person")

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
			if classID == personIdx and confidence > config.MIN_CONF:

				box = detection[0:4] * np.array([W, H, W, H])
				(centerX, centerY, width, height) = box.astype("int")

				x = int(centerX - (width / 2))
				y = int(centerY - (height / 2))

				boxes.append([x, y, int(width), int(height)])
				centroids.append((centerX, centerY))
				confidences.append(float(confidence))

	# Applying Non-Maxima Suppression
	idxs = cv2.dnn.NMSBoxes(boxes, confidences,	config.MIN_CONF, config.NMS_THRESH)

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
	#done detection

	#print("first check")
	if count == 0:
		#print("masuk sini")
		while True:
			image = frame
			cv2.imshow("image", image)
			cv2.waitKey(1)
			if len(mouse_pts) == 8:
				cv2.destroyWindow("image")
				break

		points = mouse_pts  

	# some settings after get mouse points
	#print("wtf how")
	# the first 4 points -> perspective
	src = np.float32(np.array(points[:4]))
	dst = np.float32([[0, H], [W, H], [W, 0], [0, 0]])
	perspective_transform = cv2.getPerspectiveTransform(src, dst)

	# using next 3 points for horizontal and vertical unit length(in this case 180 cm)
	pts = np.float32(np.array([points[4:7]]))
	warped_pt = cv2.perspectiveTransform(pts, perspective_transform)[0]

	distance_w = np.sqrt((warped_pt[0][0] - warped_pt[1][0]) ** 2 + (warped_pt[0][1] - warped_pt[1][1]) ** 2)
	distance_h = np.sqrt((warped_pt[0][0] - warped_pt[2][0]) ** 2 + (warped_pt[0][1] - warped_pt[2][1]) ** 2)
	pnts = np.array(points[:4], np.int32)
	cv2.polylines(frame, [pnts], True, (70, 70, 70), thickness=2)

	font = cv2.FONT_HERSHEY_PLAIN
	boxes1 = []
	for i in range(len(boxes)):
		if i in idxs:
			boxes1.append(boxes[i])
			x,y,w,h = boxes[i]

	if len(boxes1) == 0:
		count = count + 1
		continue

	# Here we will be using bottom center point of bounding box for all boxes and will transform all those
	# bottom center points to bird eye view
	person_points = utills.get_transformed_points(boxes1, perspective_transform)

	# Here we will calculate distance between transformed points(humans)
	distances_mat, bxs_mat = utills.get_distances(boxes1, person_points, distance_w, distance_h)
	risk_count = utills.get_count(distances_mat)

	frame1 = np.copy(frame)

	# Draw bird eye view and frame with bouding boxes around humans according to risk factor    
	bird_image = draw.bird_eye_view(frame, distances_mat, person_points, scale_w, scale_h, risk_count)
	img = draw.social_distancing_view(frame1, bxs_mat, boxes1, risk_count)

	# closing part
	count = count + 1
	if args["display"] > 0:
		# show the output frame
		cv2.imshow("birdImg",bird_image)
		cv2.imshow("frame",img)
		key = cv2.waitKey(1) & 0xFF
		# if the `q` key was pressed, break from the loop
		if key == ord("q"):
			break
	# if an output video file path has been supplied and the video
	# writer has not been initialized, do so now
	if args["output"] != "" and writer is None:
		# initialize our video writer
		fourcc = cv2.VideoWriter_fourcc(*"MJPG")
		writer = cv2.VideoWriter(args["output"], fourcc, 25,
			(img.shape[1], img.shape[0]), True)
	if args["output"] != "" and writer2 is None:
		fourcc2 = cv2.VideoWriter_fourcc(*"MJPG")
		writer2 = cv2.VideoWriter(args["birdview"], fourcc2, 25,
			(bird_image.shape[1], bird_image.shape[0]), True)


	# if the video writer is not None, write the frame to the output
	# video file
	if writer is not None:
		writer.write(img)
	if writer2 is not None:
		writer2.write(bird_image)

cv2.destroyAllWindows()